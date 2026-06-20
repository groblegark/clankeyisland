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
# NOTE: must NOT be named `RM` — build_march below reuses that global name
# for its own 16-bar melody, and since every build_*() reads the global at
# call time, the march list would shadow this one and feed build_rag four
# extra bars (past the nominal 12), driving end_of_track negative on save.
RAG_RM = []
def rag_phrase(bar, notes):
    for slot, pitch, ln in notes:
        RAG_RM.append((bar, slot, pitch, ln))

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

    for bar, slot, pitch, ln in RAG_RM:
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


# ----------------------------------------- the Clanker City Shuffle

# Scene 04: Midtown Gearworks. The GDD names this one: jazzy mechanical
# swing. Uptempo, major key, walking bass that actually walks, and a
# lead that's proud of itself. Everything the docks aren't.
SHUF_BPM = 132
SHUF_BARS = 16
SHUF_LOOP_BEATS = SHUF_BARS * 4 + 1

SHUF_PROG = ["C6", "C6", "F9", "C6", "Am", "D9", "G13", "G13",
             "C6", "C6", "F9", "F9", "C6", "Am", "D9G", "C6"]
SHUF_CHORDS = {
    "C6":  [n("E", 3), n("G", 3), n("A", 3), n("C", 4)],
    "F9":  [n("F", 3), n("A", 3), n("Eb", 4), n("G", 4)],
    "Am":  [n("A", 3), n("C", 4), n("E", 4)],
    "D9":  [n("D", 3), n("Gb", 3), n("C", 4), n("E", 4)],
    "G13": [n("G", 3), n("B", 3), n("F", 4), n("E", 4)],
    "D9G": [n("D", 3), n("Gb", 3), n("C", 4)],
}
SHUF_ROOTS = {"C6": n("C", 2), "F9": n("F", 2), "Am": n("A", 1),
              "D9": n("D", 2), "G13": n("G", 2), "D9G": n("D", 2)}
# walking bass: root, third-ish, fifth, approach
SHUF_WALK = {
    "C6":  [n("C", 2), n("E", 2), n("G", 2), n("A", 2)],
    "F9":  [n("F", 2), n("A", 2), n("C", 3), n("Eb", 3)],
    "Am":  [n("A", 1), n("C", 2), n("E", 2), n("G", 2)],
    "D9":  [n("D", 2), n("Gb", 2), n("A", 2), n("C", 3)],
    "G13": [n("G", 2), n("B", 2), n("D", 3), n("F", 3)],
    "D9G": [n("D", 2), n("Gb", 2), n("G", 2), n("B", 2)],
}

# the lead, proud of itself
SM = []
def shuf_phrase(bar, notes):
    for slot, pitch, ln in notes:
        SM.append((bar, slot, pitch, ln))

shuf_phrase(1,  [(0, n("G", 4), 1), (1, n("A", 4), 1), (2, n("C", 5), 1),
                 (3, n("E", 5), 1), (4, n("G", 5), 3)])
shuf_phrase(2,  [(0, n("E", 5), 1), (2, n("C", 5), 1), (4, n("A", 4), 2),
                 (6, n("G", 4), 2)])
shuf_phrase(3,  [(0, n("A", 4), 1), (1, n("C", 5), 1), (2, n("Eb", 5), 1),
                 (3, n("F", 5), 1), (4, n("G", 5), 2), (6, n("F", 5), 2)])
shuf_phrase(4,  [(0, n("E", 5), 4)])
shuf_phrase(5,  [(0, n("E", 5), 1), (1, n("D", 5), 1), (2, n("C", 5), 1),
                 (3, n("B", 4), 1), (4, n("A", 4), 3)])
shuf_phrase(6,  [(0, n("Gb", 4), 1), (2, n("A", 4), 1), (4, n("C", 5), 2),
                 (6, n("E", 5), 2)])
shuf_phrase(7,  [(0, n("D", 5), 2), (2, n("B", 4), 1), (3, n("G", 4), 1),
                 (4, n("F", 5), 2), (6, n("E", 5), 1), (7, n("D", 5), 1)])
shuf_phrase(8,  [(0, n("B", 4), 2), (4, n("G", 4), 2)])
shuf_phrase(9,  [(0, n("C", 5), 1), (1, n("E", 5), 1), (2, n("G", 5), 1),
                 (3, n("A", 5), 1), (4, n("G", 5), 3)])
shuf_phrase(10, [(0, n("E", 5), 1), (2, n("A", 4), 1), (4, n("C", 5), 4)])
shuf_phrase(11, [(0, n("Eb", 5), 1), (1, n("F", 5), 1), (2, n("G", 5), 2),
                 (4, n("A", 5), 2), (6, n("G", 5), 2)])
