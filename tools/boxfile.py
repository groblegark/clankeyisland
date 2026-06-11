"""Walkbox (.box) file reader/writer — replaces ScummC's GUI boxedit.

File layout (matches boxedit.c save format exactly):
  'boxd' u32be(len)  per box: u8 namelen, name, 8 x i16le coords
                     (ul,ur,lr,ll starting from top-most/left-most point),
                     u8 mask, u8 flags, u16le scale
  'BOXM' u32be(len)  itinerary matrix rows, RLE-ish triplet encoding
  'SCAL' u32be(48)   5 scale slots x 4 u16le

The matrix covers box 0 (the engine's invisible -32000 box, prepended by
scc at load time) plus our boxes, so num = len(boxes) + 1.
"""

import struct

SCC_BOX_INVISIBLE = 0x80
NUM_SCALE_SLOT = 4


class Box:
    def __init__(self, pts, name="", mask=0, flags=0, scale=255):
        # pts: 4 (x, y) corners in clockwise order
        self.pts = list(pts)
        self.name = name
        self.mask = mask
        self.flags = flags
        self.scale = scale


def _sides(box):
    n = len(box.pts)
    return [(box.pts[i], box.pts[(i + 1) % n]) for i in range(n)]


def are_neighbors(boxes, n1, n2):
    """Port of scc_box_are_neighbors. n1/n2 are 1-based (0 = engine box)."""
    if n1 == 0 or n2 == 0:
        return False
    a, b = boxes[n1 - 1], boxes[n2 - 1]
    if (a.flags & SCC_BOX_INVISIBLE) or (b.flags & SCC_BOX_INVISIBLE):
        return False
    for (p, q) in _sides(a):
        if p[0] == q[0]:  # vertical side
            for (r, s) in _sides(b):
                if r[0] != p[0] or s[0] != p[0]:
                    continue
                f, l = sorted((p[1], q[1]))
                f2, l2 = sorted((r[1], s[1]))
                if l < f2 or f > l2:
                    continue
                return True
        if p[1] == q[1]:  # horizontal side
            for (r, s) in _sides(b):
                if r[1] != p[1] or s[1] != p[1]:
                    continue
                f, l = sorted((p[0], q[0]))
                f2, l2 = sorted((r[0], s[0]))
                if l < f2 or f > l2:
                    continue
                return True
    return False


def itinerary_matrix(boxes):
    """Port of scc_box_get_matrix (Kleene shortest-route)."""
    num = len(boxes) + 1
    adj = [[255] * num for _ in range(num)]
    itin = [[255] * num for _ in range(num)]
    for i in range(num):
        for j in range(num):
            if i == j:
                adj[i][j] = 0
                itin[i][j] = j
            elif are_neighbors(boxes, i, j):
                adj[i][j] = 1
                itin[i][j] = j
    for k in range(num):
        for i in range(num):
            for j in range(num):
                if i == j:
                    continue
                d = adj[i][k] + adj[k][j]
                if adj[i][j] > d:
                    adj[i][j] = d
                    itin[i][j] = itin[i][k]
    return itin


def _reorder_pts(pts):
    """Start from the top-most (then left-most) point, like boxedit does."""
    up = min(range(len(pts)), key=lambda i: pts[i][1])
    rest = [i for i in range(len(pts)) if i != up]
    up2 = min(rest, key=lambda i: pts[i][1])
    if pts[up2][0] < pts[up][0]:
        up = up2
    return [pts[(up + i) % len(pts)] for i in range(4)]


def _encode_boxm(itin):
    """Replicates boxedit.c's row encoder, including its quirky run loop
    that compares against row 0 (boxm[j]) rather than the current row."""
    num = len(itin)
    flat = [v for row in itin for v in row]
    out = bytearray()
    for i in range(num):
        out.append(0xFF)
        j = 0
        while j < num:
            v = flat[i * num + j]
            if v == 255:
                j += 1
                continue
            out.append(j)
            while j < num - 1 and v == flat[j]:
                j += 1
            out.append(j)
            out.append(v)
            j += 1
    out.append(0xFF)
    return bytes(out)


def write_box_file(path, boxes, scale_slots=None):
    body = bytearray()
    for b in boxes:
        name = b.name.encode()
        body.append(len(name))
        body += name
        for (x, y) in _reorder_pts(b.pts):
            body += struct.pack("<hh", x, y)
        body.append(b.mask)
        body.append(b.flags)
        body += struct.pack("<H", b.scale)

    boxm = _encode_boxm(itinerary_matrix(boxes))

    if scale_slots is None:
        scale_slots = [(0, 0, 0, 0)] * NUM_SCALE_SLOT
    scal = b"".join(struct.pack("<4H", *s) for s in scale_slots)

    with open(path, "wb") as fd:
        fd.write(b"boxd" + struct.pack(">I", 8 + len(body)) + body)
        fd.write(b"BOXM" + struct.pack(">I", 8 + len(boxm)) + boxm)
        fd.write(b"SCAL" + struct.pack(">I", 8 + len(scal)) + scal)


def read_box_file(path):
    """Parse a boxedit-format file back into (boxes, scale_slots)."""
    data = open(path, "rb").read()
    assert data[:4] == b"boxd", "not a boxd file"
    (blen,) = struct.unpack(">I", data[4:8])
    pos, end = 8, blen
    boxes = []
    while pos < end:
        nlen = data[pos]; pos += 1
        name = data[pos:pos + nlen].decode(); pos += nlen
        coords = struct.unpack("<8h", data[pos:pos + 16]); pos += 16
        mask, flags = data[pos], data[pos + 1]; pos += 2
        (scale,) = struct.unpack("<H", data[pos:pos + 2]); pos += 2
        pts = [(coords[0], coords[1]), (coords[2], coords[3]),
               (coords[4], coords[5]), (coords[6], coords[7])]
        boxes.append(Box(pts, name, mask, flags, scale))
    assert data[pos:pos + 4] == b"BOXM"
    (mlen,) = struct.unpack(">I", data[pos + 4:pos + 8])
    spos = pos + mlen
    assert data[spos:spos + 4] == b"SCAL"
    scal = data[spos + 8:spos + 8 + 32]
    slots = [struct.unpack("<4H", scal[i * 8:i * 8 + 8]) for i in range(4)]
    return boxes, slots


if __name__ == "__main__":
    # Round-trip self-test against ScummC's shipped road.box
    import sys, os, tempfile
    ref = sys.argv[1] if len(sys.argv) > 1 else None
    if ref:
        boxes, slots = read_box_file(ref)
        tmp = tempfile.mktemp(suffix=".box")
        write_box_file(tmp, boxes, slots)
        a, b = open(ref, "rb").read(), open(tmp, "rb").read()
        os.unlink(tmp)
        if a == b:
            print(f"OK: byte-identical round-trip of {ref} "
                  f"({len(boxes)} boxes, {len(a)} bytes)")
        else:
            print(f"MISMATCH: {len(a)} vs {len(b)} bytes")
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    print(f"first diff at offset {i}: {x:02x} vs {y:02x}")
                    break
            sys.exit(1)
