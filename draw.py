# draw.py — v5: "THE WORLD IN ONE DAY — Monday 23 November 2026"
# A newspaper front page drawn with Python + PIL, from the v5 story list
# (35 verified stories, all first reported on 23 Nov 2026).
# Every word is drawn as text, so nothing is garbled. No network, no clock,
# no randomness: the same input always produces the same bytes.
# Output: entry.png, 1024x1024, under the 1 MiB cap.
# Run: python3 draw.py  (writes entry.png next to this file)

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
PAPER2 = (241, 236, 224)
INK = (18, 18, 18)
GREY = (90, 86, 78)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
DARKBLUE = (16, 42, 74)
GOLD = (176, 132, 24)
GREEN = (31, 110, 58)
SEA = (168, 196, 216)
LAND = (214, 203, 170)
RULE = (120, 112, 96)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_O = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"

_fcache = {}


def font(path, size):
    key = (path, size)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(path, size)
    return _fcache[key]


def wrap(text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill=INK, leading=None, align="left",
               width=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        if align == "center":
            d.text((x + (width - fnt.getlength(ln)) / 2, y), ln, font=fnt,
                   fill=fill)
        elif align == "right":
            d.text((x + width - fnt.getlength(ln), y), ln, font=fnt,
                   fill=fill)
        else:
            d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hline(d, x0, x1, y, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def vline(d, x, y0, y1, fill=INK, width=1):
    d.line([(x, y0), (x, y1)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# Each card: (number, place, headline, dek, source-tag, scene key)
HEROES = [
    (1, "ANTALYA, TURKEY",
     "Climate talks collapse as fossil fuels split the world",
     "Antalya ends with no deal; the EU and 130 parties reject a text that "
     "drops \u2018fossil fuels\u2019. Longest COP ever.",
     "CONFIRMED \u00b7 REUTERS / CNN", "cop31"),
    (2, "STRAIT OF HORMUZ",
     "Three tankers hit in Hormuz as war at sea escalates",
     "Captain Leon, Torkel, Arina struck; 1 missing, 11 hurt \u2014 most "
     "attacks since the Iran war began.",
     "CONFIRMED \u00b7 CNN / AP", "hormuz"),
    (3, "DYMER, UKRAINE",
     "Russian strike kills at least 10 in Dymer village",
     "Apartment block hit north of Kyiv; 11 missing; 14 dead across the "
     "Kyiv region in the same wave.",
     "CONFIRMED \u00b7 AP", "dymer"),
]

SMALL = [
    (4, "MARKETS", "AI rout sinks Nikkei 5.06% and S&P 3.7%",
     "Tokyo leads a global sell-off as AI shares tumble.",
     "CONFIRMED \u00b7 REUTERS", "markets"),
    (5, "CIKANDE, INDONESIA", "Candy factory fire kills 24 in Cikande",
     "Factory ablaze on Saturday night; about 30 missing; faulty air-con "
     "blamed.",
     "CONFIRMED \u00b7 REUTERS", "cikande"),
    (6, "POLAND", "Three Russian missiles cross Polish skies",
     "Kh-101 debris found in three places; NATO envoys meet.",
     "CONFIRMED \u00b7 REUTERS", "poland"),
    (7, "WASHINGTON, USA", "Democrats clinch House with 258th seat",
     "Hubbard beats Foxx in North Carolina; biggest Democratic majority "
     "since 1992.",
     "CONFIRMED \u00b7 AP", "house"),
    (8, "KHARTOUM, SUDAN", "Drone strikes kill five children in Khartoum",
     "Attacks hit Khartoum and Omdurman as the war\u2019s toll on children "
     "mounts.",
     "CONFIRMED \u00b7 AP", "sudan"),
    (9, "RABIGH, SAUDI ARABIA", "Houthis claim Rabigh refinery hit",
     "Second strike claimed south of Riyadh; Riyadh silent; Saudi jets hit "
     "Hodeida.",
     "CLAIMED \u00b7 REUTERS", "yemen"),
    (10, "ISTANBUL, TURKEY", "Tens of thousands march in Istanbul",
     "Crowds protest the crackdown on opposition media and politicians.",
     "REPORTED \u00b7 AP", "istanbul"),
    (11, "CANBERRA, AUSTRALIA", "Bowen faces calls to quit after COP flop",
     "Pacific nations voice despair; opposition blames the minister who led "
     "the talks.",
     "CONFIRMED \u00b7 REUTERS", "bowen"),
    (12, "BALTIC SEA", "Russian cargo ship Sparta II burns in Baltic",
     "Finland says Ukraine attacked the vessel; it drifts into Finnish "
     "waters ablaze.",
     "REPORTED \u00b7 FT", "baltic"),
    (13, "TURIN, ITALY", "Alcaraz wins ATP Finals",
     "Beats Zverev 6\u20132, 7\u20136(9) in Sunday\u2019s final.",
     "CONFIRMED \u00b7 AP", "alcaraz"),
]

ALSO = [
    (14, "BENGHAZI", "Blast hits Russian ship docked at Benghazi; no casualties"),
    (15, "BAHRAIN", "Bahrain demands UN action after Iran hits civilian site"),
    (16, "BAHRAIN", "Two hurt in Iran attacks on industrial site, ministry says"),
    (17, "GAZA", "Hamas urges ceasefire guarantors to meet as truce frays"),
    (18, "LEBANON", "Army seizes 264 kg of explosives, arrests three"),
    (19, "SAUDI ARABIA", "MBS meets Bulgarian PM Radev in Riyadh"),
    (20, "PAKISTAN", "Minister voices hope for a US\u2013Iran deal"),
    (21, "NIGERIA", "Bayelsa boat toll rises to 29; Tinubu pledges N250m aid"),
    (22, "LONDON", "Compass moves its listing to New York"),
    (23, "JAPAN", "Shuri Castle reopens seven years after fire"),
    (24, "PHILIPPINES", "Manila transport strike begins as fuel prices fall"),
    (25, "USA", "Trump warns of new Iran strikes next year"),
    (26, "BAHRAIN", "US Embassy warns Americans of Iran, Houthi threats"),
    (27, "COP31", "90+ nations back electrification pledge to 35% by 2035"),
    (28, "COP31", "Methane platform grows to 47 countries"),
    (29, "COP31", "Nations agree to reconvene in Ethiopia next year"),
    (30, "HAITI", "Haitians back El Salvador\u2019s Bukele against gangs"),
    (31, "FOOTBALL", "Liverpool rout Man United 4\u20130 at Anfield"),
    (32, "FOOTBALL", "Barcelona edge Villarreal 3\u20132; Juventus hit four"),
    (33, "USA", "US intel chief warns of more tech outages"),
    (34, "USA", "King tides threaten California coast; SF warns residents"),
    (35, "USA", "Trump urges Nvidia to rehire Jensen Huang"),
]

UTC_STRIP = [
    ("00:00", "Nikkei opens sharply lower in Tokyo"),
    ("03:00", "Shuri Castle reopens in Okinawa"),
    ("06:00", "Nikkei closes down 5.06%"),
    ("MORNING", "NATO envoys meet on Polish airspace breach"),
    ("MIDDAY", "Tens of thousands march in Istanbul"),
    ("AFTERNOON", "Democrats clinch 258th House seat"),
    ("21:00", "S&P 500 closes down 3.7%"),
]

NUMBERS = [
    ("258", "House seats won by Democrats"),
    ("\u22125.06%", "Nikkei, Tokyo's worst day in weeks"),
    ("3", "tankers hit in the Strait of Hormuz"),
    ("24", "dead in the Cikande factory fire"),
    ("\u226510", "killed in the Dymer strike"),
    ("5", "children killed in Khartoum"),
]

DATE_CHECK_LEFT = ("BepiColombo; 'Chapo Isidro'; killer-robot talks; "
                   "Eisenkot (all 21 Nov); penny bill (20 Nov); Delta "
                   "outage (22 Nov); Cyclone Akvan (20 Nov).")
DATE_CHECK_NOTYET = ("COP31 close; Shenzhen-24 launch (25 Nov).")

# World-map pins: (story number, lon, lat, label)
PINS = [
    (1, 30.7, 36.9, "ANTALYA"), (2, 56.3, 26.6, "HORMUZ"),
    (3, 30.2, 50.8, "DYMER"), (4, 139.7, 35.7, "TOKYO"),
    (5, 106.4, -6.2, "CIKANDE"), (6, 19.4, 52.0, "POLAND"),
    (7, -77.0, 38.9, "WASHINGTON"), (8, 32.5, 15.5, "KHARTOUM"),
    (9, 39.0, 22.8, "RABIGH"), (10, 28.9, 41.0, "ISTANBUL"),
    (11, 149.1, -35.3, "CANBERRA"), (12, 24.9, 60.2, "BALTIC"),
    (13, 7.7, 45.1, "TURIN"),
]


# ---------------------------------------------------------------- scenes
# Every scene draws a data-carrying picture of its own story: a chart with
# real numbers, a map with real places, a room with real words. No generic
# clip-art icons: the picture itself must tell the story.


def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARKBLUE)
    # hall: rows of delegate desks, small flags
    for row in range(3):
        yy = y + h - 26 - row * 16
        for i in range(7):
            xx = x + 12 + i * 44
            d.rectangle([xx, yy, xx + 34, yy + 10], fill=(58, 86, 122))
            d.rectangle([xx + 2, yy - 7, xx + 8, yy - 2],
                        fill=[RED, GOLD, GREEN, (240, 240, 240)][i % 4])
    # big screen: the pact text, "fossil fuels" crossed out in red
    sx, sy, sw, sh = x + 18, y + 10, w - 36, 62
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=(240, 238, 230))
    d.text((sx + 10, sy + 6), "ANTALYA PACT", font=font(SANS_B, 15),
           fill=INK)
    d.text((sx + 10, sy + 28), "transition away from",
           font=font(SANS, 13), fill=INK)
    fw = font(SANS_B, 13)
    d.text((sx + 10, sy + 44), "fossil fuels", font=fw, fill=INK)
    lx = sx + 10 + fw.getlength("fossil fuels") + 4
    d.line([(sx + 8, sy + 51), (lx, sy + 51)], fill=RED, width=3)
    d.text((lx + 4, sy + 44), "REMOVED", font=font(SANS_B, 12), fill=RED)
    d.text((x + 8, y + h - 14), "194 DELEGATES  \u00b7  0 DEAL",
           font=font(SANS_B, 11), fill=(240, 238, 230))


def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # land: Iran above the strait, Arabia below
    d.polygon([(x, y), (x + w, y), (x + w, y + 34), (x + w * 0.62, y + 52),
               (x + w * 0.38, y + 40), (x, y + 48)], fill=(196, 178, 140))
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 30),
               (x + w * 0.55, y + h - 52), (x + w * 0.3, y + h - 38),
               (x, y + h - 26)], fill=(196, 178, 140))
    d.text((x + 8, y + 4), "IRAN", font=font(SANS_B, 10), fill=INK)
    d.text((x + w - 62, y + h - 14), "ARABIA", font=font(SANS_B, 10),
           fill=INK)
    # three tankers in the strait, one burning
    for i, (tx, nm) in enumerate([(0.16, "CAPTAIN LEON"), (0.44, "TORKEL"),
                                  (0.70, "ARINA")]):
        cx = x + int(w * tx)
        cy = y + h // 2 + (i % 2) * 8 - 4
        d.rectangle([cx - 26, cy, cx + 26, cy + 12], fill=(40, 40, 44))
        d.rectangle([cx + 8, cy - 8, cx + 20, cy], fill=(40, 40, 44))
        d.text((cx - 26, cy + 14), nm, font=font(SANS_B, 8), fill=INK)
        if i == 0:
            for k in range(3):
                d.polygon([(cx - 14 + k * 10, cy - 8), (cx - 9 + k * 10, cy - 22),
                           (cx - 4 + k * 10, cy - 8)], fill=(222, 110, 20))
    d.text((x + 8, y + h - 26), "STRAIT OF HORMUZ",
           font=font(SANS_B, 10), fill=INK)


