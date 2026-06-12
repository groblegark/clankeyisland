Below is the complete content for `docs/research/STREAMER-MODE.md`.

---

# Streamer Mode — the walk-through-er as a curious human

Design for a third performance register. `validate` proves the game is
playable; `perform` records the speedrun; **streamer** records somebody
*playing* — exploring, examining the funny things, trying the
reasonable-but-wrong combination first, getting the gag, then solving.

Two properties make this more than cosmetics:

1. **The fair mistakes become regression tests.** The editorial desk
   catalogued the wrong-moves-the-game-must-answer-well
   (key-on-piano N-T1, nine-bolts-at-gate N-A1/N-L6, wrong-bolt-to-Gusket
   B1, voucher-at-the-rope N-M4) and fixes shipped for all of them. The
   deploy-gate screenplay never touches those branches — a streamer
   screenplay run in `validate` mode asserts the refusal lines still
   fire, with the exact text, every deploy.
2. **The film gets a second act structure.** Mistake → gag → solve is the
   native rhythm of adventure-game footage; the current cut is a
   solution montage.

Sources read for this design: `walkthrough/driver/walkthrough.py`,
`walkthrough/screenplay/full-run.play.yaml`, `walkthrough/post/render.py`,
`walkthrough/post/dub.py`, `docs/NOTES.md` (pairing contract),
`docs/editorial/NOTES-2026-06-12*.md`, and the live `.scc` handlers
(`tavern.scc:gusket/piano`, `alley.scc:gate/rivet`, `midtown.scc:oilBar/
grandCog`, `theater.scc:entry/lobbyDoors`) — all `lines:` blocks below are
verbatim engine truth, not transcript guesses.

---

## 1. Screenplay schema additions

A streamer screenplay is a **separate file** (e.g.
`act-one.streamer.play.yaml`), not a driver flag: it is a different
performance with different beats. It runs under both existing modes —
`validate` (fast gate: walkthrough + mistake shots, detours skipped) and
`perform` (the full cut). No third driver mode is needed.

### 1.1 `style:` and the three sugar shot types

```yaml
- name: try-the-key-on-the-piano
  mistake: {verb: Use, object: player piano, with: inventory.slot1}
  lines:
    - Wrong kind of key, wrong kind of missing.
  expect:
    - talking
    - lines-complete                              # exactly these, no extras
    - pixel: {at: inventory.slot1, is: sodium}    # the key is NOT consumed
```

| field | meaning | defaults it implies |
|---|---|---|
| `do:` | unchanged — walkthrough beat | `style: walkthrough`, `hold: 1.0` |
| `detour:` | curiosity beat: same payload shape as `do:`; flavor only, no state change | `style: detour`, `only: perform`, `hold: 1.4`, `expect: [talking]` |
| `mistake:` | a catalogued fair mistake: same payload shape as `do:` | `style: mistake`, runs in **both** modes, `hold: 2.2`, requires `lines:`, implies `expect: [talking, lines-complete]` |
| `wander:` | list of `walk:`/`hover:`/`idle:` steps (§3) | `style: wander`, `only: perform`, `expect: []` |

Exactly one of `do / detour / mistake / wander / cutscene` per shot. The
driver normalizes the sugar into the canonical
`{style, do, only, hold, pre, lines, expect}` shape before `run_shot`
sees it, so the executor stays one code path.

The asymmetry is deliberate: **detours and wanders are skipped in
validate** (they cost time and assert nothing new), **mistakes are not**
— a mistake shot is a contract test of an editorial fix, and the
`validate` run of the streamer screenplay becomes the fair-mistake gate.

### 1.2 New expectation tokens

- `lines-complete` — after the shot's watch ends, the number of talk
  segments observed during the shot must equal `len(lines)`. This is the
  "the refusal line was observed" assertion: the pairing layer (§2)
  guarantees *which* text those segments carry, the count guarantees we
  got the declared branch and not a different one (1-line vs 2-line
  branches differ on every handler audited above).
- `sentence` *(optional, cheap, recommended on every mistake)* — scan
  `take.console` since `shot_start` for the engine's
  `SNTC vrb/objA/objB` debug line matching this shot's verb/object. This
  catches the known hover-race failure where a click degrades into a
  walk (NOTES.md "Engine truth beats label guessing") — exactly the
  failure that would otherwise make a mistake shot silently pass with
  zero lines in `perform`-paced runs. Needs object-name → object-id in
  the stage map (`genassets.py` already owns `GEOM`; emit ids alongside).

