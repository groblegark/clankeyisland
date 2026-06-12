# docs/research/INGAME-VOICE.md — In-game PCM voices (feasibility spike)

## Verdict: FEASIBLE, low-risk, ~1 day for the prototype, ~2–3 days for full coverage

Every link in the chain already exists and is verified at source level. ScummC has first-class voice support (parser, linker, .sou emitter), ScummVM's DOTT path plays exactly what sld emits, the wasm build only needs one extra `cp`, and dub.py already renders cached per-line robot WAVs. The only genuinely new code is a small build tool that rewrites `egoSay("...")` → `egoSay("%V{sym}...")` and packs VOCs.

## 1. The exact mechanism (file:line evidence)

### ScummC compiler side (vendor/scummc)

- **Grammar**: `voice` is a room-body resource. `voicedecl: VOICE SYM` (scc_parse.y:688), keyword registered at scc_lexer.c:74. Definition forms (scc_parse.y:658–686):
  - `voice v = { "file.voc", sync1, sync2, ... };` (with mouth-sync ms offsets)
  - `voice v = { "file.voc" };` (no sync — fine, sync is optional)
- **Say-line reference**: string escape `%V{sym}` inside any say string. Lexer maps `V` → `SCC_STR_VOICE` (scc_lexer.c:149–150, type constant = 10 = scc_parse.h:183); parser validates the symbol is a voice (scc_parse.y:1934). Working example: vendor/scummc/examples/openquest/secretroom.scc:51 + :153 — `voice mwwwahSnd = { "sounds/mwwwah_huh_huh.voc" };` then `actorSay(commanderZif, "%V{mwwwahSnd}" "Mwaaah huh huh...");`. `egoSay` is the builtin opcode 0xBB (scc_func.h:790) and takes the same string type, so `egoSay("%V{v}Text")` works identically.
- **VOC validation**: scc_roobj_add_voice (scc_roobj.c:334) loads the .voc, prepends a `VCTL` block with big-endian sync table (scc_roobj.c:361–366), and scc_check_voc (scc_roobj.c:273) **rejects anything but pack-0 (uncompressed) type-1 blocks with terminator** — i.e. 8-bit unsigned PCM VOC, same rule as docs/research/AUDIO.md risk #6.
- **Code emission**: the say string gets `FF 0A` + a 14-byte placeholder (scc_code.c:296–303) which sld patches with the clip's file offset and VCTL size in DOTT's interleaved format (scc_ld.c:634–655: bytes `off_lo off_hi FF 0A off_b2 off_b3 FF 0A len_lo len_hi FF 0A len_b2 len_b3`).
- **.sou emission**: scc_ld_parse_voice assigns offsets starting at 8 (scc_ld.c:304, 331, `scc_voice_off = 8` at :104); scc_ld_write_sou writes `"SOU "` + 0 + concatenated VCTL+VOC blocks (scc_ld.c:1360–1375); main() writes `<out>.sou` whenever any voice exists (scc_ld.c:1458–1471). **Not XOR-encrypted** — independent of `-key 0x69`, and ScummVM expects that (`_sfxFileEncByte = 0` for non-HE, sound.cpp:1120/1151).

### ScummVM playback side (vendor/scummvm-src/engines/scumm)