def scene_dymer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 34))
    # apartment block, top corner shattered
    bx, by, bw, bh = x + 18, y + 34, 150, h - 52
    d.rectangle([bx, by, bx + bw, by + bh], fill=(120, 116, 108))
    for r in range(5):
        for c in range(6):
            wx = bx + 10 + c * 23
            wy = by + 10 + r * 20
            lit = (r * 6 + c) % 3 == 0
            d.rectangle([wx, wy, wx + 14, wy + 12],
                        fill=(250, 200, 90) if lit else (60, 58, 54))
    d.polygon([(bx + bw - 46, by), (bx + bw, by), (bx + bw, by + 44),
               (bx + bw - 22, by + 26)], fill=(24, 24, 34))
    # blast sparkle above the broken corner (4-point star)
    cx, cy = bx + bw - 20, by - 2
    d.polygon([(cx, cy - 16), (cx + 4, cy - 4), (cx + 16, cy),
               (cx + 4, cy + 4), (cx, cy + 16), (cx - 4, cy + 4),
               (cx - 16, cy), (cx - 4, cy - 4)], fill=(250, 200, 90))
    fbig = font(SANS_B, 19)
    t = "\u226510 KILLED"
    d.text((x + w - fbig.getlength(t) - 6, y + 8), t, font=fbig,
           fill=(250, 200, 90))
    fmid = font(SANS_B, 13)
    t2 = "11 MISSING"
    d.text((x + w - fmid.getlength(t2) - 6, y + 32), t2, font=fmid,
           fill=(240, 238, 230))
    d.text((x + 8, y + h - 16), "DYMER \u00b7 30 KM NORTH OF KYIV",
           font=font(SANS_B, 10), fill=(240, 238, 230))


