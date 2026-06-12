#!/usr/bin/env python3
"""Extract the spoken script from .scc sources for the walk-through-er.

The game is authored as text, so the full transcript is already in the
repo — this just reshapes it: for every object verb handler (and the
room entry cutscene) collect the egoSay() lines in source order.

Output (JSON):
  {
    "cutscenes": {"entry": ["line", ...]},
    "objects":   {"neon sign": {"Use": ["line", ...], ...}, ...}
  }

Caveat: handlers with first-visit/repeat branches (unless(flag){...})
list ALL their lines in source order. Our handlers put the first-visit
lines first, and the walkthrougher pairs observed talk segments with
lines from the front of the list, so repeat-visit lines simply never
get matched on a first-visit playthrough.

Usage: transcript.py <out.json> <file.scc> [more.scc ...]
"""

import json
import re
import sys

EGOSAY = re.compile(r'egoSay\(\s*"((?:[^"\\]|\\.)*)"')
OBJECT = re.compile(r'^\s*object\s+(\w+)\s*\{', re.M)
NAME = re.compile(r'name\s*=\s*"([^"]*)"')
SCRIPT = re.compile(r'^\s*(?:local\s+)?script\s+(\w+)\s*\(', re.M)
CASE = re.compile(r'^\s*case\s+(\w+)\s*:', re.M)


def block(src, open_brace):
    """Return (body, end) for the {...} block whose '{' is at open_brace."""
    depth = 0
    for i in range(open_brace, len(src)):
        if src[i] == '{':
            depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                return src[open_brace + 1:i], i
    raise ValueError("unbalanced braces")


def verb_lines(body):
    """Split a verb() body on case labels; adjacent labels share lines."""
    out = {}
    matches = list(CASE.finditer(body))
    i = 0
    while i < len(matches):
        labels = [matches[i].group(1)]
        # absorb immediately-following labels (case A: case B: shared body)
        while (i + 1 < len(matches)
               and not body[matches[i].end():matches[i + 1].start()].strip()):
            i += 1
            labels.append(matches[i].group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        lines = EGOSAY.findall(body[matches[i].end():end])
        if lines:
            for label in labels:
                out[label] = lines
        i += 1
    return out


ROOM = re.compile(r'^\s*room\s+(\w+)\s*\{', re.M)


def extract(src, result):
    room_m = ROOM.search(src)
    room = room_m.group(1) if room_m else "?"
    for m in OBJECT.finditer(src):
        body, _ = block(src, m.end() - 1)
        name_m = NAME.search(body)
        name = name_m.group(1) if name_m else m.group(1)
        vm = re.search(r'verb\s*\([^)]*\)\s*\{', body)
        if not vm:
            continue
        vbody, _ = block(body, vm.end() - 1)
        lines = verb_lines(vbody)
        if lines:
            result["objects"].setdefault(name, {}).update(lines)
    for m in SCRIPT.finditer(src):
        brace = src.find('{', m.end())
        if brace < 0:
            continue
        body, _ = block(src, brace)
        lines = EGOSAY.findall(body)
        # only scripts that actually talk (entry cutscenes etc.);
        # keyed by room to keep the two rooms' entry scripts apart
        if lines and m.group(1) not in result["objects"]:
            result["cutscenes"][f"{room}.{m.group(1)}"] = lines


def main():
    out_path, srcs = sys.argv[1], sys.argv[2:]
    result = {"cutscenes": {}, "objects": {}}
    for path in srcs:
        with open(path) as f:
            extract(f.read(), result)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1)
    n = sum(len(v) for o in result["objects"].values() for v in o.values())
    n += sum(len(v) for v in result["cutscenes"].values())
    print(f"{out_path}: {n} lines from {len(result['objects'])} objects, "
          f"{len(result['cutscenes'])} cutscenes")


if __name__ == "__main__":
    main()
