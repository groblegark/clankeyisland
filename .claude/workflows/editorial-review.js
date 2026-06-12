export const meta = {
  name: 'editorial-review',
  description: 'Adversarial editorial pass: puzzle/comedy/story critics + player advocate, defended, then merged',
  whenToUse: 'After drafting a scene, before validate. See docs/editorial/CHARTER.md.',
  phases: [
    { title: 'Critique', detail: 'four critics attack in parallel' },
    { title: 'Defend', detail: 'a showrunner argues each note down' },
    { title: 'Merge', detail: 'surviving notes ranked into one report' },
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
          ref: { type: 'string', description: 'file:object:verb, scene/beat, or line quote' },
          note: { type: 'string', description: 'the attack: what is wrong and why it matters' },
          suggestion: { type: 'string', description: 'optional: one possible fix' },
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
          amended: { type: 'string', description: 'if amend: the corrected note' },
        },
      },
    },
  },
}

const COMMON = `You are a critic on the editorial desk of "Clanker City
Chronicles", a homebrew SCUMM v6 comedy adventure (Monkey Island / Day of
the Tentacle register; the narrator is Sprocket, a deadpan maintenance-bot
reporting everything secondhand). Your charter: ${REPO}/docs/editorial/CHARTER.md
(read it first). Also read the PREVIOUS report and its disposition ledger
at ${REPO}/docs/editorial/NOTES-2026-06-12.md if it exists: do NOT re-raise
a note marked fixed unless the fix on the page is inadequate (then say so,
citing the new text); DO audit whether fixes introduced regressions; notes
marked deferred may be re-raised only if their absence newly bites. You are
ADVERSARIAL: the material must justify itself. Do not pad; do not praise;
find the strongest 8-12 notes you actually believe in, not a quota. Cite
precisely. Severity: BLOCKER = would make a player quit or a reviewer
wince; NOTE = real weakness worth fixing; NIT = polish.`

phase('Critique')
const critics = [
  {
    key: 'puzzles',
    prompt: `${COMMON}
You are THE PUZZLE CRITIC. Attack the puzzle design: fair-play
signposting, motivation, economy, moon logic, lock-and-key fatigue,
sameness of shape across scenes. The implemented chain so far:
docks (bolt, poster) -> tavern (bolt shims servo -> token -> darts ->
oil can) -> docks (oil Betty -> crate -> wind-up key) -> alley (dumpster
magnet -> fish 9 bolts -> gate blinks NINE -> riddle duel -> 10th bolt ->
funicular fare) -> Midtown (sign up for talent night, key as the act) ->
the Grand Cog (wake the spotlight operator -> perform -> win voucher +
backstage pass -> the Rustlers steal the key mid-ovation -> stage door).
Scene 05 (theater.scc) is NEW since the last report — weigh it hardest.
Read ${REPO}/game/docks.scc, tavern.scc, alley.scc, midtown.scc,
theater.scc, inventoryitems.scc, ${REPO}/docs/GDD.md and
${REPO}/walkthrough/screenplay/full-run.play.yaml. Return your notes.`,
  },
  {
    key: 'comedy',
    prompt: `${COMMON}
You are THE COMEDY CRITIC. Attack the jokes: deadpan discipline per
${REPO}/docs/research/NARRATION.md, repeated joke shapes (flag any
construction used 3+ times across files — e.g. "X. The Y of Z.",
"Noted. Filed.", personified objects, "...That feels thematically
significant"), jokes that explain themselves, gags that are really
exposition, and lines the author obviously loves. Scene 05
(theater.scc) is NEW since the last report — weigh it hardest. Read
every egoSay in ${REPO}/game/docks.scc, tavern.scc, alley.scc,
midtown.scc, theater.scc, inventoryitems.scc, common.scc. Quote
offending lines exactly. Return your notes.`,
  },
  {
    key: 'story',
    prompt: `${COMMON}
You are THE STORY CRITIC. Attack structure and continuity. Build the
planted/paid ledger (knock-code, poster + City Hall aide, oil voucher,
piano's missing keys, "one of three" keys, GDD's claim that the
Rustlers stole Key #1, Rivet's hint economy, the Dynamo going flat) and
flag plants with no scheduled payoff or payoffs with no plant. Check
GDD drift: ${REPO}/docs/GDD.md vs the implemented scenes (both were
revised after the last report — verify they now agree, especially the
Key #1 theft at the Grand Cog). Check stakes and escalation. Scene 05
(theater.scc) is NEW since the last report — weigh it hardest,
including whether the heist beat is earned and what it does to
Sprocket's goal structure. Read the GDD, ${REPO}/game/*.scc room
files, and ${REPO}/docs/NOTES.md. Return your notes.`,
  },
  {
    key: 'player',
    prompt: `${COMMON}
You are THE PLAYER ADVOCATE. You know NOTHING the screen does not say.
Do not read the GDD. Read only ${REPO}/walkthrough/screenplay/full-run.play.yaml
(the optimal path) and ${REPO}/walkthrough/stage/docks.transcript.json
(every line a player can see, keyed by object and verb). Simulate a
cold first play of each scene: what would you click first, where do
you stall, which solution would you never try without brute force
(e.g. would a player think to USE the bolt ON the bartender? to GIVE
a token to a dart player? to USE a key ON a box office?), which
flavor lines read as false hints, and where the hint chain has gaps.
Return your notes.`,
  },
]

