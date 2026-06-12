#!/usr/bin/env python3
"""The songbook of Clanker City Chronicles.

The score is this file: notes as data, rendered deterministically by
mido into a single-track type-0 General MIDI file, which `soun -midi`
packs into a SOUN/MIDI resource. ScummVM plays it through CoreAudio's
GM synth natively and the AdLib OPL emulator in the wasm build (see
docs/research/AUDIO.md — programs below are chosen from the ones with
decent GM->FM fallback: simple leads, synth bass, basic percussion).

Two songs:
- 'Dockside' (Scene 01): chiptune noir, a harbor at night, slightly out
  of warranty. 16 bars swung 4/4, D minor, 88 BPM, loop at beat 65.
- 'The Scrap & Barrel Rag' (Scene 02): the tavern's player piano. It is
  missing three keys, so every note that needs E5, A4 or D5 simply does
  not happen — the holes ARE the joke. 12 bars, C major, 104 BPM,
  loop at beat 49 (RAG_LOOP_BEATS).

Output: assets/generated/audio/{dockside,scrapnbarrel}.mid
"""

import os

import mido

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "assets", "generated", "audio")

PPQ = 480
BPM = 88
BARS = 16
LOOP_BEATS = BARS * 4 + 1   # game code jumps back to beat 1 from here

# swung eighths: long-short
E_LONG, E_SHORT = PPQ * 2 // 3, PPQ // 3

