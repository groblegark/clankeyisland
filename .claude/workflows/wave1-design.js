export const meta = {
  name: 'wave1-design',
  description: 'Wave 1: design every remaining scene + the two pillar spikes, massively parallel',
  phases: [
    { title: 'Design', detail: 'six scene designers + two spikes' },
  ],
}

const REPO = '/Users/matthewbaker/clankeyisland'

const SCENE_COMMON = `You are designing a scene for "Clanker City
Chronicles", a homebrew SCUMM v6 comedy adventure. REQUIRED READING, in
order: ${REPO}/docs/PRODUCTION-PLAN.md (the roadmap and your scene's
row), ${REPO}/docs/GDD.md (canon), ${REPO}/docs/NOTES.md (engine
pitfalls — verb ids, owner==VAR_EGO, dub source-order, silent room
transitions), ${REPO}/docs/editorial/CHARTER.md + the three reports in
docs/editorial/ (the desk's standards: fair-play signposting, no
vending-machine NPCs, no self-grading punchlines, smell-template ban,
embodiment self-consistency, THE CONTESTS MUST BE PLAYABLE — design at
least one beat with real player agency), ${REPO}/docs/research/NPC-DIALOG.md
(NPCs may now speak short direct punchlines; Sprocket keeps narration),
and 2-3 existing rooms in ${REPO}/game/*.scc for voice and structure
(tavern.scc and theater.scc are the best models). Your deliverable is a
COMPLETE markdown design doc: (1) scene goal + how it advances the
three-keys spine; (2) the puzzle chain as a numbered graph with every
hint's source named (fair-play audit included) and one playable-agency
beat; (3) object table: name, rect sketch on the 320x144 stage,
verbs, states; (4) full dialog draft in the game's actual deadpan
register (reported speech default, NPC direct punchlines <=12 words
where they earn it) — write ALL the lines, not summaries; (5) music
brief (genmusic.py idiom: bars, BPM, key, loop point) + SFX list
(genaudio.py idiom); (6) walkthrougher beats: canonical validate shots
AND streamer-mode detours/mistakes; (7) planted/paid ledger entries it
consumes and creates; (8) embodiment audit of its own text (power
model: the hum winds mainsprings remotely; hand-winding is crude
backup). Be exhaustive — this doc is what the implementer builds from.`

