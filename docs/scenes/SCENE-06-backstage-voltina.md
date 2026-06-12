All required reading done (PRODUCTION-PLAN, GDD, NOTES, CHARTER + all three editorial reports, NPC-DIALOG, tavern.scc, theater.scc, common.sch/dialog.scc, genmusic/genaudio, the full-run screenplay). Here is the complete design doc.

---

# SCENE 06 — Backstage: Madame Voltina
*Design doc for `docs/scenes/SCENE-06.md` — Wave 1 deliverable. Implementer builds `game/backstage.scc/.sch`, `draw_backstage` + `BACK_GEOM` + the Voltina costume in `tools/genassets.py`, the `seance` theme in `tools/genmusic.py`, five SFX in `tools/genaudio.py`, and the screenplay extension. HARD DEPENDENCY: B2+B8 (dialog-tree UI wired, walkthrougher clicks dialog options, `windTurns` recorded) ships first — desk ruling, PRODUCTION-PLAN row 06.*

---

## 1. Scene goal + the three-keys spine

**Goal:** Convert the Act-2 midpoint loss into the Act-3 plan, and put Key #2 in the player's pocket.

Sprocket arrives **key-less and robbed** — zero keys, one grievance. He leaves with:

| Spine thread | State entering | State leaving | Mechanism |
|---|---|---|---|
| **Key #1** | stolen mid-ovation (scene 05) | located: behind a door that answers to **CLANG-CLANG. CLANG. CLANG-CLANG.** | Voltina's FUTURE card echoes the knock-code on the critical path (B9 deferral: "forced echo before Act 3" — this is it) |
| **Key #2** | a rumor ("guards… things" — the clerk) | **in inventory** | her price: a reading of the player's own playthrough (NOT a fetch) |
| **Key #3** | zero plants in six scenes (N-A10) | Old Crank named on screen for the first time; "the key that winds itself" tease paid; oblique person-plant ("ask him where the third one *stands*") | dialog option, on the canonical path |
| **Antagonist motive** | blank (N-A9 disposition: "Voltina owns the reveal in Act 2") | said out loud, in her mouth: **they mean to ransom the rewind** | the FUTURE card cutscene |
| **Her want** (N-A6, no vending machines) | — | stated: a city with one future puts fortune-tellers out of work; she wants tomorrow negotiable again | dialog option + handover closer |

This is the act's information climax: the player walks out knowing *who*, *why*, *how to get in*, and *where the third key stands* — every Act 3 beat is now planted in fair play.

---

## 2. The puzzle chain

No item is fetched in this scene. Every answer is already in the player's pocket or head — the puzzle is *recognizing your own playthrough*. The scene's contest is **the Reading**: three cards, each answered by the player, each verifiable against real game state.

### Numbered graph

```
(pre) scene 05 complete: backstagePass owned, windupKey owner==0,
      inventory = [poster, magnet, oilVoucher, backstagePass]

 1. Open stage door (pass held) ──silent──> BackstageRoom
      └─ entry cutscene: robbed-arrival beat, "Mind the cables." paid
 2. Talk to Madame Voltina ──> intro cutscene
      └─ establishes: jar = Key #2 (visible, stenciled), price = a reading,
         coil mechanics ("carried things remember" / "lie and the coil bills you"),
         Card I dealt
 3. CARD I (THE PAST): Use official notice with reading table   [AGENCY]
      wrong offers (magnet/voucher/pass) = bespoke true-but-rejected
      readings of the player's route; no fail state, card waits
 4. CARD II (THE PRESENT): Use oil voucher with reading table   [AGENCY]
      wrong offers = bespoke readings (incl. windTurns branch on the pass)
 5. CARD III (THE FUTURE): dialog tree, 3 options                [AGENCY]
      a) offer the pass        -> flop (funny, repeatable)
      b) bluff about the key   -> zap gag (funny, repeatable, teaches stakes)
      c) the truth: robbed     -> climax cutscene
 6. Climax: motive reveal + knock-code echo (branch: heardKnockCode)
      + jar grounded + KEY #2 -> inventory
 7. Dialog option "the key that winds itself" -> Old Crank plant
      (canonical path includes it; not a gate)
 8. Exit to theater (silent door)
```

### Fair-play audit — every hint's source named

