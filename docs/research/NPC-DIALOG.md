# NPC direct speech — design doc

Synthesis of four investigations (engine, animation, voices, writing),
2026-06-12. Decides mechanism, animation, dub pipeline, and writing
doctrine for letting NPCs speak their own lines.

## 1. Executive summary

Give each named NPC a **costume-less real actor** (`actorSay` + per-NPC talk
color + `putActorAt` over the painted figure) — colored text over the NPC's
head, no art, no background repaint, ~6 lines of script per NPC.
**No talk animation at launch**; Madame Voltina becomes the first costumed
actor when Scene 06 is built, and optional 2-frame object-state mouth flaps
can be layered onto Gusket/Flange/Rivet later without rework.
**Voices**: per-speaker piper models + FX via a `CAST` table in dub.py, with
speaker attribution read off talk colors by both observers.
**Writing**: reported speech stays the default; NPCs get short direct
punchlines only (≤12 words, no double-telling), converted scene-at-a-time
in the ranked order below, starting with the slot-eye.
The real cost is the pipeline (transcript/driver/dub are hardcoded to
"all speech is egoSay in 105/106") — that bill is paid once, by every
option equally, so land it first and prove it on one cheap conversion.

## 2. Engine mechanism

**Chosen: per-NPC costume-less actors ("Tier A").** `actorSay` is already a
ScummC builtin (opcode 0xBA, vendor/scummc/scc_func.h:787) routed to
`o6_talkActor` → `actorTalk` (vendor/scummvm-src/engines/scumm/script_v6.cpp:223,
:2835; engines/scumm/actor.cpp:3466). For an actor in the current room the
engine uses the actor's own `_talkColor` (actor.cpp:3526) and positions text
overhead from the actor's coordinates (string.cpp:1056-1081, clamped
x∈[80,w−80]); `startAnimActor` is guarded by `_costume != 0`
(actor.cpp:2737), so a costume-less actor talks with no animation and no
crash. Per NPC: an `actor` decl + `#define <NPC>_COLOR` (common.sch),
`setActorTalkColor` in setupActors (actors.scc), `putActorAt(npc, x, y, room)`
in the room entry script. The painted background NPC stays untouched. The
multi-actor plumbing is inherited from openquest and dormant in this repo:
`actorObject[]` click routing (game/common.scc:58-62, :362-365), print-slot
defaults (game/common.scc:404-406, :593-597), and the vestigial
`BETTY_COLOR 106` (game/common.sch:62) — a fossilized intention to do
exactly this. Budget is a non-issue: the `tentacle` target gives 13 actor
slots (scumm.cpp:1734), `dimInt(actorObject,0x10)` (common.scc:584) caps
ids at 15; six named NPCs fit.

**Rejected — print-at, no actor (engine Option A).** `print` with
`_actorToPrintStrFor = 0xFF` (script_v6.cpp:2809-2812) works —
`waitForMessage()` timing intact (actor.cpp:3532) — but text is
screen-pinned (printAt per call site), the transcript gains a third speech
form to parse, and SO_END after printAt persists position overrides into the
talk slot default (script_v6.cpp:3721-3723), a stale-position landmine
mid-cutscene. It saves nothing: the pipeline cost is identical and a
costume-less actor is the same six lines with overhead tracking for free.

**Rejected — one shared "speaker puppet" actor (engine Option B).** A single
relocatable actor (putActorAt + setActorTalkColor before each line, the
openquest prop-actor pattern, examples/openquest/actors.scc:203-223) works
but makes the speaker a runtime property instead of a source-level one: the
transcript's speaker tag would have to be inferred from preceding
setActorTalkColor calls rather than read off the `actorSay(gusket_a, …)`
argument. Per-NPC actors cost nothing extra and keep speaker attribution
static and greppable.

**Rejected for now — full costumed actors everywhere (Option C / Route A).**
Mostly an art + background-repaint + occlusion project (Gusket is occluded
by the bar, T_GUSKET y48+40 vs T_BAR y80, tools/genassets.py:336-343; the
clerk lives inside the booth), plus a Makefile generalization
(COSTUME_FRAMES is sprocket-only, game/Makefile:55, :88). The engine part is
proven (multi-costume palettes are per-costume remap tables, not a shared
window — cost_parse.y:667-674, costume.cpp:817-826; openquest ships six) so
this stays available per-NPC later. Voltina gets it first: Scene 06 is
unbuilt, so her actor costs no rework.