### 1.3 Pacing & hold conventions

`hold:` (existing, perform-only sleep after the shot) gains style-based
defaults; a new `pre:` sleeps *before* the click in perform mode — on
film, the cursor sits on the object for a beat, which reads as
deliberation (the verb bar shows the sentence being considered).

| beat kind | `pre` | `hold` | rationale |
|---|---|---|---|
| walkthrough | 0 | 1.0 | as today |
| detour | 0.6 | 1.4 | the joke needs air after the line clears |
| mistake | 0.9 | 2.2 | longest pre (the player is *deciding* to try it) and longest hold (the gag lands, the player "sits with it") |
| wander step | — | per-step `idle` | §3 |
| chapter-closing shot | — | 2.5 (explicit) | breath before the title overlay |

`settle` (1.6 s, driver constant) is unchanged — it is a correctness
mechanism, not pacing.

### 1.4 Chapter markers

```yaml
- name: enter-the-tavern
  chapter: "SCENE 02  THE SCRAP AND BARREL"
  do: {verb: Open, object: tavern door}
  ...
```

`chapter:` on a shot logs a `{"type": "chapter", "t": ..., "title": ...}`
timeline event at `shot_start`. **render.py draws chapters as lower-third
overlays, not inserted cards.** This is load-bearing: the dub bed is the
take's own continuous `game-audio.webm`, and `dub.py`'s
`film_t(t) = t - trim + card` assumes exactly one leading card. Splicing
full-screen cards mid-film would shift every later line and require
cutting the bed at every splice. An overlay (FONT3 pixel-font strip,
pre-rendered PNG, ffmpeg `overlay=enable='between(t,T,T+3)'`) keeps the
time base identity — **dub.py needs zero changes**. Title and end cards
stay concat-ed at the ends only, exactly as today.

---

## 2. Mistake shots vs. line pairing — the problem and the fix

### 2.1 Why front-pairing breaks

Current pairing (`shot_lines` + `watch`): each shot fetches the **full
source-order line list** for `(object, VERB_CASE[verb])` and labels
observed segments `lines[0], lines[1], …` from the front, resetting per
shot. The contract (NOTES.md) is "walkthrough-path lines go FIRST in
source" — i.e. front-pairing is only correct for *the first, on-path
visit* to each (object, verb).

Mistake shots violate this by construction — their lines are
branch-selected and usually mid-list:

| mistake | handler | refusal position in source list | front-pairing result |
|---|---|---|---|
| give fistful to Gusket | `tavern.scc:gusket Give/UsedWith` | boltStash branch at index 4–6 of 9 | labels the refusal as *"Hold still, sir. This is a certified maintenance procedure."* — the dub would voice the success cutscene over the brush-off |
| key on piano | `tavern.scc:piano UsedWith` | index 0 (windupKey branch happens to be first) | correct **by coincidence** |
| nine bolts at gate | `alley.scc:gate Give` | index 0–1 (refusal branch is first; the *success* Give line is index 2) | correct by coincidence — and note this handler already inverts the "success first" contract, proving the contract is really "the screenplay's first visit eats the front" |
| voucher at the rope | `midtown.scc:oilBar Give/UsedWith` | index 0–1 of 3 | correct by coincidence |

So today's `try-the-fare` only dubs correctly because alley.scc happens
to put that branch first. Streamer mode adds revisits too (re-examining
the piano, second TalkTo to Gusket post-fix), where per-shot front
pairing is wrong for *any* branchy handler. "Coincidentally correct" is
not a contract.

### 2.2 Options considered

1. **Per-(object,verb) cursor** — persist consumption across shots so a
   revisit continues mid-list. Fixes *sequential repeat* handlers only;
   branchy handlers (every handler above) are not sequential — a mistake
   would consume the success lines it never spoke, corrupting pairing
   for the later *real* visit. Also stateful and impossible to verify by
   reading one shot. **Rejected as the primary mechanism.**
2. **Speaker tags** — pair by talk color (`talk` = SPROCKET_COLOR 105 vs
   `talk-2` = 106). All transcript lines are `egoSay` (one deadpan
   narrator, by design — see midtown.scc header comment), so speaker
   carries ~no information. **Rejected; not applicable to this game.**