shuf_phrase(12, [(0, n("F", 5), 4), (4, n("Eb", 5), 2)])
shuf_phrase(13, [(0, n("E", 5), 1), (1, n("G", 5), 1), (2, n("A", 5), 1),
                 (3, n("C", 6), 1), (4, n("A", 5), 3)])
shuf_phrase(14, [(0, n("E", 5), 1), (2, n("C", 5), 1), (4, n("A", 4), 2),
                 (6, n("C", 5), 2)])
shuf_phrase(15, [(0, n("E", 5), 1), (1, n("D", 5), 1), (2, n("C", 5), 1),
                 (3, n("B", 4), 1), (4, n("D", 5), 2), (6, n("B", 4), 2)])
shuf_phrase(16, [(0, n("C", 5), 6)])


def build_shuffle():
    ev = []

    def add(tick, msg, order=1):
        ev.append((tick, order, msg))

    for ch, prg, vol in [(CH_LEAD, PRG_LEAD, 88), (CH_BASS, PRG_BASS, 102),
                         (CH_EP, PRG_EP, 70), (CH_DRUM, 0, 94)]:
        add(0, mido.Message("program_change", channel=ch, program=prg), 0)
        add(0, mido.Message("control_change", channel=ch, control=7,
                            value=vol), 0)

    for bar in range(1, SHUF_BARS + 1):
        chord = SHUF_PROG[bar - 1]
        t0 = (bar - 1) * 4 * PPQ

        # bass: actually walking, four to the bar
        for beat in range(4):
            pitch = SHUF_WALK[chord][beat]
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_BASS,
                                note=pitch, velocity=82))
            add(t + PPQ * 7 // 10, mido.Message(
                "note_off", channel=CH_BASS, note=pitch, velocity=0))

        # e-piano: charleston comp — beat 1, and the and-of-two
        for tick in (t0, t0 + PPQ + E_LONG):
            for pitch in SHUF_CHORDS[chord]:
                add(tick, mido.Message("note_on", channel=CH_EP,
                                       note=pitch, velocity=56))
                add(tick + E_SHORT, mido.Message(
                    "note_off", channel=CH_EP, note=pitch, velocity=0))

        # drums: ride-pattern hats, kick 1/3, crisp snare 2/4
        for slot in range(8):
            t = t0 + slot_time(1, slot)
            add(t, mido.Message("note_on", channel=CH_DRUM, note=HAT,
                                velocity=50 if slot % 2 else 66))
            add(t + 40, mido.Message("note_off", channel=CH_DRUM,
                                     note=HAT, velocity=0))
        for beat, drum, vel in [(0, KICK, 92), (2, KICK, 76),
                                (1, SNARE, 72), (3, SNARE, 78)]:
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_DRUM, note=drum,
                                velocity=vel))
            add(t + 60, mido.Message("note_off", channel=CH_DRUM,
                                     note=drum, velocity=0))

    for bar, slot, pitch, ln in SM:
        t = slot_time(bar, slot)
        add(t, mido.Message("note_on", channel=CH_LEAD, note=pitch,
                            velocity=80))
        add(t + slot_len(slot, ln) - 30, mido.Message(
            "note_off", channel=CH_LEAD, note=pitch, velocity=0))

    mid = mido.MidiFile(type=0, ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo",
                                  tempo=mido.bpm2tempo(SHUF_BPM), time=0))
    last = 0
    for tick, _, msg in sorted(ev, key=lambda e: (e[0], e[1])):
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track",
                                  time=SHUF_BARS * 4 * PPQ - last))
    mid.tracks.append(track)
    return mid


# ------------------------------------------------- the Grand Cog Vamp

# Scene 05: house music inside the theater. An 8-bar showbiz vamp that
# could loop all night and intends to: two-feel bass, charleston comp,
# brushes, and a lead that only speaks when spoken to.
VAMP_BPM = 118
VAMP_BARS = 8
VAMP_LOOP_BEATS = VAMP_BARS * 4 + 1

VAMP_PROG = ["C6", "Am", "Dm7", "G13", "C6", "A7v", "Dm7", "G13"]
VAMP_CHORDS = {
    "C6":  [n("E", 3), n("G", 3), n("A", 3), n("C", 4)],
    "Am":  [n("A", 3), n("C", 4), n("E", 4)],
    "Dm7": [n("D", 3), n("F", 3), n("A", 3), n("C", 4)],
    "G13": [n("G", 3), n("B", 3), n("F", 4), n("E", 4)],
    "A7v": [n("A", 3), n("Db", 4), n("G", 4)],
}
VAMP_ROOTS = {"C6": n("C", 2), "Am": n("A", 1), "Dm7": n("D", 2),
              "G13": n("G", 2), "A7v": n("A", 1)}
