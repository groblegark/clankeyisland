# actorSay-then-dialog corruption (NPC direct speech, blocked 2026-06-12)

## Status: NPC-speech PIPELINE shipped; actorSay ACTIVATION deferred

The full pipeline landed and is live: per-NPC talk colors (PAL 108-112),
five costume-less NPC actors initialized in `actors.scc`, speaker-tagged
transcript extraction, driver nearest-color speaker attribution +
`speaker_mismatch` oracle, and a `genvoice.py` CAST table giving each NPC
its own piper voice in `monster.sou`. The art-doctor SYS-1/2/3 fixes (talk
collision assert, EXTRA recolor, nearest-color classification) shipped with
it. **What is NOT active: any shipped scene actually calling `actorSay`.**
The emcee pilot was reverted to reported speech (`egoSay`) like Voltina.

## The bug

A single `actorSay(emcee_a, ...)` in the theater's emcee-greeting cutscene
**corrupts the openquest dialog UI for the rest of the session.** Evidence
from validate take `20260612-175920`:

- `the-riddle-duel` (alley, `choose:2`, BEFORE the theater): **PASS** — the
  dialog UI works with all five NPC actors already declared/initialized.
- `the-emcee` (theater, runs `actorSay(emcee_a)`): **PASS** (the actorSay
  line itself renders).
- Every dialog AFTER it fails "dialog list never appeared":
  `the-amazing-sprocket` (theater wind-count), `the-truth`, and
  `the-key-that-winds-itself` (backstage Card III + hub) — and the
  dialog-driven backstage progression (`the-price`, `card-one`,
  `mind-the-cables`) fails its pixel probes downstream.
- Backstage contains **no** actorSay, so the corruption is GLOBAL and
  PERSISTENT once any actorSay has run.

The dialog code (`dialog.scc`), `common.scc`, and `backstage.scc` are
byte-identical to the last all-green build, so the engine-state corruption
comes from the `actorSay` call path, not the dialog code.

## Leading hypothesis (untested)

openquest mixes `actorSay` and `Dialog::dialogStart` successfully, but
always **within one handler** and always closes talk sequences with
`stopTalking()` / `actorSay(0xFF, "")` (e.g. `actors.scc:288,348`). Our
emcee cutscene ends each `actorSay` with only `waitForMessage()` and never
`stopTalking()`, leaving `VAR_TALK_ACTOR = emcee_a` (or a charset/print-slot
state) set across the shot boundary. `showDialog()` switches charsets
(`initCharset(dialogCharset)` → draw → `initCharset(chtest)`); a leftover
talk/charset state may be what stops the option verbs from rendering where
the driver's `dialog_open` looks.

## Next debug steps (with instrumentation, not blind 20-min validates)

1. Reproduce in a minimal native build (`make run`): one room, one
   `actorSay`, then a `dialogStart`, and watch whether the options draw.
2. Add `dbgPrint` of `VAR_TALK_ACTOR`, the current charset, and the verb
   draw state inside `showDialog()` right before/after the option loop.
3. Try `actorSay(0xFF, "")` (stopTalking) after the emcee's last line and
   re-test — the openquest-proven reset. If that fixes it, restore the
   emcee's direct lines (the wording is preserved in the `TODO(actorSay)`
   comment in `theater.scc`) and re-validate.
4. If charset is the culprit, have `showDialog` force the dialog charset
   defensively and restore `chtest` in a `try/override`.

## Restore path

The emcee's direct-speech wording is parked in the `TODO(actorSay)` comment
in `theater.scc`. Voltina (backstage) and the rest of the cast were never
converted, so only the emcee line needs restoring once the reset is proven.