3. **Explicit `lines:` on the shot** — the screenplay declares the exact
   text expected, in order; `watch()` labels segments from that list;
   `lines-complete` asserts the count. Deterministic, branch-aware,
   reviewable in the diff, and it *upgrades pairing into an assertion*:
   the editorial fair-mistake fixes are now pinned verbatim in the
   deploy gate. Cost: duplication of text between `.scc` and screenplay
   — which is exactly the property that makes it a regression test
   (a rewritten refusal line fails `validate` until the screenplay is
   updated deliberately). **Chosen.**

### 2.3 The pairing rules (driver-enforced)

1. `lines:` present → it wins, verbatim, for that shot. Mandatory for
   `mistake:`; recommended for any branchy `detour:`.
2. No `lines:` → front-pairing **only for the first visit** to that
   `(object, case)` in the take. The driver keeps a `visited` set; a
   repeat visit without explicit `lines:` is a warning in `perform` and
   a **failure in `validate`** (the lint that makes the NOTES.md
   contract machine-checked instead of folklore).
3. `lines:` never touches the visited set or any cursor — explicit shots
   are self-contained.
4. Cutscene shots are unchanged (`transcript["cutscenes"]` keyed lists).
5. Crosscheck (optional, per §1.2): the `sentence` console expectation
   proves the right verb/object dispatched, so a paired label can never
   be attached to the wrong interaction.

This also cleans up an existing latent bug for free: `full-run.play.yaml`
revisits `funicular gate` with `Use` three times (`try-the-fare` is
Give, but `pay-the-fare` and `ride-uptown` are both `Use`) — today both
front-pair from index 0 of the same list; under rule 2 the second one
must declare its lines, and the dub stops depending on luck.

---

## 3. The wander mechanic — curiosity you can see

A `wander:` shot is a list of camera-legible idle behaviors:

```yaml
- name: take-in-the-docks
  wander:
    - walk: center-east          # stage walk_targets (already in the map)
    - hover: ferry               # cursor rests on it; verb bar shows the sentence
    - idle: 1.5
    - hover: Boom-Arm Betty
    - walk: center-west
    - idle: 1.0
```

- **`walk:`** — click a `walk_targets` ref (or `[x,y]`). Arrival
  detection: poll frames until the `sprocket-body` probe (already in the
  stage palette probes) matches within a small radius of the target,
  timeout 8 s, fall back to a fixed 2.5 s. No talk expected; the settle
  machinery is bypassed (`expect: []`).
- **`hover:`** — `mouse.move` to the object's hotspot, dwell 0.9 s, **no
  click**. The SCUMM sentence line updates ("Walk to ferry" → the player
  visibly *considering* an object). This is the single cheapest
  curiosity tell on film and costs nothing in game state.
- **`idle:`** — hold N seconds. Sprocket's idle animation plus the OPL
  theme carry it; on film this is "the player reading the room."

Grammar guidance for screenplay authors: open every new room with a
wander (walk into frame, hover 1–2 future-relevant objects), and put a
short `idle` *before* each mistake — hover-the-object → idle → click is
the visual sentence "hmm… what if?". Wander shots are `only: perform` by
sugar default and log `wander_step` events for the dub sheet.

---

## 4. The film pipeline interaction (summary)

- **render.py**: reads `chapter` events; renders FONT3 lower-third PNGs
  (`make_card` generalized to transparent strips); single ffmpeg pass
  overlays each for 3 s at `t + (CARD_SEC - start)`. Default `--gif-shot`
  for streamer takes should point at a mistake shot — the gag is the
  README-able moment.
- **dub.py**: **no changes.** Time base untouched (§1.4); mistake lines
  are ordinary `line_start` events with text, snapped to video frames by
  the existing detector. With `lines-complete` enforced, the
  `(unscripted line)` dub-sheet rows should asymptote to zero.
- **dub sheet**: gains a `style` column (from `shot_start.style`) so the
  Suno arrangement pass can score mistakes differently (stab / record
  scratch / dead air are all viable under the deadpan).

---

## 5. Act One streamer screenplay — complete

