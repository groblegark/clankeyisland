I have everything I need. Here is the complete design doc.

---

# SCENE 10 — DYNAMO DISTRICT: OLD CRANK

*Clanker City Chronicles · Act 3 · design doc for the implementer*
*Models: `game/theater.scc`, `game/tavern.scc`, `game/midtown.scc`, `game/alley.scc`. Standards: `docs/editorial/CHARTER.md`, the three editorial reports, `docs/research/NPC-DIALOG.md`, `docs/research/NARRATION.md`.*
*Status going in: BLOCKER-clean target. Honors the standing desk rulings (B7 meta-monopoly, B10 smell-template ban, N-A4 no self-grading, N-A8 destiny cap, "with opinions" reserved-for-this-fence, the embodiment power model).*

---

## 0. Where the player is when this scene opens

By Scene 10 the player holds **two** keys:

- **Key #1** — `InventoryItems::windupKey` (the brass forearm key; crate → talent-show prop → stolen by the Rustlers mid-bow → recovered in the hideout, Scene 09).
- **Key #2** — `InventoryItems::secondKey` (Madame Voltina's guarded key, Scene 06). *Build dependency: if Scene 06 has not finalized the item id, Scene 10 reads whatever Scene 06 creates; the dry-run beat (§2 step 4) degrades gracefully to one key — see fallback note.*

Scene 10's job is to obtain **Key #3** and stage the finale. Key #3 is not in a crate. Key #3 is a person.

---

## 1. Scene goal + the three-keys spine

**Goal:** Get into the fenced Dynamo yard, reach the Great Dynamo up close, and acquire the third and last Key of Clankey Island — which turns out to be the wind-up key in the back of **Old Crank**, the hermit who has been the Order's living fail-safe since the Dynamo was built. The player leaves holding all three keys, with the Dynamo's three-slot interface learned, ready for the Scene 11 rewind.

**How it advances the spine:**

- **It closes the collection.** Act 1 earned Key #1; Act 2 earned Key #2; Scene 10 earns Key #3. This is the last acquisition before the finale. Rivet's planted line — *"All three together could wind the city back up. Or down."* (`alley.scc:rivet`) — becomes true in the player's pocket here.
- **It pays the game's one twist.** GDD Act 3: *"Old Crank reveals he is Key #3."* The Embodiment desk (2026-06-12) and Story desk (N-A10) both flagged that this twist had **zero plants** for five scenes; Scene 06 was assigned the forward reference *"Ask me sometime about the key that winds itself."* Scene 10 is where that retro-support **lands**: Old Crank is the key that winds itself, and the reveal is planted-then-paid **inside this scene** so a player who skipped Voltina's tease still earns it fairly (§2 fair-play audit).
- **It makes the deadline physical.** The detuning hum (N-A5 / GDD designed clock) is finally **diegetic and central**: it is this room's music, it is the gate puzzle's timing source, and it is audibly *flat by a half-step* up close — the same half-step Midtown only asserted. The city visibly powers down below, seeding the finale's room-by-room blackout.
- **It gives the antagonists' stakes a face.** The Order built the Dynamo and left a person behind as the spare. The Rustlers wanted to ransom the rewind; the rewind costs a bot his independence. The scene converts "fetch the third key" into "watch someone decide to spend himself," which is the emotional turn Act 3 needs.

---

## 2. The puzzle chain (numbered graph) + fair-play audit + the playable-agency beat

```
            [enter Dynamo District]  (entry cutscene: fence, Dynamo, the dying hum, city dimming below)
                       |
        ┌──────────────┴───────────────┐
   (1) THE FENCE/GATE                (flavor detours, non-blocking)
   governor tempo-match  ◄── PLAYABLE  · plaque (KEEP TIME)
   [dialog tree, 4 picks]   AGENCY     · fence (with opinions)
        | gateWound=1                  · overlook (city dimming)
        ▼
   (2) MEET OLD CRANK  ── metCrank=1
        |    (self-winding established = plant pay #1)
        ▼
   (3) THE DYNAMO UP CLOSE  (LookAt: hum nearly gone, THREE slots visible)
        |
        ▼
   (4) THE DRY RUN  ── Use Key#1 + Key#2 on the Dynamo  (the act's inventory-combination beat)
        |   hum lifts a half-step then stalls = "two-thirds of a heartbeat"  → dynamoPrimed=1
        |   (audible hum_lift cue; proves the rewind works; signposts the missing third)
        ▼
   (5) THE REVEAL  ── earned, not narrated  → crankRevealed=1
        |   routes that converge: Voltina's plant / Crank self-winding / the third slot's
        |   shape matches the key in Crank's back / asking Crank what he's for
        ▼
   (6) THE COST / THE GIVE  ── Crank pulls his own key, winds down  → crankGiven=1
        |   player authors the goodbye (3-option dialog; all advance, lines differ)
        |   pickupObject(crankKey)
        ▼
   [exit: all three keys in pocket → Scene 11 finale]
```

### Step detail

**(1) The fence/gate — THE PLAYABLE-AGENCY BEAT.**
The Order's yard is closed by a turnstile driven by a clockwork **governor** (a flyweight speed-regulator). Normally the Dynamo's hum keeps the governor wound and the turnstile spins free for anyone — *this is the power model in action* (remote winding). With the hum nearly dead the governor has run down and the turnstile is locked rigid; there's a worn **hand-crank socket** on the post (the crude backup, per the embodiment model). A governor regulates *speed*, so brute force makes it worse — you have to crank at the rate it expects, which is the rate the Dynamo hums.

Mechanism: the proven dialog-tree UI (`game/dialog.scc` — `dialogClear`/`dialogAdd`/`dialogStart(color,hi)`/poll `selectedSentence`/`dialogEnd`), the same machinery Scene 06's riddle duel uses. First `Use` on the gate plays a short setup (the governor pulsing out of time, Crank's offscreen voice), then opens the four picks. Wrong picks flop funny and **always retry** (no soft-lock); the right pick opens the gate.