NOTE = {n: i for i, n in enumerate(
    ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"])}


def n(name, octave):
    return 12 * (octave + 1) + NOTE[name]


# ------------------------------------------------------------ the score

# chord roots per bar (D minor harbor changes, two 8-bar passes)
PROG = ["Dm", "Dm", "Gm", "Gm", "Bb", "F", "Gm", "A7",
        "Dm", "Dm", "Gm", "Gm", "Bb", "F", "A7", "Dm"]

CHORDS = {
    "Dm": [n("D", 3), n("F", 3), n("A", 3)],
    "Gm": [n("G", 3), n("Bb", 3), n("D", 4)],
    "Bb": [n("Bb", 2), n("D", 3), n("F", 3)],
    "F":  [n("F", 3), n("A", 3), n("C", 4)],
    "A7": [n("A", 2), n("Db", 3), n("G", 3)],
}
ROOTS = {"Dm": n("D", 2), "Gm": n("G", 2), "Bb": n("Bb", 1),
         "F": n("F", 2), "A7": n("A", 1)}
FIFTH = {"Dm": n("A", 2), "Gm": n("D", 3), "Bb": n("F", 2),
         "F": n("C", 3), "A7": n("E", 2)}

# melody: (bar, beat-within-bar in swung-eighth slots, pitch, len-slots)
# slots: 0,1 = beat 1 long/short ... 8 slots per bar; None = rest
# A wistful little tune that ends each phrase looking at its feet.
M = []
def phrase(bar, notes):
    for slot, pitch, ln in notes:
        M.append((bar, slot, pitch, ln))

phrase(5,  [(0, n("D", 5), 2), (2, n("F", 5), 1), (3, n("E", 5), 1),
            (4, n("D", 5), 3)])
phrase(6,  [(0, n("C", 5), 1), (2, n("A", 4), 1), (4, n("D", 5), 4)])
phrase(7,  [(0, n("Bb", 4), 2), (2, n("D", 5), 1), (3, n("C", 5), 1),
            (4, n("Bb", 4), 2), (6, n("G", 4), 2)])
phrase(8,  [(0, n("A", 4), 6)])
phrase(9,  [(0, n("D", 5), 2), (2, n("F", 5), 1), (3, n("E", 5), 1),
            (4, n("F", 5), 3)])
phrase(10, [(0, n("G", 5), 1), (2, n("F", 5), 1), (4, n("E", 5), 4)])
phrase(11, [(0, n("D", 5), 2), (2, n("Bb", 4), 1), (3, n("C", 5), 1),
            (4, n("D", 5), 2), (6, n("F", 5), 2)])
phrase(12, [(0, n("E", 5), 4), (4, n("Db", 5), 3)])
phrase(13, [(0, n("D", 5), 2), (2, n("F", 5), 2), (4, n("Bb", 5), 3)])
phrase(14, [(0, n("A", 5), 4), (4, n("F", 5), 2), (6, n("E", 5), 2)])
phrase(15, [(0, n("E", 5), 2), (2, n("Db", 5), 2), (4, n("E", 5), 2),
            (6, n("G", 5), 2)])
phrase(16, [(0, n("D", 5), 6)])

CH_LEAD, CH_BASS, CH_EP, CH_DRUM = 0, 1, 2, 9
PRG_LEAD, PRG_BASS, PRG_EP = 80, 38, 4       # square lead, synth bass, e-piano
KICK, SNARE, HAT = 36, 38, 42


def slot_time(bar, slot):
    """Absolute ticks of a swung-eighth slot (8 per bar)."""
    beat, half = divmod(slot, 2)
    return (bar - 1) * 4 * PPQ + beat * PPQ + (E_LONG if half else 0)


def slot_len(slot, ln):
    return slot_time(1, slot + ln) - slot_time(1, slot)


def build_dockside():
    ev = []  # (tick, order, mido.Message)

    def add(tick, msg, order=1):
        ev.append((tick, order, msg))

    for ch, prg, vol in [(CH_LEAD, PRG_LEAD, 84), (CH_BASS, PRG_BASS, 100),
                         (CH_EP, PRG_EP, 66), (CH_DRUM, 0, 90)]:
        add(0, mido.Message("program_change", channel=ch, program=prg), 0)
        add(0, mido.Message("control_change", channel=ch, control=7,
                            value=vol), 0)

    for bar in range(1, BARS + 1):
        chord = PROG[bar - 1]
        t0 = (bar - 1) * 4 * PPQ

        # bass: root on 1 and 3, fifth on 2 and 4, staccato shuffle
        for beat, pitch in [(0, ROOTS[chord]), (1, FIFTH[chord]),
                            (2, ROOTS[chord]), (3, FIFTH[chord])]:
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_BASS,
                                note=pitch, velocity=78))
            add(t + PPQ * 3 // 5, mido.Message(
                "note_off", channel=CH_BASS, note=pitch, velocity=0))

        # e-piano: offbeat chord stabs (the shuffle's shoulders)
        for beat in (1, 3):
            t = t0 + beat * PPQ + E_LONG
            for pitch in CHORDS[chord]:
                add(t, mido.Message("note_on", channel=CH_EP,
                                    note=pitch, velocity=52))
                add(t + E_SHORT, mido.Message(
                    "note_off", channel=CH_EP, note=pitch, velocity=0))

        # drums: brushy hats every swung eighth, kick 1/3, snare 2/4
        for slot in range(8):
            t = t0 + slot_time(1, slot)
            add(t, mido.Message("note_on", channel=CH_DRUM, note=HAT,
                                velocity=46 if slot % 2 else 60))
            add(t + 40, mido.Message("note_off", channel=CH_DRUM,
                                     note=HAT, velocity=0))
        for beat, drum, vel in [(0, KICK, 88), (2, KICK, 70),
                                (1, SNARE, 64), (3, SNARE, 68)]:
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_DRUM, note=drum,
                                velocity=vel))
            add(t + 60, mido.Message("note_off", channel=CH_DRUM,
                                     note=drum, velocity=0))

    # melody
    for bar, slot, pitch, ln in M:
        t = slot_time(bar, slot)
        add(t, mido.Message("note_on", channel=CH_LEAD, note=pitch,
                            velocity=72))
        add(t + slot_len(slot, ln) - 30, mido.Message(
            "note_off", channel=CH_LEAD, note=pitch, velocity=0))

    mid = mido.MidiFile(type=0, ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo",
                                  tempo=mido.bpm2tempo(BPM), time=0))
    last = 0
    for tick, _, msg in sorted(ev, key=lambda e: (e[0], e[1])):
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track",
                                  time=BARS * 4 * PPQ - last))
    mid.tracks.append(track)
    return mid


# ------------------------------------------- The Scrap & Barrel Rag

RAG_BPM = 104
RAG_BARS = 12
RAG_LOOP_BEATS = RAG_BARS * 4 + 1
PRG_HONKY = 3          # honky-tonk piano: it IS a player piano

# the three keys that fell out of the piano (see draw_tavern's gap gag)
MISSING_KEYS = {n("E", 5), n("A", 4), n("D", 5)}

RAG_PROG = ["C", "C", "F", "C", "G", "F", "C", "G",
            "C", "F", "C", "G"]
RAG_CHORDS = {
    "C": [n("C", 4), n("E", 4), n("G", 4)],
    "F": [n("C", 4), n("F", 4), n("A", 4)],
    "G": [n("B", 3), n("D", 4), n("G", 4)],
}
RAG_ROOTS = {"C": n("C", 2), "F": n("F", 2), "G": n("G", 2)}
RAG_FIFTH = {"C": n("G", 2), "F": n("C", 3), "G": n("D", 3)}

# melody slots (8 swung-eighths per bar) — written to hit the missing
# keys often, because a rag with holes in it is funnier than a rag
RM = []
def rag_phrase(bar, notes):
    for slot, pitch, ln in notes:
        RM.append((bar, slot, pitch, ln))

