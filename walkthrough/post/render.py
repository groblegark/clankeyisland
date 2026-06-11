#!/usr/bin/env python3
"""Render a perform-mode take into the final film + README GIF.

The edit is data: timeline.json says where the room fades in, where every
shot and dialog line sits, and where the take ends. This script trims the
boot noise, crops the pillarbox bars (rect logged by the driver), upscales
nearest-neighbor, wraps the footage in title/end cards drawn with the
game's own 3x5 pixel font, and emits subtitles from the observed lines.

Outputs into the take directory:
  walkthrough.mp4   the film (silent — the dub is arranged separately,
                    see the dub sheet + docs/research/NARRATION.md)
  walkthrough.srt   subtitles from the timeline
  docks.gif         short highlight for the README

Usage: render.py <take-dir> [--gif-shot percussive-maintenance]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from genassets import FONT3, PAL  # noqa: E402  (the game's own pixel font)

OUT_W, OUT_H = 1280, 800
FPS = 25
CARD_SEC = 3.0
PRE_ROLL = 0.6
POST_ROLL = 2.0


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def text_size(s, scale):
    return (len(s) * 4 - 1) * scale, 5 * scale


def draw_text(im, s, y, scale, color):
    """Center FONT3 text (flat 15-bit strings, 3 wide x 5 tall)."""
    w, _ = text_size(s, scale)
    x = (im.width - w) // 2
    px = im.load()
    for ch in s:
        bits = FONT3.get(ch, FONT3[' '])
        for i, b in enumerate(bits):
            if b == "1":
                cx, cy = x + (i % 3) * scale, y + (i // 3) * scale
                for dy in range(scale):
                    for dx in range(scale):
                        px[cx + dx, cy + dy] = color
        x += 4 * scale


def make_card(lines, path):
    im = Image.new("RGB", (OUT_W, OUT_H), tuple(PAL[1]))
    n = len(lines)
    for i, (s, scale, pal_idx) in enumerate(lines):
        y = OUT_H // 2 + (i - n / 2) * 9 * max(s2 for _, s2, _ in lines)
        draw_text(im, s.upper(), int(y), scale, tuple(PAL[pal_idx]))
    im.save(path)


def card_video(png, out, dur):
    run(["ffmpeg", "-y", "-loop", "1", "-i", png, "-t", str(dur),
         "-r", str(FPS), "-pix_fmt", "yuv420p",
         "-c:v", "libx264", "-crf", "18", out])


def fmt_srt(t):
    ms = int(t * 1000)
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("take")
    ap.add_argument("--gif-shot", default="percussive-maintenance")
    ap.add_argument("--gif-out", default=None)
    args = ap.parse_args()

    take = args.take.rstrip("/")
    with open(os.path.join(take, "timeline.json")) as f:
        events = json.load(f)["events"]

    by_type = lambda t: [e for e in events if e["type"] == t]
    ready = by_type("room_ready")[0]
    rect = ready.get("rect", [0, 0, OUT_W, 720])
    start = max(0.0, ready["t"] - PRE_ROLL)
    end = by_type("shot_end")[-1]["t"] + POST_ROLL

    tmp = tempfile.mkdtemp(prefix="clankey-render-")
    x, y, w, h = rect

    # --- main footage: trim, crop bars, upscale pixel-crisp ---------------
    main_mp4 = os.path.join(tmp, "main.mp4")
    run(["ffmpeg", "-y", "-i", os.path.join(take, "take.webm"),
         "-ss", f"{start:.2f}", "-to", f"{end:.2f}",
         "-vf", (f"crop={w}:{h}:{x}:{y},"
                 f"scale={OUT_W}:{OUT_H}:flags=neighbor,fps={FPS}"),
         "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "18", main_mp4])

    # --- cards in the game's own pixel font -------------------------------
    title_png = os.path.join(tmp, "title.png")
    end_png = os.path.join(tmp, "end.png")
    make_card([("CLANKER CITY CHRONICLES", 12, 105),
               ("SCENE 01  THE DOCKS", 6, 100)], title_png)
    make_card([("TO BE CONTINUED", 10, 105),
               ("IN ACT TWO", 8, 100)], end_png)
    title_mp4 = os.path.join(tmp, "title.mp4")
    end_mp4 = os.path.join(tmp, "endcard.mp4")
    card_video(title_png, title_mp4, CARD_SEC)
    card_video(end_png, end_mp4, CARD_SEC)

    # --- concat ------------------------------------------------------------
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for p in (title_mp4, main_mp4, end_mp4):
            f.write(f"file '{p}'\n")
    final = os.path.join(take, "walkthrough.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", final])

    # --- subtitles -----------------------------------------------------------
    srt = os.path.join(take, "walkthrough.srt")
    shift = CARD_SEC - start
    lines = [e for e in by_type("line_start") if e.get("text")]
    ends = {(e["t"]): e for e in by_type("line_end")}
    with open(srt, "w") as f:
        for i, e in enumerate(lines):
            nxt = [t for t in sorted(ends) if t > e["t"]]
            t1 = (nxt[0] if nxt else e["t"] + 3.0) + shift
            f.write(f"{i+1}\n{fmt_srt(e['t']+shift)} --> {fmt_srt(t1)}\n"
                    f"{e['text']}\n\n")

    # --- README gif ----------------------------------------------------------
    shots = {e["shot"]: e["t"] for e in by_type("shot_start")}
    shot_ends = {e["shot"]: e["t"] for e in by_type("shot_end")}
    gif = args.gif_out or os.path.join(take, "docks.gif")
    if args.gif_shot in shots:
        g0 = shots[args.gif_shot] - start
        g1 = shot_ends[args.gif_shot] - start + 0.5
        run(["ffmpeg", "-y", "-i", main_mp4, "-ss", f"{g0:.2f}",
             "-to", f"{g1:.2f}",
             "-vf", ("fps=10,scale=480:-1:flags=neighbor,"
                     "split[a][b];[a]palettegen[p];[b][p]paletteuse"),
             gif])

    # edit parameters for the dub stage (post/dub.py)
    with open(os.path.join(take, "render.json"), "w") as f:
        json.dump({"trim_start": start, "trim_end": end,
                   "card_sec": CARD_SEC, "fps": FPS, "rect": rect}, f,
                  indent=1)

    dur = end - start + 2 * CARD_SEC
    print(f"{final}  ({dur:.0f}s)")
    print(srt)
    if os.path.exists(gif):
        print(f"{gif}  ({os.path.getsize(gif)//1024}K)")


if __name__ == "__main__":
    main()