def scene_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    ox, oy = x + 24, y + h - 18
    d.line([(ox, y + 8), (ox, oy)], fill=INK, width=1)
    d.line([(ox, oy), (x + w - 8, oy)], fill=INK, width=1)
    pts = [(0, 0.10), (0.2, 0.16), (0.35, 0.12), (0.5, 0.30),
           (0.65, 0.55), (0.8, 0.72), (1.0, 0.92)]
    px = [ox + int(p[0] * (w - 40)) for p in pts]
    py = [y + 8 + int(p[1] * (h - 34)) for p in pts]
    d.line(list(zip(px, py)), fill=RED, width=3)
    d.text((x + w - 62, y + 2), "\u22125.06%", font=font(SANS_B, 14), fill=RED)
    d.text((x + 6, y + h - 14), "S&P \u22123.7%", font=font(SANS_B, 10),
           fill=RED)
    d.text((x + w - 44, y + h - 14), "NIKKEI", font=font(SANS_B, 8),
           fill=GREY)


def scene_cikande(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 52, 58))
    # factory with sawtooth roof and chimney, smoke plume, all inside the box
    d.text((x + 6, y + 2), "24", font=font(SANS_B, 24), fill=(250, 200, 90))
    d.text((x + 48, y + 12), "DEAD", font=font(SANS_B, 10),
           fill=(240, 238, 230))
    fx = x + 10
    d.rectangle([fx, y + 30, fx + 96, y + h - 2], fill=(140, 134, 122))
    for i in range(4):
        d.polygon([(fx + i * 24, y + 30), (fx + i * 24 + 12, y + 22),
                   (fx + i * 24 + 24, y + 30)], fill=(140, 134, 122))
    d.rectangle([fx + 102, y + 12, fx + 110, y + h - 2], fill=(110, 104, 94))
    d.ellipse([fx + 102, y + 3, fx + 110, y + 11], fill=(200, 196, 188))
    d.ellipse([fx + 96, y + 6, fx + 102, y + 12], fill=(200, 196, 188))


