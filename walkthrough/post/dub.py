#!/usr/bin/env python3
"""Dub a rendered take: voice acting + the game's own soundtrack.

Takes the film from render.py and produces production.mp4:
  - voice acting: every dialog line the performer observed is rendered
    with piper-tts (en_US-lessac-medium — flat, measured delivery; see
    docs/research/NARRATION.md for the deadpan style rationale) and run
    through the robot-FX chain from docs/research/AUDIO.md, which both
    fits Sprocket's character and hides TTS seams
  - music/SFX bed: the take's game-audio.webm — the REAL browser audio
    (OPL theme + synthesized effects) captured by the driver's
    MediaRecorder tap during the take, so it is sample-aligned with
    what's on screen
  - mix: each voice clip lands at its line's timestamp (time-compressed
    up to 1.3x if it overruns its slot), the bed ducks under the voice
    via sidechain compression

Usage: dub.py <take-dir>
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile

VOICE = "en_US-lessac-medium"
VOICE_DATA = os.path.expanduser("~/.local/share/piper-voices")
CACHE = os.path.expanduser("~/.cache/clankey-voices")
MAX_TEMPO = 1.3
BED_LEVEL = 0.85
VOX_LEVEL = 1.0

# ring-mod-lite robotization: keeps intelligibility, adds servo
ROBOT_FX = ("highpass=f=120,lowpass=f=6200,"
            "tremolo=f=30:d=0.42,"
            "acrusher=bits=10:mode=log:mix=0.2,"
            "silenceremove=start_periods=1:start_threshold=-45dB,"
            "areverse,silenceremove=start_periods=1:start_threshold=-45dB,"
            "areverse,"
            "loudnorm=I=-17:TP=-1.5,"
            "aformat=sample_rates=48000:channel_layouts=mono")


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def dur_of(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", path]).stdout.decode().strip()
    return float(out)


def speak(text):
    """Render one robotized line, cached by content hash."""
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(f"{VOICE}|{ROBOT_FX}|{text}".encode()).hexdigest()[:16]
    fx = os.path.join(CACHE, f"{key}.wav")
    if not os.path.exists(fx):
        raw = os.path.join(CACHE, f"{key}-raw.wav")
        run([sys.executable, "-m", "piper", "--data-dir", VOICE_DATA,
             "-m", VOICE, "-f", raw], input=text.encode())
        run(["ffmpeg", "-y", "-i", raw, "-af", ROBOT_FX, fx])
        os.unlink(raw)
    return fx


def main():
    take = sys.argv[1].rstrip("/")
    with open(os.path.join(take, "timeline.json")) as f:
        events = json.load(f)["events"]
    with open(os.path.join(take, "render.json")) as f:
        edit = json.load(f)

    film = os.path.join(take, "walkthrough.mp4")
    bed_src = os.path.join(take, "game-audio.webm")
    trim, card = edit["trim_start"], edit["card_sec"]
    film_dur = dur_of(film)

    def film_t(t):
        return t - trim + card

    audio_start = next(e["t"] for e in events if e["type"] == "audio_start")
    lines = [e for e in events
             if e["type"] == "line_start" and e.get("text")
             and e["text"].strip(". ")]

    # --- render voices, fit each to its slot --------------------------------
    clips = []   # (path, film_time)
    tmp = tempfile.mkdtemp(prefix="clankey-dub-")
    for i, e in enumerate(lines):
        wav = speak(e["text"])
        t = film_t(e["t"])
        slot = (film_t(lines[i + 1]["t"]) - 0.25 if i + 1 < len(lines)
                else film_dur - card) - t
        d = dur_of(wav)
        if d > slot > 0:
            tempo = min(MAX_TEMPO, d / slot)
            fitted = os.path.join(tmp, f"line{i:02d}.wav")
            run(["ffmpeg", "-y", "-i", wav, "-af", f"atempo={tempo:.3f}",
                 fitted])
            wav = fitted
            if d / slot > MAX_TEMPO:
                print(f"  note: line {i} overruns its slot even at "
                      f"{MAX_TEMPO}x ({d:.1f}s into {slot:.1f}s)")
        clips.append((wav, t))
        print(f"  {t:7.2f}s  {e['text'][:60]}")

    # --- the mix -------------------------------------------------------------
    # bed: skip what happened before the film starts, land at the card end
    bed_skip = max(0.0, trim - audio_start)
    bed_at = card + max(0.0, audio_start - trim)

    inputs = ["-i", film, "-i", bed_src]
    for wav, _ in clips:
        inputs += ["-i", wav]

    fg = []
    fg.append(f"[1:a]atrim=start={bed_skip:.3f},asetpts=PTS-STARTPTS,"
              f"volume={BED_LEVEL},"
              f"adelay={int(bed_at*1000)}:all=1,apad[bed]")
    vox_in = []
    for i, (_, t) in enumerate(clips):
        fg.append(f"[{i+2}:a]volume={VOX_LEVEL},"
                  f"adelay={int(t*1000)}:all=1[v{i}]")
        vox_in.append(f"[v{i}]")
    fg.append(f"{''.join(vox_in)}amix=inputs={len(vox_in)}:normalize=0,"
              f"apad,asplit=2[vox][voxkey]")
    fg.append("[bed][voxkey]sidechaincompress="
              "threshold=0.04:ratio=7:attack=25:release=450[duck]")
    fg.append("[duck][vox]amix=inputs=2:normalize=0,"
              "alimiter=limit=0.95[aout]")

    out = os.path.join(take, "production.mp4")
    run(["ffmpeg", "-y", *inputs,
         "-filter_complex", ";".join(fg),
         "-map", "0:v", "-map", "[aout]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{film_dur:.2f}", out])
    print(f"{out}  ({dur_of(out):.0f}s, {len(clips)} voiced lines)")


if __name__ == "__main__":
    main()