**Landmine (all options): actorTalk silently drops or mis-renders lines for
actors not in the current room** (actor.cpp:3489-3511 — the investigations
disagree on drop-vs-uncolored-fallback; see open questions). Rule: every
speaking actor is `putActorAt` into the room before its first line, even
off-screen voices (heckler) — park them at the text position you want.

## 3. Animation plan per NPC

| NPC | Launch | Later option | Verdict from art investigation |
|---|---|---|---|
| Gusket (tavern) | Tier-A text only | 2-state mouth-crop flap (Route B) | 10px head, flap reads — YES |
| Flange (docks) | Tier-A text only | 2-state flap | 10px head — YES |
| Rivet (alley) | Tier-A text only | 2-state **lens pulse** (no mouth, genassets.py:633-635) | stylized — YES |
| Emcee (theater) | Tier-A text only | 2-state flap | 8x10 head — marginal, workable |
| Box-office clerk | Tier-A text only | none (2px eye-blink at most) | 6px sprite in booth — flap impossible; that's the gag |
| Slot-eye | Tier-A text only | none — the slot-open state IS the animation | already a 2-state object |
| Heckler | Tier-A, off-screen actor | none | a voice from the dark animates nothing |
| Voltina (Scene 06) | **Full costumed actor** | talk frames = tesla-coil arcing (free sight gag) | stand + 2 talk frames; new scene, zero rework |

The flap mechanism, when wanted, is already proven in-repo: 2-state image
swaps (marquee genassets.py:1408-1410, curtain :1422-1424) driven by a
`setObjectState` loop like signFlicker (game/docks.scc:41-54), gated on
`VAR_HAVE_MSG`. Cost ~15 LOC of genassets + ~10 LOC of room script per NPC;
the known risk is the signFlicker bug class (a missed stopScript leaves a
mouth flapping forever) and the story-flags-before-speech concurrency rule
(NOTES.md). NPCs currently have no painted mouths (eyes only), so flap
frames require drawing one — another reason to defer.

## 4. Dub pipeline changes (numbered diff list)

1. **tools/genassets.py** — add PAL[108..112] per-NPC talk colors (107 is
   warning red; 108-223 free), named probes `"talk-gusket": [108]` etc.
   alongside the existing `"talk":[105], "talk-2":[106]` (genassets.py:1313-1314),
   plus a build-time assert that no room image rows 0-104 contain
   near-collisions with any talk color (the piano-keys bug class,
   walkthrough.py:218-221). Pick colors maximally spread in hue/luma —
   dub.py reads VP8 4:2:0 footage, not lossless screenshots. (~25 lines)
2. **tools/transcript.py** — replace the egoSay-only regex (transcript.py:27)
   with one ordered alternation
   `r'(ego|actor)Say\(\s*(?:(\w+)\s*,\s*)?"((?:[^"\\]|\\.)*)"'` via
   `finditer`; emit `{"text": …, "speaker": …}` dicts instead of bare
   strings; map actor variable names → canonical speaker names via a table
   shared with the stage probes. A single ordered scan preserves the
   source-order pairing contract. (~20 lines)
3. **walkthrough/driver/walkthrough.py** — `talk_mask` (walkthrough.py:216-229)
   classifies each matched pixel by nearest talk color over the full set
   (not independent per-color TOL tests); `watch()` adds
   `speaker=<argmax count>` to `line_start` events (:321); dub sheet gains a
   speaker column (:457-479); validate mode asserts observed segment speaker
   == scripted line speaker — a mispair detector the order-only pairing
   never had. Segment splitting is untouched: a speaker change changes the
   mask signature, which already splits segments. (~40 lines)
