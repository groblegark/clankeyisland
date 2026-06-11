#!/usr/bin/env python3
"""The walk-through-er: performs Clanker City Chronicles in a browser,
asserts it is playable, and (in perform mode) records the take.

See docs/WALKTHROUGHER.md. The screenplay (YAML) says what to do and what
to expect; the stage map (generated from tools/genassets.py) says where
everything is; the transcript (extracted from the .scc sources) says what
every line of dialog is, so the timeline can pair each observed talk
segment with its exact text — that pairing becomes the dub sheet.

Modes:
  validate  fast: skip cutscenes, no recording, strict assertions, exit 0/1
  perform   cinematic: cutscenes play, beats breathe, video + timeline +
            dub sheet written to walkthrough/out/<take>/

Usage:
  python3 walkthrough/driver/walkthrough.py --serve \
      walkthrough/screenplay/01-docks.play.yaml
  python3 walkthrough/driver/walkthrough.py --mode perform --serve ...
"""

import argparse
import http.server
import json
import os
import socket
import socketserver
import sys
import tempfile
import threading
import time
from io import BytesIO

import yaml
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GAME_W, GAME_H = 320, 200
VIEWPORT = {"width": 1280, "height": 720}
TOL = 16          # per-channel color tolerance for palette probes
POLL = 0.18       # seconds between oracle polls

# Console errors that are expected and harmless (the DOTT masquerade
# warning, browser policy noise). Anything else at error level fails.
CONSOLE_ALLOW = (
    "favicon", "Web MIDI", "No voice is available",
    "Engine_SCUMM_create", "unknown", "ScummVM team", "MD5",
    "language, etc", "SCUMM gameid", "AudioContext",
)

# screenplay verb -> .scc case label (for transcript pairing)
VERB_CASE = {
    "Examine": "LookAt", "Pick up": "PickUp", "Talk to": "TalkTo",
    "Use": "Use", "Open": "Open", "Give": "Give", "Smell": "Smell",
    "Move": "Move",
}


def near(px, target):
    return (abs(px[0] - target[0]) <= TOL and abs(px[1] - target[1]) <= TOL
            and abs(px[2] - target[2]) <= TOL)


class Stage:
    def __init__(self, path):
        with open(path) as f:
            self.data = json.load(f)
        self.probes = {k: [tuple(c) for c in v]
                       for k, v in self.data["probes"].items()}

    def resolve(self, ref):
        """'neon sign' | 'inventory.slot0' | [x, y] -> game coords."""
        if isinstance(ref, (list, tuple)):
            return tuple(ref)
        if ref.startswith("inventory.slot"):
            return tuple(self.data["inventory"]["slots"][int(ref[14:])])
        if ref in self.data["objects"]:
            return tuple(self.data["objects"][ref]["hotspot"])
        if ref in self.data["walk_targets"]:
            return tuple(self.data["walk_targets"][ref])
        raise KeyError(f"unknown stage ref: {ref}")