| Pick (verb-line shown to player) | Outcome |
|---|---|
| **"Crank it hard."** | Over-speed: the governor throws a flyweight, the handle launches (`boingSnd`→`thudSnd`), the turnstile locks down *tighter*. Flop. Retry. |
| **"Crank it gently."** | The pawl never catches. Nothing happens. Flop. Retry. |
| **"Just shove the gate."** | The chain-link springs back. Flop — and the one sanctioned payoff of the reserved phrase (§4). Retry. |
| **"Match the hum."** | **WIN.** Crank in time with the dying hum, the governor stops fighting, the escapement releases (`governorSnd`→`ratchetSnd`→`thudSnd`), gate state→2. `gateWound=1`. |

**(2) Meet Old Crank.** Inside the yard. A wind-up hermit, still moving normally while the whole island stalls — because he **winds himself**. Plant pay #1 for Voltina's "key that winds itself." He wants something (not a vending machine): he is *tired of being the spare*, and afraid, and waiting is the only verb he has left. `metCrank=1`.

**(3) The Dynamo up close.** `LookAt` is the canon "hum nearly gone" beat: faint, flat by a half-step, three keyhole slots in a row, two of them the size of the keys in your pocket. The room's music is the hum itself (§5). No narration spells out the arithmetic — three slots, two keys, the player does the math (the Midtown line *"Even the fence can do that math"* already trained it).

**(4) The dry run — the inventory-combination beat (answers N-A1).** `Use windupKey on dynamo` and `Use secondKey on dynamo` seats both keys in two slots; turning them together **lifts the hum a clean half-step** (`humLiftSnd`, music swaps `hum_flat`→`hum_lift`) and then **stalls** — "two-thirds of a heartbeat." This is the act's first real two-item-on-one-mechanism combination, it is player-driven, and it does triple duty: it's the "Dynamo up close" payoff, it proves the rewind works (which is what convinces Crank in step 6), and it signposts the missing third key without anyone saying "you need a third key." Sprocket takes the keys back out afterward (you don't leave legendary keys unattended; the finale needs them). `dynamoPrimed=1`.
*Fallback (if Scene 06's Key #2 isn't built yet): the dry run runs on `windupKey` alone and lifts the hum a third, not a half — same signpost, weaker chord.*

**(5) The reveal — earned, not narrated.** With two slots filled in the player's mind and one empty, the only key-shaped thing left in the yard is the one turning in Old Crank's back. Multiple **fair** routes converge, and each is a player action, never a Sprocket announcement:
- `LookAt` the Dynamo's third slot after the dry run → its profile is described as matching a key the player has already *seen* (Crank's, step 2/its own LookAt).
- `TalkTo` Crank → a 3-option tree where the player can **ask what the Order left him here to do**; Crank says it in his own mouth (≤12 words).
- Voltina's Scene 06 plant, if the player heard it, clicks.
`crankRevealed=1` once any route fires.

**(6) The cost / the give.** After the reveal, interacting with Crank triggers him to reach back and pull **his own key** — and as he does, *he winds down* (`windDownSnd`; he slows, his talk color dims, his last lines come slower). The player gets a final 3-option dialog (the goodbye) — every option advances, the **lines differ**, so the player authors the farewell (the narrative-walkthrougher pillar). `pickupObject(crankKey)`; `crankGiven=1`. Crank becomes a still hotspot. The two pocket keys are untouched. Scene complete; the player carries three keys into Scene 11.

**Why the cost is real (and stays inside the no-death rule).** Old Crank is the one bot the blackout can't kill, *because* he is self-winding and off-grid — that is his whole identity as a hermit. Pulling his key stops him, like any wind-up whose key is removed. He is volunteering to become killable: he trades his independence for the city's, and gambles that the rewind he can't stay awake to watch actually works. He winds *down* (dormant, mid-gesture), not destroyed — and the finale's restored hum could wind him remotely again, rejoining the grid he spent his life avoiding. The cost is his autonomy and the not-knowing. His exit line is *"Wind the city. I'll catch up. Maybe."*

### Fair-play audit

| Step | Knowledge the player needs | On-screen source(s) — all reachable before the step |
|---|---|---|
| (1) crank at the hum's tempo | "match the hum," not force | **plaque**: `GOVERNOR — KEEP TIME` (diegetic signage, caps legal); the hum is **audible** (room music + Dynamo LookAt); the governor **visibly pulses out of time** (gate LookAt + setup beat); **Crank's offscreen line** *"It only answers the hum. Always did."* |
| (1) wrong picks are reasonable | hard/gentle/shove are the instincts | deliberately the first things any player tries; their flops are the gags, not punishments — always retryable |
| (4) two keys go in the Dynamo | the slots accept your keys | Dynamo LookAt names **three slots** sized to the keys; Midtown's *"One key, three slots, a fence in between"* / *"Even the fence can do that math"* pre-trained the geometry |
| (4) a third is missing | two isn't enough | the **audible half-lift then stall** is the signal; no line states it |
| (5) Crank is the third key | the spare = the man | **Voltina's plant** (S06); Crank **visibly self-winding** (step 2, his back examinable); the **third slot's profile matches his key** (Dynamo LookAt); Crank answers **what the Order left him to do** when asked |
| (6) it costs him | pulling the key stops him | the power model already established (board/Midtown: remote winding; hand-wind = backup); Crank stated self-winding in step 2; the **wind-down is shown**, not asserted |

No moon logic, no pixel hunt, no unsourced Sprocket knowledge, no lock that names a non-existent item. The one hard gate (the governor) is signposted four ways and is the playable beat; everything after it is character work with player-driven reveals.

---

## 3. Object table (320×144 stage)

