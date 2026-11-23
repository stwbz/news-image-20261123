#!/usr/bin/env python3
"""Draw the news-image entry: a newspaper front page summing up
Monday 23 November 2026, as a 1024x1024 PNG. All text is drawn with
PIL (no AI image generator) so every word is pixel-perfect.
Facts are from live news search for 23 November 2026 only."""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (251, 247, 238)
INK = (17, 17, 17)
RED = (185, 28, 28)
MUTED = (70, 70, 70)
CARD_BG = (255, 255, 255)
CARD_BORDER = (214, 208, 194)
OCEAN = (46, 111, 183)
LAND = (46, 125, 50)
STEEL = (90, 100, 110)
GOLD = (201, 162, 39)

DJV = "/usr/share/fonts/truetype/dejavu/"
LIB = "/usr/share/fonts/truetype/liberation/"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, max_w, start, minimum=14):
    """Largest font size (<= start) whose text fits max_w."""
    size = start
    while size > minimum:
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 1
    return font(path, minimum)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
title = "THE WORLD IN ONE DAY"
f_title = fit(DJV + "DejaVuSerif-Bold.ttf", title, 960, 64)
d.text((W / 2, 52), title, font=f_title, fill=INK, anchor="mm")

d.rectangle([0, 96, W, 154], fill=INK)
date = "MONDAY 23 NOVEMBER 2026"
f_date = fit(DJV + "DejaVuSans-Bold.ttf", date, 940, 44)
d.text((W / 2, 125), date, font=f_date, fill=(255, 255, 255), anchor="mm")

d.line([24, 166, W - 24, 166], fill=INK, width=3)
d.line([24, 172, W - 24, 172], fill=INK, width=1)

# ---------------------------------------------------------------- hero story
hx, hy = 24, 186
d.text((hx, hy), "CLIMATE SUMMIT", font=font(DJV + "DejaVuSans-Bold.ttf", 24), fill=RED)
f_head = font(DJV + "DejaVuSerif-Bold.ttf", 60)
d.text((hx, hy + 34), "COP31 TALKS", font=f_head, fill=INK)
d.text((hx, hy + 96), "COLLAPSE", font=f_head, fill=INK)
f_sub = font(LIB + "LiberationSans-Regular.ttf", 24)
d.text((hx, hy + 170), "Climate deal fails as nations split over fossil fuels", font=f_sub, fill=MUTED)

# cracked globe illustration (right of the hero text)
cx, cy, r = 840, 280, 105
layer = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)
ld.ellipse([4, 4, 2 * r + 4, 2 * r + 4], fill=OCEAN + (255,))
ld.ellipse([30, 40, 95, 95], fill=LAND + (255,))
ld.ellipse([110, 110, 185, 175], fill=LAND + (255,))
ld.ellipse([120, 35, 165, 70], fill=LAND + (255,))
ld.ellipse([45, 130, 90, 165], fill=LAND + (255,))
mask = Image.new("L", (2 * r + 8, 2 * r + 8), 0)
md = ImageDraw.Draw(mask)
md.ellipse([4, 4, 2 * r + 4, 2 * r + 4], fill=255)
img.paste(layer, (cx - r - 4, cy - r - 4), mask)
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
crack = [(cx - 15, cy - r + 8), (cx + 6, cy - 58), (cx - 12, cy - 18),
         (cx + 14, cy + 16), (cx - 6, cy + 56), (cx + 10, cy + r - 10)]
d.line(crack, fill=INK, width=6, joint="curve")

# ---------------------------------------------------------------- section header
d.text((24, 392), "AROUND THE WORLD", font=font(DJV + "DejaVuSans-Bold.ttf", 24), fill=INK)
d.line([24, 420, W - 24, 420], fill=INK, width=2)

# ---------------------------------------------------------------- story cards
CARDS = [
    ("HORMUZ", "Tankers struck in Strait of Hormuz", "tanker"),
    ("UKRAINE", "Russian drone hits Kyiv flats: 2 dead, 11 missing", "flats"),
    ("LIBYA", "Sea drones hit Russian warship at Benghazi", "warship"),
    ("MEXICO", "Cartel boss 'Chapo Isidro' captured", "badge"),
    ("MERCURY", "BepiColombo enters Mercury orbit", "planet"),
    ("INDONESIA", "Factory fire: 24 dead, dozens missing", "factory"),
]
# Six stories, two columns by three rows: world, not one country or beat.