VAMP_FIFTH = {"C6": n("G", 2), "Am": n("E", 2), "Dm7": n("A", 2),
              "G13": n("D", 3), "A7v": n("E", 2)}

VM = []
def vamp_phrase(bar, notes):
    for slot, pitch, ln in notes:
        VM.append((bar, slot, pitch, ln))

vamp_phrase(4, [(0, n("D", 5), 1), (1, n("E", 5), 1), (2, n("F", 5), 1),
                (3, n("E", 5), 1), (4, n("D", 5), 2)])
vamp_phrase(8, [(0, n("B", 4), 1), (2, n("D", 5), 1), (4, n("E", 5), 2),
                (6, n("G", 4), 2)])


def build_vamp():
    ev = []

    def add(tick, msg, order=1):
        ev.append((tick, order, msg))

    for ch, prg, vol in [(CH_LEAD, PRG_LEAD, 70), (CH_BASS, PRG_BASS, 96),
                         (CH_EP, PRG_EP, 64), (CH_DRUM, 0, 78)]:
        add(0, mido.Message("program_change", channel=ch, program=prg), 0)
        add(0, mido.Message("control_change", channel=ch, control=7,
                            value=vol), 0)

    for bar in range(1, VAMP_BARS + 1):
        chord = VAMP_PROG[bar - 1]
        t0 = (bar - 1) * 4 * PPQ

        # two-feel bass: root on 1, fifth on 3
        for beat, pitch in [(0, VAMP_ROOTS[chord]), (2, VAMP_FIFTH[chord])]:
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_BASS,
                                note=pitch, velocity=74))
            add(t + PPQ * 4 // 5, mido.Message(
                "note_off", channel=CH_BASS, note=pitch, velocity=0))

        # charleston comp
        for tick in (t0, t0 + PPQ + E_LONG):
            for pitch in VAMP_CHORDS[chord]:
                add(tick, mido.Message("note_on", channel=CH_EP,
                                       note=pitch, velocity=50))
                add(tick + E_SHORT, mido.Message(
                    "note_off", channel=CH_EP, note=pitch, velocity=0))

        # brushes: hats on the swung eighths, rimshot on 4
        for slot in range(8):
            t = t0 + slot_time(1, slot)
            add(t, mido.Message("note_on", channel=CH_DRUM, note=HAT,
                                velocity=38 if slot % 2 else 52))
            add(t + 40, mido.Message("note_off", channel=CH_DRUM,
                                     note=HAT, velocity=0))
        t = t0 + 3 * PPQ
        add(t, mido.Message("note_on", channel=CH_DRUM, note=SNARE,
                            velocity=52))
        add(t + 50, mido.Message("note_off", channel=CH_DRUM,
                                 note=SNARE, velocity=0))

    for bar, slot, pitch, ln in VM:
        t = slot_time(bar, slot)
        add(t, mido.Message("note_on", channel=CH_LEAD, note=pitch,
                            velocity=62))
        add(t + slot_len(slot, ln) - 30, mido.Message(
            "note_off", channel=CH_LEAD, note=pitch, velocity=0))

    mid = mido.MidiFile(type=0, ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo",
                                  tempo=mido.bpm2tempo(VAMP_BPM), time=0))
    last = 0
    for tick, _, msg in sorted(ev, key=lambda e: (e[0], e[1])):
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track",
                                  time=VAMP_BARS * 4 * PPQ - last))
    mid.tracks.append(track)
    return mid


# ----------------------------------------------- Nothing Is Wrong (March)

# Scene 08: City Hall. A civic march -- straight, not swung (Midtown
# swings, City Hall marches). 16 bars, 4/4, Bb major, 96 BPM. The joke is
# structural: bars 1-8 are pure confidence (fanfare up the Bb triad);
# bars 9-16 the bass starts resting on beat 3 (the march checking its own
# gauge) while the lead keeps going as if nothing is wrong. Underneath the
# whole form, a pedal A1 -- a half-step under the tonic's root -- holds at
# low velocity: the Dynamo's hum, flat by half a step (the N-A5 detuning
# motif's first scored appearance).
MARCH_BPM = 96
MARCH_BARS = 16
MARCH_LOOP_BEATS = MARCH_BARS * 4 + 1   # 65

