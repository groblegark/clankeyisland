# Clanker City Chronicles — Game Design Document

## Logline

A rookie maintenance-bot named **Sprocket** arrives in Clanker City with a
dream and not so much as an oil can to his name, only to discover the
**Great Dynamo** — the machine heart that powers every robot on the island —
is winding down. Sprocket has three days (of in-game story, not real time)
to find the three lost **Keys of Clankey Island** and rewind the city
before everyone grinds to a halt.

Tone: Monkey Island-style comedy. Verb-based or two-click point-and-click.
Nothing can kill you; every failure is a joke.

## Setting: Clanker City

A robot metropolis stacked in three tiers:

1. **The Docks** — rusty harbor district where Sprocket arrives. Cargo cranes,
   the Scrap & Barrel tavern, ferry to the mainland (broken, naturally).
2. **Midtown Gearworks** — neon main street. Shops: Lefty's Spare Parts,
   the Oil Bar, City Hall (run by Mayor Piston), the Grand Cog Theater.
3. **The Dynamo District** — uptown, fenced off, humming. Home of the Great
   Dynamo and the mysterious Order of the Wind-Up Key.

## Main Characters

| Character | Role |
|---|---|
| **Sprocket** | Player character. Eager rookie maintenance-bot, too small for his wrench. |
| **Mayor Piston** | Blustery steam-powered mayor. Denies the Dynamo is failing. |
| **Rivet** | Dockside scrap-dealer. Knows everything, sells hints for bolts (currency). |
| **Madame Voltina** | Fortune-telling tesla-coil bot at the Grand Cog Theater. |
| **The Rustlers** | Gang of corroded pirate-bots who steal the first Key — mid-ovation, at the Grand Cog. Their game: a city that can be wound down can be billed for winding back up. They mean to ransom the rewind. (Voltina says this out loud in Act 2.) |
| **Old Crank** | Hermit wind-up bot who remembers when the Dynamo was built. |

## Act Structure

- **Act 1 — The Docks:** Arrive, learn the Dynamo is failing, earn 10 bolts,
  out-riddle Rivet, recover **Key #1** from a crate the Order of the Wind-Up
  Key shipped as deck cargo. (A Rustler lookout watches the whole thing.)
- **Act 2 — Midtown (SHIPPED, Scenes 04-07):** Win the Grand Cog talent
  show to get backstage — the act is **a playable wind-count contest**, and
  the bold winning turn also advertises Key #1 on a lit marquee, which is
  how the Rustlers know to steal it mid-ovation. Madame Voltina guards
  **Key #2** behind **the three-card Reading**: the player answers Past /
  Present / Future cards with the items their own playthrough carries (the
  notice, the voucher), and Card III is a confession — the truth about the
  heist — that wins the key. The talent-night oil voucher opens the **Oil
  Bar** via the velvet-rope ordering gate (gated on holding Key #2, so the
  Reading must come first); inside, a **two-round oil-sommelier contest**
  (planted by the cellar list + the City Hall aide) and a **cancelled
  Dynamo work order** whose *Technician of record: O. CRANK* is the first
  WRITTEN plant that Old Crank is Key #3 and was fired for logging the
  truth. The work order is **Act-3 leverage with Crank**, not a Mayor
  errand (no City Hall confrontation is scheduled — if one is ever added,
  the loaded nine-degree door + work order is the obvious lock-and-key).
- **Act 3 — Dynamo District (planned):** Recover **Key #1** from the
  Rustlers' hideout — the tavern back door, the eavesdropped knock-code
  finally paying off. The cancelled work order clears Old Crank's name and
  earns his trust; he reveals he *is* **Key #3** (his wind-up key fits the
  Dynamo). DEFERRED PLANTS TO CASH HERE: the tavern piano's three missing
  keys (one "missing entirely" = a person), and the detuning hum /
  three-day deadline (designed in Core Mechanics, not yet escalating).
  Final sequence: rewind the Dynamo while the city powers down around you,
  room by room.

## Core Mechanics

- Nine-verb SCUMM v6 interface (ScummC), Day-of-the-Tentacle style.
- One inventory combination puzzle, minimum: the dumpster magnet splits into bare magnet + string in the Scene 09 prep pass (string from Rivet's junk heap; the tackle reused for the hideout stealth route). Decided 2026-06-12, third desk pass (N-A17) -- no more 'ideally'.
- **Bolts** as currency for a small economy in Act 1.
- Dialog trees with insult-fencing-style riddle duel vs. Rivet.

## Art Direction

- 320x200, chunky pixel art, big readable silhouettes.
- Palette: rust oranges + teal neon + sodium-lamp yellow.
- Every background needs at least one animating element (steam, neon flicker,
  rotating gear) to keep the city feeling alive.

## Audio

- Jazzy mechanical swing ("the Clanker City Shuffle") for Midtown.
- Foghorns and creaking metal for the Docks.
- The Dynamo's hum is a musical drone that detunes as the game progresses.
