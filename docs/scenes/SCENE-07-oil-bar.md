All required reading done (PRODUCTION-PLAN, GDD, NOTES, CHARTER + all three editorial reports, NPC-DIALOG, NARRATION, WALKTHROUGHER, genmusic/genaudio, tavern.scc, theater.scc, midtown.scc, alley.scc, inventoryitems.scc, common.sch, full-run screenplay). Here is the complete design doc.

---

# SCENE 07 — THE OIL BAR, INSIDE
### Design doc, 2026-06-12 — intended landing place: `docs/scenes/SCENE-07.md`

**Working title:** *A Separate Financial Instrument*

**Files this scene touches:** new `game/oilbar.scc` + `game/oilbar.sch`; edits to `game/midtown.scc` (velvet rope object, bouncer branches, silent transition), `game/inventoryitems.scc` (the cancelled work order), `game/common.sch` (3 actor decls + talk colors), `game/actors.scc` (setup), `tools/genassets.py` (room art, GEOM, three 2-state objects, inventory icon, talk-color probes), `tools/genmusic.py` (`build_oilbar`), `tools/genaudio.py` (4 new effects), `walkthrough/screenplay/` (validate shots + streamer screenplay).

**Hard dependency:** the B2+B8 dialog-tree work (THE CONTESTS MUST BE PLAYABLE) — this scene's centerpiece is a two-round dialog contest using `game/dialog.scc` and the walkthrougher's dialog-option clicking. Per the desk's standing ruling this ships before any Scene 06+ content anyway.

---

## 1. Scene goal & the three-keys spine

**Goal:** The voucher finally beats the velvet rope; inside, Sprocket works uptown society — a bouncer who outsources refusals to the rope, a sommelier of crude with no one to pour for, a frightened City Hall aide drinking the wrong oil — and walks out holding the **cancelled work order**: documentary proof, in Mayor Piston's own steam-pressed signature, that the Mayor cancelled the Dynamo's two-hundred-year maintenance contract and reallocated the money to the NOTHING IS WRONG banners.

**Spine advancement.** No key changes hands here — Scene 07 is the cover-up rail, and the cover-up rail is how the player reaches Key #3:

- **Key #1** (stolen, Scene 05) — untouched; recovery is Scene 09 (knock-code).
- **Key #2** (Voltina) — untouched; Scene 06 is a parallel Act-2 branch off the same prize cutscene (pass → backstage, voucher → here; no ordering gate between 06 and 07, both converge on 08).
- **Key #3 / Old Crank** — this scene puts the name **O. CRANK** on screen for the first time in the whole game, printed on the evidence itself ("Technician of record: O. CRANK"). This discharges the desk's standing N-A10 duty (every scene plants the twist) with a plant the player literally pockets.
- **Scene 08 lever:** the work order is the evidence the player will *act on* at City Hall — the aide says so on screen ("Take it to him. Aides can't. Aides file."). Exposing Piston is what opens the Dynamo District fence (Scene 10), where Key #3 lives.

**Canon obligations honored:** City Hall's aides drink here and talk (booth eavesdrop + the frightened aide from the nine-degree door); uptown society comedy (the bouncer, the sommelier of crude); evidence the player ACTS on (a dialog contest the player can flub funny, then a theft the player performs); N-M4's promise ("tonight it's at capacity") is confronted and defeated, not waved away.

---

## 2. The puzzle chain

### 2.1 Numbered graph

```
                         [Scene 05: oilVoucher won]
                                   |
   P1. OPEN THE ROPE  (midtown, outside)
       lock:   the velvet rope ("at capacity"; the bouncer admits the
               voucher is valid — the ROPE is the obstacle)
       key:    Use oilVoucher WITH the velvet rope (not the bar, not
               the bouncer): the voucher is "valid at participating
               establishments"; the rope's own plaque says THE ROPE.
               ESTABLISHED. The rope is an establishment. It participates.
       consumes: oilVoucher (owner -> 0). ropeOpen = 1.
                                   |
   P2. ENTER + MEET THE ROOM  (story beats, no lock)
       - entry cutscene blocks the room
       - TalkTo aide #1: he recognizes Sprocket ("You're the one with
         the paper.") and clams up; homesickness planted
       - TalkTo sommelier #1: tasting-room comedy; the Dynamo standing
         order's existence planted (two hundred years, then it stopped)
                                   |
   P3. THE ORDER — round 1 (PLAYABLE: dialog tree, pick the pour)
       3 options; two flop funny and teach; winner: dock-aged 10W-40
                                   |
   P4. THE ORDER — round 2 (PLAYABLE: dialog tree, pick the billing)
       3 options; two flop funny and teach; winner: the Dynamo
       maintenance account -> the sommelier descends to the cellar
       UNDER PROTEST. pourOrdered = 1; the bar is unattended.
                                   |
   P5. CERTIFIED ARCHIVAL WORK  (the act)
       lock:   the receipt spike (sommelier's eye, when present)
       key:    Use the spike while he's in the cellar
       yields: workOrder (inventory). Cutscene ends with the sommelier
               surfacing and serving the aide. aideServed = 1.
                                   |
   P6. THE EXPOSÉ  (TalkTo aide, served)
       The aide, holding harbor oil, confirms the cover-up in four
       short direct lines and points the evidence at City Hall.
       aideTalked = 1. -> Scene 08.
```

Interlocks: P5 requires P4 (the cellar trip is state, not a timer — the sommelier stays down until the grab; no dead ends, no dawdling penalty). P6 requires P5 (the serve happens inside the grab cutscene, so the confession can never precede the evidence). All flops are recoverable; re-TalkTo reopens the tree at round 1.

### 2.2 Fair-play audit — every hint, source named

