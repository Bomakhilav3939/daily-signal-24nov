#!/usr/bin/env python3
"""Render the news-image-20261124 entry.

1024x1024 ink-on-paper front page from news24.json: masthead, 3 leads,
10 card stories (5x2), 21 brief lines (2 columns), wire footer.
Stdlib + Pillow, no network, no randomness: same input = same image.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 24
PAPER = (247, 243, 234)
CARD_BG = (252, 249, 241)
INK = (26, 35, 64)
RED = (178, 44, 30)
BAR = (20, 27, 49)
LIGHT = (247, 243, 234)
MUTED = (70, 78, 104)
LINE = (190, 184, 168)

FD = "/usr/share/fonts/truetype/dejavu"
F = lambda n, s: ImageFont.truetype(os.path.join(FD, n), s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANSB = lambda s: F("DejaVuSans-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif-Bold.ttf", s)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(d, x, y, text, f, color, gap=2):
    for ch in text:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textlength(ch, font=f) + gap


# ---------------------------------------------------------------- icons
def ic_globe(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=2)
    d.ellipse([x + s * 0.25, y, x + s * 0.75, y + s], outline=c, width=2)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=c, width=2)


def ic_oil(d, x, y, s, c):
    d.rectangle([x + s * 0.25, y + s * 0.15, x + s * 0.75, y + s * 0.9], outline=c, width=2)
    d.line([x + s * 0.25, y + s * 0.35, x + s * 0.75, y + s * 0.35], fill=c, width=2)
    d.line([x + s * 0.25, y + s * 0.65, x + s * 0.75, y + s * 0.65], fill=c, width=2)
    d.line([x + s * 0.38, y, x + s * 0.38, y + s * 0.15], fill=c, width=2)
    d.line([x + s * 0.62, y, x + s * 0.62, y + s * 0.15], fill=c, width=2)


def ic_chip(d, x, y, s, c):
    r = s * 0.2
    d.rectangle([x + r, y + r, x + s - r, y + s - r], outline=c, width=2)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], outline=c, width=2)
    for t in (0.35, 0.5, 0.65):
        d.line([x + s * t, y, x + s * t, y + r], fill=c, width=2)
        d.line([x + s * t, y + s - r, x + s * t, y + s], fill=c, width=2)
        d.line([x, y + s * t, x + r, y + s * t], fill=c, width=2)
        d.line([x + s - r, y + s * t, x + s, y + s * t], fill=c, width=2)


def ic_drone(d, x, y, s, c):
    d.rectangle([x + s * 0.35, y + s * 0.35, x + s * 0.65, y + s * 0.65], outline=c, width=2)
    for cx, cy in ((0.18, 0.18), (0.82, 0.18), (0.18, 0.82), (0.82, 0.82)):
        d.line([x + s * 0.5, y + s * 0.5, x + s * cx, y + s * cy], fill=c, width=2)
        d.ellipse([x + s * cx - s * 0.12, y + s * cy - s * 0.12,
                   x + s * cx + s * 0.12, y + s * cy + s * 0.12], outline=c, width=2)


def ic_radar(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=2)
    d.ellipse([x + s * 0.25, y + s * 0.25, x + s * 0.75, y + s * 0.75], outline=c, width=2)
    d.line([x + s * 0.5, y + s * 0.5, x + s * 0.85, y + s * 0.15], fill=c, width=2)
    d.ellipse([x + s * 0.72, y + s * 0.12, x + s * 0.84, y + s * 0.24], fill=c)


def ic_flag(d, x, y, s, c):
    d.line([x + s * 0.25, y, x + s * 0.25, y + s], fill=c, width=2)
    d.rectangle([x + s * 0.25, y + s * 0.1, x + s * 0.8, y + s * 0.45], outline=c, width=2)
    d.line([x + s * 0.25, y + s * 0.27, x + s * 0.8, y + s * 0.27], fill=c, width=2)


def ic_scales(d, x, y, s, c):
    d.line([x + s * 0.5, y + s * 0.1, x + s * 0.5, y + s * 0.85], fill=c, width=2)
    d.line([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.2], fill=c, width=2)
    d.line([x + s * 0.35, y + s * 0.9, x + s * 0.65, y + s * 0.9], fill=c, width=2)
    for cx in (0.2, 0.8):
        d.line([x + s * cx, y + s * 0.2, x + s * (cx - 0.1), y + s * 0.5], fill=c, width=2)
        d.line([x + s * cx, y + s * 0.2, x + s * (cx + 0.1), y + s * 0.5], fill=c, width=2)
        d.arc([x + s * (cx - 0.1), y + s * 0.35, x + s * (cx + 0.1), y + s * 0.65], 0, 180, fill=c, width=2)


def ic_flame(d, x, y, s, c):
    d.polygon([(x + s * 0.5, y), (x + s * 0.72, y + s * 0.4), (x + s * 0.66, y + s * 0.55),
               (x + s * 0.8, y + s * 0.7), (x + s * 0.7, y + s * 0.92), (x + s * 0.5, y + s),
               (x + s * 0.3, y + s * 0.92), (x + s * 0.2, y + s * 0.7), (x + s * 0.34, y + s * 0.55),
               (x + s * 0.28, y + s * 0.4)], outline=c, width=2)


def ic_cross(d, x, y, s, c):
    d.rectangle([x, y, x + s, y + s], outline=c, width=2)
    cx, cy, w = x + s / 2, y + s / 2, s * 0.14
    d.line([cx - w, cy, cx + w, cy], fill=c, width=2)
    d.line([cx, cy - w, cx, cy + w], fill=c, width=2)


def ic_quake(d, x, y, s, c):
    pts = [(x, y + s * 0.7), (x + s * 0.2, y + s * 0.7), (x + s * 0.32, y + s * 0.2),
           (x + s * 0.45, y + s * 0.85), (x + s * 0.58, y + s * 0.35),
           (x + s * 0.7, y + s * 0.7), (x + s, y + s * 0.7)]
    d.line(pts, fill=c, width=2)


def ic_crowd(d, x, y, s, c):
    for i, (cx, r) in enumerate(((0.3, 0.14), (0.7, 0.14), (0.5, 0.16))):
        top = y + (s * 0.2 if i < 2 else s * 0.38)
        d.ellipse([x + s * cx - s * r, top, x + s * cx + s * r, top + s * 2 * r], outline=c, width=2)
        d.arc([x + s * cx - s * 0.28, top + s * 0.3, x + s * cx + s * 0.28, top + s * 1.1],
              0, 180, fill=c, width=2)


def ic_flood(d, x, y, s, c):
    for i, cx in enumerate((0.25, 0.55, 0.8)):
        d.polygon([(x + s * cx, y + s * (0.1 + 0.15 * i % 2)),
                   (x + s * (cx + 0.12), y + s * (0.45 + 0.15 * i % 2)),
                   (x + s * (cx - 0.12), y + s * (0.45 + 0.15 * i % 2))], outline=c, width=2)
    d.arc([x + s * 0.1, y + s * 0.6, x + s * 0.45, y + s * 0.95], 0, 180, fill=c, width=2)
    d.arc([x + s * 0.4, y + s * 0.6, x + s * 0.75, y + s * 0.95], 0, 180, fill=c, width=2)
    d.arc([x + s * 0.7, y + s * 0.6, x + s * 1.0, y + s * 0.95], 0, 180, fill=c, width=2)


def ic_ball(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=2)
    d.line([x + s * 0.5, y, x + s * 0.5, y + s], fill=c, width=2)
    d.arc([x, y + s * 0.25, x + s, y + s * 0.75], 180, 360, fill=c, width=2)


ICONS = {
    "oil": ic_oil, "chip": ic_chip, "drone": ic_drone, "radar": ic_radar,
    "flag": ic_flag, "scales": ic_scales, "flame": ic_flame, "cross": ic_cross,
    "quake": ic_quake, "crowd": ic_crowd, "flood": ic_flood, "ball": ic_ball,
}


# ---------------------------------------------------------------- layout

def lead_row(d, data, y, h):
    x0 = M
    wtxt = W - 2 * M - 64 - 18
    d.text((x0, y + 2), data["tag"], font=SANSB(12), fill=RED)
    d.text((x0, y + 20), data["headline"], font=SERIF(25), fill=INK)
    dy = y + 50
    for ln in wrap(d, data["deck"], SANS(13), wtxt)[:2]:
        d.text((x0, dy), ln, font=SANS(13), fill=MUTED)
        dy += 16
    ICONS[data["icon"]](d, W - M - 64, y + (h - 64) / 2, 64, INK)


def card(d, x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=LINE, width=1)
    d.rectangle([x, y, x + 3, y + h], fill=RED)
    d.text((x + 10, y + 6), c["region"], font=SANSB(8), fill=RED)
    ICONS[c["icon"]](d, x + w - 10 - 16, y + 5, 16, INK)
    hy = y + 20
    for ln in wrap(d, c["headline"], SANSB(12), w - 20)[:2]:
        d.text((x + 10, hy), ln, font=SANSB(12), fill=INK)
        hy += 14
    d.line([x + 10, hy + 2, x + w - 10, hy + 2], fill=LINE, width=1)
    by = hy + 7
    for ln in wrap(d, c["body"], SANS(10), w - 20)[:4]:
        d.text((x + 10, by), ln, font=SANS(10), fill=MUTED)
        by += 12


def render(path):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "news24.json")) as f:
        data = json.load(f)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.line([M, 14, W - M, 14], fill=INK, width=2)
    d.line([M, 19, W - M, 19], fill=INK, width=1)
    d.text((M, 26), data["kicker_top"], font=SANSB(13), fill=INK)
    kn = data["kicker_no"]
    d.text((W - M - d.textlength(kn, font=SANSB(13)), 26), kn, font=SANSB(13), fill=INK)
    dl = data["date_line"]
    df = SERIF(40)
    d.text(((W - d.textlength(dl, font=df)) / 2, 42), dl, font=df, fill=INK)
    d.line([M, 104, W - M, 104], fill=INK, width=3)

    # leads: 3 rows of 100
    for i, ld in enumerate(data["leads"]):
        y = 114 + i * 106
        lead_row(d, ld, y, 100)
        if i < 2:
            d.line([M, y + 103, W - M, y + 103], fill=INK, width=1)
    d.line([M, 434, W - M, 434], fill=INK, width=3)

    # cards 5x2
    cw, ch, gap = (W - 2 * M - 4 * 8) / 5, 124, 8
    for i, c in enumerate(data["cards"][:10]):
        col, row = i % 5, i // 5
        card(d, M + col * (cw + gap), 444 + row * (ch + gap), cw, ch, c)
    d.line([M, 708, W - M, 708], fill=INK, width=1)

    # briefs: 2 columns, left 11 / right 10
    col_w = (W - 2 * M - 16) / 2
    row_h = (986 - 716) / 11
    for i, b in enumerate(data["briefs"]):
        col = 0 if i < 11 else 1
        row = i if i < 11 else i - 11
        x = M + col * (col_w + 16)
        y = 716 + row * row_h
        d.text((x, y + 4), b["place"], font=SANSB(8.5), fill=RED)
        for ln in wrap(d, b["text"], SANS(11), col_w - 92)[:2]:
            d.text((x + 92, y + 3), ln, font=SANS(11), fill=INK)
            break
        if row < (11 if col == 0 else 10) - 1:
            d.line([x, y + row_h - 1, x + col_w, y + row_h - 1], fill=(226, 220, 206), width=1)

    # footer
    d.rectangle([0, 990, W, H], fill=BAR)
    d.text((M, 1002), data["wire"], font=SANS(9), fill=LIGHT)

    img.save(path, "PNG")
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    render(os.path.join(out, "entry.png"))
