#!/usr/bin/env python3
"""Generate all Clankey Island art assets as indexed BMPs + walkbox files.

Everything shares ONE master 256-color palette (SCUMM v6 rooms own the
palette; costumes map a 32-slot window of it, slots 224-255).

Outputs into assets/generated/:
  rooms/docks.bmp + docks.box     320x144 background + walkboxes
  rooms/docks_sign_on.bmp etc.    object state images (cropped from scene)
  verbs/verb_background.bmp       320x56 UI panel
  sprocket/frames/*.bmp           costume frames (indices 0-31)
  inventory/*.bmp                 inventory icons
Also writes preview.png (full scene mockup) for eyeballing.
"""

import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boxfile import Box, write_box_file

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "generated")

W, H = 320, 144          # room size (verb panel lives below at y>=144)
PANEL_H = 56

# ---------------------------------------------------------------- palette

def ramp(c1, c2, n):
    return [tuple(int(c1[k] + (c2[k] - c1[k]) * i / (n - 1)) for k in range(3))
            for i in range(n)]

PAL = [(0, 0, 0)] * 256
def setpal(idx, colors):
    for i, c in enumerate(colors):
        PAL[idx + i] = c

# 0 = black / transparent-for-objects
PAL[0] = (0, 0, 0)
PAL[1] = (10, 10, 14)                                   # near-black
setpal(2,  ramp((24, 26, 34), (200, 205, 215), 14))     # 2-15  steel grays
setpal(16, ramp((58, 24, 12), (255, 140, 40), 12))      # 16-27 rust/orange
setpal(28, ramp((8, 50, 54), (90, 245, 230), 12))       # 28-39 teal/neon
setpal(40, ramp((70, 50, 8), (255, 240, 150), 12))      # 40-51 sodium yellow
setpal(52, ramp((6, 8, 26), (66, 60, 110), 12))         # 52-63 night sky
setpal(64, ramp((40, 26, 14), (180, 130, 80), 12))      # 64-75 wood browns
setpal(76, ramp((10, 40, 18), (120, 230, 120), 12))     # 76-87 greens
setpal(88, ramp((40, 8, 44), (240, 120, 255), 12))      # 88-99 neon magenta

# UI colors (referenced by #defines in game/common.sch)
PAL[100] = (120, 235, 160)   # VERB_COLOR
PAL[101] = (255, 255, 190)   # VERB_HI_COLOR
PAL[102] = (60, 110, 80)     # VERB_DIM_COLOR
PAL[103] = (18, 24, 28)      # VERB_BACK_COLOR
PAL[104] = (235, 240, 245)   # white / narrator
PAL[105] = (255, 190, 80)    # SPROCKET_COLOR (talk text)
PAL[106] = (140, 220, 255)   # secondary talk color
PAL[107] = (255, 110, 110)   # warning red

# 224-255: costume window. 224 must be the transparent marker.
COST = 224
setpal(COST, [
    (253, 5, 255),     # 0 transparent magenta
    (12, 12, 16),      # 1 outline
    (38, 110, 110),    # 2 teal body
    (24, 70, 72),      # 3 teal shadow
    (70, 170, 160),    # 4 teal highlight
    (130, 138, 150),   # 5 steel
    (80, 86, 96),      # 6 steel dark
    (255, 210, 70),    # 7 lamp yellow
    (255, 250, 180),   # 8 lamp bright
    (170, 90, 40),     # 9 rust accent
    (90, 240, 230),    # 10 mouth light
    (200, 205, 215),   # 11 bright steel
])

FLAT_PAL = [v for c in PAL for v in c]


def new_img(w, h, fill=0):
    im = Image.new("P", (w, h), fill)
    im.putpalette(FLAT_PAL)
    return im


COST_PAL = [v for c in PAL[COST:COST + 32] for v in c]

def save_bmp(im, rel, costume=False):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if costume:
        im = im.copy()
        im.putpalette(COST_PAL)
    im.save(path, "BMP")


# ------------------------------------------------------------- background

# Object geometry, shared with the game code via docks_layout.sch
GEOM = {
    "SIGN":   (96, 6, 128, 32),
    "FERRY":  (0, 42, 44, 32),
    "CRANE":  (48, 18, 52, 72),
    # tall rect: state 1 = crate dangling at the top, state 2 = crate
    # on the dock at the bottom (after Betty gets her oil)
    "CRATE":  (120, 48, 24, 72),
    "STALL":  (150, 56, 50, 46),
    "BOARD":  (196, 66, 36, 38),
    "POSTER": (200, 72, 24, 24),
    "DOOR":   (268, 62, 28, 42),
    "DRAIN":  (148, 120, 24, 10),
    "BOLT":   (112, 116, 16, 8),
}


