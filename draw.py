#!/usr/bin/env python3
"""Draw the news-image entry: a newspaper front page summing up
Monday 23 November 2026, as a 1024x1024 PNG. All text is drawn with
PIL (no AI image generator) so every word is pixel-perfect.
Facts are from live news search for 23 November 2026 only."""

import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

# rich globe illustration (right of the hero text): a proper Earth with a
# radial-gradient ocean, recognisable continents, graticule arcs, cracks,
# embers and a smoke plume — the "collapse" made visible.
cx, cy, r = 840, 280, 105
OCEAN_DARK = (14, 52, 110)       # ocean at the limb
OCEAN_LIGHT = (74, 144, 208)     # ocean near the light (upper left)
LAND_DARK = (28, 88, 38)
GRAT = (150, 195, 230)
CRACK = (22, 18, 16)
EMBER = (235, 125, 25)
EMBER_RED = (205, 45, 35)

# soft drop shadow under the globe
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([cx - r + 8, cy - r + 10, cx + r + 8, cy + r + 10], fill=(0, 0, 0, 55))
shadow = shadow.filter(ImageFilter.GaussianBlur(8))
img.paste(shadow, (0, 0), shadow)

layer = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)
gx, gy = r + 4, r + 4            # globe centre in layer coords
hx, hy = gx - 28, gy - 32        # light source (upper left)
# ocean: deep colour over the whole disc, then a radial gradient toward
# the light, so the sphere reads round instead of flat.
ld.ellipse([4, 4, 2 * r + 4, 2 * r + 4], fill=OCEAN_DARK + (255,))
for rr in range(r, 0, -2):
    t = (rr / r) ** 0.75
    col = tuple(round(OCEAN_LIGHT[i] + (OCEAN_DARK[i] - OCEAN_LIGHT[i]) * t)
                for i in range(3))
    ld.ellipse([hx - rr, hy - rr, hx + rr, hy + rr], fill=col + (255,))

# continents (points relative to the globe centre)
CONTINENTS = [
    [(-85, -55), (-60, -78), (-35, -82), (-18, -68), (-22, -48), (-38, -42),
     (-45, -28), (-58, -35), (-70, -20), (-82, -32)],            # North America
    [(-15, -88), (2, -92), (8, -80), (-6, -76)],                 # Greenland
    [(-45, -5), (-28, -12), (-12, -2), (-8, 18), (-18, 38), (-32, 48),
     (-42, 30), (-48, 10)],                                       # South America
    [(12, -38), (32, -48), (52, -40), (58, -18), (48, 8), (32, 28),
     (16, 18), (8, -12)],                                         # Africa
    [(8, -62), (24, -72), (40, -66), (36, -50), (20, -52)],      # Europe
    [(55, -60), (85, -55), (100, -35), (95, -10), (70, -15), (58, -38)],  # Asia
    [(62, 45), (82, 40), (92, 55), (75, 68), (60, 60)],          # Australia
]
for pts in CONTINENTS:
    dark = [(gx + px, gy + py) for px, py in pts]
    main = [(gx + px - 2, gy + py - 2) for px, py in pts]
    ld.polygon(dark, fill=LAND_DARK + (255,))
    ld.polygon(main, fill=LAND + (255,), outline=LAND_DARK + (255,))

# graticule: pale latitude lines + longitude ellipses
for dy in (-52, 0, 52):
    ld.line([4, gy + dy, 2 * r + 4, gy + dy], fill=GRAT + (255,), width=1)
for rx in (35, 70):
    ld.ellipse([gx - rx, 4, gx + rx, 2 * r + 4], outline=GRAT + (255,), width=1)
ld.line([gx, 4, gx, 2 * r + 4], fill=GRAT + (255,), width=1)

# cracks radiating across the globe
cracks = [
    ([(-30, -95), (-12, -60), (-28, -25), (-2, 10), (-22, 48), (-5, 90)], 6),
    ([(35, -70), (52, -38), (34, -8), (55, 22)], 5),
    ([(-75, 15), (-55, 38), (-70, 62)], 5),
]
for pts, w in cracks:
    ld.line([(gx + px, gy + py) for px, py in pts], fill=CRACK + (255,),
            width=w, joint="curve")
# embers glowing along the cracks
ld.polygon([(gx - 17, gy - 65), (gx - 7, gy - 65), (gx - 12, gy - 55)],
           fill=EMBER + (255,))
ld.polygon([(gx - 7, gy + 5), (gx + 3, gy + 5), (gx - 2, gy + 15)],
           fill=EMBER + (255,))
ld.ellipse([gx + 48, gy - 42, gx + 56, gy - 34], fill=EMBER_RED + (255,))
ld.ellipse([gx - 26, gy - 28, gx - 20, gy - 22], fill=EMBER + (255,))
ld.ellipse([gx + 40, gy + 12, gx + 46, gy + 18], fill=EMBER_RED + (255,))