rag_phrase(1,  [(0, n("E", 5), 1), (1, n("G", 5), 1), (2, n("C", 5), 1),
                (3, n("E", 5), 1), (4, n("G", 5), 2), (6, n("A", 4), 2)])
rag_phrase(2,  [(0, n("D", 5), 1), (1, n("E", 5), 1), (2, n("C", 5), 2),
                (4, n("G", 4), 1), (5, n("A", 4), 1), (6, n("C", 5), 2)])
rag_phrase(3,  [(0, n("F", 5), 1), (1, n("A", 4), 1), (2, n("C", 5), 1),
                (3, n("D", 5), 1), (4, n("F", 5), 2), (6, n("A", 5), 2)])
rag_phrase(4,  [(0, n("E", 5), 2), (2, n("D", 5), 1), (3, n("C", 5), 1),
                (4, n("E", 4), 4)])
rag_phrase(5,  [(0, n("D", 5), 1), (1, n("B", 4), 1), (2, n("G", 4), 1),
                (3, n("D", 5), 1), (4, n("B", 4), 2), (6, n("G", 5), 2)])
rag_phrase(6,  [(0, n("A", 4), 1), (1, n("C", 5), 1), (2, n("F", 5), 1),
                (3, n("A", 4), 1), (4, n("C", 5), 4)])
rag_phrase(7,  [(0, n("C", 5), 1), (1, n("E", 5), 1), (2, n("G", 5), 1),
                (3, n("E", 5), 1), (4, n("C", 5), 2), (6, n("E", 5), 2)])
rag_phrase(8,  [(0, n("D", 5), 2), (2, n("B", 4), 1), (3, n("A", 4), 1),
                (4, n("G", 4), 4)])
rag_phrase(9,  [(0, n("C", 5), 1), (1, n("E", 5), 1), (2, n("G", 5), 2),
                (4, n("E", 5), 1), (5, n("C", 5), 1), (6, n("G", 4), 2)])
rag_phrase(10, [(0, n("A", 4), 1), (1, n("F", 5), 1), (2, n("A", 4), 1),
                (3, n("F", 5), 1), (4, n("D", 5), 4)])
rag_phrase(11, [(0, n("E", 5), 1), (1, n("C", 5), 1), (2, n("E", 5), 1),
                (3, n("C", 5), 1), (4, n("G", 4), 2), (6, n("E", 5), 2)])
rag_phrase(12, [(0, n("D", 5), 2), (2, n("B", 4), 2), (4, n("C", 5), 4)])


def build_rag():
    ev = []

    def add(tick, msg, order=1):
        ev.append((tick, order, msg))

    def note(ch, tick, pitch, dur, vel):
        if pitch in MISSING_KEYS:
            return            # that key is literally not there
        add(tick, mido.Message("note_on", channel=ch, note=pitch,
                               velocity=vel))
        add(tick + dur, mido.Message("note_off", channel=ch, note=pitch,
                                     velocity=0))

    add(0, mido.Message("program_change", channel=0, program=PRG_HONKY), 0)
    add(0, mido.Message("control_change", channel=0, control=7, value=98), 0)

    for bar in range(1, RAG_BARS + 1):
        chord = RAG_PROG[bar - 1]
        t0 = (bar - 1) * 4 * PPQ
        # stride left hand: oom (root/fifth) pah (chord)
        for beat in range(4):
            t = t0 + beat * PPQ
            if beat % 2 == 0:
                low = RAG_ROOTS[chord] if beat == 0 else RAG_FIFTH[chord]
                note(0, t, low, PPQ // 2, 74)
            else:
                for p in RAG_CHORDS[chord]:
                    note(0, t, p, PPQ // 3, 58)

    for bar, slot, pitch, ln in RM:
        t = slot_time(bar, slot)
        note(0, t, pitch, slot_len(slot, ln) - 30, 80)

    mid = mido.MidiFile(type=0, ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo",
                                  tempo=mido.bpm2tempo(RAG_BPM), time=0))
    last = 0
    for tick, _, msg in sorted(ev, key=lambda e: (e[0], e[1])):
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track",
                                  time=RAG_BARS * 4 * PPQ - last))
    mid.tracks.append(track)
    return mid


# ----------------------------------------------------- Back-Alley Blues

# Scene 03: the Rustlers' alley. The Dockside theme's lonely cousin —
# same harbor, fewer streetlights. Sparse walking bass, one e-piano
# stab per bar, a muted lead that mostly declines to comment.
ALLEY_BPM = 76
ALLEY_BARS = 12
ALLEY_LOOP_BEATS = ALLEY_BARS * 4 + 1