4. **walkthrough/post/dub.py** — same nearest-color classification in
   `detect_line_times` (dub.py:75-122), returning `(t0, t1, speaker)`;
   `speak(text)` → `speak(text, speaker)` driven by a
   `CAST = {speaker: (voice, synth_args, fx)}` table; snapper
   (dub.py:148-163) gains the constraint `segment.speaker == line.speaker`
   (a misclassified segment degrades that line to its laggy live timestamp —
   degraded, not broken). (~50 lines)
5. **Cache key discipline** — keep the exact `f"{VOICE}|{FX}|{text}"` format
   (dub.py:64) with per-speaker values substituted so every existing Sprocket
   clip in `~/.cache/clankey-voices` stays hot; any new synth args
   (`--length-scale`, `-s`) MUST join the key or stale audio is served
   silently.
6. **Voice downloads** — only `en_US-lessac-medium` is installed and piper
   1.4.2 does not auto-download; one-time
   `python3 -m piper.download_voices <voice> --data-dir ~/.local/share/piper-voices`
   per cast member. Casting: Gusket `en_US-ryan-high` pitched down
   (`asetrate=48000*0.82,aresample=48000,atempo=1.22` + heavier acrusher);
   Flange `en_US-joe-medium` `--length-scale 1.05`; Rivet `en_US-bryce-medium`
   `--length-scale 0.78`; emcee `en_GB-cori-high` + PA echo
   (`aecho=0.7:0.6:60:0.25`); Voltina `en_US-kristin-medium` + chorus/long
   echo, lowpass 5000. Budget fallback: one `en_US-libritts_r-medium`
   (904 speakers via `-s`) covers everyone, worse separation. Cheap, tinny
   NPC voices are sanctioned as characterization (NARRATION.md:77 —
   Piper-as-a-gag); Sprocket keeps lessac + ROBOT_FX unchanged.
7. **In-game voice (monster.sou)** remains parked and orthogonal
   (NOTES.md:131) — the dub stays a post-production overlay.

## 5. Writing doctrine

The reference sound is split-cast: KQ6's even narrator plus performed
character voices (NARRATION.md:11-15). The deadpan rules are *narrator*
doctrine; moving short performed lines into NPC mouths moves the game toward
its stated reference and protects Sprocket's register — the straight man
stops being asked to do voices. The desk has ruled this direction three
times (B7, N-A6, the quoted-speech overload).

Rules (to enter docs/editorial/CHARTER.md the same day the first actorSay
lands — the comedy critic currently "Reads: every egoSay" and is blind to
the new form):

1. **Sprocket keeps all narration**, all description, and any speech whose
   joke is the paraphrase (leaks, compressions, corrections, sportscasts).
   Reported is the default.
2. **NPCs get short direct lines only** (≈12 words): punchlines, refusals,
   prices, prophecies, heckles. No NPC exposition paragraphs — multi-sentence
   content stays reported.
3. **No double-telling**: Sprocket never restates what an NPC just said; he
   may tag the delivery or report consequences.
4. **The signature shape is NPC punchline, Sprocket button** — the flat
   follow-up is the post-punchline dead air NARRATION rule 5 demands,
   currently impossible when setup/punch/button share one card.