# I -- IV -- V -- I civic changes, two 8-bar passes
MARCH_PROG = ["Bb", "Bb", "Eb", "Bb", "F", "F", "Bb", "Bb",
              "Bb", "Eb", "Bb", "F", "Eb", "Bb", "F", "Bb"]
MARCH_CHORDS = {
    "Bb": [n("Bb", 3), n("D", 4), n("F", 4)],
    "Eb": [n("Eb", 3), n("G", 3), n("Bb", 3)],
    "F":  [n("F", 3), n("A", 3), n("C", 4)],
}
MARCH_ROOTS = {"Bb": n("Bb", 2), "Eb": n("Eb", 2), "F": n("F", 2)}
MARCH_FIFTH = {"Bb": n("F", 2), "Eb": n("Bb", 2), "F": n("C", 3)}

CH_PEDAL = 3                                  # the flat hum
PRG_TRUMPET = 56                              # canonical lead (fallback 80)
PRG_PEDAL = 38

# the lead: a fanfare that squares its shoulders and never sits down.
# straight quarters/eighths (slots here are STRAIGHT eighths, 8 per bar)
RM = []
def march_phrase(bar, notes):
    for slot, pitch, ln in notes:
        RM.append((bar, slot, pitch, ln))

march_phrase(1,  [(0, n("Bb", 4), 2), (2, n("D", 5), 2), (4, n("F", 5), 4)])
march_phrase(2,  [(0, n("F", 5), 2), (2, n("D", 5), 2), (4, n("Bb", 4), 4)])
march_phrase(3,  [(0, n("Eb", 5), 2), (2, n("G", 5), 2), (4, n("Bb", 5), 4)])
march_phrase(4,  [(0, n("Bb", 5), 2), (2, n("G", 5), 2), (4, n("D", 5), 4)])
march_phrase(5,  [(0, n("C", 5), 2), (2, n("F", 5), 2), (4, n("A", 5), 4)])
march_phrase(6,  [(0, n("A", 5), 2), (2, n("F", 5), 2), (4, n("C", 5), 4)])
march_phrase(7,  [(0, n("Bb", 4), 2), (2, n("F", 5), 2), (4, n("D", 5), 2),
                  (6, n("Bb", 4), 2)])
march_phrase(8,  [(0, n("Bb", 4), 8)])
march_phrase(9,  [(0, n("Bb", 4), 2), (2, n("D", 5), 2), (4, n("F", 5), 4)])
march_phrase(10, [(0, n("Bb", 5), 2), (2, n("G", 5), 2), (4, n("Eb", 5), 4)])
march_phrase(11, [(0, n("D", 5), 2), (2, n("F", 5), 2), (4, n("Bb", 5), 4)])
march_phrase(12, [(0, n("C", 5), 2), (2, n("A", 5), 2), (4, n("F", 5), 4)])
march_phrase(13, [(0, n("Eb", 5), 2), (2, n("G", 5), 2), (4, n("Bb", 5), 4)])
march_phrase(14, [(0, n("Bb", 5), 2), (2, n("F", 5), 2), (4, n("D", 5), 4)])
march_phrase(15, [(0, n("F", 5), 2), (2, n("A", 5), 2), (4, n("C", 6), 4)])
march_phrase(16, [(0, n("Bb", 5), 8)])


