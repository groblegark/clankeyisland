export const meta = {
  name: 'npc-dialog-investigation',
  description: 'Investigate giving NPCs real dialog + talk animation: engine, art, voices, writing',
  phases: [
    { title: 'Investigate', detail: 'four specialists in parallel' },
    { title: 'Synthesize', detail: 'one design doc with a recommendation' },
  ],
}

const REPO = '/Users/matthewbaker/clankeyisland'

const COMMON = `You are investigating a design change for "Clanker City
Chronicles", a homebrew SCUMM v6 adventure built with ScummC (vendored at
${REPO}/vendor/scummc — sources + examples/openquest are readable; ScummVM
source at ${REPO}/vendor/scummvm-src). Current state: ALL dialog is the
player character Sprocket reporting NPC speech secondhand (one voice, one
talk color 105/106). NPCs (Gusket, Flange, Rivet, the emcee, the box-office
clerk, Madame Voltina next scene) are PAINTED INTO THE BACKGROUND as
objects with rects — only Sprocket is a real SCUMM actor with a costume.
The question: what would it take for NPCs to speak their own lines, with
some kind of talk animation, and per-character voices in the dub? Read
${REPO}/docs/NOTES.md first (operational brain-dump), and cite concrete
file:line evidence for engine claims. Your final text is data for a
synthesizer, not prose for a human: be dense, specific, and honest about
costs and risks.`

phase('Investigate')
const findings = await parallel([
  () => agent(`${COMMON}
ENGINE MECHANICS. Investigate how non-ego speech works in SCUMM v6 via
ScummC: actorSay() for other actors (see ${REPO}/game/common.scc,
verbs.scc, dialog.scc and vendor/scummc/examples/openquest — openquest
HAS a second actor with dialog; study exactly how), talk colors per
actor (setTalkColor?), text positioning over the speaker, what
egoSay/actorSay compile to, and the dialog-tree machinery in
game/dialog.scc + dialog.sch (currently unused — how does it present
choices and who speaks). Also: can a BACKGROUND OBJECT 'speak' without
being an actor — print/say opcodes positioned at coordinates, e.g.
actorSay(0xFF,...) or printAt? Check what VAR_TALK_ACTOR / talk-state
vars exist for animation hooks. Deliver: the exact mechanisms available,
with scc API names and an openquest citation for each, plus the
minimal-change option vs the full-actor option.`,
    { label: 'engine', phase: 'Investigate' }),
  () => agent(`${COMMON}
ART & ANIMATION. Two routes to investigate concretely: (A) promote NPCs
to real actors — study ${REPO}/game/costumes/*.scost, tools/genassets.py
gen_sprocket_frames (the existing costume pipeline: 20x34 frames, 32-color
window at palette 224+, cost compiler in game/Makefile), and estimate
per-NPC cost (frames needed for stand+talk only, no walking); note the
costume palette window is SHARED (one 32-slot window) — can multiple
costumes coexist? Check ScummC cost format docs/source. (B) keep NPCs
painted + animate mouth flaps via object states — study how the docks
neonSign flicker works (docks.scc signFlicker + states) and how the
crate/dumpster/gate/marquee state swaps work; could a talk loop toggle
a 2-state mouth crop while a line displays, and what would genassets
need to emit? Deliver: per-route cost estimate (files touched, new
assets, risks like palette collisions), and which NPCs are even visible
enough for flaps (Gusket 32x40, Flange 24x48, Rivet 32x48, emcee 24x48,
clerk inside a 24x32 booth).`,
    { label: 'animation', phase: 'Investigate' }),
  () => agent(`${COMMON}
VOICES & THE DUB PIPELINE. Study ${REPO}/walkthrough/post/dub.py (piper
TTS + ROBOT_FX chain, voice cache keyed by text+fx hash),
walkthrough/driver/walkthrough.py (talk-segment detection: TALK mask =
palette colors 105/106 only — see stage probes in tools/genassets.py),
and tools/transcript.py (lines keyed by object+verb, no speaker field).
Investigate: (1) if each character got a distinct SCUMM talk color,
could the driver attribute each talk segment to a speaker by sampling
the text color, and what changes does that need in the mask/timeline?
(2) piper voice catalog actually installed/available locally (check
~/.cache or piper docs — run 'python3 -c \"import piper\" ' probes or ls
the voices dir; also check what dub.py downloads) — list candidate
voices for: gravelly bartender, smug dockworker, fast-talking dealer,
showbiz emcee, ethereal fortune-teller; (3) transcript format change to
carry a speaker tag per line (e.g. parsing a convention like
npcSay(gusket, ...) or a line-prefix marker). Deliver: a concrete
pipeline design with the smallest diff, and what breaks (the frame-sync
snapper, the dubsheet, the voice cache).`,
    { label: 'voices', phase: 'Investigate' }),
  () => agent(`${COMMON}
WRITING & COMEDY REGISTER. Read ${REPO}/docs/research/NARRATION.md (the
deadpan doctrine), docs/editorial/CHARTER.md, both editorial reports in
docs/editorial/, and the dialog in game/tavern.scc, alley.scc,
midtown.scc, theater.scc. The reported-secondhand voice is load-bearing
comedy ("He says I look like I've had a hard drive, pal") — but it also
caused real editorial findings (every NPC is a vending machine; nobody
wants anything; quoted-speech-inside-narration is doing three jobs).
Investigate: which existing beats would IMPROVE as direct NPC dialog
(candidates: Rivet's fact-selling, the emcee's patter, the slot-eye's
"Act Three, buddy", Voltina — who NEEDS her own voice in Scene 06?),
which would die (the dart hustle's reported absurdity), and what hybrid
rules preserve the register (e.g. NPCs get SHORT direct lines, Sprocket
keeps all narration and never quotes verbatim what we just heard).
Check how Monkey Island/KQ6 handle narrator-vs-NPC register per
NARRATION.md. Deliver: a style rule proposal + a ranked conversion list
with 3 example rewrites (before/after) in the game's actual voice.`,
    { label: 'writing', phase: 'Investigate' }),
])

phase('Synthesize')
const doc = await agent(`You are synthesizing four specialist
investigations into ONE design doc for "Clanker City Chronicles":
docs/research/NPC-DIALOG.md. Structure: (1) a 6-line executive summary
with a single recommendation (which mechanism, which animation route,
which voice design, which writing rules — the smallest coherent package
that ships); (2) the engine mechanism chosen, with the rejected
alternatives and why, citing the engine findings' file:line evidence;
(3) the animation plan per NPC; (4) the dub pipeline changes as a
numbered diff list; (5) the writing rules + the ranked conversion list
with the example rewrites; (6) an implementation checklist ordered so
the walkthrougher stays green at every step (this repo ships behind a
validate gate, and per docs/NOTES.md dub pairing reads source order —
flag every step that touches it); (7) open questions for the author.
Keep the repo's dry documentation voice. Return ONLY the markdown body.
The four investigations:
=== ENGINE ===
${findings[0]}
=== ANIMATION ===
${findings[1]}
=== VOICES ===
${findings[2]}
=== WRITING ===
${findings[3]}`,
  { label: 'synthesize', phase: 'Synthesize' })

return { doc }