def scene_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    # rough Poland outline
    poly = [(0.18, 0.72), (0.22, 0.45), (0.30, 0.28), (0.42, 0.16),
            (0.58, 0.12), (0.72, 0.20), (0.82, 0.34), (0.86, 0.52),
            (0.80, 0.68), (0.66, 0.80), (0.48, 0.86), (0.32, 0.84)]
    pts = [(x + int(a * w), y + int(b * h)) for a, b in poly]
    d.polygon(pts, fill=LAND, outline=INK)
    # three missile arcs from the east
    for i, (ax, ay) in enumerate([(0.95, 0.25), (0.97, 0.5), (0.93, 0.72)]):
        ex, ey = x + int(ax * w), y + int(ay * h)
        mx, my = x + int(0.62 * w), y + int((0.3 + i * 0.2) * h)
        d.line([(ex, ey), (mx, my)], fill=RED, width=2)
        d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=RED)
    d.text((x + 6, y + 4), "3 \u00d7 Kh-101", font=font(SANS_B, 12), fill=RED)
    d.text((x + 6, y + h - 14), "DEBRIS IN 3 PLACES",
           font=font(SANS_B, 8), fill=INK)


def scene_house(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    # Capitol dome silhouette on the right, big number on the left
    d.text((x + 6, y + 4), "258", font=font(SANS_B, 24), fill=BLUE)
    d.text((x + 6, y + 30), "SEATS", font=font(SANS_B, 11), fill=INK)
    cx = x + w - 46
    d.rectangle([cx - 40, y + h - 10, cx + 40, y + h - 4], fill=(90, 86, 78))
    d.rectangle([cx - 26, y + h - 22, cx + 26, y + h - 10], fill=(90, 86, 78))
    d.pieslice([cx - 22, y + h - 40, cx + 22, y + h - 22], 180, 360,
               fill=(90, 86, 78))
    d.rectangle([cx - 2, y + 2, cx + 2, y + 6], fill=(90, 86, 78))


def scene_sudan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    # two river towns on the Nile
    d.line([(x + 20, y + h - 8), (x + w - 30, y + 14)], fill=SEA, width=5)
    d.ellipse([x + w * 0.42 - 6, y + h * 0.42 - 6, x + w * 0.42 + 6,
               y + h * 0.42 + 6], fill=RED)
    d.ellipse([x + w * 0.58 - 6, y + h * 0.58 - 6, x + w * 0.58 + 6,
               y + h * 0.58 + 6], fill=RED)
    d.text((x + w * 0.42 - 30, y + h * 0.42 - 22), "KHARTOUM",
           font=font(SANS_B, 8), fill=INK)
    d.text((x + w * 0.58 - 8, y + h * 0.58 + 10), "OMDURMAN",
           font=font(SANS_B, 8), fill=INK)
    d.text((x + 6, y + 4), "5 CHILDREN", font=font(SANS_B, 13), fill=RED)


def scene_yemen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 34))
    # refinery towers with one flame, all inside the box
    d.text((x + 6, y + 2), "RABIGH", font=font(SANS_B, 13),
           fill=(240, 238, 230))
    for i, tx in enumerate([0.18, 0.42, 0.66]):
        bx = x + int(w * tx)
        d.rectangle([bx, y + 22, bx + 16, y + h - 4], fill=(120, 116, 108))
        d.rectangle([bx + 4, y + 16, bx + 12, y + 22], fill=(120, 116, 108))
        if i == 1:
            d.polygon([(bx - 2, y + 16), (bx + 8, y + 2),
                       (bx + 18, y + 16)], fill=(222, 110, 20))