def march_slot_time(bar, slot):
    """Absolute ticks of a STRAIGHT-eighth slot (8 per bar)."""
    return (bar - 1) * 4 * PPQ + slot * (PPQ // 2)


def build_march():
    ev = []

    def add(tick, msg, order=1):
        ev.append((tick, order, msg))

    for ch, prg, vol in [(CH_LEAD, PRG_TRUMPET, 96), (CH_BASS, PRG_BASS, 100),
                         (CH_EP, PRG_EP, 64), (CH_PEDAL, PRG_PEDAL, 28),
                         (CH_DRUM, 0, 96)]:
        add(0, mido.Message("program_change", channel=ch, program=prg), 0)
        add(0, mido.Message("control_change", channel=ch, control=7,
                            value=vol), 0)

    # the flat hum: a continuous pedal A1, low and underneath everything,
    # re-struck each bar so AdLib voices don't time out
    PEDAL = n("A", 1)
    for bar in range(1, MARCH_BARS + 1):
        t0 = (bar - 1) * 4 * PPQ
        add(t0, mido.Message("note_on", channel=CH_PEDAL,
                             note=PEDAL, velocity=28))
        add(t0 + 4 * PPQ - 10, mido.Message(
            "note_off", channel=CH_PEDAL, note=PEDAL, velocity=0))

    for bar in range(1, MARCH_BARS + 1):
        chord = MARCH_PROG[bar - 1]
        t0 = (bar - 1) * 4 * PPQ
        second_half = bar > 8         # the march starts checking its gauge

        # bass: oom on 1 and 3 (root), pah-fifth on 2 and 4 -- but in the
        # second half the beat-3 oom RESTS (the march checking its gauge)
        for beat in range(4):
            if second_half and beat == 2:
                continue              # the dropped beat-3 root
            if beat % 2 == 0:
                pitch = MARCH_ROOTS[chord]
            else:
                pitch = MARCH_FIFTH[chord]
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_BASS,
                                note=pitch, velocity=90))
            add(t + PPQ * 3 // 5, mido.Message(
                "note_off", channel=CH_BASS, note=pitch, velocity=0))

        # e-piano: block chords on the off-beats (2 and 4)
        for beat in (1, 3):
            t = t0 + beat * PPQ
            for pitch in MARCH_CHORDS[chord]:
                add(t, mido.Message("note_on", channel=CH_EP,
                                    note=pitch, velocity=52))
                add(t + PPQ // 2, mido.Message(
                    "note_off", channel=CH_EP, note=pitch, velocity=0))

        # drums: kick on 1/3, light hat on every eighth, parade snare with
        # a 16th-note pickup roll into bars 1 and 9
        for slot in range(8):
            t = march_slot_time(bar, slot)
            add(t, mido.Message("note_on", channel=CH_DRUM, note=HAT,
                                velocity=44 if slot % 2 else 56))
            add(t + 30, mido.Message("note_off", channel=CH_DRUM,
                                     note=HAT, velocity=0))
        for beat in (0, 2):
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_DRUM, note=KICK,
                                velocity=96))
            add(t + 50, mido.Message("note_off", channel=CH_DRUM,
                                     note=KICK, velocity=0))
        for beat in (1, 3):
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_DRUM, note=SNARE,
                                velocity=80))
            add(t + 50, mido.Message("note_off", channel=CH_DRUM,
                                     note=SNARE, velocity=0))

    # snare pickup rolls (16ths) into the downbeat of bars 1 and 9
    for downbar in (1, 9):
        t0 = (downbar - 1) * 4 * PPQ
        for k in range(1, 5):
            t = t0 - k * (PPQ // 4)
            if t < 0:
                continue
            add(t, mido.Message("note_on", channel=CH_DRUM, note=SNARE,
                                velocity=48 + (4 - k) * 8))
            add(t + 24, mido.Message("note_off", channel=CH_DRUM,
                                     note=SNARE, velocity=0))

    # the lead fanfare
    for bar, slot, pitch, ln in RM:
        t = march_slot_time(bar, slot)
        dur = ln * (PPQ // 2)
        add(t, mido.Message("note_on", channel=CH_LEAD, note=pitch,
                            velocity=92))
        add(t + dur - 30, mido.Message(
            "note_off", channel=CH_LEAD, note=pitch, velocity=0))

    mid = mido.MidiFile(type=0, ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo",
                                  tempo=mido.bpm2tempo(MARCH_BPM), time=0))
    last = 0
    for tick, _, msg in sorted(ev, key=lambda e: (e[0], e[1])):
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track",
                                  time=MARCH_BARS * 4 * PPQ - last))
    mid.tracks.append(track)
    return mid


# ===================================================================
# "The Rustlers' Den" (Scene 09) -- a work-shanty gone indoor, the alley
# blues' meaner cousin. 16 bars, 4/4, G minor, 92 BPM. The lead carries a
# constant -40-cent pitchwheel bend from tick 0: the den is downstream of
# the same dying hum as everyone else, and its song cannot quite hold true
# against its own bass (N-A5 -- Act 3's clock made audible). This is the
# on-screen evidence for the parley's "the hum is flat and dropping" line.

DEN_BPM = 92
DEN_BARS = 16
DEN_LOOP_BEATS = DEN_BARS * 4 + 1   # = 65 (the iMUSE loop point)
DEN_BEND = -1638                     # ~ -40 cents at the default +/-2 range

DEN_PROG = ["Gm", "Gm", "Cm", "Cm", "D7", "Gm", "Cm", "D7",
            "Gm", "Gm", "Eb", "Eb", "Cm", "D7", "Gm", "Gm"]
