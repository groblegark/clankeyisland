# Scene 01 — The Docks of Clanker City

**Act:** 1 · **Background:** `assets/backgrounds/docks.png` (320x200)

The opening scene. Sprocket steps off a rusting cargo ferry onto the docks.
Rain of fine metal filings. A flickering neon sign reads
"WELCOME TO CLANKER CITY — POP. 8,01,1" (the digit display is broken).

## Layout (left → right)

1. **Ferry ramp** — arrival point. The ferry immediately breaks down behind
   you (no going back; classic).
2. **Cargo crane** — inert. Operator bot **Boom-Arm Betty** is out of oil and
   frozen mid-lift, dangling a crate the player will eventually need.
3. **Rivet's scrap stall** — Rivet sells hints and junk for bolts.
4. **The Scrap & Barrel** — tavern door (exit to Scene 02).
5. **Notice board** — exposition: "DYNAMO MAINTENANCE: NOTHING IS WRONG.
   — Mayor Piston". Examining it kicks off the main quest.

## Hotspots & interactions

| Hotspot | Examine | Interact |
|---|---|---|
| Neon sign | "Population eight-oh-one-comma-one. Punctuation is dying first." | Sparks shower; a loose **bolt** drops (first currency!) |
| Boom-Arm Betty | "Frozen mid-yawn. Or mid-lift. Hard to tell." | Needs **oil can** → unfreezes, drops the crate, opens crane puzzle |
| Crate (dangling) | "Property of the Order of the Wind-Up Key." | Unreachable until Betty is oiled |
| Rivet's stall | "One bot's trash is this bot's entire business model." | Dialog: hints, buy **magnet on a string** (5 bolts) |
| Notice board | Triggers quest flag `knows_about_dynamo` | Tear off poster → inventory item (evidence for Act 2) |
| Storm drain | "Something glints down there." | **Magnet on a string** → fish out 4 bolts |

## Puzzle chain (Act 1 opener)

neon sign → 1 bolt → can't afford magnet → talk to Rivet → odd jobs →
sweep filings (3 bolts) → 4 bolts... still short → notice the storm drain →
buy nothing yet → tavern (Scene 02) earns oil can → oil Betty → crate drops →
crate contains 6 bolts + **Rustler map fragment** → buy magnet → drain bolts →
fully funded for Rivet's riddle-duel.

## Ambient animation

- Neon sign flicker (3-frame loop)
- Steam from a manhole, 8-frame loop
- Betty's eye-lights blink S.O.S. in morse (easter egg)
