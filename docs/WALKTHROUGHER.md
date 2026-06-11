# The Walk-through-er — design & implementation

A tool that *performs* Clanker City Chronicles — plays it the way a human
would, on camera, with timing and taste — and in doing so proves the game
is playable. One screenplay, two outputs:

- **A film**: a paced, recorded playthrough (webm/mp4 + a README GIF).
- **A verdict**: pass/fail with evidence, suitable for gating deploys.

The core idea: **a performance that asserts**. We never record a broken
take, and we never ship a build the performer can't get through.

## Status: IMPLEMENTED (phases 1-3)

```bash
# validate (fast, strict, exit 0/1 — run before deploying):
python3 walkthrough/driver/walkthrough.py --serve \
    walkthrough/screenplay/01-docks.play.yaml

# perform (cinematic, records video + timeline + dub sheet):
python3 walkthrough/driver/walkthrough.py --mode perform --serve \
    walkthrough/screenplay/01-docks.play.yaml

# render the take into walkthrough.mp4 + .srt + README gif:
python3 walkthrough/post/render.py walkthrough/out/<take>
```

Implementation notes vs. the original design below:
- The post-processor is `walkthrough/post/render.py` (Python, not
  render.sh — it shares the game's FONT3 pixel font for title cards).
- A transcript extractor was added (`tools/transcript.py`): the dialog
  is parsed straight from the .scc sources, so the timeline logs every
  observed talk segment with its *exact line text* — no OCR needed.
- **Audio/dub stays in the planning stage** per project direction: the
  perform take emits a `dubsheet.md` (timestamped lines + empty cue
  column) to arrange a Suno-generated music/foley/VO dub by hand. See
  docs/research/NARRATION.md (deadpan KQ6-style narration research) and
  docs/research/AUDIO.md (in-game audio + mixing pipeline research).
- Boot hardening: no screenshots while the wasm runtime spins up (races
  SDL's WebGL context creation in headless chromium), one reload retry,
  and the game rect is detected from the x-extent of non-black columns
  only (the visible y-extent shrinks when cutscenes hide the verb
  panel — aspect-based detection goes blind exactly when the arrival
  cutscene plays).

## Why this is easier for us than for normal games

Three properties of this project do most of the work:

1. **We own the stage geometry.** `tools/genassets.py` is the single
   source of truth for every object rectangle (`GEOM`), the verb panel
   layout, the walkboxes, and the master 256-color palette. The
   walkthrougher never hardcodes a pixel coordinate — it reads a
   generated *stage map*.
2. **We own the palette, so pixels are assertions.** "Did the bolt
   appear?" = "is the pixel at the bolt's hotspot one of the 4 steel
   greys (indices 2–15)?" "Is Sprocket talking?" = "are there
   SPROCKET_COLOR (105) pixels in the text band?" The palette turns
   screenshots into a machine-readable oracle — no OCR, no fuzzy image
   diffing.
3. **The web build takes argv from the URL fragment.** We can boot
   straight into the game, and pass flags (e.g. `--debuglevel=N`) to make
   ScummVM narrate engine activity to the browser console, which
   Playwright reads. Engine errors/warnings become test failures for free.

## Architecture

```
walkthrough/
  screenplay/
    01-docks.play.yaml      what to perform, what to expect (text, committed)
  stage/
    docks.stage.json        GENERATED: object rects, verb coords, palette,
                            walkboxes, inventory slots (from genassets.py)
  driver/
    walkthrough.py          Playwright driver (Python, like the rest of tools/)
    oracle.py               pixel probes + console-log assertions
    timeline.py             emits timeline.json (step → t_start/t_end)
  post/
    render.sh               ffmpeg: trim, nearest-neighbor upscale, title
                            cards, subtitles, GIF export
  out/                      (gitignored) videos, reports, failure dumps
```

### 1. The screenplay (one file per scene, plain text)

Declarative YAML. Verbs and objects by *name*, resolved against the stage
map. Example covering everything currently playable in the Docks:

```yaml
title: "Clanker City Chronicles — Scene 01: The Docks"
open:
  url: "#chronicles"          # validate mode appends --debuglevel
  wait: room-fade-in          # oracle: dock-wood pixels present

shots:
  - name: arrival
    perform: let-play          # cinematic: watch the whole cutscene
    validate: skip             # fast mode: press Escape
    expect:
      - talking                # SPROCKET_COLOR pixels seen in text band
      - console: no-errors     # beyond the known-benign allowlist

  - name: the-sign
    do: [ {verb: Examine, object: neon sign} ]
    expect: [ talking ]

  - name: percussive-maintenance
    do: [ {verb: Use, object: neon sign} ]
    expect:
      - pixel: {at: dockBolt.hotspot, is: steel}   # the bolt dropped
    timeout: 20s

  - name: legal-tender
    do: [ {verb: Pick up, object: shiny bolt} ]
    expect:
      - pixel: {at: inventory.slot0, is: steel}    # bolt in inventory
      - pixel: {at: dockBolt.hotspot, is: dock-wood}  # gone from floor

  - name: civic-duty
    do: [ {verb: Examine, object: notice board} ]
    expect: [ talking ]
  - name: take-the-evidence
    do: [ {verb: Pick up, object: official notice} ]
    expect:
      - pixel: {at: inventory.slot1, is: white}    # poster icon

  - name: meet-betty                       # performance flavor; still asserts
    do: [ {verb: Talk to, object: Boom-Arm Betty} ]
    expect: [ talking ]

close:
  card: "TO BE CONTINUED IN ACT TWO"
```

Primitive set (kept deliberately small): `do` (verb+object, walk-to x,y,
press-key), `expect` (pixel, talking, silence, console), `perform/validate`
overrides per shot, `timeout`. New scenes = new screenplay files; the
driver chains them.

### 2. The stage map (generated, never hand-written)

`tools/genassets.py --emit-stage walkthrough/stage/docks.stage.json`
dumps what it already knows:

- object name → rect + a *click hotspot* (rect center, nudged into the
  walk-reachable area) — from `GEOM`
- verb name → screen coords — from the verb layout constants
- inventory slot k → screen coords — from the verbs.scc layout
- named palette probes: `steel: [2..15]`, `dock-wood: [64..75]`,
  `sprocket-talk: [105]`, `white: [104]`, …
- walkboxes (so the driver can sanity-check that a click target is
  reachable)

When art moves, the stage map moves with it. A renamed object breaks the
screenplay loudly at resolve time, not silently at click time.

### 3. The driver (Python + Playwright, headless Chromium)

- **Coordinate mapping**: read the canvas bounding rect at runtime, map
  game (320×200) → page pixels. No baked-in viewport assumptions.
- **Acting**: for each `do`, click the verb, click the object hotspot,
  then *wait for quiescence* — poll the oracle until the expectation
  holds or the timeout dumps evidence (screenshot + console log +
  screenplay position) into `out/failures/`.
- **Two paces, same script**:
  - `--mode=validate`: Escape through cutscenes, minimal waits, no
    recording. Exit code 0/1. Target: < 60s for the Docks.
  - `--mode=perform`: real-time, cutscenes play out, an extra beat
    (`hold: 2s`) after each landed joke; recording on.
- **Console oracle**: boot with `#--debuglevel=1 chronicles` (fragment →
  argv) in validate mode. Maintain a small allowlist of known-benign
  messages (the unknown-MD5 masquerade warning, Web MIDI denial); anything
  else at error level fails the run.
- **Determinism notes**: the neon-sign flicker script is random — probes
  near the sign must accept both states (probe the *bolt*, not the sign).
  Walking speed and text speed are fixed by the game, so step timeouts
  can be tight.

### 4. Recording & the artful part

- **Capture**: in-page `canvas.captureStream(60)` + `MediaRecorder`
  (vp9 webm at native canvas resolution), chunks streamed to disk via an
  exposed binding. Fallback: CDP screencast. Pixel-perfect, no window
  chrome, no cursor jitter from the OS.
- **The edit is data, not labor**: the driver writes `timeline.json` —
  every shot's name and start/end timestamps, plus every dialog line the
  oracle saw with its timestamp. `post/render.sh` consumes it to:
  - trim boot noise, open on the room fade-in
  - insert title card and per-scene cards (shot names are the captions —
    "percussive maintenance" is *meant* to be read)
  - upscale nearest-neighbor (pixel art stays crisp) to 1280×800, 4:3
    pillarboxed on a dark steel background from the master palette
  - emit `walkthrough.srt` from the timeline (accessibility + lets the
    film work muted)
  - export `walkthrough.mp4` + a ~15s highlight `docks.gif` for the README
- **Audio hook (future)**: when the game gets sound, route SDL's WebAudio
  through a `MediaStreamDestination` into the same MediaRecorder. Until
  then, `render.sh` can lay a chiptune bed under the mp4 in post.

### 5. CI / when it runs

- **Pre-deploy gate**: build game → `build-web.sh` → serve `web/dist`
  locally → `walkthrough.py --mode=validate` → only then push `gh-pages`.
- **Post-deploy smoke**: same screenplay against the live URL (catches
  hosting regressions like the path-prefix landmine).
- **On demand**: `--mode=perform` regenerates the film + README GIF
  whenever we want a new trailer; the GIF commit doubles as proof of the
  build it was filmed on.
- Local first (the toolchain already lives on this machine); a GitHub
  Actions port needs the scummc bootstrap in the runner — phase 4, not a
  blocker.

## Build order

1. **Stage map export** from genassets.py (small; it's all already there).
2. **Driver + validate mode** with the Docks screenplay — this is the
   testing payoff, and everything in it was already proven by hand in
   this session (coordinate clicks, Escape skip, pixel checks on
   screenshots, console reading).
3. **Recording + timeline + render.sh** — performance mode.
4. **CI wiring** (gate the deploy; optional live-site smoke).

## Open questions (deliberately punted)

- Verifying *which* line was said (vs. *that* talking happened) — needs
  either OCR or a tiny debug channel in common.scc that `prints` each
  egoSay to the console. The debug-channel route fits our text-first
  ethos and costs ~3 lines of scc.
- Save-state checkpoints so long future walkthroughs can resume per-scene
  (ScummVM autosaves land in IDBFS; loadable via `--save-slot` in argv).
- Whether `perform` mode should run on the live site (prettier provenance)
  or the local build (no network hiccups in the take). Default: local.
