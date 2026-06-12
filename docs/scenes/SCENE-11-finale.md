I've read the full required stack — production plan, GDD, NOTES, charter + all three editorial reports, NPC-DIALOG, genmusic/genaudio, the walkthrougher doc, and tavern/theater/midtown sources plus all headers. Here is the complete design doc.

---

# SCENE 11 — THE FINALE: REWIND THE DYNAMO
*Design doc, 2026-06-12. Builds from: `docs/GDD.md` Act 3, `docs/PRODUCTION-PLAN.md` row 11, the editorial charter and all 2026-06-12 reports, `docs/research/NPC-DIALOG.md`. Voice models: `game/tavern.scc`, `game/theater.scc`. Target file: `game/dynamo.scc` + finale branches in all five existing rooms.*

---

## 0. Interfaces & assumptions (scenes 06, 09, 10 are designed in parallel)

This scene consumes the following contracts. If a sibling design changes one, this doc must be re-reconciled:

| From | Contract |
|---|---|
| Scene 06 | `InventoryItems::voltinaKey` (Key #2) exists, owner `VAR_EGO` at finale start. Voltina has delivered the "key that winds itself" fortune on the critical path (her greeting already plants it in `theater.scc:backstageDoor`). The knock-code forced echo happened (desk disposition, pass 2). |
| Scene 07/08 | One piece of official paper survives to the finale — `InventoryItems::poster` (the official notice) is presented at City Hall in `midtown.scc` but never consumed. **Scenes 07–08 must not consume it**, or must leave an equivalent official-paper item; the banner beat (§4.5) takes it as a *show*, not a *give* (not consumed here either — it gets one last laugh in the credits). |
| Scene 09 | `windupKey` (Key #1) recovered: owner `VAR_EGO`. Act flag `actNumber = 3` set at hideout entry. The Rustlers escaped the hideout raid at large (this scene cashes them). The hideout stands open and empty afterward. |
| Scene 10 | Room `DynamoRoom` exists, entered from Midtown (the fence object in `midtown.scc:dynamo` opens). Old Crank is a **costumed actor** (`oldCrank`, talk color per NPC-DIALOG palette plan) present in DynamoRoom, revealed as Key #3. Scene 10 ends with the player standing in DynamoRoom, fence open, all three keys accounted for. Scene 10's DynamoRoom geometry should match or supersede §3 below — whichever lands first owns `GEOM["DYNAMO_*"]`; the object *names and states* in §3 are this scene's hard requirement. |
| B2+B8 | The dialog-tree UI (`game/dialog.scc`) is wired and the walkthrougher can click dialog options. The talent-show wind-count choice shipped — the finale's wind-count choice is its designed rhyme and **reuses the same UI**. |
| NPC-DIALOG | Tier-A actors + per-NPC talk colors + speaker-attributed dub are landed through at least rank 4 (slot-eye, heckler, Rivet). This scene adds three speakers: `aide`, `rustlerLeader`, `mayorPiston` (Tier-A, costume-less) and gives lines to `gusket`, `rivet`, `slotEye`, `oldCrank`. |

**New global state** (in `game/common.sch`, alongside the existing file-scope `bit verbsOn,cursorOn,...` globals — that precedent says cross-unit globals link by name; **verify with a 2-minute two-unit test before building on it**, and if sld disagrees, fall back to the repo's documented idiom: sentinel objects in `InventoryItems` whose owner encodes the bit, `0x0F`=unset / `0`=set):

```c
// finale state (scene 11)
bit finaleKey1, finaleKey2, finaleKey3;   // keys seated
bit loadMarqueeOff, loadBannerOff, loadAmpOff;
bit blackoutDone;                          // all three loads off, walked back
bit cityRewound;                           // five turns landed
int actNumber;                             // 1/2/3 — the detuning hum clock (N-A5)
```

`actNumber` is set: `1` at boot (common.scc init), `2` in the funicular fare cutscene (`alley.scc:gate`), `3` at hideout entry (scene 09). The finale's own phases ride the bits above, not actNumber.

---

## 1. Scene goal + the three-keys spine

**Goal.** The player rewinds the Great Dynamo. To do it they must: seat all three Keys of Clankey Island in the winding head (the act that *primes* the mainspring also *powers down the city*, tier by tier, on a schedule the Order wrote sixty years ago); walk back down through their own darkened game and switch off the three loads somebody wired around the meter — a marquee with the player's name on it, City Hall's NOTHING IS WRONG banner, and the Scrap & Barrel's ampersand; survive one last Rustler shakedown that defeats itself; and then perform the final action of the game with their own hands: wind the pilot spring **exactly five turns**. Regulation. The number the game has been teaching since the talent show.

**How it advances (completes) the spine.** The three keys arrive with three relationships: Key #1 was *earned* (Act 1), *lost to showboating* (Act 2), and *taken back* (Act 3). Key #2 was *guarded and granted* (Voltina). Key #3 is *given* — it's a person's, and he gives it knowing he winds down without it. Each seating beat narrates its key's history in one sentence, so the spine is audible in the finale rather than assumed. The thematic resolution: the game opens with Sprocket too small for his wrench and ends with him turning a crank sized for a bot two sizes up — and winning not by over-winding (showbiz) but by reading the plate (maintenance). The Dynamo's first act when it wakes is to wind Old Crank's surrendered key — *the key that winds itself* — paying Voltina's fortune, the piano's "missing entirely" motif, and the title of the island in one image.

**The detuning hum's payoff.** The whole game has been drifting flat by act (§5). The finale plays the drift's terminal stage (every theme in its `_dying` variant), then the first true silence in the game (the blackout), then the only rising pitch in the score (the rewind cue ramps −160¢ → 0), and the credits play the first *in-tune* music the game has ever produced. The clock the GDD designed finally rings.

**Antagonist resolution.** The Rustlers' motive (GDD, per N-A9: *they mean to ransom the rewind*) gets its comeuppance by inversion: they climb uptown to renegotiate, spend their corroded springs' last charge on the climb, and freeze mid-threat; when the hum returns it rewinds them too — into Mayor Piston's itemized bill for "rewinding services, one city, payable in washers." A city that can be wound down can be billed for winding back up. They got one.

---

## 2. The puzzle chain

Numbered graph. `→` = hard dependency. All of it happens after scene 10's reveal; nothing here requires an item the critical path hasn't already banked.

```
            [P1: seat Key #1]──┐
            [P2: seat Key #2]──┼──→ [P3: Old Crank gives & seats Key #3]
       (P1,P2 any order;       │         (gated on P1 AND P2)
        leaving the room       │
        between seats is       ▼
        refused by Crank)   city dark except THREE LOADS
                               │
                ┌──────────────┼────────────────┐
                ▼              ▼                ▼
        [P4: marquee off] [P5: banner off] [P6: ampersand off]
         (Midtown, Use)   (Midtown, show    (Tavern, Gusket
                           official notice)  throws it himself)
                └──────── any order ─────────┘
                               │ all three
                               ▼
              [P7: blackout cutscene, walk back up]
                               │
                               ▼
              [P8: Rustler ambush self-defeats]   (cutscene, opposition beat)
                               │
                               ▼
              [P9: THE WIND — dialog choice, 3 options]
                    2 turns → flop (retry)
                    8 turns → flop, the fair mistake (retry)
                    5 turns → THE REWIND → ending → credits → stinger
```

### Fair-play audit — every hint, source named

| Needed knowledge | Sources (on-screen, before needed) | Forced? |
|---|---|---|
| The Dynamo takes three keys in three slots | Rivet's free facts, Act 1 critical path ("three wind-up keys... could wind the city back up"); `midtown.scc:dynamo:UsedWith` — "One key, three slots... Even the fence can do that math" (the N-M6 confirming refusal); `keySlots:LookAt` here ("The fence's math, in brass") | Yes (Rivet) |
| Keys seat in the winding head | The slots are the only key-shaped thing in the room; LookAt names them; Crank's coaching line ("Three keys. Three slots.") | Yes (Crank TalkTo on entry path) |
| Crank's key goes last | Crank says it directly, first coaching exchange | Yes |
| The city must reach zero load before hand-start | Crank states it the moment the three lights appear ("She can't be hand-started under load. Go turn off the city, boy."); `pilotCrank` refusal restates it state-aware if tried early | Yes |
| Which three loads | Crank names them ("A marquee. A banner. One ampersand."); each is the only lit object in its darkened room — the screen itself signposts (no pixel hunt possible: the target is the only bright thing) | Yes |
| The banner needs paperwork | Established at `midtown.scc:cityHall:UsedWith` (Act 2: the aide fears the official notice, calls it "official and correct"); the aide's finale refusal line states the want ("Turning them off is a statement.") before the player must answer it | Refusal-then-key, classic shape |
| The ampersand is Gusket's to throw | His direct line states the want; the resolution is dialog, not an item — TalkTo and Use both route to it (no verb roulette, per B5) | Yes |
| **FIVE turns** | Four sources, escalating: (1) `theater.scc` stage cutscene, Act 2 critical path — "Regulation maximum is five"; (2) `ratingPlate:LookAt` — "WIND TO FIVE. FIVE MEANS FIVE."; (3) Old Crank, forced, seconds before he stops — "Five turns on the pilot when you're back. Five means five."; (4) Sprocket's own self-wind rehearsal beat — "Five turns. Regulation."; plus the flop branches each repeat the hint. A finale must be over-determined; nobody stalls on the last click of the game. | Yes ×2 |
| The Rustlers are coming | Alley finale entry, forced: "The hideout door is open. Nobody home. Three corroded somebodies are out in this, somewhere, climbing." | Yes |

No lock names its key verbatim except where a refusal earns it (N-A2 discipline: the plate is diegetic signage, sanctioned; Crank's instruction is a character with a reason to instruct).

### The playable-agency beats (charter: THE CONTESTS MUST BE PLAYABLE)

1. **The wind-count (P9)** is the centerpiece: a real dialog-tree choice with two funny failures and a winner, the structural rhyme of the B8 talent-show choice — and a *reversal* of it. The game taught "over-winding wins" on stage; the player who applies that lesson gets launched across the platform (the designed fair mistake, streamer-mode gold), and the regulation line the show treated as a dare turns out to be the actual spec. Failures are free retries; the choice re-offers.
2. **The blackout run (P4–P6)** is free-roam: three switches, any order, three different interaction shapes (a bare Use, an item show, a negotiated handoff), each with its own beat. The player authors the order the city's last lights die in.
3. **Seating order of Keys #1/#2** is the player's (cosmetic agency; both orders fully voiced — the seat lines are per-key, not per-slot).

Failure-state inventory: none lethal, none stuck. Early crank → state-aware refusal that names remaining loads. Leaving DynamoRoom mid-seating → Crank's refusal ("Seat them all or seat none. She doesn't like half measures."). All three flop/refusal lines double as escalating hints.

---

## 3. Object table & geometry

Stage is 320×144 playfield (verb panel below). New room first, then per-room finale deltas.

### 3.1 `DynamoRoom` (new; coordinate sketch)

```
0        40        80       120      160      200      240      280     320
+--------+---------+--------+--------+--------+--------+--------+--------+ 0
| night sky          ┌──────────────────────────────┐   flywheel arc     |
| GATE  ┌─────────┐  │     DYNAMO CORE (dome,       │                    | 24
| (exit)│ CITY    │  │     slow glow pulse —        │    ╔══════╗        |
|  ▒▒   │ VISTA   │  │     the room's animating     │    ║ OLD  ║        | 48
|  ▒▒   │ (railed │  │     element per GDD)         │    ║CRANK ║        |
|  ▒▒   │overlook)│  └──┬───────────────────────┬───┘    ╚══════╝        | 72
| rustlers appear  [PILOT][ KEY SLOTS x3 ][PLATE]                        | 96
|  here (states)   [CRANK]                                               |
+---------------------- platform planks / walkbox ----------------------+ 144
```

| Object | Rect (x,y,w,h) | Verbs handled | States |
|---|---|---|---|
| `gateBack` | 0,56,24,48 | LookAt, Open/Use (silent exit → MidtownRoom) | 1 |
| `cityVista` | 28,20,64,52 | LookAt, Smell, Use | **6**: 1 all-lit · 2 docks-dark · 3 midtown-dark · 4 three-lights · 5 black · 6 relit-bright |
| `dynamoCore` | 104,4,120,72 | LookAt, Smell, TalkTo, UsedWith (keys → pointer to slots) | 3: straining(2-frame glow pulse loop, `signFlicker` pattern — **mind the stopScript bug class**) · still · rewound-glow |
| `keySlots` | 128,76,56,20 | LookAt, Use/Give/UsedWith (keys) | 4: empty · one · two · three keys (key #3 drawn turning in state 4 + `cityRewound`) |
| `ratingPlate` | 190,80,14,10 | LookAt, Smell | 1 |
| `pilotCrank` | 104,88,20,18 | LookAt, Use, Move, Smell | 2: idle · spun |
| `oldCrank` (costumed actor; clickable via `actorObject[]` routing) | stands ≈(250,108) | LookAt, TalkTo, Give/UsedWith, Smell | actor anim: standing · stopped-mid-word (frame freeze) |
| `rustlers` | 4,60,44,52 | LookAt, TalkTo, Smell, PickUp (hat gag) | 3: hidden · looming · statues-with-hats |

Walkbox: platform strip y≈100–136, full width; vista rail blocks y<100 on the left.

### 3.2 Finale deltas to existing rooms

Every revisited room gains: (a) a **dark background state** — a full-stage object `roomDark` (0,0,320,144), state 1 = lit bitmap matching the background, state 2 = the dark repaint (the proven curtain/marquee state-swap mechanism at room scale; ~45KB ×2 per room, acceptable); (b) **finale entry branch** gated on `finaleKey3` with a room-local `bit finaleSeen<Room>`; (c) **finale-first source ordering** in every touched handler (dub pairing).

| Room | Object | Change |
|---|---|---|
| Midtown | `theater` (marquee) | new state 3: marquee dark. Finale LookAt + Use (the breaker beat, P4). |
| Midtown | `cityHall` | new states: banner-lit-floodlit (only light in room) · banner-dark · **banner-NOTHING-WAS-WRONG** (ending). Finale Open/Use = the aide beat (P5); UsedWith poster routes to same beat. |
| Midtown | `station` | finale LookAt (stairs gag); Use = silent transition as ever. |
| Midtown | `boxOffice`, `oilBar`, `leftys`, `dynamo` | one finale line each (flavor tier, see §4.9 cut-list). |
| Alley | `gate` | new state: display-dim. Finale flavor in entry narration (the FREE gag — **not** on the transition verb). |
| Alley | `rivet` | finale TalkTo (the bolt inversion). |
| Alley | `hideoutDoor`, `dumpster`, `graffiti`, `fireEscape` | finale flavor lines (P2 tier). |
| Docks | `neonSign` | already has on/off; **new third art state in genassets: `POP. 8,011`** (the stinger; pays the embodiment desk's deferred sign fix). |
| Docks | `betty`(stall/crane), `ferry`, `drain`, `tavernDoor` | finale flavor lines. |
| Tavern | `barSign` | new states: **ampersand-only-lit** · dark. Use = breaker beat (P6). |
| Tavern | `gusket` | finale TalkTo (routes to same beat as barSign Use — no verb roulette). |
| Tavern | `piano`, `flange`, `rustlersTable`, `doorBack` | finale flavor lines; `doorBack` gets the slot-eye's last word. |

New inventory: `InventoryItems::crankKey` exists only inside the P3 cutscene (Crank seats it himself — it never enters the player's pockets; zero inventory churn). The `bolt` object is re-acquired in the Rivet beat (owner 0 → `pickupObject` again, legal per the owner rules in NOTES).

---

## 4. Full dialog draft

Register rules observed throughout: Sprocket narrates, reported speech default; NPC direct punchlines ≤12 words where they earn the card; no double-telling; no smell zeugma template; no self-grading; meta stays NPC-only (the slot-eye keeps the monopoly); caps only in signage and NPC mouths; **walkthrough-path branches first in source in every handler**; story flags set at the top of branches, before speech; room transitions say nothing.

### 4.1 DynamoRoom — standing hotspots (pre-seating)

```c
// dynamoCore
case LookAt:
    egoSay("The Great Dynamo, from inside the fence. It's bigger than the fence implied. Most things are smaller.");
    waitForMessage();
    egoSay("Up here the hum isn't background. It's a pulse, and it's behind on the beat.");
    return;
case TalkTo:
    egoSay("Hang in there, big fella. Help is here. Help brought keys.");
    return;
case Smell:
    egoSay("Ozone, at the source.");
    return;
case UsedWith:   // any key on the dome itself
    egoSay("Not the dome. The winding head. Even I can do that math now.");
    return;

// keySlots
case LookAt:    // state-aware, walkthrough branch first
    if (finaleKey3) { egoSay("Three keys, home. The third one is the warm one."); return; }
    if (finaleKey2 && finaleKey1) { egoSay("Two seated, one slot waiting. It's not waiting for a key. It's waiting for a hermit."); return; }
    if (finaleKey1 || finaleKey2) { egoSay("One in, two to go. The head creaks like it remembers the procedure."); return; }
    egoSay("Three slots in the winding head, key-shaped, forearm-sized. The fence's math, in brass.");
    return;
case Smell:
    egoSay("Brass. Recently disturbed.");
    return;

// ratingPlate
case LookAt:
    egoSay("A brass plate, thumb-polished: PILOT SPRING. WIND TO FIVE.");
    waitForMessage();
    egoSay("Underneath, smaller: FIVE MEANS FIVE.");
    return;
case Smell:
    egoSay("Sixty years of one thumb.");
    return;

// pilotCrank (pre-blackout refusal — state-aware hint, fair-play)
case LookAt:
    egoSay("A hand-crank, sized for a bot two sizes up from me. The crude backup. The manual of last resort.");
    return;
case Use:
case Move:
    unless (blackoutDone) {
        egoSay("It won't catch under load. Something down there is still drawing.");
        waitForMessage();
        unless (finaleKey3) { egoSay("And the keys go in first. Even crude backups have an order of operations."); return; }
        egoSay("Three lights say not yet.");
        return;
    }
    // → the wind-count dialog, §4.7
case Smell:
    egoSay("Grease applied by somebody who believed in grease.");
    return;

// cityVista
case LookAt:    // state-aware; pre-seating:
    egoSay("The whole city from above: docks, Midtown, the harbor. Every light down there runs off the spring I'm standing on.");
    return;
    // states 2/3/4/5 versions appear inside the seating cutscenes below;
    // standalone re-LookAts:
    //  state 2: "The docks are out. The tavern sign with them. Gusket is polishing in the dark."
    //  state 3: "Midtown's gone too. From up here the island is three lights and a memory."
    //  state 5: "Nothing. The first city-shaped silence in sixty years."
    //  state 6: "Every light, back, and brighter. The hum under them is in tune. I checked twice."
case Smell:
    egoSay("Wind. It's been everywhere down there and won't say.");
    return;

// gateBack — leaving mid-seating (soft gate)
case Open: case Use:
    if (finaleKey1 || finaleKey2) { unless (finaleKey3) {
        actorSay(oldCrank, "Seat them all or seat none. She doesn't like half measures.");
        egoSay("I wasn't going to leave. I was stretching. Toward the gate.");
        return;
    }}
    // otherwise: silent transition to MidtownRoom
```

### 4.2 Old Crank — coaching (TalkTo, pre-seating)

```c
unless (metCrankFinale) {
    metCrankFinale = 1;                      // flag before speech
    cutscene(0) {
        actorSay(oldCrank, "Three keys. Three slots. Any order, except mine goes last.");
        egoSay("I ask why his goes last.");
        actorSay(oldCrank, "Because I'm in no hurry to stop talking.");
    }
    return;
}
unless (finaleKey1 && finaleKey2) { actorSay(oldCrank, "Two keys, boy. Brass before flesh."); return; }
// (finaleKey1 && finaleKey2 && !finaleKey3) → routes to the P3 cutscene, §4.3
```

### 4.3 Seating the keys (P1, P2, P3)

`Use`/`Give`/`UsedWith` key on `keySlots` (both keys aliased; Give = UsedWith per B5 discipline).

**Key #1:**
```c
finaleKey1 = 1;  setObjectOwner(InventoryItems::windupKey, 0);
cutscene(0) {
    startSound(keyseatSnd);  setObjectState(keySlots, /*+1 key*/);
    egoSay("Key number one. It went up a crane, onto a marquee, through a hatch, and into a card game. It seats like none of that happened.");
    waitForMessage();
    startSound(powerdownSnd);  setObjectState(cityVista, 2);
    egoSay("Down at the harbor, the hum pulls back. Pier by pier, the docks go out.");
    waitForMessage();
    actorSay(oldCrank, "Dockside sleeps first. Dockside wakes first. We planned it that way.");
    egoSay("Somebody scheduled this blackout sixty years ago. It starts on time.");
    waitForMessage();
}
```

**Key #2:**
```c
finaleKey2 = 1;  setObjectOwner(InventoryItems::voltinaKey, 0);
cutscene(0) {
    startSound(keyseatSnd);  setObjectState(keySlots, /*+1 key*/);
    egoSay("Key number two. Voltina kept it sixty years and dusted it daily. It seats like it's coming home.");
    waitForMessage();
    startSound(powerdownSnd);  setObjectState(cityVista, 3);
    egoSay("Midtown goes next. The neon dies mid-flicker. The manholes stop hissing.");
    waitForMessage();
    actorSay(oldCrank, "Two in. The spring's drinking it all back now.");
    // DynamoRoom music steps down one hum variant here (see §5)
}
```

**Key #3 — Old Crank** (TalkTo Crank with both seated; also fires if the player uses *him* on the slots, which deserves the same scene):
```c
finaleKey3 = 1;
cutscene(0) {
    egoSay("I ask if he's sure.");
    actorSay(oldCrank, "It's a key. I've just been holding it the long way.");
    startSound(ratchetSnd);
    egoSay("He draws his own key out of his own back, walks to the head, and seats it himself. Third slot.");
    waitForMessage();
    startSound(keyseatSnd);  setObjectState(keySlots, 4);
    egoSay("It fits the way facts fit.");
    waitForMessage();
    startSound(powerdownSnd);  setObjectState(cityVista, 4);
    egoSay("The rest of the island lets go, from the water up.");
    waitForMessage();
    egoSay("Except. Three lights.");
    waitForMessage();
    actorSay(oldCrank, "Three taps somebody wired around the meter.");
    actorSay(oldCrank, "A marquee. A banner. One ampersand.");
    egoSay("He says it like a grocery list he's been keeping for years.");
    waitForMessage();
    actorSay(oldCrank, "She can't be hand-started under load. Go turn off the city, boy.");
    waitForMessage();
    actorSay(oldCrank, "Five turns on the pilot when you're back. Five means five.");
    egoSay("The plate says the same thing. They proofread each other.");
    waitForMessage();
    actorSay(oldCrank, "I'll mind the spring. Wake me when—");
    startSound(winddownSnd);
    egoSay("He doesn't finish. The spring he's held for sixty years finally gets to rest. He stops standing up, mid-word, like punctuation.");
    waitForMessage();
    // Sprocket's self-wind — the rehearsal beat
    startSound(ratchetSnd);
    egoSay("Before the stairs, I wind myself. By hand. The crude way.");
    waitForMessage();
    egoSay("Five turns. Regulation. Tonight I'm a professional.");
    waitForMessage();
}
```
Post-P3 `oldCrank:LookAt`: `"Old Crank, stopped mid-word. Holding his place in the sentence."` `TalkTo`: `"Nothing. He's keeping the rest of that sentence somewhere safe."`

### 4.4 Midtown, dark (entry + the marquee, P4)

Entry (finale branch first in source):
```c
egoSay("Midtown, dark. The only lights left are a marquee with my name on it and a banner with the city's excuse on it.");
waitForMessage();
egoSay("My eyes turn out to be the third. Standard equipment. Never needed it before.");
```

`theater` (marquee), finale branches:
```c
case LookAt:
    if (loadMarqueeOff) { egoSay("Dark, like the rest of the street. The street looks right."); return; }
    egoSay("SPROCKET, in lights, on a dead street. The bulbs are burning the city's last banked charge to spell my name.");
    waitForMessage();
    egoSay("Advertising already cost me a key. Tonight it's just expensive.");
    return;
case Open: case Use:
    unless (loadMarqueeOff) {
        loadMarqueeOff = 1;
        cutscene(0) {
            egoSay("My name, in lights, drawing the island's last charge. There's a switch for that.");
            waitForMessage();
            startSound(breakerSnd);  setObjectState(theater, 3);
            egoSay("CHUNK. The marquee goes dark, name and all.");
            waitForMessage();
            egoSay("The street forgets me instantly. Showbiz.");
            waitForMessage();
        }
        return;
    }
    egoSay("Locked and dark. Even the ghost light went home.");
    return;
```

`station`, finale `LookAt`: `"Dead on its rope. Beside it, a door I never needed: MAINTENANCE STAIRS."` → `"The fare was for not taking them."` (Use stays a silent transition.)

### 4.5 Midtown — the banner & the aide (P5)

`cityHall`, finale `Open`/`Use`/`UsedWith(poster)` all route here:
```c
unless (loadBannerOff) {
    loadBannerOff_pending...   // set loadBannerOff=1 at top of the success path
    cutscene(0) {
        egoSay("The aide's eye is in the door gap before I knock. Insomnia is a civic duty tonight.");
        waitForMessage();
        actorSay(aide, "The floodlights stay. Turning them off is a statement.");
        // success requires the official notice in pocket; walkthrough path first:
        egoSay("I show him the official notice. City letterhead. The Dynamo, in writing.");
        waitForMessage();
        actorSay(aide, "...This is official. And correct.");
        egoSay("He files it through the gap. Paper beats floodlight.");
        waitForMessage();
        startSound(breakerSnd);  // banner dark state
        actorSay(aide, "The banner is not off. It is pending.");
        egoSay("The door closes the full nine degrees. A first.");
        waitForMessage();
    }
    return;
}
egoSay("PENDING, as filed.");
return;
// no-poster branch (after, in source): the aide holds:
//   actorSay(aide, "No paper, no statement.");
//   egoSay("Bureaucracy survives the apocalypse. It IS the apocalypse's paperwork.");
//   (hint: the player has carried the notice since Act 1; if scenes 07-08
//    consumed it, THEY must hand back an official substitute — interface §0)
```
Finale `cityHall:LookAt` (pre-switch): `"NOTHING IS WRONG, floodlit, over a city with no other lights on."` → `"It's also the only thing left that's wrong."`

### 4.6 Alley & Docks, dark (transit beats) and the tavern (P6)

**Alley entry** (finale, forced):
```c
egoSay("The alley, by eye-light. The graffiti reads differently in the dark. It reads like it was right.");
waitForMessage();
egoSay("As I pass the fare gate, it spends its last pixel on one word: FREE.");
waitForMessage();
egoSay("The hideout door is open. Nobody home. Three corroded somebodies are out in this, somewhere, climbing.");
```

**Rivet, finale TalkTo:**
```c
cutscene(0) {
    egoSay("Rivet, open for business in a city with no customers. His lamp is off. He knows to the minute how much dark he can afford.");
    waitForMessage();
    actorSay(rivet, "Quiet night. Inventory: one fact, no buyers.");
    egoSay("Then he holds out a bolt. His own.");
    waitForMessage();
    actorSay(rivet, "Buying, not selling. Tell me the city comes back.");
    egoSay("I tell him it does. Five turns and a sunrise.");
    waitForMessage();
    startSound(clinkSnd);  pickupObject(InventoryItems::bolt, InventoryItems);
    egoSay("He pays the bolt without a word.");
    waitForMessage();
}
// repeat TalkTo: actorSay(rivet, "Sunrise, you said. I'm holding you to the invoice.");
```

**Docks entry** (finale): `"The docks, dark. The water's still there. Water doesn't run on anything."` → `"The S.S. Eventually sits exactly where it always sits. Consistency is its best feature."`
Flavor (P2 tier): Betty LookAt `"Boom-Arm Betty, parked mid-gesture. Cranes bank deep. She'll sleep through the whole night and lift something at dawn."`; Betty TalkTo `"I tap G-N on her hull. Two letters. She bills by the letter; she'd approve."`; neonSign LookAt `"The WELCOME sign, off. POP. 8,01,1, unreadable — its most accurate state yet."`

**Tavern entry** (finale):
```c
egoSay("The Scrap & Barrel, lit by one ampersand.");
waitForMessage();
egoSay("The piano is winding down mid-rag. Nobody is feeding it. It plays like it knows.");
// rag_dying is a ONE-SHOT here: the musicLoop watchdog must NOT restart it.
// The piano dying mid-bar IS the scene's score.
```

**The ampersand (P6)** — `barSign:Use` and `gusket:TalkTo` both route here (no verb roulette):
```c
unless (loadAmpOff) {
    cutscene(0) {
        egoSay("I explain about the meter, the pilot spring, and the ampersand.");
        waitForMessage();
        actorSay(gusket, "That sign's been lit since my first night.");
        egoSay("I tell him the Dynamo can't restart while it burns. That tonight, dark is what open looks like.");
        waitForMessage();
        actorSay(gusket, "One condition. I throw the switch.");
        egoSay("Fair. It's his bar.");
        waitForMessage();
        loadAmpOff = 1;                       // flag before the lights change
        startSound(breakerSnd);               // sign dark; if marquee+banner also
        actorSay(gusket, "We're not closed. We're holding our breath.");
        egoSay("The last light on the island goes out. His bar. His hand.");
        waitForMessage();
        // → if all three loads now off: the blackout cutscene chains here
    }
    return;
}
```
*(If the player does the ampersand before Midtown's loads, the same scene plays minus "the last light" — branch that one line: `"One light down. Two burning, uptown."`)*

**Blackout + walk back (P7)** — chains from whichever switch was third, in that room:
```c
blackoutDone = 1;                              // before speech
cutscene(2) {
    // roomDark full state; stopMusic(); true silence; startSound(humstopSnd)
    egoSay("The island holds still. Somewhere uptown, a spring the size of a building is waiting on five turns.");
    waitForMessage();
    egoSay("The walk back up is the darkest walk anyone has ever taken. I navigate by handrails and memory.");
    waitForMessage();
    putActorAt(VAR_EGO, 40, 120, DynamoRoom);
    startRoom(DynamoRoom);                     // transition itself: silent
}
```

Streamer-tier flavor (P2): `doorBack:Use` in blackout — `egoSay("CLANG-CLANG. CLANG. CLANG-CLANG.")` / `egoSay("The slot opens. Slower than usual. The eye is down to a pilot light.")` / `actorSay(slotEye, "Last act, buddy.")` / `egoSay("The slot closes.")`. `flange:LookAt`: `"Flange, parked mid-anecdote. The wall finally gets a word in."` `rustlersTable:LookAt`: `"The card table, empty. Washers still on it. Wherever they went, they expect to be back."` `piano:LookAt` (after it stops): `"It ran out mid-rag. The first silence this room has ever had. It suits nobody."` `oilBar:UsedWith(oilVoucher)` (Midtown detour): `"The rope is still up. The bouncer isn't. I step over the rope. Twice. For the principle."`

### 4.7 Return, ambush (P8), and the wind (P9)

**DynamoRoom finale-return entry:**
```c
egoSay("Back at the top. Old Crank is exactly where he stopped. The hum is so low now it's less a sound than a habit.");
waitForMessage();
startSound(knockSnd);
egoSay("From the gate behind me: CLANG-CLANG. CLANG. CLANG-CLANG. Old habits.");
waitForMessage();
setObjectState(rustlers, 2);   // looming
egoSay("Three silhouettes, salt-stiff and slow. They climbed all the way up here on banked charge to renegotiate.");
waitForMessage();
actorSay(rustlerLeader, "Nice city. Shame if nobody wound it.");
egoSay("I point at the city. It is currently off. He had a speech ready for a different island.");
waitForMessage();
actorSay(rustlerLeader, "The price just went up. Hand over the—");
startSound(winddownSnd);
egoSay("He doesn't finish the noun. Salt corrosion spends spring charge like a sailor, and the climb was the whole budget.");
waitForMessage();
startSound(winddownSnd);  startSound(winddownSnd);  setObjectState(rustlers, 3);
egoSay("His crew follows, mid-menace. Three statues with hats.");
waitForMessage();
```
Statue hotspots (flavor): LookAt `"Three statues with hats. The hats survived."`; PickUp `"Tempting. But when he reboots, I want him to know nothing here was worth stealing."`; Smell `"Salt. The sea sent representatives."`

**The wind (pilotCrank:Use, blackoutDone)** — dialog-tree UI, three options:

> **1. "Two turns. Ease her in."**
> ```
> startSound(ratchetSnd) ×2
> egoSay("Two turns. The pilot spring clears its throat and goes back to sleep.");
> egoSay("The plate said five. The plate has been right longer than I've been assembled.");
> ```
> **2. "Eight turns. It worked on stage."**  *(the designed fair mistake)*
> ```
> startSound(ratchetSnd) ×8 accelerating; startSound(boingSnd);
> putActorAt(VAR_EGO, 60, 116, DynamoRoom);   // tossed across the platform
> egoSay("Eight turns. The crank disagrees, formally.");
> egoSay("I land where I was always going to land. The crank resets itself with what I can only call contempt.");
> egoSay("Five, the plate says. Five, the hermit said. Fine.");
> ```
> **3. "Five turns. Regulation."** → §4.8.

Both flops return to the room; the choice re-offers on the next Use.

### 4.8 The rewind, the ending

```c
cityRewound = 1;                                // before speech
cutscene(2) {
    stopMusic();  startMusic(rewindSnd);        // ONE-SHOT: no imPlayerSetLoop
    startSound(ratchetSnd);
    egoSay("Five turns, counted out loud, witnessed by statues.");
    waitForMessage();
    egoSay("The pilot catches. Deep in the casing, the escapement picks up the beat it lost.");
    waitForMessage();
    egoSay("The hum comes back the way the tide comes in. Under everything, then everywhere.");
    waitForMessage();
    setObjectState(cityVista, 6);  setObjectState(dynamoCore, 3);  startSound(clinkSnd);
    egoSay("The docks light first. Pier by pier. As scheduled, sixty years ago.");
    waitForMessage();
    egoSay("Then Midtown. The neon, the manholes, the gate. Somewhere down there it's already counting.");
    waitForMessage();
    startSound(ratchetSnd);
    egoSay("In the third slot, Old Crank's key begins to turn. By itself. Wound by the machine it's winding.");
    waitForMessage();
    egoSay("The key that winds itself. The fortune was a spoiler.");
    waitForMessage();
    actorSay(oldCrank, "—it's over.");
    egoSay("He finishes the sentence from before. As far as he's concerned, nothing in between bothered to happen.");
    waitForMessage();
    actorSay(oldCrank, "Five turns?");
    egoSay("Five.");
    waitForMessage();
    actorSay(oldCrank, "Regulation bot.");
    waitForMessage();
    startSound(ratchetSnd);  setObjectState(rustlers, 2);
    egoSay("Behind us, the Rustlers reboot mid-shakedown.");
    waitForMessage();
    actorSay(rustlerLeader, "—keys! Hand over the keys!");
    egoSay("The keys are in the Dynamo, the Dynamo is winding their mainsprings, and the Mayor is coming up the hill with paperwork.");
    waitForMessage();
    egoSay("Mayor Piston, at velocity, trailing steam and one aide with a clipboard.");
    waitForMessage();
    actorSay(mayorPiston, "City Hall is pleased to report the scheduled maintenance concluded on schedule.");
    egoSay("Nothing was scheduled. It is now. Retroactively.");
    waitForMessage();
    egoSay("Then he turns to the Rustlers and presents the bill.");
    waitForMessage();
    actorSay(mayorPiston, "Itemized. Rewinding services, one city. Payable in washers.");
    egoSay("The aide staples it to the leader's hat.");
    waitForMessage();
    egoSay("Behind them, City Hall's floodlights come back on. The banner is new. NOTHING WAS WRONG.");
    waitForMessage();
    actorSay(oldCrank, "You'll stay for sunrise.");
    egoSay("Not a question. We watch the city relearn its racket. The piano downstairs is back to missing every third note.");
    waitForMessage();
    egoSay("Three days ago I got off a boat with a dream and no oil can.");
    waitForMessage();
    egoSay("Somewhere below, a sign flickers back on, comma and all. I'll fix it tomorrow. I live here now.");
    waitForMessage();
    // → fade → credits
}
```

### 4.9 Credits + stinger

Credits as in-game text cards over the relit vista (or render.py chapter cards in the film — both), styled as a maintenance work order. Music: **the Clanker City Shuffle at 0 cents** — the first in-tune music in the game.

```
CLANKER CITY CHRONICLES
WORK ORDER #8,011 — CLOSED

Parts used: 11 bolts (1 returned), 1 magnet, 1 string,
            1 oil can, 3 keys (installed).
Labor: three days.
Billed to: the Rustlers. Payable in washers.
Still missing: three piano keys.
No robot was permanently wound down in the making of this city.
[then the real credits]
```

**Post-credits stinger** (silent — no narration): cut to the docks at dawn, full power. The WELCOME sign flickers once and relights in its **new third art state: `POP. 8,011`** — at brownout voltage the wrong neon segment lit; at full power the comma sits home. The game's first object, fixed by the game's last action. Hold two seconds. The S.S. Eventually's foghorn blows one full, proud, un-drooping blast (`foghorn_proud`). Cut to black.

**Priority cut-list:** P1 (must ship): all of §4.1–4.8, credits, stinger, dark entry lines. P2 (polish pass, streamer-mode food): slot-eye "Last act, buddy.", Flange/Betty/ferry/dumpster/graffiti/fireEscape/piano/oilBar/boxOffice/leftys finale flavor.

---

## 5. Music brief & the detuning mechanism (concrete), SFX list

### 5.1 The act-flag pitch drift (N-A5 — this is the spec)

genmusic emits **static MIDI at build time**; act flags are runtime. Therefore: **bake detune variants at build time, select by flag at runtime.** Each builder in `tools/genmusic.py` gains parameters; `main()` emits variants; room `musicLoop` scripts branch on `actNumber`/finale bits to pick the `.soun`.

```python
# tools/genmusic.py — additions
def detune_events(cents):
    """GM pitchwheel, default bend range ±200 cents. Never CH_DRUM."""
    val = max(-8192, min(8191, round(8192 * cents / 200)))
    return [(0, 0, mido.Message("pitchwheel", channel=ch, pitch=val))
            for ch in (CH_LEAD, CH_BASS, CH_EP)]

# every build_* gains: (detune=0, tempo_scale=1.0, voices=ALL)
#  - prepend detune_events(detune) at tick 0, order 0
#  - set_tempo uses bpm2tempo(BPM * tempo_scale)
#  - skip note events for channels not in `voices`
```

Variant table (emitted files; MIDI is tiny — each variant is a few KB):

| Cue | act 1 (base) | act 2 | act 3 | finale `_dying` |
|---|---|---|---|---|
| dockside | 0¢ | −45¢ | −95¢ | −160¢, ×0.88 tempo, voices=(bass, ep) — drums die first, then the lead |
| scrapnbarrel (rag) | 0¢ | −45¢ | −95¢ | −160¢ **+ ritardando**: set_tempo events each bar, 104→60 BPM, ends mid-bar 8 — the player piano running out. **One-shot**: the tavern's watchdog loop must not restart it in finale state |
| backalley | 0¢ | — (act-2 room? keep −45¢ for symmetry) | −95¢ | −160¢, ×0.88, voices=(bass) |
| shuffle | — | 0¢ at first arrival... **no: −45¢** (Midtown is first heard in act 2; its "full cheer" was the N-A5 complaint — the act-2 baseline is already drifted) | −95¢ | −160¢, ×0.88, voices=(bass, ep) |
| vamp | — | −45¢ | −95¢ | not needed (theater interior closed in finale) |
| **shuffle_true** | credits: **0¢, full band** — the first in-tune cue in the game | | | |

Loop points are in **beats**, so they survive tempo scaling unchanged (`BARS*4+1`); declare each variant as its own `sound` in the room and pass the same loop-beat constant to `imPlayerSetLoop`.

**Risk note for the implementer:** native CoreAudio honors pitchwheel trivially; ScummVM's AdLib OPL driver supports pitch bend, but **the browser is canonical** — prove it with one probe take (play `shuffle` vs `shuffle_act3` in the wasm build, ear-check + dub-pipeline spectral check) before wiring all rooms. Fallback if OPL bend is broken: coarse drift by transposing note numbers (−1 semitone at act 3, −2 for `_dying`) and keep the fine bends native-only.

### 5.2 New cues

1. **"Pilot Light" (DynamoRoom hum)** — `build_hum(detune)`. 8 bars, 4/4, **56 BPM**, D root (the island's tonal center, shared with Dockside's D minor). CH_BASS: D1+D2 pedal whole notes; CH_EP: open fifth D3/A3 half-note swells, velocity 40; no drums, no lead. Loop at beat **33** (`8*4+1`). Variants: `hum_p0` = −100¢ (matches "flat by half a step", the standing canon), `hum_p1` = −120¢, `hum_p2` = −140¢, `hum_p3` = −160¢ — DynamoRoom's musicLoop steps down one variant per key seated. After `blackoutDone`: **no music**. Silence is the cue.
2. **"Five Turns" (the rewind, one-shot)** — `build_rewind()`. 12 bars, D minor → D major. Tempo ramp via per-bar `set_tempo`: 56 → 100 BPM across bars 1–8. **Pitch ramp: per-beat pitchwheel events on all melodic channels, lerping −160¢ → 0 across bars 1–8** — the detuning hum reeled back in, audibly, under the relight. Bars 1–2 bass pedal alone; bar 3 adds EP fifths; bar 5 drums enter (brushes); bar 9, in D major, the lead quotes Dockside's bars 5–8 melody (the wistful harbor theme) resolving *upward* for the first time; bars 11–12 full band, picardy D major hold. No loop — the script plays it once and the applause/clink SFX carry the tail.
3. **Credits**: `shuffle_true` (above), looped.

### 5.3 SFX (genaudio.py recipes — same ingredient kit: `partials`, `noise_burst`, `mix`, `concat`)

| Name | Recipe sketch |
|---|---|
| `keyseat` | Heavy brass home-coming: `partials(0.4, [(96,1.0,10),(160,0.6,14),(240,0.3,18)])` + `noise_burst(0.03,0.6,100)`, then one rising confirmation click `partials(0.05,[(1500,0.6,70)])`. |
| `breaker` | Knife switch: clack `partials(0.08,[(1400,0.7,70)])` + body thud `partials(0.2,[(70,1.0,18)])` + spark fizz `noise_burst(0.25,0.15,12)`. |
| `powerdown` | A city tier dying: sine gliss 520→60 Hz over 1.2 s (sample-loop like `sfx_sizzle`'s whine, deeper/longer) + sub partial, exponential fade, terminal soft thud. |
| `winddown` | A bot's spring running out: 9 clicks `partials(0.03,[(f,0.5,90)])`, f stepping 1900→1100 Hz, gaps widening 0.08→0.4 s. Used for Crank and each Rustler. |
| `humstop` | The full blackout: 0.5 s low-D drone (73.4 Hz, two partials) fading to nothing + one deep thud + 1 s of rendered silence so the cut to quiet is in the file, not the mixer. |
| `foghorn_proud` | `sfx_foghorn` recipe, droop removed, full 2.0 s envelope, third partial brighter. The stinger. |
| Reused | `ratchet` (winds), `boing` (the eight-turn launch), `knock` (the code), `clink`, `applause`, `pickup`, `plink`. |

All 8-bit unsigned mono VOC; one `.soun` per effect; music packed as `-midi` flavor only (never `-gmd`) — per `docs/research/AUDIO.md` rules.

---

## 6. Walkthrougher beats

### 6.1 Canonical validate shots (the deploy gate; terse, Escape-through)

```yaml
# scene 11 segment of full-run.play.yaml (after scene 10's closing shot)
- name: the-fences-math
  do: {verb: Examine, object: winding head}
  expect: [talking]
- name: seat-key-one
  do: {verb: Use, object: winding head, with: inventory.slot(windup key)}
  expect: [talking, pixel: {at: cityVista.docks, is: blackout}]
  timeout: 60
- name: seat-key-two
  do: {verb: Use, object: winding head, with: inventory.slot(voltina key)}
  expect: [talking, pixel: {at: cityVista.midtown, is: blackout}]
  timeout: 60
- name: the-long-way                       # Crank gives Key #3 + the five-turns brief
  do: {verb: Talk to, object: Old Crank}
  expect: [talking, pixel: {at: cityVista.threelights, is: stubborn-lit}]
  timeout: 90
- name: stairs-down                        # silent transition
  do: {verb: Use, object: dynamo gate}
  expect: [pixel: {at: midtown.roomDark, is: blackout}]
- name: the-sequel-gets-cancelled          # P4
  do: {verb: Use, object: Grand Cog Theater}
  expect: [talking, pixel: {at: marquee, is: blackout}]
- name: pending                            # P5 — poster shown, not consumed
  do: {verb: Use, object: City Hall}
  expect: [talking, pixel: {at: cityHall.banner, is: blackout}]
- name: free-at-last                       # alley dark entry narration
  do: {verb: Use, object: funicular station}     # stairs; silent
  expect: [talking]                              # entry lines incl. the FREE gag
- name: buying-not-selling                 # the Rivet inversion
  do: {verb: Talk to, object: Rivet}
  expect: [talking, pixel: {at: inventory.lastslot, is: bright-steel}]  # the bolt
- name: his-bar-his-hand                   # P6 + chained blackout cutscene
  do: {verb: Talk to, object: Gusket}
  expect: [talking, pixel: {at: tavern.roomDark, is: blackout}]
  timeout: 90
- name: old-habits                         # P8 fires inside DynamoRoom entry cutscene
  cutscene: DynamoRoom.entry
  expect: [talking, pixel: {at: rustlers, is: statue-grey}]
  timeout: 90
- name: five-means-five                    # P9 — dialog option click (B2 machinery)
  do: {verb: Use, object: pilot crank}
  dialog: "Five turns. Regulation."
  expect:
    - talking
    - pixel: {at: cityVista.docks, is: relit}
    - pixel: {at: keySlots.third, is: brass-turning}
    - console: no-errors
  timeout: 180
- name: payable-in-washers                 # ending cutscene tail
  expect: [talking]
- name: work-order-closed                  # credits card
  expect: [pixel: {at: titleband, is: white}]
- name: the-comma-comes-home               # stinger
  expect: [pixel: {at: neonSign.comma, is: neon-lit}, silence-then: foghorn]
```

New stage-map probes needed from genassets: `cityVista.docks/.midtown/.threelights`, `marquee`, `cityHall.banner`, `roomDark` per room, `rustlers`, `keySlots.third`, `neonSign.comma`, palette names `blackout`, `stubborn-lit`, `relit`, `statue-grey`.

### 6.2 Streamer-mode detours & mistakes (perform-only; schema per production plan)

```yaml
# detours — optional beats, [talking] only
- detour: jump-the-gun        # before keys: Use pilot crank → "It won't catch under load."
- detour: ask-why-last        # Talk to Old Crank twice pre-seating
- detour: the-plate           # Examine rating plate (FIVE MEANS FIVE — plants the answer on camera)
- detour: last-act-buddy      # tavern back door in blackout; the slot-eye's farewell
- detour: the-wall-gets-a-word  # Examine Flange, dark tavern
- detour: gn                  # Talk to Betty, dark docks
- detour: rope-at-capacity    # Use oil voucher on dark Oil Bar ("I step over the rope. Twice.")
- detour: washers-on-the-table  # Examine rustlers' table, dark tavern
- detour: hats-survived       # Examine the statues before winding
- detour: smell-the-source    # Smell the Dynamo

# mistakes — wrong-but-reasonable; the refusal line IS the assertion
- mistake: ease-her-in
  do: {verb: Use, object: pilot crank}
  dialog: "Two turns. Ease her in."
  expect_line: "The pilot spring clears its throat and goes back to sleep."
- mistake: it-worked-on-stage          # THE fair mistake — the game taught this
  do: {verb: Use, object: pilot crank}
  dialog: "Eight turns. It worked on stage."
  expect_line: "The crank disagrees, formally."
- mistake: dome-not-head               # Use key on the Dynamo dome
  expect_line: "Not the dome. The winding head."
- mistake: leave-mid-seating           # Open gate after one key
  expect_line: "Seat them all or seat none."
- mistake: hat-heist
  do: {verb: Pick up, object: rustler statues}
  expect_line: "nothing here was worth stealing"
```

Streamer order: detours woven into the descent (the performer examines the dark city like a person saying goodbye to it), mistakes 1–2 fired at the crank **before** the win — the eight-turn launch is the film's biggest laugh and the five-turn follow-up its quietest beat. Render.py chapter card: "ACT THREE — FIVE MEANS FIVE".

---

## 7. Planted / paid ledger

### Consumes (pays off)

| Plant | Source | Payment here |
|---|---|---|
| Three keys / "could wind the city back up. Or down." | Rivet, Act 1 | The whole scene; "or down" literalized by the load-shedding seating |
| "One key, three slots... Even the fence can do that math" | `midtown.scc:dynamo` (N-M6 fix) | `keySlots` — "The fence's math, in brass" |
| "Regulation maximum is five" | `theater.scc` stage act (B8 choice) | The winning wind-count; the eight-turn mistake is the same plant's dark side |
| "The key that winds itself. Mind the cables." | Voltina (Scene 05 greeting + Scene 06 fortune) | Crank's key turning by itself in slot three; "The fortune was a spoiler." |
| The detuning hum / "flat by half a step" / "Neither did the clunk" | GDD audio pillar; midtown entry; N-A5 | `_dying` variants → first silence → the rewind's −160¢→0 ramp → in-tune credits |
| Knock-code (2-1-2) | tavern eavesdrop (validate path since B9) | The Rustlers announce their ambush with it ("Old habits."); slot-eye detour |
| Rustler ransom motive | GDD (N-A9 fix) | "Nice city. Shame if nobody wound it." → billed in washers |
| Washers as "post-bolt currency" | `tavern.scc:rustlersTable` | "Payable in washers." |
| Marquee showboating cost Key #1 | B3 heist | His name in lights is one of the three loads; he switches it off himself |
| NOTHING IS WRONG banner / aide fears paper / "official and correct" | `midtown.scc:cityHall` | The banner is a load; the notice beats it; NOTHING **WAS** WRONG |
| Official notice (poster) | Act 1, `docks.scc:board` | Shown to the aide (not consumed; credits don't list it as a part) |
| "He pays the bolt without a word." | riddle duel (N-A4 fix kept the image) | Rivet pays a bolt for a fact, sincerely, same words |
| The ampersand "the freshest thing in here" | `tavern.scc:barSign` | It's fresh because it was wired around the meter — the third load |
| "Act Three, buddy" runner (slot-eye monopoly) | tavern/alley | "Last act, buddy." — the runner's closing telling, still NPC-only |
| POP. 8,01,1 comma / "maintenance is iterative" | docks sign + embodiment fix | Stinger: full voltage lights the right segment — the misprint was a brownout symptom all along |
| Broken ferry / sad foghorn | `docks.scc:ferry`, `sfx_foghorn` | Stinger: one proud blast |
| Power model: hum winds mainsprings remotely; hand-winding crude backup | `docks.scc:422` (embodiment BLOCKER fix) | The entire finale mechanism — see §8 |
| "Guess I live here now." | arrival cutscene | Final line: "I live here now." — no guess |
| Crane crate / "up a crane" / hook-on-a-line | Act 1 + heist | Key #1's seat line recaps its whole journey in one sentence |
| Piano's third key "missing entirely" | `tavern.scc:piano` | Deliberately **not** repaired: "back to missing every third note" + credits line "Still missing: three piano keys." The desk has re-litigated this hotspot twice; this doc's ruling: it stays a theme, closed with one flat credit line, never an item. |

### Creates

Forward plants: **none** — the game ends. Internal plants paid within the scene (listed so the desk can audit them as fair-play, not danglers): the empty-hideout line → the ambush; "three lights" vista → the three breakers; the self-wind rehearsal → the wind choice; "Wake me when—" → "—it's over."; washers on the tavern table → the bill. The stinger's `POP. 8,011` is terminal — resist the temptation to tick it to 8,012; one loop closure, not a sequel hook.

---

## 8. Embodiment audit (of this scene's own text)

Power model (canon, stated once at `docks.scc:422`): *the hum keeps every mainspring on the island wound, remotely; steam, clockwork, and engine bots all run off spring-banked charge; hand-winding is the crude, off-warranty backup.* This scene never restates it (no double-telling) and every claim below is checked against it:

1. **Seating keys darkens tiers.** Mechanism: each key engages a winding train and the Dynamo stops *feeding* a tier, banking its remaining output into the barrel — narrated as "the hum pulls back," never as lights being "drained from" bots. Crank attributes the tier order to design ("We planned it that way"), so the schedule is knowledge his body can have: he built it. ✓
2. **Bots survive the blackout on banked charge, at different rates.** Gusket (big industrial spring) and Rivet (hoards everything, including charge) stay up all night; Betty (crane, "banks deep") sleeps through it; the aide endures (City Hall has floodlight wiring; insomnia is staffed); the Rustlers die fastest — *salt corrosion = friction = spend*, the exact physics already canonized by "harbor bolts, brined stiff." The climb spends their budget: stated on screen. ✓
3. **Sprocket's own spring.** He's a bot like any other — so before the descent he hand-winds himself, on screen, with the established crude-backup verb and the established ratchet sound. The beat does double duty as the five-turns rehearsal. No "including me, as of today" ambiguity remains. ✓
4. **Stopping ≠ dying; resume mid-word.** "Grinds to a halt" has always been the game's halt model (Gusket's servo looped for years with Gusket intact). Crank and the Rustlers freeze mid-sentence and resume exactly there — a *consequence of the model*, played twice as the same joke ("Wake me when—"/"—it's over.", "Hand over the—"/"—keys!"). Consistent, and the consistency IS the gag. ✓
5. **Crank surrenders his key and winds down slowly** — removing the key doesn't unwind him; it removes his *winding interface*, so he coasts on banked charge and stops. The returning hum winds him **remotely, keyless** — exactly what the hum does to every bot, none of whom wear keys. The fortune's "key that winds itself" is the Dynamo turning his donated key as it runs: a thing a spectator can see, not a mystic assertion. ✓ (His reaching his own back: the key is socketed between his shoulders; he's had sixty years of practice. One line covers the reach — "the long way.")
6. **Sensory claims.** Sprocket identifies the three loads *only after Crank names them*, and Crank names them from lived knowledge plus the Dynamo's own load gauge implied by "three taps somebody wired around the meter" — no reading neon from a mile away. The vista shows three lit pixels; the art must actually draw them (genassets: vista state 4 = exactly three bright dots at docks-tier and midtown-tier positions, matching the probe names). Sprocket navigates the blackout by his own eye-light — bot eyes are established light sources (slot-eye, the operator's "ember"). "I never noticed they hummed" was cut from the draft for exactly this audit. ✓
7. **The funicular/stairs.** A powered funicular dies in a blackout; the maintenance stairs were always there ("the fare was for not taking them") — retro-consistent with a fare gate whose entire character is charging for the easy way. The return ascent happens in a cutscene with handrails named, not teleportation pretending otherwise. ✓
8. **The pilot crank.** A generator needing hand-excitation to bootstrap is the power model's own thesis — the *crude backup* exists at city scale, and it's crude there too: a crank sized for a bigger bot, a stamped plate, an exact turn count. The eight-turn launch reuses the established overwound-spring physics (the stage act's boing) — same body, same consequence. The under-load refusal is honest clockwork: you can't wind a spring that's actively driving load. ✓
9. **The stinger's comma.** A physical comma can't migrate; a neon *segment* can misfire at brownout voltage and light correctly at full voltage. The fix retroactively converts the Act 1 misprint into the city's first visible symptom — and the art must comply: genassets gains a third sign text state (`POP. 8,011`), shown only when `cityRewound`. This also discharges the embodiment desk's standing note that the line and the art must agree. ✓
10. **Counting discipline** (the desk's NIT class): no exact countable numbers asserted against the art anywhere in this scene — "three lights," "three statues," "three slots" are all drawn at exactly three; "pier by pier," "every third note" are ratios the art survives.

---

### Implementation pitfalls checklist (NOTES.md compliance, for the builder)

- Verb ids: **no new verbs**; everything uses the pinned set in `common.sch`.
- Ownership: keys consumed via `setObjectOwner(x, 0)`; "in pocket" checks are `== VAR_EGO`, never truthy.
- Dub source order: every handler above is written walkthrough-path-first; the flop branches of the wind dialog sit *after* the win branch in source.
- Room transitions (gate, stairs, blackout walk) say **nothing**; all arrival flavor is in entry scripts.
- Flags set at branch tops, before any `egoSay`/`actorSay`.
- `rewindSnd` and the finale `rag_dying` are one-shots: no `imPlayerSetLoop`, and the room watchdog loops must check the finale bits before restarting anything.
- The dynamoCore glow-pulse loop is the signFlicker pattern: stop it explicitly when the rewind cutscene takes the room, or it flickers over the ending.
- Every speaking actor (`aide`, `rustlerLeader`, `mayorPiston`, `slotEye`, `gusket`, `rivet`, `oldCrank`) is `putActorAt` into its room before its first line, per the NPC-DIALOG landmine.
- Global-bit linkage across compilation units: prove with a two-unit smoke test before building the finale state on it; fallback documented in §0.
- Editorial desk runs on this text before validate; the smell lines above deliberately use the flat-fact / sensor-can't-parse shapes, zero `[material] and [abstract]` zeugmas, zero self-grades, and the only ALL-CAPS are signage (`FREE`, `PENDING`, `NOTHING WAS WRONG`, `WIND TO FIVE`) and one NPC mouth.