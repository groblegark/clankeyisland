# Narration Research: The Clanker City Chronicles Walkthrough Dub

Synthesis of three research tracks (June 2026): the KQ6-CD reference and deadpan craft, the voice-tech landscape, and the direction-encoding pipeline design. Companion to [WALKTHROUGHER.md](../WALKTHROUGHER.md) (performer/timeline architecture) and the Suno music/foley plan.

---

## 1. The Target Sound: A KQ6-Derived Deadpan Style Guide

### Why King's Quest VI is the reference

The "KQ6 narrator sound" is specifically the **CD-ROM version**: Sierra replaced the floppy version's narrator (Art Lewicki, in-house non-professional) with **Bill Ratner**, a working Hollywood promo/trailer/documentary announcer (later: *Inside Out* trailers, Flint in G.I. Joe, Ambassador Udina in Mass Effect). The CD cast was 30+ professional actors (Robby Benson, Tony Jay, Russi Taylor, Don Messick) under voice director Stuart M. Rosen, cast through Hollywood coordinator John Grayson, recorded in a SoCal studio with sync work back at Sierra's Oakhurst studios ([Wikipedia](https://en.wikipedia.org/wiki/King's_Quest_VI), [Bill Ratner](https://en.wikipedia.org/wiki/Bill_Ratner)).

The KQ5→KQ6 lesson: contemporary reviews ([Computer Gaming World via Wikipedia](https://en.wikipedia.org/wiki/King's_Quest_VI)) credited KQ6's leap over KQ5's infamous amateur voice track to **professional actors + a dedicated voice director, not technology**. For a TTS pipeline that translates to: voice selection + per-line curation, not engine choice alone.

Where the comedy sits: **in the script, not the read.** Jane Jensen's 6,000+ message lines put the wit in bespoke look/touch/fail/death responses ([The Digital Antiquarian](https://www.filfre.net/2019/07/the-mortgaging-of-sierra-online/)), delivered in the same warm, even, omniscient-storyteller register as everything else. Ratner never winks. That is exactly the register *"One bolt. Only eight thousand and ten more and I can afford a personality upgrade."* wants.

### Corroborating narrators and what each contributes

- **The Stanley Parable (Kevan Brighting)** — formal RP authority maintained without cracking while the content collapses; usually one take, never played the game; won NAVGTR awards for both comedy writing *and* performance ([GameSkinny interview](https://www.gameskinny.com/culture/interview-with-kevan-brighting-the-narrator-from-the-stanley-parable/)). Lesson: a perfect voice-fingerprint fit can substitute for heavy direction.
- **Bastion (Logan Cunningham, dir. Darren Korb)** — ~3,000 lines in a blanket-draped closet, ~15 takes in 2 minutes on a single line until emphasis and tone were exact ([GDC 2012 coverage](https://www.gamedeveloper.com/audio/gdc-2012-i-bastion-i-s-audio-success-came-from-a-closet)). Lesson: lo-fi capture is fine; **per-line iteration is the quality lever** — which maps directly onto TTS candidate-generation-and-selection.
- **Thomas Was Alone (Danny Wallace, dir. Mike Bithell)** — script written to a specific voice; Wallace recorded while listening to the soundtrack so the read sat against the music; BAFTA Performance win ([PCGamesN making-of](https://www.pcgamesn.com/thomas-was-alone/the-making-of-thomas-was-alone)). Lesson: perform against the footage and music bed, not in a vacuum.

### The 12 delivery rules

Actionable for a human director or a TTS prompt:

1. **The script is the comic; the voice is the straight man.** Never perform the funny. *"One bolt. Only eight thousand and ten more…"* reads exactly like *"You see a door."* Same sincerity, same poise.
2. **Baseline register = warm broadcast storybook.** Measured ~140–155 wpm, full unhurried sentences, slightly elevated diction, low-to-mid pitch, narrow dynamic range. KQ6 warmth, not Stanley Parable contempt — this narrator *likes* the player. For TTS prompts: explicitly forbid excitement.
3. **Comedy = register-content gap.** The intonation contour for an absurd line must be identical to a mundane one's. If the personality-upgrade line sounds any different from a doorway description, the joke is dead.
4. **Punchlines end on a falling terminal pitch.** Never an upswing, never an audible smile. Telegraphing is the #1 deadpan killer — and the #1 default failure mode of consumer TTS.
5. **Pause architecture:** a short beat (~300–500ms) *before* the punchline clause; dead air (~700–1200ms) *after* the line before the next cue. Comic timing is silence placement. The timeline should encode post-punchline holds explicitly.
6. **Throw away the punchline.** Stress the setup nouns; de-emphasize the joke itself — slightly faster, slightly quieter, almost muttered-but-articulate.
7. **Know when not to inflect:** lists, repeated failures, escalating absurdity — hold the pitch flat and let repetition escalate. Reserve genuine inflection for the few real narrative beats; deadpan only reads as a choice if warmth occasionally peeks through.
8. **Emotion leaks through tempo and consonants, not volume.** Irritation = clipped consonants + longer pauses; affection = slower + softer. The narrator never raises his voice. Ever.
9. **Observational stance.** Player actions reported as plain fact ("Clanky pockets the bolt."); futile actions get the same factual cadence ("The vending machine remains unmoved by your argument.").
10. **Iterate per line (Korb) AND cast/pick (Wreden) — for TTS, do both:** lock one voice fingerprint that's intuitively right, then generate 5–15 candidates per comedic line and select on emphasis/terminal-pitch/pause criteria. Budget the most candidates for punchlines.
11. **One voice fingerprint, batch-consistent.** Generate contiguous scene batches so tone and loudness don't drift; normalize loudness; fix the synthesis config per narrator.
12. **Perform against the footage and music** (Wallace's method): time each line to its gameplay window from the timestamped timeline, check the read against the Suno bed, and let pacing breathe with the scene.

### Style-guide risks

- **"Deadpan" is not one thing.** KQ6's warm storybook, Stanley's passive-aggressive RP, and Bastion's gravelly laconic western are not interchangeable. **Adopted blend: KQ6 warmth as base, Stanley restraint on punchlines.**
- **Golden-path comedy loss.** The humor density lives in bespoke look/touch/fail responses, not the critical path. The walkthrough route should deliberately trigger flavor responses, and the timeline must leave post-punchline air (Rule 5).
- **Don't clone the references.** Ratner and Brighting are living, working actors; emulate the craft, never name-prompt or clone their voices for published videos.
- Sierra production details derive from Sierra's own promo material relayed via fan wikis; treat fine-grained KQ6 claims as marketing-grade. Any reference listening must use the CD "talkie" version specifically.
- Brighting's one-take story is survivorship bias from perfect casting fit; budgeting zero iteration on that basis would be a mistake (Bastion needed ~15 takes/line *with a professional*).

---

## 2. Voice Technology Comparison (June 2026)

The decisive question: **who actually takes per-line acting direction?**

### Hosted services

| Service | Per-line direction | Mechanism | Cost (approx) | Commercial/YouTube | Verdict |
|---|---|---|---|---|---|
| **ElevenLabs Eleven v3** | **Yes — best in class** | Inline audio tags: `[deadpan]`, `[flatly]`, `[pause]`, `[sighs]`, `[sarcastic]` ([docs](https://elevenlabs.io/blog/v3-audiotags)) | 1 credit/char; Starter $5/mo (~30 min), Creator $22/mo (~100 min) ([pricing](https://elevenlabs.io/pricing)) | Free tier = **no** commercial use + attribution; any paid plan grants commercial license incl. monetized YouTube | The reference standard — `[deadpan]` is literally a documented tag. Non-deterministic: plan 2–4 takes/line; keep chunks <500 words |
| **Hume Octave / Octave 2** | **Yes — purpose-built** | `description` param = natural-language acting instructions per utterance ([docs](https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions)) | ~half ElevenLabs | Paid plans include commercial use | Strongest conceptual fit — it's an acting-direction API; LLM-based so it understands the joke. Smaller voice library; keep directions <100 chars |
| **OpenAI gpt-4o-mini-tts** | Yes | `instructions` param per request ([docs](https://developers.openai.com/api/docs/guides/text-to-speech)) | ~$0.015/min — cheapest credible | You own outputs; fine for monetized YouTube | Excellent iteration economics; comedic nuance a notch below the top two; 13 fixed voices, no cloning |
| **Google Gemini TTS (2.5/3.1 Flash)** | Yes | NL style prompts + inline tags ([docs](https://ai.google.dev/gemini-api/docs/speech-generation)) | ~$0.09–0.20 per 10-min narration | Paid-tier outputs usable commercially | Budget dark horse: 80–90% of the controllability at ~1/10 the cost |
| **Azure AI Speech (DragonHD)** | Partial | SSML `express-as` from fixed per-voice style lists ([docs](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice)) | ~$15–30/1M chars | Clean | No free-form deadpan direction; built for newscast/chat. **Pass** |
| **Cartesia Sonic-3** | Partial | Speed/volume/emotion params, real-time focus | Competitive | Paid plans | Great latency, weak "director" story. **Pass** |
| **PlayHT / PlayAI** | — | **Dead.** Meta acqui-hire July 2025; platform sunset Dec 31, 2025 | — | — | **Exclude entirely** |

### Local / open models (macOS arm64)

| Model | License | Direction ceiling | Notes |
|---|---|---|---|
| **Maya1 (3B)** | Apache 2.0 ✅ | Closest OSS analog to ElevenLabs: NL voice design + 20+ inline emotion tags ([maya1.org](https://maya1.org/)) | Best open candidate for *directable* acting; feasible on M-series ≥16GB, slow |
| **Qwen3-TTS (0.6B/1.7B)** | Apache 2.0 ✅ | Instruction-driven timbre/emotion/prosody + cloning ([GitHub](https://github.com/QwenLM/Qwen3-TTS)) | Strong new entrant; bake off vs Maya1 |
| **Chatterbox (Resemble)** | MIT ✅ | One `exaggeration` scalar + `cfg_weight`, not semantic direction ([GitHub](https://github.com/resemble-ai/chatterbox)) | Quality beats ElevenLabs in some blind tests; MPS support; outputs carry inaudible PerTh watermark |
| **Orpheus** | Apache 2.0 ✅ | Emotion tags, mid-tier acting | Via mlx-audio |
| **Kokoro-82M** | Apache 2.0 ✅ | Essentially zero direction; fixed pleasant delivery | Sub-200ms via [native MLX port](https://github.com/gabrimatic/kokoro-mlx) — ideal for **scratch tracks** |
| **F5-TTS** | Code MIT, popular checkpoint CC-BY-**NC** ⚠️ | Emotion only via reference clip | NC checkpoint is a landmine for monetized YouTube. Avoid |
| **XTTS-v2 (Coqui)** | CPML ⚠️, no commercial path (Coqui dead Jan 2024) | Aging | Licensing dead end. **Skip** |
| **Piper** | MIT ✅ | None | Only as a gag: background robots that *sound* like cheap TTS |

Local bottom line: the Apache-licensed 2025–26 generation is genuinely good and legally clean, but per-line direction granularity and take-to-take reliability still trail ElevenLabs v3/Hume, and M-series iteration is seconds-to-minutes per line vs ~1s hosted.

### Ranked top-3 recommendation

1. **ElevenLabs Eleven v3, Creator plan ($22/mo; drop to $5 Starter after the bulk render).** Best deadpan controllability (documented `[deadpan]`/`[flatly]`/`[pause]` tags), best hosted quality ceiling, seconds-fast per-line re-rolls. Mitigate v3 nondeterminism by generating 2–4 candidates per line and letting the pipeline pick — the timeline architecture makes per-line caching/re-rolls natural. Never ship free-tier audio (no commercial rights + attribution requirement).
2. **Hume Octave** — the acting-instructions native ("bored municipal robot, dry, beat before the punchline"), ~half the price, sometimes lands the joke unprompted. Run a 20-line bake-off against v3 before committing. Budget alternative in this slot: **Gemini 3.1 Flash TTS** at ~$0.10–0.20 per 10 minutes.
3. **Human + $100–250 USB mic, optionally + speech-to-speech conversion.** Highest comedy ceiling, period — deadpan is 90% timing, and timing is what TTS is worst at. A full SCUMM game is realistically 500–2,000 lines ≈ 1–4 weekends at 25–60 lines/hour. **Killer hybrid:** record the human for timing and emphasis, then run through voice conversion (ElevenLabs Voice Changer, or Chatterbox VC locally) for per-character robot timbres — sidesteps the entire "how do I direct a TTS to be funny" problem. Worst "re-render one line in CI" story, though.

**Fully-local honorable mention:** Maya1 if the project later wants a no-cloud pipeline (accept a quality step down). Use **Kokoro-MLX for instant scratch audio** while iterating on timeline/sync tooling, then swap in real voices.

**Suno:** music-first; v5.5 "Voices" is a *singing*-persona feature and spoken-word prompting is unreliable ([Suno v5.5](https://suno.com/blog/v5-5)). Keep it confined to the sibling music/foley plan — with one carve-out: a sung intro/outro theme that name-drops the game, which Suno excels at.

---

## 3. The Direction Track: Sidecar Format Proposal

Grounding: dialog source of truth is the `egoSay(...)` strings in `game/*.scc` (worked examples below are `game/docks.scc:64,66,135` and `game/inventoryitems.scc:46`). The performer already emits `timeline.json` with per-line timestamps but punts on line *identity* — now a hard prerequisite (§6).

### Design principles

- **The .scc stays the single source of truth for *what* is said; the sidecar carries only *how*.** A linter asserts every sidecar `text` byte-matches a string in the .scc; mismatch fails loudly (same philosophy as the stage map).
- **Stable line IDs by content hash, readable slug for humans:** `id: docks/arrival-2` + `sha: first 10 hex of sha1(speaker + "|" + text)`. Editing a line's text changes the hash, which *correctly* invalidates its approved take; reordering/moving lines does not.
- **Canonical direction is structured and engine-neutral; engine syntax is generated** by a small compiler (`tools/voicedirect.py`). Anything load-bearing for timing (beats, pauses) is structured so it survives an engine swap; `prompt` is the freeform escape hatch.
- **Direction ≠ approval state.** Direction is committed and hand-edited (`voice/direction/*.yaml`); take/approval state is machine-written (`voice/takes/<scene>/status.yaml`).

### Worked example: `voice/direction/docks.direction.yaml`

```yaml
version: 1

personas:
  sprocket:
    voice: { elevenlabs: "<voice-id>", openai: "ash", chatterbox: "ref/sprocket.wav" }
    base_prompt: >
      A small, earnest maintenance robot narrating his own life like it's a
      hard-boiled noir he can't quite afford. Deadpan, dry, mid-register,
      lightly metallic warmth. Early-90s CD-ROM adventure-game voice acting
      (King's Quest VI energy): committed, theatrical diction, but never
      winking at the joke. Jokes are delivered as plain facts.
    pacing: { wpm: 150 }          # persona default; lines may override
    defaults: { pre_pause_ms: 150, post_pause_ms: 250 }

lines:
  - id: docks/arrival-1
    sha: 3f2a9c01d4
    speaker: sprocket
    text: "Clanker City! The big smoke! The city of ten thousand gears!"
    direction:
      inflection: [mock-grandeur, rising-sequence]   # three escalating exclamations
      pacing: { wpm: 165 }                           # slight accelerando, big-arrival energy
      beats:
        - { after: "Clanker City!", pause_ms: 250 }
        - { after: "The big smoke!", pause_ms: 250 }
      prompt: >
        Triumphant arrival monologue, each exclamation slightly bigger than
        the last — a hick robot announcing the metropolis to nobody.
        Genuinely thrilled, zero irony yet.

  - id: docks/arrival-2
    sha: 81be07aa52
    speaker: sprocket
    text: "One small maintenance-bot, one dream, and not so much as an oil can to my name."
    direction:
      inflection: [wistful, trailing-off]
      pacing: { wpm: 135 }                           # the comedown after the fanfare
      pre_pause_ms: 400                              # beat of silence after the previous high
      beats:
        - { after: "one dream,", pause_ms: 350 }     # the list lands on its broke punchline
      emphasis: ["oil can"]
      prompt: >
        Deflating from the previous line's grandeur. A noir hero's
        self-introduction, except the tragic detail is an oil can.
        Trail off slightly on "to my name."

  - id: docks/bolt-rain
    sha: c6d0e8b913
    speaker: sprocket
    text: "It rained a bolt. In this town that's basically a tip."
    direction:
      inflection: [deadpan, flat]
      split:                                          # hard beat: render as two segments
        - { text: "It rained a bolt.", prompt: "Plain observation. Almost bored." }
        - gap_ms: 450                                 # the comedic beat, owned by us not the model
        - { text: "In this town that's basically a tip.",
            prompt: "Flatter and a shade slower than the setup; a man counting his blessings and reaching one.",
            pacing: { wpm: 125 } }
      emphasis: ["basically"]                         # the 'italics on basically' note
      post_pause_ms: 600                              # let it sit (perform mode already holds 2s on jokes)

  - id: inventory/notice-examine
    sha: 0a77f1d2c8
    speaker: sprocket
    text: "Nothing says 'something is wrong' like an official notice that nothing is wrong."
    direction:
      inflection: [deadpan]
      pacing: { wpm: 140 }
      quote_voice:                                    # the quoted fragment gets its own micro-direction
        - { span: "something is wrong", style: "slightly announcer-ish, as if reading the notice aloud" }
      emphasis: ["nothing is wrong"]                  # the SECOND occurrence — totally flat; the joke is the echo
      beats:
        - { after: "like an official notice", pause_ms: 200 }
      prompt: >
        The joke is the repetition: first "something is wrong" is quoted,
        a little performed; the closing "nothing is wrong" is dead flat,
        like reading small print. Do not smile.
```

**Field vocabulary** (kept small, like the screenplay primitives): `inflection` from a fixed enum (`flat, deadpan, wistful, trailing-off, mock-grandeur, rising-sequence, urgent, sotto`); `pacing` is `wpm` (lowered to engine rate params or prompt words) or per-beat marks; `pre/post_pause_ms` are **mixer offsets, not baked into audio**; `split` is the only structure that changes render units; `emphasis`/`quote_voice` lower to tags or prompt sentences.

---

## 4. Comedic-Beat Engineering: What Survives Each Engine Class

Engine classes (verified against current docs):

- **Tag-based** — ElevenLabs v3 (inline `[flatly]` tags; `<break time="x.xs"/>` up to ~3s, but [ElevenLabs' own docs](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) warn stacked break tags cause instability/artifacts); Hume Octave (`description` + inline `[pause]`/`[long pause]`).
- **Prompt-based** — OpenAI `gpt-4o-mini-tts` `instructions`; Hume's description doubles here. Pause *placement* via prompt is approximate and unreliable.
- **Parameter-based** — Chatterbox: `exaggeration` (~0.3 = subdued/deadpan) and `cfg_weight` (lower = slower, more deliberate). No per-word control.
- **None** — Kokoro/Piper-class: text in, audio out; punctuation and speed only.

| Technique | Tag (11L v3 / Hume) | Prompt (4o-mini) | Param (Chatterbox) | None (Kokoro) |
|---|---|---|---|---|
| **Split at the beat, concat with exact silence** | ✅ | ✅ | ✅ | ✅ — the only universal technique |
| Engine-inserted measured silence | ⚠️ works but unstable/quantized | ❌ unreliable | ❌ | ❌ (ellipsis nudge only) |
| Different style per setup vs punchline | ✅ tags mid-text or per-segment | ✅ natively (separate requests) | ⚠️ per-segment param changes | ❌ |
| Post-trim breaths/leading silence (DSP) | ✅ | ✅ | ✅ | ✅ |
| Slow the punchline | ✅ tag/prompt or ffmpeg `atempo` | ⚠️ prompt or `atempo` | ✅ cfg_weight or `atempo` | `atempo` only |
| Multi-take render + human pick | ✅ | ✅ | ✅ | ⚠️ low variance |

**The doctrine: own the timing in the editor, not the model.** The beat in *"It rained a bolt. ⟨450ms⟩ In this town that's basically a tip."* should be real digital silence between two trimmed renders — deterministic, engine-portable, adjustable in review without re-rendering. Engine-side pause syntax is a nice-to-have lowering target, not the mechanism.

Post pipeline per take: trim leading/trailing silence and breaths (`ffmpeg silenceremove` / pydub), loudness-normalize each clip (mono dialog, ~-16 LUFS) so concatenated segments are seamless, then assemble splits with their `gap_ms`. Render 2–3 takes by default for any `split`/`emphasis`-bearing line; flat connective lines get 1.

---

## 5. The Review Loop

Cheap, text/file-first, same shape as the screenplay/stage-map split (artistic intent in committed text, generated state in machine files, human touchpoint = one HTML page per scene):

```
voice/
  direction/docks.direction.yaml        committed, hand-edited
  takes/docks/<line_id>/take-01.wav     rendered audio (git-LFS or release artifact)
  takes/docks/<line_id>/take-01.json    {engine, params, direction_sha, duration_ms}
  takes/docks/status.yaml               machine-written approval state
```

1. **`voicedirect.py render docks`** — renders only lines whose `direction_sha` changed, are missing takes, or are marked `redo`. Idempotent; **approved lines are never re-rendered** (engines are nondeterministic — a re-render is a different performance).
2. **`voicedirect.py review docks`** — emits one static `out/review/docks.html`: a row per line with text, direction summary, an `<audio>` player per take, radio buttons (approve take N / redo), and a free-text redo note. No server: "Export decisions" serializes the form to `decisions.yaml` (localStorage backup against tab loss).
3. **`voicedirect.py apply decisions.yaml`** — writes `status.yaml` (`approved: take-02` with duration, or `status: redo`) and appends each redo note verbatim to that line's working `prompt` ("punchline came too fast — more dead air before 'basically'"), so **the note *is* the next round's direction**. Loop; only rejected lines re-render.

---

## 6. Integration with the Walkthrough-er Timeline and the Suno Plan

### Two pacing regimes

- **Game-paced (mix in post, no driver change):** `render.sh` lays each approved take at `t_start(line) + pre_pause_ms` via ffmpeg `adelay`, ducking the Suno music bed under dialog. Requirement: `duration_ms + post_pause_ms ≤ t_end − t_start` for every line, where the window comes from SCUMM's length-based text timing. The compiler imports per-line `max_duration_ms` from a validate-mode timeline; the renderer flags window-busting takes at *render* time, not mix time. **This regime is hostile to deadpan** — the pause that makes a joke work eats window you may not have.
- **Audio-paced (recommended for perform mode):** the performer holds the text until the audio would end — approved durations are known *before* the run (in `status.yaml`), so the driver waits `max(scumm_text_time, pre_pause + duration + post_pause)` after each line. A small extension of the existing `hold: 2s` joke-beat mechanic. Requirements: (a) takes frozen/approved before a perform run — the film's pacing is a function of the dub; (b) pre/post pauses live as *mix offsets* in the sidecar, not baked into WAVs; (c) the mixer asserts no two takes overlap given their offsets (`waitForMessage()` serializes same-actor lines today, but future two-actor exchanges won't be).

### The line-identity prerequisite

Matching takes to timestamps needs line *identity*, not just "talking happened" — exactly the debug channel WALKTHROUGHER.md punts on. A ~3-line `prints`-each-egoSay shim in `common.scc` carrying the same `sha` the sidecar uses closes the loop: **.scc text → sha → direction → take → timeline event → mix offset.** Without it, the dub mix has nothing to anchor to.

### Subtitles and music

- The **dub timings** (not the SCUMM text band) should drive `walkthrough.srt`, so subtitles match what's heard.
- Suno stays on the music/foley side: bed ducked under dialog at mix, plus the optional sung intro/outro theme. Per Rule 12, hero-line reads get checked against the music bed before approval.

---

## 7. Decision Summary

### Default stack to adopt when we leave the planning stage

| Layer | Choice |
|---|---|
| Style target | KQ6-CD warmth as base register, Stanley Parable restraint on punchlines (Rules 1–12, §1) |
| Hero engine | **ElevenLabs Eleven v3, Creator plan**; 2–4 candidates per comedic line, human pick |
| Challenger | **Hume Octave** — 20-line bake-off vs v3 before committing volume |
| Scratch tracks | **Kokoro-MLX** locally, instant, swapped out before any publish |
| Timing | **Owned in the editor**: split renders + exact digital silence + trim + -16 LUFS normalize; engine pause syntax is a lowering target only |
| Direction format | Engine-neutral YAML sidecar (§3), content-sha line IDs, `voicedirect.py` compiler + linter |
| Review | Render → static-HTML review page → decisions.yaml → redo notes become direction |
| Sync | Audio-paced perform mode; egoSay→console sha channel; dub-driven SRT |
| Music/foley | Suno (separate plan); no spoken narration via Suno |
| Storage | git-LFS or release artifacts for WAVs from day one |

**Build order:** (1) egoSay→console debug channel + sha-based line extractor; (2) `voicedirect.py` schema + linter + compiler with one backend (prompt-based is cheapest to start; structured fields keep the door open to v3 for hero lines); (3) split/trim/normalize post pipeline + multi-take render; (4) review HTML + decisions loop; (5) audio-paced perform mode + mix step in `render.sh`.

### Standing risks

- **Re-rendering drift:** approved lines are frozen artifacts keyed by (text, direction) hash; casual re-renders re-perform the cut.
- **Engine lock-in:** never commit ElevenLabs tags/`<break>` markup as canonical direction — generate it.
- **Text edits orphan takes:** the sidecar linter must run in the same gate as the walkthrough validator, or the film ships a dub of a line the game no longer says.
- **Cost drift:** per-line re-rolls multiply character counts; meter usage in the pipeline (a heavily-iterated 2,000-line script can blow past Creator credits).
- **Licensing:** no free-tier ElevenLabs audio; no XTTS-v2 or the NC F5-TTS checkpoint; Chatterbox outputs carry an inaudible watermark (acceptable, but a conscious choice); YouTube may require synthetic-voice disclosure.
- **Vendor death:** PlayHT's deletion is the cautionary tale — the sidecar→audio interface stays vendor-agnostic.

### Open questions

1. **v3 vs Hume bake-off result** — which engine actually lands the four worked-example lines best (20-line test, blind pick)?
2. **Human-hybrid trigger** — at what line count / quality gap do we switch hero lines to recorded-human + voice conversion?
3. **Persona spread** — one narrator voice vs distinct timbres for incidental robots (and whether Piper-as-a-gag is funny or just cheap).
4. **Take storage** — git-LFS vs release artifacts (decide before the first real render batch).
5. **Window pressure** — how often game-paced windows actually bust under deadpan reads; data from the first validate-mode timeline decides how aggressively to lean on audio-paced mode.
6. **YouTube AI-disclosure posture** for the published videos.