DEN_CHORDS = {
    "Gm": [n("G", 3), n("Bb", 3), n("D", 4)],
    "Cm": [n("C", 3), n("Eb", 3), n("G", 3)],
    "D7": [n("D", 3), n("Gb", 3), n("C", 4)],
    "Eb": [n("Eb", 3), n("G", 3), n("Bb", 3)],
}
DEN_ROOTS = {"Gm": n("G", 2), "Cm": n("C", 2), "D7": n("D", 2),
             "Eb": n("Eb", 2)}

PRG_ACCORDION = 21          # GM 21 accordion lead (audition fallback GM 80)
PRG_DEN_BASS = 38           # GM 38 synth bass

# the lead: call-and-response phrases that always land a beat late, like a
# crew that hauls on "heave" not "ho." enters bar 3. straight eighths.
DM = []
def den_phrase(bar, notes):
    for slot, pitch, ln in notes:
        DM.append((bar, slot, pitch, ln))

den_phrase(3,  [(2, n("G", 4), 2), (4, n("Bb", 4), 2), (6, n("C", 5), 2)])
den_phrase(4,  [(2, n("Bb", 4), 2), (4, n("G", 4), 4)])
den_phrase(5,  [(2, n("A", 4), 2), (4, n("D", 5), 2), (6, n("C", 5), 2)])
den_phrase(6,  [(2, n("Bb", 4), 2), (4, n("G", 4), 4)])
den_phrase(7,  [(2, n("Eb", 5), 2), (4, n("C", 5), 2), (6, n("G", 4), 2)])
den_phrase(8,  [(2, n("Gb", 4), 2), (4, n("A", 4), 4)])
den_phrase(11, [(2, n("Bb", 4), 2), (4, n("Eb", 5), 2), (6, n("D", 5), 2)])
den_phrase(12, [(2, n("Bb", 4), 2), (4, n("G", 4), 4)])
den_phrase(13, [(2, n("C", 5), 2), (4, n("Eb", 5), 2), (6, n("D", 5), 2)])
den_phrase(14, [(2, n("Gb", 4), 2), (4, n("A", 4), 4)])
den_phrase(15, [(2, n("G", 4), 2), (4, n("Bb", 4), 2), (6, n("D", 5), 2)])
den_phrase(16, [(0, n("G", 4), 8)])


def den_slot_time(bar, slot):
    """Absolute ticks of a STRAIGHT-eighth slot (8 per bar)."""
    return (bar - 1) * 4 * PPQ + slot * (PPQ // 2)


def build_den():
    ev = []

    def add(tick, msg, order=1):
        ev.append((tick, order, msg))

    for ch, prg, vol in [(CH_LEAD, PRG_ACCORDION, 88),
                         (CH_BASS, PRG_DEN_BASS, 104), (CH_DRUM, 0, 96)]:
        add(0, mido.Message("program_change", channel=ch, program=prg), 0)
        add(0, mido.Message("control_change", channel=ch, control=7,
                            value=vol), 0)

    # the detuning hum: the lead bends flat from tick 0 and stays there.
    add(0, mido.Message("pitchwheel", channel=CH_LEAD, pitch=DEN_BEND), 0)

    for bar in range(1, DEN_BARS + 1):
        chord = DEN_PROG[bar - 1]
        t0 = (bar - 1) * 4 * PPQ

        # bass: boots on planks, roots stomped on beats 1 and 3 ONLY (no
        # walk -- the alley blues' meaner cousin)
        for beat in (0, 2):
            t = t0 + beat * PPQ
            pitch = DEN_ROOTS[chord]
            add(t, mido.Message("note_on", channel=CH_BASS,
                                note=pitch, velocity=100))
            add(t + PPQ * 3 // 5, mido.Message(
                "note_off", channel=CH_BASS, note=pitch, velocity=0))

        # drums: kick doubles the stomp (1 and 3), snare on 2 and 4, NO hat
        # (sparser = menace)
        for beat in (0, 2):
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_DRUM, note=KICK,
                                velocity=100))
            add(t + 50, mido.Message("note_off", channel=CH_DRUM,
                                     note=KICK, velocity=0))
        for beat in (1, 3):
            t = t0 + beat * PPQ
            add(t, mido.Message("note_on", channel=CH_DRUM, note=SNARE,
                                velocity=78))
            add(t + 50, mido.Message("note_off", channel=CH_DRUM,
                                     note=SNARE, velocity=0))

    # the lead: call-and-response, landing a beat late
    for bar, slot, pitch, ln in DM:
        t = den_slot_time(bar, slot)
        dur = ln * (PPQ // 2)
        add(t, mido.Message("note_on", channel=CH_LEAD, note=pitch,
                            velocity=86))
        add(t + dur - 30, mido.Message(
            "note_off", channel=CH_LEAD, note=pitch, velocity=0))

    mid = mido.MidiFile(type=0, ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo",
                                  tempo=mido.bpm2tempo(DEN_BPM), time=0))
    last = 0
    for tick, _, msg in sorted(ev, key=lambda e: (e[0], e[1])):
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track",
                                  time=DEN_BARS * 4 * PPQ - last))
    mid.tracks.append(track)
    return mid