class Oracle:
    """Reads the screen. All checks happen on a 320x200 nearest-neighbor
    downsample of the game area, so palette colors survive scaling."""

    def __init__(self, page, stage):
        self.page = page
        self.stage = stage
        self.rect = None          # game area in page pixels (x, y, w, h)
        self.frozen = False       # set once the room is detected at rect

    def _frame(self):
        img = Image.open(BytesIO(self.page.screenshot())).convert("RGB")
        if not self.frozen:
            # keep re-deriving until boot confirms the room renders here
            box = self._game_bbox(img)
            if box is None:
                return None
            self.rect = box
        x, y, w, h = self.rect
        return img.crop((x, y, x + w, y + h)).resize(
            (GAME_W, GAME_H), Image.NEAREST)

    @staticmethod
    def _game_bbox(img):
        """Game area inside the pillarbox bars.

        SDL letterboxes horizontally but fills the viewport height, so
        the rect is (x-extent of non-black columns, full height). Only
        the x-extent is detected — the y-extent shrinks whenever the
        verb panel is hidden (cutscenes render the room area only), so
        it cannot be trusted. The pre-boot logo canvas fills the whole
        viewport and is rejected by the aspect bound.
        """
        small = img.resize((img.width // 4, img.height // 4), Image.NEAREST)
        px = small.load()
        xs = [xx for xx in range(small.width)
              if any(sum(px[xx, yy]) > 24 for yy in range(small.height))]
        if not xs:
            return None
        x0, w = min(xs) * 4, (max(xs) + 1 - min(xs)) * 4
        if w < 100 or not 1.1 < w / img.height < 1.6:
            return None
        return (x0, 0, w, img.height)

    def probe(self, frame, point, probe_name, radius=2):
        colors = self.stage.probes[probe_name]
        px = frame.load()
        x0, y0 = point
        for yy in range(max(0, y0 - radius), min(GAME_H, y0 + radius + 1)):
            for xx in range(max(0, x0 - radius), min(GAME_W, x0 + radius + 1)):
                p = px[xx, yy]
                if any(near(p, c) for c in colors):
                    return True
        return False

    def talk_mask(self, frame):
        """Set of positions showing talk-colored text (room area only)."""
        colors = self.stage.probes["talk"] + self.stage.probes["talk-2"] \
            + self.stage.probes["white"]
        px = frame.load()
        mask = []
        for yy in range(0, 104, 2):
            for xx in range(0, GAME_W, 2):
                p = px[xx, yy]
                if any(near(p, c) for c in colors):
                    mask.append((xx, yy))
        return frozenset(mask)

    def room_ready(self, frame):
        return (self.probe(frame, (60, 130), "dock-wood", radius=4)
                and self.probe(frame, (250, 130), "dock-wood", radius=4))


class Take:
    """One run: timeline, console log, failure evidence."""

    def __init__(self, out_dir):
        self.out = out_dir
        os.makedirs(out_dir, exist_ok=True)
        self.t0 = time.monotonic()
        self.events = []
        self.console = []
        self.failures = []

    def t(self):
        return round(time.monotonic() - self.t0, 2)

    def log(self, type_, **kw):
        self.events.append({"t": self.t(), "type": type_, **kw})

    def fail(self, shot, why, frame=None):
        self.failures.append({"shot": shot, "why": why, "t": self.t()})
        self.log("failure", shot=shot, why=why)
        print(f"  FAIL [{shot}] {why}", file=sys.stderr)
        if frame is not None:
            fdir = os.path.join(self.out, "failures")
            os.makedirs(fdir, exist_ok=True)
            frame.resize((GAME_W * 3, GAME_H * 3), Image.NEAREST).save(
                os.path.join(fdir, f"{shot}.png"))

    def save(self):
        with open(os.path.join(self.out, "timeline.json"), "w") as f:
            json.dump({"events": self.events, "failures": self.failures},
                      f, indent=1)
        with open(os.path.join(self.out, "console.log"), "w") as f:
            f.writelines(f"[{c['type']}] {c['text']}\n" for c in self.console)


class Performer:
    def __init__(self, page, stage, transcript, take, mode):
        self.page = page
        self.stage = stage
        self.transcript = transcript
        self.take = take
        self.mode = mode
        self.oracle = Oracle(page, stage)

    # ---------------------------------------------------------- helpers

    def click_game(self, point):
        x, y = point
        rx, ry, rw, rh = self.oracle.rect
        self.page.mouse.click(rx + (x + 0.5) * rw / GAME_W,
                              ry + (y + 0.5) * rh / GAME_H)

    def watch(self, until, timeout, lines=None, settle=0.0):
        """Poll the oracle; track talk segments; return (ok, frame).

        until(frame) -> bool decides success; success must then hold
        through `settle` seconds of continued quiet (no talking).
        """
        deadline = time.monotonic() + timeout
        cur_sig, seg_count = None, 0
        ok_since = None
        frame = None
        while time.monotonic() < deadline:
            frame = self.oracle._frame()
            if frame is None:
                time.sleep(POLL)
                continue
            mask = self.oracle.talk_mask(frame)
            talking = len(mask) >= 6
            sig = mask if talking else None
            if talking and sig != cur_sig:
                if cur_sig is not None:
                    self.take.log("line_end", index=seg_count - 1)
                text = None
                if lines and seg_count < len(lines):
                    text = lines[seg_count]
                self.take.log("line_start", index=seg_count, text=text)
                seg_count += 1
            elif not talking and cur_sig is not None:
                self.take.log("line_end", index=seg_count - 1)
            cur_sig = sig
            if until(frame) and not talking:
                if ok_since is None:
                    ok_since = time.monotonic()
                if time.monotonic() - ok_since >= settle:
                    return True, frame
            else:
                ok_since = None
            time.sleep(POLL)
        return False, frame

    def expectations(self, expects, segments_seen):
        """Build an until() that checks all pixel expectations."""
        pixel_checks = []
        wants_talking = False
        for e in expects or []:
            if e == "talking":
                wants_talking = True
            elif isinstance(e, dict) and "pixel" in e:
                p = e["pixel"]
                pixel_checks.append((self.stage.resolve(p["at"]), p["is"]))

        def until(frame):
            if wants_talking and not segments_seen():
                return False
            return all(self.oracle.probe(frame, pt, probe)
                       for pt, probe in pixel_checks)
        return until

    # ------------------------------------------------------------ shots

    def boot(self, url):
        self.take.log("boot", url=url)
        for attempt in range(2):
            self.page.goto(url)
            # no screenshots while the wasm runtime spins up — early
            # captures can race SDL's WebGL context creation
            try:
                self.page.wait_for_function(
                    "() => window.Module && Module.calledRun",
                    timeout=60000)
            except Exception:
                pass
            time.sleep(1.0)
            ok, frame = self.watch(self.oracle.room_ready, timeout=45)
            if ok:
                self.oracle.frozen = True
                self.take.log("room_ready", attempt=attempt,
                              rect=list(self.oracle.rect))
                return True
            self.take.log("boot_retry", attempt=attempt)
            self.oracle.rect, self.oracle.frozen = None, False
        self.take.fail("boot", "room never faded in", frame)
        return False

    def run_shot(self, shot):
        name = shot["name"]
        only = shot.get("only")
        if only and only != self.mode:
            return True
        self.take.log("shot_start", shot=name)
        print(f"  [{name}]")

        lines = self.shot_lines(shot)
        seg_base = self.count_segments()

        if "do" in shot:
            d = shot["do"]
            if "verb" in d:
                self.click_game(tuple(self.stage.data["verbs"][d["verb"]]))
                time.sleep(0.4)
                self.click_game(self.stage.resolve(d["object"]))
            elif "walk" in d:
                self.click_game(self.stage.resolve(d["walk"]))
            elif "press" in d:
                self.page.keyboard.press(d["press"])

        def segments_seen():
            return self.count_segments() > seg_base

        if shot.get("cutscene") and self.mode == "validate":
            # let the first line land (proves the cutscene talks), then
            # skip the rest via the cutscene override
            self.watch(lambda f: segments_seen(), timeout=30, lines=lines)
            self.page.keyboard.press("Escape")

        until = self.expectations(shot.get("expect"), segments_seen)
        settle = 1.2 if self.mode == "perform" else 0.6
        ok, frame = self.watch(until, timeout=shot.get("timeout", 40),
                               lines=lines, settle=settle)
        if not ok:
            self.take.fail(name, "expectations not met before timeout", frame)
        if self.mode == "perform":
            time.sleep(shot.get("hold", 1.0))
        self.take.log("shot_end", shot=name, ok=ok)
        return ok

    def shot_lines(self, shot):
        if shot.get("cutscene"):
            return self.transcript["cutscenes"].get(shot["cutscene"], [])
        d = shot.get("do", {})
        if "verb" in d:
            case = VERB_CASE.get(d["verb"], d["verb"])
            return (self.transcript["objects"]
                    .get(d["object"], {}).get(case, []))
        return []

    def count_segments(self):
        return sum(1 for e in self.take.events if e["type"] == "line_start")


# ------------------------------------------------------------- dub sheet

def write_dub_sheet(take, screenplay):
    rows = []
    shot = None
    for e in take.events:
        if e["type"] == "shot_start":
            shot = e["shot"]
            rows.append((e["t"], "scene", shot, ""))
        elif e["type"] == "line_start":
            rows.append((e["t"], "line", shot or "",
                         e.get("text") or "(unscripted line)"))
    path = os.path.join(take.out, "dubsheet.md")
    with open(path, "w") as f:
        f.write(f"# Dub sheet — {screenplay.get('title', 'take')}\n\n")
        f.write("Fill the cue column to arrange music/foley/VO "
                "(see the Suno dub plan in docs/WALKTHROUGHER.md).\n\n")
        f.write("| time | kind | shot | text | cue |\n")
        f.write("|------|------|------|------|-----|\n")
        for t, kind, shot_, text in rows:
            mm, ss = divmod(t, 60)
            text = text.replace("|", "\\|")
            f.write(f"| {int(mm):02d}:{ss:05.2f} | {kind} | {shot_} "
                    f"| {text} | |\n")
    print(f"  dub sheet: {path}")


# ------------------------------------------------------------ local serve

def serve_dist(site_path="/clankeyisland"):
    """Serve web/dist under site_path on a free port; return base URL."""
    srv_root = tempfile.mkdtemp(prefix="clankey-serve-")
    os.symlink(os.path.join(ROOT, "web", "dist"),
               srv_root + site_path)
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=srv_root, **kw)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", port), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{port}{site_path}/"


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("screenplay")
    ap.add_argument("--mode", choices=["validate", "perform"],
                    default="validate")
    ap.add_argument("--url", help="site base URL (default: --serve)")
    ap.add_argument("--serve", action="store_true",
                    help="serve web/dist locally")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    with open(args.screenplay) as f:
        screenplay = yaml.safe_load(f)
    stage = Stage(os.path.join(ROOT, "walkthrough", "stage",
                               screenplay["stage"]))
    with open(os.path.join(ROOT, "walkthrough", "stage",
                           screenplay["transcript"])) as f:
        transcript = json.load(f)

    url = args.url or (serve_dist() if args.serve or not args.url else None)
    target = url + "#" + screenplay.get("game", "chronicles")

    take_name = time.strftime("%Y%m%d-%H%M%S") + "-" + args.mode
    out_dir = args.out or os.path.join(ROOT, "walkthrough", "out", take_name)
    take = Take(out_dir)

    print(f"{args.mode} take -> {out_dir}")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx_kw = {"viewport": VIEWPORT}
        if args.mode == "perform":
            ctx_kw.update(record_video_dir=out_dir,
                          record_video_size=VIEWPORT)
        ctx = browser.new_context(**ctx_kw)
        page = ctx.new_page()
        take.t0 = time.monotonic()   # video recording starts with the page;
        page.on("console", lambda m: take.console.append(  # align clocks
            {"type": m.type, "text": m.text}))

        perf = Performer(page, stage, transcript, take, args.mode)
        ok = perf.boot(target)
        if ok:
            for shot in screenplay["shots"]:
                if not perf.run_shot(shot) and args.mode == "validate":
                    pass  # keep going: report all failures in one run
        ctx.close()   # flushes the video file
        browser.close()

    # console errors beyond the allowlist are failures
    for c in take.console:
        if (c["type"] == "error" and c["text"].strip()
                and not any(a in c["text"] for a in CONSOLE_ALLOW)):
            take.failures.append({"shot": "(console)", "why": c["text"]})

    take.save()
    if args.mode == "perform":
        for f in os.listdir(out_dir):
            if f.endswith(".webm"):
                os.rename(os.path.join(out_dir, f),
                          os.path.join(out_dir, "take.webm"))
        write_dub_sheet(take, screenplay)

    if take.failures:
        print(f"\nFAILED: {len(take.failures)} problem(s); "
              f"evidence in {out_dir}", file=sys.stderr)
        sys.exit(1)
    print(f"\nPASS: {sum(1 for e in take.events if e['type'] == 'shot_end')} "
          f"shots, {sum(1 for e in take.events if e['type'] == 'line_start')} "
          f"dialog lines observed")


if __name__ == "__main__":
    main()
