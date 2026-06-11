# Clankey Island 🤖🏝️

A point-and-click adventure game set in **Clanker City**, the robot metropolis —
built to run in [ScummVM](https://www.scummvm.org/).

> *Deep in the Rust Belt Sea lies Clankey Island, home to Clanker City: a
> sprawling metropolis of robots, where steam hisses from manhole covers,
> neon gears spin above every storefront, and somewhere downtown the Great
> Dynamo is starting to wind down...*

## How this works

ScummVM doesn't author games — it *runs* them. We author everything as plain
text and compile to a **real SCUMM v6 game** (the Day of the Tentacle engine)
using [ScummC](https://github.com/AlbanBedel/scummc). No editor, no GUI:
rooms, dialog, and logic are C-like `.scc` scripts; costumes are `.scost`
text files pointing at image frames. See `tools/BUILD.md` for the pipeline,
and `tools/setup-scummc.sh` to bootstrap the toolchain.

1. Author scenes, scripts, and assets here (this repo is the source of truth).
2. `make` → `scc` compiles, `sld` links → `tentacle.000/.001`.
3. `scummvm -p game/build scumm:tentacle` → play.

```
assets/      Art, music, sound — source files (PNG, etc.)
  backgrounds/   Room background paintings (320x200 or 640x400)
  sprites/       Characters, objects, cursors
  portraits/     Dialog portraits
  music/         Tunes (the Clanker City Shuffle goes here)
  sfx/           Clanks, hisses, servo whirs
  fonts/
game/
  scenes/        One design doc per room/scene
  scripts/       Game logic / dialog scripts
docs/
  GDD.md         Game design document — story, characters, puzzles
tools/           Build & conversion helpers
```

## Running ScummVM

```bash
brew install scummvm   # already handled
scummvm                # launcher; add the compiled game directory
```

## Status

- [x] Repo + project skeleton
- [x] Game design doc (docs/GDD.md)
- [x] First scene designs (game/scenes/)
- [x] ScummC toolchain building on macOS/arm64 (tools/setup-scummc.sh)
- [x] Demo game (openquest) compiled + detected by ScummVM 2026.2.0
- [ ] First playable Clankey Island room (.scc) — derive from openquest
- [ ] Concept art for Docks of Clanker City
