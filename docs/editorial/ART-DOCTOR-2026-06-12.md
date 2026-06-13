# ART DOCTOR — NPC cast exam, 2026-06-12

Visit type: DIAGNOSIS ONLY (genassets.py contended by two mid-merge branches;
no edits performed). Patients: the full painted NPC cast + Sprocket's frames,
examined as rendered BMPs at 3x–8x against the house style, the draw_* code,
the speech-era talk-color law (PAL 108–112), and the screenplay probe set.

All genassets.py line refs are against the current working tree (1769 lines).
Driver refs are walkthrough/driver/walkthrough.py.

---

## Systemic findings (these gate the whole speech rollout)

### SYS-1 · BLOCKER — The talk-color near-collision build assert does not exist
NPC-DIALOG.md §4 item 1 requires "a build-time assert that no room image rows
0-104 contain near-collisions with any talk color (the piano-keys bug class)."
genassets.py contains **zero asserts** (verified by grep). The palette comment
at genassets.py:61-62 cites the requirement; nothing enforces it. Every other
finding below was found by hand-running exactly the scan the assert should do.
- **Prescription**: in `main()` (genassets.py:1629), after each room render,
  scan rows 0-104 against PAL[105], PAL[106], PAL[108..112] with per-channel
  tolerance TOL(16, walkthrough.py:41) **plus a VP8 margin (+8)** and fail the
  build on any hit. ~15 lines. This is the first thing to land post-merge.
- Affected: build only. No rects, no probes.

### SYS-2 · BLOCKER — PAL[112] (EXTRA) is a near-twin of PAL[105] (SPROCKET)
PAL[105]=(255,190,80) at genassets.py:58; PAL[112]=(255,170,90) at :67.
Δ=(0,20,10) — the G channel exceeds driver TOL by only 4 and the dub reads
VP8 4:2:0 footage (the palette's own comment, :61-62, warns about exactly
this). `talk_mask` (walkthrough.py:216-235) tests families **first-match with
break**, sprocket family first — so a clerk/bouncer/heckler/slot-eye line that
smears 4 units in G classifies as *Sprocket*, silently corrupting speaker
attribution, segment signatures, and the dub CAST routing. The slot-eye is
conversion target #1 (NPC-DIALOG §5 rank 2) and it speaks in EXTRA_COLOR —
this lands directly on the rollout's critical path.
- **Prescription** (per NPC-DIALOG §7 Q7): retire the vestigial
  `BETTY_COLOR 106` / "talk-2" and give the EXTRA pool 106's RGB
  (140,220,255) — maximally far from 105 in hue, already plumbed through the
  whole observation stack. Touches: PAL[112] or `#define EXTRA_COLOR`
  (game/common.sch:86, currently 112), STAGE_PROBES `"talk-extra"` and
  `"talk-2"` (genassets.py:1566, :1573), `talk_mask` sprocket-family union
  (walkthrough.py:221-222 — talk-2 must leave the sprocket family), and
  actors.scc:52 (`setActorTalkColor(EXTRA_COLOR)` follows the define).
- Affected probes: stage-map `probes` block (regenerate with --emit-stage).
  No screenplay YAML references talk-extra yet — convert before the slot-eye
  lands, and this is free.

### SYS-3 · BLOCKER — Driver classifies talk pixels first-match, not nearest-color
STAGE_PROBES' comment (genassets.py:1567-1568) claims "the driver classifies
talk pixels by nearest color" — the code does not (walkthrough.py:227-233:
independent per-color `near()` tests, `break` on first family). NPC-DIALOG §4
item 3 specifies nearest-color over the full set. The comment is currently a
lie, and first-match ordering is what turns SYS-2's near-miss into silent
misattribution instead of a detectable tie.
- **Prescription**: implement nearest-color classification in `talk_mask`
  (~10 lines) before the first NPC conversion take is trusted; until then
  treat any dub speaker column as unverified.