- **String escape**: `case 10:` in CHARSET_1 processing (string.cpp:496–511) decodes the 14-byte offset/length exactly as sld writes them and calls `_sound->talkSound(offset, length, DIGI_SND_MODE_TALKIE)` (string.cpp:507) — DOTT is v6, so it takes the non-HE branch.
- **File discovery**: setupSfxFile tries `<basename>.sou` then `monster.sou` (sound.cpp:1126–1136); since we link as `tentacle`, **either tentacle.sou or monster.sou works** — the Makefile's `cp tentacle.sou monster.sou` is belt-and-braces.
- **Playback**: the v6 branch ("verified for INDY4, DOTT and SAM", sound.cpp:651) skips the 8-byte VCTL header (`offset += 8`, sound.cpp:695), reads the BE sync table into `_mouthSyncTimes` (sound.cpp:1152–1156), then plays the VOC at kSpeechSoundType. Talk timing switches from char-count to sound-driven: `_haveActorSpeechMsg = !_sound->isSoundRunning(kTalkSoundID)` (actor.cpp:3447), and `case 10` sets `_haveActorSpeechMsg = false` (string.cpp:510) so the line stays up while the clip plays.
- **Speech vs text config**: `speech_mute` → `_voiceMode = 2` (text only, early return at sound.cpp:653); else `_voiceMode = subtitles ? 1 : 0` (scumm.cpp:2633–2636). Defaults give voice+text. If the .sou is missing, ScummVM force-enables subtitles (scumm.cpp:1541–1543) — graceful degradation for free.

### The wasm build gap (the actual bug to fix)

