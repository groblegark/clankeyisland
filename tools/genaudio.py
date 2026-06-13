#!/usr/bin/env python3
"""Generate all Clanker City Chronicles sound effects as VOC files.

Text-first like everything else: each effect is a little synthesis
recipe (decaying metal partials, noise bursts, servo sweeps) rendered
deterministically to 8-bit unsigned mono VOC — the one format ScummC's
`soun -voc` packs into a SOUN/SOU resource that ScummVM's digital mixer
plays on every target, native and wasm alike (see docs/research/AUDIO.md).

Outputs into assets/generated/audio/*.voc
"""

import math
import os
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "generated", "audio")
RATE = 22050


# ------------------------------------------------------------ VOC writer

def write_voc(path, samples):
    """8-bit unsigned mono VOC: header + one type-1 block + terminator."""
    data = bytes(max(0, min(255, int(s * 127) + 128)) for s in samples)
    version = 0x010A
    checksum = (~version + 0x1234) & 0xFFFF
    hdr = b"Creative Voice File\x1a" + struct.pack("<HHH", 26, version, checksum)
    sr_code = 256 - (1000000 // RATE)
    blk_len = len(data) + 2
    block = bytes([1, blk_len & 0xFF, (blk_len >> 8) & 0xFF,
                   (blk_len >> 16) & 0xFF, sr_code, 0]) + data
    with open(path, "wb") as f:
        f.write(hdr + block + b"\x00")


# ----------------------------------------------------------- ingredients

def silence(dur):
    return [0.0] * int(RATE * dur)


def partials(dur, parts, attack=0.002):
    """Sum of decaying sine partials: [(freq, amp, decay_per_sec), ...]"""
    n = int(RATE * dur)
    out = []
    for i in range(n):
        t = i / RATE
        env_in = min(1.0, t / attack) if attack else 1.0
        s = sum(a * math.exp(-d * t) * math.sin(2 * math.pi * f * t)
                for f, a, d in parts)
        out.append(s * env_in)
    return out


def noise_burst(dur, amp, decay):
    """Deterministic pseudo-noise (LCG) with exponential decay."""
    n = int(RATE * dur)
    seed, out = 0x2A, []
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        r = (seed / 0x3FFFFFFF) - 1.0
        out.append(amp * r * math.exp(-decay * i / RATE))
    return out


def mix(*tracks):
    n = max(len(t) for t in tracks)
    out = [0.0] * n
    for t in tracks:
        for i, s in enumerate(t):
            out[i] += s
    peak = max(1e-9, max(abs(s) for s in out))
    return [s * 0.85 / peak for s in out] if peak > 0.85 else out


def concat(*tracks):
    return [s for t in tracks for s in t]


# ---------------------------------------------------------------- effects

def sfx_whack():
    """A good honest whack on a neon sign: clang of inharmonic metal."""
    clang = partials(0.45, [(317, 0.9, 9), (723, 0.7, 11), (1245, 0.5, 14),
                            (2083, 0.35, 18), (3170, 0.2, 24)])
    thump = noise_burst(0.06, 0.8, 60)
    return mix(clang, thump)


def sfx_bolt_drop():
    """A bolt raining onto dock planks: tink, pause, smaller tink."""
    tink = partials(0.12, [(1830, 0.8, 35), (2740, 0.5, 45), (4100, 0.3, 60)])
    tink2 = partials(0.08, [(1830, 0.4, 50), (2740, 0.25, 60)])
    return concat(tink, silence(0.09), tink2)


def sfx_pickup():
    """Servo chirp: a quick rising sweep with a click of satisfaction."""
    n = int(RATE * 0.13)
    sweep = []
    for i in range(n):
        t = i / RATE
        f = 420 + (980 - 420) * (t / 0.13)
        phase = 2 * math.pi * (420 * t + (980 - 420) * t * t / (2 * 0.13))
        square = 1.0 if math.sin(phase) >= 0 else -1.0
        sweep.append(0.35 * square * (1.0 - t / 0.15))
    click = partials(0.03, [(2600, 0.6, 80)])
    return mix(concat(sweep, click))


def sfx_knock():
    """Two polite knocks on a tavern door that opens in Act Two."""
    def thud():
        return mix(partials(0.16, [(118, 1.0, 22), (203, 0.4, 30)]),
                   noise_burst(0.025, 0.5, 120))
    return concat(thud(), silence(0.16), thud())


def sfx_foghorn():
    """The S.S. Eventually's foghorn: a wheeze chosen to be heard as
    optimism. Slow attack, sad droop at the end, breathy throughout."""
    dur, n = 1.4, int(RATE * 1.4)
    out = []
    for i in range(n):
        t = i / RATE
        droop = 1.0 - 0.06 * max(0.0, (t - 0.9) / 0.5)
        f1, f2 = 92 * droop, 138.5 * droop
        env = min(1.0, t / 0.25) * (1.0 if t < 1.0 else max(0.0, 1 - (t - 1.0) / 0.4))
        trem = 1.0 + 0.18 * math.sin(2 * math.pi * 6.5 * t)
        s = (0.7 * math.sin(2 * math.pi * f1 * t)
             + 0.4 * math.sin(2 * math.pi * f2 * t)
             + 0.12 * math.sin(2 * math.pi * 3 * f1 * t))
        out.append(s * env * trem * 0.6)
    breath = noise_burst(dur, 0.1, 1.2)
    return mix(out, breath)


def sfx_ratchet():
    """Gusket's stuck servo getting shimmed: three rising clicks and a
    happy whirr of a glass finally set down."""
    clicks = []
    for i, f in enumerate((900, 1250, 1700)):
        clicks.append(partials(0.05, [(f, 0.7, 60), (f * 2.1, 0.3, 80)]))
        clicks.append(silence(0.07))
    n = int(RATE * 0.35)
    whirr = []
    for i in range(n):
        t = i / RATE
        f = 220 + 340 * t / 0.35
        sq = 1.0 if math.sin(2 * math.pi * f * t) >= 0 else -1.0
        whirr.append(0.25 * sq * (1 - t / 0.4))
    return concat(*clicks, silence(0.05), mix(whirr))


def sfx_dart():
    """One dart: short whoosh, then a cork-board thunk."""
    n = int(RATE * 0.12)
    seed, whoosh = 0x51, []
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        r = (seed / 0x3FFFFFFF) - 1.0
        env = math.sin(math.pi * i / n)
        whoosh.append(0.35 * r * env)
    thunk = mix(partials(0.09, [(210, 1.0, 40), (470, 0.4, 60)]),
                noise_burst(0.02, 0.6, 200))
    return concat(whoosh, thunk)


def sfx_sizzle():
    """A dockworker showing off until his arm servo overheats:
    rising electrical sizzle, pop, sad descending whine."""
    n = int(RATE * 0.7)
    seed, fry = 0xA7, []
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        r = (seed / 0x3FFFFFFF) - 1.0
        env = (i / n) ** 2
        buzz = math.sin(2 * math.pi * 110 * i / RATE)
        fry.append((0.5 * r + 0.3 * buzz) * env * 0.8)
    pop = noise_burst(0.04, 1.0, 90)
    m = int(RATE * 0.5)
    whine = []
    for i in range(m):
        t = i / RATE
        f = 800 - 560 * t / 0.5
        whine.append(0.3 * math.sin(2 * math.pi * f * t) * (1 - t / 0.55))
    return concat(mix(fry), pop, whine)


def sfx_clink():
    """A drink token hitting the bar: two bright coin tinks."""
    t1 = partials(0.1, [(2350, 0.8, 40), (3520, 0.5, 55), (5290, 0.3, 70)])
    t2 = partials(0.07, [(2350, 0.4, 55), (3520, 0.25, 70)])
    return concat(t1, silence(0.06), t2)


def sfx_thud():
    """A cargo crate meeting the dock from a moderate height,
    with the planks complaining afterward."""
    boom = partials(0.5, [(55, 1.0, 7), (82, 0.6, 10), (130, 0.3, 16)],
                    attack=0.001)
    crack = noise_burst(0.08, 0.9, 50)
    rattle = partials(0.3, [(160, 0.25, 18), (245, 0.15, 22)])
    return concat(mix(boom, crack), rattle)


def sfx_plink():
    """The player piano demonstrating its range: two honest notes,
    then the third key that just... isn't."""
    p1 = partials(0.28, [(523, 0.8, 8), (1046, 0.3, 14), (1569, 0.15, 20)])
    p2 = partials(0.28, [(659, 0.8, 8), (1318, 0.3, 14), (1977, 0.15, 20)])
    ghost = mix(partials(0.18, [(140, 0.3, 30)]),
                noise_burst(0.03, 0.25, 150))   # felt thump, no string
    return concat(p1, silence(0.02), p2, silence(0.02), ghost)


def sfx_splash():
    """A magnet on a string meeting the harbor: plop, fizz, one drip."""
    plop = mix(partials(0.09, [(170, 1.0, 28), (88, 0.6, 22)]),
               noise_burst(0.03, 0.7, 120))
    fizz = noise_burst(0.4, 0.22, 8)
    drip = partials(0.06, [(880, 0.4, 60), (1320, 0.2, 80)])
    return concat(plop, fizz, silence(0.14), drip)


def sfx_creak():
    """A municipal dumpster lid exercising its right to complain,
    then giving up with a slam."""
    n = int(RATE * 0.55)
    groan = []
    for i in range(n):
        t = i / RATE
        f = 360 + 110 * math.sin(2 * math.pi * 2.6 * t) + 180 * t
        sq = 1.0 if math.sin(2 * math.pi * f * t) >= 0 else -1.0
        groan.append(0.2 * sq * (0.35 + 0.65 * math.sin(math.pi * i / n)))
    slam = mix(partials(0.14, [(92, 1.0, 24), (150, 0.5, 30)]),
               noise_burst(0.03, 0.6, 90))
    return concat(groan, silence(0.05), slam)


def sfx_boing():
    """A self-wound mainspring letting go: a deep twang dropping into
    a wobble that takes its time accepting the situation."""
    n = int(RATE * 0.85)
    out = []
    for i in range(n):
        t = i / RATE
        f = 340 * math.exp(-1.6 * t) + 70
        wob = 1.0 + 0.5 * math.exp(-2.0 * t) * math.sin(2 * math.pi * 11 * t)
        env = math.exp(-2.2 * t)
        out.append(0.7 * env * math.sin(2 * math.pi * f * t * wob))
    twang = noise_burst(0.02, 0.8, 200)
    return mix(concat(twang, []), out)


def sfx_clunk():
    """The S.S. Eventually's engine giving out -- the 'expensive' clunk.
    A heavy low seizure with one bright partial that snaps off early
    (the last fixable thing in the engine, dying mid-ring), settling
    into a dead boiler boom. No clean ring sustains: this is machinery
    losing an argument with physics."""
    # the seizure: a struck flywheel that should ring, but the ring is
    # killed fast by the decay -- 'expensive', not yet 'permanent'
    seize = partials(0.55, [(58, 1.0, 6), (87, 0.7, 9), (131, 0.45, 13),
                            (640, 0.4, 40), (910, 0.25, 55)], attack=0.001)
    grind = noise_burst(0.10, 0.85, 28)          # metal-on-metal scrape
    # a single failing piston knock partway through, off-beat
    knock = partials(0.12, [(140, 0.8, 26), (220, 0.4, 34)], attack=0.001)
    return concat(mix(seize, grind), silence(0.04),
                  mix(knock, noise_burst(0.04, 0.5, 60)))


def sfx_clunk_dead():
    """The same engine's SECOND clunk -- the 'PERMANENT' one. Heavier,
    lower, no bright partials at all (nothing left to fix), a longer
    dead tail that just... stops. A mainspring's last unwind into a
    boiler going cold. The comedy is the deadness."""
    # pure low mass, no upper partials -- the brightness that meant
    # 'fixable' is gone. Slow attack so it lands like a body, not a hit.
    boom = partials(0.85, [(46, 1.0, 4.5), (69, 0.6, 7), (104, 0.3, 11)],
                    attack=0.004)
    thud = noise_burst(0.14, 0.7, 18)            # muffled, low-energy
    # one final sub-drop: the mainspring slack going to zero
    n = int(RATE * 0.45)
    drop = []
    for i in range(n):
        t = i / RATE
        f = 95 * math.exp(-3.0 * t) + 38         # glides down to a floor
        env = math.exp(-3.5 * t)
        drop.append(0.55 * env * math.sin(2 * math.pi * f * t))
    return concat(mix(boom, thud), mix(drop))


def sfx_coded_knock():
    """The Rustlers' password knock, the 2-1-2 the whole game keeps
    echoing: CLANG-CLANG. CLANG. CLANG-CLANG. Five strikes on a metal
    door in two-one-two rhythm -- close within a group, a beat between
    groups -- so the motif is recognizable by ear, not just on screen.
    Bright inharmonic clang (it's struck plate, not a polite thud)."""
    def clang():
        return mix(partials(0.16, [(430, 0.9, 16), (970, 0.6, 22),
                                   (1640, 0.4, 30), (2510, 0.22, 40)],
                            attack=0.001),
                   noise_burst(0.02, 0.5, 110))
    intra, inter = silence(0.05), silence(0.20)    # within-group / between
    return concat(clang(), intra, clang(), inter,   # CLANG-CLANG.
                  clang(), inter,                    # CLANG.
                  clang(), intra, clang())           # CLANG-CLANG.


def sfx_manhole():
    """Midtown's manholes hissing 'in a higher register' (the entry line
    names it; nothing played). A faint pressurized hiss that fades in,
    holds, and tapers -- band-passed pseudo-noise sitting ABOVE the
    Shuffle's brass so it reads as escaping steam, not a rumble. Low
    amp (~0.16) and brief: it's a breath the street takes, not a leak.
    One-shot on room entry -- no loop, so it can't fight the music."""
    dur, n = 1.1, int(RATE * 1.1)
    seed, out = 0x3C, []
    prev = 0.0
    for i in range(n):
        t = i / RATE
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        r = (seed / 0x3FFFFFFF) - 1.0
        # one-pole high-pass: keep the airy top, drop the rumble so it
        # sits clear of the walking bass
        hp = r - prev
        prev = r
        # swell in over 0.18s, hold, taper from 0.7s -- a sighed breath
        env = min(1.0, t / 0.18) * (1.0 if t < 0.7
                                    else max(0.0, 1.0 - (t - 0.7) / 0.4))
        # a faint whistle riding the noise: the 'higher register'
        whistle = 0.18 * math.sin(2 * math.pi * 2300 * t)
        out.append((0.85 * hp + whistle) * env * 0.16)
    return out


def sfx_crowd():
    """The Grand Cog's packed house before the act -- 'forty bots, and
    not one of them came here to be impressed.' A low murmur bed: many
    overlapping slow vowel-ish swells (idling engines, fans, the room
    holding its breath) under a soft noise floor. Deliberately dull and
    dark so it sits UNDER the brass vamp, never on top of it. One-shot
    on entry; low amp (~0.18)."""
    dur, n = 2.0, int(RATE * 2.0)
    # a handful of detuned low formants, each wandering, summed: the
    # texture of a crowd murmuring without any one voice resolving
    voices = [(196, 0.7, 0.13), (233, 0.6, 0.19), (262, 0.55, 0.11),
              (311, 0.5, 0.23), (175, 0.6, 0.17)]
    out = []
    for i in range(n):
        t = i / RATE
        s = 0.0
        for f, a, rate in voices:
            # slow amplitude wander per voice (different rates = no beat)
            wob = 0.5 + 0.5 * math.sin(2 * math.pi * rate * t)
            s += a * wob * math.sin(2 * math.pi * f * t)
        # gentle swell in/out so the room arrives and settles
        env = min(1.0, t / 0.4) * (1.0 if t < 1.4
                                   else max(0.0, 1.0 - (t - 1.4) / 0.6))
        out.append(s * env)
    floor = noise_burst(dur, 0.10, 0.3)     # the HVAC of forty bots
    murmur = mix(out, floor)
    return [s * 0.18 for s in murmur]       # sit it under the vamp


def sfx_drip():
    """The Rustlers' alley, 'where the city keeps its rough drafts' --
    damp brick behind the tavern. A cluster of irregular water drips
    into a shallow puddle: each a short tuned plink with a noise plop,
    spaced unevenly (LCG) so it reads as a leak, not a metronome. The
    Back-Alley Blues is the sparsest score in the game, so a few drips
    sit in its silences. One-shot on entry; low amp."""
    def drip(f):
        plink = partials(0.07, [(f, 0.7, 55), (f * 1.5, 0.3, 70)])
        plop = noise_burst(0.015, 0.25, 180)
        return mix(plink, plop)
    # uneven spacing + pitch from the LCG: a leak keeping no time
    seed = 0x6D
    parts, pitches = [], (1150, 1480, 980, 1320)
    for k in range(4):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        gap = 0.16 + (seed >> 7) % 220 / 1000.0    # 0.16..0.38s
        parts.append(drip(pitches[k]))
        if k < 3:
            parts.append(silence(gap))
    return [s * 0.5 for s in concat(*parts)]        # keep it faint


def sfx_applause():
    """A full house coming apart: dense little claps with a swell,
    deterministic like everything else in this town."""
    dur = 2.2
    n = int(RATE * dur)
    seed, out = 0x77, [0.0] * n
    i = 0
    while i < n:
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        gap = 90 + (seed >> 8) % 700           # next clap, in samples
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        amp = 0.25 + ((seed >> 9) % 100) / 220.0
        t = i / RATE
        swell = min(1.0, t / 0.5) * (1.0 if t < 1.5 else
                                     max(0.0, 1.0 - (t - 1.5) / 0.7))
        clap_len = int(RATE * 0.025)
        s2 = seed
        for j in range(clap_len):
            if i + j >= n:
                break
            s2 = (s2 * 1103515245 + 12345) & 0x7FFFFFFF
            r = (s2 / 0x3FFFFFFF) - 1.0
            out[i + j] += amp * swell * r * math.exp(-140 * j / RATE)
        i += gap
    peak = max(abs(s) for s in out)
    return [s * 0.8 / peak for s in out]


def sfx_steam():
    """Pressure-relief hiss: a kettle conceding a point (Scene 08, R1
    win + flavor vents). Filtered noise + a thin resonance at the relief
    valve's pitch."""
    return mix(noise_burst(0.55, 0.75, 7),
               partials(0.55, [(3800, 0.15, 10)]))


def sfx_stamp():
    """The VOID stamp: a felt-padded thunk + a click (Scene 08)."""
    return mix(partials(0.09, [(150, 0.9, 40), (90, 0.7, 30)]),
               noise_burst(0.03, 0.6, 90))


def sfx_creak9():
    """A door surrendering degree by degree -- nine short ticks with
    shrinking silences between them (0.14s -> 0.04s, an accelerando), the
    81-degree opening (Scene 08)."""
    tick = lambda: partials(0.05, [(620, 0.5, 50), (1240, 0.3, 60)])
    gaps = [0.14, 0.125, 0.11, 0.095, 0.08, 0.065, 0.05, 0.04]
    parts = []
    for i in range(9):
        parts.append(tick())
        if i < 8:
            parts.append(silence(gaps[i]))
    return concat(*parts)


def sfx_sag():
    """The Round 3 brownout: a two-block glide from A down to A-flat (the
    half-step made audible), overall amplitude sagging then half-
    recovering (Scene 08)."""
    a = partials(0.6, [(220, 0.5, 1.2)])      # A
    ab = partials(0.7, [(207, 0.5, 1.0)])     # A-flat, a half-step under
    glide = concat(a, ab)
    # amplitude envelope: sag through the dip, half-recover at the tail
    n = len(glide)
    out = []
    for i, s in enumerate(glide):
        t = i / n
        if t < 0.5:
            env = 1.0 - 0.7 * (t / 0.5)        # sag to 0.3
        else:
            env = 0.3 + 0.25 * ((t - 0.5) / 0.5)  # half-recover to 0.55
        out.append(s * env)
    peak = max(1e-9, max(abs(s) for s in out))
    return [s * 0.8 / peak for s in out]


def sfx_whistle():
    """A strained boiler whistle: two close partials beating (Scene 08,
    Piston's bluster peaks)."""
    return partials(0.4, [(932, 0.6, 4), (988, 0.5, 4)])


def sfx_governor():
    """The clockwork governor on the gate post (Scene 10): a regular train
    of short high metallic escapement ticks over a low whirring undertone --
    a speed-regulator turning. The gate puzzle's timing source made audible
    (it 'only answers the hum')."""
    whir = partials(0.9, [(180, 0.4, 3), (360, 0.25, 4)])
    tick = lambda: partials(0.03, [(2600, 0.6, 80), (3900, 0.3, 100)])
    gap = silence(0.09)                       # ~120ms tick interval
    train_parts = []
    for i in range(7):                        # ~0.9s of ticks
        train_parts.append(tick())
        if i < 6:
            train_parts.append(gap)
    train = concat(*train_parts)
    return mix(whir, train)


def sfx_winddown():
    """Old Crank pulling his own key and winding down (Scene 10, the cost):
    a descending square sweep ~600->80Hz with falling amplitude (the reverse
    of sfx_pickup's hopeful rising chirp), plus a DECELERATING tick train
    that thins to silence -- a mainspring giving up the last of its turn."""
    n = int(RATE * 1.3)
    sweep = []
    for i in range(n):
        t = i / RATE
        f = 600 - (600 - 80) * (t / 1.3)
        phase = 2 * math.pi * (600 * t - (600 - 80) * t * t / (2 * 1.3))
        square = 1.0 if math.sin(phase) >= 0 else -1.0
        sweep.append(0.4 * square * (1.0 - t / 1.35))
    tick = lambda: partials(0.025, [(1700, 0.5, 90), (2550, 0.25, 110)])
    # decelerating gaps: 90ms growing toward 260ms, then nothing
    gaps = [0.09, 0.115, 0.145, 0.18, 0.22, 0.26]
    train_parts = []
    for i, gp in enumerate(gaps):
        train_parts.append(tick())
        train_parts.append(silence(gp))
    train = concat(*train_parts)
    return mix(sweep, train)


def sfx_humlift():
    """The dry run catching (Scene 10, two keys turned): a swelling chord
    rising a semitone -- two partial stacks a half-step apart, the upper
    fading in over ~0.7s, a soft harmonic shimmer on top. Short, hopeful,
    then cut (it stalls). Db -> D, the N-A5 detuning reversed for one beat."""
    # the flat chord already sounding (Db) -- steady
    flat = partials(0.9, [(277, 0.45, 1.0), (415, 0.3, 1.2), (554, 0.2, 1.4)])
    # the lifted chord (D, a semitone up) fading IN over 0.7s
    n = len(flat)
    lifted = []
    for i in range(n):
        t = i / RATE
        env_in = min(1.0, t / 0.7)
        s = (0.45 * math.sin(2 * math.pi * 294 * t)
             + 0.3 * math.sin(2 * math.pi * 440 * t)
             + 0.2 * math.sin(2 * math.pi * 587 * t))
        decay = math.exp(-0.8 * t)
        lifted.append(s * env_in * decay)
    shimmer = partials(0.9, [(1175, 0.12, 3), (1760, 0.08, 4)], attack=0.4)
    return mix(flat, lifted, shimmer)


def sfx_keyturn():
    """A heavy brass key seating and turning in a big lock (Scene 10): a
    lower, slower ratchet variant -- a few deep brass clicks ending in a
    detent clunk. Bigger than sfx_ratchet; it's the Dynamo's collar."""
    clicks = []
    for f in (240, 360, 520):
        clicks.append(partials(0.07, [(f, 0.7, 30), (f * 1.8, 0.3, 45)]))
        clicks.append(silence(0.1))
    clunk = mix(partials(0.16, [(120, 0.9, 22), (200, 0.5, 30)]),
                noise_burst(0.03, 0.5, 90))
    return concat(*clicks, silence(0.04), clunk)


EFFECTS = {
    "whack": sfx_whack,
    "bolt_drop": sfx_bolt_drop,
    "pickup": sfx_pickup,
    "knock": sfx_knock,
    "foghorn": sfx_foghorn,
    "ratchet": sfx_ratchet,
    "dart": sfx_dart,
    "sizzle": sfx_sizzle,
    "clink": sfx_clink,
    "thud": sfx_thud,
    "plink": sfx_plink,
    "splash": sfx_splash,
    "creak": sfx_creak,
    "boing": sfx_boing,
    "clunk": sfx_clunk,
    "clunk_dead": sfx_clunk_dead,
    "coded_knock": sfx_coded_knock,
    "applause": sfx_applause,
    "steam": sfx_steam,
    "manhole": sfx_manhole,
    "crowd": sfx_crowd,
    "drip": sfx_drip,
    "stamp": sfx_stamp,
    "creak9": sfx_creak9,
    "sag": sfx_sag,
    "whistle": sfx_whistle,
    "governor": sfx_governor,
    "winddown": sfx_winddown,
    "humlift": sfx_humlift,
    "keyturn": sfx_keyturn,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in EFFECTS.items():
        path = os.path.join(OUT, f"{name}.voc")
        samples = fn()
        write_voc(path, samples)
        print(f"{path}  ({len(samples)/RATE:.2f}s)")


if __name__ == "__main__":
    main()
