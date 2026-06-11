# Clanker City Chronicles — Audio Plan

## 1. In-game audio pipeline (decided defaults)

**Music (one path, no alternatives):**
- **Author**: committed `.py` files using a mido note-DSL (lists of `(pitch, duration)` tuples per channel, PPQ=480, GM programs — chiptune palette like 80/square-lead + 38/synth-bass). Pin `mido==1.3.3` in `requirements.txt`. Output is byte-deterministic.
- **Emit**: type-0/single-track GM SMF. Emit single-track directly from mido (or flatten with ScummC's `midi -merge-track ... -set-type 0`).
- **Package**: `soun -o cue.soun -midi cue.mid` → **SOUN/MIDI basetag**. This is the load-bearing choice: the `MIDI` basetag is loaded wholesale by ScummVM (sound.cpp:1296) and *bypasses* the SOU-container flavor filter, and iMUSE's `getBestMidiDriver` explicitly routes MIDI-flavor sounds through AdLib when no native driver exists ("Route it through AdLib anyway"). Do **not** use `soun -gmd` (silently dropped under the AdLib driver) and do not bother authoring `ADL ` sysex resources — GM→FM fallback tables in `audio/adlib.cpp` handle it.
- **Declare/play** in `.scc`: `sound themeSnd = "theme.soun";` inside the `room {}` header; `startMusic(themeSnd)` / `stopMusic()`. Looping: `imPlayerSetLoop(player, count, tobeat, totick, frombeat, fromtick)` from script (the resource format carries no loop data); transitions via `imPlayerFade`/`imQueueCommand`.

**SFX:**
- Generate/convert to **8-bit unsigned mono uncompressed VOC** (sox/ffmpeg → raw → `raw2voc -r 22050`, or sox direct-to-.voc; VOC must be block type 1, pack 0, with terminator).
- `soun -o phone.soun -voc phone.voc` → SOUN/SOU/SBL. Plays through the digital mixer regardless of MIDI driver, native and wasm.
- `.scc`: `sound phoneSnd = "phone.soun";` + `startSound(phoneSnd)` / `stopSound()` / `isSoundRunning()`.
- **Rule: one .soun = one thing.** Never combine `-voc` with `-adl`/`-midi`; ScummVM picks exactly one sub-block per container.
- Never use `-spk` (soun.c:201 bug loads the wrong file).

**In-game speech (optional, viable contra Investigator 2):** ScummC's `sld` *does* build the .sou — `voice name = { "line.voc", 500 };` declarations + `%V{name}` in `actorSay` → linker emits `tentacle.sou`; copy to `monster.sou` next to `tentacle.000/.001` (example.mak ships this exact rule). Same 8-bit unsigned mono VOC constraint. Treat as polish, not MVP.

**Build/link:** `scc -o room.roobj -V 6 -R gamedir room.scc` → `sld -o tentacle -key 0x69 *.roobj` → `cp tentacle.sou monster.sou`.

**What plays where — no wasm rebuild needed:**
- **wasm**: AdLib OPL emulator is unconditionally compiled (`LINK_PLUGIN(ADLIB)`); GM detection finds nothing (no FluidSynth, WebMIDI fails MDCK_AUTO, MT-32 ROM-less) and falls through to AdLib. Pin it anyway for determinism: serve a `scummvm.ini` with `[tentacle] music_driver=adlib opl_driver=db`, **and** put `--music-driver=adlib --opl-driver=db` in the URL fragment (IDBFS persists stale inis for returning visitors; fragment args are the reliable override).
- **native macOS**: CoreAudio's GM DLS softsynth auto-wins `MDT_PREFER_GM` — real General MIDI timbres. Same data, different sound; audition on both.

## 2. Narration stack for walkthrough videos (decided defaults)

- **TTS**: **piper-tts** (pip), voice **en_US-lessac-medium** (~63 MB onnx, fetched via `python -m piper.download_voices en_US-lessac-medium` in the Makefile — not committed). Offline, ~4× realtime on CPU, clean licensing (Blizzard 2013 dataset). Fallback for character flavor: macOS `say -v Zarvox/Trinoids` (pre-robotized, zero FX). **Do not use edge-tts** for published output (TOS exposure, fragile endpoint).
- **Robot FX — Chain A** (ring-mod lite, keeps intelligibility):
  ```
  ffmpeg -i in.wav -af "highpass=f=100,lowpass=f=5500,tremolo=f=28:d=0.65,acrusher=bits=10:mode=log:mix=0.3,chorus=0.6:0.9:50|60:0.4|0.32:0.25|0.4:2|2.3,alimiter=limit=0.9" out.wav
  ```
  Tune robot-ness via `tremolo d=0.4..0.8` and `acrusher mix`. Chain B (afftfilt phase-zero vocoder) reserved for a harder-monotone character if needed.
- **Mixing**: timestamped CSV/JSON of `{file, ms}` → small Python generator → one ffmpeg filtergraph: per-clip `adelay=<ms>:all=1` → `amix=normalize=0` → `apad` into a speech bus, used both as `sidechaincompress` key (threshold=0.06:ratio=8:attack=20:release=400) against the game/music track and mixed on top; final `amix normalize=0:duration=first` + alimiter; `-c:v copy`. (Verified recipe from Investigator 3; replaces `[0:a]` with real music when it lands.)

## 3. Build order + first concrete milestones

**Track A — in-game SFX (do first, lowest risk):**
Milestone A1: one VOC SFX (`raw2voc` → `soun -voc` → `sound` decl → `startSound`) audible in **both** native ScummVM and the wasm build after a click. Proves the whole resource/link/playback chain end-to-end.

**Track B — in-game music:**
Milestone B1: mido theme `.py` → single-track GM `.mid` → `soun -midi` → `startMusic` playing in native (GM/DLS) **and** wasm (OPL2 via `--music-driver=adlib`), with a working `imPlayerSetLoop` loop. This is the riskiest integration point (Investigator 3's flagged unknown) — validate before writing more music.

**Track C — video narration (fully independent; start in parallel):**
Milestone C1: `make narration` produces one ducked, robotized line mixed onto a screen-capture clip from a timestamps file. (piper install + Chain A + filtergraph generator, all already verified in /tmp.)

**Track D — in-game speech (last, optional):**
Milestone D1: one `voice` decl + `%V{}` actorSay line playing from `monster.sou`.

Order: A1 → B1 → C1 (parallel with A/B) → D1.

## 4. Top risks + mitigations

1. **GM-on-AdLib instrument quality** (the one genuine unknown): plain GM SMF through the OPL2 GM→FM fallback may sound wrong; some GM programs warn "No AdLib instrument defined". *Mitigation*: B1 milestone tests this first; restrict the palette to GM programs with good FM mappings (basic leads/bass/percussion); only if unacceptable, have mido emit iMUSE AdLib instrument sysex into an `ADL ` resource.
2. **Browser autoplay**: AudioContext suspended until first click/keypress — intro music is silently lost on URL-fragment autostart. *Mitigation*: gate game start behind a click overlay, or cue music only after first interaction.
3. **Silent-in-wasm resource shapes**: GMD/ROL-only SOU containers are dropped under the AdLib driver; one-sound-per-container rule. *Mitigation*: pipeline only ever emits SOUN/MIDI (music) or SOUN/SOU/SBL (SFX); enforce in the Makefile.
4. **Stale persisted scummvm.ini in IDBFS**: shipped config changes don't reach returning visitors. *Mitigation*: always pass `--music-driver=adlib --opl-driver=db` as URL-fragment args.
5. **Native/wasm timbre divergence** (DLS GM vs OPL2 FM). *Mitigation*: audition every cue on both targets as part of the music review loop; wasm is the canonical reference.
6. **VOC strictness**: 8-bit unsigned mono uncompressed, type-1/pack-0, terminator required; `soun -spk` is buggy. *Mitigation*: single conversion helper script; never invoke `-spk`.
7. **Determinism/licensing of narration**: pin `mido==1.3.3` and piper in requirements.txt; keep onnx models out of git (Makefile download); check the MODEL_CARD before adopting any voice beyond lessac/ljspeech; avoid edge-tts.
8. **Disk pressure**: host at ~1.6 GiB free — builds with large intermediates may fail. *Mitigation*: clean intermediates in the Makefile; free space before A1.