Room `DynamoRoom`, image `rooms/dynamo.bmp`, `boxd rooms/dynamo.box`. Player arrives up from Midtown/the funicular at the **left** edge; the yard and Dynamo are **right**, up the hill. ASCII sketch (origin top-left, 320 wide, playfield ~144 tall):

```
 0        64       128      192      256     319
 0 +----------------------------------------------+
   |                          [====DYNAMO=====]    |  dynamo  x200 y8 w104 h76
   |        [plaque]   [fence==============]       |  fence x40 y36 w150 h22
 40|       ___________________________________     |  plaque x46 y28 w26 h10
   | [way] |  [GATE] |          [CRANK] [bench]|    |  gate x66 y48 w28 h56
 56| [down]| governor|           ))            |    |  oldCrank x126 y54 w28 h50
   | |    || socket  |          ((            ||    |  workbench x162 y60 w42 h44
   | |    ||_________|                        ||    |  wayDown x0 y52 w22 h52
100| [~~~overlook: the city, dimming~~~]          |  overlook x6 y104 w110 h26
   +----------------------------------------------+
```

| Object | rect (x,y,w,h) | class | states | verbs handled | bits read/set |
|---|---|---|---|---|---|
| **wayDown** | 0,52,22,52 | Openable | — | LookAt, Open/Use (→ MidtownRoom, silent transition) | — |
| **fence** | 40,36,150,22 | — | — | LookAt, Use (shove→opinion), Smell | — |
| **plaque** | 46,28,26,10 | — | — | LookAt (`GOVERNOR — KEEP TIME`, fair-play hint) | — |
| **gate** | 66,48,28,56 | Openable | `gate_closed.bmp` / `gate_open.bmp` (state 1→2) | LookAt, Open/Use (governor dialog tree), Move, Smell | sets `gateWound` |
| **oldCrank** | 126,54,28,50 | Person | (Tier-A actor overlay; painted figure in bg; wound-down via talk-color dim + line pacing) | LookAt, TalkTo (meet / reveal tree / give tree), Use/Give (windup motion → reveal/give), Smell | reads all; sets `metCrank`, `crankRevealed`, `crankGiven` |
| **workbench** | 162,60,42,44 | — | — | LookAt (spare keys → "spare" plant), Use/PickUp (refused), Smell | — |
| **dynamo** | 200,8,104,76 | — | — | LookAt (hum nearly gone, three slots), TalkTo, Use/UsedWith(windupKey, secondKey → dry run), Smell | reads `metCrank`; sets `dynamoPrimed` |
| **overlook** | 6,104,110,26 | — | — | LookAt (the city dimming below — stakes/finale seed), Smell | — |

**Actor:** `oldCrank` is a costume-less Tier-A actor (`actor oldCrank;` in `common.sch`, `#define CRANK_COLOR <108..112>`, `setActorTalkColor` in `actors.scc`, `putActorAt(oldCrank, 138, 96, DynamoRoom)` in entry — and **park him in-room even before his first line** per the NPC-DIALOG landmine). The painted hermit lives in `rooms/dynamo.bmp`; his self-winding key in his back is drawn (examinable). Wound-down state = dim the talk color + slow line pacing (no new costume needed; Voltina remains the first *costumed* actor). His offscreen gate-hint line is still `putActorAt` into the yard first.

**New art the room needs (genassets.py):** the fence run with the gate's two states (closed/open turnstile), the governor + hand-crank socket on the post (visibly pulsing — a 2-state flicker like `signFlicker`/marquee), the plaque, the Great Dynamo with **three keyhole slots** drawn at key scale, Old Crank with a visible **key in his back** and a wound-down pose variant, the workbench of spares, and the **overlook** showing the city below with patches going dark (palette-dim a few window clusters, mirroring the docks brownout). Per the Embodiment desk: *paint what the text claims* — the dimming city, the three slots, and Crank's key must all exist on screen.

**New story flags** (add to `dynamo.sch`, mirroring `theater.sch`):
```
room DynamoRoom {
    bit visitedDynamoDistrict;
    bit gateWound;
    bit metCrank;
    bit dynamoPrimed;
    bit crankRevealed;
    bit crankGiven;
    object wayDown; object fence; object plaque; object gate;
    object oldCrank; object workbench; object dynamo; object overlook;
}
```
**New inventory item** (`inventoryitems.scc` / `.sch`): `crankKey` — name `"the third key"`, art `inventory/inv_crankkey.bmp` (Preposition `to`/`on`; LookAt/Use/Smell per the existing item template). Created by step 6.

---

## 4. Full dialog draft

*Register: Sprocket narrates (reported speech default, KQ6-CD deadpan, falling terminals, no winks, no act-naming). Old Crank is a direct-speech NPC, lines ≤12 words, deadpan-weary. No `[material] and [abstract]` smell zeugmas. No self-grading buttons. "With opinions" appears exactly once (the fence). Walkthrough-path lines go FIRST in source per `(object,verb)` — the dub pairing contract.*

### Room entry (`DynamoRoom.entry`, cutscene, `unless(visitedDynamoDistrict)`)
```
egoSay("Top of the hill. The Dynamo District, where the city keeps the thing it won't talk about.");
egoSay("Behind the fence: the Great Dynamo. Bigger up close. Quieter up close, which is the part that worries me.");
egoSay("The hum's still going. Barely. Like something counting down and losing its place.");
egoSay("Below, the lights are going out in patches. Up here, the thing that's supposed to stop that is barely turning.");
```

### wayDown (exit, left)
```
LookAt:  egoSay("Back down the rail to Midtown. Downhill's the easy direction. It always is.");
Open/Use: // silent room transition (dub pairing); arrival flavor lives in MidtownRoom.entry
         putActorAt(VAR_EGO, 286, 120, MidtownRoom); startRoom(MidtownRoom);
```