| Puzzle | Hint | Source (on-screen) | Status |
|---|---|---|---|
| P1 | "The rope is a separate financial instrument." | `midtown:oilBar:UsedWith(voucher)` first presentation | SHIPPED (N-M4 fix) |
| P1 | "Valid at participating establishments." | `inventoryitems:oilVoucher:LookAt` | SHIPPED |
| P1 | Plaque: "THE ROPE. ESTABLISHED. No date." | NEW `midtown:velvetRope:LookAt` | the keystone inference |
| P1 | Escalation: "Separate instruments get redeemed separately." | NEW second voucher presentation to the bouncer | escalating hint, desk-approved pattern |
| P3 | Aide's eye "keeps sliding to the dark end of the shelf" | `oilbar:aide:LookAt` | hint 1, oblique |
| P3 | "The oil up here is too educated." | `oilbar:aide:TalkTo` #1 (direct line) | hint 2, oblique |
| P3 | "You can't get an honest 10W-40 above the funicular." | `oilbar:aide:TalkTo` #2 (escalation) | names it on SECOND contact only (N-A2 discipline) |
| P3 | Bottom shelf: "dark glass and no biographies. Working oil." | `oilbar:backBar:LookAt` | environmental |
| P3 | Poster-on-aide mistake: he drains half his glass for courage | `oilbar:aide:UsedWith(poster)` | productive mistake teaches drink⇒nerve |
| P3 | "He asks what the bot at the end is having. Nothing, currently." | `oilbar:sommelier:TalkTo` (pre-metAide filler) | catches sommelier-first players |
| P4 | DYNAMO MAINTENANCE — STANDING ORDER, stamped CANCELLED | `oilbar:cellarList:LookAt` | the account's existence, visible |
| P4 | Two-hundred-year contract story | `oilbar:sommelier:TalkTo` #1 — **forced**: intro always precedes the dialog tree (no unsourced knowledge; N-L3 lesson) | structural |
| P4 | "Civic reassurance" toast | `oilbar:boothAides:TalkTo` (optional) + the "City Hall settles in banners" flop (in-tree) | the flop itself teaches |
| P5 | "The bottom page has a municipal seal." | `oilbar:receiptSpike:LookAt` (sommelier present) | target named before the window |
| P5 | "The bar is suddenly very unattended." | round-2 win cutscene, last card | window signpost on the critical path |
| P5 | "His eye is on the pour, the door, and the spike." | `oilbar:receiptSpike:Use` refusal (present) | refusal that teaches |
| P5 | "Bars keep paper. Bars always do." | `oilbar:aide:TalkTo` during the window | redundant source |
| P6→08 | "Take it to him. Aides can't. Aides file." + workOrder Use line | exposé cutscene + `inventoryitems:workOrder:Use` | forward pointer at a SCHEDULED scene |

No lock names its key verbatim on first contact; every lock has ≥2 sources; every refusal on the critical path points somewhere (post-fix house standard). The one inference the scene demands (rope = establishment) has three independent on-screen legs.

### 2.3 The playable-agency beat (charter: THE CONTESTS MUST BE PLAYABLE)

P3+P4 is a two-round dialog contest with **nine reachable outcomes**, four of them funny flops with distinct content, all recoverable, the winners planted. The player can be *wrong* in character ("Your finest single-origin" is the polite-society move and it flops gloriously). This is the B2 shape — pick from 3, two flop funny — executed on new material. The theft (P5) is a second, smaller agency beat: the player chooses the moment and performs the act; nobody performs it for them. The scene contains zero spectator victories.

---

## 3. Object table

Stage is 320×144 (verb panel below). New room `OilBarRoom`; two new objects in `MidtownRoom`.

```
 0        40        80       120       160       200       240       280  320
 +---------+---------+---------+---------+---------+---------+---------+---+
 |             [portrait of                [centrifuge]                     | 0
 |    [back bar / single-origin shelf]      x152 y4    [portrait Piston]   | 16
 | [door]   x36 y24 w96 h32                            x224 y16 w36 h40    | 32
 | x8 y56                                                                  | 48
 | w24 h48  [somm.]                 [aide]        [booth of aides]         | 56
 |          x80 y52 w24 h44         x172 y56      x216 y76 w64 h40         | 72
 |   [list]   [bar counter x32 y84 w128 h26] [spike]                       | 84
 |   x40 y74    w20 h14              x140 y70 w14 h18                      | 100
 |                          [cellar hatch x148 y106 w24 h12]               | 112
 |                    (walk floor y 112-132)                               | 128
 +--------------------------------------------------------------------------+ 144
```

### MidtownRoom additions

| Object | Rect (x,y,w,h) | Verbs | States |
|---|---|---|---|
| `velvetRope` | 104, 96, 48, 12 (strip in front of the Oil Bar facade) | LookAt, Smell, Use/Open/Move, UsedWith(voucher) | 1 = hung between posts; 2 = unhooked, hanging from one post. Drawn in genassets (2-state, marquee pattern) |
| `oilBar` (existing) | unchanged | + TalkTo (bouncer); UsedWith gains `voucherShown` escalation branch; Open/Use gains silent transition when `ropeOpen` | unchanged |

### OilBarRoom

| Object | Rect | Verbs | States / notes |
|---|---|---|---|
| `doorOut` | 8, 56, 24, 48, dir EAST | LookAt, Open/Use (SILENT → MidtownRoom, putActorAt 130, 120) | — |
| `backBar` | 36, 24, 96, 32 | LookAt, PickUp, Smell | top shelf lit amber; bottom shelf dark glass (painted, not a state) |
| `portrait` | 224, 16, 36, 40 | LookAt, Use/PickUp, Smell | Mayor Piston in oils, overflowing his frame onto the wall (painted gag) |
| `centrifuge` | 152, 4, 40, 20 | LookAt, Use, Smell | **the room's animating element**: 2-frame rotation flicker, signFlicker-pattern loop (mind the stopScript bug class) |
| `sommelier` | 80, 52, 24, 44, dir SOUTH, class Person | LookAt, TalkTo (intro / dialog tree / fillers), Give/UsedWith, Smell | 1 = at post; 2 = absent (cellar). Costume-less actor `sommA` for actorSay, parked at (92, 96) |
| `oilBarCounter` | 32, 84, 128, 26 | LookAt, Use, Smell | — |
| `cellarList` | 40, 74, 20, 14 | LookAt, Use, Smell | the menu; carries the CANCELLED plant |
| `receiptSpike` | 140, 70, 14, 18 | LookAt, Use/PickUp/Open (the grab), Smell | 1 = full; 2 = minus one page (post-grab) |
| `aide` | 172, 56, 24, 48, dir SOUTH, class Person | LookAt, TalkTo (intro / hint / window / exposé / after), Give/UsedWith(poster, workOrder), Smell | painted on stool; costume-less actor `aideA` parked at (184, 100) |
| `boothAides` | 216, 76, 64, 40, class Person | LookAt, TalkTo (eavesdrop), Smell | costume-less actor `boothA` parked at (244, 110) for one line |
| `cellarHatch` | 148, 106, 24, 12 | LookAt, Open/Use, Smell | painted floor hatch; never opens for the player |

### Inventory

| Item | Name | Verbs | Notes |
|---|---|---|---|
| `workOrder` | "cancelled work order" | LookAt (4 cards — the dossier), Use (Scene-08 pointer), Smell, Preposition "to", standard `if(objB)` UsedWith routing | icon `inv_workorder.bmp` (paper + red stamp). Consumed in Scene 08 |

### New flags (oilbar.sch / midtown.sch)

`ropeOpen, voucherShown, visitedOilBar, metSommelier, metAide, aideHinted, heardBoothToast, pourOrdered, aideServed, aideTalked` — all bits. "Sommelier in cellar" is **derived**: `pourOrdered && !aideServed` (one less bit to desync). New actors in common.sch: `bouncerA` (color 115), `sommA` (113), `aideA` (114); `boothA` reuses 114 (same caste, same voice family — or claim the fossil BETTY_COLOR 106 per NPC-DIALOG open question 7).

---

## 4. Full dialog draft