const batches = await parallel(critics.map(c => () =>
  agent(c.prompt, { label: `critic:${c.key}`, phase: 'Critique', schema: NOTES_SCHEMA })
    .then(r => r && { key: c.key, notes: r.notes })))

const live = batches.filter(Boolean)

phase('Defend')
const defended = await parallel(live.map(b => () =>
  agent(`You are THE SHOWRUNNER of "Clanker City Chronicles", defending the
material against the ${b.key} critic. Charter: ${REPO}/docs/editorial/CHARTER.md.
For each numbered note below, rule keep / kill / amend with a reason.
Kill notes that misread the text, demand a different game, duplicate
another note in this batch, or punish intentional running gags that are
still under the 3-use budget (verify counts in ${REPO}/game/*.scc before
ruling). Amend notes that are right but overstated. KEEP every note you
cannot actually refute — bias toward keeping BLOCKERs; do not protect
darlings.
${b.notes.map((n, i) => `${i}. [${n.severity}] ${n.ref} — ${n.note}${n.suggestion ? ` (suggests: ${n.suggestion})` : ''}`).join('\n')}`,
    { label: `defend:${b.key}`, phase: 'Defend', schema: VERDICTS_SCHEMA })
    .then(v => v && {
      key: b.key,
      notes: b.notes
        .map((n, i) => ({ n, v: v.verdicts.find(x => x.index === i) }))
        .filter(x => x.v && x.v.ruling !== 'kill')
        .map(x => x.v.ruling === 'amend' && x.v.amended
          ? { ...x.n, note: x.v.amended, amended: true }
          : x.n),
    })))

const surviving = defended.filter(Boolean)
log(`surviving notes: ${surviving.map(b => `${b.key}=${b.notes.length}`).join(', ')}`)

phase('Merge')
const report = await agent(`You are the desk editor merging the surviving
editorial notes for "Clanker City Chronicles" (charter:
${REPO}/docs/editorial/CHARTER.md) into one markdown report. Dedup notes
that attack the same line/beat from different angles (keep the sharpest
phrasing, credit both desks). Order: BLOCKERs, then NOTEs grouped by
scene/file, then NITs as a terse list. For each item keep: severity,
the precise ref, the note, the suggestion if any, and which desk(s)
raised it. Start the report with a 4-6 line "state of the show" summary
in the desk's dry voice. Return ONLY the markdown body (no preamble) —
it will be committed verbatim as docs/editorial/NOTES-<date>.md.
${JSON.stringify(surviving)}`,
  { label: 'merge', phase: 'Merge' })

return { report, counts: surviving.map(b => ({ desk: b.key, kept: b.notes.length })) }