mask = Image.new("L", (2 * r + 8, 2 * r + 8), 0)
md = ImageDraw.Draw(mask)
md.ellipse([4, 4, 2 * r + 4, 2 * r + 4], fill=255)
img.paste(layer, (cx - r - 4, cy - r - 4), mask)
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)

# smoke plume rising from the top of the globe, drifting up-left
smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sm = ImageDraw.Draw(smoke)
sm.ellipse([818 - 12, 186 - 12, 818 + 12, 186 + 12], fill=(150, 150, 150, 130))
sm.ellipse([795 - 13, 174 - 13, 795 + 13, 174 + 13], fill=(160, 160, 160, 105))
sm.ellipse([774 - 9, 164 - 9, 774 + 9, 164 + 9], fill=(170, 170, 170, 80))
smoke = smoke.filter(ImageFilter.GaussianBlur(3))
img.paste(smoke, (0, 0), smoke)

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
    # wake trailing behind the stern
    dr.line([x + 2, y + 68, x - 6, y + 74], fill=(140, 180, 220), width=2)
    dr.line([x + 6, y + 72, x - 2, y + 78], fill=(140, 180, 220), width=2)


def icon_flats(dr, x, y, s):
    # apartment block with a damaged top-right corner
    dr.rectangle([x + 10, y + 14, x + 66, y + 68], fill=(150, 150, 150), outline=INK, width=2)
    for wx in (18, 34, 50):
        for wy in (22, 38, 54):
            dr.rectangle([x + wx, y + wy, x + wx + 8, y + wy + 8], fill=(60, 60, 60))
    # broken corner: jagged dark bite out of the top right
    dr.polygon([(x + 66, y + 14), (x + 66, y + 34), (x + 54, y + 26),
                (x + 58, y + 14)], fill=(40, 40, 40))
    # jagged notch broken out of the top edge
    dr.polygon([(x + 28, y + 14), (x + 34, y + 22), (x + 40, y + 14)], fill=CARD_BG)
    dr.polygon([(x + 50, y + 68), (x + 58, y + 76), (x + 66, y + 68),
                (x + 74, y + 76), (x + 82, y + 68)], fill=(100, 100, 100))
    # small flame at the damage
    dr.polygon([(x + 58, y + 14), (x + 62, y + 4), (x + 66, y + 14)], fill=(230, 120, 20))
    # smoke column rising from the damage
    dr.ellipse([x + 57, y - 2, x + 69, y + 10], fill=(150, 150, 150))
    dr.ellipse([x + 61, y - 6, x + 71, y + 4], fill=(170, 170, 170))


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
    # wake trailing behind the stern
    dr.line([x + 2, y + 64, x - 4, y + 70], fill=(140, 180, 220), width=2)
    dr.line([x + 6, y + 68, x + 0, y + 74], fill=(140, 180, 220), width=2)
    # red light on the mast top
    dr.ellipse([x + 39, y + 10, x + 43, y + 14], fill=RED)


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
    # chain link joining the two rings
    dr.line([x + 68, y + 68, x + 74, y + 72], fill=STEEL, width=3)


def icon_planet(dr, x, y, s):
    # Mercury with a ring and a tiny spacecraft
    cxp, cyp, rp = x + 40, y + 42, 26
    dr.ellipse([cxp - rp - 26, cyp - 10, cxp + rp + 26, cyp + 10],
               outline=(150, 150, 150), width=3)
    dr.ellipse([cxp - rp, cyp - rp, cxp + rp, cyp + rp], fill=(169, 144, 126), outline=INK, width=2)
    dr.ellipse([cxp - 14, cyp - 8, cxp - 6, cyp], fill=(120, 100, 88))
    dr.ellipse([cxp + 4, cyp + 6, cxp + 12, cyp + 14], fill=(120, 100, 88))
    dr.ellipse([cxp + 8, cyp - 14, cxp + 14, cyp - 8], fill=(120, 100, 88))
    dr.ellipse([cxp - 4, cyp + 14, cxp + 4, cyp + 20], fill=(120, 100, 88))
    # small gold sparkle near the trail
    dr.ellipse([x + 58, y + 20, x + 62, y + 24], fill=GOLD)
    # spacecraft dot with trail
    dr.line([x + 66, y + 12, x + 76, y + 6], fill=INK, width=2)
    dr.polygon([(x + 76, y + 2), (x + 84, y + 8), (x + 76, y + 12)], fill=RED)


def icon_factory(dr, x, y, s):
    # smoke from the taller chimney
    dr.ellipse([x + 54, y - 2, x + 68, y + 12], fill=(150, 150, 150))
    dr.ellipse([x + 58, y - 6, x + 70, y + 4], fill=(170, 170, 170))
    dr.polygon([(x + 14, y + 34), (x + 22, y + 14), (x + 30, y + 34)], fill=(230, 120, 20))
    dr.polygon([(x + 18, y + 34), (x + 22, y + 22), (x + 26, y + 34)], fill=(250, 200, 40))
    # chimney (taller than v2)
    dr.rectangle([x + 58, y + 10, x + 70, y + 56], fill=STEEL, outline=INK, width=1)
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
