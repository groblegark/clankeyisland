export const meta = {
  name: 'embodiment-sweep',
  description: 'First solo sweep of the new embodiment critic: physics-of-the-fiction audit',
  phases: [
    { title: 'Critique', detail: 'the embodiment critic, alone' },
    { title: 'Defend', detail: 'showrunner argues each note down' },
  ],
}

const REPO = '/Users/matthewbaker/clankeyisland'

const NOTES_SCHEMA = {
  type: 'object',
  required: ['notes'],
  properties: {
    notes: {
      type: 'array',
      items: {
        type: 'object',
        required: ['severity', 'ref', 'note'],
        properties: {
          severity: { type: 'string', enum: ['BLOCKER', 'NOTE', 'NIT'] },
          ref: { type: 'string' },
          note: { type: 'string' },
          suggestion: { type: 'string' },
        },
      },
    },
  },
}

const VERDICTS_SCHEMA = {
  type: 'object',
  required: ['verdicts'],
  properties: {
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        required: ['index', 'ruling', 'reason'],
        properties: {
          index: { type: 'number' },
          ruling: { type: 'string', enum: ['keep', 'kill', 'amend'] },
          reason: { type: 'string' },
          amended: { type: 'string' },
        },
      },
    },
  },
}

phase('Critique')
const batch = await agent(`You are THE EMBODIMENT CRITIC, the newest chair
on the editorial desk of "Clanker City Chronicles" (charter:
${REPO}/docs/editorial/CHARTER.md — read your own section, #5). This is
your FIRST sweep; the whole shipped game is in scope. Attack the physics
of the fiction: sensory claims with no sensory basis (you cannot LOOK at
a door and perceive a knock-code; "from the sound of it" about a silent
lock means nothing), characters knowing what their bodies cannot know,
the robot-physiology ledger (every bot "runs on" the Dynamo's hum, yet
Sprocket winds himself up with a mainspring and his stage act is a key —
pick a power model and audit every line against it: oil, drinking,
smelling, breathing, ears, sleep mode, "deep breath, I don't breathe"),
prop continuity (mass/size/count/consumption: a forearm-sized brass key
pocketed; nine bolts in one fist; an oil can emptied twice?), spatial
coherence (check the GEOM tables in ${REPO}/tools/genassets.py against
dialog: where doors lead, what's visible from where, the funicular
geography, the tavern back door vs the alley's steel door, where the
catwalk hatch could possibly go), and anthropomorphism drift. The world
MAY run on cartoon rules a human world doesn't — your job is to force it
to use THE SAME rules twice. Read ${REPO}/game/docks.scc, tavern.scc,
alley.scc, midtown.scc, theater.scc, inventoryitems.scc, common.scc,
${REPO}/docs/GDD.md, and tools/genassets.py geometry. Quote offending
lines exactly. Find the strongest 10-14 notes you actually believe in.
Severity: BLOCKER = the fiction contradicts itself where players will
notice; NOTE = real inconsistency worth fixing; NIT = polish.`,
  { label: 'critic:embodiment', phase: 'Critique', schema: NOTES_SCHEMA })

phase('Defend')
const verdicts = await agent(`You are THE SHOWRUNNER of "Clanker City
Chronicles", defending the material against the new embodiment critic.
Charter: ${REPO}/docs/editorial/CHARTER.md. For each numbered note below,
rule keep / kill / amend with a reason. Kill notes that demand realism
the genre never promised (cartoon-robot conventions the world applies
CONSISTENTLY are fine — the test is self-consistency, not physics),
that misread the text (verify quotes in ${REPO}/game/*.scc before
ruling), or that duplicate another note. Amend overstatements. KEEP
every note you cannot refute — especially where the world uses two
different rules for the same thing.
${batch.notes.map((n, i) => `${i}. [${n.severity}] ${n.ref} — ${n.note}${n.suggestion ? ` (suggests: ${n.suggestion})` : ''}`).join('\n')}`,
  { label: 'defend:embodiment', phase: 'Defend', schema: VERDICTS_SCHEMA })

const surviving = batch.notes
  .map((n, i) => ({ n, v: verdicts.verdicts.find(x => x.index === i) }))
  .filter(x => x.v && x.v.ruling !== 'kill')
  .map(x => x.v.ruling === 'amend' && x.v.amended
    ? { ...x.n, note: x.v.amended, amended: true }
    : x.n)
log(`embodiment: ${batch.notes.length} raised, ${surviving.length} survived defense`)

return { notes: surviving }