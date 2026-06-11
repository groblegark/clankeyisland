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


EFFECTS = {
    "whack": sfx_whack,
    "bolt_drop": sfx_bolt_drop,
    "pickup": sfx_pickup,
    "knock": sfx_knock,
    "foghorn": sfx_foghorn,
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
