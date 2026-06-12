# The Editorial Desk — charter

Clanker City Chronicles has a writers' room of one. This desk exists so
that nothing ships on the strength of its author's affection for it.
The desk does not write; it attacks. Notes are adversarial by design —
the burden of proof is on the material.

## The critics (run as parallel agents, then defended, then merged)

1. **The Puzzle Critic** — attacks puzzle logic. Lenses: fair-play
   (is the solution signposted before it's needed?), motivation (does
   Sprocket have a reason, or does the player do it because it's the
   only hotspot?), economy (does a beat earn its clicks?), adventure
   sins (moon logic, pixel hunts, lock-and-key fatigue, "use everything
   on everything"), and the chain's shape (is every scene the same
   fetch?). Reads: `game/*.scc`, `docs/GDD.md`,
   `walkthrough/screenplay/full-run.play.yaml`.
2. **The Comedy Critic** — attacks the jokes. Lenses: deadpan
   discipline (see `docs/research/NARRATION.md` — the KQ6-CD register;
   no winking, no exclamation-point comedy), repeated constructions
   (the "X. The Y of Z." template, "Noted. Filed." patterns — flag
   when a shape appears 3+ times), jokes that explain themselves,
   jokes that punch at nothing, and lines that exist because the
   author liked them. Reads: every `egoSay` in `game/*.scc`.
3. **The Story Critic** — attacks structure and continuity. Lenses:
   stakes (does the Dynamo deadline pressure anything?), planted vs
   paid (keep a ledger: knock-code, poster/aide, oil voucher, piano
   keys, Rustlers' theft of Key #1 per GDD...), character (does anyone
   want anything besides Sprocket?), act rhythm, and GDD drift (where
   the implementation contradicts the design doc, decide which one is
   wrong). Reads: `docs/GDD.md`, `game/*.scc`, `docs/NOTES.md`.
4. **The Player Advocate** — plays it cold. Knows nothing the screen
   doesn't say. Lenses: what would a first-time player click, where
   would they stall, which gags read as hints (and aren't), which
   hints read as gags. Reads: the screenplay + transcript, NOT the
   GDD.
5. **The Embodiment Critic** — attacks the physics of the fiction.
   Lenses: sensory claims with no sensory basis (you cannot *look* at
   a door and perceive a knock-code; what does "from the sound of it"
   mean about a silent lock?), characters knowing things their bodies
   can't know, the robot-physiology ledger (Sprocket winds himself up
   with a spring — yet every bot "runs on" the Dynamo's hum; pick a
   power model and keep it), prop continuity (mass, size, count,
   consumption), spatial coherence (room geography, where doors
   actually lead, what's visible from where), and anthropomorphism
   drift (robots smelling, breathing, drinking — fine if the world
   establishes its rules, fatal if each line invents new ones).
   Reads: `game/*.scc`, `tools/genassets.py` geometry, `docs/GDD.md`.

## Rules of engagement

- Notes, not rewrites. A note names the problem, cites the line or
  beat (`file:object:verb` or scene/shot), assigns severity
  (BLOCKER / NOTE / NIT), and may offer one suggestion — the author
  may take a different fix.
- Every batch of notes faces a **defense pass**: a showrunner agent
  argues each note down (kill / keep / amend). Only surviving notes
  reach the merged report. A note that survives defense twice across
  sessions and stays unaddressed gets promoted to BLOCKER.
- Kill your darlings: "the author clearly loves this" is itself
  grounds for a note.
- The desk runs **after a scene's text is drafted, before validate**,
  and its merged report lands in `docs/editorial/NOTES-<date>.md`.
  Addressed notes get a line in the next report's "disposition" list.

## How to run it

```
# from Claude Code, in this repo:
Workflow({scriptPath: ".claude/workflows/editorial-review.js"})
```