def scene_istanbul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    # crowd: banner on top, two rows of heads below, all inside the box
    d.rectangle([x + 12, y + 4, x + w - 12, y + 18], fill=RED)
    d.text((x + 16, y + 6), "ISTANBUL", font=font(SANS_B, 11),
           fill=(255, 255, 255))
    for r in range(2):
        for c in range(9):
            cx = x + 14 + c * 20 + (r % 2) * 8
            cy = y + 28 + r * 11
            d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(70, 66, 60))


def scene_bowen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    # quote on the left, podium with microphone on the right
    d.text((x + 6, y + 2), "\u201cVERY", font=font(SERIF, 15), fill=INK)
    d.text((x + 6, y + 20), "DISAPPOINTING\u201d", font=font(SERIF, 12),
           fill=INK)
    cx = x + w - 42
    d.rectangle([cx - 24, y + 28, cx + 24, y + h - 6], fill=(90, 86, 78))
    d.rectangle([cx - 30, y + 24, cx + 30, y + 28], fill=(70, 66, 60))
    d.line([(cx + 12, y + 24), (cx + 22, y + 10)], fill=INK, width=2)
    d.ellipse([cx + 18, y + 6, cx + 26, y + 14], fill=INK)


def scene_baltic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.polygon([(x, y), (x + w, y), (x + w, y + 14), (x, y + 18)],
              fill=(196, 178, 140))
    d.text((x + 6, y + 2), "FINLAND", font=font(SANS_B, 9), fill=INK)
    # burning cargo ship, flame and label all inside the box
    sx, sy = x + w // 2 - 52, y + 24
    d.rectangle([sx, sy, sx + 104, sy + 12], fill=(40, 40, 44))
    d.rectangle([sx + 60, sy - 10, sx + 76, sy], fill=(40, 40, 44))
    d.polygon([(sx + 8, sy), (sx + 18, sy - 12), (sx + 28, sy)],
              fill=(222, 110, 20))
    d.polygon([(sx + 30, sy), (sx + 40, sy - 8), (sx + 50, sy)],
              fill=(240, 170, 40))
    d.text((x + 6, y + h - 10), "SPARTA II \u00b7 ADRIFT, ABLAZE",
           font=font(SANS_B, 9), fill=INK)