Covers the full shipped Act One (scenes 01–05, the `full-run` scope).
Every `lines:` block below is verbatim from the `.scc` handlers, branch-
checked against game state at that point in the run. Inventory
compaction is tracked in comments (the NOTES.md pitfall). Estimated
runtime **≈ 14½ min** of footage vs ≈ 8 for the straight perform cut;
per-chapter subtotals in the section headers.

```yaml
# Clanker City Chronicles — Act One, as played by somebody curious.
# The streamer cut: every catalogued fair mistake gets tried on camera,
# gets its refusal, and the refusal is ASSERTED (this file is also the
# fair-mistake regression gate when run in validate mode).

title: "Clanker City Chronicles — Act One, Played Honest"
game: "--debuglevel=1 chronicles"
stage: docks.stage.json
transcript: docks.transcript.json

shots:
  # ============================ SCENE 01: THE DOCKS (~2:30) ============
  - name: arrival
    chapter: "SCENE 01  THE DOCKS"
    cutscene: DockRoom.entry
    expect: [talking]
    timeout: 60                                              # ~0:35

  - name: take-in-the-docks                                  # ~0:10
    wander:
      - walk: center-east
      - hover: ferry
      - idle: 1.5
      - hover: neon sign

  - name: my-ride                                            # ~0:06
    detour: {verb: Examine, object: ferry}
    lines:
      - The S.S. Eventually. My ride here, and apparently nothing's ride anywhere ever again.

  - name: morale-officer                                     # ~0:10
    detour: {verb: Talk to, object: ferry}
    lines:
      - Hang in there, buddy.
      - The foghorn wheezed. I'm choosing to hear that as optimism.

  - name: the-sign                                           # ~0:10
    do: {verb: Examine, object: neon sign}
    expect: [talking]

  - name: percussive-maintenance                             # ~0:12
    do: {verb: Use, object: neon sign}
    expect:
      - talking
      - pixel: {at: shiny bolt, is: bright-steel}

  - name: legal-tender                                       # ~0:08
    do: {verb: Pick up, object: shiny bolt}                  # bolt -> slot0
    expect:
      - talking
      - pixel: {at: inventory.slot0, is: bright-steel}

  - name: who-is-up-there                                    # ~0:12
    detour: {verb: Examine, object: Boom-Arm Betty}          # the O-I-L plant
    lines:
      - A cargo crane, frozen mid-lift. Or mid-yawn. Hard to tell.
      - The operator plate says 'BOOM-ARM BETTY'. Her eye-light is blinking in morse.
      - O... I... L. Yeah, Betty, we've all been there.

  - name: meet-betty                                         # ~0:12
    do: {verb: Talk to, object: Boom-Arm Betty}
    expect: [talking]
    hold: 1.5

  - name: civic-duty                                         # ~0:10
    do: {verb: Examine, object: notice board}
    expect: [talking]

  - name: take-the-evidence                                  # ~0:06
    do: {verb: Pick up, object: official notice}             # poster -> slot1
    expect:
      - pixel: {at: inventory.slot1, is: bright-steel}

  - name: destiny-up-a-crane                                 # ~0:10
    detour: {verb: Examine, object: crate}
    lines:
      - "Stenciled on the side: PROPERTY OF THE ORDER OF THE WIND-UP KEY."
      - Ominous AND conveniently plot-relevant. Also up a crane.

  # a reasonable wrong move, refused with a hint — pure streamer gold,
  # and it teaches the oil chain on camera
  - name: jump-for-it                                        # ~0:12
    mistake: {verb: Open, object: crate}
    lines:
      - "It's eight feet up. Fine: four. My arms are stock parts and the principle is load-bearing."
      - Betty could set it down, if anyone gave her a drink of oil.
    expect: [talking, lines-complete]

  # =================== SCENE 02: THE SCRAP & BARREL (~2:15) ===========
  - name: enter-the-tavern
    chapter: "SCENE 02  THE SCRAP AND BARREL"
    do: {verb: Open, object: tavern door}
    expect:
      - pixel: {at: [88, 9], is: magenta}
    timeout: 60

  - name: take-in-the-bar                                    # ~0:08
    wander:
      - hover: player piano
      - idle: 1.2
      - hover: Gusket

  - name: the-piano                                          # ~0:10
    do: {verb: Examine, object: player piano}                # the 3-keys plant
    expect: [talking]

  - name: top-shelf                                          # ~0:06
    detour: {verb: Examine, object: bottle shelf}
    lines:
      - Top-shelf lubricants. Literally. The bottom shelf is the same stuff with dust on it.

  - name: five-finger-discount                               # ~0:10
    detour: {verb: Pick up, object: bottle shelf}
    lines:
      - Gusket's eye is tracking me like a security camera.
      - Because it is one. There's a little red light.

  - name: talk-to-the-barman                                 # ~0:16
    detour: {verb: Talk to, object: Gusket}                  # pre-fix branch
    only: perform
    lines:
      - He says I look like I've had a hard drive, pal.
      - I ask about oil. He says oil is for paying customers and his last can rode off with the dart league.
      - He'd shake my hand, he says, but his arm's been polishing this glass since the Dynamo dimmed.
      - The servo's jammed. A little shim in the ratchet would free it.
    timeout: 60

  - name: certified-maintenance                              # ~0:25
    do: {verb: Use, object: Gusket, with: inventory.slot0}   # bolt consumed:
    expect:                                                  # poster->0, token->1
      - talking
      - pixel: {at: inventory.slot1, is: greens}
    timeout: 60

  - name: extremely-casual                                   # ~0:14
    do: {verb: Talk to, object: "rustlers' table"}           # knock-code (B9)
    expect: [talking]
    timeout: 60
    hold: 1.5

  - name: size-up-the-champ                                  # ~0:10
    detour: {verb: Talk to, object: Flange}
    lines:
      - "He says: darts, table stakes one drink token, house rules, he always wins."
      - The oil can on his belt is the wager. The smugness comes free.

  - name: the-dart-hustle                                    # ~0:35
    do: {verb: Give, object: Flange, with: inventory.slot1}  # token consumed:
    expect:                                                  # poster->0, oilcan->1
      - talking
      - pixel: {at: [284, 175], is: red}
    timeout: 90

  # ===================== SCENE 01 AGAIN: THE PAYOFF (~1:00) ===========
  - name: back-to-the-docks
    do: {verb: Open, object: door to the docks}
    expect:
      - pixel: {at: [10, 4], is: sky}
    timeout: 60

  - name: doctors-orders                                     # ~0:18
    do: {verb: Use, object: Boom-Arm Betty, with: inventory.slot1}
    expect:                                                  # oilcan consumed
      - talking
      - pixel: {at: [132, 56], is: sky}
    timeout: 60

  - name: the-first-key                                      # ~0:20
    do: {verb: Open, object: crate}                          # key -> slot1
    expect:
      - talking
      - pixel: {at: inventory.slot1, is: sodium}
    timeout: 60
    hold: 2.0

  - name: admire-the-key                                     # ~0:08
    detour: {verb: Examine, object: wind-up key}
    lines:
      - A brass wind-up key the size of my forearm. Somebody polished it for years. Somebody is going to want it back.

  # ---- FAIR MISTAKE 1: key-on-piano (editorial N-T1) ------------------
  # the piano is "missing three keys", I am HOLDING a key. Obviously.
  - name: a-theory-about-the-piano                           # ~0:08
    do: {verb: Open, object: tavern door}
    expect:
      - pixel: {at: [88, 9], is: magenta}
    timeout: 60

  - name: count-the-keys-again                               # ~0:10
    detour: {verb: Examine, object: player piano}            # REVISIT: explicit
    lines:
      - A player piano, playing itself. It's missing three keys.
      - ...That feels thematically significant.

  - name: try-the-key-on-the-piano                           # ~0:09
    mistake: {verb: Use, object: player piano, with: inventory.slot1}
    lines:
      - Wrong kind of key, wrong kind of missing.
    expect:
      - talking
      - lines-complete
      - pixel: {at: inventory.slot1, is: sodium}             # key NOT consumed
    hold: 2.4                                                # let the gag sit

  - name: fine-fine                                          # ~0:08
    do: {verb: Open, object: door to the docks}
    expect:
      - pixel: {at: [10, 4], is: sky}
    timeout: 60

  # ================ SCENE 03: THE RUSTLERS' ALLEY (~2:20) =============
  - name: into-the-alley
    chapter: "SCENE 03  THE RUSTLERS ALLEY"
    do: {verb: Open, object: alley mouth}
    expect:
      - pixel: {at: [76, 24], is: magenta}
    timeout: 60

  - name: meet-rivet                                         # ~0:25
    do: {verb: Talk to, object: Rivet}                       # welcome bundle
    expect: [talking]
    timeout: 60

  - name: the-wall                                           # ~0:08
    detour: {verb: Examine, object: graffiti}

  - name: message-discipline                                 # ~0:10
    detour: {verb: Open, object: steel door}
    timeout: 60

  - name: the-watcher                                        # ~0:10
    detour: {verb: Examine, object: fire escape}             # Rustler plant
    lines:
      - A fire escape, and on it a Rustler with a spyglass, pointed at the docks.
      - He's taking notes. I'm in the notes.

  - name: friendly-wave                                      # ~0:06
    detour: {verb: Talk to, object: fire escape}
    lines:
      - I wave up at him. He writes that down too.

  - name: nose-first                                         # ~0:06
    detour: {verb: Smell, object: dumpster}
    lines:
      - Banana oil and municipal despair.

  - name: dumpster-diving                                    # ~0:14
    do: {verb: Open, object: dumpster}                       # magnet -> slot2
    expect:
      - talking
      - pixel: {at: inventory.slot2, is: red}
    timeout: 60

  - name: back-out-front                                     # ~0:08
    do: {verb: Open, object: way to the docks}
    expect:
      - pixel: {at: [10, 4], is: sky}
    timeout: 60

  - name: gone-fishing                                       # ~0:14
    do: {verb: Use, object: storm drain, with: inventory.slot2}
    expect:                                                  # stash -> slot3
      - talking
      - pixel: {at: inventory.slot3, is: bright-steel}
    timeout: 60

  # ---- FAIR MISTAKE 2: wrong bolt to Gusket (editorial B1) ------------
  # Gusket BUYS bolts, right? I have NINE. This is an economy.
  - name: bolts-are-money-here                               # ~0:08
    do: {verb: Open, object: tavern door}
    expect:
      - pixel: {at: [88, 9], is: magenta}
    timeout: 60

  - name: offer-the-fistful                                  # ~0:12
    mistake: {verb: Give, object: Gusket, with: inventory.slot3}
    lines:
      - Harbor bolts. Brined stiff. The shim wants one dry and dock-fresh, he says.
      - The WELCOME sign sheds those, if a bot asks it firmly enough.
    expect:
      - talking
      - lines-complete
      - pixel: {at: inventory.slot3, is: bright-steel}       # stash returned
    timeout: 60
    # (yes — post-fix he points at a sign that already shed its bolt; the
    #  desk flagged the unconditional pointer in pass2. on film it plays
    #  as Gusket being Gusket.)

  - name: noted                                              # ~0:08
    do: {verb: Open, object: door to the docks}
    expect:
      - pixel: {at: [10, 4], is: sky}
    timeout: 60

  # ---- FAIR MISTAKE 3: nine bolts at the gate (editorial N-A1) --------
  - name: back-to-the-alley                                  # ~0:08
    do: {verb: Open, object: alley mouth}
    expect:
      - pixel: {at: [76, 24], is: magenta}
    timeout: 60

  - name: surely-this-is-enough                              # ~0:12
    mistake: {verb: Give, object: funicular gate, with: inventory.slot3}
    lines:
      - I feed it the fistful. It counts, blinks NINE, and returns the lot.
      - Smug, for a gate. Rivet would know where a tenth grows.
    expect:
      - talking
      - lines-complete
      - pixel: {at: inventory.slot3, is: bright-steel}       # the lot, returned
    timeout: 60
    hold: 2.6                                                # NINE. sit with it.

  - name: the-riddle-duel                                    # ~0:35
    do: {verb: Talk to, object: Rivet}                       # tenth -> slot4
    expect: [talking]
    timeout: 90

  - name: pay-the-fare                                       # ~0:20
    do: {verb: Use, object: funicular gate}                  # stash+tenth consumed:
    lines:                                                   # poster0 key1 magnet2
      - Ten bolts in the hopper. It counts them twice. Trust died in this town years ago.
      - The gate ratchets up, and a little brass car rolls down to meet me, lit up like a promise.
    expect:
      - talking
      - pixel: {at: [284, 70], is: sodium}
    timeout: 90
    # explicit lines: REVISIT of (gate, Use) — front-pairing forbidden here

  - name: now-boarding                                       # ~0:08
    do: {verb: Examine, object: funicular gate}
    lines:
      - Gate's open, car's lit. Midtown keeps glittering like it doesn't know I'm coming.
    expect: [talking]
    timeout: 60
    hold: 2.5                                                # chapter close

  # ================ SCENE 04: MIDTOWN GEARWORKS (~2:00) ===============
  - name: ride-uptown
    chapter: "SCENE 04  MIDTOWN GEARWORKS"
    do: {verb: Use, object: funicular gate}
    lines:
      - Uptown. I can hear the neon from here.
    expect:
      - talking
      - pixel: {at: [180, 30], is: sodium}
    timeout: 90

  - name: main-street                                        # ~0:10
    wander:
      - walk: midtown-center
      - hover: the Great Dynamo
      - idle: 1.6
      - hover: City Hall

  - name: meet-the-clerk                                     # ~0:15
    do: {verb: Talk to, object: box office}
    expect: [talking]
    timeout: 60

  - name: the-dynamo                                         # ~0:10
    detour: {verb: Examine, object: the Great Dynamo}

  - name: nothing-is-wrong                                   # ~0:08
    detour: {verb: Examine, object: City Hall}

  - name: nine-degrees                                       # ~0:08
    detour: {verb: Open, object: City Hall}

  - name: a-velvet-rope-for-robots                           # ~0:10
    detour: {verb: Examine, object: the Oil Bar}             # plants the rope
    lines:
      - The Oil Bar. Uptown filtered, triple distilled, quadruple priced.
      - There's a velvet rope. For robots. To stand behind. Voluntarily.

  - name: try-the-door-anyway                                # ~0:12
    detour: {verb: Use, object: the Oil Bar}                 # bouncer, take 1
    lines:
      - A bouncer the size of a vending machine looks at my dock rust and invents a dress code.
      - I'm on the list, I tell him. He shows me the list. It's a picture of the door.
    hold: 2.0

  - name: the-act                                            # ~0:25
    do: {verb: Use, object: box office, with: inventory.slot1}
    expect:
      - talking
      - pixel: {at: [182, 50], is: sodium}
    timeout: 90

  - name: in-lights                                          # ~0:10
    do: {verb: Examine, object: Grand Cog Theater}
    expect: [talking]
    timeout: 60
    hold: 2.5

  # ================== SCENE 05: TALENT NIGHT (~2:45) ==================
  - name: enter-the-grand-cog
    chapter: "SCENE 05  TALENT NIGHT"
    do: {verb: Open, object: Grand Cog Theater}
    expect:
      - talking
      - pixel: {at: [110, 12], is: sodium}
    timeout: 90

  - name: the-emcee                                          # ~0:12
    do: {verb: Talk to, object: the emcee}
    expect: [talking]
    timeout: 60

  - name: tough-room                                         # ~0:08
    detour: {verb: Talk to, object: the audience}

  - name: house-lights                                       # ~0:10
    do: {verb: Use, object: spotlight booth}
    expect: [talking]
    timeout: 60

  - name: the-amazing-sprocket                               # ~1:00
    do: {verb: Use, object: the stage, with: inventory.slot1}
    expect:                                                  # key STOLEN mid-ovation:
      - talking                                              # poster0 magnet1
      - pixel: {at: [220, 40], is: teal}                     # voucher2 pass3
      - pixel: {at: inventory.slot2, is: sodium}
    timeout: 150
    hold: 2.5

  # ---- FAIR MISTAKE 4: voucher at the rope (editorial N-M4) -----------
  # I am a PRIZEWINNER holding a PREMIUM OIL VOUCHER and there is exactly
  # one establishment with a rope. Cash me out.
  - name: read-the-fine-print                                # ~0:10
    detour: {verb: Examine, object: oil voucher}
    lines:
      - GOOD FOR ONE PREMIUM OIL SERVICE. Valid at participating establishments.
      - The only establishment that participates has a velvet rope.

  - name: out-to-the-street                                  # ~0:06
    do: {verb: Open, object: lobby doors}                    # silent transition
    expect:
      - pixel: {at: [180, 30], is: sodium}                   # marquee = Midtown
    timeout: 60

  - name: cash-it-in                                         # ~0:14
    mistake: {verb: Give, object: the Oil Bar, with: inventory.slot2}
    lines:
      - The bouncer reads it. Valid, he admits. The rope, he explains, is a separate financial instrument.
      - Tonight it's at capacity. The rope. Is at capacity.
    expect:
      - talking
      - lines-complete
      - pixel: {at: inventory.slot2, is: sodium}             # voucher kept
    timeout: 60
    hold: 2.8                                                # the act's best refusal

  - name: back-inside                                        # ~0:08
    do: {verb: Open, object: Grand Cog Theater}              # re-entry is silent
    expect:                                                  # (visitedTheater gate)
      - pixel: {at: [110, 12], is: sodium}
    timeout: 90

  - name: stage-door                                         # ~0:12
    do: {verb: Open, object: stage door}
    expect: [talking]
    timeout: 60
    hold: 2.5
```

