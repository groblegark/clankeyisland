# Production plan — finishing Clanker City Chronicles

Adopted 2026-06-12. The goal: the complete game, Acts 1-3, start to
finish, plus the three pillars Matt set for the final product:

1. **In-game synth voices** (stretch): real PCM speech inside the game —
   per-line TTS packed into `monster.sou` via ScummC `voice` decls, so
   the browser build TALKS. The dub pipeline's piper+FX chain becomes
   the in-game voice source; the NPC-DIALOG.md CAST table assigns
   voices per speaker.
2. **Narrative walkthrougher**: the films must exploit the story, not
   just prove the chain.
3. **Streamer mode**: the performer plays like a person, not a proof —
   no shortcuts; it explores rooms the way a curious player would,
   examines the funny things, tries the wrong-but-reasonable
   combination first (the fair mistakes the editorial desk catalogued:
   key-on-piano, nine-bolts-at-the-gate, give-bolt-to-Gusket), gets the
   gag, then finds the answer. Validate mode keeps the terse canonical
   chain as the deploy gate; perform mode gets a second, longer
   "streamer screenplay" that is the film.

## Remaining content (GDD Acts 2-3)

| # | Scene | Beat | Status |
|---|---|---|---|
| 06 | Backstage / Madame Voltina | Key #2's guardian; fortunes; says the Rustlers' motive out loud; plants "the key that winds itself" (Old Crank); forced knock-code echo | design |
| 07 | The Oil Bar, inside | voucher beats the rope; City Hall's aides drink and talk; the exposé thread (the poster) | design |
| 08 | City Hall / Mayor Piston | the cover-up confronted; steam-powered bluster | design |
| 09 | The Rustlers' hideout (Act 3 opens) | tavern back door + knock-code; recover Key #1; the ransom plot surfaces | design |
| 10 | Dynamo District / Old Crank | the fence opens; Old Crank IS Key #3 | design |
| 11 | The finale | rewind the Dynamo while the city powers down room by room (the detuning hum finally lands) | design |

## Cross-cutting work items

- **THE CONTESTS MUST BE PLAYABLE** (editorial B2+B8): dialog-tree
  riddle duel; wind-count as a player choice; walkthrougher learns to
  click dialog options. Blocks Scene 06 content per desk ruling.
- **NPC direct speech** (docs/research/NPC-DIALOG.md): costume-less
  actors, per-NPC talk colors, speaker-attributed dub. Voltina ships as
  the first costumed actor.
- **In-game voices** (pillar 1): spike `soun`/`sld` monster.sou support
  in ScummC, `voice` declarations next to each say-line, build-time TTS
  render into the .sou, ScummVM speech-mode flags. If ScummC's voice
  path is broken, fallback: text-only in game, voices remain film-only.
- **Streamer screenplays** (pillar 3): screenplay schema grows
  `detour:` shots (optional beats with no expectations beyond
  [talking]) and `mistake:` shots (wrong-combo attempts whose expected
  refusal line IS the assertion); a full-game streamer screenplay per
  act; render.py chapter cards per scene.
- **The detuning hum** (editorial N-A5): genmusic act-flag pitch drift.
- **Editorial cadence**: the five-chair desk runs per scene draft;
  embodiment sweep included. No scene ships with open BLOCKERs.

## Execution shape: parallel waves

- **Wave 1 (design, massively parallel, no build contention):** scene
  design docs 06-11 (one agent each: puzzle chain, objects+geometry,
  dialog draft in repo voice, music brief, screenplay beats) + the
  monster.sou voice spike + the streamer-screenplay schema design.
  Each lands as `docs/scenes/SCENE-XX.md` + research docs.
- **Wave 2 (build, parallelized where files don't collide):** B2+B8
  contests; then scenes 06-08 implemented one at a time behind the
  validate gate (rooms share headers/verbs — integration is serial by
  design), with art/music/screenplay generation parallel per scene.
- **Wave 3:** Act 3 (scenes 09-11), the finale's power-down sequence,
  the detuning hum.
- **Wave 4 (release):** full streamer playthrough film, in-game voices
  if the spike lands, README/site polish, the two-act demo becomes
  the whole game.

The validate gate stays the law: nothing merges red, and the desk
reviews every scene's text before it ships.


## Standing editorial debt (third desk pass, 2026-06-12)

Deferred WITH OWNERS -- the desk caught two "marked fixed, never landed"
items this pass; this table is the fix for that failure mode.

| Item | What | Lands with |
|------|------|-----------|
| N-A11 + N-TH7 | Contest variety: one contest charges for flops, one needs cross-room recall (plant the 8 in the dumpster's grease manual), vary winner slots | Before the next contest ships (Scene 08+) |
| N-A12/A13/A14 | Punch-noun ration ("Growth." etc.), town-aphorism ration, refusal-grammar variety (desk keeper lists in NOTES-2026-06-12-scene06.md) | Next punch-up sweep |
| N-TH9 | Win-cutscene pacing: flatten 3-4 beats, dead air after the hook | Film/streamer pass |
| N-A17 | Magnet/string split (DECIDED: ships, GDD updated) | Scene 09 prep |
| Player NIT | only:perform flop shots for the wind-count + "one act per night" line | Streamer screenplay |
| B12 rider | SCENE-07 brief: add backstage.scc to required reading; voucher gate is the rope (voltKey-keyed); fix stale "first Crank mention" claim | Scene 07 build pass, FIRST |


## Scene 07 desk debt (third-pass additions, 2026-06-12)

| Item | What | Lands with |
|------|------|-----------|
| N-11 | Every set-piece contest is the same 3-option/free-retry machine x4; give one stakes or non-menu input | Next contest pass (Scene 08+) |
| N-14 | Deadline (3 days) + detuning hum designed but unimplemented; genmusic act-flag pitch drift + one NPC names the clock | Cheap escalation pass |
| N-15 | Tavern piano three-missing-keys plant has no Act-3 payoff scheduled (now noted in GDD) | Act 3 |
| N-16 | Robot taste/mouth ledger inconsistent ("I don't have teeth" vs bots tasting constantly) | Next punch-up |
| N-17 | Catwalk heist escape (up, into the roof) points away from the bottom-tier hideout | One catwalk line |
| B-02 rider | City Hall / Mayor confrontation: DECIDE whether Act 3 adds it (loaded door + work order = the lock-and-key) or the work order stays Crank-only leverage | Act 3 planning |
| N-08/09/10 | Signposting polish: restate the goal post-heist; jar-before-toll redirect; sommelier idle-hint | Next polish |