### fence
```
LookAt:  egoSay("The fence with opinions. Wrought iron, wound tight, and certain it was here first.");
         egoSay("There's a gate in it. The gate is where opinions are negotiated.");
Use:     egoSay("I lean on it. The fence has opinions. It just shared one.");           // sanctioned payoff of the reserved phrase
Smell:   egoSay("Rust held together by paint held together by rust.");                  // recursion, not zeugma
```

### plaque (fair-play hint, diegetic caps legal)
```
LookAt:  egoSay("A brass plaque, polished by nobody for a long time: GOVERNOR — KEEP TIME.");
         egoSay("Under it, smaller: ORDER OF THE WIND-UP KEY. So this is their front porch.");
```

### gate — the governor (the playable beat)
```
LookAt:  if(gateWound) { egoSay("Open. The governor's spinning sweet now, in time with itself for once."); return; }
         egoSay("A turnstile run by a governor — little flyweights that should be spinning.");
         egoSay("They're twitching instead. Trying to keep time with something they can't hear anymore.");
         egoSay("There's a hand-crank socket on the post, worn shiny. Other hands. Older hands.");

Open/Use/Move:
         if(gateWound) { /* silent: you walk through; no transition line */ return; }
         unless(heardGateHint) {                      // first contact: setup + Crank's offscreen nudge
             heardGateHint = 1;                        // (local script bit; or fold into gateWound setup)
             cutscene(0) {
                 startSound(governorSnd);
                 egoSay("I take the crank. The governor lurches, fights me, locks.");
                 waitForMessage();
                 egoSay("From inside the yard, a voice. Dry as a dropped washer.");
                 waitForMessage();
                 actorSay(oldCrank, "It only answers the hum. Always did.");      // 6 words, fair hint
                 waitForMessage();
             }
         }
         // --- dialog tree: how do I crank it? ---
         Dialog::dialogClear(1);
         Dialog::dialogAdd("Crank it hard.");
         Dialog::dialogAdd("Crank it gently.");
         Dialog::dialogAdd("Match the hum.");
         Dialog::dialogAdd("Just shove the gate.");
         Dialog::dialogStart(SPROCKET_COLOR, VERB_HI_COLOR);
         // poll selectedSentence; on choice:
         //  0 (hard):
         cutscene(0) {
             startSound(governorSnd); egoSay("I commit. The governor overspeeds, throws a weight, and bites down harder.");
             waitForMessage(); startSound(boingSnd); startSound(thudSnd);
             egoSay("The crank handle leaves. I find it later. Worse than when I started.");
             waitForMessage();
         }   // retry
         //  1 (gently):
         egoSay("I coax it. The pawl never catches. The gate waits for me to mean it.");   // retry
         //  2 (match the hum):  WIN
         cutscene(0) {
             startSound(governorSnd);
             egoSay("I crank in time with the dying hum. Slow. Flat. Apologetic.");
             waitForMessage();
             startSound(ratchetSnd); setObjectState(gate, 2); startSound(thudSnd);
             gateWound = 1;
             egoSay("The governor stops fighting me. The escapement lets go. The turnstile turns.");
             waitForMessage();
         }
         //  3 (shove):
         egoSay("I put a shoulder into it. The fence shares a second opinion. Same as the first.");   // retry
         Dialog::dialogEnd();

Smell:   egoSay("Cold iron. The crank socket smells of every hand that gave up here.");   // flat fact + image, no zeugma
```