ALLEY_PROG = ["Am", "Am", "Dm6", "Am", "F", "E7", "Am", "E7",
              "Am", "Dm6", "E7", "Am"]
ALLEY_CHORDS = {
    "Am":  [n("A", 3), n("C", 4), n("E", 4)],
    "Dm6": [n("D", 3), n("F", 3), n("B", 3)],
    "F":   [n("F", 3), n("A", 3), n("C", 4)],
    "E7":  [n("E", 3), n("Ab", 3), n("D", 4)],
}
ALLEY_ROOTS = {"Am": n("A", 1), "Dm6": n("D", 2), "F": n("F", 1),
               "E7": n("E", 2)}
ALLEY_FIFTH = {"Am": n("E", 2), "Dm6": n("A", 2), "F": n("C", 2),
               "E7": n("B", 2)}

# the lead speaks in bars 3-4, 7-8 and 11-12 and otherwise minds its own
AM = []
def alley_phrase(bar, notes):
    for slot, pitch, ln in notes:
        AM.append((bar, slot, pitch, ln))

alley_phrase(3,  [(0, n("A", 4), 2), (2, n("C", 5), 1), (3, n("B", 4), 1),
                  (4, n("A", 4), 4)])
alley_phrase(4,  [(0, n("E", 4), 6)])
alley_phrase(7,  [(0, n("C", 5), 2), (2, n("B", 4), 1), (3, n("A", 4), 1),
                  (4, n("E", 4), 3)])
alley_phrase(8,  [(0, n("Ab", 4), 4), (4, n("B", 4), 2)])
alley_phrase(11, [(0, n("E", 5), 2), (2, n("D", 5), 1), (3, n("B", 4), 1),
                  (4, n("Ab", 4), 2)])
alley_phrase(12, [(0, n("A", 4), 8)])


def build_backalley():
    ev = []

    def add(tick, msg, order=1):
        ev.append((tick, order, msg))

    for ch, prg, vol in [(CH_LEAD, PRG_LEAD, 62), (CH_BASS, PRG_BASS, 92),
                         (CH_EP, PRG_EP, 58)]:
        add(0, mido.Message("program_change", channel=ch, program=prg), 0)
        add(0, mido.Message("control_change", channel=ch, control=7,
                            value=vol), 0)

    for bar in range(1, ALLEY_BARS + 1):
        chord = ALLEY_PROG[bar - 1]
        t0 = (bar - 1) * 4 * PPQ

        # bass: root on 1, fifth on 3, nothing in between. An alley walk.
        for beat, pitch in [(0, ALLEY_ROOTS[chord]),
                            (2, ALLEY_FIFTH[chord])]:
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_BASS,
                                note=pitch, velocity=70))
            add(t + PPQ * 4 // 5, mido.Message(
                "note_off", channel=CH_BASS, note=pitch, velocity=0))

        # e-piano: one stab per bar, on the and-of-two, like a shrug
        t = t0 + PPQ + E_LONG
        for pitch in ALLEY_CHORDS[chord]:
            add(t, mido.Message("note_on", channel=CH_EP,
                                note=pitch, velocity=44))
            add(t + PPQ // 2, mido.Message(
                "note_off", channel=CH_EP, note=pitch, velocity=0))

    for bar, slot, pitch, ln in AM:
        t = slot_time(bar, slot)
        add(t, mido.Message("note_on", channel=CH_LEAD, note=pitch,
                            velocity=56))
        add(t + slot_len(slot, ln) - 30, mido.Message(
            "note_off", channel=CH_LEAD, note=pitch, velocity=0))

    mid = mido.MidiFile(type=0, ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo",
                                  tempo=mido.bpm2tempo(ALLEY_BPM), time=0))
    last = 0
    for tick, _, msg in sorted(ev, key=lambda e: (e[0], e[1])):
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track",
                                  time=ALLEY_BARS * 4 * PPQ - last))
    mid.tracks.append(track)
    return mid


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for name, build, bars, bpm, loop in [
            ("dockside", build_dockside, BARS, BPM, LOOP_BEATS),
            ("scrapnbarrel", build_rag, RAG_BARS, RAG_BPM, RAG_LOOP_BEATS),
            ("backalley", build_backalley, ALLEY_BARS, ALLEY_BPM,
             ALLEY_LOOP_BEATS)]:
        path = os.path.join(OUTDIR, f"{name}.mid")
        build().save(path)
        print(f"{path}  ({bars} bars, {bars * 4 * 60 / bpm:.0f}s, "
              f"loop at beat {loop})")


if __name__ == "__main__":
    main()