def emit_den():
    """Emit ONLY rustlersden.mid -- do NOT run main(), which crashes on
    build_rag's mido negative-delta bug (Scene 08 did the same for
    cityhall.mid). Run: python3 -c 'import genmusic; genmusic.emit_den()'
    or via the __main__ guard below with the 'den' argument."""
    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, "rustlersden.mid")
    build_den().save(path)
    print(f"{path}  ({DEN_BARS} bars, "
          f"{DEN_BARS * 4 * 60 / DEN_BPM:.0f}s, loop at beat {DEN_LOOP_BEATS})")


# ------------------------------------------------ The Dynamo's Hum (N-A5)

# Scene 10: the Dynamo District. Not a tune -- a drone that is winding down
# and detuned. The GDD's designed clock, finally diegetic and central: it is
# this room's music, the gate puzzle's timing source, and audibly FLAT by a
# half-step up close. Two act-flag states so the dry run can audibly reverse
# it (the N-A5 pitch-drift, scoped to this room):
#   dynamohum (default): the hum nearly gone, voiced a semitone LOW -- the
#     drone sits on Db where D belongs (a real semitone, GM-on-AdLib safe).
#   dynamohum_lift (dry-run cue): the same 8 bars transposed up to D, fuller
#     (lead drops fewer notes, EP swells, +6 on cc7) -- the half-step lift.
# 8 bars, 50 BPM (a dying machine), 4/4. Sparse, three voices, no drums.
DHUM_BPM = 50
DHUM_BARS = 8
DHUM_LOOP_BEATS = DHUM_BARS * 4 + 1     # 33

PRG_DRONE = 38    # synth bass (the sustained low drone)
PRG_PAD = 4       # e-piano (the slow pulsing mid cluster)
PRG_HUMLEAD = 80  # square (the faltering lead that drops notes)

# the faltering lead: a slow line that should hold the hum's pitch but
# keeps losing beats as the machine fails. (bar, slot[0..7], scale-degree
# offset from the drone root, len-slots). The MISSING set silences ~1 in 3.
DHUM_LEAD = [
    (1, 0, 12, 4), (1, 4, 19, 4),
    (2, 0, 15, 2), (2, 2, 12, 2), (2, 4, 12, 4),
    (3, 0, 19, 4), (3, 4, 15, 4),
    (4, 0, 12, 8),
    (5, 0, 12, 4), (5, 4, 19, 4),
    (6, 0, 15, 2), (6, 2, 17, 2), (6, 4, 12, 4),
    (7, 0, 19, 4), (7, 4, 15, 4),
    (8, 0, 12, 8),
]
# notes that "drop out" -- silenced as the hum misses beats (~1 in 3)
DHUM_MISSING = {(2, 2), (3, 4), (5, 4), (6, 2), (7, 4)}


