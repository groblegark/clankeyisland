# SCENE 09 — THE RUSTLERS' HIDEOUT (Act 3 opens)

Design doc, Wave 1. Lands as `docs/scenes/SCENE-09.md`. Implementer builds `game/hideout.scc` + `hideout.sch`, addenda to `tavern.scc` / `alley.scc`, `draw_hideout` in `tools/genassets.py`, "The Rustlers' Den" in `tools/genmusic.py`, five new effects in `tools/genaudio.py`, and the scene's shots in `walkthrough/screenplay/`.

---

## 1. Scene goal & the three-keys spine

**Goal:** Open Act 3 by cashing every check Act 1–2 wrote at this door. The knock-code (planted S02, echoed by the heist hatch in S05 and by Voltina in S06) finally opens the tavern's back door. Inside: the Rustlers' leader gets a face (**Captain Capstan**, decommissioned harbor winch-bot) and a want (the ransom — make winding a paid trade again), the slot-eye's "Act Three, buddy" converts from refusal to admission ticket, and the player recovers **Key #1** by one of two real paths: **parley** (dialog-tree negotiation, the contest) or **stealth** (the theater heist inverted — the player fishes the key back on the Rustlers' own hook-on-a-line).

**Spine:** Player enters holding Key #2 (Voltina, S06) and zero leads on #3. Player exits holding Keys #1 and #2, plus the game's first on-screen pointer at Old Crank ("the old crank up the hill"), feeding Scene 10. If the parley path was taken, the Rustlers become the contracted **rewind crew** — hands the finale (S11) needs at the Dynamo.

**Why this scene isn't a fetch:** there is no item to find and carry back. The key is visible from the first minute, hanging over the card table. The whole scene is *how do you take it* — argue it down or reel it up.

**Geometry:** The hideout is the space between the tavern's east wall and the alley — the tavern's `doorBack` (x=288) opens into its west wall; its east steel door is the alley's `hideoutDoor` seen from inside; a loft over the den is reached from the alley fire escape (x=144), which is how the heist crew came home from the theater with their tackle. One room, two levels.

---

## 2. The puzzle chain

### Numbered graph

```
            [act3Started]  (set by Scene 08's close — contract, §10)
                  |
   ┌──────────────┴───────────────────────────────┐
   |                                              |
 (1) FRONT: knock code on tavern doorBack     (2) TOP: alley fire escape
   |  2-1-2 → slot-eye → "Act Three, buddy."     |  lookout gone, rungs
   |  → bar lifts, door opens                    |  freshly oiled → climb
   |                                              |  to loft shutter
 (3) den entry cutscene                       (4) open loft hatch
   |  Capstan dictating the ransom note          |  forced eavesdrop:
   |  → leader's face, want, guest rule          |  the ransom, overheard
   |  → ransomKnown                              |  → ransomKnown
   |                                              |  + sees cleat/line/key rig
 (5) PARLEY (dialog tree, Capstan)            (6) STEALTH (the loft)
   |  stage 1: pick the argument                 |  mistake: magnet through
   |   a) civic appeal      — flop               |   hatch → grabs the steel
   |   b) invoke City Hall  — flop               |   washers pot → caught →
   |   c) "who winds the    — WINS               |   ejected to alley (retry)
   |       winders?"                             |  solve: Use the brass cleat
   |  stage 2: pick the offer                    |   → reel the key up on the
   |   a) bolts (he has 0)  — flop               |   Rustlers' own tackle
   |   b) backstage pass    — flop               |
   |   c) rewind contract   — WINS               |
   |        |                                     |
 (7) Capstan reels the key down on her        (8) key in hand, exit by the
     own crank → KEY #1 (keyByParley)             shutter → KEY #1 (keyByTheft)
                  |                               |
                  └───────────┬───────────────────┘
                       [keyRecovered]
              + plant: "the old crank up the hill" (parley path,
                or trophy-wall LookAt on the theft path — see §4)
```

Nodes (1)/(2) and (5)/(6) are **parallel, both live, mutually visible** — a player may knock first, hear the demand, walk out, and go steal it; or get ejected from the loft and walk in the front like an adult. Both branches surface the ransom plot (3 and 4 both set `ransomKnown`); the leader's want is never skippable.

### Fair-play audit — every hint, with its source named

| Needed knowledge | Source(s), in order of planting | Forced? |
|---|---|---|
| The knock-code 2-1-2 | S02 `rustlersTable:TalkTo` (on the canonical validate path since B9); S05 heist hatch echo ("Two clangs. One. Two."); S06 Voltina's forced echo (desk assignment, pass-2 dispositions — **contract: S06's echo sets `heardKnockCode`**) | Yes, by S06 |
| Where the door is | The slot-eye refused the player here twice ("Act Three, buddy", S02+S03); S09's tavern addendum: the rustlers' table is empty, "the game moved somewhere with a door policy"; S03 `hideoutDoor` post-heist branch "it knows what I'm here about now" | Yes (twice refused = remembered) |
| Act 3 has started | Scene 08's closing beat points back downhill (contract, §10); the hum is audibly flatter (den song ships detuned, §5) | Yes |
| The Rustlers' motive | GDD; S06 Voltina says it out loud (canon); restated by Capstan's own dictation in BOTH entry beats (3) and (4) | Yes |
| Stealth entry exists | S03 `fireEscape:UsedWith oilcan`: "rusted shut **on purpose**. It's a security feature" — the lock named its own key condition; Act 3 LookAt shows the change: lookout's post empty, rungs freshly oiled (they hauled the heist tackle up at night) | No (it's the optional path) |
| Hook beats magnet on brass | S05 heist: "A hook on a line... somebody else's magnet-on-a-string" (they brought a hook for a reason); S09 custom refusal: "The magnet holds no opinion about brass" | Taught on first wrong try |
| The cleat is the steal | Hatch eavesdrop closes on it: "The line runs up to a cleat by my foot"; cleat LookAt traces the rig | Yes, within the path |
| The winning argument (who winds the winders?) | Power model on the S01 notice board (the hum winds every mainspring remotely; hand-winding is crude backup — forced read since B4); POP. 8,011 (S01 sign); Rivet's free fact ("wind the city back up. **Or down**", S03); the flat hum in the player's ears | Yes |
| The winning offer (the contract) | Capstan's own want, stated in her intro ("retired. By the city, not by choice"), the RECEIPTS drawer, the trophy wall (a working life, ended); she asks the question directly: "make me a better offer" | Yes |