5. **NPCs may perform; the narrator never does** (exclamation is legal in
   the emcee's mouth; N-M2 bound the narrator, not the cast).
6. **Meta stays NPC-only** (B7); the slot-eye keeps the monopoly.
7. **Mechanical**: per-(object,verb) source order remains
   walkthrough-path-first; speaker is a per-line tag, not a stream reset.

**Protected class — never convert** (the joke lives in the paraphrase):
the "hard drive, pal" leak (tavern.scc:176), "mind the everything"
(tavern.scc:61), the one-drink-per-life correction (tavern.scc:190), the
entire dart-hustle sportscast (tavern.scc:349-383). Keep
`actorSay(gusket, "You look like you've had a hard drive, pal.")` in the
style doc as the canonical regression example — worse in every way.

**Ranked conversion list:**

1. **Madame Voltina** (theater.scc:361-367 + all of Scene 06) — MUST.
   Prophecy paraphrased by the protagonist has no authority; her scheduled
   plants need verbatim delivery. Scene 06 unwritten = zero rework.
2. **Slot-eye** (tavern.scc:413, alley.scc:116,128) — near-free, already
   direct text; the game's best line gets its own card and voice.
3. **Audience heckler** (theater.scc:180 "WORSE NOW.", :186 "ENCORE") —
   free; a voice from the dark wants a different voice.
4. **Rivet's priced facts** (alley.scc:321-336, 341-352) — the hint economy
   becomes audible characterization; appraisal narration stays Sprocket's.
5. **Emcee's patter** (theater.scc:208-214, 224, 227) — pairs with the B8
   wind-count rework, which touches this scene anyway.
6. **Box-office clerk, two lines** (midtown.scc:234, :236).
7. **Rustlers' knock-code line only** (tavern.scc:288) — optional, flagged
   risky; the leaning-casually frame stays Sprocket's.
8. **Gusket: at most the shim hint** (tavern.scc:181).
9. **NEVER**: Flange/dart hustle; the riddle-duel narration shell (the B2
   dialog tree makes the picked riddles direct by necessity; outcome beats
   stay reported — "He pays the bolt without a word." is untouchable).

**Example rewrites:**

A. Voltina's door (theater.scc:361-367) — quoted speech doing three jobs:

```
BEFORE
  egoSay("The dark behind him smells like ozone and incense. A voice from it says: 'I have been expecting you, key-bearer.'");
  egoSay("I start to explain about the key. 'I know,' says the voice. 'Ask me sometime about the key that winds itself. Mind the cables.'");
  egoSay("Madame Voltina. I'm going to need a minute, and possibly a will.");

AFTER
  egoSay("The dark behind him smells like ozone and incense.");
  actorSay(voltina, "I have been expecting you, key-bearer.");
  egoSay("I start to explain about the key.");
  actorSay(voltina, "I know.");
  actorSay(voltina, "Ask me sometime about the key that winds itself. Mind the cables.");
  egoSay("Madame Voltina. I'm going to need a minute, and possibly a will.");
```

"I know." gets its own card, color, and beat — the two-word omniscience
joke buried mid-sentence becomes the scene's timing spine.

B. Slot-eye (tavern.scc:409-414) — the punchline/button split:

```
BEFORE
  egoSay("CLANG-CLANG. CLANG. CLANG-CLANG.");
  egoSay("A slot opens. An eye looks at me. A voice says: 'Act Three, buddy.' The slot closes.");

AFTER
  egoSay("CLANG-CLANG. CLANG. CLANG-CLANG.");
  egoSay("A slot opens. An eye looks at me.");
  actorSay(slotEye, "Act Three, buddy.");
  egoSay("The slot closes.");
```

C. Emcee's intro (theater.scc:208-214) — tag-the-delivery:

```
BEFORE
  egoSay("Sprocket, he says, reading the marquee off my face. The wind-up act. You're on next.");
  egoSay("One problem: the spotlight operator went into low-power mode during the juggler. The juggler had that effect.");
  egoSay("House rule: no spot, no act. He says it like the rule has a plaque somewhere.");
  egoSay("He looks from my key to the dark booth and back. He likes my chances, he says. Conditionally.");

AFTER
  actorSay(emcee, "Sprocket! The wind-up act. You're on next.");
  egoSay("He read the marquee off my face.");
  actorSay(emcee, "Small wrinkle. The spotlight operator went low-power during the juggler. The juggler has that effect.");
  actorSay(emcee, "No spot, no act.");
  egoSay("He says it like the rule has a plaque somewhere.");
  egoSay("He looks from my key to the dark booth and back. He likes my chances. Conditionally.");
```

The register gap between the emcee's showbiz and Sprocket's dry tags is a
new joke the one-voice version structurally cannot make.

## 6. Implementation checklist

Ordered so the Act One validate gate stays green after every step. Steps
marked **[DUB PAIRING]** touch the source-order pairing contract
(NOTES.md "Walkthrough-path lines go FIRST" — pairing hands out lines in
source order per handler; the rule now binds actorSay lines too).

1. genassets.py: 5 talk-color palette slots + named probes + the
   scenery-collision build assert. Rebuild rooms, run validate. (New probes
   match nothing yet — green.)
2. **[DUB PAIRING]** transcript.py ordered alternation regex + `{text,
   speaker}` dict schema, landed atomically with the walkthrough.py consumers
   of the schema (shot_lines/lines at walkthrough.py:319-321, :437-449).
   All lines are still egoSay so pairing output is identical; validate.
   The single ordered `finditer` is what preserves the pairing contract —
   two separate scans would not.
3. walkthrough.py: nearest-color talk_mask classification, `speaker=` on
   line_start, dub-sheet speaker column, validate-mode speaker assert.
   Validate (every segment classifies as sprocket/105 — green).
4. **[DUB PAIRING]** dub.py: speaker in detect_line_times, CAST table,
   `speak(text, speaker)`, speaker-keyed cache, speaker-constrained snapper.
   The snapper change alters which segment a line may claim; re-dub one
   existing take and diff against the previous production.mp4 before
   trusting it. Cache key format preserved → Sprocket clips stay hot.
5. Tier-A actors: actor decls + colors in common.sch, setupActors blocks in
   actors.scc (setActorTalkColor; setActorIgnoreBoxes or box-snapping drags
   Gusket out from behind the bar), putActorAt in room entry scripts. No
   actorSay lines yet → transcript unchanged → validate green.
6. Download cast voices; wire CAST entries.
7. **[DUB PAIRING]** Probe conversion: the slot-eye (rank 2, cheapest).
   First handler whose line count/order changes — re-check the
   walkthrough-path-first ordering inside that handler and the screenplay's
   talk-segment expectations. Record a take; verify VP8 speaker
   classification against the new colors before converting anything else.
8. Same day as step 7: the writing rules (section 5) enter
   docs/editorial/CHARTER.md and the comedy critic's read set extends to
   actorSay, or the desk cannot enforce the ≤12-word and no-double-telling
   rules.
9. **[DUB PAIRING]** Heckler, then Rivet, then emcee/clerk — one scene per
   pass, each behind validate, each re-checking handler line order and
   screenplay segment counts. Mixed ego/actor lines in one handler extract
   as ONE interleaved ordered list. Room-transition verbs still say nothing
   (NOTES.md:135-139) — the rule applies to NPCs too.
10. Voltina: gated behind B2+B8 per the desk's standing ruling — but the
    machinery is proven by then, so Scene 06 is written direct-speech-native
    from day one, with her costumed actor (stand + 2 arcing talk frames,
    sprocket.scost talk-limb pattern, Makefile %.scost rule already generic).
11. Optional, unscheduled: Route-B mouth flaps for Gusket/Flange/Rivet
    (mind the stopScript/signFlicker bug class); Tier-B mouth-overlay
    costumes if flaps disappoint.

## 7. Open questions for the author

1. **The not-in-room behavior is disputed**: the engine investigation reads
   actorTalk as silently *dropping* the line (actor.cpp:3491-3493 →
   return at :3510-3511); the voices investigation reads it as falling back
   to the default string color with no anim (:3514-3517). The mitigation
   (always putActorAt, even for off-screen voices) is the same either way,
   but settle it with a 2-minute test before writing the heckler.
2. **Talk color picks**: which 5 of slots 108-223? Needs the hue/luma-spread
   choice plus one probe take through VP8 before the colors are trusted —
   who signs off the palette?
3. **Cast vs budget**: five per-NPC voice downloads (~60-110MB each) or the
   single libritts_r multi-speaker model? The doc recommends the former;
   the latter is one download and one audition session.
4. **Charter wording**: does the desk accept the ≤12-word rule and
   no-double-telling as written, or does it want its own formulation? It
   must land with step 8, not after.
5. **Flaps at all?** Tier-A text may be enough; the flap work is pure polish
   with a known footgun. Decide after seeing the slot-eye and heckler dubbed.
6. **The clerk**: the booth makes animation impossible and that's currently
   read as the gag. Confirm the gag is intentional before anyone "fixes" it.
7. **Does the unused `BETTY_COLOR 106` get retired or assigned?** It's
   plumbed through the whole observation stack as "talk-2" — cheapest
   possible first NPC color if a character claims it.