def _build_dynamohum(transpose, lifted):
    """transpose: semitone shift of the whole drone (0 = Db home; +1 = D).
    lifted: the dry-run version -- fuller, fewer dropped notes, louder."""
    ev = []

    def add(tick, msg, order=1):
        ev.append((tick, order, msg))

    # the drone root: Db1 at home (the flat), D1 when lifted. fifth above.
    root = n("Db", 1) + transpose
    fifth = n("Ab", 1) + transpose
    cluster = [n("Db", 3) + transpose, n("E", 3) + transpose,
               n("Ab", 3) + transpose]      # a Db-minor-ish breathing cluster

    bump = 6 if lifted else 0
    for ch, prg, vol in [(CH_LEAD, PRG_HUMLEAD, 44 + bump),
                         (CH_BASS, PRG_DRONE, 52 + bump),
                         (CH_EP, PRG_PAD, 40 + bump)]:
        add(0, mido.Message("program_change", channel=ch, program=prg), 0)
        add(0, mido.Message("control_change", channel=ch, control=7,
                            value=vol), 0)

    # the sustained low drone: root + fifth, re-struck each bar so AdLib
    # voices don't time out. low velocity (a machine, barely turning).
    for bar in range(1, DHUM_BARS + 1):
        t0 = (bar - 1) * 4 * PPQ
        for p in (root, fifth):
            add(t0, mido.Message("note_on", channel=CH_BASS, note=p,
                                 velocity=48 + bump))
            add(t0 + 4 * PPQ - 8, mido.Message(
                "note_off", channel=CH_BASS, note=p, velocity=0))

    # the slow pulsing mid: the cluster breathes once per bar (swells more
    # when lifted -- a longer, fuller bloom)
    cl_len = (PPQ * 3) if lifted else (PPQ * 2)
    for bar in range(1, DHUM_BARS + 1):
        t0 = (bar - 1) * 4 * PPQ + PPQ      # land it on beat 2
        for p in cluster:
            add(t0, mido.Message("note_on", channel=CH_EP, note=p,
                                 velocity=40 + bump))
            add(t0 + cl_len, mido.Message(
                "note_off", channel=CH_EP, note=p, velocity=0))

    # the faltering lead: drops notes as it fails. when lifted, fewer drop
    # (the hum catching) -- skip only every OTHER missing note.
    drop_idx = 0
    for bar, slot, deg, ln in DHUM_LEAD:
        is_missing = (bar, slot) in DHUM_MISSING
        if is_missing:
            drop_idx += 1
            if not lifted:
                continue                    # flat: all missing notes silent
            if drop_idx % 2 == 0:
                continue                    # lifted: only half still drop
        pitch = root + 12 + deg            # an octave + scale degree up
        t = (bar - 1) * 4 * PPQ + slot * (PPQ // 2)
        dur = ln * (PPQ // 2)
        add(t, mido.Message("note_on", channel=CH_LEAD, note=pitch,
                            velocity=50 + bump))
        add(t + dur - 20, mido.Message(
            "note_off", channel=CH_LEAD, note=pitch, velocity=0))

    mid = mido.MidiFile(type=0, ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("set_tempo",
                                  tempo=mido.bpm2tempo(DHUM_BPM), time=0))
    last = 0
    for tick, _, msg in sorted(ev, key=lambda e: (e[0], e[1])):
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track",
                                  time=DHUM_BARS * 4 * PPQ - last))
    mid.tracks.append(track)
    return mid


def build_dynamohum():
    return _build_dynamohum(transpose=0, lifted=False)


def build_dynamohum_lift():
    return _build_dynamohum(transpose=1, lifted=True)


def emit_dynamohum():
    """Scene 10's two MIDIs, emitted directly (builder + save), WITHOUT
    running main() -- main()'s build_rag path has a pre-existing crash on
    some mido versions (NOTES.md). This writes ONLY dynamohum*.mid and
    touches no other song. (Mirrors how Scene 08 added cityhall.mid.)"""
    os.makedirs(OUTDIR, exist_ok=True)
    for name, build in [("dynamohum", build_dynamohum),
                        ("dynamohum_lift", build_dynamohum_lift)]:
        path = os.path.join(OUTDIR, f"{name}.mid")
        build().save(path)
        print(f"{path}  ({DHUM_BARS} bars, "
              f"{DHUM_BARS * 4 * 60 / DHUM_BPM:.0f}s, "
              f"loop at beat {DHUM_LOOP_BEATS})")



def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for name, build, bars, bpm, loop in [
            ("dockside", build_dockside, BARS, BPM, LOOP_BEATS),
            ("scrapnbarrel", build_rag, RAG_BARS, RAG_BPM, RAG_LOOP_BEATS),
            ("backalley", build_backalley, ALLEY_BARS, ALLEY_BPM,
             ALLEY_LOOP_BEATS),
            ("shuffle", build_shuffle, SHUF_BARS, SHUF_BPM,
             SHUF_LOOP_BEATS),
            ("vamp", build_vamp, VAMP_BARS, VAMP_BPM, VAMP_LOOP_BEATS),
            ("cityhall", build_march, MARCH_BARS, MARCH_BPM,
             MARCH_LOOP_BEATS)]:
        path = os.path.join(OUTDIR, f"{name}.mid")
        build().save(path)
        print(f"{path}  ({bars} bars, {bars * 4 * 60 / bpm:.0f}s, "
              f"loop at beat {loop})")


if __name__ == "__main__":
    import sys
    # `python3 tools/genmusic.py den` emits ONLY rustlersden.mid, avoiding
    # main()'s pre-existing build_rag crash (mido negative-delta bug).
    if len(sys.argv) > 1 and sys.argv[1] == "den":
        emit_den()
    elif len(sys.argv) > 1 and sys.argv[1] == "emit-dynamo":
        emit_dynamohum()
    else:
        main()
