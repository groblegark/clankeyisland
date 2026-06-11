# Build pipeline — ScummC (no editor, no GUI, text all the way down)

We build a **real SCUMM v6 game** (the Day of the Tentacle engine) from plain
text using [ScummC](https://github.com/AlbanBedel/scummc), and play it in
ScummVM's core SCUMM engine. Every part of the game is a diffable file:

| Game part | Source format | Tool |
|---|---|---|
| Rooms, objects, logic, dialog | `.scc` C-like scripts | `scc` (compiler) |
| Costumes (actor sprites/anims) | `.scost` text + BMP/GIF frames | `cost` |
| Fonts | BMP charset sheets | `char` |
| Sounds | VOC samples | `soun` |
| Music | MIDI | `midi` |
| Final game | `.roobj` objects → `<name>.000/.001` | `sld` (linker) |

## Setup (one-time)

```bash
tools/setup-scummc.sh
```

Clones ScummC into `vendor/scummc` (gitignored), applies our patches from
`tools/patches/` (arm64 endianness in `configure`; `man/` → `man/tools/`
path fix in `Makefile.target`), and builds with Homebrew bison 3.x
(system bison 2.3 is too old).

GTK+/SDL are optional — they only gate the GUI tools (`boxedit`, `costview`),
which we deliberately don't use. Walkboxes get declared in `.scc` text.

## Build & run

```bash
make            # in game/ — compiles .scc → .roobj, links → clankey.000/.001
scummvm --detect --path=game/build
scummvm -p game/build scumm:tentacle
```

ScummVM has no detection entry for homebrew SCUMM games, so the linked files
are named `tentacle.000/.001` and run under the Day of the Tentacle gameid —
the standard ScummC trick, verified working with ScummVM 2026.2.0.

## Reference

- `vendor/scummc/examples/openquest/` — complete worked example game
  (rooms, costumes, verbs, dialogs); our Makefile derives from it.
- `vendor/scummc/man/` — tool man pages; the ScummC wiki has the `.scc`
  language tour.

## Asset specs (SCUMM v6)

- Backgrounds: 320x200 BMP, 256-color indexed palette
- Costume frames: BMP/GIF, palette index 0 = transparent
- Sounds: 8-bit unsigned VOC (`raw2voc` converts raw PCM)
- Music: standard MIDI files
