I've read the production plan, GDD, NOTES, the full editorial corpus (CHARTER + both desk passes + the embodiment sweep), NPC-DIALOG.md, and the tavern/theater/midtown/docks/alley/inventory sources. Here is the complete design doc.

---

# SCENE 08 — CITY HALL: MAYOR PISTON
### `docs/scenes/SCENE-08.md` — design doc for implementation (Wave 1 deliverable)

New room: `CityHallRoom` (`game/cityhall.scc` + `game/cityhall.sch`), plus edits to `game/midtown.scc` (the City Hall door pays off) and `game/inventoryitems.scc` (two items). Art: `tools/genassets.py` `CITYHALL_GEOM` + `draw_cityhall`. Music: `tools/genmusic.py` third song. SFX: `tools/genaudio.py` five new recipes.

---

## 1. Scene goal & how it advances the three-keys spine

**Goal:** The cover-up collapses in private while surviving in public. Sprocket walks in with paper (the official notice he has carried since Scene 01, plus the Oil Bar tab from Scene 07) and walks out with the **Rustlers' ransom note** — the letter that turns the locked tavern back door from a gag ("Act Three, buddy") into a destination. Mayor Piston converts from banner-shaped obstacle to the game's most compromised ally: he knows the Dynamo is failing, he knows the Order is gone, and he cannot be seen knowing either.

**Spine advancement, key by key:**
- **Key #1 (stolen at the heist):** the ransom note is the recovery path. It names the Scrap & Barrel back door and notates the knock — the **forced critical-path echo of the 2-1-2 knock-code** before Act 3 (the second echo; Voltina's Scene 06 echo is the first — redundancy is intentional, this one is on the validate path and unmissable).
- **Key #2 (Voltina's):** untouched here; no dependency in either direction (see §3 interfaces).
- **Key #3 (Old Crank):** second plant, from a new angle — the Order's pension list has one name left, deliveries go up the hill. Scene 06 plants "the key that winds itself"; Scene 08 plants "the last Order bot lives past the fence." Neither says the twist.
- **The clock (editorial N-A5):** Piston states the deadline from authority: the engineers gave the Dynamo three days, two days ago. Act 3 is the last day. (Arithmetic against the GDD logline: prognosis issued the day before Sprocket's arrival → arrival day + Act 2 day + final day = the GDD's three days of story. The detuning hum gets its first scripted on-screen sag here, mid-confrontation.)
- **NPC wants (editorial N-A6):** Piston wants the lid kept on AND the problem solved, deniably — a want that persists into Act 3. Caliper wants his signature back. Neither is a vending machine; both oppose before they assist.

---

## 2. Canon obligations checklist (from the brief)

| Obligation | Where it lands |
|---|---|
| The official notice pays off | Round 1 of the confrontation: laid on the blotter, stamped VOID — "Now it's official twice." Item survives with a new LookAt state. |
| The nine-degrees aide | Named (**Caliper**, protractor lapel pin), pays off geometrically: the bar tab opens "the other eighty-one degrees." Degrees become the scene's running unit. |
| Piston's steam physiology obeys the power model | Stated once, at his LookAt: *"The hum winds him like everybody. The steam is just the oratory."* Boiler = actuation/voice; mainspring = the hum's spring-bank, like every bot per the docks board lecture. The brownout beat is built on this (§11 full audit). |
| Outcome positions Act 3 | He knows the Dynamo is failing (confesses the three-day prognosis), knows about the Order (pension list → Old Crank plant, fence plant for Scene 10), and hands over the ransom note (Scene 09's door-opener). |
| Confrontation is playable | Three-round evidence/dialog duel via the `dialog.scc` UI (B2+B8 plumbing). §4. |

---

## 3. Interface contracts with adjacent scenes (parallel-design declarations)

**Consumes from Scene 07 (Oil Bar interior) — REQUIRED:**
- Flag `heardAides` — Sprocket overheard City Hall's aides talking inside the Oil Bar.
- Item `InventoryItems::barTab` — a tab charged to **"DYNAMO MAINT. — CONTINGENCY"**, signed **Caliper**. Scene 08 specifies this item fully (§6, §7.8) so either doc can own it; if Scene 07's designer ships a different evidence prop, the implementer maps the id and keeps the two facts it must carry: (1) a maintenance budget line that officially doesn't exist, (2) Caliper's signature. Scene 07 should let Sprocket *keep* the tab and point it at City Hall (the item's Use line does this; a spoken beat in the bar is better).

**Consumes from Scene 06 (Voltina) — SOFT:** nothing gated. If Voltina's fortune wants to breadcrumb this scene, the cheapest line is motive-shaped: the ransom needs a recipient — *ask the bot who got the bill.* Not required; the bar tab's Use line and the City Hall door both point here independently.

**Produces for Scene 09 (hideout):** `pistonCracked` flag + `InventoryItems::ransomNote` (carries the 2-1-2 knock notation and "WE HAVE THE FIRST KEY"). Scene 09 may additionally check `heardKnockCode` (already validate-path since B9).

**Produces for Scene 10 (Dynamo District / Old Crank):** two spoken plants — the pension list with one name, deliveries up the hill — and the curtained window's dust clue (Piston privately watches the Dynamo). No flag needed; Scene 10 may quote the pension list.

