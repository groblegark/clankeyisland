# Project notes — operational knowledge

Things learned the hard way, kept out of the polished docs. Newest first
within each section. See also: README (pipeline overview),
docs/WALKTHROUGHER.md (performer), docs/research/ (audio + narration).

## Daily commands

```bash
cd game && make run                 # build + play natively
cd game && make tentacle            # just build (build/tentacle.000/.001)
./tools/build-web.sh                # full web bundle -> web/dist
python3 walkthrough/driver/walkthrough.py --serve \
    walkthrough/screenplay/01-docks.play.yaml          # validate (gate)
python3 walkthrough/driver/walkthrough.py --mode perform --serve ...
python3 walkthrough/post/render.py walkthrough/out/<take>   # film + gif
python3 walkthrough/post/dub.py    walkthrough/out/<take>   # + voice/music
```

Deploy = push `web/dist` as the `gh-pages` branch (orphan commit in a
temp dir, force-push). Live at https://groblegark.github.io/clankeyisland/
about a minute later. Always run validate first.

## Pitfalls / gotchas

- **scummvm.ini is cached in visitors' IndexedDB** on first visit and
  never re-fetched. Config changes (e.g. new game targets) won't reach
  returning visitors — rename the target or accept it. URL-fragment args
  (`#--music-driver=adlib chronicles`) are the reliable override.
- **The wasm bakes its data path** (`/clankeyisland/data`) at configure
  time, and upstream configure *clobbers* `--datadir` for wasm32 — our
  patch `tools/patches/0002` fixes that. The site cannot move off the
  `/clankeyisland/` path prefix without a rebuild (`SITE_PATH=`).
- **Browser autoplay**: visitors get silence until their first click
  (AudioContext suspended; SDL resumes on input). The walkthrougher
  launches Chromium with `--autoplay-policy=no-user-gesture-required`.
  A "click to start" overlay in index.html is the future fix.
- **Native vs wasm timbre differs**: CoreAudio GM synth vs AdLib OPL2
  emulation. Same MIDI, different instruments. The browser is canonical.
- **soun resource rules** (from docs/research/AUDIO.md): one .soun = one
  thing; music must be the `-midi` (SOUN/MIDI) flavor, never `-gmd`
  (silently dropped under AdLib); SFX must be 8-bit unsigned mono VOC;
  never use `-spk` (buggy in soun.c).
- **In a take directory** only `production.mp4` has sound. `take.webm` /
  `walkthrough.mp4` are silent footage; `game-audio.webm` is audio-only.
- **Playwright quirks** (cost a debugging session each): page bindings
  silently dropped streamed audio chunks (collect one blob via
  `evaluate` instead); early screenshots race SDL's WebGL context
  creation during wasm boot (wait for `Module.calledRun`); the visible
  game aspect changes when cutscenes hide the verb panel (detect the
  game rect by x-extent only); the driver's end-of-take rename loop must
  not catch `game-audio.webm`.
- **iMUSE loop**: `imPlayerSetLoop(snd, 999, 1, 0, 65, 0)` — 65 =
  LOOP_BEATS in tools/genmusic.py (16 bars × 4 + 1). A watchdog script
  in docks.scc restarts the theme if the loop falls off the end.
- **ScummVM ini parser wants `#` comments**, not `;`.
- **Voice tier**: OPENAI_API_KEY is out of quota and the Azure resource
  only deploys DeepSeek-R1 (no TTS), so dub.py uses local piper-tts
  (lessac) + robot FX. Upgrading to ElevenLabs/funded OpenAI is a
  drop-in swap in dub.py `speak()` — see docs/research/NARRATION.md for
  the directable-TTS comparison and the deadpan style instructions.

## Where things are

- ScummC toolchain: `vendor/scummc` (gitignored; tools/setup-scummc.sh).
  Binaries under `vendor/scummc/build.*/<arch>/` (scc, sld, cost, char,
  soun, midi).
- ScummVM source for the wasm build: `vendor/scummvm-src` (gitignored;
  build-web.sh clones + patches it).
- All art/audio is generated: genassets.py (gfx + stage map),
  genaudio.py (VOC sfx), genmusic.py (theme MIDI), transcript.py
  (dialog JSON). Re-run after changing any of them; the game Makefile
  picks the outputs up from assets/generated/.
- Voice cache: `~/.cache/clankey-voices` (keyed by text+fx hash —
  rewriting a line re-renders only that line).

## Next steps (in rough order)

1. Scene 02: the Scrap & Barrel tavern (game/scenes/02-scrap-and-barrel.md)
   — earns the oil can; unlocks Betty/crate. New room = new bg in
   genassets, walkboxes, .scc, screenplay, stage map entries.
2. "Click to start" overlay so visitors hear the arrival music.
3. Wire validate as a hard gate inside build-web.sh / a deploy script.
4. Optional dub upgrades: funded TTS for real deadpan direction; the
   Suno music/foley arrangement pass over the emitted dub sheet.
5. In-game speech (monster.sou via ScummC `voice` decls) — parked.