def icon_tanker(dr, x, y, s):
    # smoke + flame above the deck
    dr.ellipse([x + 30, y + 2, x + 44, y + 16], fill=(150, 150, 150))
    dr.ellipse([x + 38, y - 6, x + 52, y + 8], fill=(170, 170, 170))
    dr.polygon([(x + 48, y + 22), (x + 54, y + 8), (x + 60, y + 22)], fill=(230, 120, 20))
    dr.polygon([(x + 51, y + 22), (x + 54, y + 13), (x + 57, y + 22)], fill=(250, 200, 40))
    # containers on deck
    dr.rectangle([x + 6, y + 30, x + 26, y + 48], fill=(185, 28, 28))
    dr.rectangle([x + 28, y + 30, x + 48, y + 48], fill=(46, 111, 183))
    dr.rectangle([x + 50, y + 30, x + 62, y + 48], fill=(201, 162, 39))
    # bridge tower
    dr.rectangle([x + 64, y + 24, x + 78, y + 48], fill=(240, 240, 240), outline=INK, width=1)
    # hull
    dr.polygon([(x + 2, y + 48), (x + 82, y + 48), (x + 74, y + 66), (x + 10, y + 66)],
               fill=(31, 41, 55))
    # water
    dr.line([x, y + 74, x + 84, y + 74], fill=OCEAN, width=3)
    dr.line([x + 8, y + 80, x + 76, y + 80], fill=OCEAN, width=2)


def icon_flats(dr, x, y, s):
    # apartment block with a damaged top-right corner
    dr.rectangle([x + 10, y + 14, x + 66, y + 68], fill=(150, 150, 150), outline=INK, width=2)
    for wx in (18, 34, 50):
        for wy in (22, 38, 54):
            dr.rectangle([x + wx, y + wy, x + wx + 8, y + wy + 8], fill=(60, 60, 60))
    # broken corner: jagged dark bite out of the top right
    dr.polygon([(x + 66, y + 14), (x + 66, y + 34), (x + 54, y + 26),
                (x + 58, y + 14)], fill=(40, 40, 40))
    dr.polygon([(x + 50, y + 68), (x + 58, y + 76), (x + 66, y + 68),
                (x + 74, y + 76), (x + 82, y + 68)], fill=(100, 100, 100))
    # small flame at the damage
    dr.polygon([(x + 58, y + 14), (x + 62, y + 4), (x + 66, y + 14)], fill=(230, 120, 20))


def icon_warship(dr, x, y, s):
    # drone above
    dr.rectangle([x + 30, y + 4, x + 38, y + 10], fill=INK)
    dr.ellipse([x + 24, y + 2, x + 30, y + 8], fill=INK)
    dr.ellipse([x + 38, y + 2, x + 44, y + 8], fill=INK)
    # superstructure + mast
    dr.rectangle([x + 30, y + 26, x + 52, y + 46], fill=(200, 200, 200), outline=INK, width=1)
    dr.line([x + 41, y + 26, x + 41, y + 12], fill=INK, width=3)
    # hull with pointed bow
    dr.polygon([(x + 6, y + 46), (x + 78, y + 46), (x + 70, y + 62),
                (x + 14, y + 62)], fill=STEEL)
    dr.line([x, y + 70, x + 84, y + 70], fill=OCEAN, width=3)
    dr.line([x + 8, y + 76, x + 76, y + 76], fill=OCEAN, width=2)


def icon_badge(dr, x, y, s):
    # gold badge with a star
    cxb, cyb = x + 34, y + 34
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 30 if i % 2 == 0 else 13
        pts.append((cxb + rad * math.cos(ang), cyb + rad * math.sin(ang)))
    dr.polygon(pts, fill=GOLD, outline=(120, 90, 10))
    dr.ellipse([cxb - 15, cyb - 15, cxb + 15, cyb + 15], fill=(255, 255, 255))
    dr.text((cxb, cyb), "\u2605", font=font(DJV + "DejaVuSans-Bold.ttf", 26),
            fill=GOLD, anchor="mm")
    # handcuff rings
    dr.ellipse([x + 56, y + 56, x + 76, y + 76], outline=STEEL, width=4)
    dr.ellipse([x + 64, y + 62, x + 84, y + 82], outline=STEEL, width=4)


def icon_planet(dr, x, y, s):
    # Mercury with a ring and a tiny spacecraft
    cxp, cyp, rp = x + 40, y + 42, 26
    dr.ellipse([cxp - rp - 26, cyp - 10, cxp + rp + 26, cyp + 10],
               outline=(150, 150, 150), width=3)
    dr.ellipse([cxp - rp, cyp - rp, cxp + rp, cyp + rp], fill=(169, 144, 126), outline=INK, width=2)
    dr.ellipse([cxp - 14, cyp - 8, cxp - 6, cyp], fill=(120, 100, 88))
    dr.ellipse([cxp + 4, cyp + 6, cxp + 12, cyp + 14], fill=(120, 100, 88))
    dr.ellipse([cxp + 8, cyp - 14, cxp + 14, cyp - 8], fill=(120, 100, 88))
    # spacecraft dot with trail
    dr.line([x + 66, y + 12, x + 76, y + 6], fill=INK, width=2)
    dr.polygon([(x + 76, y + 2), (x + 84, y + 8), (x + 76, y + 12)], fill=RED)


