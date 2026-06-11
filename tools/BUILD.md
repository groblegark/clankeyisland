# Build pipeline notes

Target: an AGS game package that ScummVM (installed via `brew install scummvm`)
runs natively.

## The honest state of AGS authoring on macOS

- The **AGS Editor** (scene wiring, script compiling, packaging) is
  Windows-only (.NET/WinForms). Realistic options from a Mac:
  1. Run the editor under CrossOver/Wine or a Windows VM (UTM/Parallels).
  2. Use the editor's command-line compile (`AGSEditor.exe /compile`) in that
     same VM/Wine, driven from a script here, so the repo stays source-of-truth.
- The **AGS runtime** is cross-platform, but we don't need it — ScummVM *is*
  our runtime.

## Asset specs

| Asset | Spec |
|---|---|
| Backgrounds | 320x200 PNG (Midtown: 640x200 scrolling), indexed color OK |
| Sprites | PNG with magenta (#FF00FF) or alpha transparency |
| Walk cycles | 4 directions minimum, 6–8 frames each |
| Music | MIDI or OGG (OGG preferred for the jazz tracks) |
| SFX | OGG/WAV, mono, 22 kHz is plenty |

## Smoke test

```bash
scummvm --detect /path/to/compiled-game/   # should report engine: AGS
scummvm -p /path/to/compiled-game/ ags     # play
```