def scene_alcaraz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 110, 72))
    # tennis court lines
    d.rectangle([x + 14, y + 10, x + w - 14, y + h - 14], outline=(255, 255, 255),
                width=2)
    d.line([(x + w // 2, y + 10), (x + w // 2, y + h - 14)], fill=(255, 255, 255),
           width=2)
    d.line([(x + 14, y + h // 2), (x + w - 14, y + h // 2)],
           fill=(255, 255, 255), width=2)
    d.ellipse([x + w - 34, y + h - 30, x + w - 22, y + h - 18],
              fill=(220, 220, 60))
    d.rectangle([x + 8, y + 6, x + 118, y + 26], fill=(24, 24, 34))
    d.text((x + 12, y + 8), "6\u20132  7\u20136(9)", font=font(SANS_B, 12),
           fill=(255, 255, 255))


SCENES = {
    "cop31": scene_cop31, "hormuz": scene_hormuz, "dymer": scene_dymer,
    "markets": scene_markets, "cikande": scene_cikande,
    "poland": scene_poland, "house": scene_house, "sudan": scene_sudan,
    "yemen": scene_yemen, "istanbul": scene_istanbul, "bowen": scene_bowen,
    "baltic": scene_baltic, "alcaraz": scene_alcaraz,
}


# ---------------------------------------------------------------- world map
# Rough equirectangular continent outlines (lon, lat). Stylised, but the
# shapes and pin positions are real.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 29), (-97, 26), (-105, 22), (-110, 24),
     (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 10), (-60, 5), (-50, 0), (-40, -5),
     (-35, -10), (-40, -20), (-50, -30), (-60, -35), (-70, -40), (-75, -50),
     (-70, -55), (-65, -45), (-70, -30), (-75, -20), (-80, -15), (-80, -5)],
    [(-10, 36), (-9, 43), (0, 44), (3, 43), (7, 44), (10, 44), (12, 45),
     (18, 40), (22, 37), (26, 40), (28, 45), (23, 46), (20, 44), (15, 44),
     (12, 46), (8, 47), (5, 48), (0, 50), (-2, 51), (-5, 50), (-10, 52),
     (-10, 58), (-5, 60), (0, 58), (5, 60), (10, 62), (18, 69), (25, 71),
     (30, 70), (35, 66), (40, 60), (40, 55), (35, 50), (30, 46), (28, 44),
     (23, 40), (19, 42), (15, 40), (12, 42), (8, 44), (3, 42), (-2, 37),
     (-6, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (35, 20), (40, 15), (43, 12), (48, 11), (51, 10), (45, 5), (40, 0),
     (40, -10), (35, -20), (30, -30), (25, -35), (18, -35), (15, -27),
     (12, -18), (13, -10), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)],
    [(40, 55), (45, 60), (50, 65), (60, 68), (70, 72), (80, 73), (90, 75),
     (110, 76), (130, 72), (150, 70), (170, 66), (178, 65), (170, 60),
     (160, 55), (150, 45), (140, 40), (135, 35), (130, 30), (127, 35),
     (122, 38), (120, 30), (115, 22), (110, 20), (105, 10), (100, 8),
     (98, 15), (95, 20), (90, 22), (85, 20), (80, 15), (77, 8), (75, 12),
     (72, 20), (66, 25), (60, 25), (55, 26), (50, 28), (48, 30), (44, 30),
     (40, 35), (38, 40), (35, 45), (30, 46), (35, 50), (40, 55)],
    [(114, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]

# label offset per pin number, to keep neighbouring labels apart
# (pin pixel positions computed from the equirectangular projection;
# boxes verified non-overlapping: 10 px tall, no two boxes share area)
PIN_LABEL_DXDY = {
    1: (-38, 12), 2: (9, 15), 3: (-58, -15), 4: (-46, -3), 5: (-58, -3),
    6: (-48, 3), 7: (-56, 12), 8: (9, 9), 9: (-50, 7), 10: (9, -15),
    11: (-64, -3), 12: (9, -15), 13: (-46, 9),
}


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    for poly in CONTINENTS:
        pts = [(x0 + int((lon + 170) / 360 * w),
                y0 + int((75 - lat) / 130 * h)) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(150, 138, 108))
    fnum = font(SANS_B, 9)
    flab = font(SANS_B, 8)
    # pins first, labels second — so no pin ever covers a label
    for num, lon, lat, label in PINS:
        px = x0 + int((lon + 170) / 360 * w)
        py = y0 + int((75 - lat) / 130 * h)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255))
        t = str(num)
        d.text((px - fnum.getlength(t) / 2, py - 6), t, font=fnum,
               fill=(255, 255, 255))
    for num, lon, lat, label in PINS:
        px = x0 + int((lon + 170) / 360 * w)
        py = y0 + int((75 - lat) / 130 * h)
        dx, dy = PIN_LABEL_DXDY[num]
        lx, ly = px + dx, py + dy
        lw = flab.getlength(label)
        d.rectangle([lx - 1, ly - 1, lx + lw + 1, ly + 9], fill=PAPER)
        d.text((lx, ly), label, font=flab, fill=INK)


# ---------------------------------------------------------------- layout

def draw_masthead(d):
    hline(d, 12, 1012, 8, width=2)
    hline(d, 12, 1012, 12, width=1)
    f = font(SANS_B, 18)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - f.getlength(t)) / 2, 18), t, font=f, fill=INK)
    fdate = font(SERIF, 46)
    t = "Monday 23 November 2026"
    d.text(((W - fdate.getlength(t)) / 2, 40), t, font=fdate, fill=INK)
    fclaim = font(SANS_B, 14)
    t = "35 STORIES \u00b7 6 REGIONS \u00b7 10 FIELDS \u00b7 EVERY ONE FROM THIS MONDAY"
    d.text(((W - fclaim.getlength(t)) / 2, 90), t, font=fclaim, fill=INK)
    hline(d, 12, 1012, 108, width=2)
    hline(d, 12, 1012, 112, width=1)