No lock names its key verbatim (N-A2 discipline): the door hints are dents and chalk, the stealth hint is fresh oil where rust was policy, the dialog winners are inferences from forced facts, and every flop teaches by refusal, not by pointing.

### The playable-agency beats (editorial B2/B8 compliance)

1. **The parley is a two-stage dialog tree** (uses the B2-era `dialog.scc` UI): six pickable options across two stages, four of which flop *funny and recoverable*. The player can lose the argument repeatedly at no cost but pride.
2. **The route itself is a choice** — front door vs. fire escape, talk vs. theft, with different fiction downstream (`keyByParley` / `keyByTheft`).
3. **Stealth is failable**: the reasonable-wrong tool (the player's own beloved magnet) gets you *caught and comically ejected* — a real consequence, fully retryable, per "nothing can kill you; every failure is a joke."

---

## 3. Object table

Stage is 320×144 (verb panel below y≥144). **Loft strip: y 0–48** (walk line ≈ y 44, disconnected from the den's walkboxes — no ladder; the hatch is freight-only, the crew commutes by fire escape). **Den: y 48–144** (walk line ≈ y 118–126, like every other room). Rects are sketches for `draw_hideout` / GEOM; hotspots default to rect centers.

| # | Object | Rect (x,y,w,h) | Verbs handled | States / flags |
|---|---|---|---|---|
| 1 | `doorTavern` — back of the back door | 8,64,24,48 | LookAt, Open/Use (silent exit → TavernRoom) | — |
| 2 | `doorStation` — slot, chalk tally, crate stack | 34,64,22,40 | LookAt, Use | — |
| 3 | `slotEye` — the doorbot (Person; Tier-A actor, has the slot-eye talk color from NPC-DIALOG rank 2) | 38,84,14,28 | LookAt, TalkTo | — |
| 4 | `stove` — pot-belly stove | 62,72,24,40 | LookAt, Use, Smell | flue exits through the tavern chimney (painted) |
| 5 | `framedNotice` — framed cease-and-desist | 60,46,28,20 | LookAt, Use, PickUp | the only dusted thing in the room |
| 6 | `cardTable` — four Rustlers, pot of washers (Person) | 100,88,56,34 | LookAt, TalkTo, UsedWith(magnet), Smell | the tavern trio + the ex-lookout (his spyglass on the table) |
| 7 | `keyOnLine` — Key #1 on the heist hook | 122,52,14,30 | LookAt, PickUp/Use, UsedWith(magnet), Smell | states: hanging / gone (post-recovery, line drawn slack) |
| 8 | `ransomDesk` — drafts in seniority order | 180,88,44,34 | LookAt, Use/PickUp, Smell | states: ransom drafts / work order (post-parley) |
| 9 | `capstan` — Captain Capstan (Person; Tier-A actor, **new talk color** per NPC-DIALOG step 1) | 192,52,36,60 | LookAt, TalkTo (dialog tree), Give/UsedWith, Smell | parley state machine (§4) |
| 10 | `trophyWall` — plaques and one reserved nail | 240,36,48,28 | LookAt | states: nail bare / work order hung (post-parley); carries the theft-path Old Crank plant |
| 11 | `doorAlley` — the BACK back door, from inside | 288,64,24,48 | LookAt, Open/Use, Smell | states: barred / unbarred (post-`keyRecovered`); silent exit → AlleyRoom |
| 12 | `hatch` — loft hatch over the card table | 118,32,22,14 | LookAt, Open (forced eavesdrop), UsedWith(magnet — the flop) | states: closed / open |
| 13 | `loftCleat` — brass cleat, tackle tied off | 98,34,12,12 | LookAt, Use (the steal) | states: loaded / slack |
| 14 | `loftShutter` — how the heist came home | 284,24,24,22 | LookAt, Open/Use (silent exit → AlleyRoom, at the fire-escape top) | latches from habit, not commitment |

**Art notes (genassets contract):** rafter pulley painted between hatch and keyOnLine (the line is the heist tackle, drawn taut hanging / slack gone — 2 states like the dumpster); the four card players reuse the tavern-trio silhouette recipe plus the spyglass on the table; Capstan reads as a winch — cable shoulders, crank hands, drum chest stenciled `4,000 LBS W.L.`; the den's animating element is the stove's flicker (signFlicker recipe). **Alley art**: `fireEscape` gains a lookout-less state (keyed `act3Started`) and a shutter detail at the ladder top. Talk-color palette: one new slot for Capstan, build-assert per NPC-DIALOG step 1.

**Engine notes (NOTES.md compliance, for the implementer):** all shared verbs from `common.sch` (ids pinned); ownership tests are `== VAR_EGO`, recovery is `pickupObject(InventoryItems::windupKey, InventoryItems)` (its owner is 0 since the heist); story flags set at the **top** of branches, before speech; walkthrough-path branches **first in source** inside every handler; both exits and the shutter/fire-escape transitions **say nothing**; `putActorAt` Capstan and the slot-eye in `entry()` before any `actorSay`.

---

## 4. Dialog draft — the full text

Register: Sprocket narrates, reported speech default; NPCs get direct punchlines ≤12 words; meta stays in the slot-eye's mouth only; no smell-zeugma template; no self-grading. Written as build-ready structure; `walkthrough-path lines first` ordering is already baked in.

### 4a. Tavern addenda (`tavern.scc`)

```
object rustlersTable — verb TalkTo / LookAt: NEW act3 branch, FIRST in source
    if (act3Started) {
        // LookAt and TalkTo share this state; give LookAt:
        egoSay("The table's empty. Cards racked, washers gone, chairs squared away.");
        egoSay("Wherever the game moved, it moved somewhere with a door policy.");
        return;
    }
    ... existing branches unchanged ...

object doorBack — verb Open/Use: NEW branch, FIRST in source
    if (heardKnockCode && act3Started) {
        if (doorBackOpen) {
            // silent transition (room-transition rule):
            putActorAt(VAR_EGO, 28, 118, HideoutRoom);
            startRoom(HideoutRoom);
            return;
        }
        doorBackOpen = 1;                         // flag before speech
        cutscene(0) {
            startSound(knockSnd);
            egoSay("CLANG-CLANG. CLANG. CLANG-CLANG.");
            egoSay("The slot opens. The eye looks at me. For a long time.");
            actorSay(slotEye, "Act Three, buddy.");
            startSound(barliftSnd);
            egoSay("The bar lifts. The same three words, and this time they're a ticket.");
        }
        return;
    }
    ... existing heardKnockCode refusal and dented-plate branches unchanged
        (they now only fire pre-act3) ...
```

*(The slot-eye gag pays off at the threshold: the refusal line, verbatim, becomes the admission. He was never stonewalling — he was quoting the schedule.)*

### 4b. Alley addenda (`alley.scc`)

```
object hideoutDoor — Open/Use: NEW act3 branch, FIRST in source
    if (act3Started) {
        cutscene(0) {
            startSound(knockSnd);
            egoSay("CLANG-CLANG. CLANG. CLANG-CLANG.");
            egoSay("The slot opens. The eye looks pained.");
            actorSay(slotEye, "Front door's the front, buddy.");
            egoSay("Message discipline survives even success.");
        }
        return;
    }
    ... existing branches unchanged ...

object fireEscape — LookAt: NEW act3 branch, FIRST in source
    if (act3Started) {
        egoSay("The lookout's post is empty. And the rungs are freshly oiled, top to bottom.");
        egoSay("Somebody's been hauling midnight cargo up to that shutter. The security feature died of convenience.");
        return;
    }
    ... existing lines unchanged ...

object fireEscape — Use/PickUp: NEW act3 branch, FIRST in source
    if (act3Started) {
        if (ejectedOnce && !keyRecovered) {
            egoSay("The shutter's still unlatched. Their security model never planned for stubborn.");
        }
        // silent transition to the loft:
        enteredViaLoft = 1;
        putActorAt(VAR_EGO, 296, 44, HideoutRoom);
        startRoom(HideoutRoom);
        return;
    }
    ... existing rusted-shut lines unchanged ...
```

*(One spoken line then a transition on the same verb is the gate's proven pattern only when split across clicks; here the `ejectedOnce` line plays before the silent climb on the same click — implementer: if dub pairing complains, move that line to the loft-shutter LookAt instead. Flagged for the desk.)*

### 4c. The hideout room (`hideout.scc`)

**Entry script:**

```
local script entry() {
    startScript(1, musicLoop, []);                 // The Rustlers' Den, §5
    putActorAt(capstan_a, 208, 110, HideoutRoom);  // speakers in-room before lines
    putActorAt(slotEye_a,  44, 110, HideoutRoom);

    if (enteredViaLoft) { enteredViaLoft = 0; return; }   // loft arrivals get silence;
                                                          // the hatch owns the reveal
    unless (denEntered) {
        denEntered = 1;
        ransomKnown = 1;                            // flags before speech
        cutscene(2) {
            walkActorTo(VAR_EGO, 64, 124); waitForActor(VAR_EGO);
            egoSay("The Rustlers' hideout. The room between the tavern's back wall and the alley. The city forgot to put it on either side.");
            egoSay("Smaller than the legend. Tidier, too. Somebody in here squares chairs.");
            egoSay("At the desk: a winch-bot the size of a cargo door, dictating to a quill lashed to her own left crank.");
            actorSay(capstan, "...item four. The rewind: three keys, one city, our rates.");
            egoSay("She sees me. Everyone sees me. Four hands of cards go face down in unison.");
            actorSay(capstan, "The wind-up act. You knocked the code, so you're a guest.");
            if (getObjectOwner(InventoryItems::keyTwo) == VAR_EGO) {
                actorSay(capstan, "Guests leave with what they carried in. House rule. Relax.");
                egoSay("My chest compartment relaxes by one percent.");
            }
            actorSay(capstan, "Captain Capstan. Wind-up crew, retired. By the city, not by choice.");
            egoSay("And over the card table, on the hook that took it: my key.");
        }
    }
}
```

**doorTavern** —
- LookAt: `"The back of the back door: a bar, a slot, and the doorbot's entire career."`
- Open/Use: silent → `putActorAt(VAR_EGO, 282, 120, TavernRoom); startRoom(TavernRoom);`

**doorStation** —
- LookAt: `"A bolted stack of crates, exactly slot-high. Beside the slot, a chalk tally: WRONG and RIGHT."` / `"WRONG is winning by a margin you could retire on."`
- Use: `"The slot is licensed equipment. The license is glaring at me."`

**slotEye** —
- LookAt: `"The eye, the whole bot at last. Knee-high, mostly eyelid, all protocol."`
- TalkTo (first): `actorSay(slotEye, "Never doubted you, buddy.")` / ego: `"He doubted me twice. Both times are in chalk."`
- TalkTo (repeat): `"He's drilling slot timing against a sand timer. There are standards."`

**stove** —
- LookAt: `"A pot-belly stove. The flue exits through the tavern's chimney next door. The landlord doesn't know."`
- Use: `"It's at a rolling boil of something I'm not asking about."`
- Smell: `"Driftwood. Kelp. A stew with a past."`

**framedNotice** —
- LookAt: `"A framed cease-and-desist from City Hall, stamped by the Mayor's own office."` / `"They dusted the frame. Nothing else in here is dusted."`
- Use/PickUp: `"It's exhibit A of the grievance collection. Touching exhibits voids my guest status."`

**cardTable** —
- LookAt (pre-recovery): `"The tavern trio, plus the spyglass. Four hands of cards, one pot of washers, zero trust."` / `"The lookout finally got a seat at the game. He keeps glancing at where his window isn't."`
- LookAt (post-recovery): `"The game resumes. The pot is washers again, now that the big score is paperwork."`
- TalkTo (first): `"The one in the hat squints at me, sure he knows me from somewhere acoustic."` / `"I have never leaned near anyone in my life, I tell him. Casually. He lets it go."`
- TalkTo (repeat): `"They're arguing over whether the spyglass counts as a tell."`
- UsedWith magnet: `"Fishing steel washers off a manned table. Even the duck wouldn't back this plan."`
- Smell: `"Salt. They track the harbor in on their feet."`

**keyOnLine** —
- LookAt (hanging): `"My key, over the table, still rigged to the very hook that took it."` / `"They never re-rigged. Why retire a working crime."`
- LookAt (gone): `"The hook hangs empty. Pensioned off."`
- PickUp/Use (hanging): `"It hangs at exactly cutlass height. The geometry is a contract clause."` / `"I reach. Four chairs scrape. I un-reach. The chairs scrape back."`
- UsedWith magnet: `"Brass. The magnet holds no opinion about brass. That's why they brought a hook in the first place."` / `"Also: four witnesses."`
- Smell: `"From down here, just rope tar. They keep my property out of nose range. Deliberately, I assume."`

**ransomDesk** —
- LookAt (pre-parley): `"Drafts of a ransom note, filed in seniority order. The number grows a digit per draft."` / `"The latest is denominated in washers. Post-bolt currency found its true believers."`
- LookAt (post-parley): `"The ransom note, flipped over and reborn as a work order. Same numbers. Fewer threats."`
- Use/PickUp: `"Her quill, her desk, her margins. I've seen what she benches."`
- Smell: `"Ink and lamp smoke. The grievance keeps office hours."`

**capstan** —
- LookAt (pre-recovery): `"A harbor winch-bot, decommissioned. Cable for shoulders, a crank where each hand should be, a drum chest wound tight."` / `"The drum is stenciled 4,000 POUNDS WORKING LOAD. Nothing about her reads decorative."`
- LookAt (post-recovery): `"Same rig, new posture. Employed suits her."`
- Smell: `"Tarred rope. The real thing. Nobody's made it in an epoch — she has a supplier or a hoard."`
- Give/UsedWith keyTwo: `actorSay(capstan, "Guest rule, wind-up act. Don't tempt the help.")`
- Give/UsedWith backstagePass (outside the tree): `"She'll hear offers at the desk, in order, like a business."`
- Give/UsedWith anything else: `"She appraises it against the ransom and files it under petty."`
- **TalkTo — the parley** (requires `!keyRecovered`; post-recovery states below):

```
opening (every time the tree opens):
    egoSay("I ask after my key. She asks after my city's credit rating.");
    actorSay(capstan, "Ransom isn't theft. It's maintenance, invoiced in advance.");
    egoSay("She slides me the current draft. The number has six digits and a footnote.");

STAGE 1 — pick the argument:
  [1] "The city needs that key back."        — FLOP, repickable
        egoSay("I explain that the city needs the key. Sincerely. With gestures.");
        actorSay(capstan, "The city needed winders once. We kept the receipts.");
        egoSay("She points at a drawer. The drawer is labeled RECEIPTS, GRIEVANCE, MIXED.");
  [2] "City Hall will hear about this."      — FLOP, repickable
        egoSay("I invoke City Hall. The room enjoys that.");
        actorSay(capstan, "His last cease-and-desist is over the stove. Framed.");
        egoSay("It is. They dusted it.");
  [3] "Who pays a ransom after the city stops?"   — WINNER
        egoSay("I ask who signs the cheque. Ransom needs a payer. Payers need wound springs.");
        egoSay("The hum is flat and dropping. Past a point, this city can't surrender. It can only stop.");
        actorSay(capstan, "We can wind them awake to pay. Hand-winding is what we do.");
        egoSay("Six of you. Eight thousand of them, give or take this room.");
        egoSay("And when the hum quits — who winds the winders?");
        egoSay("Her crank stops mid-polish. The card game stops pretending to be a card game.");
        actorSay(capstan, "...The plan assumed somebody stays wound.");
        egoSay("Plans usually do.");
        actorSay(capstan, "Then make me a better offer than a dead invoice.");
        → set arithmeticLanded; open STAGE 2
  [4] "I'll think about it."                 — exit tree

STAGE 2 — pick the offer (gated on arithmeticLanded):
  [1] "I can get you bolts. Eventually."     — FLOP, repickable
        egoSay("I offer bolts. I have zero bolts. I offer the concept of bolts.");
        actorSay(capstan, "We invented owing. Try again.");
  [2] "One backstage pass, barely used."     — FLOP, repickable
        egoSay("I offer the backstage pass. She reads the lanyard. Bicycle chain. Good chain.");
        actorSay(capstan, "Tempting. The act, not the access.");
        egoSay("She's heard about the act. Everyone has heard about the act.");
  [3] "Wind the Dynamo with me. On the books."    — WINNER
        // flags before speech:
        keyRecovered = 1;  keyByParley = 1;
        cutscene(0) {
            egoSay("The rewind is a job, I tell her. Three keys, one machine the size of a district, and my arms are stock parts.");
            egoSay("First call goes to a certified wind-up crew. Paid. In writing. Starting with the bots who kept the skill alive.");
            actorSay(capstan, "In writing means in writing, wind-up act.");
            startSound(scribbleSnd);
            egoSay("She flips the ransom note over. I write the work order on the back. Same numbers, fewer threats.");
            actorSay(capstan, "Crew! Pay the gentleman his key.");
            startSound(winchSnd);
            setObjectState(keyOnLine, 2);
            egoSay("She hooks the line to her wrist drum and pays it out, smooth as a tide chart.");
            startSound(clinkSnd);
            pickupObject(InventoryItems::windupKey, InventoryItems);
            egoSay("The key comes down like a settled invoice. I sign for it by holding on.");
            actorSay(capstan, "On the house: the third key isn't lost. It's retired.");
            actorSay(capstan, "Ask the old crank up the hill how retirement's paying.");
            egoSay("She says it like a name and not a description.");
            setObjectState(ransomDesk, 2);  setObjectState(trophyWall, 2);
        }
  [4] "Let me think."                        — exit tree

TalkTo (post-parley):
    egoSay("She's drilling the crew on crank form. Heave, hold, quarter-turn. The shanty writes itself.");
    actorSay(capstan, "Invoice us when the city's ready, wind-up act.");
```

**trophyWall** —
- LookAt (state 1): `"Plaques: BEST KNOTS. FASTEST REEL. EMPLOYEE OF THE EPOCH. All one employee, all older than the Dynamo."` / `"Under them, an old crew photo. One winder stands apart, up a hill of his own already."` *(← theft-path Old Crank plant: present on both routes, paid by Capstan's mouth on the parley route)*
- LookAt (state 2, post-parley): `"The work order hangs on a fresh nail. First new plaque of the epoch."`

**doorAlley** —
- LookAt: `"The famous steel door, from the famous inside. The red lamp is just a lamp in here."`
- Open/Use (pre-`keyRecovered`): `"Barred. It's the emergency exit, and my being here isn't an emergency yet. Says the doorbot's posture."`
- Open/Use (post-`keyRecovered`): silent → `putActorAt(VAR_EGO, 66, 120, AlleyRoom); startRoom(AlleyRoom);`
- Smell: `"Airtight from this side too. Commitment."`

**hatch** (loft) —
- Open (first; sets `loftEntered`, `ransomKnown` **before** speech):
```
cutscene(0) {
    startSound(creakSnd);
    setObjectState(hatch, 2);
    egoSay("I ease the hatch. Below: cards, stove, and the boardroom voice of a winch-bot reading a draft aloud.");
    actorSay(capstan, "...item four. The rewind: three keys, one city, our rates.");
    actorSay(capstan, "They retired hand-winding. Fine. Then the rewind is a private contract.");
    egoSay("The ransom. Voltina called it: a city that can be wound down can be billed for winding back up.");
    egoSay("And under the hatch, over the table: my key. Still rigged to the hook that took it.");
    egoSay("The line runs up over a pulley to a cleat by my foot.");
}
```
- Open (repeat): just toggles, no line.
- LookAt: `"A hatch over the card table. The tackle's pulley is screwed to the rafter beside it."` / `"This is where my key got reeled home."`
- **UsedWith magnet** (hatch open, `!keyRecovered`) — the caught-and-ejected flop:
```
ejectedOnce = 1;                                  // flag before speech
cutscene(0) {
    egoSay("Old reliable. I lower the magnet on its string, aiming brass.");
    egoSay("The magnet ignores brass — and finds the pot of washers. Steel, the lot of them.");
    startSound(washersSnd);
    egoSay("The pot sings. Four heads come up in close harmony.");
    actorSay(capstan, "Loft.");
    egoSay("Two of them come up the outside rigging like weather. Boarding is the one skill they kept current.");
    startSound(thudSnd);
    egoSay("I am escorted down and out with one Rustler per arm. Professional courtesy.");
    egoSay("Behind me, the slot opens. The eye confirms I'm still ejected. I am.");
    putActorAt(VAR_EGO, 66, 120, AlleyRoom);
    startRoom(AlleyRoom);
}
```
- UsedWith magnet (hatch closed): `"Through a shut hatch, the magnet would be fishing for the hatch."`

**loftCleat** —
- LookAt (hatch closed): `"A cleat, tied off sailor-tight. The line disappears through a shut hatch. Could be anything down there. Anchors. Laundry."` *(points at the hatch — fair-play)*
- LookAt (hatch open, loaded): `"A brass cleat, tied off sailor-tight. The line goes over the pulley and down to my key."`
- LookAt (slack): `"Line's slack. The rig is between engagements."`
- **Use** (hatch open, `!keyRecovered`) — the steal:
```
keyRecovered = 1;  keyByTheft = 1;                // flags before speech
cutscene(0) {
    egoSay("I take the line off the cleat. The trick is to reel like you're nobody.");
    startSound(reelSnd);
    egoSay("Quarter-turn at a time, between shanty beats. The key rises past four hats and zero glances.");
    setObjectState(keyOnLine, 2);
    startSound(clinkSnd);
    pickupObject(InventoryItems::windupKey, InventoryItems);
    egoSay("Brass in hand, off their own hook. They stole it by fishing. The harbor keeps what this town drops.");
    egoSay("Below, somebody finally folds. Time to be a rumor.");
}
```
- Use (hatch closed): `"Reeling in mystery cargo through a shut hatch is how stories start. Hatch first."`
- Use (slack): `"Nothing left on the line but precedent."`

**loftShutter** —
- LookAt: `"The shutter the heist came home through. It latches from habit, not commitment."`
- Open/Use: silent → alley (fire-escape foot): `putActorAt(VAR_EGO, 152, 120, AlleyRoom); startRoom(AlleyRoom);`

**Post-theft front door** (tavern `doorBack`, replaces the act3 entry branch when `keyByTheft`):
```
startSound(knockSnd);
egoSay("CLANG-CLANG. CLANG. CLANG-CLANG.");
egoSay("The slot opens. The eye looks at me for a long time.");
actorSay(slotEye, "Intermission, buddy.");
egoSay("The slot closes. Fair.");
```

---

## 5. Music brief + SFX

### "The Rustlers' Den" (`tools/genmusic.py`)

- **16 bars, 4/4, G minor, 92 BPM.** `DEN_BARS = 16; DEN_BPM = 92; DEN_LOOP_BEATS = DEN_BARS * 4 + 1  # = 65`. Room script: `imPlayerSetLoop(denSnd, 999, 1, 0, 65, 0)` + the standard watchdog loop.
- **Shape:** a work-shanty gone indoor — two 8-bar passes. `PROG = [Gm Gm Cm Cm | D7 Gm Cm D7 | Gm Gm Eb Eb | Cm D7 Gm Gm]`. Bass stomps roots on beats 1 and 3 only (boots on planks, no walk — this is the alley blues' meaner cousin). Kick doubles the stomp; snare on 2 and 4, no hat (sparser = menace). Lead enters bar 3, call-and-response phrases that always land a beat late, like a crew that hauls on "heave" not "ho."
- **Instruments** (AUDIO.md FM-fallback discipline): lead **GM 21 accordion** — audition the OPL2 fallback in the browser first; if it mushes, drop to GM 80 square lead (the house sound). Bass GM 38 synth bass. Drums KICK/SNARE only.
- **The detuning hum lands here (N-A5):** the lead channel carries a constant `pitchwheel = -1638` (≈ −40 cents at the default ±2-semitone range) from tick 0. The den is downstream of the same dying hum as everyone else; its song cannot quite hold true against its own bass. This is Act 3's clock made audible *without* waiting on the global act-flag mechanism — and it is the on-screen evidence for the parley's "the hum is flat and dropping" line.
- Output: `assets/generated/audio/rustlersden.mid` → `rustlersden.soun` (the `-midi` flavor, never `-gmd`).

### SFX (`tools/genaudio.py`, 8-bit unsigned mono VOC recipes)

| File | Recipe sketch | Used by |
|---|---|---|
| `barlift.voc` | `concat(noise_burst(0.35, 0.45, 9), partials(0.4, [(82,1.0,7),(164,0.55,9),(247,0.3,12)]))` — scrape, then a heavy thunk | the door bar lifting (4a) |
| `reel.voc` | 14 clicks: `partials(0.03, [(2300,0.6,90),(1150,0.3,70)])` with gaps shrinking 0.09s→0.04s — a fishing reel paid out carefully | the cleat steal |
| `winch.voc` | 6 slow clicks `partials(0.05, [(1400,0.7,60),(700,0.4,40)])` at 0.16s intervals over a low-amp reuse of the creak partials | Capstan paying the key down |
| `washers.voc` | 6 staggered `partials` bursts, 2.8–5.2 kHz, decays 20–35, onsets 0–0.18s, mixed — a pot of steel washers singing | the magnet flop |
| `scribble.voc` | three `noise_burst(0.08, 0.35, 45)` with 0.05s gaps | the work order |
| *(reused)* | `knock`, `creak`, `clink`, `pickup`, `thud` | throughout |

**Dub casting (NPC-DIALOG CAST contract):** Capstan — a low female piper voice (e.g. `en_GB-alba-medium`, `asetrate=48000*0.88` + a slow flanger: cable under load); slot-eye keeps the voice assigned at conversion rank 2. New talk color for Capstan per pipeline step 1, with the VP8 probe take before trust.

---

## 6. Walkthrougher beats

### Canonical validate (appended to `full-run.play.yaml`; parley path — it films the face, the want, and the contest)

```yaml
  # --------------------------------- Scene 09: the Rustlers' hideout
  - name: the-empty-table          # breadcrumb: the game moved
    do: {verb: Examine, object: "rustlers' table"}
    expect: [talking]
  - name: the-code-pays            # 2-1-2, and the same three words open it
    do: {verb: Open, object: back door}
    expect: [talking]
    timeout: 60
    hold: 1.5
  - name: walk-in                  # silent transition (second click)
    do: {verb: Open, object: back door}
    expect:
      - pixel: {at: [70, 80], is: den-lamplight}   # den palette probe
    timeout: 60
  - name: the-management           # Capstan dictating; guest rule; her name
    cutscene: HideoutRoom.entry
    expect: [talking]
    timeout: 60
  - name: still-on-the-hook        # the key, filed where it landed
    do: {verb: Examine, object: key on a line}
    expect: [talking]
  - name: the-going-rate           # parley opens; the six-digit draft
    do: {verb: Talk to, object: Captain Capstan}
    expect: [talking]
  - name: who-winds-the-winders    # stage-1 winner
    do: {dialog: 3}                # B2 dialog-click support
    expect: [talking]
    hold: 1.5
  - name: in-writing               # stage-2 winner; the key comes down
    do: {dialog: 3}
    expect:
      - talking
      - pixel: {at: inventory.slot, is: bright-brass}   # Key #1 returns
    timeout: 90
  - name: the-emergency-exit       # unbarred now; silent out to the alley
    do: {verb: Open, object: steel door}
    expect:
      - pixel: {at: [88, 30], is: alley-sky}
    timeout: 60
```

### Stealth validate (`hideout-stealth.play.yaml` — second gate run; THE CONTESTS MUST BE PLAYABLE means both routes stay provably winnable)

Same boot through Scene 08, diverging at Act 3: `oiled-rungs` (Examine fire escape → talking) → `up-the-back` (Use fire escape → loft pixel probe) → `little-pitchers` (Open hatch → talking; Capstan's overheard rates) → `reel-quiet` (Use brass cleat → talking + bright-brass inventory probe) → `out-the-shutter` (Open shutter → alley probe).

### Streamer mode (perform screenplay — the arc is *try sneaky, fail funny, walk in the front like an adult*)

- `detour:` knock the alley steel door first — "Front door's the front, buddy."
- `detour:` the empty rustlers' table; the tavern piano one more time.
- `detour:` examine the fire escape (the oiled rungs read).
- climb up; `detour:` examine cleat through the shut hatch (anchors, laundry); open hatch (eavesdrop beat).
- `mistake:` Use hatch with magnet — the washers sing, "Loft.", ejected with one Rustler per arm. The ejection cutscene IS the assertion.
- knock the front; "Act Three, buddy."; the management cutscene.
- `detour:` exhibit A (the framed cease-and-desist); the slot-eye's chalk tally; the trophy wall (the crew photo); smell the stove.
- `mistake:` Pick up the key from the floor — "Four chairs scrape. I un-reach."
- `mistake:` Use key on... nothing; open parley: `mistake:` dialog 1 (RECEIPTS, GRIEVANCE, MIXED), `mistake:` dialog 2 (the camera finds the framed notice over the stove — the gag pays on film).
- dialog 3 (the arithmetic; hold on "Plans usually do."), `mistake:` stage-2 dialog 2 (the pass — "Tempting. The act, not the access."), dialog 3 (the contract; the winch; the Old Crank plant gets the chapter-card outro).

---

## 7. Planted / paid ledger

**Consumed here (planted earlier → paid in S09):**

| Plant | Planted | Paid |
|---|---|---|
| Knock-code 2-1-2 | S02 rustlers' table (canonical path); S05 hatch echo; S06 Voltina forced echo | Opens the door; the hat-Rustler half-recognizes "somewhere acoustic" |
| "Act Three, buddy" (×2 refusals) | S02 doorBack, S03 hideoutDoor | Same words, now the admission; "Intermission, buddy" / "Front door's the front" extend the runner in the same mouth |
| Hook-on-a-line tackle | S05 heist ("somebody else's magnet-on-a-string") | Key still rigged to it; the stealth steal reels it on their own gear; the parley pays it out on the same line |
| Magnet-on-a-string + brass | S01 tool; S05 hook choice | The flop teaches why they brought a hook; washers (steel) sing |
| Fire escape "rusted shut on purpose" + lookout | S03 | Lookout gone (he's at the table, glancing at where his window isn't); rungs oiled by their own heist logistics |
| Rustlers' motive (ransom the rewind) | GDD; S06 Voltina says it aloud | Capstan's dictation, drafts, and mouth — the want has a face |
| Rivet's "...or down" | S03 free facts | The plan's mechanism, finally claimed |
| Washers as "post-bolt currency" | S02 card table | The ransom's denomination; the magnet's downfall |
| POP. 8,011 | S01 sign | "Eight thousand of them, give or take this room" |
| Power model (hum winds mainsprings remotely; hand-winding crude backup) | S01 board (forced, B4/embodiment fix) | Capstan's entire biography and the winning argument: *who winds the winders?* |
| "I wind myself. Eight full turns." | S05 | Sprocket = "the wind-up act" in every Rustler mouth |
| Rivet's municipal-lie collecting | S03 | Cousin gag: the dusted, framed cease-and-desist |

**Created here (paid later):**

| Plant | Pays in |
|---|---|
| "Ask the old crank up the hill how retirement's paying." + the crew-photo winder "up a hill of his own already" | S10 — first on-screen Old Crank pointer on BOTH routes (closes the N-A10 debt) |
| "The third key isn't lost. It's retired." | S10 — the Crank-IS-Key-#3 reveal stops being unsourced |
| The work order / `keyByParley` | S11 — the rewind needs hands; the wind-up crew is contracted (finale contract, §10) |
| `keyByTheft` | S10/S11 flavor: the crew turns up at the Dynamo anyway, contract unsigned, grievance intact (one branch line, finale's call) |
| The den song's bent lead (−40 cents) | S11's detuning ramp has a mid-act waypoint to be continuous with |

---

## 8. Embodiment audit (of this document's own text)

**Power model** (the hum winds every mainspring remotely; hand-winding is the crude backup): this scene is *built on* the model rather than near it. Capstan's biography (a professional hand-winder made obsolete the day the hum started), her trade ("Hand-winding is what we do"), the ransom mechanism (corner the backup before the primary dies), and the kill-shot argument ("who winds the winders?" — the winders are hum-wound too) are all derivations from the stated model, not new physics. No battery, fuel, or breath language anywhere in the draft. "My chest compartment relaxes by one percent" keeps the body mechanical.

**Senses:** The eavesdrop is an open hatch directly over the speaker — an air path, not narration-through-walls (the chair's founding sin, avoided). The knock beats are sound on metal. Smell lines audited against the B10 do-not-reuse list: all are flat facts, escalating lists, or institutional jokes — zero `[material] and [abstract noun]` zeugmas. The one ranged smell (keyOnLine) hedges itself on the page ("out of nose range").

**Props:** The key is brass and forearm-sized: the magnet refusal is correct physics and retro-justifies the heist's hook. The washers are steel — the same metal the magnet fished from the drain, so the flop is consistent with the tool's whole career. The tackle already lifted this key once (S05), and Capstan is stenciled for 4,000 lbs — every load in the scene is inside rated capacity. The ransom note and the work order are one sheet, two sides, tracked through both desk states. The quill is lashed to her crank — crank-hands can't hold a pen, so the text says so before a critic does.

**Spatial:** Hideout = tavern's east wall (west door) to alley (east door); the stove flue exits through the shared tavern chimney; the loft shutter sits at the top of the alley fire escape the heist crew demonstrably used (it's how the oiled rungs become a clue). Hatch (x=118) hangs over keyOnLine (x=122) over the card table — the rig lines up on screen. Loft and den walkboxes are disconnected; nobody walks a ladder that isn't painted. The loft floor is at y≈44 so a 34-px actor's head stays on the 144-px stage.

**Counts:** Rustler census = six: Capstan, the doorbot, the tavern trio, the ex-lookout. "Four hands of cards" ✓; "four heads come up" ✓; "two of them come up the rigging" then "one Rustler per arm" ✓; "Six of you" ✓ (all six are on screen when Sprocket says it). "Eight thousand of them, **give or take this room**" blurs the 8,011 to survive its own arithmetic. The chalk tally's two columns match Sprocket's two prior knocks (one right code refused, one wrong knock-knock).

**Register compliance:** every `actorSay` ≤12 words; exclamation appears only in Capstan's "Crew!" (NPCs may perform); the meta runner stays exclusively in the slot-eye's mouth; no Sprocket line names an act; no punchline grades itself ("Plans usually do." is a button, not a medal); banned constructions ("it's all they do", "with opinions", "destiny", "thematically significant") — zero occurrences.

---

## 9. New state (hideout.sch + addenda)

```
room HideoutRoom {
    bit denEntered;        // front entry cutscene played
    bit loftEntered;       // hatch eavesdrop played
    bit ransomKnown;       // set by EITHER entry beat; gates the steal + parley winner
    bit arithmeticLanded;  // parley stage 1 won
    bit keyRecovered;      // either route
    bit keyByParley;
    bit keyByTheft;
    bit ejectedOnce;       // magnet flop happened (retry flavor line)
}
// tavern.sch: bit doorBackOpen;
// alley.sch:  bit enteredViaLoft;   (transient routing flag)
```

`keyRecovered` is a bit even though `getObjectOwner(windupKey) == VAR_EGO` would serve, because scenes 10–11 will consume the keys at the Dynamo and must still know the recovery happened (the owner==VAR_EGO pitfall, NOTES.md).

## 10. Contracts with neighboring scenes (cross-doc, Wave 1)

1. **Scene 08** owns `bit act3Started`, set in its closing cutscene, whose final beat must point back downhill (suggested closing image: the Mayor's aides fleeing with the hum a half-step flat, and Sprocket: "Everyone official is out of keys. The unofficial ones drink downstairs.").
2. **Scene 06** must (a) ship `InventoryItems::keyTwo` surviving to Act 3, and (b) make Voltina's forced knock-code echo **set `heardKnockCode`** — it is knowledge transfer either way, and it makes this scene's door unbrickable. Her "says the motive out loud" beat is consumed verbatim by the hatch line ("Voltina called it").
3. **Scene 10** receives the Old Crank plant ("up the hill", "retirement") and "the third key isn't lost. It's retired."
4. **Scene 11** receives the wind-up crew: `keyByParley` ⇒ contracted hands at the rewind; `keyByTheft` ⇒ they arrive uncontracted and the finale decides the price of that. The finale's detune ramp should pass through −40 cents (this room's lead) on its way down.
5. **B2/B8 dialog-tree machinery** (dialog UI + walkthrougher `{dialog: N}` shots) is a hard dependency, per the desk's standing ruling — already scheduled ahead of all Act 2–3 content.