**Does NOT consume:** the oil voucher (Scene 07's business), Key #2, the backstage pass.

---

## 4. Puzzle chain — numbered graph, fair-play audit, agency beat

```
 [S01: poster taken]──────────────────────────────┐
 [S04: aide opens door 9°; poster → closes 8 of 9]│
 [S07: heardAides + barTab]──────┐                │
                                 v                v
 (1) midtown: Use barTab on City Hall ──> door opens the other 81°
                                 │         (cityHallOpen = 1)
                                 v
 (2) Open City Hall ──> CityHallRoom (silent transition; entry cutscene)
                                 │
 (3) optional recon (each plants a later beat):
     LookAt gauge      ──> "graduated in mainspring turns"   [plants R3]
     LookAt desk       ──> "crank handle worn shiny"         [plants R3]
     LookAt window     ──> dust on velvet, none on cord      [character clue]
     TalkTo Caliper    ──> "Arguments need a second participant."  [R3 KEY HINT
                            — promoted onto the validate path, B9-style]
                                 v
 (4) TalkTo Piston ──> intro cutscene ──> DIALOG TREE (the Denial Duel)
       ROUND 1  denial: "Nothing is wrong. It's on every banner."
         flop A: "The Dynamo is flat by half a step."
         flop B: "Rivet says otherwise."
         WIN   : "Show him his own notice."        [evidence: poster]
                  → poster stamped VOID (posterVoided)
       ROUND 2  denial: "Maintenance is budgeted at zero."
         flop A: "The curtains disagree."           [rewards window recon]
         flop B: "Zero is a suspicious number."
         WIN   : "Show him the bar tab."            [evidence: barTab]
       ROUND 3  scripted brownout: hum sags, gauge dips, his hand
                drifts to the crank dock
         flop A: "Offer him a wind. Professionally."
         flop B: "Point at the gauge."
         WIN   : "Say nothing."
                                 v
 (5) confession cutscene: three days / two days ago; the Order pensioned
     off, one name left, up the hill; the ransom note (2-1-2 knock);
     pickup ransomNote; pistonCracked = 1
                                 v
 [Act 3 / Scene 09: ransomNote + knock-code open the hideout chain]
```

**Fair-play audit — every hint, named source:**

| Move | Hint(s), with on-screen source | Status |
|---|---|---|
| (1) barTab opens the door | barTab Use line: "It's a City Hall expense. Somebody at City Hall should really see it." (item's own authoritative text, the N-I1 lesson applied); Scene 07's aides scene (interface); NEW midtown door line after the poster beat: through the one-degree gap, "lamplight and the smell of single-origin crude" → "Municipal aides drinking the good stuff. On whose tab, I wonder." (scent already established as the Oil Bar's signature in `midtown.scc:oilBar:Smell`; Sprocket's precision nose is established canon) | 3 sources, one in-scene; no lock names its key verbatim (N-A2 compliant — none of them say "tab") |
| R1 win (the notice) | The poster's own LookAt has taught its logic since Scene 01 ("Nothing says 'something is wrong' like an official notice that nothing is wrong") — on the validate path via the `civic-duty` shot; the duel option is literally "show him" the thing the player has carried for two acts | Fair; the player owns this inference already |
| R2 win (the tab) | The tab got the player through the door 60 seconds earlier — its power over City Hall is demonstrated, not asserted; Caliper's signature was named at the door cutscene | Taught by play, the strongest kind of signpost |
| R3 win (silence) | Caliper, in-scene, on the validate path: "Arguments need a second participant."; the gauge LookAt ("graduated in mainspring turns") + desk LookAt ("crank handle worn shiny") make the tell legible; the brownout beat narrates the tell ("his hand drifts toward the crank dock"); precedent: the riddle duel's "He pays the bolt without a word" taught silence-as-victory in Act 1 | Three in-scene plants, one of them forced; the two flops are near-misses that re-fire the round (no loss state) |
| Guaranteed evidence | Poster: duel-gated since the N-L3 fix (held by every player who reached Midtown). barTab: it's the door key, and Sprocket explicitly takes it back at the door ("Evidence keeps.") — no missing-evidence dead end is reachable | No soft-lock |

**The playable-agency beat (charter mandate: THE CONTESTS MUST BE PLAYABLE):** the Denial Duel is a real contest — three rounds, three choices each, two of which go wrong *funny* (and stay available for the streamer to mine), winner gated on the player's read of the room, with one evidence-presentation per round and a final round whose answer is the deadpan thesis of the whole game: trust the gap. It cannot be lost (flops loop with escalating brush-offs), it cannot be won by clicking everything once (flops return to the menu; the menu doesn't shrink), and the player authors the crack — the loss of Key #1 landed on Sprocket (B8's complaint), the cracking of Piston lands on the player. Requires the B2+B8 dialog plumbing, which the production plan sequences before any Scene 06-08 implementation.

**Shape variety check (N-A1):** beat 1 is item-on-door, beat 4 is a dialog contest with embedded evidence presentation, beat 3 is optional environmental reading that changes how beat 4 reads. No fetch. The scene contains zero new "use single item on single hotspot, receive item" links.

---

## 5. Object table — `CityHallRoom`, 320×144 stage

Layout (left → right): exit door | Caliper's desk + Caliper | portrait gallery over the banner stack | curtained window | gauge, big desk, Piston. Sprocket enters at (24,120), walkbox floor band y≈108–134.

```
y=0   ┌────────────────────────────────────────────────────────────────┐
      │        [portraits 96,8 72x40]   [window 176,8 40x44]           │
      │ [door                                        [gauge 224,28     │
      │  4,56                                          20x24]          │
      │  24x48] [caliper 48,52 20x44]            [piston 240,40 44x56] │
      │         [aideDesk 40,84 48x28] [bannerStack    [mayorDesk      │
      │                                 104,96 40x24]   196,84 92x36]  │
y=143 └────────────────────────────────────────────────────────────────┘
```

| # | Object | Rect (x,y,w,h) | dir | class | Verbs handled | States |
|---|---|---|---|---|---|---|
| 1 | `doorOut` — "door to the street" | 4,56,24,48 | EAST | Openable | LookAt, Open/Use (silent → MidtownRoom, put ego at 276,120) | 1 |
| 2 | `caliper` — "Caliper" | 48,52,20,44 | SOUTH | Person | LookAt, TalkTo, Smell, Give/UsedWith | 1 (Tier-A actor for speech) |
| 3 | `aideDesk` — "aide's desk" | 40,84,48,28 | NORTH | — | LookAt, Use, Smell | 1 |
| 4 | `portraits` — "portrait gallery" | 96,8,72,40 | NORTH | — | LookAt, PickUp/Use, Smell | 1 |
| 5 | `bannerStack` — "spare banners" | 104,96,40,24 | NORTH | — | LookAt, PickUp, Use, Smell | 1 |
| 6 | `windowDynamo` — "curtained window" | 176,8,40,44 | NORTH | Openable | LookAt, Open/Use, Smell | 2: curtains closed / open (open reveals the Dynamo, painted small) |
| 7 | `gauge` — "civic gauge" | 224,28,20,24 | NORTH | — | LookAt, Use/Move, Smell | 2: needle high / needle low (brownout + post-crack) |
| 8 | `mayorDesk` — "the Mayor's desk" | 196,84,92,36 | NORTH | — | LookAt, Use, Smell | 1 (crank dock + VOID stamp painted in) |
| 9 | `piston` — "Mayor Piston" | 240,40,44,56 | SOUTH | Person | LookAt, TalkTo, Smell, Give/UsedWith | 1 painted figure + 2-state stack-puff overlay (the room's animating element) |

**Midtown edits** (existing `cityHall` object, 240,32,72,72): Use gains a `cityHallOpen` silent-transition branch (FIRST in source) and a post-poster breadcrumb branch; UsedWith gains the `barTab` branch; UsedWith poster sets new flag `showedNotice`; LookAt gains post-open and post-crack branches.

**Art notes:** marble paint over sheet metal (the entry line is checkable — keep the seams visible); Piston's stovepipe stack puffs on a 2-state `setObjectState` loop, signFlicker-style — **mind the stopScript/signFlicker bug class** (kill the loop inside cutscenes that reposition him, restart after). Gauge needle is two drawn states, not a claim the text makes against static art (the marquee-bulb lesson). The window's open state paints the Dynamo small and distant — Midtown already establishes line-of-sight from street level, and City Hall is uphill-adjacent on the same street.

---

## 6. New items, flags, actors

**Items (`inventoryitems.scc`, with the standard `Use`→`objB` routing boilerplate and `Preposition` cases):**

- `barTab` — "Oil Bar tab" (icon: `inv_bartab.bmp`, parchment-yellow so pixel probes distinguish it from the white poster/note). *If Scene 07 ships it, that doc's lines win; these are the fallback spec.*
- `ransomNote` — "ransom note" (icon: `inv_ransom.bmp`, white with a red smudge — probe-distinct).

**Flags (`cityhall.sch` unless noted):** `visitedCityHall`, `pistonRound` (int: 0 none / 1 / 2 / 3 / 4 cracked), `pistonCracked` (bit, == pistonRound 4, kept as a bit for other rooms to test cheaply), `posterVoided`, `curtainsOpen`. In `midtown.sch`: `cityHallOpen`, `showedNotice`. From Scene 07 (`oilbar.sch` or wherever 07 puts it): `heardAides`.

**Actors (NPC-DIALOG Tier-A, costume-less):** `piston_a` talk color **PAL[113]** (brass gold), `caliper_a` talk color **PAL[114]** (cool slate) — next free slots after the 108–112 batch; both need the hue/luma VP8 probe take before trust, and the scenery-collision build assert. `putActorAt` both in `CityHallRoom.entry` (Piston at 262,96; Caliper at 58,96); **Caliper must also be `putActorAt` into MidtownRoom** before his one door line (the actorTalk not-in-room landmine). Dub CAST: Piston = `en_GB-alan-medium`, `--length-scale 1.12`, pitched down (`asetrate=48000*0.9,aresample=48000,atempo=1.11`), low-shelf boost + a short plate — pompous, resonant; Caliper = `en_US-joe-medium`, `--length-scale 0.92`, dry + gentle high-pass — thin and precise. New synth args join the cache key.

---

## 7. Full dialog draft

Register rules applied throughout: Sprocket reports; NPCs get direct punchlines ≤12 words (counts verified); no double-telling; no self-grading; no `[material] and [abstract]` smell zeugmas (shapes used: flat fact, escalating list, sensor-can't-parse); no Sprocket act-naming; **walkthrough-path branches FIRST in source within every handler** (dub pairing); room transitions say nothing.

### 7.1 Midtown — `cityHall` object (edits)

```
LookAt:
  if (pistonCracked):
      egoSay("City Hall. The banner still says NOTHING IS WRONG.");
      egoSay("It's true now, in the sense that it's a work order.");
  else if (cityHallOpen):
      egoSay("The door stands open. The banner over it hasn't been told.");
  else:  [existing two lines unchanged]

Open / Use:
  if (cityHallOpen):
      // silent transition — FIRST in source
      putActorAt(VAR_EGO, 24, 120, CityHallRoom); startRoom(CityHallRoom);
  else if (showedNotice):
      egoSay("The gap is one degree now. Through it: lamplight, and single-origin crude.");
      egoSay("Municipal aides drinking the good stuff. On whose tab, I wonder.");
  else:  [existing two aide lines unchanged]

UsedWith:
  if (objB == barTab) and not cityHallOpen:
      cutscene:
        egoSay("I post the bar tab through the gap, signature side first.");
        egoSay("Silence. Then the sound of a door rethinking its angle.");
        startSound(creak9Snd);
        [setObjectState if the door gets an open state in art]
        egoSay("The door opens the other eighty-one degrees.");
        actorSay(caliper_a, "You never showed me that.");                    // 5 words
        egoSay("Shown, he means, to the Mayor. We understand each other.");
        egoSay("I take the tab back. Evidence keeps.");
      cityHallOpen = 1;   // flag set at branch top per story-flags-before-speech rule
  if (objB == barTab) and cityHallOpen:
      egoSay("It already opened the door. Now it has an appointment upstairs.");
  if (objB == poster):
      showedNotice = 1;   [then the existing three lines unchanged]
```

### 7.2 `CityHallRoom.entry` (first visit)

```
cutscene(2):
  putActorAt(VAR_EGO, 24, 120); walkActorTo(70, 124);
  egoSay("City Hall, inside. Marble paint over sheet metal. The echo is load-bearing.");
  egoSay("A hallway of portraits, a desk of stamps, and at the end: the Mayor.");
  egoSay("You can hear him from here. He sounds like a kettle that won committee.");
  egoSay("Caliper follows at exactly arm's length. He measured.");
```

### 7.3 `caliper`

```
LookAt:
  egoSay("Caliper. The aide who rations doors by the degree.");
  egoSay("His lapel pin is a protractor. Of course it is.");
TalkTo (first):
  egoSay("I ask how a bot ends up dispensing angles for a living.");
  egoSay("Doors are budget items, he says. Every degree has a cost center.");
TalkTo (second+, pre-crack)  — THE ROUND-3 PLANT, validate path:
  egoSay("I ask about the Mayor. He says the Mayor has never lost an argument.");
  actorSay(caliper_a, "Arguments need a second participant.");               // 5 words
  egoSay("His protractor pin catches the light.");
TalkTo (post-crack):
  egoSay("He's drafting the next notice. The word NOTHING is doing a lot of work in it.");
Smell:
  egoSay("Ink pads. Three colors. All of them red.");
Give/UsedWith poster:
  egoSay("He's seen it. Eight degrees' worth.");
Give/UsedWith barTab:
  egoSay("He looks at the signature, then at the middle distance, where his career is.");
default Give/UsedWith:
  egoSay("He files it under RETURNED, UNFILED, and returns it.");
```

### 7.4 `aideDesk`

```
LookAt:
  egoSay("A desk defended by rubber stamps. RECEIVED. DECLINED. DECLINED HARDER.");
Use:
  egoSay("I reach for a stamp. Caliper produces a form for requesting forms.");
Smell:
  egoSay("Endorsing ink. The desk has opinions it's allowed to publish.");
```

*(One "with opinions" exists in the game, on the Dynamo's fence; this is "opinions it's allowed to publish" — a different machine. If the desk objects, cut to "Endorsing ink. Fresh pad." )*

### 7.5 `portraits`

```
LookAt:
  egoSay("Mayors Piston the First through Fourth. The same boiler, different dents.");
  egoSay("Four portraits, one paint job between them. Municipal continuity.");
PickUp / Use:
  egoSay("Bolted to the wall. Somebody anticipated me, four mayors ago.");
Smell:
  egoSay("Varnish. Recent. History gets refreshed here on a schedule.");
```

### 7.6 `bannerStack`

```
LookAt:
  egoSay("Spare banners, rolled and racked. NOTHING IS WRONG, in every size down to lapel.");
  egoSay("There's a fresh crate of them. Confidence has a reorder point.");
PickUp:
  egoSay("The small ones are lapel-sized. My lapel declines.");
Use:
  egoSay("I don't need a banner. I'm carrying the rebuttal.");
Smell:
  egoSay("Fresh ink. The same suspicious vintage as my notice.");
```

### 7.7 `windowDynamo`

```
LookAt (curtains closed):
  egoSay("One window, floor to ceiling, curtained shut. It faces the Dynamo District.");
  egoSay("Dust on the velvet. None on the pull cord. Somebody checks, then closes them again.");
LookAt (open):
  egoSay("The Dynamo fills the window. From this office you can't not see it.");
Open / Use (closed):
  startSound(creakSnd); setObjectState(windowDynamo, 2); curtainsOpen = 1;
  egoSay("I pull the cord. The Dynamo, up the hill, framed like a portrait nobody commissioned.");
Open / Use (open):
  egoSay("It's seen. That was the whole job.");
Smell:
  egoSay("Velvet. Underneath it, ozone off the hill.");
```

### 7.8 `gauge`

```
LookAt (pre-crack, needle high):
  egoSay("A brass gauge on the desk, labeled CIVIC OPTIMISM. The needle says plenty.");
  egoSay("The dial behind the label is graduated in mainspring turns.");
LookAt (post-crack, needle low):
  egoSay("Relabeled in pencil: RESERVE. The needle has stopped pretending.");
Use / Move:
  egoSay("Wired through the desk and into the Mayor's chair.");
Smell:
  egoSay("Brass polish and pencil shavings.");
```

### 7.9 `mayorDesk`

```
LookAt:
  egoSay("A desk you could dock a ferry at. One blotter, one stamp, one crank dock on the side.");
  egoSay("The crank handle is worn shiny.");
Use:
  egoSay("The stamp says VOID. A whole desk, organized around one word.");
Smell:
  egoSay("Warm metal. The desk sits downwind of a boiler.");
```

### 7.10 `piston` — LookAt / Smell / item verbs

```
LookAt (pre-crack):
  egoSay("Mayor Piston. A boiler in a sash. The pressure does his gesturing for him.");
  egoSay("The hum winds him like everybody. The steam is just the oratory.");
LookAt (post-crack):
  egoSay("He's down to working pressure. It suits him.");
Smell:
  egoSay("Coal smoke. He precedes himself.");
Give/UsedWith poster (outside the tree, pre-crack):
  egoSay("He waves it at the visitor's chair. Appointments are conducted seated.");
  egoSay("Fine. We'll do this with words first.");
Give/UsedWith poster (posterVoided):
  egoSay("Already stamped. The desk only escalates to ignoring.");
Give/UsedWith barTab (outside the tree):
  egoSay("Paper goes through channels. The channel is me, talking. So: talking.");
default Give/UsedWith:
  egoSay("He takes nothing by hand. Hands are for gesturing.");
```

### 7.11 The confrontation — `piston:TalkTo`

**Intro cutscene (pistonRound == 0 → 1):**

```
egoSay("He's mid-speech when I reach the desk. There's no audience. He doesn't need one.");
actorSay(piston_a, "Ah. The talent. Tremendous act. The city thanks you.");        // 9 words
egoSay("I mention the robbery. He calls that 'the magic of live theater'.");
egoSay("I put it to him straight: the Dynamo is dying and the city is lying.");
actorSay(piston_a, "Nothing is wrong. It's on every banner.");                      // 7 words
→ open ROUND 1 menu
```

**Re-entry (TalkTo while pistonRound 1–3, after leaving):**

```
actorSay(piston_a, "Back for more civics?");                                        // 4 words
→ reopen current round's menu (Round 3 re-fires the brownout beat first)
```

**ROUND 1 menu** (dialogAdd strings, ≤40 chars):
1. `The Dynamo is flat by half a step.`
2. `Show him his own notice.` ← **winner**
3. `Rivet says otherwise.`
4. `I withdraw to regroup.` (leave: `egoSay("I withdraw to regroup. The banners watch me go.");` — dialog ends, resumable)

```
Option 2 (WINNER — source-order FIRST in the round's block):
  egoSay("I unfold the official notice on his blotter. NOTHING IS WRONG. His signature.");
  actorSay(piston_a, "Standard reassurance. We issue them on a schedule.");          // 8 words
  egoSay("I ask what the schedule reassures us about, if nothing is wrong.");
  startSound(steamSnd);
  egoSay("Steam escapes from somewhere official.");
  actorSay(piston_a, "Caliper. The stamp.");                                         // 3 words
  startSound(stampSnd);
  posterVoided = 1;
  egoSay("He stamps my notice VOID, with feeling. Now it's official twice.");
  actorSay(piston_a, "Maintenance is budgeted at zero. Because nothing needs maintaining."); // 9 words
  pistonRound = 2;  → ROUND 2 menu

Option 1 (flop):
  egoSay("I tell him the hum is flat. By half a step.");
  actorSay(piston_a, "Retuned. By request. The city prefers a softer key.");         // 9 words
  egoSay("The city is built in C. I let it go. For now.");
  [repeat pick]: actorSay(piston_a, "Still retuned. Still by request.");             // 5 words
                 egoSay("Still flat.");

Option 3 (flop):
  egoSay("I cite my source: Rivet. Knows everything, sells most of it.");
  actorSay(piston_a, "Rivet once sold this office its own staplers.");               // 8 words
  egoSay("I don't doubt it. I still don't doubt him either.");
  [repeat pick]: actorSay(piston_a, "The staplers, Sprocket.");                      // 3 words
                 egoSay("We've both met the staplers. Moving on.");
```

**ROUND 2 menu:**
1. `The curtains disagree.`
2. `Show him the bar tab.` ← **winner**
3. `Zero is a suspicious number.`
4. `I withdraw to regroup.`

```
Option 2 (WINNER — FIRST in source):
  egoSay("I lay the Oil Bar tab on the blotter, next to my voided notice.");
  egoSay("Four rounds of single-origin crude. Charged to DYNAMO MAINT. — CONTINGENCY. Signed: Caliper.");
  actorSay(caliper_a, "I can explain the signature.");                               // 5 words
  actorSay(piston_a, "You cannot. It's a very good signature.");                     // 7 words
  egoSay("The boiler drops a register. The room gets one degree more honest.");
  actorSay(piston_a, "The Dynamo is fine. I have never felt better.");               // 9 words
  pistonRound = 3;  → ROUND 3 brownout beat + menu
  // ^ the pronoun slip ("I", for "it") is the round's hinge — see §11

Option 1 (flop — rewards window recon):
  egoSay("I mention the curtains. Dust on the velvet, none on the cord.");
  actorSay(piston_a, "I enjoy the view. Briefly. In private.");                      // 7 words
  egoSay("That one was true. I bank it.");
  [repeat pick]: actorSay(piston_a, "The view is municipal property.");              // 5 words
                 egoSay("So is the lie. Round numbers all around.");

Option 3 (flop):
  egoSay("Zero, I observe, is a very round number for a machine that size.");
  actorSay(piston_a, "Zero is the most honest number we publish.");                  // 8 words
  egoSay("I believe that more than he wants me to.");
  [repeat pick]: actorSay(piston_a, "Audited annually. By us.");                     // 4 words
                 egoSay("The auditor sends his regards, I'm sure.");
```

**ROUND 3 — scripted brownout beat fires when the round opens (and on each re-entry):**

```
startSound(sagSnd);
setObjectState(gauge, 2);                       // needle drops
egoSay("The hum sags. The gauge needle leans. His hand drifts toward the crank dock.");
→ ROUND 3 menu
```

Menu:
1. `Offer him a wind. Professionally.`
2. `Point at the gauge.`
3. `Say nothing.` ← **winner**
4. `I withdraw to regroup.` (leave here: `egoSay("I step out. Behind me, a ratchet, briskly. We'll both pretend otherwise.");`)

```
Option 3 (WINNER — FIRST in source) → CONFESSION CUTSCENE:
  egoSay("I say nothing. I'm a maintenance-bot. We're comfortable around things that wind down.");
  egoSay("The needle does the talking.");
  actorSay(piston_a, "Oh, hang the banners.");                                       // 4 words
  startSound(ratchetSnd);
  egoSay("He docks the crank and winds himself, right there, in front of a maintenance-bot.");
  egoSay("Eight turns. The maximum is five. He signs the maximums.");
  actorSay(piston_a, "It's been sagging since spring. The engineers gave it three days."); // 11 words
  actorSay(piston_a, "That was two days ago.");                                      // 5 words
  egoSay("I ask about the Order. The bots who built the thing.");
  actorSay(piston_a, "Wound down. One by one. Pensioned off the books.");            // 9 words
  actorSay(piston_a, "One name left on the list. Deliveries go up the hill.");       // 11 words
  egoSay("Up the hill is the Dynamo District. Behind the fence with opinions.");
  egoSay("Then he opens a drawer and slides a letter across. Crumpled and uncrumpled. Repeatedly.");
  egoSay("WINDING IS A SERVICE NOW, it says. WE HAVE THE FIRST KEY. RATES ON REQUEST.");
  egoSay("Terms of contact: the Scrap & Barrel back door. Knock twice, once, twice.");
  egoSay("I know that knock. I've been on the wrong side of it twice.");
  actorSay(piston_a, "The city cannot pay.");                                        // 4 words
  actorSay(piston_a, "The city cannot be seen refusing to pay.");                    // 8 words
  actorSay(piston_a, "You, fortunately, are not the city.");                         // 6 words
  startSound(pickupSnd);
  pickupObject(InventoryItems::ransomNote, InventoryItems);
  egoSay("I get the letter, the knock, and the deniability. The city gets to be fine.");
  actorSay(piston_a, "Nothing is wrong, son. Go fix it.");                           // 7 words
  // END on the NPC line. No button. Dead air is the button.
  pistonRound = 4; pistonCracked = 1;   // set BEFORE the cutscene speech block
                                        // per story-flags-before-speech (top of branch)

Option 1 (flop, near-miss):
  egoSay("I offer a courtesy wind. Free estimate. No appointment necessary.");
  actorSay(piston_a, "The Mayor does not receive maintenance during office hours."); // 9 words
  egoSay("He says it with his hand still on the crank. We both notice.");
  egoSay("He finds one more pound of pressure somewhere.");
  [repeat pick]: actorSay(piston_a, "Office hours, Sprocket.");                      // 3 words

Option 2 (flop):
  egoSay("I point at the gauge. The needle, the pencil line, the math.");
  actorSay(piston_a, "That gauge measures optimism. Optimism varies.");              // 6 words
  egoSay("He turns it face-down. The needle scrapes the blotter on the way.");
  [repeat pick]: actorSay(piston_a, "It's face-down. Optimism is resting.");         // 6 words
```

**Post-crack `piston:TalkTo`:**

```
egoSay("He asks, off the record, how the maintenance business is.");
egoSay("Booming, I tell him. Also off the record.");
```

### 7.12 Inventory items — full text

```
barTab:
  LookAt:
    egoSay("An Oil Bar tab. Four single-origin rounds, charged to DYNAMO MAINT. — CONTINGENCY.");
    egoSay("Signed: Caliper, in a hand that measures its angles.");
  Use (no objB):
    egoSay("It's a City Hall expense. Somebody at City Hall should really see it.");
  Smell:
    egoSay("Single-origin crude, four glasses deep.");

ransomNote:
  LookAt:
    egoSay("WINDING IS A SERVICE NOW. WE HAVE THE FIRST KEY. RATES ON REQUEST.");
    egoSay("Below that, the knock, notated. Two. One. Two. Sheet music for a door.");
  Use (no objB):
    egoSay("It's an invitation. The dress code is 'expendable'.");
  Smell:
    egoSay("Salt corrosion. Postmarked the harbor.");

poster (EDIT — add branch keyed on posterVoided, FIRST in source if it
becomes the walkthrough-read state):
  LookAt (posterVoided):
    egoSay("\"DYNAMO MAINTENANCE: NOTHING IS WRONG.\" Now with a VOID stamp.");
    egoSay("Denied, then voided. The most official object I own.");
```

---

## 8. Music brief + SFX list

### Music — "Nothing Is Wrong (March)" (`genmusic.py` third song)

- **File:** `assets/generated/audio/cityhall.mid` → `cityhall.soun` (SOUN/MIDI flavor — never `-gmd`).
- **Form:** 16 bars, 4/4, straight (not swung — the march does not shuffle; Midtown swings, City Hall marches). **BPM 96. Key: B♭ major.** `MARCH_LOOP_BEATS = BARS * 4 + 1 = 65`.
- **Loop idiom:** `imPlayerSetLoop(marchSnd, 999, 1, 0, 65, 0)` + the standard `musicLoop()` watchdog (`delay(120); unless(isSoundRunning(...)) restart`).
- **Channels/programs** (AUDIO.md GM→FM-safe set): CH0 lead PRG 56 trumpet (fallback PRG 80 square lead if the OPL2 render disappoints — **audition in the browser; AdLib is canonical**); CH1 bass PRG 38 synth bass, oom on 1 and 3, pah-fifth on 2 and 4; CH2 comp PRG 4 e-piano, block chords on the off-beats; CH9 percussion: parade snare (16th-note pickup rolls into bars 1 and 9), kick on 1/3, light hat.
- **The joke, structurally:** bars 1–8 are pure civic confidence — fanfare arpeggio up the B♭ triad, square shoulders. Bars 9–16 the bass starts *resting on beat 3* (the march checking its own gauge) while the lead keeps going as if nothing is wrong. Underneath the entire form, CH3 (PRG 38, velocity ~28) holds a pedal **A1 — a half-step under the tonic's root**: the Dynamo's hum, flat by half a step, audible under the confidence for any player who already heard Midtown's "It's flat. By half a step." This is the N-A5 detuning-hum motif's first scored appearance; the act-flag pitch-drift work can later widen this interval globally.
- **During the brownout beat:** the march does NOT dip (the city pretending is funnier, and iMUSE micro-modulation isn't worth the risk); the `sag.soun` SFX carries the power dip on top.

### SFX (`genaudio.py` recipes — 8-bit unsigned mono VOC, deterministic)

| File | Recipe (existing ingredients) | Used at |
|---|---|---|
| `steam.voc` → `steamSnd` | `mix(noise_burst(0.55, 0.75, 7), partials(0.55, [(3800, 0.15, 10)]))` — a pressure-relief hiss; a kettle conceding a point | R1 win, flavor vents |
| `stamp.voc` → `stampSnd` | `mix(partials(0.09, [(150,0.9,40),(90,0.7,30)]), noise_burst(0.03, 0.6, 90))` — felt-padded thunk + click | the VOID stamp |
| `creak9.voc` → `creak9Snd` | `concat` of **nine** short tick `partials(0.05, [(620,0.5,50),(1240,0.3,60)])` with shrinking silences (0.14s → 0.04s, accelerando) — a door surrendering degree by degree | the 81-degree opening |
| `sag.voc` → `sagSnd` | two-block glide: `partials(0.6, [(220,0.5,1.2)])` into `partials(0.7, [(207,0.5,1.0)])` with a 0.05s crossfade-shaped dip in between (A → A♭, the half-step made audible), overall amplitude sagging then half-recovering | the Round 3 brownout |
| `whistle.voc` → `whistleSnd` (optional) | `partials(0.4, [(932,0.6,4),(988,0.5,4)])` — two close partials beating; a strained boiler whistle | Piston's bluster peaks (intro cutscene) |
| reused | `ratchetSnd` (the crank — already the game's winding sound: continuity), `knockSnd`, `pickupSnd`, `clinkSnd`, `creakSnd` | throughout |

---

## 9. Walkthrougher beats

Schema note: `choose:` shots depend on the B2+B8 walkthrougher dialog-option support; `detour:`/`mistake:` shots use the streamer-screenplay schema from the production plan (mistakes assert their refusal line; detours expect only `[talking]`). Inventory slot indices below are placeholders — ScummVM compacts on removal; compute at integration against the Act 2 inventory state (expected held set entering this scene: poster, magnet, backstage pass, barTab, ± voucher per Scene 07).

### Canonical validate shots (append to `full-run.play.yaml`)

```yaml
  # --------------------------------- Scene 08: City Hall, Mayor Piston
  - name: paper-trail
    do: {verb: Use, object: City Hall, with: inventory.slot<barTab>}
    expect: [talking]            # the 81-degrees cutscene
    timeout: 60
  - name: the-other-eighty-one-degrees
    do: {verb: Open, object: City Hall}
    expect:
      - pixel: {at: [160, 80], is: marble-paint}    # CityHallRoom probe
    timeout: 60
  - name: marble-paint                                # entry cutscene
    cutscene: CityHallRoom.entry
    expect: [talking]
    timeout: 60
  - name: civic-optimism                              # R3 plant 1 (fair-play, forced)
    do: {verb: Examine, object: civic gauge}
    expect: [talking]
  - name: an-argument-of-one                          # R3 KEY HINT (B9-style promotion)
    do: {verb: Talk to, object: Caliper}
    expect: [talking]
  - name: the-second-participant                      # second TalkTo carries the hint line
    do: {verb: Talk to, object: Caliper}
    expect: [talking]
    hold: 1.5
  - name: the-confrontation
    do: {verb: Talk to, object: Mayor Piston}
    expect: [talking, dialog-open]                    # dialog verbs visible at y>=145
    timeout: 90
  - name: exhibit-a
    choose: "Show him his own notice."
    expect: [talking]                                 # VOID stamp beat
    timeout: 90
  - name: exhibit-b
    choose: "Show him the bar tab."
    expect: [talking]
    timeout: 90
  - name: say-nothing
    choose: "Say nothing."
    expect:
      - talking
      - pixel: {at: inventory.slot<ransomNote>, is: white}   # the note lands
    timeout: 120
    hold: 2
```

### Streamer-mode detours & mistakes (the film's screenplay)

```yaml
  - name: four-mayors-one-boiler
    detour: {verb: Examine, object: portrait gallery}
  - name: confidence-reorder-point
    detour: {verb: Examine, object: spare banners}
  - name: the-dust-tells
    detour: {verb: Examine, object: curtained window}
  - name: pull-the-cord
    detour: {verb: Open, object: curtained window}        # curtains open, Dynamo framed
  - name: he-precedes-himself
    detour: {verb: Smell, object: Mayor Piston}
  - name: paper-through-channels                          # wrong-but-reasonable first move
    mistake: {verb: Give, object: Mayor Piston, with: inventory.slot<poster>}
    line: "He waves it at the visitor's chair. Appointments are conducted seated."
  - name: half-a-step-flat                                # R1 flop, played first
    mistake: {choose: "The Dynamo is flat by half a step."}
    line: "Retuned. By request. The city prefers a softer key."
  - name: the-staplers                                    # R1 flop two — the gag mine
    mistake: {choose: "Rivet says otherwise."}
    line: "Rivet once sold this office its own staplers."
  - name: the-curtains-disagree                           # R2 flop that rewards the detour
    mistake: {choose: "The curtains disagree."}
    line: "I enjoy the view. Briefly. In private."
  - name: courtesy-wind                                   # R3 near-miss before the win
    mistake: {choose: "Offer him a wind. Professionally."}
    line: "The Mayor does not receive maintenance during office hours."
  - name: aftermath                                       # post-crack mop-up
    detour: {verb: Talk to, object: Caliper}
  - name: official-twice
    detour: {verb: Examine, object: inventory.slot<poster>}  # the VOIDed notice
```

---

## 10. Planted/paid ledger

**Consumes (pays off):**

| Plant | Planted at | Paid here |
|---|---|---|
| Official notice / poster | Scene 01 board (`docks.scc`), validate path | Round 1 evidence; stamped VOID; "Now it's official twice." Item retained with new LookAt state. |
| Nine-degrees aide | Scene 04 `midtown.scc:cityHall:Use` ("exactly nine degrees", "anyone holding paper") | Named Caliper; "the other eighty-one degrees"; paper — the thing aides fear — is exactly what defeats them, twice. |
| NOTHING IS WRONG banners/notices | Scenes 01 + 04 | Banner stack interior gag; the final line weaponizes the slogan as a blessing ("Nothing is wrong, son. Go fix it."); the public banner survives — the cover-up persists outward by design. |
| Oil Bar single-origin crude | Scene 04 `oilBar:Smell` | Scent through the door gap is the breadcrumb to Scene 07; the tab is "four glasses deep." |
| Aides drink and talk / barTab | Scene 07 (interface, §3) | Door key + Round 2 evidence. |
| Knock-code 2-1-2 | Scene 02 rustlers' table (validate path since B9); heist hatch echo (Scene 05); Voltina echo (Scene 06) | **Forced critical-path echo #2**: notated on the ransom note; "I know that knock. I've been on the wrong side of it twice." |
| Rivet's "or down" / Rustlers' ransom motive | Scene 03 Rivet lore; Voltina says it aloud (Scene 06, per N-A9 disposition) | The ransom note is the motive made paper: "WINDING IS A SERVICE NOW." |
| "Act Three, buddy" slot-eye | Scenes 02/03 | The note is the ticket the slot-eye was waiting for (cashed in Scene 09). |
| Sprocket's 8-turn overwind / "regulation maximum is five" | Scene 05 stage act | "Eight turns. The maximum is five. He signs the maximums." |
| The fence with opinions | Scene 04 dynamo LookAt | "Behind the fence with opinions" — deliveries go up the hill. |
| Suspiciously fresh ink | Scene 01 poster Smell | Banner stack: "the same suspicious vintage as my notice." |

**Creates (plants):**

| Plant | Pays off at |
|---|---|
| `ransomNote` item (knock notation, "WE HAVE THE FIRST KEY") | Scene 09 — hideout entry + the ransom plot in person |
| `pistonCracked` flag | Scene 09 gating; Act 3 city-state lines; finale (a mayor who can finally act in public when the lights go out) |
| Order pension list, one name, deliveries up the hill | Scene 10 — Old Crank (second shadow of the Key #3 twist; does not say it) |
| The three-days/two-days-ago clock | Act 3 pressure; the finale's power-down (N-A5) |
| Curtain dust / "I enjoy the view. Briefly. In private." | Character runway for Piston's Act 3 appearance; Scene 10 may reuse the window framing |
| Caliper drafting "the next notice" | Optional Act 3 gag surface (the banner finally changes) |

---

## 11. Embodiment audit (of this scene's own text)

**Power model (the chair's standing rule: the hum winds mainsprings remotely; hand-winding is crude short-burst backup):**
- The model is restated exactly once, at Piston's LookAt: *"The hum winds him like everybody. The steam is just the oratory."* Steam = actuation, voice, gesture (his subsystem flavor); the mainspring = hum-banked life support, per the docks board lecture ("Steam bot, clockwork bot, engine bot: all spring-banked"). No line claims he "runs on steam."
- The brownout beat is built ON the model rather than against it: the hum sags → his bank sags → the boiler cannot help (steam was never the winding path — no line suggests it could be, which protects the plot from a "why not steam-wind the city" hole) → the crank dock is the crude backup, and a mayor with a *worn-shiny* crank handle has been on backup for months. The wear is the confession before the confession, and it's wear — perceivable by eye.
- "Eight turns. The maximum is five." — hand-winding's recklessness was established at the stage act; Piston over-winding is desperation within the established rule, not a new rule.
- The gauge is the bank made visible: "graduated in mainspring turns," wired to his chair. Its needle is two drawn art states; the text never claims a motion the art doesn't make (the marquee-bulb lesson). The dip coincides with `sag.soun` so the room's power event is audible, visible, and stated — three channels, one fact.
- "The Dynamo is fine. I have never felt better." — the pronoun slip is the embodiment thesis spoken by the embodiment: his health and the Dynamo's are the same circuit. Intentional, load-bearing, and consistent.

**Sensory claims, line by line:**
- Crude smell through a one-degree gap: scent established as the Oil Bar's signature (`oilBar:Smell`); Sprocket's precision nose is canon (post-sweep default). A one-degree gap passes air. OK.
- "Dust on the velvet. None on the cord." — visual evidence of use, the exact shape the chair's knock-code fix demanded (dented plate at knuckle height). OK.
- "The needle scrapes the blotter on the way" — Sprocket cannot read a face-down gauge, so the line gives him sound instead of sight. Deliberate.
- "You can hear him from here" (entry) — Piston is a boiler with a voice; volume is his characterization everywhere. OK.
- "Crumpled and uncrumpled. Repeatedly." — paper carries its history visibly. OK.
- No robot breathes, swallows, or sweats anywhere in the scene ("the sound of a door rethinking its angle" replaced an early "swallow" draft). Aides drinking oil is established canon (Oil Bar, drink tokens).

**Geometry & props:**
- Door arithmetic: 9° opened (S04) − 8° closed = 1° gap (the midtown eye/smell lines fit through it); 9° + "the other eighty-one" = 90°, a full door swing. Checks.
- The barTab is posted through the gap and **explicitly taken back** ("Evidence keeps.") so it exists for Round 2. The poster is duel-stake-gated since N-L3, so it is guaranteed held; it is stamped, not confiscated. The ransom note is handed over on screen, drawer to blotter to pocket. No prop teleports, none is consumed silently.
- Window faces the Dynamo: Midtown establishes street-level line of sight uphill; City Hall fronts that street. The open-state art paints the Dynamo small and distant — claims sized to the pixels.
- "Marble paint over sheet metal" — checkable in art (keep seams visible); the portraits' "same boiler, different dents" reads as the literal same chassis repainted, which is robot-true rather than dynasty-fudged.
- Piston "hasn't left" / heaviness is never asserted as a rule — deliberately omitted (an earlier draft claimed "the boiler doesn't do hills"; cut, because Act 3 may want him mobile).
- Character lies are not embodiment breaks but are flagged for the record: "Retuned. By request." (he cannot tune the Dynamo — that is the point), "That gauge measures optimism" (it measures spring turns; the LookAt told the truth first, so the player catches the lie — that's the gag working as designed).
- "It's been sagging since spring" — season-now is unestablished anywhere in canon; the line implies only "a while ago." Safe. The clock math (three days, issued two days ago = the GDD's three story days, final day = Act 3) is reconciled in §1.

---

## 12. Implementation notes (the pitfalls, pre-paid)

- **Verb ids:** use only verbs declared `@ id` in `common.sch`; the dialog tree uses `dialogVerb0..4`/`dialogUp/Down` from `dialog.sch`. No new verbs.
- **Owner checks:** "is held" = `getObjectOwner(x) == VAR_EGO` (never truthiness — owners default to 0x0F); consumption (none in this scene except none — tab and poster and note all survive) would be `setObjectOwner(x, 0)`.
- **Dub source order:** within every handler, walkthrough-path branch first (marked in §7); within each duel round's source block, the winner's lines first, flops after — mirroring `rivet:TalkTo`. Mixed `egoSay`/`actorSay` in one handler extract as ONE ordered list (NPC-DIALOG §6.9); the B2 contest plumbing owns the final pairing convention for `choose:` shots — coordinate before recording takes.
- **Silent transitions:** both City Hall enter (midtown `Use` post-`cityHallOpen`) and exit (`doorOut`) say nothing; all arrival flavor is in `CityHallRoom.entry`, all door comedy is in the `UsedWith` cutscene which does NOT transition.
- **Story flags before speech:** `cityHallOpen`, `posterVoided`, `pistonRound`, `pistonCracked` all set at branch top, before their cutscene's first line.
- **Actor placement:** `putActorAt` both Tier-A actors in `CityHallRoom.entry`; **also `putActorAt(caliper_a, ...)` in MidtownRoom** before the door cutscene's one Caliper line (actorTalk drops/mis-renders lines for actors not in the room). Park them; never move the painted figures.
- **Animating element:** Piston's stack-puff is a `setObjectState` loop (signFlicker pattern) — stop it on cutscene entry that repositions anything, restart on exit; a missed `stopScript` leaves the mayor smoking forever.
- **Dialog UI:** `dialogClear(1)` → `dialogAdd(...)` per option → `dialogStart(PISTON_DIALOG_COLOR, hi)` → poll `selectedSentence` → `dialogEnd()`. Rebuild the menu each round (don't mutate in place); flop picks re-add the same menu.
- **Palette:** PAL[113]/PAL[114] need genassets named probes (`talk-piston`, `talk-caliper`), the scenery-collision assert, and one VP8 probe take before any dub is trusted.
- **Editorial desk:** this draft runs the five-chair desk before validate, per charter; the text above pre-clears the known templates (zeugma census: zero new instances; "with opinions": one callback to the sanctioned fence line, inside a quoted ego callback — defensible, flagged for the desk; self-grading: the scene ends on an NPC line with no button, twice).