Register rules applied throughout: Sprocket reports; NPCs get direct punchlines ≤12 words; no double-telling; NPC punchline → Sprocket flat button; no self-grading; no smell-template zeugma; no Sprocket act-naming; caps only on diegetic signage. **Branch order inside each handler is dub order** (walkthrough-path branches first, in canonical chronological order; off-path hint/repeat branches after — marked below).

### 4.1 MidtownRoom — the rope and the bouncer

```c
// NEW object — velvetRope.
// putActorAt(bouncerA, 128, 100, MidtownRoom) in midtown entry (landmine:
// every speaking actor must be in the room before its first line).

object velvetRope {
    verb(int vrb,int objA,int objB) {
    case LookAt:
        if(ropeOpen) {
            egoSay("The rope hangs from one post, off duty. Honorably discharged.");
            return;
        }
        egoSay("Velvet over steel cable, slung between two brass posts. The posts get polished. The street doesn't.");
        waitForMessage();
        egoSay("A plaque on the near post: THE ROPE. ESTABLISHED. No date. Established as a concept.");
        return;
    case Use:
    case Open:
    case Move:
        if(ropeOpen) {
            egoSay("Unhooked. The rope and I are past it.");
            return;
        }
        egoSay("I test the rope. The bouncer tests me back.");
        waitForMessage();
        actorSay(bouncerA, "Touching the rope is a service. It's not included.");
        return;
    case Give:
    case UsedWith:
        if(objB == InventoryItems::oilVoucher) {
            // walkthrough path — FIRST in source
            unless(ropeOpen) {
                ropeOpen = 1;                       // flag before speech
                cutscene(0) {
                    egoSay("Valid at participating establishments, says the voucher. ESTABLISHED, says the rope's own plaque.");
                    waitForMessage();
                    egoSay("I present the voucher to the rope. Formally. The bouncer watches me do the paperwork.");
                    waitForMessage();
                    egoSay("He reads the voucher. He reads the plaque. Somewhere in there, a precedent forms.");
                    waitForMessage();
                    actorSay(bouncerA, "The rope participates.");
                    waitForMessage();
                    startSound(unhookSnd);
                    setObjectState(velvetRope, 2);
                    setObjectOwner(InventoryItems::oilVoucher, 0);
                    egoSay("He unhooks the rope and folds it over his arm like a sommelier's towel.");
                    waitForMessage();
                    actorSay(bouncerA, "Capacity was the rope's grievance. The rope has been compensated.");
                    waitForMessage();
                    egoSay("One premium oil service, spent on a length of velvet. Uptown.");
                    waitForMessage();
                }
                return;
            }
            return;   // unreachable: voucher consumed with the open
        }
        egoSay("The rope declines. Through the bouncer. The rope has people.");
        return;
    case Smell:
        egoSay("Velvet. Under the velvet, cable. Under the cable, I suspect more velvet.");
        return;
    }
}
```

```c
// EDITS to existing object oilBar (midtown.scc)

case Open:
case Use:
    if(ropeOpen) {
        // room transitions say NOTHING (docs/NOTES.md) —
        // arrival flavor lives in OilBarRoom.entry
        putActorAt(VAR_EGO, 28, 118, OilBarRoom);
        startRoom(OilBarRoom);
        return;
    }
    egoSay("A bouncer the size of a vending machine looks at my dock rust and invents a dress code.");   // shipped
    waitForMessage();
    egoSay("I'm on the list, I tell him. He shows me the list. It's a picture of the door.");            // shipped
    return;

case TalkTo:                                       // NEW
    if(ropeOpen) {
        actorSay(bouncerA, "The rope remembers you fondly.");
        waitForMessage();
        egoSay("We've all grown.");
        return;
    }
    egoSay("I ask about the rope's hours. The rope keeps its own counsel, he says. He interprets.");
    waitForMessage();
    actorSay(bouncerA, "The rope sees everyone. Eventually.");
    return;

case Give:
case UsedWith:
    if(objB == InventoryItems::oilVoucher) {
        unless(voucherShown) {                     // first presentation — shipped lines, FIRST in source
            voucherShown = 1;
            egoSay("The bouncer reads it. Valid, he admits. The rope, he explains, is a separate financial instrument.");
            waitForMessage();
            egoSay("Tonight it's at capacity. The rope. Is at capacity.");
            return;
        }
        // escalation — the N-M4 promise grows its second leg
        egoSay("He reads it again. Still valid. The rope, he repeats, is a separate financial instrument.");
        waitForMessage();
        actorSay(bouncerA, "Separate instruments get redeemed separately.");
        waitForMessage();
        egoSay("He says it slowly, like directions to a window.");
        return;
    }
    if(objB == InventoryItems::backstagePass) {    // streamer mistake — pays the pass's own Use line
        egoSay("I show him ALL ACCESS, over my own startled face.");
        waitForMessage();
        actorSay(bouncerA, "That opens a door. This is a rope.");
        waitForMessage();
        egoSay("The pass goes back in my pocket, access intact.");
        return;
    }
    if(objB == InventoryItems::poster) {           // streamer mistake
        egoSay("I hold up the official notice. NOTHING IS WRONG.");
        waitForMessage();
        actorSay(bouncerA, "Agreed.");
        waitForMessage();
        egoSay("Professionally, nothing ever is.");
        return;
    }
    egoSay("He doesn't hold things. Holding things is a different department.");   // shipped
    return;
```

### 4.2 OilBarRoom — entry

```c
local script entry() {
    startScript(1, musicLoop, []);   // The Single-Origin Sway, loop beat 49
    startScript(1, centrifugeSpin, []);
    putActorAt(sommA,  92,  96, OilBarRoom);   // all speakers parked before
    putActorAt(aideA,  184, 100, OilBarRoom);  // any line (actorTalk landmine)
    putActorAt(boothA, 244, 110, OilBarRoom);

    unless(visitedOilBar) {
        visitedOilBar = 1;
        cutscene(2) {
            putActorAt(VAR_EGO, 28, 118, OilBarRoom);
            walkActorTo(VAR_EGO, 70, 124);
            waitForActor(VAR_EGO);
            egoSay("The Oil Bar, inside. Everything is amber: the light, the bottles, the prices.");
            waitForMessage();
            egoSay("A ceiling centrifuge spins the house pour to a shine. The music is what a tuxedo would hum.");
            waitForMessage();
            egoSay("In the corner booth, City Hall aides are drinking lunch at nine in the evening.");
            waitForMessage();
            egoSay("And alone at the bar: a fresh civic crest on an old chassis, folded over a glass like a memo nobody filed.");
            waitForMessage();
        }
    }
}
```

### 4.3 The sommelier

