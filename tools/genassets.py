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

import glob
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
# per-NPC talk colors (NPC-DIALOG.md item 1) -- spread in hue AND luma:
# the dub reads VP8 4:2:0 footage, not lossless screenshots
PAL[108] = (120, 255, 120)   # GUSKET_COLOR  (bartender green)
PAL[109] = (255, 140, 220)   # VOLTINA_COLOR (tesla pink)
PAL[110] = (255, 255, 120)   # EMCEE_COLOR   (footlight yellow)
PAL[111] = (170, 150, 255)   # RIVET_COLOR   (back-alley violet)
PAL[112] = (140, 220, 255)   # EXTRA_COLOR (took the retired talk-2 cyan; old orange was 4 over driver TOL from SPROCKET under VP8 -- art doctor SYS-2)

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
    # the gap to the Rustlers' alley (Scene 03), sign included
    "ALLEY":  (300, 44, 20, 60),
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

    # --- the neon sign (at the waterline, BEHIND the dockside props:
    # its posts run down to the dock edge, so everything that stands
    # on the dock — board, stall, tavern — must paint over it)
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

    # --- the alley mouth (between tavern and cliff, to Scene 03)
    ax2, ay2, aw2, ah2 = GEOM["ALLEY"]
    d.rectangle([302, 56, 319, 104], fill=1)                  # the gap
    for gy2 in range(62, 100, 12):                            # depth hints
        d.line([(305, gy2), (308, gy2 + 4)], fill=52)
    d.rectangle([300, 44, 319, 54], fill=1)                   # sign panel
    d.rectangle([300, 44, 319, 54], outline=6)
    _neon_text(im, "ALLEY", 300, 46, 45)

    # --- storm drain
    gx, gy, gw, gh = GEOM["DRAIN"]
    d.rectangle([gx, gy, gx + gw, gy + gh], fill=1)
    for x in range(gx + 2, gx + gw - 1, 4):
        d.line([(x, gy + 1), (x, gy + gh - 1)], fill=4)
    im.putpixel((gx + gw // 2, gy + gh - 2), 45)   # glint

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


# ------------------------------------------------- the Rustlers' alley

# Scene 03 geometry. A_DUMPSTER is tall so the open-lid state stays
# inside the object rect (same trick as the docks crate).
ALLEY_GEOM = {
    "A_MOUTH":    (0, 56, 24, 48),
    "A_HIDEOUT":  (40, 56, 24, 48),
    "A_GRAFFITI": (72, 24, 64, 24),
    "A_DUMPSTER": (80, 56, 56, 48),
    "A_ESCAPE":   (144, 8, 32, 64),
    "A_RIVET":    (192, 56, 32, 48),
    "A_JUNK":     (224, 72, 32, 32),
    "A_GATE":     (264, 24, 48, 80),
}


def draw_alley(gate="closed", lid="closed"):
    im = new_img(W, H)
    d = ImageDraw.Draw(im)
    g = ALLEY_GEOM

    # --- a slot of night sky between the rooflines
    for y in range(0, 20):
        idx = 52 + min(11, y * 9 // 20)
        d.line([(0, y), (W, y)], fill=idx)
    for sx, sy in [(30, 4), (90, 9), (170, 3), (230, 11), (300, 6),
                   (130, 14)]:
        im.putpixel((sx, sy), 104)

    # --- back wall: the tavern's rear. Rust plating, zero hospitality.
    d.rectangle([0, 20, W, 108], fill=16)
    for y in range(26, 108, 8):
        d.line([(0, y), (W, y)], fill=17)
    for x in range(20, W, 56):                       # plate seams
        d.line([(x, 20), (x, 108)], fill=17)
    for rx, ry in [(28, 50), (130, 88), (210, 34), (250, 92)]:
        d.ellipse([rx, ry, rx + 10, ry + 5], fill=18)   # rust blooms
    d.line([(0, 108), (W, 108)], fill=19)

    # --- ground: wet asphalt with one honest puddle
    d.rectangle([0, 109, W, H], fill=3)
    for y in range(113, H, 7):
        d.line([(0, y), (W, y)], fill=2)
    d.ellipse([196, 122, 244, 132], fill=53)         # puddle
    d.line([(204, 126), (236, 126)], fill=33)        # neon sheen

    # --- mouth back to the docks (west), with dock-glow spilling in
    mx, my, mw, mh = g["A_MOUTH"]
    d.rectangle([mx, my, mx + mw, my + mh], fill=1)
    d.rectangle([mx, my, mx + 3, my + mh], fill=53)  # far light
    for yy in range(my + 30, my + mh, 5):
        d.line([(mx + 4, yy), (mx + 9, yy)], fill=41)
    d.rectangle([mx, my - 12, mx + 19, my - 2], fill=1)
    d.rectangle([mx, my - 12, mx + 19, my - 2], outline=6)
    _neon_text(im, "DOCKS", mx + 1, my - 10, 42)

    # --- the door you are not supposed to notice
    hx, hy, hw, hh = g["A_HIDEOUT"]
    d.rectangle([hx - 3, hy - 3, hx + hw + 3, hy + hh], fill=17)
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=5)
    for yy in range(hy + 6, hy + hh, 10):            # rivets, no handle
        im.putpixel((hx + 3, yy), 6)
        im.putpixel((hx + hw - 3, yy), 6)
    d.rectangle([hx + 5, hy + 14, hx + hw - 5, hy + 18], fill=1)  # eye slot
    d.rectangle([hx + hw // 2 - 1, hy - 8, hx + hw // 2 + 1, hy - 6],
                fill=107)                            # fresh red lamp

    # --- the wall, annotated by the public
    _neon_text(im, "DYNAMO IS FINE", 76, 24, 94)
    d.line([(75, 27), (132, 25)], fill=107)          # the cross-out
    _neon_text(im, "IT IS NOT", 80, 32, 84)
    _neon_text(im, "NO REFUNDS", 78, 40, 45)

    # --- municipal dumpster (Rivet's, legally)
    dx2, dy2, dw2, dh2 = g["A_DUMPSTER"]
    body_t = dy2 + 26                                # body top (y=82)
    d.rectangle([dx2 + 2, body_t, dx2 + dw2 - 2, dy2 + dh2 - 2], fill=80)
    for x in range(dx2 + 8, dx2 + dw2 - 4, 10):      # ridges
        d.line([(x, body_t + 2), (x, dy2 + dh2 - 4)], fill=78)
    im.putpixel((dx2 + 4, dy2 + dh2 - 1), 1)         # wheels
    im.putpixel((dx2 + dw2 - 5, dy2 + dh2 - 1), 1)
    if lid == "closed":
        d.polygon([(dx2, body_t), (dx2 + dw2, body_t),
                   (dx2 + dw2 - 4, body_t - 6), (dx2 + 4, body_t - 6)],
                  fill=82)
        d.rectangle([dx2 + 22, body_t - 5, dx2 + 34, body_t - 3], fill=84)
    else:
        d.rectangle([dx2 + 4, body_t - 6, dx2 + dw2 - 4, body_t], fill=1)
        d.polygon([(dx2 + 2, body_t - 4), (dx2 + dw2 - 2, body_t - 4),
                   (dx2 + dw2 - 10, dy2 + 2), (dx2 + 10, dy2 + 2)],
                  fill=78)                           # lid thrown back
        d.rectangle([dx2 + 12, body_t - 5, dx2 + 15, body_t - 3],
                    fill=47)                         # the duck (seized)

    # --- fire escape, with management
    ex, ey, ew, eh = g["A_ESCAPE"]
    for py2 in (ey + 16, ey + 36, ey + 56):          # platforms
        d.line([(ex + 2, py2), (ex + ew - 2, py2)], fill=6)
        d.line([(ex + 2, py2 - 6), (ex + ew - 2, py2 - 6)], fill=6)
        for x in range(ex + 4, ex + ew - 2, 5):
            d.line([(x, py2 - 6), (x, py2)], fill=6)
    d.line([(ex + ew - 4, ey + 16), (ex + 4, ey + 36)], fill=8)   # stairs
    d.line([(ex + ew - 4, ey + 36), (ex + 4, ey + 56)], fill=8)
    # the Rustler lookout, taking notes on the top platform
    d.rectangle([ex + 8, ey + 4, ex + 18, ey + 15], fill=1)       # body
    d.rectangle([ex + 10, ey, ex + 16, ey + 4], fill=1)           # head
    im.putpixel((ex + 11, ey + 2), 107)                           # the eye
    d.line([(ex + 8, ey + 6), (ex - 2, ey + 3)], fill=1)          # spyglass
    im.putpixel((ex - 3, ey + 3), 31)

    # --- Rivet, sorting screws by mood
    rx, ry, rw, rh = g["A_RIVET"]
    d.ellipse([rx + 6, ry + 14, rx + 26, ry + 38], fill=5)        # round bot
    d.pieslice([rx + 6, ry + 14, rx + 26, ry + 38], 180, 270,
               fill=9)                                            # odd plate
    d.pieslice([rx + 6, ry + 14, rx + 26, ry + 38], 0, 60,
               fill=66)                                           # odder one
    d.ellipse([rx + 11, ry + 18, rx + 21, ry + 28], fill=6)       # eye ring
    d.ellipse([rx + 13, ry + 20, rx + 19, ry + 26], fill=44)      # the lens
    im.putpixel((rx + 16, ry + 23), 1)                            # pupil
    d.line([(rx + 6, ry + 28), (rx, ry + 36)], fill=6)            # arms
    d.line([(rx + 26, ry + 28), (rx + 32, ry + 38)], fill=6)
    d.rectangle([rx + 10, ry + 38, rx + 13, ry + 46], fill=6)     # stub legs
    d.rectangle([rx + 19, ry + 38, rx + 22, ry + 46], fill=6)
    for bx2, by2 in [(rx - 2, ry + 44), (rx + 2, ry + 46),
                     (rx + 30, ry + 45)]:                         # the moods
        d.rectangle([bx2, by2, bx2 + 2, by2 + 1], fill=12)

    # --- the stock
    jx, jy, jw, jh = g["A_JUNK"]
    d.polygon([(jx, jy + jh), (jx + 8, jy + 10), (jx + 18, jy + 16),
               (jx + 26, jy + 4), (jx + jw, jy + jh)], fill=6)
    d.ellipse([jx + 18, jy + 14, jx + 30, jy + 26], outline=11)   # a wheel
    d.rectangle([jx + 2, jy + 20, jx + 14, jy + 24], fill=18)     # a pipe
    d.line([(jx + 8, jy + 12), (jx + 12, jy + 4)], fill=8)        # a spring

    # --- the funicular gate: Act Two, coin-operated
    fx, fy, fw, fh = g["A_GATE"]
    # rails climbing the cliff out the top-right
    d.line([(fx + 24, fy + 80), (fx + 46, fy)], fill=8)
    d.line([(fx + 32, fy + 80), (fx + 47, fy + 20)], fill=8)
    for i in range(5):                               # ties
        ty2 = fy + 70 - i * 14
        d.line([(fx + 26 + i * 4, ty2), (fx + 34 + i * 4, ty2)], fill=6)
    d.rectangle([fx + 4, fy + 16, fx + 8, fy + 80], fill=6)       # posts
    d.rectangle([fx + 40, fy + 16, fx + 44, fy + 80], fill=6)
    d.rectangle([fx + 4, fy + 12, fx + 44, fy + 16], fill=6)      # beam
    d.rectangle([fx + 2, fy, fx + 46, fy + 10], fill=1)           # sign
    d.rectangle([fx + 2, fy, fx + 46, fy + 10], outline=6)
    _neon_text(im, "MIDTOWN", fx + 4, fy + 2, 45)
    for i in range(3):                               # the up arrow
        d.line([(fx + 36 + i, fy + 7 - i), (fx + 40 - i, fy + 7 - i)],
               fill=45)
    # the opening
    d.rectangle([fx + 8, fy + 20, fx + 40, fy + 80], fill=1)
    if gate == "closed":
        for x in range(fx + 8, fx + 40, 6):          # lattice
            d.line([(x, fy + 20), (x + 12, fy + 80)], fill=6)
            d.line([(x + 12, fy + 20), (x, fy + 80)], fill=6)
    else:
        # the little brass car, lit up like a promise
        d.rectangle([fx + 12, fy + 34, fx + 36, fy + 76], fill=24)
        d.rectangle([fx + 12, fy + 30, fx + 36, fy + 34], fill=6)  # roof
        d.rectangle([fx + 16, fy + 40, fx + 32, fy + 52], fill=44)  # window
        d.line([(fx + 24, fy + 40), (fx + 24, fy + 52)], fill=6)
        d.line([(fx + 12, fy + 60), (fx + 36, fy + 60)], fill=9)
        im.putpixel((fx + 24, fy + 78), 47)          # headlamp
    # fare box on the post, with the price of the future on it
    d.rectangle([fx, fy + 56, fx + 11, fy + 80], fill=5)
    d.rectangle([fx + 2, fy + 60, fx + 9, fy + 62], fill=1)       # slot
    _neon_text(im, "10", fx + 2, fy + 68, 107)

    return im


# --------------------------------------------------- Midtown Gearworks

# Scene 04 geometry. The theater rect covers the marquee (its state
# change is Sprocket's name going up in lights); the box office sits
# below it, non-overlapping. The oil bar facade gives its bottom strip
# to the velvet rope (Scene 07: 2-state, hung/unhooked) so the two
# hotspots never overlap; the rope rect is 8-multiple sized (strips).
MIDTOWN_GEOM = {
    "M_STATION":   (0, 48, 32, 56),
    "M_LEFTYS":    (40, 40, 56, 64),
    "M_OILBAR":    (104, 48, 48, 40),
    "M_ROPE":      (104, 88, 48, 16),
    "M_THEATER":   (160, 24, 72, 48),
    "M_BOXOFFICE": (184, 72, 24, 32),
    "M_CITYHALL":  (240, 32, 72, 72),
    "M_DYNAMO":    (272, 0, 40, 28),
}


def draw_midtown(marquee="blank", rope="hung"):
    im = new_img(W, H)
    d = ImageDraw.Draw(im)
    g = MIDTOWN_GEOM

    # --- sky: thinner up here, and better lit
    for y in range(0, 36):
        idx = 52 + min(11, y * 11 // 36)
        d.line([(0, y), (W, y)], fill=idx)
    for sx, sy in [(20, 5), (60, 12), (110, 3), (150, 9), (200, 6),
                   (250, 4), (40, 20), (135, 16)]:
        im.putpixel((sx, sy), 104)

    # --- the Dynamo District, up the hill behind its fence
    dx0, dy0, dw0, dh0 = g["M_DYNAMO"]
    d.polygon([(dx0 - 8, dy0 + dh0 + 8), (dx0 + 12, dy0 + 10),
               (dx0 + dw0 + 8, dy0 + dh0 + 8)], fill=53)         # the hill
    d.ellipse([dx0 + 12, dy0 + 6, dx0 + 32, dy0 + 20], fill=6)   # the dome
    d.line([(dx0 + 22, dy0 + 6), (dx0 + 22, dy0)], fill=8)       # the coil
    d.ellipse([dx0 + 20, dy0 - 2, dx0 + 24, dy0 + 2], outline=45)
    im.putpixel((dx0 + 22, dy0), 107)                            # the spark
    for fx2 in range(dx0 - 6, dx0 + dw0 + 6, 4):                 # the fence
        d.line([(fx2, dy0 + 24), (fx2, dy0 + 27)], fill=6)

    # --- street wall behind everything
    d.rectangle([0, 36, W, 104], fill=4)
    for y in range(42, 104, 10):
        d.line([(0, y), (W, y)], fill=3)
    d.line([(0, 104), (W, 104)], fill=8)

    # --- funicular station (the way back down)
    sx, sy, sw, sh = g["M_STATION"]
    d.line([(sx + 10, sy + sh), (sx - 8, sy + sh + 30)], fill=8)  # rails
    d.line([(sx + 18, sy + sh), (sx + 2, sy + sh + 30)], fill=8)
    d.rectangle([sx + 2, sy + 10, sx + 28, sy + sh], fill=6)      # kiosk
    d.rectangle([sx + 6, sy + 20, sx + 24, sy + 38], fill=1)      # archway
    d.rectangle([sx, sy, sx + 31, sy + 10], fill=1)               # sign
    d.rectangle([sx, sy, sx + 31, sy + 10], outline=6)
    _neon_text(im, "DOWN", sx + 6, sy + 2, 42)
    im.putpixel((sx + 15, sy + 30), 44)                           # car light

    # --- Lefty's Spare Parts
    lx, ly, lw, lh = g["M_LEFTYS"]
    d.rectangle([lx, ly + 12, lx + lw, ly + lh], fill=19)         # shopfront
    d.rectangle([lx, ly, lx + lw, ly + 12], fill=1)               # sign
    d.rectangle([lx, ly, lx + lw, ly + 12], outline=6)
    _neon_text(im, "LEFTYS", lx + 16, ly + 3, 84)
    d.rectangle([lx + 6, ly + 20, lx + 34, ly + 48], fill=44)     # lit window
    for px2, py2 in [(lx + 10, ly + 28), (lx + 18, ly + 36),
                     (lx + 26, ly + 26)]:                         # the stock
        d.ellipse([px2, py2, px2 + 6, py2 + 6], outline=9)
    d.rectangle([lx + 40, ly + 24, lx + 52, ly + lh - 2], fill=68)  # door
    d.rectangle([lx + 42, ly + 30, lx + 50, ly + 36], fill=1)     # CLOSED
    _neon_text(im, "NO", lx + 43, ly + 31, 107)

    # --- the Oil Bar, uptown filtered (the painted facade runs the
    # full 56px down to the street; the OBJECT rect stops at y88 so
    # the velvet rope strip below it owns its own clicks)
    ox, oy, ow = g["M_OILBAR"][0], g["M_OILBAR"][1], g["M_OILBAR"][2]
    fb = oy + 56                                                  # base
    d.rectangle([ox, oy, ox + ow, fb], fill=1)                    # facade
    for y in range(oy + 4, fb, 6):
        d.line([(ox, y), (ox + ow, y)], fill=5)
    d.rectangle([ox + 14, oy + 26, ox + 34, fb], fill=5)          # door
    d.rectangle([ox + 16, oy + 30, ox + 32, oy + 44], fill=53)    # smoked
    # neon oil-can glyph, cocktail style
    d.rectangle([ox + 14, oy + 6, ox + 26, oy + 16], outline=94)
    d.line([(ox + 26, oy + 8), (ox + 34, oy + 4)], fill=94)
    im.putpixel((ox + 35, oy + 4), 95)
    _neon_text(im, "OIL", ox + 16, oy + 8, 94)
    # velvet rope: two brass posts, one standard (M_ROPE covers this
    # strip — keep all rope paint inside y 88..104). M_OILBAR ends at
    # y88, so oy + oh below means the facade base at y104.
    rope_b = oy + 56                                       # facade base
    for rx2 in (ox + 6, ox + 42):
        d.rectangle([rx2, rope_b - 14, rx2 + 2, rope_b], fill=45)
        im.putpixel((rx2 + 1, rope_b - 15), 47)
    if rope == "hung":
        d.arc([ox + 8, rope_b - 18, ox + 42, rope_b - 4], 0, 180, fill=107)
    else:
        # unhooked: coiled over the left post, off duty
        # (screenplay probe: (112, 95) red only in this state)
        d.rectangle([ox + 5, rope_b - 14, ox + 11, rope_b - 2], fill=107)
        for ly in (rope_b - 11, rope_b - 7):
            d.line([(ox + 5, ly), (ox + 11, ly)], fill=18)

    # --- the Grand Cog Theater
    tx, ty, tw, th = g["M_THEATER"]
    d.rectangle([tx, ty + 40, tx + tw, 104], fill=9)              # facade
    for y in range(ty + 44, 104, 8):
        d.line([(tx, y), (tx + tw, y)], fill=24)
    # entrance doors (between marquee and box office)
    d.rectangle([tx + 6, ty + 52, tx + 20, 102], fill=64)
    d.rectangle([tx + 52, ty + 52, tx + 66, 102], fill=64)
    d.ellipse([tx + 15, ty + 70, tx + 18, ty + 74], outline=44)
    d.ellipse([tx + 54, ty + 70, tx + 57, ty + 74], outline=44)
    # the marquee
    d.rectangle([tx, ty, tx + tw, ty + 40], fill=1)
    d.rectangle([tx, ty, tx + tw, ty + 40], outline=6)
    for x in range(tx + 2, tx + tw - 1, 4):                       # bulbs
        im.putpixel((x, ty + 2), 47 if (x // 4) % 3 else 41)
        im.putpixel((x, ty + 38), 47 if (x // 4) % 3 else 41)
    _neon_text(im, "GRAND COG", tx + 19, ty + 6, 45)
    _neon_text(im, "TALENT NITE", tx + 15, ty + 16, 104)
    if marquee == "sprocket":
        _neon_text(im, "SPROCKET", tx + 21, ty + 26, 47)
    else:
        d.line([(tx + 22, ty + 28), (tx + 50, ty + 28)], fill=5)  # blank line

    # --- box office
    bx, by, bw, bh = g["M_BOXOFFICE"]
    d.rectangle([bx, by, bx + bw, by + bh], fill=24)
    d.rectangle([bx + 4, by + 4, bx + bw - 4, by + 18], fill=44)  # window
    d.rectangle([bx + 8, by + 8, bx + 14, by + 14], fill=6)       # the clerk
    d.rectangle([bx + 9, by + 9, bx + 11, by + 11], fill=31)      # clerk eye
    d.rectangle([bx + 2, by + 20, bx + bw - 2, by + 26], fill=1)  # slot
    _neon_text(im, "ACTS", bx + 4, by + 21, 45)

    # --- City Hall, where nothing is wrong
    cx, cy, cw, ch = g["M_CITYHALL"]
    d.polygon([(cx, cy + 16), (cx + cw // 2, cy), (cx + cw, cy + 16)],
              fill=11)                                            # pediment
    d.rectangle([cx, cy + 16, cx + cw, 104], fill=5)
    for colx in range(cx + 6, cx + cw - 4, 16):                   # columns
        d.rectangle([colx, cy + 22, colx + 6, 102], fill=11)
        d.line([(colx + 3, cy + 22), (colx + 3, 102)], fill=8)
    d.rectangle([cx + 30, cy + 56, cx + 42, 102], fill=64)        # door
    im.putpixel((cx + 39, cy + 78), 44)                           # handle
    # the banner
    d.rectangle([cx + 2, cy + 30, cx + cw - 2, cy + 44], fill=104)
    d.rectangle([cx + 2, cy + 30, cx + cw - 2, cy + 44], outline=1)
    _neon_text(im, "NOTHING", cx + 21, cy + 32, 107)
    _neon_text(im, "IS WRONG", cx + 19, cy + 38, 107)

    # --- street lamps between the storefronts
    for px2 in (100, 156, 236):
        d.rectangle([px2, 60, px2 + 1, 104], fill=6)
        d.ellipse([px2 - 3, 54, px2 + 4, 61], fill=44)
        im.putpixel((px2, 57), 47)

    # --- pavement: cleaner up here, and it knows it
    d.rectangle([0, 105, W, H], fill=5)
    for y in range(110, H, 8):
        d.line([(0, y), (W, y)], fill=4)
    d.line([(0, 106), (W, 106)], fill=8)                          # curb
    # a gear-shaped manhole, hissing in a higher register
    d.ellipse([146, 122, 174, 132], outline=6)
    d.ellipse([152, 124, 168, 130], outline=6)
    for wx2, wy2 in [(158, 118), (162, 114), (157, 110)]:         # steam
        im.putpixel((wx2, wy2), 11)

    return im


# ------------------------------------------- inside the Grand Cog

# Scene 05 geometry. The stage rect is big so the curtain state change
# (closed -> open mid-performance) stays inside the object rect.
GRAND_GEOM = {
    "G_DOOR_OUT":   (0, 56, 24, 48),
    "G_CATWALK":    (168, 0, 104, 16),
    "G_SPOT":       (32, 8, 32, 32),
    "G_CHANDELIER": (88, 0, 48, 24),
    "G_AUDIENCE":   (24, 88, 96, 32),
    "G_EMCEE":      (128, 56, 24, 48),
    "G_STAGE":      (160, 16, 120, 96),
    "G_BACKSTAGE":  (288, 56, 24, 48),
}


def draw_theater(curtain="closed", watcher=True):
    im = new_img(W, H)
    d = ImageDraw.Draw(im)
    g = GRAND_GEOM

    # --- house walls: red-velvet rust, brass trim
    d.rectangle([0, 0, W, 108], fill=17)
    for y in range(8, 108, 12):
        d.line([(0, y), (W, y)], fill=16)
    d.line([(0, 108), (W, 108)], fill=46)             # brass rail
    # carpet
    d.rectangle([0, 109, W, H], fill=18)
    for y in range(113, H, 6):
        d.line([(0, y), (W, y)], fill=16)
    for x in range(0, W, 22):                         # carpet diamonds
        im.putpixel((x + 11, 116), 24)
        im.putpixel((x, 122), 24)

    # --- the chandelier: made of actual chandeliers
    cx, cy, cw, ch = g["G_CHANDELIER"]
    d.line([(cx + cw // 2, 0), (cx + cw // 2, cy + 8)], fill=46)
    d.polygon([(cx + 6, cy + 16), (cx + cw - 6, cy + 16),
               (cx + cw - 14, cy + 8), (cx + 14, cy + 8)], fill=46)
    for lx in range(cx + 8, cx + cw - 4, 8):
        im.putpixel((lx, cy + 18), 47)
        im.putpixel((lx, cy + 19), 44)
    for lx in (cx + 16, cx + cw - 16):                # the sub-chandeliers
        d.line([(lx, cy + 16), (lx, cy + 21)], fill=46)
        im.putpixel((lx, cy + 22), 47)

    # --- lobby doors (back out to the street)
    dx, dy, dw, dh = g["G_DOOR_OUT"]
    d.rectangle([dx - 3, dy - 3, dx + dw + 3, dy + dh], fill=19)
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=64)
    d.line([(dx + dw // 2, dy), (dx + dw // 2, dy + dh)], fill=66)
    d.rectangle([dx + 4, dy + 8, dx + 10, dy + 16], fill=44)   # lobby glow
    d.ellipse([dx + dw - 9, dy + 22, dx + dw - 5, dy + 26], outline=46)

    # --- spotlight booth, operator included
    sx, sy, sw, sh = g["G_SPOT"]
    d.rectangle([sx, sy + 8, sx + sw, sy + sh], fill=6)
    d.rectangle([sx + 4, sy + 12, sx + sw - 4, sy + 24], fill=1)  # window
    d.rectangle([sx + 10, sy + 14, sx + 18, sy + 22], fill=5)     # operator
    d.rectangle([sx + 12, sy + 16, sx + 14, sy + 18], fill=2)     # dim eye
    d.ellipse([sx + 20, sy + 14, sx + 28, sy + 22], outline=11)   # the lamp
    im.putpixel((sx + 24, sy + 18), 8)

    # --- the audience: rows of bots, professionally unimpressed
    ax, ay, aw, ah = g["G_AUDIENCE"]
    for row in (0, 1):
        ry = ay + row * 14
        d.rectangle([ax, ry + 10, ax + aw, ry + 13], fill=64)     # seat backs
        for i, hx in enumerate(range(ax + 4 + row * 6, ax + aw - 6, 13)):
            d.rectangle([hx, ry, hx + 8, ry + 10], fill=1)        # heads
            eye = [44, 31, 107, 94, 45][(i + row) % 5]
            d.rectangle([hx + 2, ry + 3, hx + 3, ry + 4], fill=eye)
            if (i + row) % 4 == 2:
                d.rectangle([hx + 5, ry + 3, hx + 6, ry + 4], fill=eye)
    # the rivals in the front row: a juggler mid-drop, a foghorn singer
    d.rectangle([ax + 8, ay - 10, ax + 16, ay], fill=5)           # juggler
    for jx, jy in [(ax + 4, ay - 16), (ax + 12, ay - 20), (ax + 19, ay - 13)]:
        d.ellipse([jx, jy, jx + 3, jy + 3], outline=11)
    im.putpixel((ax + 6, ay - 2), 107)                            # one dropped
    d.rectangle([ax + 70, ay - 12, ax + 78, ay], fill=18)         # the singer
    d.ellipse([ax + 71, ay - 18, ax + 77, ay - 12], outline=18)   # horn mouth

    # --- the emcee: tuxedo paint job, telescoping arm
    ex, ey, ew, eh = g["G_EMCEE"]
    d.rectangle([ex + 6, ey + 14, ex + 18, ey + 40], fill=1)      # tux body
    d.polygon([(ex + 9, ey + 14), (ex + 15, ey + 14),
               (ex + 12, ey + 24)], fill=104)                     # shirt vee
    im.putpixel((ex + 12, ey + 18), 107)                          # bow tie
    d.rectangle([ex + 8, ey + 4, ex + 16, ey + 14], fill=5)       # head
    d.rectangle([ex + 9, ey + 2, ex + 15, ey + 4], fill=1)        # tiny hat
    d.rectangle([ex + 10, ey + 7, ex + 11, ey + 9], fill=45)      # eyes
    d.rectangle([ex + 13, ey + 7, ex + 14, ey + 9], fill=45)
    d.line([(ex + 18, ey + 20), (ex + 26, ey + 10)], fill=6)      # mic arm
    d.rectangle([ex + 25, ey + 7, ex + 28, ey + 10], fill=2)      # the mic
    d.rectangle([ex + 8, ey + 40, ex + 11, ey + 48], fill=6)      # legs
    d.rectangle([ex + 13, ey + 40, ex + 16, ey + 48], fill=6)

    # --- the catwalk over the stage (where the act's witnesses perch)
    tx, ty, tw, th = g["G_STAGE"]
    d.rectangle([tx + 8, ty - 8, tx + tw - 8, ty - 4], fill=6)    # walkway
    for x in range(tx + 12, tx + tw - 8, 8):
        d.line([(x, ty - 4), (x, ty - 1)], fill=6)                # rail dots
    d.rectangle([tx + 70, ty - 8, tx + 82, ty - 6], fill=1)       # the hatch
    if watcher:
        d.rectangle([tx + 44, ty - 16, tx + 52, ty - 8], fill=1)  # a watcher
        im.putpixel((tx + 46, ty - 13), 107)                      # the eye
        d.line([(tx + 52, ty - 12), (tx + 58, ty - 14)], fill=1)  # spyglass

    # --- the stage
    d.rectangle([tx, ty + th - 16, tx + tw, ty + th], fill=66)    # apron
    for x in range(tx + 4, tx + tw, 12):
        d.line([(x, ty + th - 16), (x, ty + th)], fill=64)
    d.rectangle([tx + 4, ty, tx + tw - 4, ty + 8], fill=46)       # arch top
    d.rectangle([tx + 4, ty, tx + 10, ty + th - 16], fill=46)     # arch sides
    d.rectangle([tx + tw - 10, ty, tx + tw - 4, ty + th - 16], fill=46)
    for bx in range(tx + 8, tx + tw - 6, 8):                      # arch bulbs
        im.putpixel((bx, ty + 4), 47)
    if curtain == "closed":
        # the curtain: heavy red folds, waiting
        d.rectangle([tx + 10, ty + 8, tx + tw - 10, ty + th - 16], fill=20)
        for x in range(tx + 14, tx + tw - 10, 8):
            d.line([(x, ty + 8), (x, ty + th - 16)], fill=18)
        d.polygon([(tx + 10, ty + 8), (tx + tw - 10, ty + 8),
                   (tx + tw - 10, ty + 16), (tx + 10, ty + 16)], fill=24)
    else:
        # curtain open: teal backdrop, mic stand, and a spotlight pool
        d.rectangle([tx + 10, ty + 8, tx + tw - 10, ty + th - 16], fill=29)
        for y in range(ty + 12, ty + th - 16, 6):                 # backdrop
            d.line([(tx + 10, y), (tx + tw - 10, y)], fill=30)
        d.rectangle([tx + 10, ty + 8, tx + 16, ty + th - 16], fill=20)
        d.rectangle([tx + tw - 16, ty + 8, tx + tw - 10, ty + th - 16],
                    fill=20)                                      # tied back
        d.ellipse([tx + 38, ty + th - 28, tx + 82, ty + th - 12],
                  fill=44)                                        # the pool
        d.line([(tx + 60, ty + th - 36), (tx + 60, ty + th - 18)], fill=2)
        d.rectangle([tx + 58, ty + th - 39, tx + 62, ty + th - 36],
                    fill=1)                                       # the mic
        for gx2, gy2 in [(tx + 30, ty + 20), (tx + 70, ty + 14),
                         (tx + 90, ty + 26), (tx + 50, ty + 30)]:
            im.putpixel((gx2, gy2), 47)                           # confetti
            im.putpixel((gx2 + 2, gy2 + 3), 94)

    # --- the stage door
    bx, by, bw, bh = g["G_BACKSTAGE"]
    d.rectangle([bx - 3, by - 3, bx + bw + 3, by + bh], fill=19)
    d.rectangle([bx, by, bx + bw, by + bh], fill=4)
    d.rectangle([bx + 4, by + 12, bx + bw - 4, by + 20], fill=1)
    _neon_text(im, "SD", bx + 8, by + 14, 45)                     # STAGE DOOR
    im.putpixel((bx + bw // 2, by - 6), 94)                       # violet lamp

    return im


# --------------------------------------- backstage at the Grand Cog

# Scene 06 geometry. These rects ARE the object rects in
# game/backstage.scc — keep the two in sync. The reading-table rect
# holds all five card states; the jar and the ghost light get 2-state
# crops (the ghost light flickers: the N-A5 deadline texture).
BACK_GEOM = {
    # state-bearing rects (table, jar, ghost) are 8-multiple sized:
    # SCUMM strips — "Image width and height must be multiples of 8"
    "B_DOOR":     (0, 56, 24, 48),
    "B_RACK":     (32, 36, 44, 60),
    "B_GHOST":    (88, 48, 16, 56),
    "B_VOLTINA":  (148, 28, 48, 52),
    "B_TABLE":    (136, 80, 72, 32),
    "B_CAROUSEL": (208, 64, 24, 32),
    "B_JAR":      (240, 48, 32, 48),
    "B_FUSE":     (296, 24, 18, 28),
    "B_CABLES":   (120, 116, 150, 16),
}

# the three cards on the felt (12x10 each; all state crops share these).
# Screenplay probe anchors derived from here: card I face (150, 90),
# card II face (166, 89), card III back (183, 89), key stem (256, 68).
BACK_CARDS = [(146, 88), (162, 88), (178, 88)]


def draw_backstage(cards=0, jar="key", ghost="lit"):
    """cards: 0 bare felt, 1 card I up, 2 +card II up, 3 +card III face
    down, 4 card III turned. jar: "key"/"empty". ghost: "lit"/"dark"."""
    im = new_img(W, H)
    d = ImageDraw.Draw(im)
    g = BACK_GEOM

    # --- brick back wall: the unpainted side of showbiz
    d.rectangle([0, 0, W, 104], fill=17)
    for y in range(7, 104, 8):
        d.line([(0, y), (W, y)], fill=16)
        off = 8 if (y // 8) % 2 else 0
        for x in range(off, W, 16):
            d.line([(x, y - 7), (x, y)], fill=16)
    # counterweight rail, ropes, sandbags (top-left)
    d.rectangle([0, 4, 64, 6], fill=6)
    for rx in (10, 22, 34):
        d.line([(rx, 7), (rx, 30)], fill=65)
        d.rectangle([rx - 3, 30, rx + 3, 42], fill=66)     # sandbag
        d.line([(rx - 3, 36), (rx + 3, 36)], fill=64)

    # --- wood floor (boards, not the house carpet)
    d.rectangle([0, 105, W, H], fill=65)
    for y in range(110, H, 7):
        d.line([(0, y), (W, y)], fill=64)
    for x in range(13, W, 26):
        d.line([(x, 105), (x, H)], fill=64)

    # --- the parlor: a half-shell of deep curtain where the fire exit
    # should be (drawn first; the booth furniture sits on it)
    d.rectangle([136, 16, 288, 86], fill=18)
    for x in range(142, 288, 8):
        d.line([(x, 20), (x, 86)], fill=20)
    d.rectangle([136, 16, 288, 19], fill=24)               # pelmet
    for x in range(141, 288, 12):
        im.putpixel((x, 20), 24)

    # --- stage door (back to the theater, west wall)
    dx, dy, dw, dh = g["B_DOOR"]
    d.rectangle([dx, dy - 3, dx + dw + 3, dy + dh], fill=19)
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=64)
    d.rectangle([dx + 4, dy + 6, dx + dw - 4, dy + 12], fill=44)   # glow
    d.rectangle([dx + dw - 8, dy + 24, dx + dw - 3, dy + 26], fill=11)

    # --- costume rack: forty years of acts on hangers
    rx, ry, rw, rh = g["B_RACK"]
    d.line([(rx, ry + 4), (rx + rw, ry + 4)], fill=6)      # rail
    d.rectangle([rx, ry + 4, rx + 2, ry + rh], fill=6)     # legs
    d.rectangle([rx + rw - 2, ry + 4, rx + rw, ry + rh], fill=6)
    d.rectangle([rx + 6, ry + 8, rx + 16, ry + 34], fill=66)   # bear suit
    d.rectangle([rx + 8, ry + 5, rx + 14, ry + 10], fill=67)   # bear head
    d.rectangle([rx + 20, ry + 8, rx + 30, ry + 32], fill=5)   # bot suit
    d.rectangle([rx + 22, ry + 12, rx + 28, ry + 15], fill=2)  # visor
    for i in range(8):                                          # the boa
        im.putpixel((rx + 35 + (i % 2), ry + 8 + i * 3), 94)
    for hx in (rx + 11, rx + 25, rx + 36):
        d.line([(hx, ry + 4), (hx, ry + 8)], fill=11)      # hooks

    # --- ghost light: theater law says it never goes out. It flickers.
    gx, gy, gw, gh = g["B_GHOST"]
    d.line([(gx + 8, gy + 16), (gx + 8, gy + gh - 4)], fill=6)   # pole
    d.line([(gx + 3, gy + gh), (gx + 8, gy + gh - 4)], fill=6)   # tripod
    d.line([(gx + 13, gy + gh), (gx + 8, gy + gh - 4)], fill=6)
    if ghost == "lit":
        d.ellipse([gx + 2, gy + 2, gx + 14, gy + 16], outline=44)
        d.ellipse([gx + 4, gy + 4, gx + 12, gy + 14], fill=50)
        im.putpixel((gx + 8, gy + 8), 51)
    else:
        d.ellipse([gx + 2, gy + 2, gx + 14, gy + 16], outline=6)
        d.ellipse([gx + 4, gy + 4, gx + 12, gy + 14], fill=42)

    # --- fuse box: every fuse labeled HER
    fx, fy, fw, fh = g["B_FUSE"]
    d.rectangle([fx, fy, fx + fw - 1, fy + fh], fill=6)
    d.rectangle([fx + 2, fy + 2, fx + fw - 3, fy + 14], fill=5)
    for i in range(3):
        d.rectangle([fx + 4 + i * 4, fy + 5, fx + 5 + i * 4, fy + 10],
                    fill=107)                              # the fuses
    _neon_text(im, "HER", fx + 3, fy + 18, 107)

    # --- cables: every one of them feeds the parlor, and glows
    d.line([(fx + 8, fy + fh), (fx + 8, 118)], fill=9)     # down the wall
    cx0, cy0, cw0, ch0 = g["B_CABLES"]
    for i, yy in enumerate((118, 122, 126)):
        d.line([(cx0 + 4, yy), (fx + 8, yy - i)], fill=9 if i % 2 else 1)
    for x in range(cx0 + 8, cx0 + cw0 - 8, 12):            # the glow
        im.putpixel((x, 120), 31)
        im.putpixel((x + 6, 124), 31)

    # --- Madame Voltina: a tesla coil in a shawl. She's the ball.
    vx, vy, vw, vh = g["B_VOLTINA"]
    vcx = vx + vw // 2                                     # 172
    d.polygon([(vcx - 12, vy + vh), (vcx + 12, vy + vh),
               (vcx + 8, vy + 18), (vcx - 8, vy + 18)], fill=19)   # shawl
    for i, ry2 in enumerate(range(vy + 20, vy + 52, 8)):
        d.ellipse([vcx - 9 + i, ry2, vcx + 9 - i, ry2 + 5],
                  outline=46)                              # coil rings
    im.putpixel((vcx - 7, vy + 24), 107)                   # fuse brooch
    d.ellipse([vcx - 8, vy, vcx + 8, vy + 16], fill=29)    # the dome
    d.ellipse([vcx - 8, vy, vcx + 8, vy + 16], outline=11)
    d.line([(vcx - 3, vy + 11), (vcx, vy + 4), (vcx + 2, vy + 9),
            (vcx + 4, vy + 5)], fill=39)                   # the filament
    im.putpixel((vcx, vy + 4), 104)
    im.putpixel((vcx - 10, vy + 14), 104)                  # insulator
    im.putpixel((vcx + 10, vy + 14), 104)                  # earrings

    # --- the reading table: green felt, scorch marks in threes
    tx, ty, tw, th = g["B_TABLE"]
    d.rectangle([tx + 4, ty + 4, tx + tw - 4, ty + 20], fill=80)   # felt
    d.rectangle([tx + 2, ty + 2, tx + tw - 2, ty + 4], fill=66)    # edge
    d.rectangle([tx + 4, ty + 20, tx + tw - 4, ty + 22], fill=64)
    d.rectangle([tx + 6, ty + 22, tx + 10, ty + th], fill=64)      # legs
    d.rectangle([tx + tw - 10, ty + 22, tx + tw - 6, ty + th], fill=64)
    for sx in (tx + 14, tx + 34, tx + 54):                 # the scorches
        for k in range(3):
            im.putpixel((sx + k * 2, ty + 18), 77)

    # the cards (cumulative: the reading's progress is the art state)
    def card_up(pos, face):
        ux, uy = pos
        d.rectangle([ux, uy, ux + 11, uy + 9], fill=104)
        d.rectangle([ux, uy, ux + 11, uy + 9], outline=6)
        if face == "press":          # a printing press, smiling
            d.rectangle([ux + 3, uy + 4, ux + 8, uy + 6], fill=1)
            im.putpixel((ux + 4, uy + 8), 1)
            im.putpixel((ux + 7, uy + 8), 1)
        elif face == "hand":         # an open hand, palm up
            d.rectangle([ux + 3, uy + 5, ux + 8, uy + 7], fill=1)
            for fpx in range(ux + 3, ux + 9, 2):
                im.putpixel((fpx, uy + 4), 1)
        else:                        # a city upside down, being shaken
            for cpx in range(ux + 3, ux + 10, 3):
                d.line([(cpx, uy + 3), (cpx, uy + 5)], fill=1)
            im.putpixel((ux + 5, uy + 7), 1)
            im.putpixel((ux + 8, uy + 7), 1)

    def card_down(pos):              # rust back, brass border
        ux, uy = pos
        d.rectangle([ux, uy, ux + 11, uy + 9], fill=20)
        d.rectangle([ux, uy, ux + 11, uy + 9], outline=46)
        d.line([(ux + 2, uy + 3), (ux + 9, uy + 7)], fill=24)
        d.line([(ux + 9, uy + 3), (ux + 2, uy + 7)], fill=24)

    if cards >= 1:
        card_up(BACK_CARDS[0], "press")
    if cards >= 2:
        card_up(BACK_CARDS[1], "hand")
    if cards == 3:
        card_down(BACK_CARDS[2])
    if cards >= 4:
        card_up(BACK_CARDS[2], "city")

    # --- the card carousel: it deals for her. It has seniority.
    ax, ay, aw, ah = g["B_CAROUSEL"]
    d.rectangle([ax + 8, ay + 18, ax + aw - 8, ay + ah], fill=64)  # stand
    d.ellipse([ax + 2, ay + 4, ax + aw - 2, ay + 18], fill=46)     # drum
    d.ellipse([ax + 2, ay + 4, ax + aw - 2, ay + 18], outline=9)
    for px2 in range(ax + 6, ax + aw - 4, 4):
        d.line([(px2, ay + 7), (px2, ay + 15)], fill=1)            # slots
    d.line([(ax + aw - 3, ay + 7), (ax + aw + 1, ay + 3)], fill=11)

    # --- the key in the jar (Key #2; the stencil matches the crate)
    jx, jy, jw, jh = g["B_JAR"]
    d.rectangle([jx + 6, jy + 36, jx + jw - 6, jy + jh], fill=66)  # plinth
    d.rectangle([jx + 4, jy + 34, jx + jw - 4, jy + 36], fill=64)
    d.rectangle([jx + 7, jy + 4, jx + jw - 7, jy + 34], fill=31)   # glass
    d.rectangle([jx + 7, jy + 4, jx + jw - 7, jy + 34], outline=11)
    d.rectangle([jx + 9, jy + 1, jx + jw - 9, jy + 4], fill=5)     # lid
    if jar == "key":
        d.ellipse([jx + 11, jy + 8, jx + 21, jy + 16], outline=46) # bow
        d.rectangle([jx + 15, jy + 16, jx + 17, jy + 28], fill=46) # stem
        d.rectangle([jx + 13, jy + 26, jx + 19, jy + 30], fill=47) # flag
        im.putpixel((jx + 16, jy + 12), 39)                # arc shimmer
    else:
        im.putpixel((jx + 14, jy + 20), 39)                # residual arc
    for sy in (jy + 31, jy + 33):                          # stencil bars
        d.line([(jx + 10, sy), (jx + 16, sy)], fill=104)

    return im


# ------------------------------------------------ the Oil Bar, inside

# Scene 07 geometry. These rects ARE the object rects in
# game/oilbar.scc — keep the two in sync. State-bearing rects
# (sommelier, spike, centrifuge) are 8-multiple sized (SCUMM strips).
# Screenplay probe anchors (all y<=75 so the ego can never occlude
# them — Scene 06's probe-vs-walk-target lesson):
#   back-bar backlight   (100, 30)  sodium — the room-is-amber probe
#   sommelier head       (92, 60)   somm-black at post / dock-wood away
#   spike top page       (146, 73)  white when full / dock-wood taken
OILBAR_GEOM = {
    "O_DOOR":     (8, 56, 24, 48),
    "O_BACKBAR":  (36, 24, 96, 32),
    "O_SOMM":     (80, 52, 24, 48),
    "O_COUNTER":  (32, 84, 128, 26),
    "O_LIST":     (40, 72, 16, 16),
    "O_SPIKE":    (140, 64, 16, 24),
    "O_CFUGE":    (152, 4, 40, 16),
    "O_AIDE":     (172, 56, 24, 48),
    "O_BOOTH":    (216, 76, 64, 40),
    "O_PORTRAIT": (224, 16, 36, 40),
    "O_HATCH":    (148, 104, 24, 16),
}


def draw_oilbar(somm="post", spike="full", spin=0):
    """somm: "post"/"cellar". spike: "full"/"taken". spin: 0/1 (the
    centrifuge's two rotation frames — the room's animating element)."""
    im = new_img(W, H)
    d = ImageDraw.Draw(im)
    g = OILBAR_GEOM

    # --- ceiling: dark, with the centrifuge's amber halo
    d.rectangle([0, 0, W, 22], fill=1)
    d.ellipse([140, 2, 204, 26], outline=42)

    # --- walls: mahogany panels, amber-lit
    d.rectangle([0, 22, W, 104], fill=65)
    for y in range(28, 104, 10):
        d.line([(0, y), (W, y)], fill=64)
    for x in range(0, W, 44):
        d.line([(x, 22), (x, 104)], fill=64)
    d.line([(0, 104), (W, 104)], fill=46)             # brass baseboard
    # amber sconces
    for sx in (24, 208, 296):
        d.ellipse([sx - 4, 30, sx + 4, 38], fill=44)
        im.putpixel((sx, 33), 47)

    # --- floor: parquet with a polish you could land on
    d.rectangle([0, 105, W, H], fill=66)
    for y in range(109, H, 6):
        d.line([(0, y), (W, y)], fill=64)
    for x in range(0, W, 24):
        off = 3 if (x // 24) % 2 else 0
        for y in range(105 + off, H, 6):
            d.line([(x, y), (x, y + 5)], fill=65)
    d.line([(0, 106), (W, 106)], fill=47)             # the polish

    # --- cellar hatch (painted floor fixture; never opens on screen)
    hx, hy, hw, hh = g["O_HATCH"]
    d.rectangle([hx + 2, hy + 2, hx + hw - 2, hy + hh - 2], fill=64)
    d.rectangle([hx + 2, hy + 2, hx + hw - 2, hy + hh - 2], outline=9)
    for px2 in (hx + 4, hx + hw - 5):                 # brass hinges
        im.putpixel((px2, hy + 3), 46)
    d.ellipse([hx + hw // 2 - 2, hy + 6, hx + hw // 2 + 2, hy + 10],
              outline=46)                             # lift ring

    # --- frosted door to the street (teal neon leaking through)
    dx, dy, dw, dh = g["O_DOOR"]
    d.rectangle([dx - 3, dy - 3, dx + dw + 3, dy + dh], fill=64)
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=5)
    d.rectangle([dx + 4, dy + 6, dx + dw - 4, dy + 28], fill=53)  # frosted
    for fy in range(dy + 9, dy + 26, 5):
        d.line([(dx + 6, fy), (dx + dw - 6, fy)], fill=31)        # neon leak
    d.ellipse([dx + dw - 8, dy + 30, dx + dw - 4, dy + 34], outline=46)

    # --- back bar: biographies up top, working oil below
    bx, by, bw, bh = g["O_BACKBAR"]
    d.rectangle([bx, by, bx + bw, by + bh], fill=64)
    d.rectangle([bx + 2, by + 2, bx + bw - 2, by + 13], fill=42)  # backlight
    d.rectangle([bx, by + 13, bx + bw, by + 15], fill=70)         # shelf
    for i, ox2 in enumerate(range(bx + 6, bx + bw - 6, 11)):      # top row
        col = [45, 24, 47, 44, 27, 46][i % 6]
        d.rectangle([ox2, by + 4, ox2 + 5, by + 13], fill=col)
        d.rectangle([ox2 + 1, by + 3, ox2 + 4, by + 4], fill=6)   # cap
        im.putpixel((ox2 + 1, by + 6), 104)                       # glint
        im.putpixel((ox2 + 3, by + 11), 1)                        # biography
    d.rectangle([bx, by + 28, bx + bw, by + 30], fill=70)         # low shelf
    for ox2 in range(bx + 8, bx + bw - 6, 13):                    # dark row
        d.rectangle([ox2, by + 18, ox2 + 5, by + 28], fill=52)
        d.rectangle([ox2 + 1, by + 17, ox2 + 4, by + 18], fill=1)
    # (no glints, no biographies: working oil)

    # --- portrait of Mayor Piston, recently enlarged
    px, py, pw, ph = g["O_PORTRAIT"]
    d.rectangle([px + 2, py + 2, px + pw - 2, py + ph - 2], fill=20)
    d.rectangle([px + 8, py + 8, px + pw - 8, py + 22], fill=5)   # the face
    d.rectangle([px + 10, py + 12, px + 12, py + 14], fill=44)    # eyes
    d.rectangle([px + 16, py + 12, px + 18, py + 14], fill=44)
    d.rectangle([px + 8, py + 22, px + pw - 8, py + ph - 6], fill=18)
    d.rectangle([px, py, px + pw, py + ph], outline=46)           # frame
    d.rectangle([px + 1, py + 1, px + pw - 1, py + ph - 1], outline=46)
    # the frame didn't keep up: he continues onto the wall
    d.rectangle([px + pw + 1, py + 12, px + pw + 6, py + 20], fill=5)
    d.rectangle([px + pw + 2, py + 14, px + pw + 4, py + 16], fill=44)

    # --- ceiling centrifuge (2-frame spin)
    cx, cy, cw, ch = g["O_CFUGE"]
    for hx2 in (cx + 8, cx + cw - 8):
        d.line([(hx2, 0), (hx2, cy + 4)], fill=6)                 # hangers
    d.ellipse([cx + 2, cy + 2, cx + cw - 2, cy + ch - 2], fill=46)
    d.ellipse([cx + 2, cy + 2, cx + cw - 2, cy + ch - 2], outline=9)
    marks = (cx + 8, cx + 18, cx + 28) if spin == 0 else \
            (cx + 13, cx + 23, cx + 33)
    for mx in marks:                                              # streaks
        d.line([(mx, cy + 5), (mx + 3, cy + ch - 5)], fill=24)
    im.putpixel((cx + cw // 2, cy + ch - 2), 47)                  # the shine

    # --- the sommelier (behind the counter; absence is a painted
    # state, not a vanishing — the cellar trip has a body to miss)
    sx2, sy2 = g["O_SOMM"][0], g["O_SOMM"][1]
    if somm == "post":
        d.rectangle([sx2 + 6, sy2 + 14, sx2 + 18, sy2 + 40], fill=1)  # chassis
        d.rectangle([sx2 + 8, sy2 + 2, sx2 + 16, sy2 + 14], fill=1)   # head
        d.rectangle([sx2 + 9, sy2 + 6, sx2 + 11, sy2 + 8], fill=44)   # eyes
        d.rectangle([sx2 + 13, sy2 + 6, sx2 + 15, sy2 + 8], fill=44)
        im.putpixel((sx2 + 12, sy2 + 15), 107)                        # bow tie
        d.rectangle([sx2 + 18, sy2 + 18, sx2 + 23, sy2 + 26],
                    fill=104)                                     # the towel
        d.line([(sx2 + 6, sy2 + 18), (sx2, sy2 + 24)], fill=6)    # decant arm
        d.line([(sx2, sy2 + 24), (sx2 + 4, sy2 + 30)], fill=6)
        im.putpixel((sx2, sy2 + 24), 11)                          # a joint
        im.putpixel((sx2 + 4, sy2 + 30), 11)                      # another

    # --- bar counter (painted to x208 so the aide sits AT it; the
    # object rect stops at x160 per OILBAR_GEOM)
    kx2, ky2 = g["O_COUNTER"][0], g["O_COUNTER"][1]
    bar_r = 208
    d.rectangle([kx2, ky2, bar_r, ky2 + 5], fill=68)              # top
    d.line([(kx2, ky2), (bar_r, ky2)], fill=47)                   # amber edge
    d.rectangle([kx2, ky2 + 5, bar_r, ky2 + 25], fill=66)         # front
    for x in range(kx2 + 8, bar_r - 12, 20):
        d.rectangle([x, ky2 + 9, x + 12, ky2 + 21], fill=64)      # panels
    d.line([(kx2, ky2 + 23), (bar_r, ky2 + 23)], fill=46)         # brass rail

    # --- the cellar list, standing on the counter
    lx2, ly2 = g["O_LIST"][0], g["O_LIST"][1]
    d.rectangle([lx2 + 2, ly2 + 2, lx2 + 14, ly2 + 14], fill=104)
    d.rectangle([lx2 + 2, ly2 + 2, lx2 + 14, ly2 + 14], outline=6)
    for ty2 in (ly2 + 5, ly2 + 7, ly2 + 9):
        d.line([(lx2 + 4, ty2), (lx2 + 12, ty2)], fill=6)
    d.line([(lx2 + 4, ly2 + 11), (lx2 + 12, ly2 + 11)], fill=107)  # CANCELLED

    # --- the receipt spike (the bar's paper history, oldest at the
    # bottom; state 2 is minus one municipal document)
    qx, qy = g["O_SPIKE"][0], g["O_SPIKE"][1]
    d.rectangle([qx + 7, qy + 2, qx + 9, qy + 20], fill=46)       # the spike
    im.putpixel((qx + 8, qy + 1), 47)                             # the tip
    if spike == "full":
        d.rectangle([qx + 2, qy + 8, qx + 14, qy + 19], fill=104)  # the stack
        d.line([(qx + 2, qy + 12), (qx + 14, qy + 12)], fill=2)
        d.line([(qx + 2, qy + 16), (qx + 14, qy + 16)], fill=2)
        im.putpixel((qx + 11, qy + 17), 107)                      # the seal
        im.putpixel((qx + 4, qy + 18), 64)                        # thumbprint
    else:
        d.rectangle([qx + 2, qy + 12, qx + 14, qy + 18], fill=104)
        d.line([(qx + 2, qy + 15), (qx + 14, qy + 15)], fill=2)

    # --- the aide, alone at the bar (folded over a glass like a memo
    # nobody filed; drawn over the counter front)
    ax2, ay2 = g["O_AIDE"][0], g["O_AIDE"][1]
    d.rectangle([ax2 + 8, ay2 + 40, ax2 + 16, ay2 + 44], fill=64)  # stool
    d.rectangle([ax2 + 11, ay2 + 44, ax2 + 13, ay2 + 54], fill=6)
    d.rectangle([ax2 + 5, ay2 + 16, ax2 + 17, ay2 + 40], fill=5)   # chassis
    d.rectangle([ax2 + 5, ay2 + 16, ax2 + 17, ay2 + 18], fill=11)
    d.rectangle([ax2 + 8, ay2 + 20, ax2 + 13, ay2 + 26], fill=31)  # the crest
    d.rectangle([ax2 + 6, ay2 + 6, ax2 + 15, ay2 + 16], fill=6)    # head, low
    d.rectangle([ax2 + 8, ay2 + 9, ax2 + 10, ay2 + 11], fill=44)   # eyes
    d.rectangle([ax2 + 12, ay2 + 9, ax2 + 14, ay2 + 11], fill=44)
    d.line([(ax2 + 5, ay2 + 22), (ax2 - 4, ay2 + 28)], fill=6)     # arm
    d.rectangle([ax2 - 6, ay2 + 20, ax2 - 2, ay2 + 28], fill=11)   # the glass
    d.rectangle([ax2 - 5, ay2 + 22, ax2 - 3, ay2 + 28], fill=45)   # untouched

    # --- the corner booth: drinking in formation
    bx2, by2, bw2, bh2 = g["O_BOOTH"]
    d.rectangle([bx2 + 2, by2, bx2 + bw2 - 2, by2 + 30], fill=18)  # bench
    d.rectangle([bx2 + 2, by2, bx2 + bw2 - 2, by2 + 4], fill=24)
    for hx3 in (bx2 + 10, bx2 + 28, bx2 + 46):                    # the aides
        d.rectangle([hx3, by2 + 6, hx3 + 10, by2 + 14], fill=6)   # heads
        d.rectangle([hx3 + 2, by2 + 9, hx3 + 3, by2 + 10], fill=44)
        d.rectangle([hx3 + 6, by2 + 9, hx3 + 7, by2 + 10], fill=44)
        d.rectangle([hx3 - 1, by2 + 14, hx3 + 11, by2 + 26], fill=5)
    d.ellipse([bx2 + 8, by2 + 24, bx2 + bw2 - 8, by2 + 36], fill=68)
    for gx in (bx2 + 16, bx2 + 30, bx2 + 44):                     # in step
        d.rectangle([gx, by2 + 20, gx + 3, by2 + 26], fill=11)
        d.rectangle([gx + 1, by2 + 22, gx + 2, by2 + 26], fill=45)

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
    # magnet on a string: the harbor's least regulated financial instrument
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.rectangle([10, 6, 30, 11], fill=107)                 # bar magnet
    d.rectangle([10, 6, 13, 11], fill=104)                 # painted pole
    d.rectangle([27, 6, 30, 11], fill=104)
    d.line([(20, 6), (20, 3)], fill=11)                    # the string
    d.line([(20, 3), (33, 1)], fill=11)
    icons["inv_magnet"] = im
    # a fistful of bolts: nine, allegedly
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    for hx, hy in [(13, 7), (19, 5), (25, 8), (16, 10), (22, 11)]:
        d.polygon([(hx - 3, hy), (hx, hy - 3), (hx + 3, hy),
                   (hx + 3, hy + 2), (hx, hy + 4), (hx - 3, hy + 2)],
                  fill=12)
        im.putpixel((hx, hy - 2), 14)
    d.rectangle([28, 8, 33, 10], fill=10)                  # one escapee
    icons["inv_boltstash"] = im
    # oil voucher: a ticket with a drop on it, redeemable uptown
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.rectangle([9, 4, 31, 12], fill=44)
    for px in (9, 31):                                     # perforations
        for py in range(5, 12, 2):
            im.putpixel((px, py), 0)
    d.polygon([(15, 6), (13, 9), (15, 11), (17, 9)], fill=18)   # the drop
    d.line([(20, 7), (28, 7)], fill=1)
    d.line([(20, 9), (26, 9)], fill=1)
    icons["inv_voucher"] = im
    # backstage pass: laminated card on a bicycle-chain lanyard
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    for lx in range(8, 32, 4):                             # the lanyard
        im.putpixel((lx, 3), 11)
        im.putpixel((lx + 2, 2), 6)
    d.rectangle([13, 5, 27, 14], fill=94)                  # the card
    d.rectangle([14, 6, 26, 13], outline=90)
    d.line([(16, 8), (24, 8)], fill=104)
    d.line([(16, 11), (22, 11)], fill=104)
    icons["inv_pass"] = im
    # the second key: brass, jar-aged, never been on a marquee
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.rectangle([8, 4, 16, 12], outline=46, width=2)       # square bow
    d.rectangle([16, 7, 28, 9], fill=45)                   # stem
    d.rectangle([28, 4, 31, 12], fill=46)                  # flag
    d.rectangle([29, 7, 31, 9], fill=0)                    # notch
    im.putpixel((12, 8), 31)                               # ozone glint
    icons["inv_voltkey"] = im
    # the cancelled work order: municipal paper, red stamp, banner swatch
    im = new_img(40, 16)
    d = ImageDraw.Draw(im)
    d.rectangle([9, 3, 31, 13], fill=104)                  # the page
    d.line([(12, 5), (28, 5)], fill=6)
    d.line([(12, 7), (26, 7)], fill=6)
    d.line([(12, 9), (24, 9)], fill=6)
    d.line([(13, 11), (27, 6)], fill=107)                  # CANCELLED
    d.rectangle([28, 10, 31, 13], fill=31)                 # banner swatch
    im.putpixel((29, 10), 1)                               # the staple
    icons["inv_workorder"] = im
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
    "ALLEY":  "alley mouth",
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

ALLEY_OBJECT_NAMES = {
    "A_MOUTH":    "way to the docks",
    "A_HIDEOUT":  "steel door",
    "A_GRAFFITI": "graffiti",
    "A_DUMPSTER": "dumpster",
    "A_ESCAPE":   "fire escape",
    "A_RIVET":    "Rivet",
    "A_JUNK":     "junk heap",
    "A_GATE":     "funicular gate",
}

GRAND_OBJECT_NAMES = {
    "G_DOOR_OUT":   "lobby doors",
    "G_CATWALK":    "catwalk",
    "G_SPOT":       "spotlight booth",
    "G_CHANDELIER": "chandelier",
    "G_AUDIENCE":   "the audience",
    "G_EMCEE":      "the emcee",
    "G_STAGE":      "the stage",
    "G_BACKSTAGE":  "stage door",
}

BACK_OBJECT_NAMES = {
    "B_DOOR":     "door to the stage",
    "B_RACK":     "costume rack",
    "B_GHOST":    "ghost light",
    "B_VOLTINA":  "Madame Voltina",
    "B_TABLE":    "reading table",
    "B_CAROUSEL": "card carousel",
    "B_JAR":      "key in a jar",
    "B_FUSE":     "fuse box",
    "B_CABLES":   "cables",
}

MIDTOWN_OBJECT_NAMES = {
    "M_STATION":   "funicular station",
    "M_LEFTYS":    "Lefty's Spare Parts",
    "M_OILBAR":    "the Oil Bar",
    "M_ROPE":      "velvet rope",
    "M_THEATER":   "Grand Cog Theater",
    "M_BOXOFFICE": "box office",
    "M_CITYHALL":  "City Hall",
    "M_DYNAMO":    "the Great Dynamo",
}

OILBAR_OBJECT_NAMES = {
    "O_DOOR":     "door to the street",
    "O_BACKBAR":  "back bar",
    "O_SOMM":     "oil sommelier",
    "O_COUNTER":  "bar counter",
    "O_LIST":     "cellar list",
    "O_SPIKE":    "receipt spike",
    "O_CFUGE":    "centrifuge",
    "O_AIDE":     "the aide",
    "O_BOOTH":    "booth of aides",
    "O_PORTRAIT": "portrait of the Mayor",
    "O_HATCH":    "cellar hatch",
}

# rect centers make bad click targets for a few objects
STAGE_HOTSPOT_OVERRIDES = {
    "CRATE":      (132, 110),  # click low: works hanging or grounded
    "A_DUMPSTER": (108, 94),   # click the body, not the open-lid air
    "A_GATE":     (288, 96),   # click the gate, not the sign
    # click the rope's right end: the ego walks to the click, and the
    # unhooked-coil probe lives on the LEFT post (112, 95) — keep the
    # ego's 20px span clear of it (Scene 06 probe-occlusion lesson)
    "M_ROPE":     (146, 98),
}

TAVERN_WALKBOXES = [
    ("tavwest", [(16, 112), (160, 112), (160, 140), (16, 140)]),
    ("taveast", [(160, 112), (304, 112), (304, 140), (160, 140)]),
]

ALLEY_WALKBOXES = [
    ("alleywest", [(8, 112), (168, 112), (168, 140), (8, 140)]),
    ("alleyeast", [(168, 112), (304, 112), (304, 140), (168, 140)]),
]

MIDTOWN_WALKBOXES = [
    ("midwest", [(8, 112), (168, 112), (168, 140), (8, 140)]),
    ("mideast", [(168, 112), (312, 112), (312, 140), (168, 140)]),
]

GRAND_WALKBOXES = [
    ("grwest", [(8, 112), (160, 112), (160, 140), (8, 140)]),
    ("greast", [(160, 112), (304, 112), (304, 140), (160, 140)]),
]

BACK_WALKBOXES = [
    ("backwest", [(8, 112), (160, 112), (160, 140), (8, 140)]),
    ("backeast", [(160, 112), (304, 112), (304, 140), (160, 140)]),
]

OILBAR_WALKBOXES = [
    ("oilwest", [(8, 112), (160, 112), (160, 140), (8, 140)]),
    ("oileast", [(160, 112), (304, 112), (304, 140), (160, 140)]),
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
    # per-NPC talk colors: the driver classifies talk pixels by nearest
    # color to attribute segments to speakers (NPC-DIALOG.md item 3)
    "talk-gusket":  [108],
    "talk-voltina": [109],
    "talk-emcee":   [110],
    "talk-rivet":   [111],
    "talk-extra":   [112],
    "red":       [107],
    "sprocket-body": [COST + 2, COST + 3, COST + 4],
    # Scene 06: the brass key in (and gone from) Voltina's jar, and the
    # card faces on the felt (Scene 06 screenplay probes)
    "brass":      [45, 46, 47],
    "card-white": [104],
    # Scene 07: the amber room glow (back-bar backlight + bottles) and
    # the sommelier's black chassis (Scene 07 screenplay probes)
    "amber":      list(range(40, 52)),
    "somm-black": [1],
}


TALK_COLOR_TOL = 16 + 8   # driver TOL + VP8 4:2:0 smear margin


def assert_no_talk_collisions():
    """No room paint may approximate a talk color (rows 0-104): the
    driver reads those colors as SPEECH. The piano-keys bug class,
    made un-shippable (NPC-DIALOG.md item 1, art doctor SYS-1)."""
    talk = {name: [PAL[i] for i in idxs]
            for name, idxs in STAGE_PROBES.items()
            if name.startswith("talk")}
    rooms = [os.path.join(OUT, "rooms", f"{r}.bmp")
             for r in ("docks", "tavern", "alley", "midtown",
                       "theater", "backstage")]
    bad = []
    for path in rooms:
        if not os.path.exists(path):
            continue
        im = Image.open(path).convert("RGB")
        px = im.load()
        for yy in range(0, 104):
            for xx in range(im.size[0]):
                p = px[xx, yy]
                for fam, cols in talk.items():
                    for c in cols:
                        if all(abs(a - b) <= TALK_COLOR_TOL
                               for a, b in zip(p, c)):
                            bad.append((os.path.basename(path),
                                        xx, yy, fam, p))
    if bad:
        for b in bad[:10]:
            print("TALK COLLISION:", b)
        raise SystemExit(
            f"{len(bad)} room pixels approximate talk colors -- "
            "the driver would hallucinate speech. Repaint or "
            "re-pick the talk color.")


def emit_stage(path):
    import json
    objects = {}
    for names, geom in [(STAGE_OBJECT_NAMES, GEOM),
                        (TAVERN_OBJECT_NAMES, TAVERN_GEOM),
                        (ALLEY_OBJECT_NAMES, ALLEY_GEOM),
                        (MIDTOWN_OBJECT_NAMES, MIDTOWN_GEOM),
                        (GRAND_OBJECT_NAMES, GRAND_GEOM),
                        (BACK_OBJECT_NAMES, BACK_GEOM),
                        (OILBAR_OBJECT_NAMES, OILBAR_GEOM)]:
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
                      for n, pts in (WALKBOXES + TAVERN_WALKBOXES
                                     + ALLEY_WALKBOXES + MIDTOWN_WALKBOXES
                                     + GRAND_WALKBOXES + BACK_WALKBOXES
                                     + OILBAR_WALKBOXES)],
        "walk_targets": {"center-west": [120, 126], "center-east": [250, 126],
                         "tavern-center": [150, 126],
                         "alley-center": [150, 126],
                         "midtown-center": [150, 126],
                         "grand-center": [140, 126],
                         "backstage-center": [100, 126],
                         "oilbar-center": [120, 126]},
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

    # Scene 03: the Rustlers' alley
    alley = draw_alley()
    alley_open = draw_alley(gate="open", lid="open")

    def acrop(src, key):
        x, y, w, h = ALLEY_GEOM[key]
        return src.crop((x, y, x + w, y + h))

    save_bmp(alley, "rooms/alley.bmp")
    save_bmp(acrop(alley, "A_DUMPSTER"), "rooms/dumpster_closed.bmp")
    save_bmp(acrop(alley_open, "A_DUMPSTER"), "rooms/dumpster_open.bmp")
    save_bmp(acrop(alley, "A_GATE"), "rooms/gate_closed.bmp")
    save_bmp(acrop(alley_open, "A_GATE"), "rooms/gate_open.bmp")
    write_box_file(os.path.join(OUT, "rooms", "alley.box"),
                   [Box(pts, name=n) for n, pts in ALLEY_WALKBOXES])

    # Scene 04: Midtown Gearworks
    midtown = draw_midtown()
    midtown_lit = draw_midtown(marquee="sprocket")

    def mcrop(src, key):
        x, y, w, h = MIDTOWN_GEOM[key]
        return src.crop((x, y, x + w, y + h))

    save_bmp(midtown, "rooms/midtown.bmp")
    save_bmp(mcrop(midtown, "M_THEATER"), "rooms/marquee_blank.bmp")
    save_bmp(mcrop(midtown_lit, "M_THEATER"), "rooms/marquee_sprocket.bmp")
    save_bmp(mcrop(midtown, "M_ROPE"), "rooms/rope_hung.bmp")
    save_bmp(mcrop(draw_midtown(rope="open"), "M_ROPE"),
             "rooms/rope_open.bmp")
    write_box_file(os.path.join(OUT, "rooms", "midtown.box"),
                   [Box(pts, name=n) for n, pts in MIDTOWN_WALKBOXES])

    # Scene 05: inside the Grand Cog
    grand = draw_theater()
    grand_open = draw_theater(curtain="open")

    def gcrop(src, key):
        x, y, w, h = GRAND_GEOM[key]
        return src.crop((x, y, x + w, y + h))

    save_bmp(grand, "rooms/theater.bmp")
    save_bmp(gcrop(grand, "G_STAGE"), "rooms/curtain_closed.bmp")
    save_bmp(gcrop(grand_open, "G_STAGE"), "rooms/curtain_open.bmp")
    save_bmp(gcrop(grand, "G_CATWALK"), "rooms/catwalk_watch.bmp")
    save_bmp(gcrop(draw_theater(watcher=False), "G_CATWALK"),
             "rooms/catwalk_empty.bmp")
    write_box_file(os.path.join(OUT, "rooms", "theater.box"),
                   [Box(pts, name=n) for n, pts in GRAND_WALKBOXES])

    # Scene 06: backstage — Madame Voltina
    back = draw_backstage()

    def bcrop(src, key):
        x, y, w, h = BACK_GEOM[key]
        return src.crop((x, y, x + w, y + h))

    save_bmp(back, "rooms/backstage.bmp")
    save_bmp(bcrop(back, "B_TABLE"), "rooms/table_bare.bmp")
    save_bmp(bcrop(draw_backstage(cards=1), "B_TABLE"),
             "rooms/table_card1.bmp")
    save_bmp(bcrop(draw_backstage(cards=2), "B_TABLE"),
             "rooms/table_card2.bmp")
    save_bmp(bcrop(draw_backstage(cards=3), "B_TABLE"),
             "rooms/table_card3down.bmp")
    save_bmp(bcrop(draw_backstage(cards=4), "B_TABLE"),
             "rooms/table_card3up.bmp")
    save_bmp(bcrop(back, "B_JAR"), "rooms/jar_key.bmp")
    save_bmp(bcrop(draw_backstage(jar="empty"), "B_JAR"),
             "rooms/jar_empty.bmp")
    save_bmp(bcrop(back, "B_GHOST"), "rooms/ghost_lit.bmp")
    save_bmp(bcrop(draw_backstage(ghost="dark"), "B_GHOST"),
             "rooms/ghost_dark.bmp")
    write_box_file(os.path.join(OUT, "rooms", "backstage.box"),
                   [Box(pts, name=n) for n, pts in BACK_WALKBOXES])

    # Scene 07: the Oil Bar, inside
    oil = draw_oilbar()

    def ocrop(src, key):
        x, y, w, h = OILBAR_GEOM[key]
        return src.crop((x, y, x + w, y + h))

    save_bmp(oil, "rooms/oilbar.bmp")
    save_bmp(ocrop(oil, "O_SOMM"), "rooms/somm_post.bmp")
    save_bmp(ocrop(draw_oilbar(somm="cellar"), "O_SOMM"),
             "rooms/somm_away.bmp")
    save_bmp(ocrop(oil, "O_SPIKE"), "rooms/spike_full.bmp")
    save_bmp(ocrop(draw_oilbar(spike="taken"), "O_SPIKE"),
             "rooms/spike_taken.bmp")
    save_bmp(ocrop(oil, "O_CFUGE"), "rooms/cfuge_a.bmp")
    save_bmp(ocrop(draw_oilbar(spin=1), "O_CFUGE"), "rooms/cfuge_b.bmp")
    write_box_file(os.path.join(OUT, "rooms", "oilbar.box"),
                   [Box(pts, name=n) for n, pts in OILBAR_WALKBOXES])

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
    assert_no_talk_collisions()
    print(f"Assets written to {OUT}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--emit-stage":
        emit_stage(sys.argv[2] if len(sys.argv) > 2 else
                   os.path.join(ROOT, "walkthrough", "stage",
                                "docks.stage.json"))
    else:
        main()