phase('Design')
const jobs = [
  ['scene-06', `${SCENE_COMMON}
SCENE 06 — BACKSTAGE: MADAME VOLTINA. The fortune-telling tesla-coil
bot, first costumed talking actor (her talk animation is coil arcs —
design her look for genassets). Canon obligations: she guards Key #2;
she says the Rustlers' motive out loud (they mean to ransom the rewind
— GDD); she plants Old Crank ("the key that winds itself", her stage-door
tease already exists); she echoes the knock-code so Act 3's lock is in
every player's head; Sprocket arrives key-less and robbed. Her price
for Key #2 should NOT be a fetch — the desk demands agency: design a
fortune-telling beat with real choices (her cards/coils read the
player's actual playthrough — the walkthrougher state flags make this
technically free). Output the complete design doc.`],
  ['scene-07', `${SCENE_COMMON}
SCENE 07 — THE OIL BAR, INSIDE. The voucher finally beats the velvet
rope. Canon obligations: City Hall's aides drink here and talk (the
expose thread — the aide who feared the poster); uptown society comedy
(the bouncer, the sommelier of crude); a beat that advances the Mayor
Piston cover-up with evidence the player ACTS on, not watches. Mind
N-M4's promise: the bouncer already validates the voucher "tonight
it's at capacity" — your scene opens that rope. Output the complete
design doc.`],
  ['scene-08', `${SCENE_COMMON}
SCENE 08 — CITY HALL: MAYOR PISTON. The steam-powered mayor who denies
everything, confronted with the exposé. Canon obligations: the official
notice (the poster the player has carried since Scene 01) pays off; the
nine-degrees aide; Piston's steam physiology must obey the power model
(steam bot, spring-banked by the hum — the embodiment chair will
check); outcome positions Act 3 (he knows the Dynamo is failing and
knows about the Order). Design the confrontation as a playable beat
(dialog tree or evidence-presentation), not a cutscene. Output the
complete design doc.`],
  ['scene-09', `${SCENE_COMMON}
SCENE 09 — THE RUSTLERS' HIDEOUT (Act 3 opens). The tavern back door +
the knock-code, finally. Canon obligations: recover Key #1; the ransom
plot surfaces (their leader gets a face and a want); the slot-eye gag
pays off from the inside; the heist's hook-on-a-line tackle reappears
(rule-reuse); stealth-or-talk player choice preferred over a fetch.
The hideout is BEHIND the tavern's east wall (geometry: tavern doorBack
at x=288; design the room as the space between tavern and alley).
Output the complete design doc.`],
  ['scene-10', `${SCENE_COMMON}
SCENE 10 — DYNAMO DISTRICT: OLD CRANK. Up the hill, behind the fence
with opinions. Canon obligations: Old Crank the hermit wind-up bot IS
Key #3 (his key fits the Dynamo) — the reveal must be planted-then-paid
within the scene AND retro-supported by Voltina's "key that winds
itself"; the fence/gate entry puzzle; the Dynamo up close (the hum,
nearly gone); Crank's choice to give himself must cost something.
Output the complete design doc.`],
  ['scene-11', `${SCENE_COMMON}
SCENE 11 — THE FINALE: REWIND THE DYNAMO. The GDD's set piece: rewind
while the city powers down around you, room by room. Design the
power-down as revisits of existing rooms going dark (object states +
music dropping out — the detuning hum's payoff), the three keys used
in sequence (three slots — the fence could do that math), a final
player action that matters, and the ending beat(s) + credits gag.
Also specify the genmusic detuning mechanism (act-flag pitch drift)
concretely. Output the complete design doc.`],
  ['voice-spike', `You are running a feasibility spike for IN-GAME PCM
VOICES in "Clanker City Chronicles" (SCUMM v6 via ScummC, played in
ScummVM-wasm). Investigate, with file:line evidence: (1) ScummC's
voice support — grep ${REPO}/vendor/scummc for 'voice', 'sou',
'monster' (scc parser voice decls? sld's tentacle.sou emission — the
game Makefile already does 'cp tentacle.sou monster.sou'); how does a
say-line reference a voice clip (egoSay voice syntax in scc grammar)?
(2) ScummVM side: how DOTT plays monster.sou (engines/scumm — VOC
chunks? talkSound offsets?), what ini/flags select speech vs text
(speech_mute, subtitles). (3) The wasm build: does our build-web.sh
ship .sou (check tools/build-web.sh — it copies tentacle.000/.001
only). (4) The pipeline shape: walkthrough/post/dub.py already renders
per-line piper+FX WAVs cached by text hash — design the build step
that renders every transcript line and packs monster.sou (sample
format VOC 8-bit unsigned mono per docs/research/AUDIO.md rules?).
Deliver: docs/research/INGAME-VOICE.md content — feasibility verdict,
the exact mechanism, a minimal end-to-end prototype plan (one line of
Sprocket speaking in the browser), risks, and effort estimate.`],
  ['streamer-spike', `You are designing STREAMER MODE for the
walk-through-er of "Clanker City Chronicles" — the performer should
play like a curious human, not a proof: explore, examine the funny
things, try reasonable-but-wrong combinations first, get the gag, then
solve. Read ${REPO}/walkthrough/driver/walkthrough.py (shot schema,
modes, expectations, line pairing — note the per-(object,verb)
source-order pairing contract in docs/NOTES.md), the screenplay
${REPO}/walkthrough/screenplay/full-run.play.yaml, walkthrough/post/render.py
+ dub.py (the film pipeline), and the editorial reports' catalogued
fair mistakes (key-on-piano, nine-bolts-at-gate, give-bolt-to-Gusket,
voucher-at-the-rope). Design: (1) screenplay schema additions —
detour: and mistake: shot types (expectations = the refusal line
observed), pacing/hold conventions, chapter markers per scene for
render.py title cards; (2) how mistake shots interact with line
pairing WITHOUT breaking it (the refusal lines are mid-list — does
per-shot front-pairing mislabel them? propose the fix: pairing by
(object,verb) cursor? speaker tags? explicit line: field on the
shot?); (3) a wander mechanic (walk-to shots, idle holds) that reads
as curiosity on film; (4) the full Act One streamer screenplay as a
concrete example, beat by beat, with timing estimates; (5) driver
diff list. Deliver: docs/research/STREAMER-MODE.md content, complete.`],
]

const results = await parallel(jobs.map(([key, prompt]) => () =>
  agent(prompt, { label: key, phase: 'Design' }).then(r => ({ key, doc: r }))))

return { docs: results.filter(Boolean).map(r => r.key) , results: results.filter(Boolean) }