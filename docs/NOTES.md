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
    walkthrough/screenplay/full-run.play.yaml          # validate (gate)
python3 walkthrough/driver/walkthrough.py --mode perform --serve ...
python3 walkthrough/post/render.py walkthrough/out/<take>   # film + gif
python3 walkthrough/post/dub.py    walkthrough/out/<take>   # + voice/music
```

Deploy = `./tools/deploy-web.sh` — builds, runs the Act One validate
gate, and pushes `web/dist` as the `gh-pages` branch. Live at
https://groblegark.github.io/clankeyisland/ about a minute later.

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
- **Object owners default to 0x0F, not 0**: sld fills unset owners with
  0x0F (scc_ld.c), so `getObjectOwner(item)` is truthy for items the
  player has never touched. "In my pocket" is `== VAR_EGO` (pickupObject
  does putOwner(obj, VAR_EGO)); "consumed" is owner 0 via
  setObjectOwner(x, 0). Cost a validate run: the dumpster skipped its
  own loot and Rivet's riddle duel fired before the bolts existed.
- **Walkthrough-path lines go FIRST in source** inside each verb
  handler: transcript pairing hands out egoSay lines in source order
  (tools/transcript.py), so guard/hint/repeat branches must sit
  textually after the success path or the dub voices the wrong lines
  (the gate narrated its own failure gag over the fare cutscene).
- **ScummC verb ids are per-compilation-unit** (assigned in first-use
  order) and sld keeps each unit's baked constants — declare every
  shared verb with an explicit `@ id` in common.sch or units silently
  disagree (cost a full day: "Use X with Y" never worked).
- **The sentence executor dispatches to objA's script.** An inventory
  item with a bare `case Use:` gag swallows every "Use it with Y"
  sentence — items must route `if(objB)` to objB's UsedWith themselves
  (see inventoryitems.scc). Same for defaultAction's Give case.
- **ScummVM compacts inventory on removal**: consume the bolt and the
  poster shifts into slot 0; new items append after. Slot-based
  screenplay expectations must model this.
- **Story flags before speech**: object scripts can run concurrently
  with a cutscene; set bits at the top of a branch, not mid-dialog.
- **Engine truth beats label guessing**: the sentence executor
  dbgPrints `SNTC vrb/objA/objB` (needs `--debuglevel=1`, which the
  screenplays pass via their `game:` field) — read the take's
  console.log instead of trusting transcript-paired line labels.
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

## The editorial desk

Every scene's text faces an adversarial critique before it ships:
puzzle / comedy / story critics + a cold player advocate, a showrunner
defense pass, one merged report. Charter: `docs/editorial/CHARTER.md`;
run via `Workflow({scriptPath: ".claude/workflows/editorial-review.js"})`.
Reports land in `docs/editorial/NOTES-<date>.md` with a disposition
ledger. First pass (2026-06-12): 7 BLOCKERs — 6 fixed same day (incl.
the Rustlers now stealing Key #1 mid-ovation), B2 deferred.

## Next steps (in rough order)

1. B2+B8 from the editorial desk, combined: THE CONTESTS MUST BE
   PLAYABLE. Wire the dialog-tree UI (game/dialog.scc, unused) into
   Rivet's duel (3 pickable riddles, two flop funny) and make the
   talent-show performance a player choice (wind-count 1-8; the
   "regulation maximum is five" line retro-justifies over-winding as
   the winner). Teach the walkthrougher to click dialog options. Fold
   in N-A1 (magnet + string as separate finds). The desk's ruling:
   no Scene 06 content until this lands.
2. Scene 06: backstage — Madame Voltina (Key #2), with Key #1 freshly
   stolen by the Rustlers (recovery is Act 3, knock-code).
3. The detuning hum (editorial N-A5): act-flag-driven pitch drift in
   genmusic.py — the GDD's designed clock.
4. Optional dub upgrades: funded TTS for real deadpan direction; the
   Suno music/foley arrangement pass over the emitted dub sheet.
5. In-game speech (monster.sou via ScummC `voice` decls) — parked.
(Scene 05 — talent night, the heist, and the editorial pass — shipped
2026-06-12, same day as Scene 04.)

Room-transition verbs (doors, the funicular) say NOTHING: dub pairing
consumes same-verb lines in order, so a spoken ride line desyncs the
previous cutscene's dub. Arrival flavor belongs in the destination
room's entry script.