```c
object sommelier {
    verb(int vrb,int objA,int objB) {
    case LookAt:
        if(pourOrdered && !aideServed) {       // absent state
            egoSay("Not at his post. From below the floor: the sound of a bottle being judged.");
            return;
        }
        if(aideServed) {
            egoSay("Back at his post, towel refolded. The cellar dust didn't dare follow him up.");
            return;
        }
        egoSay("The sommelier. White towel, black chassis, a decanting arm with more joints than I have parts.");
        waitForMessage();
        egoSay("He's listening to a thimble of crude. The crude is apparently confiding in him.");
        return;

    case TalkTo:
        // BRANCH ORDER = dub order: intro, then the contest, then fillers.
        unless(metSommelier) {
            metSommelier = 1;
            cutscene(0) {
                egoSay("He pours a thimble of crude, swirls it, and holds it up to where an ear would be.");
                waitForMessage();
                actorSay(sommA, "Derrick Nine. A confident year.");
                waitForMessage();
                egoSay("I ask if anyone in this room could tell it from the house pour.");
                waitForMessage();
                actorSay(sommA, "No.");
                waitForMessage();
                egoSay("He pours it back. Gently. So the bottle doesn't hear.");
                waitForMessage();
                egoSay("I ask about the old days. This bar oiled the Great Dynamo, he says. Two hundred years. By the barrel. By appointment.");
                waitForMessage();
                actorSay(sommA, "Never late. Never tipped. Never complained.");
                waitForMessage();
                egoSay("Then, last spring, it stopped. He won't say more. Grief, or a nondisclosure.");
                waitForMessage();
            }
            return;
        }
        if(metAide && !pourOrdered) {
            startScript(0, orderDialog, []);   // the contest — see 4.4
            return;
        }
        if(pourOrdered && !aideServed) {       // window filler
            egoSay("From under the floor, the sound of a vintage being forgiven.");
            return;
        }
        if(aideServed) {
            egoSay("He's re-alphabetizing the derricks, west to east. The evening took something out of him.");
            return;
        }
        // !metAide filler — points at the aide
        egoSay("He asks what the bot at the end is having. Nothing, currently. It worries us both.");
        return;

    case Give:
    case UsedWith:
        egoSay("He receives it on the towel, inspects it, and returns it. The towel forgives everything.");
        return;
    case Smell:
        egoSay("Nothing. He out-clean-rooms my sensor.");
        return;
    }
}
```

### 4.4 The contest (dialog tree — `game/dialog.scc` UI)

**Round 1 — the pour.** Lead-in (Sprocket): `egoSay("He asks, with ceremony, what the gentleman at the end will be having.");`

| Option (player-clicked, Sprocket speaks it) | Outcome |
|---|---|
| 1. "Your finest single-origin." | FLOP — `egoSay("The sommelier ascends three emotional registers and decants Derrick Nine like a christening.");` `egoSay("The aide takes one nose of it and slides it back, untouched.");` `actorSay(aideA, "Too educated.");` `actorSay(sommA, "Refused. Derrick Nine, refused. I'll be closing early.");` — tree closes; re-TalkTo reopens |
| 2. "Another round of the house pour." | FLOP — `actorSay(sommA, "He has one. He hasn't touched it in an hour.");` `egoSay("The glass is full. The glass has been full all night.");` — tree closes |
| 3. "Something dock-aged. A working 10W-40." | WIN — `egoSay("The towel stops moving.");` → round 2 |

**Round 2 — the billing.** Lead-in: `actorSay(sommA, "Dock-aged. And this is billed to?");`