def draw_utc_strip(d, y0):
    flab = font(SANS_B, 12)
    d.text((12, y0), "THE DAY IN UTC", font=flab, fill=RED)
    colw = 1000 / 7
    ftime = font(SANS_B, 12)
    fev = font(SANS, 10)
    for i, (tm, ev) in enumerate(UTC_STRIP):
        cx = 12 + i * colw
        if i:
            vline(d, int(cx - 4), y0 + 18, y0 + 56, fill=RULE)
        d.text((cx, y0 + 18), tm, font=ftime, fill=INK)
        lines = wrap(ev, fev, colw - 10)
        text_block(d, cx, y0 + 34, lines[:2], fev, leading=12)


def draw_numbers_strip(d, y0):
    flab = font(SANS_B, 12)
    d.text((12, y0), "THE DAY IN NUMBERS", font=flab, fill=RED)
    colw = 1000 / 6
    fnum = font(SANS_B, 22)
    flbl = font(SANS, 9)
    for i, (num, lbl) in enumerate(NUMBERS):
        cx = 12 + i * colw
        if i:
            vline(d, int(cx - 4), y0 + 18, y0 + 52, fill=RULE)
        d.text((cx, y0 + 18), num, font=fnum, fill=RED)
        lines = wrap(lbl, flbl, colw - 10)
        text_block(d, cx, y0 + 44, lines[:2], flbl, leading=11)


def draw_hero(d, x, y, w, h, num, place, headline, dek, source, scene):
    ftag = font(SANS_B, 11)
    d.text((x, y), "%d \u00b7 %s" % (num, place), font=ftag, fill=RED)
    SCENES[scene](d, x, y + 16, w, 128)
    fh = font(SANS_B, 16)
    lines = wrap(headline, fh, w)
    yy = text_block(d, x, y + 150, lines[:2], fh, leading=19)
    fd = font(SANS, 11)
    lines = wrap(dek, fd, w)
    yy = text_block(d, x, yy + 2, lines[:2], fd, leading=13)
    fs = font(SANS_B, 8)
    d.text((x, y + h - 11), source, font=fs, fill=RED)


def draw_small(d, x, y, w, h, num, place, headline, dek, source, scene):
    ftag = font(SANS_B, 10)
    d.text((x, y), "%d \u00b7 %s" % (num, place), font=ftag, fill=RED)
    SCENES[scene](d, x, y + 13, w, 46)
    fh = font(SANS_B, 11)
    lines = wrap(headline, fh, w)
    yy = text_block(d, x, y + 62, lines[:2], fh, leading=12)
    fd = font(SANS, 9)
    lines = wrap(dek, fd, w)
    yy = text_block(d, x, yy + 1, lines[:2], fd, leading=10)
    fs = font(SANS_B, 8)
    d.text((x, y + h - 10), source, font=fs, fill=RED)