def icon_factory(dr, x, y, s):
    # flame + smoke
    dr.ellipse([x + 52, y + 2, x + 64, y + 14], fill=(150, 150, 150))
    dr.polygon([(x + 14, y + 34), (x + 22, y + 14), (x + 30, y + 34)], fill=(230, 120, 20))
    dr.polygon([(x + 18, y + 34), (x + 22, y + 22), (x + 26, y + 34)], fill=(250, 200, 40))
    # chimney
    dr.rectangle([x + 58, y + 18, x + 70, y + 56], fill=STEEL, outline=INK, width=1)
    # sawtooth-roof factory body
    dr.polygon([(x + 6, y + 56), (x + 6, y + 36), (x + 18, y + 28), (x + 30, y + 36),
                (x + 42, y + 28), (x + 54, y + 36), (x + 58, y + 36), (x + 58, y + 56),
                (x + 78, y + 56), (x + 78, y + 72), (x + 6, y + 72)], fill=(90, 90, 90))
    dr.rectangle([x + 14, y + 58, x + 22, y + 66], fill=(250, 200, 40))
    dr.rectangle([x + 28, y + 58, x + 36, y + 66], fill=(250, 200, 40))


ICONS = {"tanker": icon_tanker, "flats": icon_flats, "warship": icon_warship,
         "badge": icon_badge, "planet": icon_planet, "factory": icon_factory}

grid_x, grid_y = 24, 430
card_w, card_h, gap = 480, 124, 12
f_label = font(LIB + "LiberationSans-Bold.ttf", 28)
for i, (label, caption, kind) in enumerate(CARDS):
    col, row = i % 2, i // 2
    x = grid_x + col * (card_w + gap)
    y = grid_y + row * (card_h + gap)
    d.rounded_rectangle([x, y, x + card_w, y + card_h], radius=8,
                        fill=CARD_BG, outline=CARD_BORDER, width=2)
    ICONS[kind](d, x + 14, y + 8, 84)
    d.text((x + 112, y + 14), label, font=f_label, fill=INK)
    lw = f_label.getlength(label)
    d.line([x + 112, y + 48, x + 112 + lw, y + 48], fill=RED, width=3)
    f_cap = fit(LIB + "LiberationSans-Regular.ttf", caption, card_w - 28, 20, minimum=15)
    d.text((x + 14, y + 96), caption, font=f_cap, fill=(40, 40, 40))

# ---------------------------------------------------------------- also today
d.text((24, 838), "ALSO TODAY", font=font(DJV + "DejaVuSans-Bold.ttf", 22), fill=INK)
d.line([24, 864, W - 24, 864], fill=INK, width=2)

ALSO = [
    ("POLAND", "Missiles confirmed Russian as NATO meets"),
    ("UN", "128 states agree to curb killer robots"),
    ("ISRAEL", "Netanyahu\u2013Eisenkot talks end without a deal"),
    ("MARKETS", "Asian shares slide as COP31 fails"),
    ("SUDAN", "Drone strikes hit Khartoum, UN facility damaged"),
    ("JAPAN", "Shuri Castle reopens seven years after fire"),
    ("USA", "Democrats win House majority, biggest since 1992"),
    ("SPORT", "UK set to host 2035 Women's World Cup"),
]
# Two columns, four rows: eight more verified stories of the day, so the
# page carries 15 stories across regions and fields instead of seven.
also_w = 480
also_size = 19
while also_size > 14:
    fb = font(LIB + "LiberationSans-Bold.ttf", also_size)
    fr = font(LIB + "LiberationSans-Regular.ttf", also_size)
    if all(fb.getlength(lead + " \u2014 ") + fr.getlength(clause) <= also_w
           for lead, clause in ALSO):
        break
    also_size -= 1
f_also_b = font(LIB + "LiberationSans-Bold.ttf", also_size)
f_also = font(LIB + "LiberationSans-Regular.ttf", also_size)
for j, (lead, clause) in enumerate(ALSO):
    col, row = j % 2, j // 2
    ax = 24 + col * 496
    ay = 876 + row * 24
    d.text((ax, ay), lead + " \u2014 ", font=f_also_b, fill=INK)
    d.text((ax + f_also_b.getlength(lead + " \u2014 "), ay), clause,
           font=f_also, fill=(40, 40, 40))

# ---------------------------------------------------------------- sport strip
d.line([24, 978, W - 24, 978], fill=INK, width=2)
f_sport_b = font(LIB + "LiberationSans-Bold.ttf", 22)
f_sport = font(LIB + "LiberationSans-Regular.ttf", 22)
sx, sy = 24, 990
d.text((sx, sy), "SPORT: ", font=f_sport_b, fill=INK)
d.text((sx + f_sport_b.getlength("SPORT: "), sy),
       "Alcaraz wins ATP Finals \u00b7 Liverpool beat Man United",
       font=f_sport, fill=MUTED)

img.save(OUT, "PNG")
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