tools/build-web.sh:60–61 copies **only tentacle.000 and tentacle.001** into `data/games/chronicles/`. The .sou never ships. Fix is one line (add `tentacle.sou` and/or `monster.sou` to the cp) — the `build-make_http_index.py` regeneration that follows already handles the index.json sizes. Optionally add `subtitles=true` / `speech_mute=false` to web/scummvm.ini.in `[chronicles]` for explicitness (note IDBFS ini staleness for returning visitors — AUDIO.md risk #4 — but the defaults already do the right thing, so this is non-critical).

### The voice-asset pipeline we already have

- walkthrough/post/dub.py:62–73 `speak(text)`: piper en_US-lessac-medium + ROBOT_FX chain, **cached by sha1(voice|fx|text) in ~/.cache/clankey-voices** — exactly the per-line renderer needed, just at 48 kHz float; needs a downstream `-ar 22050 -ac 1 -acodec pcm_u8` conversion.
- tools/genaudio.py:24 `write_voc()` already writes spec-compliant 22050 Hz type-1/pack-0 VOCs in pure python (vendor raw2voc.c:44/118 is the C equivalent).
- tools/transcript.py already parses every `egoSay` string out of the .scc sources (regex at transcript.py:26) — the same extraction the voice packer needs. Current corpus: ~412 egoSay lines across game/*.scc (common 20, alley 79, tavern 70, midtown 61, docks 79, inventoryitems 41, theater 62).

## 2. Pipeline design (full build step)

New tool `tools/genvoice.py`, run between scc sources and `scc` compile (slot into game/Makefile as a `%.scc → build/%.voiced.scc` preprocessing rule so hand-written sources stay clean):

1. For each room .scc, find every `egoSay("...")` (and later `actorSay(actor, "...")`) string literal.
2. For each line: `sym = "vx_" + sha1(text)[:10]`; render via dub.py's speak() cache; convert to `build/voices/<sym>.voc` (ffmpeg `-ar 22050 -ac 1 -f u8` → write_voc, or sox direct).
3. Emit the rewritten room source: inject `voice vx_...= { "voices/....voc" };` declarations **inside the `room { }` body** (voicedef is a room resource — scc_parse.y:537/638) and prefix each string with `%V{vx_...}` (at string start, matching original DOTT convention and the openquest example).
4. Makefile compiles the .voiced.scc (BUILD is already on the -I/-R paths); `sld` then emits tentacle.sou automatically; existing `cp tentacle.sou monster.sou` rule (game/Makefile tentacle target) already runs.
5. build-web.sh ships the .sou (one-line fix above).

Multi-room duplication note: a voice clip is a room resource, so a line shared across rooms (common.scc helpers) gets declared once in whatever room compiles it — common.scc is its own room, fine. Hash-keyed VOC files dedupe the rendering cost.

## 3. Minimal end-to-end prototype (Milestone D1: one Sprocket line in the browser)

1. `text="..."` ← pick one docks.scc egoSay line. Render: `python -c 'from dub import speak; ...'` → `ffmpeg -i fx.wav -ar 22050 -ac 1 -f u8 line.raw` → `vendor/scummc/build.*/raw2voc -r 22050 -o line.voc line.raw` (or genaudio.write_voc). Put it at `game/voices/hello.voc`.
2. Edit docks.scc room body: `voice helloVox = { "voices/hello.voc" };` and the chosen line → `egoSay("%V{helloVox}...");` (add `-R .` already covered by `-R $(GAME_DIR)`... verify resource path resolution; worst case use a path relative to cwd at scc invocation).
3. `make -C game tentacle` → confirm `build/tentacle.sou` + `build/monster.sou` exist and `xxd | head` shows `SOU ` then `VCTL`.
4. Native smoke test: `make -C game run`, trigger the line, hear robot voice + see sound-driven talk timing.
5. Add `tentacle.sou` to build-web.sh:60 cp; `tools/build-web.sh serve`; click through, trigger the line in the browser.

## 4. Risks

1. **Payload size / load latency** (the real cost): ~412 ego lines × ~3 s × 22 KB/s ≈ 27 MB monster.sou; setupSfxFile opens it at engine init, so the emscripten HTTP filesystem may fetch the whole file at game start. Mitigations: 11025 Hz (≈ 14 MB, period-appropriate), or measure whether the wasm HTTP FS does range reads before worrying.
2. **VOC strictness**: must be 8-bit unsigned mono uncompressed type-1/pack-0 with terminator or scc_roobj.c:273 hard-rejects at compile — single shared conversion helper, same rule already enforced for SFX (AUDIO.md risk #6).
3. **Walkthrough double-dubbing**: the driver's MediaRecorder bed will now contain real in-game speech; dub.py's piper overlay would speak every line twice. Coordinate: once in-game voice ships, dub.py drops its voice track (a simplification — the game audio becomes the single source).
4. **Source-rewrite fragility**: regex-rewriting .scc (multi-part string literals, `\"` escapes, lines inside `unless{}`) — reuse transcript.py's proven extraction; lines transcript.py can't see, genvoice.py shouldn't touch.
5. **Mouth sync**: zero sync points means no mouth-flap animation timing; optional polish later (estimate word boundaries → ms offsets in the voicedef synclist).
6. **IDBFS staleness**: returning visitors keep the cached game data; bumping file sizes changes index.json but the HTTP FS may serve stale cached blobs — verify with a hard refresh path documented.

## 5. Effort estimate

- D1 prototype (one line, browser-audible): **0.5–1 day** (mostly build plumbing + the two smoke tests).
- Full pipeline (genvoice.py, Makefile integration, all ~412 ego lines, size tuning): **+1–2 days**; piper render of the full corpus is minutes (cache-warm from prior dubs for any line already performed).
- Polish (NPC actorSay voices with distinct FX per character, mouth-sync tables): **+1–2 days**, optional.

Key files: `/Users/matthewbaker/clankeyisland/vendor/scummc/scc_parse.y` (:658,:688,:1934), `scc_lexer.c` (:74,:149), `scc_code.c` (:296), `scc_roobj.c` (:273,:334), `scc_ld.c` (:304,:331,:634,:1360,:1458); `/Users/matthewbaker/clankeyisland/vendor/scummvm-src/engines/scumm/string.cpp` (:496–511), `sound.cpp` (:651–740,:1019,:1126–1156), `scumm.cpp` (:1541,:2633), `actor.cpp` (:3447); `/Users/matthewbaker/clankeyisland/tools/build-web.sh` (:60), `/Users/matthewbaker/clankeyisland/game/Makefile` (tentacle target), `/Users/matthewbaker/clankeyisland/walkthrough/post/dub.py` (:62), `/Users/matthewbaker/clankeyisland/tools/genaudio.py` (:24), `/Users/matthewbaker/clankeyisland/tools/transcript.py` (:26).