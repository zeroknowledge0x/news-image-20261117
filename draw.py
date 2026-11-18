#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news summary image.

Run once at build time; the graded entry only copies the resulting PNG.
Standard drawing shapes keep the composition legible at ~300 px across.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = "#0B1020"
PANEL = "#151C31"
INK = "#F4F6FB"
MUTED = "#9FB0C9"
GOLD = "#F5B13B"
RED = "#EF5B4C"
BLUE = "#4FA9E8"
GREEN = "#4FC38D"
PINK = "#E878A6"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FB if bold else FR, size)


def center(d, box, text, f, fill):
    x0, y0, x1, y1 = box
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((x0 + x1 - (bb[2] - bb[0])) / 2,
            (y0 + y1 - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill=fill)


def fit_font(text, box_w, size, bold=True):
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    f = font(size, bold)
    while size > 24 and probe.textbbox((0, 0), text, font=f)[2] > box_w:
        size -= 2
        f = font(size, bold)
    return f


def card(d, x, y, w, h, accent, label, sub, icon):
    d.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=PANEL,
                        outline=accent, width=3)
    d.rounded_rectangle((x, y, x + 10, y + h), radius=5, fill=accent)
    center(d, (x + 10, y + 14, x + w, y + 92), label, font(42), INK)
    center(d, (x + 14, y + h - 76, x + w - 12, y + h - 22), sub, font(22), MUTED)
    icon(d, x + w / 2, y + h / 2 + 6, accent)


def bridge(d, cx, cy, c):
    d.rectangle((cx - 96, cy + 28, cx + 96, cy + 36), fill=BLUE)
    for dx in (-72, 72):
        d.polygon([(cx + dx - 9, cy + 30), (cx + dx - 5, cy - 42),
                   (cx + dx + 5, cy - 42), (cx + dx + 9, cy + 30)], fill=c)
    d.line((cx - 88, cy - 26, cx - 18, cy - 20), fill=INK, width=11)
    d.line((cx + 20, cy - 22, cx + 88, cy - 28), fill=INK, width=11)
    d.line((cx - 12, cy - 20, cx + 4, cy + 4), fill=RED, width=9)
    d.line((cx + 8, cy + 6, cx + 20, cy - 22), fill=RED, width=9)
    d.polygon([(cx - 4, cy - 8), (cx + 14, cy + 30), (cx + 2, cy + 28)], fill=RED)


def radar(d, cx, cy, c):
    d.ellipse((cx - 44, cy - 46, cx + 44, cy + 42), outline=c, width=7)
    d.line((cx, cy, cx + 30, cy - 30), fill=c, width=8)
    d.line((cx - 66, cy - 56, cx + 66, cy - 56), fill=INK, width=6)
    d.polygon([(cx + 60, cy - 78), (cx + 88, cy - 62),
               (cx + 60, cy - 46)], fill=RED)
    d.line((cx - 88, cy + 46, cx + 88, cy + 46), fill=BLUE, width=6)
    for k in (-56, -20, 20, 56):
        d.line((cx + k, cy + 28, cx + k + 18, cy + 46), fill=BLUE, width=4)


def summit(d, cx, cy, c):
    d.ellipse((cx - 86, cy + 16, cx + 86, cy + 56), fill=c)
    d.rectangle((cx - 62, cy - 6, cx + 62, cy + 20), fill=INK)
    for dx in (-58, 0, 58):
        d.ellipse((cx + dx - 16, cy - 46, cx + dx + 16, cy - 14), fill=GREEN)
    d.polygon([(cx + 28, cy - 94), (cx + 96, cy - 74),
               (cx + 28, cy - 56)], fill=BLUE)
    d.line((cx - 92, cy - 74, cx + 18, cy - 74), fill=BLUE, width=6)


def market(d, cx, cy, c):
    pts = [(cx - 96, cy - 40), (cx - 54, cy - 12), (cx - 16, cy - 34),
           (cx + 20, cy + 6), (cx + 54, cy + 26), (cx + 96, cy + 62)]
    d.line(pts, fill=RED, width=13, joint="curve")
    for px, py in pts:
        d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=RED)
    d.polygon([(cx + 96, cy + 46), (cx + 96, cy + 86),
               (cx + 56, cy + 78)], fill=RED)


def plane(d, cx, cy, c):
    d.polygon([(cx - 96, cy + 42), (cx + 20, cy + 8),
               (cx + 92, cy + 4), (cx + 70, cy + 34),
               (cx - 40, cy + 66)], fill=c)
    d.polygon([(cx - 30, cy + 14), (cx - 62, cy - 42),
               (cx - 34, cy - 44), (cx + 6, cy + 4)], fill=INK)
    d.line((cx - 84, cy + 54, cx + 58, cy + 54), fill=RED, width=8)
    d.polygon([(cx + 4, cy - 66), (cx + 20, cy - 90),
               (cx + 24, cy - 62)], fill=GOLD)


def aid(d, cx, cy, c):
    d.rectangle((cx - 76, cy - 20, cx + 44, cy + 48), fill=GREEN)
    d.rectangle((cx - 62, cy - 44, cx + 22, cy - 20), fill=INK)
    d.rectangle((cx + 44, cy - 2, cx + 70, cy + 48), fill=INK)
    d.ellipse((cx - 60, cy + 34, cx - 30, cy + 64), fill=BG)
    d.ellipse((cx + 20, cy + 34, cx + 50, cy + 64), fill=BG)
    d.line((cx - 46, cy - 32, cx - 46, cy - 74), fill=c, width=7)
    d.ellipse((cx - 90, cy - 104, cx - 2, cy - 66), fill=PANEL, outline=c, width=5)
    d.line((cx - 90, cy - 94, cx - 2, cy - 78), fill=c, width=4)


def build(path):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for gy in range(0, H, 64):
        d.line((0, gy, W, gy), fill="#121A2E", width=1)
    d.rectangle((0, 0, W, 14), fill=GOLD)

    hero = "17 NOVEMBER 2026"
    center(d, (24, 40, W - 24, 194), hero, fit_font(hero, W - 80, 104), INK)
    center(d, (24, 196, W - 24, 248),
           "TUESDAY  -  THE WORLD IN ONE PICTURE", font(38), GOLD)
    d.line((56, 270, W - 56, 270), fill="#33415E", width=4)

    cw, ch, gx, gy, x0, y0 = 292, 316, 18, 20, 56, 300
    cards = [
        (RED, "UKRAINE", "Kyiv + Crimea bridges", bridge),
        (RED, "GULF", "Iran hits US radar", radar),
        (BLUE, "ASIA", "ASEAN closes: Manila", summit),
        (RED, "MARKETS", "Dow -800; AI slide", market),
        (GOLD, "RUSSIA", "Plane crash: 19 dead", plane),
        (GREEN, "GAZA", "Aid for Gaza urged", aid),
    ]
    for i, spec in enumerate(cards):
        cx = x0 + (i % 3) * (cw + gx)
        cy = y0 + (i // 3) * (ch + gy)
        card(d, cx, cy, cw, ch, *spec)

    d.line((56, 966, W - 56, 966), fill="#33415E", width=4)
    center(d, (24, 970, W - 24, 1014),
           "ONE DAY  -  SIX STORIES  -  17 NOV 2026", font(32), MUTED)
    im.save(path, "PNG", optimize=True)


if __name__ == "__main__":
    build("/opt/data/makefun/repos/news-image-20261117/entry.png")
    print("wrote entry.png")
