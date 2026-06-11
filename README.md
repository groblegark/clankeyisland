# Clankey Island 🤖🏝️

A point-and-click adventure game set in **Clanker City**, the robot metropolis —
built to run in [ScummVM](https://www.scummvm.org/).

> *Deep in the Rust Belt Sea lies Clankey Island, home to Clanker City: a
> sprawling metropolis of robots, where steam hisses from manhole covers,
> neon gears spin above every storefront, and somewhere downtown the Great
> Dynamo is starting to wind down...*

## How this works

ScummVM doesn't author games — it *runs* them. The supported path for making a
**new** game that ScummVM plays natively is to build it as an
**AGS (Adventure Game Studio)** game; ScummVM ships a full AGS engine
(AGS 2.5+ games are supported since ScummVM 2.5).

So the pipeline is:

1. Author scenes, scripts, and assets here (this repo is the source of truth).
2. Compile to an AGS game file (`.ags` / `game28.dta`).
3. Drop the compiled game into ScummVM → play.

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
- [ ] Concept art for Docks of Clanker City
- [ ] AGS project + first playable room
- [ ] Compiled build running in ScummVM