Chapter subtotals: 2:30 + 2:15 + 1:00 + 0:35 (piano leg) + 2:20 + 0:30
(Gusket leg) + 1:25 (gate→fare) + 2:00 + 2:45 ≈ **14:20** of footage +
6 s of cards. Estimates assume ≈ 2.6 s/line + 1.6 s settle + holds;
cutscene figures taken from `full-run` take experience.

Verification before first perform: one `validate` run of this file
(mistake shots assert in validate), plus a console scan for `SNTC` lines
on the four mistakes confirming dispatch — both already supported by the
diff list below.

---

## 6. Driver diff list

`walkthrough/driver/walkthrough.py`:

1. **`normalize_shot(shot)`** (new, called once over
   `screenplay["shots"]`): expand `detour:` / `mistake:` / `wander:`
   sugar into canonical `{style, do, only, lines, pre, hold, expect}`;
   apply style defaults from §1.3; `mistake` without `lines:` is a
   screenplay error (hard fail at load).
2. **`LineBook`** (new class, replaces `shot_lines`): explicit
   `shot["lines"]` wins; else first-visit front-pairing from the
   transcript with a `visited[(object, case)]` set; repeat visit without
   `lines:` → warning in perform, failure in validate. Cutscene path
   unchanged.
3. **`run_shot`**: honor `pre:` (perform-mode sleep before the first
   click); after `watch`, if `lines-complete` ∈ expect, compare
   `count_segments() - seg_base` to `len(lines)` and `take.fail` with
   observed-vs-declared on mismatch; pass `style` into
   `take.log("shot_start", …)`.