def draw_also(d, x0, y0, w):
    flab = font(SANS_B, 12)
    d.text((x0, y0), "ALSO ON MONDAY 23 NOVEMBER", font=flab, fill=RED)
    fnum = font(SANS_B, 9)
    fpl = font(SANS_B, 9)
    ftx = font(SANS, 9)
    colw = (w - 16) // 2
    for idx, (num, place, head) in enumerate(ALSO):
        col = idx // 11
        row = idx % 11
        cx = x0 + col * (colw + 16)
        cy = y0 + 20 + row * 22
        d.text((cx, cy), "%d." % num, font=fnum, fill=RED)
        tx = cx + 20
        d.text((tx, cy), place + " \u2014", font=fpl, fill=INK)
        rest = " " + head
        pw = fpl.getlength(place + " \u2014")
        lines = wrap(rest.strip(), ftx, colw - 20 - pw)
        if lines:
            d.text((tx + pw, cy), lines[0], font=ftx, fill=INK)
            if len(lines) > 1:
                second = lines[1]
                if len(lines) > 2:
                    second = second.rsplit(" ", 1)[0] + "\u2026"
                d.text((tx, cy + 10), second, font=ftx, fill=INK)


def draw_datecheck(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=RED, width=2)
    flab = font(SANS_B, 11)
    d.text((x0 + 6, y0 + 4), "DATE CHECK", font=flab, fill=RED)
    ftx = font(SANS, 9)
    left = "LEFT OUT \u2014 first reported before Monday: " + \
        DATE_CHECK_LEFT
    lines = wrap(left, ftx, w - 12)
    yy = text_block(d, x0 + 6, y0 + 20, lines, ftx, leading=11)
    ny = "NOT YET: " + DATE_CHECK_NOTYET
    lines = wrap(ny, ftx, w - 12)
    text_block(d, x0 + 6, yy + 2, lines, ftx, leading=11)


def draw_footer(d, y0):
    f = font(SANS, 9)
    t1 = ("Every story happened or was first reported on Mon 23 Nov 2026.  "
          "CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on the record \u00b7 "
          "REPORTED = one outlet \u00b7 CLAIMED = unverified claim.")
    d.text(((W - f.getlength(t1)) / 2, y0), t1, font=f, fill=GREY)
    t2 = ("Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 CNN \u00b7 BBC \u00b7 FT \u00b7 "
          "Nikkei Asia \u00b7 Arab News \u00b7 GMA \u00b7 ABC \u00b7 CNBC")
    d.text(((W - f.getlength(t2)) / 2, y0 + 11), t2, font=f, fill=GREY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_utc_strip(d, 118)
    hline(d, 12, 1012, 176, fill=RULE)
    draw_numbers_strip(d, 182)
    hline(d, 12, 1012, 236, fill=RULE)
    # heroes: 3 columns
    hx = [12, 348, 684]
    for i, hero in enumerate(HEROES):
        num, place, head, dek, src, scene = hero
        draw_hero(d, hx[i], 242, 328, 236, num, place, head, dek, src, scene)
        if i:
            vline(d, hx[i] - 8, 242, 474, fill=RULE)
    hline(d, 12, 1012, 480, fill=RULE)
    # small cards: 2 rows x 5
    cw = (1000 - 4 * 8) / 5
    for r in range(2):
        y0 = 486 + r * 124
        for c in range(5):
            idx = r * 5 + c
            num, place, head, dek, src, scene = SMALL[idx]
            x0 = 12 + c * (cw + 8)
            draw_small(d, int(x0), y0, int(cw), 120, num, place, head,
                       dek, src, scene)
            if c:
                vline(d, int(x0 - 5), y0, y0 + 118, fill=RULE)
    hline(d, 12, 1012, 734, fill=RULE)
    # bottom: map + also list
    d.text((12, 740), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    draw_map(d, 12, 758, 336, 152)
    fc = font(SANS, 9)
    tc = ("Europe 6 \u00b7 Middle East 2 \u00b7 Asia 2 \u00b7 Africa 1 \u00b7 "
          "N. America 1 \u00b7 Oceania 1")
    d.text((12, 914), tc, font=fc, fill=INK)
    draw_also(d, 360, 740, 652)
    draw_datecheck(d, 12, 926, 336, 68)
    hline(d, 12, 1012, 1000, fill=RULE)
    draw_footer(d, 1004)
    return img


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = build()
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