| Option | Outcome |
|---|---|
| 1. "My tab." | FLOP — `actorSay(sommA, "Tabs here are inherited, not opened.");` `egoSay("I have no ancestors. It's a known gap.");` — back to round 2 (or close + reopen; implementer's call, note it in the screenplay) |
| 2. "City Hall's tab." | FLOP — `actorSay(sommA, "City Hall settles in banners now. We have enough banners.");` `egoSay("The booth in the corner drinks to that without hearing it.");` |
| 3. "The Dynamo maintenance account." | **WIN** — cutscene below |

```c
// round-2 win cutscene
pourOrdered = 1;                                   // flag before speech
cutscene(0) {
    actorSay(sommA, "That account is closed.");
    waitForMessage();
    egoSay("Then it can stand one last round, I say. For two hundred years of never complaining.");
    waitForMessage();
    actorSay(sommA, "...Decanted under protest.");
    waitForMessage();
    egoSay("He folds the towel like a flag and opens the floor.");
    waitForMessage();
    startSound(creakSnd);
    startSound(stepsSnd);
    setObjectState(sommelier, 2);                  // figure gone
    egoSay("The cellar takes him. The bar is suddenly very unattended.");
    waitForMessage();
}
```

### 4.5 The receipt spike (the act)

```c
object receiptSpike {
    verb(int vrb,int objA,int objB) {
    case LookAt:
        if(getObjectOwner(InventoryItems::workOrder) == VAR_EGO) {
            egoSay("The spike, minus one municipal document. The grease thumbprints kept their counsel.");
            return;
        }
        if(pourOrdered && !aideServed) {
            egoSay("Unguarded paper. The rarest vintage in the building.");
            return;
        }
        egoSay("A brass spike by the till, impaling the bar's paper history. Oldest at the bottom.");
        waitForMessage();
        egoSay("The bottom page has a municipal seal and two centuries of grease thumbprints.");
        return;

    case Use:
    case PickUp:
    case Open:
        // walkthrough path FIRST: the grab
        if(pourOrdered && !aideServed) {
            aideServed = 1;                        // flag before speech
            cutscene(0) {
                egoSay("The cellar is still sighing under the floor. I perform some quiet, certified archival work.");
                waitForMessage();
                startSound(paperSnd);
                setObjectState(receiptSpike, 2);
                pickupObject(InventoryItems::workOrder, InventoryItems);
                egoSay("Bottom of the spike: the Dynamo standing order. Two hundred years of weekly oil.");
                waitForMessage();
                egoSay("Across it, a stamp: CANCELLED BY ORDER OF THE MAYOR. Signed in steam-pressed ink: M. PISTON.");
                waitForMessage();
                startSound(stepsSnd);
                startSound(creakSnd);
                setObjectState(sommelier, 1);      // he surfaces
                egoSay("The floor opens. The sommelier surfaces with a dusty bottle and a look of moral exemption.");
                waitForMessage();
                actorSay(sommA, "Your harbor sludge, sir. Decanted.");
                waitForMessage();
                startSound(pourSnd);
                egoSay("He pours it the way you'd lower a casket. The aide takes the glass with both hands.");
                waitForMessage();
            }
            return;
        }
        if(getObjectOwner(InventoryItems::workOrder) == VAR_EGO) {
            egoSay("I have the page that matters. The rest is beverage history.");
            return;
        }
        // refusal that teaches the window
        egoSay("His eye is on the pour, the door, and the spike. All three. It's a sommelier thing.");
        return;

    case Smell:
        egoSay("Two centuries of bar air, pressed flat.");
        return;
    }
}
```

### 4.6 The aide

```c
object aide {
    verb(int vrb,int objA,int objB) {
    case LookAt:
        if(aideTalked) {
            egoSay("He's reading the coaster like it's mail from home.");
            return;
        }
        if(aideServed) {
            egoSay("Working oil in an uptown glass. He looks like a bot whose feet finally reach the floor.");
            return;
        }
        egoSay("A City Hall aide, off the clock. The crest on his chest is fresher than the chassis under it.");
        waitForMessage();
        egoSay("He has the house pour and isn't drinking it. His eye keeps sliding to the dark end of the shelf.");
        return;

    case TalkTo:
        // BRANCH ORDER = dub order: intro -> exposé -> after -> fillers.
        unless(metAide) {
            metAide = 1;
            cutscene(0) {
                egoSay("I take the stool one over. Bar protocol: close enough to talk, far enough to deny it.");
                waitForMessage();
                egoSay("He clocks me, and something behind his face files itself.");
                waitForMessage();
                actorSay(aideA, "You're the one with the paper.");
                waitForMessage();
                egoSay("The door at City Hall. Nine degrees of daylight, one eye. His.");
                waitForMessage();
                egoSay("I mention the Mayor. He develops a deep professional interest in his coaster.");
                waitForMessage();
                actorSay(aideA, "I file things. I don't say them.");
                waitForMessage();
                egoSay("I mention the oil instead. He looks at his glass like it's a co-worker.");
                waitForMessage();
                actorSay(aideA, "The oil up here is too educated.");
                waitForMessage();
                egoSay("Homesick. For the harbor, and for oil that argues back.");
                waitForMessage();
            }
            return;
        }
        if(aideServed && !aideTalked) {            // THE EXPOSÉ
            aideTalked = 1;                        // flag before speech
            cutscene(0) {
                egoSay("He drinks like the harbor's in the glass. For one minute he's a dock bot somebody painted a crest on.");
                waitForMessage();
                actorSay(aideA, "Ask it quiet.");
                waitForMessage();
                egoSay("I ask, quiet, who cancelled the Dynamo's maintenance.");
                waitForMessage();
                actorSay(aideA, "Who signs everything?");
                waitForMessage();
                egoSay("I don't say the name. The paper in my pocket says it in steam-press.");
                waitForMessage();
                actorSay(aideA, "He cancelled the rewind to pay for reassurance. Then needed more.");
                waitForMessage();
                egoSay("Bigger banners, flatter hum. The budget and the Dynamo, winding down together.");
                waitForMessage();
                actorSay(aideA, "Take it to him. Aides can't. Aides file.");
                waitForMessage();
                egoSay("He goes back to his glass. I leave him the rest of the harbor.");
                waitForMessage();
            }
            return;
        }
        if(aideTalked) {
            egoSay("He tips the glass at me a quarter inch. Maximum legal gratitude, for an aide.");
            return;
        }
        if(pourOrdered) {                          // the window filler/hint
            egoSay("He's watching the cellar door the way dock bots watch a ferry.");
            waitForMessage();
            actorSay(aideA, "Bars keep paper. Bars always do.");
            return;
        }
        // escalating hint, second contact (off-path; textually last)
        unless(aideHinted) {
            aideHinted = 1;
            egoSay("He's tilting the house pour and watching it not move. Wrong viscosity. Wrong everything.");
            waitForMessage();
            actorSay(aideA, "You can't get an honest 10W-40 above the funicular.");
            return;
        }
        egoSay("He's reached the bottom of the coaster. Both sides.");
        return;

    case Give:
    case UsedWith:
        if(objB == InventoryItems::poster) {       // productive mistake
            egoSay("I slide the official notice along the bar. NOTHING IS WRONG.");
            waitForMessage();
            egoSay("He goes still the way filing cabinets are still.");
            waitForMessage();
            actorSay(aideA, "Put it away. Walls have aides.");
            waitForMessage();
            egoSay("He drains half the house pour anyway. The half he's been avoiding all night.");
            return;
        }
        if(objB == InventoryItems::workOrder) {
            actorSay(aideA, "I never saw that.");
            waitForMessage();
            egoSay("He says it with his eyes shut. Thorough.");
            return;
        }
        egoSay("He won't take anything with a paper trail. It's a lifestyle.");
        return;

    case Smell:
        egoSay("Primer, and under it, salt. Harbor primer.");
        return;
    }
}
```

### 4.7 The booth, and the furniture

```c
object boothAides {
    case LookAt:
        egoSay("A corner booth of City Hall aides, drinking in formation.");
        waitForMessage();
        egoSay("Every chassis the same civic grey. The paint chart probably calls it Plausible.");
        return;
    case TalkTo:
        unless(heardBoothToast) {
            heardBoothToast = 1;
            cutscene(0) {
                egoSay("I lean on the rail nearby. Casually. The lean has become a discipline.");
                waitForMessage();
                egoSay("They're toasting the new banner. The big one. Readable from the harbor.");
                waitForMessage();
                egoSay("A young one asks which line item the banners come out of. The booth goes quiet on schedule.");
                waitForMessage();
                actorSay(boothA, "Civic reassurance.");
                waitForMessage();
                egoSay("They drink at once, in formation. The question retires.");
                waitForMessage();
            }
            return;
        }
        egoSay("They've moved on to whether NOTHING IS WRONG needs a comma. Careers are riding on the comma.");
        return;
    case Smell:
        egoSay("Civic grey doesn't smell. It's in the spec.");
        return;

object backBar {
    case LookAt:
        egoSay("Single-origin crudes, racked by derrick. Each bottle has a little biography.");
        waitForMessage();
        egoSay("The bottom shelf is dark glass and no biographies. Working oil. Visitors don't ask.");
        return;
    case PickUp:
        egoSay("The sommelier doesn't move. The shelf is somehow already between us.");
        return;
    case Smell:
        egoSay("Crude, in seventeen accents.");
        return;

object cellarList {
    case LookAt:
        egoSay("The cellar list. Single-origins by derrick, vintages by viscosity, prices by audacity.");
        waitForMessage();
        egoSay("At the bottom, in older type: DYNAMO MAINTENANCE — STANDING ORDER.");
        waitForMessage();
        egoSay("Someone has stamped CANCELLED across it. The stamp is the freshest ink on the page.");
        return;
    case Use:
        egoSay("Nothing on it is for me. My warranty cites statutes, and the statutes cite my warranty.");
        return;
    case Smell:
        egoSay("Nothing. It's laminated against exactly me.");
        return;

object oilBarCounter {
    case LookAt:
        egoSay("Amber-lit steel with a mahogany opinion of itself. You could land small aircraft on the polish.");
        return;
    case Use:
        egoSay("I order nothing. The stool and I are both here in a professional capacity.");
        return;
    case Smell:
        egoSay("Nothing escapes the polish. Including smells.");
        return;

object portrait {
    case LookAt:
        egoSay("Mayor Piston, in oils. Recently enlarged.");
        waitForMessage();
        egoSay("The frame didn't keep up. He continues some distance onto the wall.");
        return;
    case Use:
    case PickUp:
        egoSay("It's bolted to the wall. The wall seems resigned.");
        return;
    case Smell:
        egoSay("Oil paint. The one oil in the building nobody will pour.");
        return;

object centrifuge {
    case LookAt:
        egoSay("The house centrifuge, spinning the evening's pour to a shine.");
        waitForMessage();
        egoSay("Round and round goes the sediment, learning nothing.");
        return;
    case Use:
        egoSay("It's at speed. Anything I added would be redistributed. Widely.");
        return;
    case Smell:
        egoSay("Warm crude on a carousel.");
        return;

object cellarHatch {
    case LookAt:
        egoSay("A floor hatch behind the bar, brass-hinged. The cellar: where oil goes to think.");
        return;
    case Open:
    case Use:
        if(pourOrdered && !aideServed) {
            egoSay("Occupied by management. I'd be interrupting a communion.");
            return;
        }
        egoSay("Staff only. The hinges would report me.");
        return;
    case Smell:
        egoSay("Cool air through the seams. Down there it's still last century.");
        return;

object doorOut {
    case LookAt:
        egoSay("The way back to the street. Frosted glass keeps the neon out and the amber in.");
        return;
    case Open:
    case Use:
        // SILENT (room-transition rule)
        putActorAt(VAR_EGO, 130, 120, MidtownRoom);
        startRoom(MidtownRoom);
        return;
```

### 4.8 The work order (inventoryitems.scc)

```c
object workOrder {
    name = "cancelled work order";
    case LookAt:
        egoSay("DYNAMO MAINTENANCE — STANDING ORDER. Weekly, by the barrel, two hundred years.");
        waitForMessage();
        egoSay("Stamped: CANCELLED BY ORDER OF THE MAYOR. Signed in steam-pressed ink, M. PISTON.");
        waitForMessage();
        egoSay("Funds reallocated to CIVIC REASSURANCE. There's a banner swatch stapled to the corner.");
        waitForMessage();
        egoSay("Technician of record: O. CRANK. No forwarding address.");
        return;
    case Use:
        // standard if(objB) UsedWith routing block first (see inventoryitems.scc pattern)
        egoSay("Paper this heavy wants a desk to land on. There's one at City Hall, nine degrees open.");
        return;
    case Smell:
        egoSay("Bar grease over municipal toner. Provenance.");
        return;
    case Preposition: sntcPrepo[0] = "to";
}
```

### 4.9 Casting & talk colors (dub pipeline, NPC-DIALOG §4)

| Speaker | Color | Piper audition | FX |
|---|---|---|---|
| bouncer | 115 | `en_US-danny-low`, pitched down (`asetrate=48000*0.90,aresample=48000`) | light acrusher; slow `--length-scale 1.08` |
| sommelier | 113 | `en_GB-alan-medium`, `--length-scale 1.12` | small plate reverb `aecho=0.6:0.5:40:0.2`, lowpass 6000 |
| aide | 114 | `en_US-hfc_male-medium`, `--length-scale 0.92` | dry, slight tremolo (nervous) |
| booth aide | 114 (shared) or fossil 106 | aide's voice, `-s` variant if libritts fallback | as aide |

New colors join the genassets PAL probes + the scenery-collision build assert; one VP8 probe take before trusting them. Cache-key discipline per NPC-DIALOG §4.5.

---

## 5. Music brief & SFX list

### 5.1 Music — "The Single-Origin Sway" (`build_oilbar` in genmusic.py)

- **Form:** 12 bars, 4/4, swung eighths (reuse `slot_time`/`E_LONG`). **BPM 72** — the slowest theme in the game; uptown never hurries. **Key: B♭ major** (the NOTE table already has Bb).
- **Progression:** `["Bbmaj7","Gm7","Cm7","F7","Bbmaj7","Ebmaj7","Cm7","F7","Dm7","G7","Cm7","F7"]` — loops cleanly back to B♭maj7.
- **Loop point:** `OILBAR_LOOP_BEATS = 12 * 4 + 1 = 49`; room script `imPlayerSetLoop(oilbarSnd, 999, 1, 0, 49, 0)` with the standard watchdog `musicLoop` (docks pattern).
- **Arrangement (GM→FM-safe programs only, per AUDIO.md):** CH_BASS `PRG_BASS 38`, two-feel (root on 1, fifth on 3, long 4/5-beat notes — the alley walk, but content). CH_EP `PRG_EP 4`, lounge backbeat: chord on 2 and 4, velocity ~48 (NOT charleston — that's the theater's; this room sits back where the vamp leans forward). CH_LEAD `PRG_LEAD 80` at velocity ~54, sparse: pickup phrases in bars 4, 8, and 11–12 only — "a lead that orders for you." **No drum channel** (the alley precedent; a lounge with no drummer is the joke and the class).
- **The detuning hum hook (N-A5):** add a pianissimo low B♭1 pedal (CH_EP, velocity ~30, whole notes). When the act-flag pitch-drift work lands in genmusic, this drone is the scene's drift surface (−30 cents late Act 2) — the Dynamo is audible from uptown and it's audible in the room tone. Mark with a TODO comment referencing the N-A5 work item; ship at concert pitch until then.
- **Output:** `assets/generated/audio/oilbar.mid` → `-midi` SOUN flavor (never `-gmd`).

### 5.2 SFX (genaudio.py recipes — 8-bit unsigned mono VOC, one .soun each)

| Name | Recipe (genaudio idiom) | Used at |
|---|---|---|
| `unhook` | brass clip release: `partials(0.05,[(2600,0.7,70),(3900,0.4,90)])` + `silence(0.04)` + velvet whump `mix(partials(0.14,[(95,0.9,26),(160,0.4,34)]), noise_burst(0.03,0.4,110))` ≈ 0.3s | the rope opens |
| `pour` | viscous decant, ~0.9s: three descending glugs — sine bursts at 150/122/100 Hz, each `partials(0.16,[(f,0.8,14),(f*2,0.25,20)])` separated by `silence(0.10)`, laid over faint `noise_burst(0.9,0.10,3)` fizz | the serve |
| `steps` | three wood thuds descending: `partials(0.14,[(130,1.0,26)])`, `(102,...)`, `(80,...)` with `silence(0.18)` gaps + a tail `noise_burst(0.04,0.3,90)` | cellar descent AND return (reused) |
| `paper` | a page off a spike: `noise_burst(0.16,0.35,22)` swish + `partials(0.03,[(2200,0.5,90)])` tick | the grab |
| reused | `clink` (glass down), `creak` (hatch), `pickup` (inventory), `plink` (nothing — not used) | — |

Room `sound` decls: `oilbarSnd, unhookSnd, pourSnd, stepsSnd, paperSnd, clinkSnd, creakSnd, pickupSnd` (unhookSnd also declared in midtown.scc for the rope cutscene).

---

## 6. Walkthrougher beats

### 6.1 Canonical validate shots (append to `full-run.play.yaml`; deploy gate)

```yaml
  # ------------------------------------ Scene 07: the Oil Bar
  - name: a-separate-financial-instrument        # one presentation; the shipped capacity beat
    do: {verb: Use, object: the Oil Bar, with: inventory.slot<voucher>}
    expect: [talking]
  - name: established-as-a-concept
    do: {verb: Examine, object: velvet rope}
    expect: [talking]
  - name: the-rope-participates
    do: {verb: Use, object: velvet rope, with: inventory.slot<voucher>}
    expect:
      - talking
      - pixel: {at: velvet rope, is: brass}      # state 2: unhooked (post pixel)
    timeout: 90
    hold: 2.0
    # NOTE: voucher consumed -> inventory compacts; later slot refs shift
  - name: past-the-rope
    do: {verb: Open, object: the Oil Bar}
    expect:
      - pixel: {at: [160, 10], is: amber}        # interior glow probe
    timeout: 60
  - name: oil-bar-arrival
    cutscene: OilBarRoom.entry
    expect: [talking]
    timeout: 60
  - name: the-folded-memo
    do: {verb: Talk to, object: the aide}
    expect: [talking]                            # speaker assert: aide color 114
    timeout: 60
  - name: the-sommelier-of-crude
    do: {verb: Talk to, object: oil sommelier}
    expect: [talking]                            # speaker assert: somm color 113
    timeout: 60
  - name: the-order                              # B2 dialog primitive
    do:
      - {verb: Talk to, object: oil sommelier}
      - {dialog: "Something dock-aged. A working 10W-40."}
      - {dialog: "The Dynamo maintenance account."}
    expect:
      - talking
      - pixel: {at: oil sommelier, is: backbar-wood}   # figure absent
    timeout: 120
  - name: certified-archival-work
    do: {verb: Use, object: receipt spike}
    expect:
      - talking
      - pixel: {at: inventory.slot<workorder>, is: white}  # the page
      - pixel: {at: oil sommelier, is: somm-black}         # he's back
    timeout: 120
    hold: 1.5
  - name: walls-have-aides                       # the exposé
    do: {verb: Talk to, object: the aide}
    expect: [talking]
    timeout: 90
    hold: 2.0
```

(Validate-mode speaker assertions ride the NPC-DIALOG step-3 machinery: each actorSay segment must classify as its speaker's color.)

### 6.2 Streamer-mode detours & mistakes (`only: perform`; the refusal line IS the assertion)

| Shot | Type | Action | Expected beat |
|---|---|---|---|
| `the-list-is-a-door` | mistake | Open the Oil Bar pre-rope | picture-of-the-door gag (shipped) |
| `all-access-meets-rope` | mistake | Use backstage pass with the Oil Bar | "That opens a door. This is a rope." |
| `professionally-agreed` | mistake | Use poster with the Oil Bar | "Agreed." |
| `redeemed-separately` | detour | second voucher presentation to bouncer | the escalation hint |
| `velvet-all-the-way-down` | detour | Smell velvet rope | escalating-list gag |
| `the-house-portrait` | detour | Examine portrait | frame-overflow gag |
| `learning-nothing` | detour | Examine centrifuge | — |
| `drinking-in-formation` | detour | Talk to booth of aides | "Civic reassurance." |
| `the-comma` | detour | Talk to booth again | comma careers |
| `too-educated` | mistake | dialog: "Your finest single-origin." | aide refuses Derrick Nine |
| `not-touching-it` | mistake | dialog: "Another round of the house pour." | "He hasn't touched it in an hour." |
| `no-ancestors` | mistake | dialog round 2: "My tab." | "Tabs here are inherited, not opened." |
| `settles-in-banners` | mistake | dialog round 2: "City Hall's tab." | the motive leak |
| `walls-have-aides-early` | mistake | Use poster with the aide (pre-pour) | "Put it away. Walls have aides." |
| `sommelier-thing` | mistake | Use receipt spike (sommelier present) | the three-eyed refusal |
| `staff-only` | detour | Open cellar hatch | hinges would report |
| `the-dossier` | detour | Examine cancelled work order | the 4-card evidence read incl. O. CRANK |
| `maximum-legal-gratitude` | detour | Talk to aide after the exposé | quarter-inch toast |

The streamer screenplay plays the contest wrong-first (single-origin → house pour → win), per the production plan's streamer doctrine: get the gag, then find the answer.

---

## 7. Planted / paid ledger

**Consumes (pays off):**

| Plant | Source | Paid here by |
|---|---|---|
| oilVoucher + both its self-descriptions ("participating establishments", "saving it for somewhere with a rope") | Scene 05 prize; N-M3/N-M4 dispositions | P1 — spent on the rope, the GDD's exact promise |
| "The rope is a separate financial instrument" / "at capacity" | midtown N-M4 fix | confronted and defeated; capacity was the rope's grievance |
| backstagePass Use line ("opens exactly one door") | inventoryitems | the bouncer mistake beat |
| The aide who feared the poster (door opened nine degrees) | midtown cityHall:UsedWith(poster) | he recognizes Sprocket: "You're the one with the paper." |
| NOTHING IS WRONG banners (board, City Hall, poster) | Scenes 01/04 | the banner budget IS the cover-up's cost center |
| Sprocket's palate/scent library ("Mmm. Zinc-plated.", esters line) | Scenes 01–02 | tasting-room comedy stands on established hardware |
| The casual-lean runner | tavern rustlersTable | one echo ("the lean has become a discipline") — second use, at budget |
| GDD Act 2 sentence ("the oil voucher gets Sprocket past the velvet rope, where City Hall drinks and talks") | GDD | executed in full |

**Creates (plants), with scheduled payers:**

| Plant | Pays where | Status |
|---|---|---|
| `workOrder` item (signature, banner reallocation) | Scene 08 — the confrontation lever; its Use line points only at City Hall | SCHEDULED (production row 08) |
| "Technician of record: O. CRANK" | Scene 10 — Old Crank IS Key #3; first on-screen name (N-A10 duty) | SCHEDULED (production row 10) |
| "Take it to him. Aides can't. Aides file." | Scene 08 directive | SCHEDULED |
| "Civic reassurance" + the comma debate | Scene 08 Piston bluster material | SCHEDULED |
| The aide as sympathizer (knows Sprocket has the paper) | Scene 08, optional: the door opens all nine degrees | scheduled-optional; phrased non-promissory (no named missing item — N-T3 lesson) |
| The cellar / "down there it's still last century" | none — pure texture, no item named | deliberately closed |

No new unscheduled item promises. Audit: no line in the scene names an object that doesn't exist or isn't scheduled.

---

## 8. Embodiment audit (self-audit of this text)

**Power model (the ledger rule):** the hum winds every mainspring on the island remotely; hand-winding is the crude off-warranty backup. This scene makes **zero** power claims: drinking oil is *lubrication culture*, never recharge — the aide drinks for nerve and homesickness, the booth drinks socially, nobody "refuels." No line says "low-power," no one winds anything. The one hum reference ("flatter hum", exposé) is about the Dynamo itself, consistent with canon. ✓

Line-by-line items:

1. **Sprocket doesn't drink** — preserved and re-stated twice in-register (warranty statutes); he orders *for* the aide. Consistent with tavern canon ("my warranty names additives by statute number"). ✓
2. **The sommelier "listens to" crude** — grounded: viscosity is audible (glug rate); a decanting specialist auditing pour-sound is real physics played straight, same class as the gate's worn-bolt gauge. ✓
3. **No blushing robots** — the aide "goes still the way filing cabinets are still" (chosen over any color-change idiom; paint doesn't blanch). His relaxation is "by one rivet" — mechanical. ✓
4. **Recognition is asymmetric and sighted:** the aide saw Sprocket *through* the nine-degree gap (one eye looking out sees the whole street); Sprocket only ever saw an eye, so he identifies the aide by the **fresh City Hall crest** plus the aide's self-identification — never by the eye. ✓
5. **Why the bar holds the evidence:** the Oil Bar was the *supplier* on the standing order; a supplier keeps its copy of the cancellation it was served. The spike is the bar's own paper history, oldest at the bottom — the document's location is load-bearing, not convenient. ✓
6. **"Steam-pressed ink"** — Piston is canonically steam-powered; his signature medium is in-fiction consistent (and plants his physiology for Scene 08's "steam-powered bluster"). ✓
7. **Prop continuity:** the work order is one page plus a stapled banner swatch — pocketable, drawn as a paper icon; the voucher visibly leaves inventory at the rope (compaction modeled in the screenplay); the spike loses a visible page (state 2). ✓
8. **Geometry:** cellar under the bar with a painted hatch (the descent has a door, a sound, and a duration); the rope has two painted states; the sommelier's absence is a painted state, not a vanishing; the booth, portrait, centrifuge all exist in GEOM before any line mentions them (no theater-catwalk regression). ✓
9. **Count discipline:** no exact counts on countable art — "in formation," "seventeen accents" (smells aren't drawn), "two hundred years" (off-screen history, where exact numbers are allowed per the embodiment dispositions). ✓
10. **Smell lines:** all five new Smell verbs avoid the banned `[material] and [abstract]` template — shapes used: escalating recursion (rope), sensor-can't-parse (list, booth grey, counter), flat fact (centrifuge, spike), material-with-provenance (aide's "harbor primer," which does story work). One "and" construction ("Primer, and under it, salt") is material+material with a payload, not the zeugma. ✓
11. **Sound claims:** "from below the floor: the sound of a bottle being judged" — there IS sound below the floor (steps SFX, decanting); the wit is in the attribution, not an invented sense. The cellar's "sighing" is the hatch's air seam, established by the hatch's own Smell line. ✓

---

## 9. Implementer's pitfall checklist (engine notes, all from docs/NOTES.md + NPC-DIALOG)

1. **Verb ids:** use only common.sch's pinned verbs; no new verbs needed.
2. **Owner semantics:** "in pocket" = `getObjectOwner(x) == VAR_EGO`; voucher consumption = `setObjectOwner(x, 0)` (owner 0, never "false-y" checks — sld fills unset owners with 0x0F).
3. **Dub source order:** branch order inside each handler is canonical-chronological first, off-path after — the orders written in §4 are normative (aide: intro → exposé → after → window → hint; sommelier: intro → dialog → fillers; spike: grab first). Mixed egoSay/actorSay lines in one handler extract as ONE interleaved ordered list.
4. **Silent transitions:** oilBar→OilBarRoom and doorOut→Midtown say NOTHING; all arrival flavor is in entry scripts.
5. **Story flags before

9. **Implementer's pitfall checklist (continued)**

5. **Story flags before speech:** `ropeOpen`, `pourOrdered`, `aideServed`, `aideTalked` are all set at the *top* of their cutscenes (concurrency rule), as written in §4.
6. **Speaking actors in-room:** `putActorAt` for `bouncerA` in MidtownRoom's entry and for `sommA`/`aideA`/`boothA` in OilBarRoom's entry, before any line — actorTalk drops/mis-renders lines for actors not in the room.
7. **Inventory compaction:** the voucher is consumed mid-scene; every later `inventory.slot<N>` expectation in the screenplay must model the shift (the ScummVM compaction rule).
8. **The centrifuge flicker loop** is the signFlicker bug class — pair every `startScript` with a stop on room exit, and gate any future flap on `VAR_HAVE_MSG`.
9. **Dialog-tree re-entry:** re-TalkTo reopens at round 1; a mid-tree exit must `dialogClear` (the dialog.scc plumbing's responsibility) so stale options never linger.
10. **genassets additions:** OilBarRoom art (320×144 amber; teal neon visible through the frosted door glass for palette continuity), GEOM entries per §3, three 2-state objects (rope, sommelier figure, spike), `inv_workorder.bmp`, talk-color probes 113/114/115 + the scenery-collision assert, stage-map export.
11. **soun rules:** music is `-midi` flavor only; the four new SFX are 8-bit unsigned mono VOC; one .soun = one thing; never `-spk`.
12. **Editorial gate:** this text faces the five-chair desk before validate; the scene ships with zero open BLOCKERs, and the streamer screenplay's mistake shots assert the refusal lines verbatim.

**Known tensions to flag for the desk (pre-declared):**
- The aide's escalation line names "10W-40" on second contact — deliberate escalating-hint policy (N-A2 disposition pattern), not first-contact answer-naming.
- "Too educated." appears twice (aide intro + flop callback) — an intentional 2-use runner, under the 3+ threshold.
- The bouncer is the size of a vending machine and is written to *want* nothing — his want is the rope's dignity, which is the joke; if the desk reads him as a vending-machine NPC, the defense is that he's a *lawyer*, and the player beats him at law.

---

**END OF DESIGN DOC** — Scene 07 "The Oil Bar, Inside" / *A Separate Financial Instrument*. Sections: (1) goal+spine, (2) puzzle graph P1–P6 with fair-play audit and the two-round playable contest, (3) object table with rects on the 320×144 stage, (4) complete dialog draft (every line written, branch order normative), (5) music brief (12 bars, 72 BPM, B♭ major, loop beat 49) + 4 SFX recipes, (6) validate shots + streamer detours/mistakes, (7) planted/paid ledger, (8) embodiment audit, (9) implementation checklist. Source files read: `/Users/matthewbaker/clankeyisland/docs/PRODUCTION-PLAN.md`, `docs/GDD.md`, `docs/NOTES.md`, `docs/editorial/CHARTER.md` + all three reports, `docs/research/NPC-DIALOG.md`, `docs/research/NARRATION.md`, `docs/WALKTHROUGHER.md`, `game/{tavern,theater,midtown,alley,inventoryitems}.scc`, `game/common.sch`, `tools/{genmusic,genaudio}.py`, `walkthrough/screenplay/full-run.play.yaml`. Intended landing path: `/Users/matthewbaker/clankeyisland/docs/scenes/SCENE-07.md` (file not written per subagent contract — parent should write this output there).