| Step | Solution | Hint sources (all on screen BEFORE needed) |
|---|---|---|
| 1 | pass opens door | scene 05 prize cutscene; stagehand refusal line (shipped) |
| 2 | talk to her | she hails the player in the entry cutscene ("Mind the cables." — you cannot miss her) |
| 3 | the notice = "the lie the city printed" | **(a)** the card's own text, spoken by Voltina; **(b)** the notice's inventory LookAt — "Nothing says 'something is wrong' like an official notice that nothing is wrong" (shipped, docks); **(c)** Rivet "collects municipal lies" (shipped, alley, canonical path) |
| 4 | the voucher = "the debt this city owes you" | **(a)** card text; **(b)** voucher LookAt: a winning, redeemable, "the only establishment that participates has a velvet rope" (shipped); **(c)** the card woodcut: an open hand, palm up |
| 5 | tell the truth | **(a)** her stage-door "I know." (shipped — she cannot be lied to about the key); **(b)** Cards I/II establish the coil's truth-arc behavior *before* the stakes rise — the feedback IS the tutorial; **(c)** her intro: "Lie, and the coil bills you." (explicit rule, stated once, before it's needed); **(d)** the bluff option's zap is a free, harmless demonstration |
| 6 | knock-code | **gift, not puzzle** — Act 3's key is deliberately handed to every player (B9 deferral discharged). Branch: eavesdroppers get recognition, cold players get the rhythm fresh |
| 7 | Old Crank | forward plant, oblique by design (it's Act 3's twist, not this scene's lock) |

**Adventure-sin check:** no moon logic (each card names a *property*, never the item — the N-A2 "answer key on first contact" pattern is avoided: "the lie the city printed" requires one inference, and three prior plants fund it); no pixel hunt (the jar is 28×48 and humming); no lock-and-key fatigue (zero fetches — the chain's shape is new: *prove your own history*); the wrong choices are jokes, not punishments; nothing dead-ends (wrong cards return to a patient table, flop dialog options return to the tree).

### The agency beat (desk mandate: THE CONTESTS MUST BE PLAYABLE)

The reading is three real decisions with differentiated outcomes:

- **Cards I & II** — the player chooses which of four inventory items to stake. Wrong items aren't generic refusals: the coil *reads them anyway*, and the reading is a true recap of what that object did in this playthrough (the magnet fished the drain; the pass was won at the player's actual `windTurns` count). The wrong answers are content, personalized by route — the desk's "her coils read the player's actual playthrough" requirement, made of branches the walkthrougher state flags already prove.
- **Card III** — a dialog tree where the winning move is a *confession*, the bluff is the scene's best zap gag, and the rule that decides it ("the coil bills for lies") was taught two cards ago. Two flops funny, one winner inferable: exactly the B2 riddle-duel shape, in a new costume.
- **No spectator victory:** nothing in this scene auto-fires. `TalkTo` with the right inventory does NOT resolve the scene (contrast B2/B8's sins) — the player places every card.

---

## 3. Object table

Stage is 320×144 (verb panel below y=144, per `genassets.py` `W, H = 320, 144`). New `BACK_GEOM` in genassets; hotspots default to rect center, walkbox is the floor band y≈104–140 with an apron in front of the table.

| Object | Rect (x,y,w,h) | dir | Verbs handled | States |
|---|---|---|---|---|
| `doorStage` — "stage door" | (0, 56, 24, 48) | E | LookAt; Open/Use (**silent** `startRoom(TheaterRoom)`) | 1 |
| `costumeRack` — "costume rack" | (32, 36, 44, 60) | N | LookAt, Use, Smell | 1 |
| `ghostLight` — "ghost light" | (84, 52, 16, 52) | N | LookAt, Use | 2: lit / dark — a `signFlicker`-class loop makes it stutter (the deadline texture, N-A5; **mind the stopScript bug**) |
| `fuseBox` — "fuse box" | (296, 24, 18, 28) | E | LookAt, Open/Use | 1 |
| `voltina` — "Madame Voltina" (actor-object: hotspot routes via `actorObject[]`; speech/anim via costumed actor) | (148, 28, 48, 56); actor feet at (172, 100), `setActorIgnoreBoxes` | S | LookAt, TalkTo (dialog hub), Give/UsedWith (alias to table), Smell | actor costume: stand + talk-A + talk-B (coil arcs) |
| `readingTable` — "reading table" | (140, 84, 64, 28) | N | LookAt, Use, Give/UsedWith (the cards), Smell | 5: bare felt / Card I up / Card II up / Card III face-down / Card III turned (woodcut: a city upside down, being shaken) |
| `cardCarousel` — "card carousel" | (208, 64, 24, 32) | N | LookAt, PickUp, Use | 1 |
| `keyJar` — "key in a jar" | (244, 48, 28, 48) | N | LookAt, Open/Use/PickUp (zap gag), Smell | 2: jar w/ brass key / jar empty |
| `cables` — "cables" | (120, 116, 150, 16) | N | LookAt, Use/Move, Smell | 1 |
| **inventory:** `voltKey` — "the second key" | (icon, brass) | — | LookAt, Use, Smell, UsedWith routing | — |

**Room art brief (`draw_backstage`):** brick back wall (rust 17/19) with rope, sandbags, counterweight rail top-left; Voltina's parlor center-right — a half-shell of deep curtain behind her spot, the felt table, carousel, pedestal jar; cables painted from the fuse box along the floor strip into the booth; ghost light is the one warm sodium point left of center. Animating element (GDD rule): the ghost-light flicker + the jar's faint arc shimmer.

**Voltina's look (genassets costume spec — first costumed talking actor):**
- Sprite ~36×56 (taller than Sprocket's 34 — she should loom politely).
- Body: a brass coil column (3–4 stacked torus rings, palette brass 46/47) wrapped in a deep-rust shawl (17/19) pinned with a fuse brooch; ceramic-insulator earrings.
- Head: a glass dome (teal glass tones) with a plasma filament inside — **there is no crystal ball; she's the ball.**
- Frames: `stand` (filament idle, faint), `talk-A` (arc from dome to left shoulder electrode, dome bright), `talk-B` (arc to right electrode). Driven as costume talk-limb frames per the sprocket.scost pattern (Makefile `%.scost` rule is already generic — NPC-DIALOG §6.10). Alternating A/B reads as crackle.
- **Talk color:** claim palette index **106** (`BETTY_COLOR`, the fossil "talk-2" probe already plumbed through transcript/driver/dub — NPC-DIALOG open question 7) IF its hue reads as electric lilac/teal on VP8 footage; otherwise assign slot 108 with a `"talk-voltina"` probe + the scenery-collision build assert. One probe take through VP8 before trusting it.
- Dub CAST entry: `en_US-kristin-medium` + chorus + long echo (`aecho`) + lowpass 5000 (NPC-DIALOG §4.6).

---

## 4. Full dialog draft

Register rules applied: Sprocket = reported deadpan narration; Voltina = direct punchlines ≤12 words; no double-telling; NPC punchline → Sprocket button; walkthrough-path lines FIRST in source per handler; no smell zeugma, no self-grading, no Sprocket act-naming, caps only diegetic.

### 4.1 Theater-side change (theater.scc, `backstageDoor`)

The shipped greeting **stays** (it's canon — the tease) but converts to actorSay per NPC-DIALOG example A, and the door grows a second, **silent** transition click:

```c
case Open:
case Use:
    // walkthrough path first: after the greeting, the door just opens
    if (voltinaGreeted) {                       // silent transition (NOTES rule)
        putActorAt(VAR_EGO, 30, 120, BackstageRoom);
        startRoom(BackstageRoom);
        return;
    }
    if (getObjectOwner(InventoryItems::backstagePass) == VAR_EGO) {
        voltinaGreeted = 1;                     // flag before speech
        cutscene(0) {
            // LANDMINE: actorSay drops lines for actors not in the room —
            // park voltina_a at the door's text position first.
            putActorAt(voltina_a, 296, 70, TheaterRoom);
            egoSay("I flash the pass. The stagehand reads it twice. Nothing in his build explains how he steps aside, but he does.");
            waitForMessage();
            egoSay("The dark behind him smells like ozone and incense.");
            waitForMessage();
            actorSay(voltina_a, "I have been expecting you, key-bearer.");
            waitForMessage();
            egoSay("I start to explain about the key.");
            waitForMessage();
            actorSay(voltina_a, "I know.");
            waitForMessage();
            actorSay(voltina_a, "Ask me sometime about the key that winds itself. Mind the cables.");
            waitForMessage();
            egoSay("Madame Voltina. I'm going to need a minute, and possibly a will.");
            waitForMessage();
        }
        return;
    }
    egoSay("A stagehand the shape of a filing cabinet fills the doorway. Pass-holders only.");
    return;
```

### 4.2 Backstage entry (first visit cutscene)

```c
local script entry() {
    startScript(1, musicLoop, []);                 // the seance theme
    putActorAt(voltina_a, 172, 100, BackstageRoom); // ALWAYS, every entry
    unless (visitedBackstage) {
        visitedBackstage = 1;
        cutscene(2) {
            putActorAt(VAR_EGO, 30, 120, BackstageRoom);
            walkActorTo(VAR_EGO, 80, 124);
            waitForActor(VAR_EGO);
            egoSay("Backstage. Rope, sandbags, and a fortune-teller's parlor where the fire exit should be.");
            waitForMessage();
            egoSay("Three keys wind this city back up. As of the ovation, I hold none of them.");
            waitForMessage();
            egoSay("The cables on the floor all run one direction. The direction glows.");
            waitForMessage();
            actorSay(voltina_a, "Mind the cables.");
            waitForMessage();
            egoSay("I mind the cables.");
            waitForMessage();
        }
    }
}
```

### 4.3 Madame Voltina (actor-object)

```c
case LookAt:
    egoSay("A tesla coil in a shawl. Her head is a glass dome with weather inside.");
    waitForMessage();
    egoSay("There's no crystal ball on the table. She's the ball.");
    return;

case TalkTo:
    unless (metVoltina) {
        metVoltina = 1;
        readingStage = 1;                       // flags before speech
        cutscene(0) {
            actorSay(voltina_a, "Sprocket. Late of the docks, lately of the stage.");
            waitForMessage();
            egoSay("I ask how she follows my career.");
            waitForMessage();
            actorSay(voltina_a, "The theater is wired. I am the wiring.");
            waitForMessage();
            actorSay(voltina_a, "You came for the one in the jar.");
            waitForMessage();
            egoSay("There's a jar. In the jar: a brass key the size of my forearm. The stencil on the glass matches the crate my luck came in.");
            waitForMessage();
            actorSay(voltina_a, "The Order left it with me. I vet the bearer.");
            waitForMessage();
            actorSay(voltina_a, "The price is a reading. Yours.");
            waitForMessage();
            egoSay("I ask what the reading costs. The reading is the cost.");
            waitForMessage();
            actorSay(voltina_a, "Used to be I'd read you cold. The brownouts ended cold reads.");
            waitForMessage();
            actorSay(voltina_a, "Three cards. Past, present, future.");
            waitForMessage();
            actorSay(voltina_a, "Answer each with what you carry. Carried things remember.");
            waitForMessage();
            actorSay(voltina_a, "Lie, and the coil bills you.");
            waitForMessage();
            startSound(dealSnd);
            setObjectState(readingTable, 2);    // CARD I up
            egoSay("A card snaps onto the felt. A woodcut of a printing press, smiling.");
            waitForMessage();
            actorSay(voltina_a, "The past. Place the lie this city printed you.");
            waitForMessage();
        }
        return;
    }
    startScript(voltinaHub, []);                // dialog tree, below
    return;

case Give:
case UsedWith:
    // alias: handing her things = placing them on the table
    startObjectVerb(readingTable, UsedWith, objB);   // implementer: route per
    return;                                          // inventoryitems.scc pattern

case Smell:
    egoSay("Ozone at a concentration my manual files under 'leave'.");
    return;
```

**The dialog hub (`voltinaHub`, dialog.scc UI; ≤5 options, MAX_DIALOG_LINES):**

Options shown (state-dependent):
1. *"Tell me about the key that winds itself."* — until asked
2. *"Who took my key?"*
3. *"What do you get out of vetting key-bearers?"* — until asked
4. *"That's all for now."*

```
OPTION 1 (the Old Crank plant — canonical path):
    egoSay("I ask about the key that winds itself. As instructed.");
    actorSay(voltina_a, "Old Crank. Up the hill, behind the fence. Older than the hum.");
    actorSay(voltina_a, "He was winding himself before the city needed winding.");
    actorSay(voltina_a, "When you hold two keys, ask him where the third one stands.");
    egoSay("A hermit, a fence, and a riddle with posture.");

OPTION 2, before the reading completes:
    actorSay(voltina_a, "The cards answer that one. Place them.");
    egoSay("The felt is greener on the business side of the table.");
OPTION 2, after:
    actorSay(voltina_a, "Their door answers to the knock. Doors are not loyal.");
    egoSay("Twice. Once. Twice. I've got it.");

OPTION 3 (her want — N-A6 discharge):
    egoSay("I ask what she gets out of vetting key-bearers.");
    actorSay(voltina_a, "A city with one future puts fortune-tellers out of work.");
    actorSay(voltina_a, "Everyone stopping is not a fortune. It's a schedule.");
    egoSay("She wants tomorrow back on the table. Professionally.");

OPTION 4:
    actorSay(voltina_a, "Mind the cables.");
    egoSay("I'm learning.");
```

### 4.4 The reading table

```c
case LookAt:
    if (readingStage == 0) {
        egoSay("Green felt, scorch marks in threes. The scorches are tidy. The felt has accepted its life.");
        return;
    }
    if (readingStage == 1) { egoSay("Card one, face up: a printing press, smiling. The felt waits."); return; }
    if (readingStage == 2) { egoSay("Card two, face up: an open hand, palm up. Municipal."); return; }
    if (readingStage == 3) { egoSay("Card three, face down. The first two didn't do that."); return; }
    egoSay("Three cards spent, one key paid. The felt looks satisfied. For felt.");
    return;

case Give:
case UsedWith:
    // ============ CARD I — walkthrough path FIRST in source ============
    if (readingStage == 1 && objB == InventoryItems::poster) {
        readingStage = 2;                              // flag before speech
        cutscene(0) {
            startSound(arcSnd);
            egoSay("The arc hits the notice and goes the color of a courtroom.");
            waitForMessage();
            actorSay(voltina_a, "NOTHING IS WRONG. Issued in bulk. Believed by no one.");
            waitForMessage();
            actorSay(voltina_a, "You pried it off a public board. Past, verified.");
            waitForMessage();
            egoSay("She slides it back across the felt. The past is mine to keep.");
            waitForMessage();
            startSound(dealSnd);
            setObjectState(readingTable, 3);           // CARD II up
            egoSay("Card two: a woodcut of an open hand, palm up. Municipal.");
            waitForMessage();
            actorSay(voltina_a, "The present. Place the debt this city owes you.");
            waitForMessage();
        }
        return;
    }
    // ============ CARD II — walkthrough path ============
    if (readingStage == 2 && objB == InventoryItems::oilVoucher) {
        readingStage = 3;
        cutscene(0) {
            startSound(arcSnd);
            actorSay(voltina_a, "One free oil. Redeemable where the rope is velvet.");
            waitForMessage();
            egoSay("She taps it twice with an arc and hands it back uncashed.");
            waitForMessage();
            actorSay(voltina_a, "Cash it where City Hall drinks. Debts talk after hours.");
            waitForMessage();
            startSound(dealSnd);
            setObjectState(readingTable, 4);           // CARD III, face down
            egoSay("Card three lands face down. The first two didn't do that.");
            waitForMessage();
            actorSay(voltina_a, "The future. Place the key.");
            waitForMessage();
            egoSay("The table waits. My pockets hold a notice, a magnet, a voucher, and a pass. Notably: no key.");
            waitForMessage();
            startScript(futureCard, []);               // the dialog tree
        }
        return;
    }
    // ============ wrong offers, CARD I (after the success path) ============
    if (readingStage == 1) {
        if (objB == InventoryItems::magnet) {
            startSound(fizzleSnd);
            actorSay(voltina_a, "It fished nine bolts out of a drain. True. Not printed.");
            waitForMessage();
            egoSay("The coil reads by touch, and everything I've carried is a diary.");
            return;
        }
        if (objB == InventoryItems::oilVoucher) {
            startSound(fizzleSnd);
            actorSay(voltina_a, "Ink so fresh it's still deciding. That isn't past. That's Tuesday.");
            return;
        }
        if (objB == InventoryItems::backstagePass) {
            startSound(fizzleSnd);
            actorSay(voltina_a, "You earned that an hour ago. The past takes longer to print.");
            return;
        }
        actorSay(voltina_a, "The card is patient.");          // generic repeat
        return;
    }
    // ============ wrong offers, CARD II ============
    if (readingStage == 2) {
        if (objB == InventoryItems::poster) {
            startSound(fizzleSnd);
            actorSay(voltina_a, "That's what the city owes itself. Pockets again.");
            return;
        }
        if (objB == InventoryItems::magnet) {
            startSound(fizzleSnd);
            actorSay(voltina_a, "The harbor paid that one. Nine bolts, settled.");
            return;
        }
        if (objB == InventoryItems::backstagePass) {
            startSound(fizzleSnd);
            // personalization branch — gWindTurns is the B8 global
            if (gWindTurns > 5) {
                actorSay(voltina_a, "You won that at eight turns. Regulation is five.");
                waitForMessage();
                egoSay("The coil watched my act. Everyone's a critic with provenance.");
                return;
            }
            actorSay(voltina_a, "Square winnings. A pass is permission, not debt.");
            return;
        }
        actorSay(voltina_a, "The card is patient.");
        return;
    }
    if (readingStage >= 4) {
        egoSay("The reading is over. The felt is off the clock.");
        return;
    }
    egoSay("She hasn't dealt yet. Cards first, business after.");
    return;

case Use:
    egoSay("It's her table. I've seen what the coil does to volunteers.");
    return;
case Smell:
    egoSay("Ozone. Old felt. More ozone.");
    return;
```

*(Implementer note: the `gWindTurns > 5` literal — "eight turns" — assumes B8's winner is 8. If B8 ships 6/7 as alternate winners, use three literal-string variants bucketed per count; never `%i{}` interpolation — variable text breaks transcript pairing and the dub cache.)*

### 4.5 Card III — the future (dialog tree, `futureCard`)

Options:
1. *"Offer the backstage pass. It opens doors."*
2. *"The key is in my other chassis."*
3. *"The truth: I had it, I advertised it, a hook took it."*

```
OPTION 1 (flop, repeatable):
    egoSay("I deal the pass onto the felt with intent.");
    startSound(fizzleSnd);
    actorSay(voltina_a, "That opens one door. The future has more doors.");
    -> back to the tree

OPTION 2 (the zap gag, repeatable):
    egoSay("I explain that the key is in my other chassis.");
    startSound(arcBigSnd);
    egoSay("The arc that finds me is small, educational, and extremely specific.");
    actorSay(voltina_a, "The coil bills for lies.");
    -> back to the tree

OPTION 3 (winner — the climax cutscene):
    readingStage = 4; gHeardKnockCode = 1; heardKnockCode = 1;   // flags first
    egoSay("The truth, then. I had it. I put my name in bulbs and the key on a lit stage, and a hook took it at the bow.");
    actorSay(voltina_a, "Truth.");
    egoSay("The arc doesn't flinch. Neither of us mentions whose idea the bulbs were.");
    startSound(creakSnd);
    setObjectState(readingTable, 5);
    egoSay("She turns the card with an arc. A woodcut of a city, held upside down, being shaken.");
    actorSay(voltina_a, "The Rustlers don't want a dark city.");
    actorSay(voltina_a, "They want a city that pays to stay lit.");
    actorSay(voltina_a, "Wind it down. Ransom the rewind. Salvage rates. Their words.");
    egoSay("Piracy, with invoices.");
    actorSay(voltina_a, "Your future knocks. Twice. Once. Twice.");
    // dub note: canonical path HAS heardKnockCode (B9 promoted the eavesdrop
    // onto the validate path) -> recognition branch goes FIRST in source.
    [if tavern eavesdrop already done]
        egoSay("I know that knock. It plays cards in the Scrap & Barrel.");
    [else]
        egoSay("Twice. Once. Twice. I file the rhythm somewhere fireproof.");
    actorSay(voltina_a, "The reading is paid. Ground yourself.");
    egoSay("She earths the jar with a rod the size of a conductor's baton. The lid gives a small, ceremonial pop.");
    startSound(jarSnd);
    setObjectState(keyJar, 2);                       // jar empty
    startSound(pickupSnd);
    pickupObject(InventoryItems::voltKey, InventoryItems);
    actorSay(voltina_a, "Key the second. Lose it slower.");
    egoSay("One key in hand, one behind a knock, one up a hill. The math is moving again.");
    actorSay(voltina_a, "Make tomorrow negotiable again. I have appointments.");
```

### 4.6 The key jar

```c
case LookAt:
    if (readingStage >= 4) {
        egoSay("Empty. The stencil stays: PROPERTY OF THE ORDER OF THE WIND-UP KEY. One absence, well documented.");
        return;
    }
    egoSay("A brass wind-up key in a glass jar. The jar is stenciled: PROPERTY OF THE ORDER OF THE WIND-UP KEY.");
    waitForMessage();
    egoSay("The jar hums. Not the city's hum. A private one.");
    return;
case Open:
case Use:
case PickUp:
    if (readingStage >= 4) { egoSay("Already mine. The jar and I are square."); return; }
    startSound(arcSnd);
    egoSay("I reach. The jar reaches back.");
    waitForMessage();
    actorSay(voltina_a, "The deposit is charged. So is the jar.");
    return;
case Smell:
    egoSay("Glass, brass, and a hum I can taste in my teeth. I don't have teeth.");
    return;
```

### 4.7 Flavor hotspots

```c
// ghost light
case LookAt:
    egoSay("A bare bulb on a stand, center backstage. Theater law: it never goes out.");
    waitForMessage();
    egoSay("It's flickering.");                  // the clock, flat, on screen (art flickers too)
    return;
case Use:
    egoSay("Not my circuit. Some maintenance is above my pay grade, which is zero.");
    return;

// costume rack
case LookAt:
    egoSay("Forty years of acts on hangers. A bear suit for a bot. A bot suit for, presumably, a bear.");
    return;
case Use:
    egoSay("Nothing in my size. Everything in my price range.");
    return;
case Smell:
    egoSay("Mothballs, losing.");
    return;

// cables
case LookAt:
    egoSay("Cables, braided like the city's worst haircut. Every one of them feeds the parlor.");
    return;
case Use:
case Move:
    egoSay("Each one is load-bearing. So is her patience.");
    return;
case Smell:
    egoSay("Warm rubber.");
    return;

// fuse box
case LookAt:
    egoSay("The theater's fuse box. Somebody has labeled every single fuse HER.");
    return;
case Open:
case Use:
    egoSay("I leave it shut. The wiring outranks me, and the wiring is a person.");
    return;

// stage door (back out)
case LookAt:
    egoSay("Back to the stage. The confetti should be settling by now.");
    return;
case Open:
case Use:
    putActorAt(VAR_EGO, 270, 120, TheaterRoom);   // SILENT (NOTES rule)
    startRoom(TheaterRoom);
    return;

// card carousel
case LookAt:
    egoSay("A brass carousel of punch-cards. The holes are the fortunes. The cards are just chaperones.");
    return;
case PickUp:
case Use:
    egoSay("It deals for her. It has seniority.");
    return;
```

### 4.8 Inventory item: `voltKey` — "the second key"

```c
case LookAt:
    egoSay("Brass, forearm-sized, second of three. This one has never been on a marquee. We're keeping it that way.");
    return;
case Use:
    egoSay("It wants the Dynamo. The Dynamo wants its siblings first.");
    return;
case Smell:
    egoSay("Ozone. It kept the jar's accent.");
    return;
// UsedWith: route to objB per the inventoryitems.scc pattern (NOTES: items
// must dispatch "Use it with Y" to objB's UsedWith themselves).
```

---

## 5. Music brief + SFX list

### Music — "The Backstage Séance" (`seance`, genmusic.py idiom)

| Param | Value |
|---|---|
| Name / builder | `seance` / `build_seance()` |
| Meter / bars | **3/4**, `SEANCE_BARS = 16` (the game's first waltz — the parlor doesn't swing, it sways) |
| BPM | `SEANCE_BPM = 72` |
| Key | A minor (Am–Dm–E7–Am changes, two 8-bar passes; bar 12 borrows F to go somewhere unwise) |
| Loop | `SEANCE_LOOP_BEATS = SEANCE_BARS * 3 + 1 = 49`; script: `imPlayerSetLoop(seanceSnd, 999, 1, 0, 49, 0)` + the standard watchdog loop |
| Channels | `CH_LEAD` prog **80** (square lead) — a thin theremin-ish melody, narrow range, chromatic neighbor tones, enters bar 5 like the house style; `CH_EP` prog **4** (e-piano) — rising 3-note arpeggios on beats 2–3 only (the cards being shuffled); `CH_BASS` prog **38** — pedal drone, root held full bars (the coil's idle); `CH_DRUM` — closed hat ticks on beats 2 and 3 only, no kick (a meter ticking, not a band) |
| FM-fallback safety | programs 80/38/4 already proven in the other five themes (AUDIO.md palette rule) |
| Detuning-hum hook | the bass drone channel is the designated first customer for the N-A5 act-flag pitch-bend drift — mido `pitchwheel` on `CH_BASS`, cents scaled by act flag. Note the hook in the file docstring; implementation rides the N-A5 work item |

### SFX (genaudio.py idiom — 8-bit unsigned mono VOC, one .soun per effect)

| File | Recipe (existing ingredient functions) |
|---|---|
| `arc.voc` — truth arc | `mix(noise_burst(0.18, 0.85, 40), partials(0.18, [(3200,0.5,30),(5100,0.35,45)], attack=0.001))` — bright crackle, fast decay |
| `arcbig.voc` — the bluff zap | `concat(arc-recipe, silence(0.04), arc-recipe at 1.2× amp with partials up a fifth)` ~0.45s — same voice, raised |
| `fizzle.voc` — wrong card | `concat` of three short `partials` hits descending 1800→900→400 Hz with lengthening decay, + `noise_burst(0.25, 0.3, 14)` under — an arc giving up |
| `deal.voc` — card snap | `mix(noise_burst(0.03, 0.6, 200), partials(0.08, [(700,0.4,90)]))` — thwip + felt tap |
| `charge.voc` — coil winding up (entry/idle flourish, optional) | rising square sweep 200→1400 Hz over 0.5s (the `sfx_pickup` sweep loop, inverted and stretched) |
| `jar.voc` — the ceremonial pop | `concat(noise_burst(0.04, 0.9, 80), partials(0.3, [(1568,0.5,8),(2349,0.3,12)]))` — pop + glass ring |
| Reused | `pickup.soun` (key into pocket), `creak.soun` (card turn), `knock.soun` (NOT used here — the code is spoken; keeps the tavern door's sound signature unique) |

Room header declarations: `sound seanceSnd = "seance.soun"; sound arcSnd = "arc.soun";` etc. Music = `soun -midi`, SFX = `soun -voc` (never `-gmd`, never `-spk`).

---

## 6. Walkthrougher beats

### Canonical validate shots (append to `full-run.play.yaml`; deploy-gate)

```yaml
  # ------------------------------------- Scene 06: the reading
  - name: mind-the-cables
    do: {verb: Open, object: stage door}        # 2nd Open: silent transition
    expect:
      - talking                                 # backstage entry cutscene
      - pixel: {at: [258, 70], is: brass}       # the key, in its jar
    timeout: 90

  - name: the-parlor
    only: perform
    do: {verb: Examine, object: Madame Voltina}
    expect: [talking]

  - name: the-price
    do: {verb: Talk to, object: Madame Voltina}
    expect:
      - talking
      - speaker: voltina                        # first costumed-actor assert
      - pixel: {at: [165, 92], is: card-white}  # Card I on the felt
    timeout: 120

  - name: card-one
    do: {verb: Use, object: reading table, with: inventory.slot0}   # the notice
    expect: [talking]
    timeout: 90

  - name: card-two
    do: {verb: Use, object: reading table, with: inventory.slot2}   # the voucher
    expect: [talking]
    timeout: 90

  - name: the-truth                             # B2's dialog-click primitive
    do: {dialog: 3}
    expect:
      - talking
      - speaker: voltina
      - pixel: {at: [258, 70], is: glass-teal}  # jar EMPTY: brass gone
    timeout: 180

  - name: the-key-that-winds-itself
    do: {verb: Talk to, object: Madame Voltina}
    then: {dialog: 1}
    expect: [talking]
    timeout: 90

  - name: back-through-the-curtain
    do: {verb: Open, object: stage door}
    expect:
      - pixel: {at: [110, 12], is: sodium}      # the chandelier again
    timeout: 60
```

**Inventory-probe note:** `voltKey` is the 5th item; the 2×2 panel shows slots 0–3, so the key lands off-page. Do NOT probe an inventory slot for it — the jar-empty pixel is the pickup assertion (plus the `SNTC`/owner console oracle in validate mode). Nothing is consumed this scene, so no compaction: poster 0, magnet 1, voucher 2, pass 3, key 4.

### Streamer-mode detours and mistakes (the screenplay-schema `detour:`/`mistake:` shots)

```yaml
  - name: grabby
    mistake: {verb: Use, object: key in a jar}        # before the reading
    expect-line: "The deposit is charged. So is the jar."

  - name: wrong-past
    mistake: {verb: Use, object: reading table, with: inventory.slot1}  # magnet on Card I
    expect-line: "It fished nine bolts out of a drain. True. Not printed."

  - name: the-bluff
    mistake: {dialog: 2}                              # Card III lie -> the zap
    expect-line: "The coil bills for lies."
    hold: 2.0

  - name: ghost-light
    detour: {verb: Examine, object: ghost light}      # the clock beat
  - name: wardrobe
    detour: {verb: Examine, object: costume rack}
  - name: haircut
    detour: {verb: Examine, object: cables}
  - name: her-fuses
    detour: {verb: Examine, object: fuse box}
  - name: occupational-hazards
    detour: {verb: Talk to, object: Madame Voltina}   # hub option 3: her want
    then: {dialog: 3}
```

The mistakes are exactly the fair, reasonable wrong moves the desk catalogues: grab the visible prize, offer the wrong-but-true item, lie to the psychic. Each refusal line is the assertion; the streamer gets the gag, then finds the answer.

---

## 7. Planted/paid ledger

**Consumes (pays off):**

| Plant | Source | Paid here as |
|---|---|---|
| "Ask me sometime about the key that winds itself. Mind the cables." | theater.scc stage-door greeting | hub option 1 (Old Crank named, first time on screen — N-A10 discharged) + entry "I mind the cables." |
| "I have been expecting you, key-bearer." / "I know." | theater greeting | "The theater is wired. I am the wiring." (grounded omniscience) + Card III's truth-only design |
| "And guards… things. He doesn't say what things." | midtown clerk | the jar, visible, stenciled |
| The Order's stencil (crate, docks) | docks.scc | the jar's matching stencil — the mythology's second physical artifact |
| Rivet's "all three together could wind the city back up. Or down." | alley.scc | the motive reveal claims the "or down" plant (N-A9 closed on screen) |
| Rivet "collects municipal lies" + the notice's own LookAt | alley/docks | Card I's answer ("the lie the city printed") |
| The knock-code eavesdrop (2-1-2) | tavern rustlersTable | the FUTURE card echo; recognition branch for eavesdroppers (B9 deferral: forced echo — DONE) |
| The heist / "Everyone in this house saw a triumph." | theater.scc | entry beat: key-less arrival, goal restated (the N-A7 missing reaction completed) |
| The wind-count choice (B8) | theater stage act | "You won that at eight turns. Regulation is five." |
| Oil voucher's velvet-rope promise | inventoryitems + N-M4 bouncer | re-pointed, uncashed: "Cash it where City Hall drinks." |

**Creates (to be paid):**

| Plant | Pays off in |
|---|---|
| **Key #2 in inventory** | Scene 11 finale (one of three slots) |
| **Knock-code in every player's head** + `heardKnockCode` set globally | Scene 09: the tavern back door / hideout |
| **Rustlers' motive: ransom the rewind** | Scene 09 (the ransom plot surfaces) and the stakes of Scene 11 |
| **Old Crank: up the hill, winds himself, "ask him where the third one stands"** | Scene 10 (Old Crank IS Key #3) |
| **"Cash it where City Hall drinks. Debts talk after hours."** | Scene 07 (Oil Bar: voucher beats the rope; the aides talk) |
| **"NOTHING IS WRONG. Issued in bulk."** re-energizes the notice | Scenes 07–08 (the exposé thread; the notice frightens the aides) |
| **Voltina's want** (tomorrow negotiable again) | Scene 11 callback surface (the desk wants NPC wants to recur) |
| **The ghost light flickering** | the N-A5 detuning clock's first backstage symptom; escalates in Act 3 |
| GDD sync item: Voltina holds Key #2 *for the Order* | one GDD sentence, so the Order/Crank/Voltina triangle is arbitrable canon |

---

## 8. Embodiment audit (of this scene's own text)

Power model (canon since the physiology BLOCKER fix): **the hum winds every mainspring on the island remotely; hand-winding is the crude, off-warranty backup.**

| Claim in this scene | Audit |
|---|---|
| Voltina is cable-fed; "the brownouts ended cold reads" | Consistent: her mainspring is her *life* like everyone's; the **coil is her instrument**, and it draws more than a spring banks — hence the cables, the fuse box labeled HER, and thin arcs under brownout. The scene states the dependency through objects (cables/fuses) and one line; never contradicts the hum-winds-springs model. |
| Her knowledge of the heist/Sprocket's name | Grounded: "The theater is wired. I am the wiring." — in-building omniscience has a stated mechanism. No claim of seeing the docks. |
| Her knowledge of the magnet/drain, the notice, the wind-count | Grounded: "Answer each with what you carry. Carried things remember." — contact reads, stated ONCE, before any object is read. Every recap line reads an object physically on her felt, or an act performed inside her wired building (the eight turns). |
| The knock-code prophecy | Precognition via cards — the one supernatural power the world established for her in scene 05 ("I have been expecting you") and uses consistently. She never claims to have *heard* the Rustlers; "Their words" arrives through the reading. |
| The zap | "Small, educational" — harmless, GDD's nothing-can-kill-you law. The jar zap and the bluff zap are the same physics (charged things bite). |
| Sensory claims by Sprocket | Jar/stencil/cards: visible. Pop/hum: audible. The zap: felt. "A hum I can taste in my teeth. I don't have teeth." — the sensor-can't-parse shape, self-aware about its own body. No knock-code-from-silence class errors. |
| Prop continuity | Notice and voucher explicitly returned on screen (both are needed in scenes 07–08); the key leaves a visibly empty jar (art state 2); nothing changes mass or count; the carousel deals because she has arcs, not hands — the dealing mechanism is drawn and lampshade-free. |
| Spatial coherence | Theater's `backstageDoor` is the east wall (x288); backstage's exit is the west wall (x0) — the rooms join correctly. No line claims sight of the catwalk/hatch from backstage. |
| Art/text agreement | "It's flickering" requires the ghost light to actually flicker (object-state loop) — the brownout-NOTE lesson, pre-empted. No exact countable numbers asserted against drawn art (scorch marks "in threes" are paintable; bulb counts avoided). |
| Talk animation | Her speech IS arcing — the costume talk frames are the same phenomenon the fiction describes; voice = arc-modulated (dub chain: chorus + long echo). |

Template bans verified: zero "[material] and [abstract noun]" Smell lines (shapes used: escalating list, flat fact, sensor-can't-parse); no "destiny", no "with opinions", no "Noted. Filed.", no Sprocket act-naming, no self-grading punchlines (every punchline ends the beat; buttons tag delivery, never restate), all-caps only on diegetic signage/quotes (NOTHING IS WRONG, STAGE DOOR, HER), every Voltina line ≤12 words, multi-sentence exposition stays in Sprocket's reported register.

---

## 9. Implementation notes (the landmines, pre-cleared)

1. **Cross-room flags.** Cross-room state convention is inventory ownership (theater.sch comment). This scene needs to *read* `heardKnockCode`/`windTurns` and *write* `heardKnockCode`. Fix: **move `heardKnockCode` from `tavern.sch`'s room block to `common.sch` as a plain global bit** (like `verbsOn`), and have B8 declare `gWindTurns` as a `common.sch` global int. Five-minute change, removes all cross-unit doubt; tavern call sites are syntactically unchanged.
2. **Dub source-order.** Inside every handler, canonical-path branches first: table `UsedWith` = Card-I-notice block, then Card-II-voucher block, then all wrong-item branches; Card III climax puts the `heardKnockCode` *recognition* line first (the eavesdrop is on the validate path per the B9 disposition).
3. **Silent transitions.** Both door verbs that transition say nothing; all arrival flavor lives in `BackstageRoom.entry`. The theater door's greeting cutscene does NOT transition (shipped behavior kept); the post-greeting click does, silently.
4. **actorSay not-in-room landmine.** `putActorAt(voltina_a, …)` in BOTH the theater greeting (parked at the door text position) and every backstage entry, before any line.
5. **Flags before speech** — `readingStage`, `metVoltina`, `gHeardKnockCode` set at branch tops, never mid-cutscene.
6. **Ghost-light flicker** uses the `signFlicker` pattern — remember the stopScript-on-exit bug class.
7. **New verb ids:** none — all shared verbs already pinned in `common.sch`.
8. **Pipeline touch list:** `backstage.scc/.sch`, `common.sch` (voltina actor decl + VOLTINA_COLOR + globals), `actors.scc` (talk color), `inventoryitems.scc/.sch` (`voltKey`), `theater.scc` (door edit + greeting conversion), `genassets.py` (`BACK_GEOM`, `draw_backstage`, card/jar states, voltina costume frames, talk-color probe + collision assert, stage-map emit), `genmusic.py` (`seance`), `genaudio.py` (5 SFX), `game/Makefile` (voltina.scost), `dub.py` CAST (kristin + chorus/echo/lowpass-5000), `full-run.play.yaml` + streamer screenplay, then the editorial desk before validate — no scene ships with open BLOCKERs.