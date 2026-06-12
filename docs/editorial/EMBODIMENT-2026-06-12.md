# Embodiment Critic — first sweep, 2026-06-12

The desk's fifth chair (charter §5), solo inaugural sweep over the
whole shipped game. 10 notes survived the showrunner defense.

### [BLOCKER] docks.scc:board:LookAt ("The Great Dynamo powers every bot on this island. Including me, as of today.") + midtown.scc:dynamo:LookAt ("Every bot on this island runs on that hum. Including me.") vs theater.scc:stage:UsedWith ("I wind myself. Eight full turns. Regulation maximum is five.") + docs/GDD.md (Mayor Piston "steam-powered", Old Crank "hermit wind-up bot")

[BLOCKER] docks.scc:417 ('The Great Dynamo powers every bot on this island. Including me, as of today.') + midtown.scc:337 ('Every bot on this island runs on that hum. Including me.') vs theater.scc:271 ('I wind myself. Eight full turns. Regulation maximum is five.') + docs/GDD.md (Mayor Piston 'steam-powered', Old Crank 'hermit wind-up bot') — The robot-physiology ledger does not balance. Twice, on the critical path, the game asserts every bot runs on the Dynamo's hum — absolutely. Yet 'Including me, as of today' concedes Sprocket ran on something else until this morning (what? how did he switch by stepping off a ferry?); the GDD's mayor runs on steam and Old Crank — a hermit who must survive the very blackout the plot threatens — on clockwork; and the Act 2 centerpiece has Sprocket winding his own mainspring under a regulation ('maximum is five') that only exists if wind-up bodies are commonplace. The stage act itself is consistent (eight turns spent as pure launch, no power consequence — the spring reads as actuator, not life support), but the player has to invent that model; the text never states it, and the absolute 'every bot' claims contradict the off-grid bots the story requires. (suggests: Say the model once, early, where the board already lectures: the Dynamo's hum keeps every mainspring on the island wound remotely — steam, clockwork, and engine bots all run off spring-banked charge — and hand-winding is the crude short-burst backup. That retro-justifies the regulation line, explains 'as of today', and keeps Old-Crank-as-Key-#3 coherent. Then audit 'low-power mode', 'brownouts', and 'runs on that hum' against it.)

**Suggestion:** Pick one model and say it once, early, where the board already lectures: the Dynamo's hum keeps every mainspring on the island wound remotely — steam, clockwork, and engine bots all run off spring-banked charge — and hand-winding is the crude emergency backup (which makes the stage act reckless rather than contradictory, retro-justifies the regulation line, and keeps Old-Crank-as-Key-#3 coherent). Then audit "low-power mode", "brownouts", and "runs on that hum" against it.

### [BLOCKER] tavern.scc:doorBack:Open — "Locked. From the sound of it, there's a knock-code. From the smell of it, I don't want to know."

A sensory claim with no sensory basis, on the exact line the charter names as my founding example. This branch only plays when heardKnockCode is NOT set: Sprocket has heard nothing — the door is locked and silent, and no sound a locked door makes encodes the existence of a knock-code. The Smell half at least has cover (the Smell verb on the same door yields "Rust, secrets, and back-alley grease"); the sound half is the narrator reading the puzzle table. And it matters mechanically: this is the breadcrumb that points the player at the rustlersTable eavesdrop, so the hint for the game's one earned secret rests on a sense with no object.

**Suggestion:** Ground it in something a body could perceive: "Locked. The plate by the door is dented at knuckle height — in a pattern. Somebody knocks here in code." Or let him overhear a muffled CLANG-CLANG admit someone inside while he stands there.

### [BLOCKER] docks.scc:neonSign:LookAt — "POP. 8,011. The comma found its way home. You're welcome, city." vs tools/genassets.py:194 — _neon_text(im, "POP. 8,01,1", ...) painted identically into both sign states (genassets.py:1367-1374 build only sign_on/sign_off from the same text)

[BLOCKER] docks.scc:163 ('POP. 8,011. The comma found its way home. You're welcome, city.') vs tools/genassets.py:194 — _neon_text(im, 'POP. 8,01,1', ...) painted identically into both sign states (genassets.py:1373-1374 crop sign_on/sign_off from the same scene) — The first desk asked for a payoff line confirming the sign got fixed; the line shipped, but the art didn't. Both sign bitmaps still read 8,01,1, so the player examines a sign that visibly says 8,01,1 while Sprocket reads 8,011 off it — a text/screen contradiction parked on the tutorial object every player will Look at twice. (suggests: Add a post-whack sign text state in genassets ('POP. 8,011') keyed off signShookBolt — or keep the art and let the line own it: 'Still 8,01,1. The bolt wasn't load-bearing for the comma. Maintenance is iterative.')

**Suggestion:** Add a third sign text state in genassets (post-whack: "POP. 8,011") keyed off signShookBolt — or keep the art and invert the line: "Still 8,01,1. The bolt wasn't load-bearing for the comma. Maintenance is iterative."

### [NOTE] theater.scc:entry ("And up on the catwalk: one more, with a spyglass.") + theater.scc:stage:UsedWith ("Up on the catwalk, a hatch clicks shut." / "Everyone in this house saw a triumph. I saw a hatch.") vs tools/genassets.py:848-856 GRAND_GEOM + draw_theater (no catwalk, no hatch, no Rustler anywhere in the room art or object table)

[NOTE] theater.scc:64 ('And up on the catwalk: one more, with a spyglass.') + theater.scc:307/311 ('Up on the catwalk, a hatch clicks shut.' / 'Everyone in this house saw a triumph. I saw a hatch.') vs tools/genassets.py:848-856 GRAND_GEOM + draw_theater (no catwalk, no hatch, no Rustler anywhere in the room art or object table) — The catwalk on which the act's biggest story beat is staged exists only in dialog. GRAND_GEOM has seven entries — door, spot booth, chandelier, audience, emcee, stage, stage door — and draw_theater paints exactly those; there is no catwalk structure, no figure, no hatch for the player who goes looking (and after 'I saw a hatch', they will look — and find no hotspot). The heist's physical staging is also untracked: the key's location is never narrated between 'I wind myself' and 'I reach for the key' — he ricochets off the proscenium and lands across the stage — and the grab itself is never shown, under a spotlight whose operator is 'tracking the stage like it owes him money.' (suggests: Draw the catwalk: a strip over the stage in draw_theater with a hatch and a silhouette (the alley fire escape already shows how cheap a lookout is to paint — genassets.py:615). Then track the prop with one line — 'The key is still on the boards where the spring spat it' — and let the grab use a hook on a line from the hatch, mirroring Sprocket's own magnet-on-a-string.)

**Suggestion:** Draw the catwalk: a strip over the stage in draw_theater with a hatch and a silhouette (the alley fire escape already shows how cheap a lookout is to paint). Then track the prop with one line — "The key is still on the boards where the spring spat it" — and let the grab use a hook on a line from the hatch above the stage (mirroring Sprocket's own magnet-on-a-string, which is the kind of rule-reuse this world owes us).

### [NOTE] common.scc:defaultAction:Smell — "My olfactory sensor only detects rust. It is very happy here." vs ~20 scripted Smell lines (tavern.scc:shelf "Esters, additives...", alley.scc:dumpster "Banana oil...", theater.scc:emcee "Pomade.", theater.scc:backstageDoor "Ozone and incense", inventoryitems.scc:oilVoucher "Thermal paper.", midtown.scc:oilBar "Single-origin crude.")

The fallback line states a hardware spec — rust-only olfactory sensor — that every authored Smell line in the game violates. Sprocket distinguishes esters from additives, identifies banana oil, pomade, incense, thermal paper, and grades crude by origin; he is the most sensitive nose in the city except when he sniffs an unscripted object, at which point his own spec sheet contradicts five rooms of evidence. This is distinct from the comedy desk's zeugma census (B10): theirs is about the joke shape, this is about the body. The world has firmly established that Sprocket's nose is a precision instrument; the default un-establishes it on every unhandled object.

**Suggestion:** Rewrite the default to fit the established sensorium: "Nothing my scent library has a match for. Filing it under 'municipal.'"

### [NOTE] alley.scc:rivet:TalkTo ("Gates can count — it's all they do.") vs alley.scc:gate:Use ("I feed it ten. It counts ten, blinks NINE, and spits the dry one back stamped UNCIRCULATED." / "The fare wants money that's suffered.")

[NIT] alley.scc:254 ('Gates can count — it's all they do.') vs alley.scc:454-456 (the gate rejects the dry bolt by condition and stamps it UNCIRCULATED) — The gate's coin-condition rejection is fine: real fare boxes validate as part of counting, and the stamp sits inside the established (and consistently used) perceptive-municipal-hardware rule. But Rivet's 'it's all they do' is an exclusivity claim the gate disproves two screens later. It's character patter from an unreliable salesman, so it's a nit, not a contradiction — still, the cheapest fix in the batch. (suggests: Cut 'it's all they do' from Rivet's line, or bend it: 'Gates can count — counting is most of what they do.')

**Suggestion:** Make the rejection counting-shaped: the slot is gauged for worn bolts and the dry one physically won't drop ("It counts ten. The dry one won't fit the slot — the gauge is worn-bolt-sized. Money has to suffer into circulation here.") — or cut "it's all they do" from Rivet.

### [NOTE] docks.scc:tavernDoor:LookAt ("I can hear a player piano in there, missing several keys.") vs tavern.scc:piano:Use ("The roll plays on through the gaps. Two of the missing keys still sound their notes. The third doesn't.")

The inside line is the best physics in the game — a player piano's roll drives the action behind the keys, so missing keycaps still sound, and only the fully-missing third one leaves a hole. But that same fact convicts the outside line: from the street, by ear, at most ONE absent note is detectable, and "missing keys" can't be heard at all — only missing notes can. Sprocket audits the keyboard through a closed door using information his ears cannot carry, and the game itself proves it two rooms later.

**Suggestion:** Outside: "I can hear a player piano in there. There's a hole in the tune it keeps not noticing." — which also plants the inside observation instead of pre-spoiling it.

### [NOTE] docks.scc:entry — "The streetlights pick that moment to dim. All of them. Together. Like the city skipped a heartbeat." vs tools/genassets.py:120-302 draw_scene (no streetlights exist on the docks: mooring posts, neon sign, tavern window, skyline windows — and nothing scripted dims during the cutscene)

The premise beat — added last sweep as unskippable, so every player sees it — narrates an event on hardware the screen doesn't have. The docks background contains no streetlights, and no setObjectState or palette trick dims anything while the line plays; Sprocket reports a city-wide brownout while the art holds perfectly steady. For the one line whose whole job is "the city skipped a heartbeat," the city visibly doesn't.

**Suggestion:** Dim what's drawn: flick the neon sign to its off state and back during the line (signFlicker's machinery already does this) and name what exists — "The sign, the tavern window, the lights across the water — all of them dip. Together."

### [NIT] docks.scc:crate:LookAt/Use — "Ominous AND conveniently plot-relevant. Also twenty feet up." / "It's twenty feet up. My arms are stock parts." vs tools/genassets.py:102-117 GEOM["CRATE"]=(120,48,24,72), hanging state drawn at top (y≈50-65) over dock surface at y=84

The text claims twenty feet, twice; the art hangs the crate roughly half a sprite-height above the planks (Sprocket's costume canvas is 34px tall, the gap is ~19px). On screen it dangles at head height, comfortably pokeable, and the player who measures by eye will wonder why stock arms can't reach it.

**Suggestion:** Either hoist the hanging state to the crane arm's actual height in the art, or let the line own the truth: "It's eight feet up. Fine — four. My arms are stock parts and the principle is load-bearing."

### [NIT] midtown.scc:theater:LookAt ("Two of the bulbs are out. Forty-one of them aren't.") + theater.scc:chandelier:LookAt ("Forty-one sockets, thirty-eight working.") + theater.scc:entry ("Forty bots") vs tools/genassets.py:789-791 (≈36 marquee bulbs, every third one drawn dim), 882-887 (≈7 chandelier lights), 906-916 (≈14 audience heads)

[NIT] midtown.scc:182 ('Two of the bulbs are out. Forty-one of them aren't.') vs tools/genassets.py:789-791 (~36 marquee bulbs drawn, every third one dim) — The marquee's bulbs are individually drawn and countable, and the art encodes a different fact than the line: roughly a third of them are dark, while Sprocket reports exactly two out (of a claimed 43). Unlike the chandelier's 41 sockets or the forty-bot house — lo-fi shorthand no player will audit — the marquee's out-ratio is visible at a glance and contradicts the claim. (suggests: Either make the art agree (two dim bulbs) or blur the line to what's drawn: 'A third of the bulbs are out. The rest are compensating.')

**Suggestion:** Count what's drawn, or blur the claims to ratios the art can survive ("all but two", "most of its sockets"). Reserve exact numbers for things off screen.

---

## Dispositions (author, 2026-06-12, same day)

All fixed, same day:
- **Physiology BLOCKER** — the power model is now stated once, where the
  board lectures: the hum winds every mainspring on the island remotely;
  hand-winding is the crude off-warranty backup. The stage act is now
  reckless instead of contradictory.
- **Knock-code BLOCKER** (the chair's founding example) — the door no
  longer sounds like a protocol; the plate beside it is dented at
  knuckle height, in a pattern.
- **Sign BLOCKER** (pass-1 regression) — the line now agrees with the
  art: "Still POP. 8,01,1. The bolt wasn't load-bearing for the comma.
  Maintenance is iterative."
- **Catwalk NOTE** — the catwalk, hatch, and watcher are now painted in
  draw_theater; the heist tracks the key prop and the grab is a hook on
  a line — somebody else's magnet-on-a-string.
- **Smell-spec NOTE** — the default fallback no longer claims a
  rust-only sensor the whole script contradicts.
- **Gate-gauge NOTE** — the slot gauge is worn-bolt-sized; money here
  has to have suffered.
- **Tavern-door NOTE** — you hear the hole in the tune, not the missing
  keys.
- **Brownout NOTE** — the arrival dimming now dims the screen (the neon
  sign drops to its off state on the line) and names what's drawn.
- **Both counting NITs** — exact numbers blurred to ratios the art can
  survive; the crate is "up a crane."