4. **`sentence` expectation** (optional): record console length at
   `shot_start`; after the shot, scan new console entries for
   `SNTC <verb-id>/<objA>/<objB>` matching the shot (needs
   name → object-id map added to the stage JSON by `tools/genassets.py`).
5. **Wander executor** (new `run_wander(steps)`): `walk` → click +
   `_wait_arrival` (poll `sprocket-body` probe within radius of target,
   8 s timeout, 2.5 s fallback); `hover` → `_page_xy` + `mouse.move` +
   0.9 s dwell, no click; `idle` → sleep; log `wander_step` events;
   skipped entirely in validate.
6. **Chapter events**: `chapter:` on a shot logs
   `{"type": "chapter", "title": …}` at shot start.
7. **`write_dub_sheet`**: add a `style` column from `shot_start` events.

`walkthrough/post/render.py`:

8. **Chapter lower-thirds**: collect `chapter` events; generalize
   `make_card` into `make_strip` (FONT3 on transparent PNG); overlay
   each for 3 s via one ffmpeg `overlay=enable='between(t,…)'` chain on
   `main_mp4`. No concat changes; `render.json` unchanged.
9. **`--gif-shot`**: no code change, but streamer takes should pass a
   mistake shot (e.g. `surely-this-is-enough`).

`walkthrough/post/dub.py`:

10. **No changes** (the overlay-not-insert chapter decision exists
    precisely to keep `film_t` and the bed alignment intact).

`tools/genassets.py` / stage map:

11. Emit object ids alongside hotspots (for diff #4); `walk_targets`
    already suffice for wander.

Out of scope (noted for later): speaker-color pairing (single-narrator
game — no signal today), per-branch transcript extraction in
`tools/transcript.py` (explicit `lines:` makes it unnecessary), and the
dialog-tree UI work (NOTES.md next-step #1) which will need a new
`choose:` shot type when the contests become playable.