### SYS-4 · NOTE — Talk-color/character color-rhyme is absent for 3 of 5 speakers
The player's only speaker cue is text color. The paint rhymes for the emcee
(gold eyes ≈ footlight yellow) and the extras' clerk (orange booth, PAL 24)
but NOT for Gusket (green text; zero green on him), Rivet (violet text; zero
violet), or Voltina (pink text; zero pink). Speech-era readability wants one
talk-hued accent per speaker, using **dark-ramp cousins** so SYS-1's assert
stays green:
- Gusket: contents of the polished glass (genassets.py:438) → 86 (110,212,110).
- Rivet: the mood-screws (:643-645, currently steel 12) → 96 (185,89,197) —
  "sorting screws by mood" gets funnier, and violet appears on him.
- Voltina: see VOL-2 below.
All three are mask-safe (min per-channel Δ vs their talk colors: 43, 51, 40).

---

## Per-patient charts

### 1. Boom-Arm Betty — docks (draw_scene, genassets.py:217-228)
**BLOCKER (character-vs-blob)**: Betty fails the character exam. She is a
crane with a 1-pixel near-black "eye" (`im.putpixel((cx+17,cy+7), 1)`, :226)
set in a cab window filled 44 (:225) — and PAL[44]=(137,119,60) renders as
dead olive-khaki, not a lit window. At 3x the eye is invisible and the cab
reads as cargo, yet the script gives her a name, three Look-At beats, and the
whole oil-voucher transaction (docks.scc:261-359, "the gentleness of a very
large aunt"). The fiction sells a personality the paint refuses to show.
- **Prescription**: invert the values — window fill 1 (dark glass), eye 2x2
  fill 49 (221,205,124, lit), and one antenna pixel on the cab roof. 3 lines
  at :225-226. Mask-safe (49 vs 105: ΔR=34; vs 110: ΔG=50).
- Affected: nothing. CRANE rect (109:112) has no state crops; stage-map
  hotspot derives from GEOM center, unchanged; no screenplay probe touches
  the cab.
- **NOTE (future speech)**: `BETTY_COLOR 106` is being recommended for
  reassignment to the extras (SYS-2). If Betty ever speaks, her text clamps
  from x=66 to x=80 and lands on the CLANKER CITY sign's teal neon
  (:200, color 37) — cyan-on-cyan. Pick her a warm color and a parking spot
  left of the sign when that day comes.

### 2a. Gusket — tavern (draw_tavern, genassets.py:427-441)
**Reads as a character**: barrel body + hoops + cap + the eternal
glass-polishing loops all land. Two findings:
- **NOTE**: eyes fill 44 (:434-435) — the same dead-khaki problem as Betty.
  His head is the darkest thing behind the bar and his green talk text will
  point at a bot with no visible light in him. Bump eyes to 47, and add the
  SYS-4 green accent (glass contents 86 at :438).
- **NOTE (talk headroom)**: gusket_a will park at the bar (T_GUSKET
  64,48,32,40); text overhead lands across the bottle shelves (:404-413) —
  six bottle colors plus 104-white glints, the busiest surface in the room.
  Readable but noisy; one mitigating option is parking him 4px lower so text
  catches the shelf-board band. Not worth repainting shelves over.
- Affected by eye fix: nothing (no state crops in T_GUSKET, no probes).

### 2b. Flange — tavern (genassets.py:492-503)
**Passes**: hard-hat 45 + teal eyes 31 + dart mid-throw = posture, prop,
accent. Two NITs:
- **NIT**: the "tool belt" (:495) is fill 9 — that's mid-STEEL in the room
  palette, an invisible gray-on-gray stripe. The comment thinks 9 is rust
  (it is in the COSTUME window, not the room palette). Use 24 (rust-orange)
  so the belt exists.
- **NIT (doc)**: NPC-DIALOG.md §3 table says "Flange (docks)". He is painted,
  named, and hustling darts in the **tavern** (T_WORKER). Fix the row.

### 2c. The three Rustlers — tavern card table (genassets.py:461-480)
**NOTE (character-vs-blob + cross-room consistency)**: three armless rust
boxes (:475-477) whose heads (20) barely separate from bodies (18) — Δ is two
steps of the same ramp. The captain's hat (:478-480) is the only posture in
the scene the script calls "mid-argument." Worse: the gang's identity marker
is incoherent. The fire-escape lookout (alley, :622-627) and the catwalk
watcher (theater, :953-957) are black silhouettes with a single **red eye
(107)** — a strong, repeatable "Rustler = one red eye" code. At the table,
only Rustler #1 has the red eye; #2 wears 44 (khaki), #3 wears 31 (teal)
(:472-474). Meanwhile the theater audience hands out 107-red eyes to two
random patrons (:921 eye pool) — diluting the code further.
- **Prescription**: (a) all three table Rustlers get 107 eyes (vary eye
  *position*, not color, for individuality — they keep the hat and the
  body-height stagger); (b) give each a 1px arm-line toward the pot (the
  argument); (c) remove 107 from the audience eye pool at :921 (swap for 41
  amber — the pool keeps five entries). 6-8 lines total.
- Affected: nothing — no state crops in T_TABLE or G_AUDIENCE, no probes.
  (The knock-code line, NPC-DIALOG rank 7, is optional EXTRA-pool speech;
  red-eye coherence matters before that lands, not before the emcee.)

### 3. Rivet — alley (draw_alley, genassets.py:629-645)
**Passes — best character in the cast**: round silhouette, mismatched plate
wedges, big lens eye, mood-screw piles. Findings:
- **NOTE**: lens 44 again (:637) — the third dead-khaki "light" in the cast.
  Lens to 46/47 keeps the warm look and actually glows.
- **NOTE (SYS-4)**: mood-screws (:643-645) → 96 violet, his talk color rhyme.
- **Talk headroom: CLEAN** — bare rust wall above A_RIVET; violet on rust is
  the best text contrast in the game. Rivet (rank 4) needs no paint to speak.
- Affected: nothing (A_RIVET has no state crops; no probes).

### 4a. Box-office clerk — midtown (draw_midtown, genassets.py:806-813)
**Passes as the gag** ("6px sprite in booth — flap impossible; that's the
gag", NPC-DIALOG §3, confirmed intentional pending §7 Q6).
- **NOTE**: booth window fill 44 (:809) — the khaki problem again; the booth
  should be the one *lit* thing under the marquee. Window to 46, clerk block
  stays 6, eye 31 stays. The orange booth (24) already rhymes with the extras'
  current orange — if SYS-2 moves the extras to cyan-blue, the clerk's eye
  (31, teal) becomes the rhyme instead. Convenient.
- **NOTE (talk headroom)**: the booth sits directly under the marquee;
  clerk text (two converted lines, midtown.scc:234,236) will print over
  "TALENT NITE" in 104-white (:800) — text-over-text mush. Mitigation at
  conversion time: park extra_a at the booth's y-bottom so one-line text falls
  in the facade band (y 64-72) between marquee and window. Flagging now so
  the conversion doesn't discover it on camera.
- Affected by window recolor: M_THEATER state crops (marquee_blank/
  marquee_sprocket) do NOT include the box office (non-overlapping rects,
  comment :696-698) — safe. Screenplay probes (180,30)/(182,50) are marquee
  text rows — untouched.

### 4b. The Oil Bar bouncer — midtown (genassets.py:765-781)
**NOTE (fiction disagreement)**: midtown.scc:140 — "A bouncer the size of a
vending machine looks at my dock rust and invents a dress code." **No bouncer
is painted.** The rope (:777-781) guards an empty doorway; the voucher beat
(:156, "the rope is a separate financial instrument") plays against nobody.
He is also a future EXTRA-pool speaker with no body to park text over.
- **Prescription**: paint a vending-machine bot in the left band of M_OILBAR
  (x ox..ox+13 is free wall, :766-771): boxy 2-wide silhouette in 5/6 steel,
  one coin-slot mouth-slit (1), one eye 31, one item-button glint 94 to echo
  the OIL neon. ~6 lines after :771. Mask-safe trivially.
- Affected: nothing — M_OILBAR has no state crops, no probes point inside.

### 5. THE EMCEE — theater (draw_theater, genassets.py:933-946) — first speaking NPC
He is already live: `actorSay(emcee_a, …)` at theater.scc:255,261,267, parked
at (140,102) (theater.scc:59) — dead-center of his painted figure (ex+12=140,
feet ey+48=104). Position agreement: exact. The tux thesis reads at 3x: black
body, white shirt vee, gray head. The fiction (theater.scc:249: "Tuxedo paint
job, telescoping mic arm") is HALF delivered:
- **NOTE — the mic arm doesn't read.** One thin 6-gray diagonal (:943) ending
  in a fill-2 near-black lump (:944) against a dark rust wall. At 3x the prop
  that the script points at twice (:249, :273 "He points his mic arm at the
  booth") is invisible. Prescription: telescoping segments — split the arm
  into two strokes (6 then 11), mic head to 5 with a 1px 45 windscreen glint.
  2-3 lines at :943-944. The arm tip (ex+28=156) stays clear of G_STAGE
  (x≥160) — curtain state crops unaffected.
- **NOTE — eyes are dim khaki (45, :941-942).** He speaks in footlight yellow
  (110); his eyes are the player's speaker-attribution anchor and the rhyme
  is the right idea executed too dark. Bump to 49 (221,205,124): reads lit,
  Δ vs PAL[110] = (34,50,4) — mask-safe per-channel.
- **NIT — the bow tie is a misplaced red button.** :938 puts the single 107
  pixel at (ex+12, ey+18), mid-sternum inside the shirt vee. A bow tie lives
  at the collar: move to ey+15 and widen to 3x1. One line.
- **Talk headroom: GOOD.** Bare rust wall from y24 to his hat (y58) across
  the full clamp range — yellow-on-dark-rust is excellent. Only multi-line
  wraps could graze the chandelier's sodium bulbs (y≤24, :890-895); his
  converted lines are short (≤12-word rule). The screenplay's chandelier
  probe (full-run:228,363 at (110,12), "is: sodium") is evaluated only when
  `not talking` (walkthrough.py:351) — no probe interaction.
- Affected by all three fixes: nothing — G_EMCEE has no state crops; no
  screenplay pixel probe enters (128,56,24,48). Cheapest possible upgrades to
  the cast member whose readability now matters most.

### 6a. The audience — theater (genassets.py:914-931)
**Passes**: rows of black heads with varied eye-dots over seat backs reads
exactly as "professionally unimpressed"; juggler and foghorn singer are
legible micro-gags. One change, already prescribed in 2c: remove 107 from
the eye pool (:921) to protect the Rustler red-eye code. NIT: the singer's
horn-mouth (outline 18 on wall 17, :931) is one step of contrast from
existing — outline 9 if anyone is in the file anyway.

### 6b. The spotlight operator — theater (genassets.py:905-912)
**NOTE (deliberate blob, slightly over-achieved)**: the operator (:909) is a
5-gray block whose "dim eye" fill 2 (:910) is invisible against the 1-black
window — the low-power gag (theater.scc fiction: "went into low-power mode
during the juggler") currently reads as *no occupant at all*, which undercuts
Use-spotlight-booth being a puzzle verb (full-run:242). Prescription: the eye
gets one 16-dark-rust ember pixel — asleep, not absent. One line at :910.
The lamp's dead center (fill 8 steel, :912) could be 41 (dark sodium ember)
for the same "banked fire" read. No crops, no probes touched.

### 6c. The catwalk watcher — theater (genassets.py:953-957)
**Passes** (matches the alley lookout: black body, red eye, spyglass) with
one **NIT**: the lookout's spyglass has a teal lens glint (alley :627,
color 31); the watcher's does not (:957). Add `im.putpixel` at the spyglass
tip, color 31, for gang-kit parity.
- **Affected — flag**: the watcher lives inside G_CATWALK (168,0,104,16) →
  this edit regenerates **catwalk_watch.bmp** (state crop, genassets.py:1689).
  catwalk_empty.bmp re-renders identically (watcher=False). The theater.scc
  catwalk object states must be re-imported on next build; no screenplay
  probe reads the catwalk.

### 7. MADAME VOLTINA — backstage (draw_backstage, genassets.py:1119-1134)
The concept is the best in the game — "a tesla coil in a shawl. She's the
ball." Dome with filament (:1128-1132) is excellent. But:

- **VOL-1 · BLOCKER (silhouette)**: her shawl is fill 19 (:1122-1123) on a
  parlor curtain of fill 18 with 20 stripes (:1060-1062) — adjacent steps of
  the same rust ramp. At 3x she has no silhouette: the dome and rings float
  disembodied on the curtain. Painted fix: shawl to 1/near-black with a 19
  rim-light edge — and this matters MORE for the costume era, see VOL-3.
- **VOL-2 · NOTE (accent/talk rhyme)**: her talk color is tesla **pink**
  (109); her paint has zero pink. The fuse brooch (:1127) is one 107 pixel
  *sitting on a brass coil-ring row* — invisible. Prescription: brooch 2x2 at
  97 (203,100,204), moved 2px off the ring line. Mask-safe vs 109
  (ΔR=52). The 104-white insulator "earrings" (:1133-1134) read as stray
  noise pixels at 3x — fold them to 11 or drop them.
- **VOL-3 · What the costume conversion needs from this paint** (she becomes
  the first costumed actor; talk frames = tesla-coil arcs, NPC-DIALOG §3):
  1. **A painted-out background variant.** The costumed actor will draw OVER
     the painted Voltina — double-exposure. `draw_backstage` needs a
     `voltina=False` param (skip :1119-1134) and the room must ship without
     her, or B_VOLTINA (148,28,48,52 — already an object rect per :1006-1009)
     gets a "vacant parlor" state crop. **Landmine**: her shawl's bottom row
     (y=80, x160-184, polygon :1122) lies INSIDE the B_TABLE crop
     (136,80,72,32) — painting her out changes the top row of **all five
     table_*.bmp state images** (:1703-1711). Re-import all five; the
     screenplay card probes (full-run:290,303,311 at y89-90) sit 9px below
     the changed row — unaffected, but re-run validate.
  2. **Costume window additions** (genassets.py:71-84; 12 of 32 slots used,
     20 free at 236+): she needs BRASS (coil rings — no brass exists in the
     window; add ~(171,154,85)≈PAL[46]), a DARK SHAWL color distinct from
     both curtain rust and Sprocket's teal shadow, and her PINK accent
     (~(203,100,204), mask-safe). The arc/talk-frame color is already there:
     COST+10 "mouth light" (90,240,230) ≈ PAL[39], the same value as her
     painted filament — the tesla arcs cost zero new slots.
  3. **Geometry**: her painted figure is ~28x52 vs Sprocket's 20x34 canvas —
     her costume needs a taller canvas with ~4px of empty headroom above the
     dome for arc frames to flail in. Feet/park position: painted bottom is
     y=80 (she's behind the table, which starts at y=82) — putActorAt
     (172, 80) + setActorIgnoreBoxes, or box-snapping drags her onto the
     floor walkbox and in front of her own table.
  4. **Dome teal**: COST+2/3/4 are Sprocket's body teals. Sharing them is
     palette-cheap but identity-expensive; with 20 free slots, give her dome
     its own deeper teal and keep Sprocket's triad his.
- **Talk headroom: GOOD.** Pink over dark curtain/brick, centered x≈172 —
  clean. (See SYS/GHOST below for the one hazard in this room.)

### 7b. The ghost light — backstage (genassets.py:1088-1099) — speech-era hazard
**NOTE (escalates to BLOCKER when Scene 06 speech lands)**: the lit globe
(:1095 fill 50, :1096 hot-pixel 51) is the only paint in any room that
approximates a talk color: PAL[51]=(255,240,150) vs EMCEE 110 (255,255,120),
Δ=(0,15,30) — inside driver TOL on R and G, 14 units of VP8 chroma smear from
a full false-positive. The globe's hot pixel (96,56) sits ON the talk_mask
scan grid (even/even, walkthrough.py:229-230), and the ghost light *flickers*
(lit/dark states) — during Voltina's lines this is a machine for spurious
mask-signature changes and "emcee" misattribution in her scene.
- **Prescription**: lit globe fill 48 (204,188,111), hot pixel 49; halo
  outline 44 stays. Two value changes at :1095-1096.
- Affected: regenerates **ghost_lit.bmp** (state crop :1715); ghost_dark
  untouched; no screenplay probe reads the ghost (verified — jar probes at
  (256,68) are brass/teal). SYS-1's assert is what makes this class of bug
  impossible to reintroduce.

### 8. Sprocket's frames — assets/generated/sprocket/frames/ (genassets.py:1233-1319)
The same exam, protagonist edition:
- **Passes**: silhouette chunky and readable at 3x; one accent (lamp yellow
  eyes/gauge/antenna) consistently held; talk mouth (COST+10) is the
  sanctioned deliberate mouth per canon; N-facing frames correctly show no
  face. Walk cycle A/B/C/D reads.
- **NIT (palette, speech-era)**: costume LAMP (255,210,70) vs his own talk
  color 105 (255,190,80): Δ=(0,20,10) — the same near-miss class as SYS-2.
  His eye/gauge pixels are in talk_mask's scan rows wherever he stands;
  only the ≥6-position threshold (walkthrough.py:322) and the step-2 grid
  keep his own eyes from registering as speech. Lived-with today; if SYS-2's
  re-pick happens, nudge LAMP to (255,215,55) in the same commit and the
  whole orange neighborhood is clean.
- **NIT**: `talk_*_01` frames are pixel-identical to `stand_*` (mouth-closed
  = SHAD, :1292/:1296), and `talk_N_00`/`talk_N_01` are identical to each
  other (the `talk` flag is a no-op for facing N). Correct behavior, wasted
  bytes; harmless. No action.
- **Voltina relevance**: the talk-limb pattern here (2-frame mouth swap) is
  the proven template her arc frames copy (NPC-DIALOG §6 step 10).

---

## Prioritized treatment plan (ordered by what unblocks NPC speech)

| # | Sev | Treatment | genassets.py | Else touched |
|---|-----|-----------|--------------|--------------|
| 1 | BLOCKER | SYS-1 build assert (rows 0-104 vs talk colors, TOL+8) | main(), ~:1629 | — |
| 2 | BLOCKER | SYS-2 EXTRA color re-pick (take 106, retire talk-2) | :67, :1566, :1573 | common.sch:80,:86; walkthrough.py:221-222; re-emit stage map |
| 3 | BLOCKER | SYS-3 nearest-color talk_mask (make :1567 comment true) | — | walkthrough.py:227-233 |
| 4 | NOTE | Ghost-light recolor 50/51→48/49 (pre-Scene-06 speech) | :1095-1096 | ghost_lit.bmp re-import |
| 5 | NOTE | Emcee package: eyes 45→49, mic-arm telescoping + glint, bow tie to collar | :941-944, :938 | — (first speaking NPC; he's live NOW) |
| 6 | BLOCKER* | VOL-1 shawl silhouette + VOL-3.1 `voltina=False` variant | :1119-1134, main() | table_*.bmp x5 re-import, backstage.scc vacant state, validate re-run (*blocks her costume conversion, not the Tier-A rollout) |
| 7 | NOTE | VOL-3.2 costume window: brass + shawl + pink slots (arcs free via COST+10) | :71-84 | her future .scost |
| 8 | NOTE | Clerk booth window 44→46; conversion-time text-parking note (marquee mush) | :809 | midtown conversion checklist |
| 9 | NOTE | Slot-eye headroom: alley door text vs graffiti; tavern back-door text vs dartboard — park positions chosen at conversion | — | alley/tavern conversion checklist |
| 10 | NOTE | Betty: window/eye inversion + lit eye | :225-226 | — |
| 11 | NOTE | Oil Bar bouncer painted (fiction debt, future EXTRA speaker) | after :771 | — |
| 12 | NOTE | Rustler red-eye standardization + arms; audience pool drops 107 | :472-480, :921 | — |
| 13 | NOTE | Dead-khaki light sweep: Gusket eyes 44→47, Rivet lens 44→46 (+SYS-4 rhymes: glass 86, screws 96, brooch 97) | :434-435, :438, :637, :643-645, :1127 | — |
| 14 | NIT | Watcher spyglass glint (catwalk_watch.bmp re-import), Flange belt 9→24, spot-op ember eye, Voltina earrings, NPC-DIALOG "Flange (docks)" row | :957, :495, :910, :1133-1134 | docs/research/NPC-DIALOG.md §3 |

Items 1-3 are one sitting and make every later color decision checkable;
nothing else should merge into the speech pipeline before them. Item 5 is the
only paint the *currently live* speaking NPC needs. Item 6 is the long pole
for Voltina and can start the moment genassets.py settles.

— the art doctor