### oldCrank (the hermit — meet / reveal / cost)
```
LookAt:
  if(crankGiven) { egoSay("Old Crank, wound all the way down. Mid-gesture. Waiting again, the only way he has left."); return; }
  unless(metCrank) {
      egoSay("A wind-up bot older than the streetlights, oiled to a shine nobody's seen him do.");
      egoSay("Everything on this island is stalling out. He's the only thing still keeping time.");
      egoSay("There's a key in his back. It's turning. Slowly. On its own.");      // the plant, examinable
      return;
  }
  egoSay("Old Crank. Built to last, and made to wait. Bad combination, long-term.");

TalkTo:
  // ---- first meeting ----
  unless(metCrank) {
      metCrank = 1;
      cutscene(0) {
          egoSay("I introduce myself. The maintenance-bot. Three days late and one key short.");
          waitForMessage();
          actorSay(oldCrank, "I know what you are. You're the one they send last.");   // 9 words
          waitForMessage();
          egoSay("He doesn't get up. The key in his back keeps turning. Nobody's winding it.");
          waitForMessage();
          actorSay(oldCrank, "I wind myself. Last one on this hill who can.");            // 9 words — plant pay #1
          waitForMessage();
      }
      return;
  }
  // ---- reveal tree (after dynamoPrimed; before the give) ----
  if(dynamoPrimed) {
   unless(crankRevealed) {
      Dialog::dialogClear(1);
      Dialog::dialogAdd("How are you still moving? Everything else has stopped.");
      Dialog::dialogAdd("What did the Order leave you up here to do?");
      Dialog::dialogAdd("The Dynamo's third slot is the size of your key.");
      Dialog::dialogStart(SPROCKET_COLOR, VERB_HI_COLOR);
      // 0:
      actorSay(oldCrank, "I'm off their grid. Have been since before yours.");        // 9
      egoSay("Off the grid. The one bot the blackout can't reach. I start doing math I don't like.");
      // 1:
      cutscene(0) {
          actorSay(oldCrank, "Wait. Be the spare. I'm the third key.");                // 8 — reveal from his mouth
          waitForMessage();
          egoSay("He says it the way you'd report the weather. The bottom drops out of the room anyway.");
          waitForMessage();
          crankRevealed = 1;
      }
      // 2:
      cutscene(0) {
          actorSay(oldCrank, "It would be. It's the one I'm wearing.");                 // 8
          waitForMessage();
          egoSay("He taps the key in his own back. The math finishes itself. I wish it hadn't.");
          waitForMessage();
          crankRevealed = 1;
      }
      Dialog::dialogEnd();
      return;
   }
   // ---- the give tree (the cost; player authors the goodbye) ----
   unless(crankGiven) {
      egoSay("He's already reaching back for it. I'm the one who needs the minute now.");
      waitForMessage();
      Dialog::dialogClear(1);
      Dialog::dialogAdd("Stop. There has to be another way.");
      Dialog::dialogAdd("Are you sure about this?");
      Dialog::dialogAdd("Thank you.");
      Dialog::dialogStart(SPROCKET_COLOR, VERB_HI_COLOR);
      // 0:
      actorSay(oldCrank, "I've checked. For longer than you've been wound.");          // 8
      // 1:
      actorSay(oldCrank, "I'm the spare. Spares wait. I've waited enough.");           // 8
      // 2:
      actorSay(oldCrank, "Don't. Just make it worth the quiet.");                      // 7
      // --- the give (any pick falls through to here) ---
      cutscene(0) {
          startSound(ratchetSnd);
          egoSay("He works the key out of his own back. It's heavier than mine. Warmer, too.");
          waitForMessage();
          startSound(windDownSnd);
          egoSay("The turning in him slows. His voice comes down a register, then a register more.");
          waitForMessage();
          actorSay(oldCrank, "Pull a wind-up's key, the wind-up stops. Simple.");      // 8 — slower delivery
          waitForMessage();
          startSound(pickupSnd);
          pickupObject(InventoryItems::crankKey, InventoryItems);
          crankGiven = 1;
          egoSay("Three keys. The set's complete. It weighs about a person.");
          waitForMessage();
          actorSay(oldCrank, "Wind the city. I'll catch up. Maybe.");                  // 7 — last words, slowest
          waitForMessage();
          egoSay("Then nothing. He's still. Mid-gesture, like he meant to wave and ran out of road.");
          waitForMessage();
      }
      return;
   }
   // post-give
   egoSay("Nothing. The key that answered everything is in my hand now.");
   return;
  }
  // metCrank but not yet primed: he won't be hurried
  actorSay(oldCrank, "Show me it's worth it first. Then we'll talk.");                 // 9 — his WANT: proof
  return;

Use / Give:
  // taking his key by force, pre-give: refused (you don't yank a stranger's mainspring)
  if(objB == InventoryItems::windupKey || objB == InventoryItems::secondKey) {
      egoSay("I'm not winding a stranger with my key. That's how you end up in his stories.");
      return;
  }
  unless(crankRevealed) { egoSay("He's a person, not a vending machine. I keep being reminded."); return; }
  // after reveal, Use routes into the give:
  startObject2(oldCrank, TalkTo, [ TalkTo, oldCrank, 0 ]);
  return;

Smell:
  if(crankGiven) { egoSay("Brass polish, going cold. The good kind. The kind they stopped making."); return; }
  egoSay("Brass polish and... no. Just brass polish. Decades of it.");                  // sensor self-correct, not zeugma
```

### dynamo (up close — hum nearly gone; the dry run)
```
LookAt:
  if(dynamoPrimed) {
      egoSay("Two slots turned, one dark. The hum settled back to flat the second I let go.");
      egoSay("Two-thirds of a heartbeat. The last third has a slot the size of a key I've seen.");   // points at Crank
      return;
  }
  egoSay("The Great Dynamo, close enough to touch and too big to believe.");
  egoSay("The hum's almost gone. Flat by a half-step, and getting flatter while I stand here.");
  egoSay("Three keyhole slots in a row. Two of them are the size of what's in my pockets.");           // fair-play geometry
TalkTo:
  egoSay("Hang on, big fella. The cavalry's here. The cavalry is me and two keys and a bad feeling.");
Use / UsedWith:
  if(objB == InventoryItems::windupKey || objB == InventoryItems::secondKey) {
      unless(metCrank) { egoSay("I could start turning keys in the city's heart unsupervised. I could also wait the one minute."); return; }
      unless(dynamoPrimed) {
          dynamoPrimed = 1;
          cutscene(0) {
              startSound(ratchetSnd);
              egoSay("I seat both keys and turn. Together. The slots take them like they were measured for it.");
              waitForMessage();
              startSound(humLiftSnd);                       // music: hum_flat -> hum_lift
              egoSay("The hum climbs. A half-step, clean, the way Midtown should have sounded.");
              waitForMessage();
              egoSay("Then it stalls. Holds. Sags back to flat. Two keys is two-thirds of a turn.");
              waitForMessage();
              egoSay("Behind me, Old Crank stops pretending he isn't watching.");      // bridges to the reveal
              waitForMessage();
              startSound(pickupSnd);                          // takes the keys back out
              egoSay("I take my keys back. You don't leave these in a lock and walk away.");
              waitForMessage();
          }
          return;
      }
      egoSay("Same two slots, same half-step, same sag. The third one's still waiting on somebody.");
      return;
  }
  if(objB == InventoryItems::crankKey) {
      egoSay("Not yet. All three at once, or it's just noise and grief. That's the finale's problem.");   // sets up Scene 11
      return;
  }
  egoSay("The Dynamo doesn't accessorize. It has very specific taste in keys.");
Smell:
  egoSay("Ozone, going stale. Up close it's almost no smell at all, which is the whole problem.");        // sensor noticing absence
```

### workbench (flavor / "spare" plant / streamer detour)
```
LookAt:  egoSay("A workbench of spare springs and half-keys, sorted by a hand that had nothing but time.");
         egoSay("Everything here is a spare for something. He fits right in.");                          // quiet plant
Use/PickUp: egoSay("It's his life's filing. I'm not the one who gets to close the drawer.");
Smell:   egoSay("Clock oil. The kind they stopped making, same as the bot who bought it.");
```

### overlook (the stakes / finale seed)
```
LookAt:  egoSay("From up here the whole city fits in one window. Tonight it's losing that window block by block.");
         egoSay("A streetlamp gives up. Then a sign. Then a whole street, polite about it.");
Smell:   egoSay("The wind up here carries the whole city. It carries less of it every hour.");            // escalating, no zeugma
```