def draw_scene(sign_lit=True, with_poster=True, crate="hanging"):
    im = new_img(W, H)
    d = ImageDraw.Draw(im)

    # --- sky gradient (night, deep navy up top)
    for y in range(0, 62):
        idx = 52 + min(11, max(0, (y * 9) // 62))
        d.line([(0, y), (W, y)], fill=idx)
    # stars
    for (sx, sy) in [(12, 6), (40, 14), (75, 4), (150, 10), (240, 5),
                     (280, 12), (305, 7), (190, 16), (105, 9), (260, 20)]:
        im.putpixel((sx, sy), 104)

    # --- skyline silhouette of Clanker City
    sky = 56  # skyline base
    d.rectangle([0, sky - 26, 18, sky], fill=53)
    d.rectangle([22, sky - 36, 38, sky], fill=54)
    d.rectangle([42, sky - 20, 58, sky], fill=53)
    d.rectangle([120, sky - 30, 140, sky], fill=54)
    d.rectangle([146, sky - 44, 166, sky], fill=53)   # gear tower
    d.ellipse([146, sky - 58, 166, sky - 38], outline=55, width=2)  # gear
    for a in range(8):  # gear teeth as dots
        import math
        ang = a * math.pi / 4
        tx = 156 + int(12 * math.cos(ang))
        ty = sky - 48 + int(12 * math.sin(ang))
        d.rectangle([tx - 1, ty - 1, tx + 1, ty + 1], fill=55)
    d.rectangle([170, sky - 26, 196, sky], fill=54)
    d.rectangle([200, sky - 38, 214, sky], fill=53)
    d.rectangle([300, sky - 30, 318, sky], fill=54)
    # lit windows
    for (wx, wy) in [(26, sky - 30), (30, sky - 22), (150, sky - 36),
                     (174, sky - 18), (204, sky - 30), (305, sky - 24),
                     (8, sky - 18), (50, sky - 14)]:
        d.rectangle([wx, wy, wx + 1, wy + 2], fill=43)
    # blinking antenna light
    d.line([(156, sky - 58), (156, sky - 66)], fill=6)
    im.putpixel((156, sky - 67), 107)

    # --- water
    d.rectangle([0, 62, W, 84], fill=29)
    for y in range(63, 84, 3):
        for x in range((y * 7) % 13, W, 26):
            d.line([(x, y), (x + 8, y)], fill=31)
    # neon reflection smear under sign area
    for y in range(64, 80, 2):
        d.line([(112, y), (132, y)], fill=33)

    # --- dock planks
    d.rectangle([0, 84, W, H], fill=66)
    for y in range(84, H, 6):
        d.line([(0, y), (W, y)], fill=64)
    for x in range(0, W, 32):
        off = 3 if (x // 32) % 2 else 0
        for y in range(84 + off, H, 6):
            d.line([(x, y), (x, y + 5)], fill=65)
    # dock edge highlight
    d.line([(0, 84), (W, 84)], fill=68)
    # mooring posts along edge
    for px in [70, 180, 250]:
        d.rectangle([px, 76, px + 5, 88], fill=65)
        d.rectangle([px, 75, px + 5, 76], fill=68)

    # --- ferry (broken, listing) at far left
    fx, fy, fw, fh = GEOM["FERRY"]
    d.polygon([(fx, fy + 24), (fx + fw, fy + 28), (fx + fw - 6, fy + 34),
               (fx + 2, fy + 32)], fill=6)                       # hull
    d.rectangle([fx + 8, fy + 12, fx + 30, fy + 24], fill=5)     # cabin
    d.rectangle([fx + 12, fy + 15, fx + 16, fy + 19], fill=1)    # window
    d.rectangle([fx + 22, fy + 4, fx + 27, fy + 14], fill=18)    # funnel
    d.line([(fx + 24, fy + 2), (fx + 28, fy - 2)], fill=4)       # sad smoke
    d.line([(fx + 29, fy - 3), (fx + 33, fy - 5)], fill=3)

    # --- crane + Boom-Arm Betty
    cx, cy, cw, ch = GEOM["CRANE"]
    base_y = cy + ch
    d.rectangle([cx + 18, cy + 12, cx + 26, base_y], fill=19)    # tower
    for y in range(cy + 14, base_y, 6):                          # lattice
        d.line([(cx + 18, y), (cx + 26, y + 4)], fill=17)
        d.line([(cx + 26, y), (cx + 18, y + 4)], fill=17)
    d.rectangle([cx + 12, cy + 2, cx + 34, cy + 14], fill=21)    # cab
    d.rectangle([cx + 15, cy + 5, cx + 21, cy + 10], fill=44)    # cab window
    im.putpixel((cx + 17, cy + 7), 1)                            # Betty's eye
    d.rectangle([cx + 34, cy + 6, cx + 78, cy + 9], fill=19)     # arm
    d.line([(cx + 76, cy + 9), (cx + 76, cy + 30)], fill=11)     # cable

    # crate (within the tall GEOM["CRATE"] rect; see object states)
    kx, ky, kw, kh = GEOM["CRATE"]

    def draw_crate(top):
        d.rectangle([kx + 2, top, kx + kw - 3, top + 15], fill=67)
        d.rectangle([kx + 2, top, kx + kw - 3, top + 15], outline=64)
        d.line([(kx + 2, top + 7), (kx + kw - 3, top + 7)], fill=64)
        d.line([(kx + kw // 2, top), (kx + kw // 2, top + 15)], fill=64)

    if crate == "hanging":
        draw_crate(ky + 2)
    elif crate == "ground":
        # limp cable swinging free, crate sitting on the dock
        d.line([(cx + 76, cy + 30), (cx + 74, cy + 44)], fill=11)
        draw_crate(ky + kh - 16)

    # --- Rivet's scrap stall (shuttered)
    sx, sy, sw, sh = GEOM["STALL"]
    d.rectangle([sx, sy + 10, sx + sw, sy + sh], fill=6)         # booth
    for i in range(0, sw, 8):                                    # awning
        d.rectangle([sx + i, sy, sx + i + 7, sy + 10],
                    fill=24 if (i // 8) % 2 else 9)
    d.rectangle([sx + 4, sy + 18, sx + sw - 4, sy + sh - 6], fill=4)  # shutter
    for y in range(sy + 20, sy + sh - 6, 4):
        d.line([(sx + 4, y), (sx + sw - 4, y)], fill=6)
    d.rectangle([sx + 14, sy + 24, sx + sw - 14, sy + 34], fill=46)   # sign
    d.line([(sx + 16, sy + 27), (sx + sw - 16, sy + 27)], fill=1)
    d.line([(sx + 16, sy + 31), (sx + sw - 22, sy + 31)], fill=1)

    # --- notice board
    bx, by, bw, bh = GEOM["BOARD"]
    d.rectangle([bx + 4, by + bh - 10, bx + 7, by + bh + 14], fill=64)
    d.rectangle([bx + bw - 8, by + bh - 10, bx + bw - 5, by + bh + 14], fill=64)
    d.rectangle([bx, by, bx + bw, by + bh - 6], fill=70)
    d.rectangle([bx + 2, by + 2, bx + bw - 2, by + bh - 8], fill=66)
    if with_poster:
        px, py, pw, ph = GEOM["POSTER"]
        d.rectangle([px + 2, py + 2, px + pw - 3, py + ph - 3], fill=14)
        for ly in range(py + 6, py + ph - 5, 4):
            d.line([(px + 4, ly), (px + pw - 6, ly)], fill=6)
        d.line([(px + 4, py + 5), (px + pw // 2, py + 5)], fill=107)

    # --- tavern front (right)
    tx, ty = 240, 30
    d.rectangle([tx, ty, 319, 104], fill=20)                     # wall
    for y in range(ty + 2, 104, 8):                              # plating
        d.line([(tx, y), (319, y)], fill=18)
    dx, dy, dw, dh = GEOM["DOOR"]
    d.rectangle([dx - 3, dy - 3, dx + dw + 3, dy + dh], fill=17) # frame
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=68)             # door
    d.line([(dx + dw // 2, dy), (dx + dw // 2, dy + dh)], fill=64)
    d.ellipse([dx + dw - 9, dy + 20, dx + dw - 5, dy + 24], outline=44)
    d.rectangle([dx + 4, dy + 6, dx + 12, dy + 12], fill=42)     # porthole
    # tavern window with warm glow
    d.rectangle([tx + 8, ty + 24, tx + 22, ty + 40], fill=44)
    d.line([(tx + 15, ty + 24), (tx + 15, ty + 40)], fill=18)
    d.line([(tx + 8, ty + 32), (tx + 22, ty + 32)], fill=18)
    # tavern sign: a mug glyph
    d.rectangle([tx + 6, ty - 14, tx + 38, ty - 2], fill=2)
    d.rectangle([tx + 10, ty - 12, tx + 18, ty - 4], fill=46)
    d.arc([tx + 18, ty - 11, tx + 24, ty - 5], 270, 90, fill=46)
    d.rectangle([tx + 26, ty - 12, tx + 36, ty - 4], fill=2)

    # --- storm drain
    gx, gy, gw, gh = GEOM["DRAIN"]
    d.rectangle([gx, gy, gx + gw, gy + gh], fill=1)
    for x in range(gx + 2, gx + gw - 1, 4):
        d.line([(x, gy + 1), (x, gy + gh - 1)], fill=4)
    im.putpixel((gx + gw // 2, gy + gh - 2), 45)   # glint

    # --- the neon sign
    nx, ny, nw, nh = GEOM["SIGN"]
    d.rectangle([nx + 4, ny + nh, nx + 7, 84], fill=6)            # posts
    d.rectangle([nx + nw - 8, ny + nh, nx + nw - 5, 84], fill=6)
    d.rectangle([nx, ny, nx + nw, ny + nh], fill=1)               # panel
    d.rectangle([nx, ny, nx + nw, ny + nh], outline=6)
    main = 37 if sign_lit else 30
    sub = 42 if sign_lit else 41
    _neon_text(im, "CLANKER CITY", nx + 8, ny + 4, main)
    _neon_text(im, "POP. 8,01,1", nx + 26, ny + 18, sub, small=True)
    if sign_lit:  # glow dots on frame
        for x in range(nx + 2, nx + nw, 6):
            im.putpixel((x, ny + 1), 39)
            im.putpixel((x, ny + nh - 1), 39)

    return im


FONT3 = {  # minimal 3x5 caps font for in-art signage
    'A': "010101111101101", 'B': "110101110101110", 'C': "011100100100011",
    'D': "110101101101110", 'E': "111100110100111", 'F': "111100110100100",
    'G': "011100101101011", 'H': "101101111101101", 'I': "111010010010111",
    'K': "101110100110101", 'L': "100100100100111", 'M': "101111111101101",
    'N': "101111111111101", 'O': "010101101101010", 'P': "110101110100100",
    'R': "110101110110101", 'S': "011100010001110", 'T': "111010010010010",
    'U': "101101101101011", 'V': "101101101101010", 'W': "101101111111101",
    'Y': "101101010010010", '.': "000000000000010", ',': "000000000010100",
    '0': "010101101101010", '1': "010110010010111", '8': "010101010101010",
    '&': "010101010101011", ' ': "000000000000000",
}


def _neon_text(im, text, x, y, color, small=False):
    step = 4
    for ch in text:
        bits = FONT3.get(ch, FONT3[' '])
        for i, b in enumerate(bits):
            if b == '1':
                px, py = x + (i % 3), y + (i // 3)
                im.putpixel((px, py), color)
        x += step


# ------------------------------------------------- the Scrap & Barrel

# Scene 02 interior geometry (all rects 8-aligned for SCUMM strips)
TAVERN_GEOM = {
    "T_DOOR_OUT":  (8, 56, 24, 48),
    "T_SIGN":      (40, 8, 96, 16),
    "T_SHELF":     (40, 32, 96, 24),
    "T_BAR":       (32, 80, 112, 32),
    "T_GUSKET":    (64, 48, 32, 40),
    "T_PIANO":     (152, 40, 56, 64),
    "T_TABLE":     (200, 88, 48, 32),
    "T_DART":      (272, 32, 24, 24),
    "T_WORKER":    (248, 60, 24, 48),
    "T_DOOR_BACK": (288, 56, 24, 48),
}


def draw_tavern():
    im = new_img(W, H)
    d = ImageDraw.Draw(im)
    g = TAVERN_GEOM

    # --- walls: warm dark rust plating
    d.rectangle([0, 0, W, 104], fill=17)
    for y in range(6, 104, 8):
        d.line([(0, y), (W, y)], fill=16)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, 104)], fill=16)
    d.line([(0, 104), (W, 104)], fill=19)                  # baseboard

    # --- floor: tavern planks, warmer than the docks
    d.rectangle([0, 105, W, H], fill=67)
    for y in range(105, H, 6):
        d.line([(0, y), (W, y)], fill=64)
    for x in range(0, W, 28):
        off = 3 if (x // 28) % 2 else 0
        for y in range(105 + off, H, 6):
            d.line([(x, y), (x, y + 5)], fill=65)

    # --- hanging lamps with sodium glow pools
    for lx in (88, 224):
        d.line([(lx, 0), (lx, 14)], fill=1)
        d.polygon([(lx - 7, 20), (lx + 7, 20), (lx + 3, 14),
                   (lx - 3, 14)], fill=9)
        d.ellipse([lx - 10, 19, lx + 10, 27], fill=44)
        im.putpixel((lx, 22), 47)
        # dim wall glow
        d.ellipse([lx - 26, 12, lx + 26, 44], outline=18)

    # --- front door (back out to the docks)
    dx, dy, dw, dh = g["T_DOOR_OUT"]
    d.rectangle([dx - 3, dy - 3, dx + dw + 3, dy + dh], fill=19)
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=68)
    d.line([(dx + dw // 2, dy), (dx + dw // 2, dy + dh)], fill=64)
    d.rectangle([dx + 4, dy + 8, dx + 12, dy + 16], fill=55)   # night porthole
    im.putpixel((dx + 7, dy + 11), 104)                        # a star
    d.ellipse([dx + dw - 8, dy + 22, dx + dw - 4, dy + 26], outline=44)

    # --- neon sign over the bar
    nx, ny, nw, nh = g["T_SIGN"]
    d.rectangle([nx, ny, nx + nw, ny + nh], fill=1)
    d.rectangle([nx, ny, nx + nw, ny + nh], outline=6)
    _neon_text(im, "SCRAP & BARREL", nx + 19, ny + 6, 94)
    for x in range(nx + 2, nx + nw, 6):
        im.putpixel((x, ny + 1), 92)
        im.putpixel((x, ny + nh - 1), 92)

    # --- bottle shelves
    sx, sy, sw, sh = g["T_SHELF"]
    for row in (0, 1):
        by = sy + row * 12
        d.rectangle([sx, by + 9, sx + sw, by + 11], fill=70)   # board
        for i, bx in enumerate(range(sx + 4, sx + sw - 4, 11)):
            col = [33, 45, 94, 82, 11, 24][(i + row * 3) % 6]
            d.rectangle([bx, by + 1, bx + 5, by + 9], fill=col)
            d.rectangle([bx + 1, by, bx + 4, by + 1], fill=6)  # cap
            im.putpixel((bx + 1, by + 3), 104)                 # glint

    # --- bar counter
    bx, by, bw, bh = g["T_BAR"]
    d.rectangle([bx, by, bx + bw, by + 4], fill=68)            # top
    d.rectangle([bx, by + 4, bx + bw, by + bh], fill=66)       # front
    for x in range(bx + 6, bx + bw, 18):
        d.rectangle([x, by + 8, x + 10, by + bh - 4], fill=64)
    d.line([(bx, by + bh - 2), (bx + bw, by + bh - 2)], fill=46)  # brass rail
    # glasses of 10W-40 on the counter
    for gx2 in (bx + 14, bx + 86):
        d.rectangle([gx2, by - 6, gx2 + 4, by], fill=11)
        d.rectangle([gx2 + 1, by - 4, gx2 + 3, by], fill=45)

    # --- Gusket, polishing the same glass forever
    gx, gy, gw, gh = g["T_GUSKET"]
    d.rectangle([gx + 8, gy + 14, gx + 24, gy + 36], fill=5)   # barrel body
    d.rectangle([gx + 8, gy + 20, gx + 24, gy + 22], fill=6)   # hoop
    d.rectangle([gx + 8, gy + 28, gx + 24, gy + 30], fill=6)
    d.rectangle([gx + 11, gy + 4, gx + 21, gy + 14], fill=6)   # head
    d.rectangle([gx + 10, gy + 2, gx + 22, gy + 5], fill=9)    # cap
    d.rectangle([gx + 13, gy + 8, gx + 15, gy + 10], fill=44)  # eyes
    d.rectangle([gx + 18, gy + 8, gx + 20, gy + 10], fill=44)
    d.line([(gx + 8, gy + 18), (gx + 2, gy + 26)], fill=6)     # left arm
    d.line([(gx + 24, gy + 18), (gx + 30, gy + 12)], fill=6)   # stuck arm
    d.rectangle([gx + 28, gy + 6, gx + 32, gy + 12], fill=11)  # the glass
    for r in (3, 6):                                           # polish loops
        d.ellipse([gx + 27 - r, gy + 6 - r, gx + 33 + r, gy + 12 + r],
                  outline=18)

    # --- player piano (missing three keys)
    px, py, pw, ph = g["T_PIANO"]
    d.rectangle([px, py, px + pw, py + ph - 8], fill=70)       # body
    d.rectangle([px, py, px + pw, py + 4], fill=68)            # lid
    d.rectangle([px + 6, py + 8, px + pw - 6, py + 24], fill=14)   # roll
    for x in range(px + 9, px + pw - 7, 3):                    # perforations
        im.putpixel((x, py + 12), 1)
        im.putpixel((x + 1, py + 18), 1)
    keys_y = py + ph - 20
    d.rectangle([px + 2, keys_y, px + pw - 2, keys_y + 10], fill=1)
    missing = (3, 7, 11)
    for i, kx2 in enumerate(range(px + 4, px + pw - 4, 4)):
        if i in missing:
            continue                                           # the gag
        d.rectangle([kx2, keys_y + 1, kx2 + 2, keys_y + 9], fill=104)
    d.rectangle([px + 4, py + ph - 8, px + 8, py + ph], fill=68)   # legs
    d.rectangle([px + pw - 8, py + ph - 8, px + pw - 4, py + ph], fill=68)

    # --- the Rustlers' corner table
    tx, ty, tw, th = g["T_TABLE"]
    d.ellipse([tx + 4, ty + 6, tx + tw - 4, ty + 22], fill=68)
    d.rectangle([tx + tw // 2 - 2, ty + 20, tx + tw // 2 + 2, ty + th],
                fill=64)
    for wx2, wy2 in [(tx + 14, ty + 11), (tx + 22, ty + 14),
                     (tx + 30, ty + 10)]:                      # washer pot
        d.ellipse([wx2, wy2, wx2 + 3, wy2 + 2], outline=11)
    for cx2, cy2 in [(tx + 10, ty + 15), (tx + 33, ty + 15)]:  # cards
        d.rectangle([cx2, cy2, cx2 + 4, cy2 + 5], fill=104)
    # three corroded pirate-bots, mid-argument
    for i, (rx, ry, eye) in enumerate([(tx - 6, ty - 8, 107),
                                       (tx + 18, ty - 16, 44),
                                       (tx + 42, ty - 8, 31)]):
        d.rectangle([rx + 2, ry + 10, rx + 12, ry + 26], fill=18)  # body
        d.rectangle([rx + 4, ry + 2, rx + 10, ry + 10], fill=20)   # head
        d.rectangle([rx + 5, ry + 5, rx + 7, ry + 7], fill=eye)    # one eye
        if i == 1:
            d.polygon([(rx + 3, ry + 2), (rx + 11, ry + 2),
                       (rx + 7, ry - 3)], fill=1)              # captain hat

    # --- dartboard with three darts in it
    ax, ay, aw, ah = g["T_DART"]
    d.ellipse([ax, ay, ax + aw, ay + ah], fill=104)
    d.ellipse([ax + 3, ay + 3, ax + aw - 3, ay + ah - 3], fill=107)
    d.ellipse([ax + 7, ay + 7, ax + aw - 7, ay + ah - 7], fill=104)
    d.ellipse([ax + 10, ay + 10, ax + aw - 10, ay + ah - 10], fill=1)
    for ddx, ddy in [(4, 6), (16, 4), (9, 18)]:
        d.line([(ax + ddx, ay + ddy), (ax + ddx + 5, ay + ddy - 5)], fill=11)
        im.putpixel((ax + ddx + 5, ay + ddy - 5), 31)

    # --- Flange the dockworker, between games
    wx, wy, ww, wh = g["T_WORKER"]
    d.rectangle([wx + 4, wy + 14, wx + 20, wy + 38], fill=5)   # body
    d.rectangle([wx + 4, wy + 24, wx + 20, wy + 26], fill=9)   # tool belt
    d.rectangle([wx + 7, wy + 4, wx + 17, wy + 14], fill=6)    # head
    d.rectangle([wx + 5, wy + 2, wx + 19, wy + 6], fill=45)    # hard hat
    d.rectangle([wx + 9, wy + 8, wx + 11, wy + 10], fill=31)   # eyes
    d.rectangle([wx + 14, wy + 8, wx + 16, wy + 10], fill=31)
    d.line([(wx + 20, wy + 18), (wx + 26, wy + 12)], fill=6)   # dart arm
    d.line([(wx + 26, wy + 12), (wx + 29, wy + 9)], fill=11)   # dart
    d.rectangle([wx + 6, wy + 38, wx + 9, wy + 46], fill=6)    # legs
    d.rectangle([wx + 15, wy + 38, wx + 18, wy + 46], fill=6)

    # --- back door (to the Rustlers' alley, someday)
    kx, ky, kw, kh = g["T_DOOR_BACK"]
    d.rectangle([kx - 3, ky - 3, kx + kw + 3, ky + kh], fill=16)
    d.rectangle([kx, ky, kx + kw, ky + kh], fill=4)
    for bdy in range(ky + 6, ky + kh, 10):
        im.putpixel((kx + 3, bdy), 6)
        im.putpixel((kx + kw - 3, bdy), 6)
    d.rectangle([kx + 4, ky + 14, kx + kw - 4, ky + 22], fill=1)
    _neon_text(im, "NO", kx + 9, ky + 16, 107)
    im.putpixel((kx + kw // 2, ky - 6), 107)                   # red lamp

    return im


# ----------------------------------------------------------- verb panel

def draw_verb_panel():
    im = new_img(W, PANEL_H, 103)
    d = ImageDraw.Draw(im)
    d.line([(0, 0), (W, 0)], fill=34)            # neon top edge
    d.line([(0, 1), (W, 1)], fill=30)
    for x in range(6, W, 24):                    # rivets
        im.putpixel((x, 4), 6)
        im.putpixel((x, PANEL_H - 3), 6)
    # inventory area separator
    d.line([(212, 4), (212, PANEL_H - 4)], fill=6)
    d.line([(306, 4), (306, PANEL_H - 4)], fill=6)
    return im


# ------------------------------------------------------------- Sprocket
# Costume frames: indices 0-31 (0=transparent), mapped to room pal 224+.
# Canvas 20x34, feet on bottom row, x-centered.

CW, CH = 20, 34

def _sprocket_base(d, legs="stand", facing="S", talk=False):
    """Draw Sprocket on a 20x34 canvas. Origin top-left."""
    O, BODY, SHAD, HI, ST, STD, LAMP, LB, RUST, MOUTH, BST = \
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

    # legs (y 24..33)
    if legs == "stand":
        lpos = [(6, 24, 9, 33), (11, 24, 14, 33)]
        feet = [(4, 31, 9, 33), (11, 31, 16, 33)]
    elif legs == "A":        # left forward
        lpos = [(4, 24, 7, 33), (12, 24, 15, 33)]
        feet = [(2, 31, 7, 33), (12, 31, 17, 33)]
    elif legs == "B":        # passing
        lpos = [(7, 24, 10, 32), (10, 24, 13, 33)]
        feet = [(5, 30, 10, 32), (10, 31, 15, 33)]
    elif legs == "C":        # right forward
        lpos = [(12, 24, 15, 33), (4, 24, 7, 33)]
        feet = [(12, 31, 17, 33), (2, 31, 7, 33)]
    else:                    # "D" passing 2
        lpos = [(10, 24, 13, 33), (7, 24, 10, 32)]
        feet = [(10, 31, 15, 33), (5, 30, 10, 32)]
    for r in lpos:
        d.rectangle(r, fill=STD)
    for r in feet:
        d.rectangle(r, fill=ST)

    # torso (y 12..24)
    d.rectangle([4, 12, 15, 24], fill=BODY)
    d.rectangle([4, 12, 15, 13], fill=HI)
    d.rectangle([4, 23, 15, 24], fill=SHAD)
    d.rectangle([4, 12, 4, 24], fill=SHAD)
    if facing == "S":
        d.rectangle([7, 15, 12, 20], fill=STD)        # chest panel
        d.rectangle([8, 16, 9, 17], fill=LAMP)        # gauge
        d.point((11, 19), fill=RUST)
    elif facing == "N":
        d.rectangle([6, 14, 13, 22], fill=SHAD)       # back hatch
        d.line([(6, 18), (13, 18)], fill=O)
    # arms
    if facing in ("S", "N"):
        d.rectangle([2, 13, 3, 22], fill=ST)
        d.rectangle([16, 13, 17, 22], fill=ST)
        d.rectangle([2, 22, 3, 23], fill=STD)
        d.rectangle([16, 22, 17, 23], fill=STD)
    else:  # E side view: one near arm
        d.rectangle([9, 14, 11, 23], fill=ST)
        d.rectangle([9, 22, 11, 23], fill=STD)

    # head (y 2..12) with antenna
    d.rectangle([5, 3, 14, 11], fill=BODY)
    d.rectangle([5, 3, 14, 4], fill=HI)
    d.rectangle([5, 10, 14, 11], fill=SHAD)
    d.line([(9, 0), (9, 2)], fill=ST)
    d.point((9, 0), fill=LB)
    if facing == "S":
        d.rectangle([7, 6, 8, 7], fill=LAMP)          # eyes
        d.rectangle([11, 6, 12, 7], fill=LAMP)
        d.point((7, 6), fill=LB)
        d.point((11, 6), fill=LB)
        d.rectangle([8, 9, 11, 9], fill=MOUTH if talk else SHAD)
    elif facing == "E":
        d.rectangle([12, 6, 13, 7], fill=LAMP)
        d.point((12, 6), fill=LB)
        d.rectangle([12, 9, 14, 9], fill=MOUTH if talk else SHAD)
    elif facing == "N":
        d.rectangle([6, 5, 13, 9], fill=SHAD)         # back of head vent
        for x in range(7, 13, 2):
            d.line([(x, 6), (x, 8)], fill=BODY)


def gen_sprocket_frames():
    frames = {}
    for legs, n in [("A", 0), ("B", 1), ("C", 2), ("D", 3)]:
        for facing in ("E", "S", "N"):
            im = new_img(CW, CH)
            _sprocket_base(ImageDraw.Draw(im), legs=legs, facing=facing)
            frames[f"walk_{facing}_{n:02d}"] = im
    for facing in ("E", "S", "N"):
        im = new_img(CW, CH)
        _sprocket_base(ImageDraw.Draw(im), legs="stand", facing=facing)
        frames[f"stand_{facing}"] = im
        for tn, talk in [(0, True), (1, False)]:
            im = new_img(CW, CH)
            _sprocket_base(ImageDraw.Draw(im), legs="stand",
                           facing=facing, talk=talk)
            frames[f"talk_{facing}_{tn:02d}"] = im
    return frames


# ---------------------------------------------------------- inventory icons

def gen_inventory_icons():
    icons = {}
    # bolt: hex head + threaded shaft
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.polygon([(8, 4), (13, 2), (18, 4), (18, 10), (13, 12), (8, 10)], fill=12)
    d.polygon([(8, 4), (13, 2), (18, 4)], fill=14)
    d.rectangle([18, 5, 32, 9], fill=10)
    for x in range(20, 32, 3):
        d.line([(x, 5), (x, 9)], fill=6)
    icons["inv_bolt"] = im
    # poster: rolled scroll
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.rectangle([10, 3, 30, 13], fill=14)
    d.line([(12, 6), (28, 6)], fill=107)
    d.line([(12, 9), (24, 9)], fill=6)
    d.line([(12, 11), (26, 11)], fill=6)
    d.rectangle([8, 2, 10, 14], fill=11)
    d.rectangle([30, 2, 32, 14], fill=11)
    icons["inv_poster"] = im
    # drink token: hex coin, house currency of the Scrap & Barrel
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.polygon([(14, 8), (17, 2), (23, 2), (26, 8), (23, 14), (17, 14)],
              fill=82)
    d.polygon([(14, 8), (17, 2), (23, 2), (26, 8), (23, 14), (17, 14)],
              outline=78)
    d.rectangle([19, 6, 21, 10], fill=86)
    icons["inv_token"] = im
    # oil can: the classic long-spout oiler
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.rectangle([10, 7, 20, 13], fill=11)                  # body
    d.polygon([(10, 7), (20, 7), (15, 3)], fill=6)         # cone top
    d.line([(15, 4), (28, 1)], fill=11)                    # spout
    im.putpixel((29, 1), 45)                               # oil drop
    d.rectangle([9, 13, 21, 14], fill=107)                 # red base
    d.arc([20, 8, 26, 14], 270, 90, fill=6)                # handle
    icons["inv_oilcan"] = im
    # wind-up key: one third of a fortune-shaped plot device
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.ellipse([8, 4, 16, 12], outline=46, width=2)         # bow
    d.rectangle([16, 7, 28, 9], fill=45)                   # stem
    d.rectangle([28, 4, 31, 12], fill=46)                  # flag
    d.rectangle([29, 7, 31, 9], fill=0)                    # notch
    icons["inv_windupkey"] = im
    return icons


# ------------------------------------------------------------- stage map
# Machine-readable stage description for the walk-through-er
# (docs/WALKTHROUGHER.md). Everything here derives from the same constants
# that paint the art, so the walkthrougher can never drift from the game.
# Object names must match `name = "..."` in game/docks.scc.

STAGE_OBJECT_NAMES = {
    "SIGN":   "neon sign",
    "BOLT":   "shiny bolt",
    "FERRY":  "ferry",
    "CRANE":  "Boom-Arm Betty",
    "CRATE":  "crate",
    "STALL":  "scrap stall",
    "BOARD":  "notice board",
    "POSTER": "official notice",
    "DOOR":   "tavern door",
    "DRAIN":  "storm drain",
}

TAVERN_OBJECT_NAMES = {
    "T_DOOR_OUT":  "door to the docks",
    "T_SIGN":      "neon bar sign",
    "T_SHELF":     "bottle shelf",
    "T_BAR":       "bar",
    "T_GUSKET":    "Gusket",
    "T_PIANO":     "player piano",
    "T_TABLE":     "rustlers' table",
    "T_DART":      "dartboard",
    "T_WORKER":    "Flange",
    "T_DOOR_BACK": "back door",
}

# rect centers make bad click targets for a few objects
STAGE_HOTSPOT_OVERRIDES = {
    "CRATE": (132, 110),       # click low: works hanging or grounded
}

TAVERN_WALKBOXES = [
    ("tavwest", [(16, 112), (160, 112), (160, 140), (16, 140)]),
    ("taveast", [(160, 112), (304, 112), (304, 140), (160, 140)]),
]

# Verb anchors from game/verbs.scc (verbCenter() -> x is the center;
# y is the text top, so the click point sits a few pixels lower).
STAGE_VERBS = {
    "Pick up": (102, 161), "Examine": (146, 161), "Open":  (188, 161),
    "Talk to": (102, 174), "Give":    (146, 174), "Smell": (188, 174),
    "Use":     (146, 187), "Move":    (188, 187),
}

# Inventory slots from game/verbs.scc: 216+c*48, 162+l*18,
# INVENTORY_COL=2 x INVENTORY_LINE=2 (common.sch), icons 40x16.
STAGE_INV_SLOTS = [(216 + c * 48 + 20, 162 + l * 18 + 8)
                   for l in range(2) for c in range(2)]

WALKBOXES = [
    ("dockwest", [(8, 106), (190, 106), (190, 140), (8, 140)]),
    ("dockeast", [(190, 106), (312, 106), (312, 140), (190, 140)]),
]

STAGE_PROBES = {
    "steel":     list(range(2, 16)),
    "rust":      list(range(16, 28)),
    "teal":      list(range(28, 40)),
    "sodium":    list(range(40, 52)),
    "sky":       list(range(52, 64)),
    "dock-wood": list(range(64, 76)),
    "magenta":   list(range(90, 100)),
    "greens":    list(range(78, 88)),
    "bright-steel": list(range(9, 16)),
    "verb":      [100],
    "verb-hi":   [101],
    "white":     [104],
    "talk":      [105],   # SPROCKET_COLOR — egoSay text
    "talk-2":    [106],
    "red":       [107],
    "sprocket-body": [COST + 2, COST + 3, COST + 4],
}


def emit_stage(path):
    import json
    objects = {}
    for names, geom in [(STAGE_OBJECT_NAMES, GEOM),
                        (TAVERN_OBJECT_NAMES, TAVERN_GEOM)]:
        for key, name in names.items():
            x, y, w, h = geom[key]
            hs = STAGE_HOTSPOT_OVERRIDES.get(key, (x + w // 2, y + h // 2))
            objects[name] = {"rect": [x, y, w, h], "hotspot": list(hs)}
    stage = {
        "comment": "GENERATED by tools/genassets.py --emit-stage; do not edit",
        "screen": {"w": W, "h": H + PANEL_H, "room_h": H},
        "objects": objects,
        "verbs": {name: [x, y + 5] for name, (x, y) in STAGE_VERBS.items()},
        "inventory": {"slots": [list(p) for p in STAGE_INV_SLOTS],
                      "up": [311, 170], "down": [311, 190]},
        "probes": {name: [list(PAL[i]) for i in idxs]
                   for name, idxs in STAGE_PROBES.items()},
        "walkboxes": [{"name": n, "points": [list(p) for p in pts]}
                      for n, pts in WALKBOXES + TAVERN_WALKBOXES],
        "walk_targets": {"center-west": [120, 126], "center-east": [250, 126],
                         "tavern-center": [150, 126]},
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(stage, f, indent=1)
    print(f"Stage map written to {path}")


# ---------------------------------------------------------------- main

def crop(im, key):
    x, y, w, h = GEOM[key]
    return im.crop((x, y, x + w, y + h))


def main():
    os.makedirs(OUT, exist_ok=True)

    lit = draw_scene(sign_lit=True, with_poster=False)
    unlit = draw_scene(sign_lit=False, with_poster=False)
    postered = draw_scene(sign_lit=True, with_poster=True)
    grounded = draw_scene(sign_lit=True, with_poster=False, crate="ground")

    save_bmp(lit, "rooms/docks.bmp")
    save_bmp(crop(lit, "SIGN"), "rooms/sign_on.bmp")
    save_bmp(crop(unlit, "SIGN"), "rooms/sign_off.bmp")
    save_bmp(crop(postered, "POSTER"), "rooms/poster_obj.bmp")
    save_bmp(crop(lit, "CRATE"), "rooms/crate_hanging.bmp")
    save_bmp(crop(grounded, "CRATE"), "rooms/crate_ground.bmp")

    # Scene 02: the Scrap & Barrel
    save_bmp(draw_tavern(), "rooms/tavern.bmp")
    write_box_file(os.path.join(OUT, "rooms", "tavern.box"),
                   [Box(pts, name=n) for n, pts in TAVERN_WALKBOXES])

    # bolt sprite on dock floor (background-colored patch + bolt)
    bx, by, bw, bh = GEOM["BOLT"]
    bolt = crop(lit, "BOLT")
    d = ImageDraw.Draw(bolt)
    d.polygon([(1, 3), (3, 1), (6, 1), (8, 3), (8, 5), (6, 7), (3, 7), (1, 5)],
              fill=12)
    d.rectangle([8, 3, 11, 5], fill=10)
    d.point((3, 2), fill=14)
    save_bmp(bolt, "rooms/bolt_obj.bmp")

    save_bmp(draw_verb_panel(), "verbs/verb_background.bmp")

    for name, im in gen_sprocket_frames().items():
        save_bmp(im, f"sprocket/frames/{name}.bmp", costume=True)

    for name, im in gen_inventory_icons().items():
        save_bmp(im, f"inventory/{name}.bmp")

    # walkbox: dock floor. Two boxes joined at x=190 so the matrix is real.
    write_box_file(os.path.join(OUT, "rooms", "docks.box"),
                   [Box(pts, name=n) for n, pts in WALKBOXES])

    # preview montage for humans
    prev = Image.new("RGB", (W, H + PANEL_H))
    prev.paste(postered.convert("RGB"), (0, 0))
    prev.paste(draw_verb_panel().convert("RGB"), (0, H))
    frames = gen_sprocket_frames()
    for name, px in [("stand_S", 120), ("walk_E_00", 200), ("talk_S_00", 250)]:
        f = frames[name]
        raw = f.tobytes()
        mask = Image.frombytes("L", f.size,
                               bytes(255 if b else 0 for b in raw))
        f = Image.frombytes("P", f.size,
                            bytes((b + COST) & 0xFF for b in raw))
        f.putpalette(FLAT_PAL)
        prev.paste(f.convert("RGB"), (px, 140 - CH), mask)
    prev = prev.resize((W * 3, (H + PANEL_H) * 3), Image.NEAREST)
    prev.save(os.path.join(OUT, "preview.png"))
    print(f"Assets written to {OUT}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--emit-stage":
        emit_stage(sys.argv[2] if len(sys.argv) > 2 else
                   os.path.join(ROOT, "walkthrough", "stage",
                                "docks.stage.json"))
    else:
        main()
