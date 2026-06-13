#!/usr/bin/env python3
"""Inject in-game PCM voice clips into .scc room sources.

This is the engine-native replacement for the walkthrough dub's
screen-scrape voice pairing (which drifted whenever a "..." beat
painted too few talk pixels to detect). Here the engine itself ties
each clip to its say line — DOTT's talkie mechanism — so audio and
text cannot desynchronize: ScummVM holds the line on screen exactly
as long as the clip plays (sound-driven talk timing).

For each egoSay("...") string in a room source:
  1. render a robot-voiced clip with the same piper+FX chain and
     content-hash cache as walkthrough/post/dub.py,
  2. resample to 8-bit unsigned mono VOC (the only format
     scc_roobj.c:273 accepts) at VOICE_RATE,
  3. declare it as a room `voice` resource and prefix the string with
     %V{sym}; sld then packs every clip into tentacle.sou and patches
     the say opcode with the clip's offset (scc_ld.c:634).

Lines with no letters ("...", "") stay silent beats on char-count
timing. Strings already carrying a %V escape are left alone.

Usage: genvoice.py -o build/docks.voiced.scc --voices build/voices docks.scc
"""

import argparse
import hashlib
import os
import re
import struct
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "walkthrough", "post"))
import dub  # speak(): cached piper + robot FX render

# 11025 Hz halves the .sou payload vs 22050 and suits the robot FX;
# VOC sr_code can't hit 11025 exactly (1e6/(256-165)) but the ~0.8%
# pitch shift is inaudible under the FX chain.
VOICE_RATE = 11025

SAY = re.compile(
    r'((?:egoSay\(\s*|actorSay\(\s*(\w+)\s*,\s*)")'
    r'((?:[^"\\]|\\.)*)("\s*)(?=[,)])')

# The NPC cast (NPC-DIALOG.md item 6): per-speaker piper voice + FX.
# Cheap tinny NPC voices are sanctioned characterization
# (NARRATION.md). Sprocket stays lessac + ROBOT_FX (dub.py defaults).
NPC_FX_BASE = ("silenceremove=start_periods=1:start_threshold=-45dB,"
               "areverse,silenceremove=start_periods=1:"
               "start_threshold=-45dB,areverse,"
               "loudnorm=I=-17:TP=-1.5,"
               "aformat=sample_rates=48000:channel_layouts=mono")
CAST = {
    # actor symbol -> (piper voice, fx chain)
    "gusket_a": ("en_US-ryan-high",
                 "asetrate=48000*0.82,aresample=48000,atempo=1.22,"
                 "acrusher=bits=8:mode=log:mix=0.35," + NPC_FX_BASE),
    "voltina_a": ("en_US-kristin-medium",
                  "aecho=0.7:0.5:120:0.3,chorus=0.6:0.9:55:0.4:0.25:2,"
                  "lowpass=f=5000," + NPC_FX_BASE),
    "emcee_a": ("en_GB-cori-high",
                "aecho=0.7:0.6:60:0.25,highpass=f=200," + NPC_FX_BASE),
    "rivet_a": ("en_US-bryce-medium",
                "atempo=1.12,acrusher=bits=9:mode=log:mix=0.25,"
                + NPC_FX_BASE),
    "extra_a": ("en_US-joe-medium",
                "highpass=f=300,lowpass=f=3400," + NPC_FX_BASE),
}
ROOM = re.compile(r'^room\s+\w+\s*\{', re.M)


def unescape(s):
    return s.replace('\\"', '"').replace("\\\\", "\\")


def write_voc(path, u8data):
    """Wrap raw 8-bit unsigned samples as a pack-0 type-1 VOC."""
    version = 0x010A
    checksum = (~version + 0x1234) & 0xFFFF
    hdr = b"Creative Voice File\x1a" + struct.pack("<HHH", 26, version, checksum)
    sr_code = 256 - (1000000 // VOICE_RATE)
    blk_len = len(u8data) + 2
    block = bytes([1, blk_len & 0xFF, (blk_len >> 8) & 0xFF,
                   (blk_len >> 16) & 0xFF, sr_code, 0]) + u8data
    with open(path, "wb") as f:
        f.write(hdr + block + b"\x00")


def render_voc(text, voices_dir, sym, actor=None):
    out = os.path.join(voices_dir, sym + ".voc")
    if os.path.exists(out):
        return
    voice, fx_chain = CAST.get(actor, (None, None))
    fx = dub.speak(text, voice=voice, fx_chain=fx_chain)
    raw = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", fx,
         "-ar", str(VOICE_RATE), "-ac", "1", "-f", "u8", "pipe:1"],
        capture_output=True, check=True).stdout
    write_voc(out, raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--voices", default=None,
                    help="VOC output dir (default: <outdir>/voices)")
    ap.add_argument("source")
    args = ap.parse_args()

    voices_dir = args.voices or os.path.join(
        os.path.dirname(args.output) or ".", "voices")
    os.makedirs(voices_dir, exist_ok=True)

    src = open(args.source).read()
    # adjacent-literal concatenation after an egoSay string would hide
    # part of the line from the renderer — refuse rather than mis-voice
    for m in re.finditer(
            r'(?:ego|actor)Say\([^)"]*"(?:[^"\\]|\\.)*"\s*"', src):
        line = src[:m.start()].count("\n") + 1
        sys.exit(f"{args.source}:{line}: adjacent string literals in "
                 "egoSay not supported by genvoice.py — join them first")

    syms = {}  # sym -> voc relpath (decl order = first appearance)

    def voice_sub(m):
        actor, text = m.group(2), m.group(3)
        if not re.search(r"[A-Za-z]", text) or "%V{" in text:
            return m.group(0)
        if actor == "0xFF":
            return m.group(0)
        # speaker is part of the identity: the same words in another
        # mouth are another clip
        key = f"{actor or 'ego'}|{text}"
        sym = "vx_" + hashlib.sha1(key.encode()).hexdigest()[:10]
        if sym not in syms:
            render_voc(unescape(text), voices_dir, sym, actor=actor)
            syms[sym] = f"voices/{sym}.voc"
        return f'{m.group(1)}%V{{{sym}}}{text}{m.group(4)}'

    out = SAY.sub(voice_sub, src)

    if syms:
        room = ROOM.search(out)
        if not room:
            sys.exit(f"{args.source}: has say lines but no room block")
        # room params (image=, boxd=, trans=) must precede body entries
        # (scc_parse.y:497) — inject before the first decl/script/object
        entry = re.search(
            r"^\s*(?:sound|cost|voice|chset|object|verb|(?:local\s+)?script)\b",
            out[room.end():], re.M)
        if not entry:
            sys.exit(f"{args.source}: no room body entry to anchor on")
        at = room.end() + entry.start()
        decls = "\n    // generated by tools/genvoice.py — in-game voice\n"
        decls += "".join(f'    voice {s} = {{ "{p}" }};\n'
                         for s, p in syms.items())
        out = out[:at] + decls + out[at:]

    with open(args.output, "w") as f:
        f.write(out)
    print(f"{os.path.basename(args.source)}: {len(syms)} voiced lines")


if __name__ == "__main__":
    main()