### crankKey (new inventory item)
```
LookAt:  egoSay("Old Crank's key. Heavier than mine, and still a little warm. I'm choosing not to dwell.");
         waitForMessage();
         egoSay("It winds the thing that winds everything. It used to wind him.");
Use:     // routes to objB UsedWith like the other items; bare:
         egoSay("Three keys, one machine, one finale. It's not a here-problem.");
Smell:   egoSay("Brass and clock oil. Him, basically. I put it back in my pocket gently.");                // "Him, basically" tag, not zeugma
```

---

## 5. Music brief + SFX list

### Music — "The Dynamo's Hum" (`genmusic.py` idiom)

The GDD's designed clock (N-A5), finally **diegetic and central**. Not a tune — a *drone that is winding down and detuned*. Implemented as **two act-flag states** so the dry run can audibly reverse it (the N-A5 "act-flag-driven pitch drift," scoped to this room):

- **`dynamohum_flat`** (default room loop): the hum nearly gone.
  - **Key:** D (the game's home key — full circle to Dockside's D minor), but **voiced a semitone low** — the drone sits on **Db where D belongs**. This is "flat by a half-step" made literal and **GM-on-AdLib safe** (real semitone, no microtones, which the OPL2 fallback can't do reliably; see `docs/research/AUDIO.md`).
  - **BPM:** 50 (a dying machine). **Bars:** 8. **Time:** 4/4. **Loop point:** `DHUM_LOOP_BEATS = 8*4 + 1 = 33` (jump back via `imPlayerSetLoop(snd,999,1,0,33,0)`, watchdog-restarted like every other room).
  - **Texture (sparse, three voices, drop-out as it dies):** a sustained low **drone** on `PRG_BASS` (38, synth bass) holding Db1/Ab1; a slow pulsing **mid** on `PRG_EP` (4, e-piano) breathing a Db minor cluster once per bar; a faltering **lead** on `PRG_LEAD` (80, square) that *drops notes* — like the Scrap & Barrel rag drops piano keys, the hum is *missing beats* as it fails (reuse the rag's `MISSING_KEYS` trick: a small drop-set that silences ~1 in 3 lead notes). No drums; a machine doesn't keep a backbeat while it dies. Low velocities (≤56), `control_change 7` volumes ~40–60.
  - **Channels/programs:** `CH_LEAD=0/PRG_LEAD=80`, `CH_BASS=1/PRG_BASS=38`, `CH_EP=2/PRG_EP=4` (the established palette; all good GM→FM mappings).
- **`dynamohum_lift`** (dry-run cue, step 4): the same eight bars **transposed up the semitone to D** (un-flattened), fuller (lead drops *fewer* notes, EP cluster swells, +6 on each `cc7`), played once over the dry-run cutscene, then the room returns to `dynamohum_flat`. This is the audible "half-step up" payoff and the seed of the finale's full restoration (three keys → all the way to D, sustained).

Register in `genmusic.py`'s emit table exactly like the others:
```
("dynamohum",      build_dynamohum,      DHUM_BARS, DHUM_BPM, DHUM_LOOP_BEATS),
("dynamohum_lift", build_dynamohum_lift, DHUM_BARS, DHUM_BPM, DHUM_LOOP_BEATS),
```
`DHUM_BPM = 50`, `DHUM_BARS = 8`. Pack with `soun -o dynamohum.soun -midi dynamohum.mid` (SOUN/MIDI flavor, never `-gmd`). Audition on **both** native (DLS GM) and wasm (OPL2) — wasm is canonical.

### SFX (`genaudio.py` idiom — synthesis recipes → 8-bit unsigned mono VOC)

New effects (add to the `sfx_*` registry dict at the bottom):

| name | recipe sketch | used by |
|---|---|---|
| **`governor`** | escapement: a regular train of short high metallic ticks — `partials(0.03, [(2600,0.6,80),(3900,0.3,100)])` repeated at a ~120ms interval over ~0.9s, over a low whirring undertone `partials(0.9,[(180,0.4,3),(360,0.25,4)])`; `mix`/`concat` the tick train onto the whir | gate winding (setup + each pick) |
| **`winddown`** | the sacrifice: a descending square sweep ~600Hz→80Hz over ~1.3s with falling amplitude (reverse of `sfx_pickup`'s rising chirp), plus a **decelerating** tick train (interval growing 90ms→260ms) that thins to silence | Crank pulling his key, step 6 |
| **`humlift`** | the hum catching: a swelling chord rising a semitone — two `partials` stacks a half-step apart, the upper fading in over ~0.7s (`attack` ramp), a soft harmonic shimmer on top — short, hopeful, then cut | the dry run, step 4 |
| **`keyturn`** *(optional; can reuse `ratchet`)* | a heavy brass key in a big lock: lower/slower `sfx_ratchet` variant — `partials` ~200–600Hz with a `thud()`-style clunk on the final detent | seating/turning keys in the Dynamo |

**Reused, already in the bank:** `ratchet` (key/gate turning), `clink`, `pickup` (key acquired), `thud` (gate detent, launched handle), `boing` (over-wound handle launch), `creak`. Declare in the room header the same way every room does (`sound governorSnd = "governor.soun";` …). VOC rules hold: 8-bit unsigned mono, type-1/pack-0, terminator; never `-spk`.

---

## 6. Walkthrougher beats (`walkthrough/screenplay/`)

Schema per `docs/WALKTHROUGHER.md` + the pillar-3 growth (`detour:`/`mistake:` shots; `only: perform`). Validate path stays terse and is the **deploy gate**; perform/streamer path is the **film** and exercises the fair mistakes the desk catalogued (gate flops, key-on-fence, force-take). Pixel probes use the master palette per the stage map.

### Canonical (validate) shots — appended to `full-run.play.yaml`

```yaml
  # ----------------------------------- Scene 10: Dynamo District / Old Crank
  - name: up-the-hill
    cutscene: DynamoRoom.entry
    expect: [talking]
    timeout: 60

  - name: the-plaque                 # fair-play: read KEEP TIME before the puzzle
    do: {verb: Examine, object: plaque}
    expect: [talking]

  - name: the-governor               # PLAYABLE BEAT: open the dialog, pick the winner
    do: {verb: Use, object: gate}
    expect: [talking]                # setup + Crank's offscreen hint, then options
    timeout: 60
  - name: match-the-hum
    dialog: {choose: "Match the hum."}   # driver clicks the dialog option
    expect:
      - talking
      - pixel: {at: [80, 60], is: sky}   # turnstile open: yard visible through the gate
    timeout: 60

  - name: meet-old-crank
    do: {verb: Talk to, object: oldCrank}
    expect: [talking]
    timeout: 60
    hold: 1.5

  - name: the-dynamo-up-close
    do: {verb: Examine, object: the Great Dynamo}
    expect: [talking]

  - name: the-dry-run                # the inventory-combination beat; hum lifts a half-step
    do: {verb: Use, object: the Great Dynamo, with: inventory.slot0}   # Key #1
    expect: [talking]
    timeout: 60
  - name: the-dry-run-two
    do: {verb: Use, object: the Great Dynamo, with: inventory.slot1}   # Key #2 -> dynamoPrimed
    expect: [talking]
    timeout: 60
    hold: 2.0

  - name: the-reveal
    do: {verb: Talk to, object: oldCrank}
    dialog: {choose: "What did the Order leave you up here to do?"}
    expect: [talking]                # Crank: "I'm the third key."
    timeout: 60
    hold: 2.0

  - name: the-cost
    do: {verb: Talk to, object: oldCrank}
    dialog: {choose: "Thank you."}   # the give cutscene; Crank winds down
    expect:
      - talking
      - pixel: {at: inventory.slot2, is: sodium}   # the third key (brass) in pocket
    timeout: 120
    hold: 2.5
```

### Streamer-mode detours + mistakes (perform film — the wrong-but-reasonable, refusal line IS the assertion)

```yaml
  - name: m-crank-it-hard           # mistake: brute force first (the instinct)
    only: perform
    do: {verb: Use, object: gate}
    dialog: {choose: "Crank it hard."}
    mistake: true
    expect: [talking]               # governor overspeeds, handle launches — the gag
  - name: m-crank-it-gently         # mistake: over-correct
    only: perform
    dialog: {choose: "Crank it gently."}
    mistake: true
    expect: [talking]               # "waits for me to mean it"
  - name: m-shove-the-gate          # mistake: the fence shares an opinion
    only: perform
    dialog: {choose: "Just shove the gate."}
    mistake: true
    expect: [talking]               # the one sanctioned "with opinions" payoff
    # ...then the canonical match-the-hum lands

  - name: d-the-fence               # detour: flavor
    only: perform
    do: {verb: Examine, object: fence}
    expect: [talking]
  - name: d-the-overlook            # detour: the city dimming (stakes/finale seed)
    only: perform
    do: {verb: Examine, object: overlook}
    expect: [talking]
    hold: 1.5
  - name: d-the-workbench           # detour: the "spare" plant
    only: perform
    do: {verb: Examine, object: workbench}
    expect: [talking]

  - name: m-key-on-fence            # mistake: wrong target for the keys
    only: perform
    do: {verb: Use, object: fence, with: inventory.slot0}
    mistake: true
    expect: [talking]               # generic-decline guard (custom refusal lives on oldCrank/dynamo, not the fence)
  - name: m-one-key-dynamo          # mistake: try the Dynamo with only one key seated
    only: perform
    do: {verb: Use, object: the Great Dynamo, with: inventory.slot0}
    mistake: true
    expect: [talking]               # half-lift then sag: "two keys is two-thirds of a turn"
  - name: m-take-cranks-key         # mistake: yank his key with mine, pre-reveal
    only: perform
    do: {verb: Use, object: oldCrank, with: inventory.slot0}
    mistake: true
    expect: [talking]               # "I'm not winding a stranger with my key."
  - name: m-third-key-now           # mistake: rush the finale with the third key
    only: perform
    do: {verb: Use, object: the Great Dynamo, with: inventory.slot2}
    mistake: true
    expect: [talking]               # "All three at once... that's the finale's problem."
```

Driver note: the `dialog:` primitive (choose a labeled option) is the same support B2/B8 add for the riddle duel and wind-count — Scene 10 reuses it, no new driver capability beyond what the contests already require. Engine-truth check: read the take's `SNTC vrb/objA/objB` console lines (`--debuglevel=1`) to confirm the right object scripts fired, per `docs/NOTES.md`.

---

## 7. Planted/paid ledger

### Plants this scene PAYS (consumes)

| Plant | Source | Paid by |
|---|---|---|
| *"Ask me sometime about the key that winds itself."* | Voltina, Scene 06 (`theater.scc:backstageDoor`; N-A10 disposition) | Old Crank **winds himself** — he is the key that winds itself (step 2, reveal) |
| *Old Crank IS Key #3* | GDD Act 3 | the scene's spine; planted (key in his back, examinable) then paid (reveal + give) **inside the scene**, so it's fair without the Voltina tease |
| *"One key, three slots, a fence in between" / "Even the fence can do that math"* | `midtown.scc:dynamo:UsedWith` | the fence is **here**; the Dynamo has **three slots**; the player brings the keys |
| *"the fence with opinions"* (reserved phrase, NIT) | `midtown.scc:dynamo:LookAt` | the fence, shoved, **shares one opinion** — the phrase's single sanctioned payoff |
| *The Order of the Wind-Up Key* (stencil-only mythology; desk: "exists as one stencil") | crate stencil (`docks.scc`), Rivet lore (`alley.scc`) | the Order's **yard, plaque, and last member** (Crank) finally embodied on screen |
| *"All three together could wind the city back up. Or down."* | `alley.scc:rivet:TalkTo` | the player now **holds all three** — Scene 11 winds up |
| *The power model* (hum winds mainsprings remotely; hand-wind = crude backup) | `docks.scc:board`, Embodiment 2026-06-12 fix | the gate's dead remote-winding → **hand-crank backup**; Crank's **self-winding** is the model's stated exception |
| *The detuning hum / "flat by half a step"* (N-A5, GDD clock) | GDD; `midtown.scc:entry`/`dynamo:LookAt` | the room's **music**, the gate puzzle's **timing source**, and the dry-run **half-step lift** — finally audible at the source |
| *Key #1 + Key #2* | windupKey (S01/S09), secondKey (S06) | the **dry run** (step 4) |

### Plants this scene CREATES (for the finale, Scene 11)

| Created | For |
|---|---|
| `crankKey` (Key #3) in inventory | the finale's three-key rewind |
| The Dynamo's **three-slot interface**, taught by the dry run | the finale's interaction (the player already knows how keys seat) |
| `hum_lift` behavior (keys → pitch up a half-step) | the finale's full restoration — N-A5's drift **reversed**; three keys → all the way to D |
| Old Crank **wound down**, "I'll catch up. Maybe." | the finale's emotional stake — does the restored hum wind him again? |
| The **overlook**: city dimming in patches | the finale's "power down room by room" sequence (GDD Scene 11) |

---

## 8. Embodiment audit (self-review against the desk's fifth chair)

The Embodiment Critic reads its own text. This scene was written **to** the chair, so the audit is a checklist, not a confession:

1. **Power model — consistent and load-bearing.** The single established model (hum winds every mainspring remotely; hand-winding is the crude off-warranty backup) is *the engine of the gate puzzle*: remote winding is dead → the governor ran down → you hand-crank (the backup), and the backup is crude (it fights you; the answer is to match the machine's own tempo). Old Crank is the model's **stated exception, not a contradiction**: he is *self-winding and off-grid* — which is the only thing that makes him a viable third key (a self-winding source can drive the Dynamo rather than draining it) and the only reason a hermit survives the blackout. The line *"I'm off their grid. Have been since before yours."* says the model out loud. The cost is *within* the model: pull a wind-up's key and it stops; give up self-winding and you become dependent on the very hum you're restoring. No "as of today" hand-wave, no new physics.

2. **Sensory claims all have a sensory basis.** The hum is **heard** (Midtown already established it's audible from a distance; up close it's fainter — `Smell` even reports the *absence* of ozone, the sensor noticing nothing, which is fresh and honest). The governor's out-of-time pulse is **seen** (drawn, 2-state flicker). Crank's self-winding key is **seen** (in his back, examinable, named in his LookAt before any reveal). The third slot's size match is **seen** (Dynamo LookAt). The city dimming is **seen** (overlook art draws the dark patches — the brownout the Embodiment desk demanded actually dim what's drawn). No "from the sound of it" reading a silent lock; no smelling a knock-code.

3. **No unsourced protagonist knowledge (the B6 class).** The reveal is **player-earned** through four visible/heard signposts, and where it's spoken it's spoken by **Crank** ("I'm the third key"), not asserted by Sprocket from the GDD. Sprocket does the *math* on screen ("The math finishes itself") rather than knowing the answer cold.

4. **Prop & count continuity.** Three keys, three slots, throughout. Two in pocket (`windupKey`, `secondKey`) + Crank's (`crankKey`) = three. The dry run **returns** the two keys to inventory (stated, with a reason) so the count is honest for the finale; nothing is left in a lock and forgotten. `crankKey` is created exactly once, at the give.

5. **Spatial coherence.** Up the hill from Midtown (the funicular's top), behind the fence the Dynamo was always visible behind; the Dynamo is right/back (the destination), the gate foreground-left (the barrier), the city *below* (the overlook). Matches every prior reference to the district's geography. `wayDown` returns to Midtown silently (room-transition lines say nothing — dub pairing).

6. **Anthropomorphism discipline.** Smell lines avoid the banned `[material] and [abstract noun]` zeugma (B10 do-not-reuse list) — they use recursion ("rust held together by paint held together by rust"), the sensor self-correcting ("and… no. Just brass polish"), absence ("almost no smell at all, which is the whole problem"), and the escalating list ("a streetlamp gives up. Then a sign. Then a whole street"). "With opinions" appears once (the fence, the reserved object). No caps upswing punchlines (caps only on diegetic signage: `GOVERNOR — KEEP TIME`, `ORDER OF THE WIND-UP KEY`). No self-grading buttons (the wind-down ends on the *image* — "ran out of road" — not a narrator's score). No Sprocket act-naming (meta stays the slot-eye's monopoly, and there's no slot-eye here, so there's none).

**Residual risk flagged for the desk:** the give cutscene is the most emotionally direct beat in the game; the danger is the narrator *performing* the sadness (NARRATION rule 1: the script is the comic/the drama, the voice is the straight man). The draft keeps Sprocket's lines flat and lets Crank's ≤12-word direct lines and the wind-down SFX carry it. If a read comes back warm, cut Sprocket's reaction further, never Crank's.

---

*Deliverable ends. Build order suggestion for the implementer: art (`genassets.py`: room, gate 2-state, governor flicker, Dynamo three slots, Crank + key + wound-down pose, overlook dimming, plaque) → `genmusic.py` two hum states → `genaudio.py` four SFX → `dynamo.sch`/`.scc` + `crankKey` in `inventoryitems.*` → wire the gate dialog tree against `Dialog::*` (shared with the B2/B8 contest work) → screenplay shots → editorial desk pass (embodiment sweep included) → validate gate. No scene ships with open BLOCKERs.*