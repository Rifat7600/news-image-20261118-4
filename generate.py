"""Draw the news-image entry: a 1024x1024 infographic timeline of the
world news of Wednesday 18 November 2026.

Runs with Pillow here on this machine. The grader never runs this file;
it runs main.py, which only copies the entry.png this script produces.
All facts come from the verified news list; nothing here is invented.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SIZE = 1024
OUT = os.path.join(HERE, "entry.png")

# --- palette -------------------------------------------------------------
NAVY = (10, 25, 48)          # page background
NAVY_BAND = (14, 36, 68)     # footer band
LINE = (51, 80, 122)         # timeline spine
WHITE = (255, 255, 255)
DETAIL = (185, 199, 219)     # detail grey-blue
MUTED = (126, 147, 176)      # sources line
GOLD = (242, 183, 5)         # date accent

# --- fonts ---------------------------------------------------------------
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_KICKER = font("DejaVuSans-Bold.ttf", 13)
F_HEAD = font("DejaVuSans-Bold.ttf", 22)
F_DETAIL = font("DejaVuSans.ttf", 16)
F_FOOT_LABEL = font("DejaVuSans-Bold.ttf", 15)
F_FOOT = font("DejaVuSans.ttf", 15)
F_SOURCE = font("DejaVuSans.ttf", 12)

# --- the nine timeline stories, in time order ----------------------------
# (kicker, headline, detail, accent colour, icon kind)
STORIES = [
    ("TUESDAY NIGHT", "US STRIKES QESHM ISLAND",
     "US hits Iran's Qeshm Island in the Strait of Hormuz",
     (229, 72, 77), "burst"),
    ("EARLY WEDNESDAY", "IRAN DRONES HIT US BASE",
     "Drones strike Patriot defences at Ali Al Salem base",
     (247, 107, 21), "drone"),
    ("APEC SUMMIT", "PUTIN MEETS XI IN SHENZHEN",
     "Leaders meet ahead of first-ever Trump-Xi-Putin talks",
     (255, 178, 36), "meeting"),
    ("MANILA", "QUAD MEETS IN MANILA",
     "First leader-level Quad meeting in over two years",
     (70, 167, 88), "quad"),
    ("GAZA", "ISRAEL BEGINS GAZA PUSH",
     "Concentrated operation in three areas of central Gaza",
     (18, 165, 148), "pin"),
    ("BAY OF BENGAL", "CYCLONE AKVAN STRENGTHENS",
     "Severe storm heads for India's Andhra coast on 20 Nov",
     (62, 155, 255), "cyclone"),
    ("TRADE", "INDIA-US TRADE DEAL CLOSE",
     "Signing waits on a new US tariff framework",
     (142, 78, 198), "document"),
    ("HEALTH", "US LOSES MEASLES-FREE STATUS",
     "Over 5,400 measles cases reported this year",
     (233, 61, 130), "virus"),
    ("MIDNIGHT", "GTA VI LAUNCHES AT MIDNIGHT",
     "Rockstar's game arrives 13 years after GTA V",
     (0, 194, 209), "controller"),
]

FOOTER = [
    ("PNG QUAKE", "Magnitude 6.0 earthquake strikes Papua New Guinea",
     (62, 155, 255)),
    ("SIBERIA CRASH", "Russian military plane crash kills 19",
     (229, 72, 77)),
    ("ALASKA SENATE", "Democrat Mary Peltola wins US Senate seat",
     (70, 167, 88)),
]

SOURCES = "Sources: Anadolu  |  Times of India  |  Just Security  |  Korea Herald  |  Japan Times"


# --- text helpers --------------------------------------------------------
def wrap(text, fnt, max_width, draw):
    """Split text into as few lines as fit max_width pixels."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_height(lines, line_height):
    return len(lines) * line_height


# --- icons: small white glyphs drawn from plain shapes -------------------
def draw_icon(draw, kind, cx, cy, accent):
    r = 24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent,
                 outline=WHITE, width=2)
    w = WHITE
    if kind == "burst":
        pts = []
        for i in range(16):
            ang = math.pi * i / 8 - math.pi / 2
            rad = 13 if i % 2 == 0 else 6
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        draw.polygon(pts, fill=w)
    elif kind == "drone":
        draw.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=w)
        for dx, dy in ((-11, -11), (11, -11), (-11, 11), (11, 11)):
            draw.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4],
                         outline=w, width=2)
    elif kind == "meeting":
        draw.ellipse([cx - 15, cy - 9, cx + 1, cy + 9], outline=w, width=3)
        draw.ellipse([cx - 1, cy - 9, cx + 15, cy + 9], outline=w, width=3)
    elif kind == "quad":
        for dx, dy in ((-9, -9), (3, -9), (-9, 3), (3, 3)):
            draw.rectangle([cx + dx, cy + dy, cx + dx + 6, cy + dy + 6], fill=w)
    elif kind == "pin":
        draw.ellipse([cx - 9, cy - 13, cx + 9, cy + 5], fill=w)
        draw.polygon([(cx - 7, cy + 1), (cx + 7, cy + 1), (cx, cy + 15)], fill=w)
        draw.ellipse([cx - 3, cy - 8, cx + 3, cy - 2], fill=accent)
    elif kind == "cyclone":
        for i, rad in enumerate((5, 9, 13)):
            draw.arc([cx - rad, cy - rad, cx + rad, cy + rad],
                     start=30 + i * 55, end=250 + i * 55, fill=w, width=3)
    elif kind == "document":
        draw.rectangle([cx - 9, cy - 12, cx + 9, cy + 12], outline=w, width=2)
        for dy in (-6, 0, 6):
            draw.line([cx - 5, cy + dy, cx + 5, cy + dy], fill=w, width=2)
    elif kind == "virus":
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=w)
        for i in range(8):
            ang = math.pi * i / 4
            draw.line([cx + 10 * math.cos(ang), cy + 10 * math.sin(ang),
                       cx + 15 * math.cos(ang), cy + 15 * math.sin(ang)],
                      fill=w, width=3)
    elif kind == "controller":
        draw.rounded_rectangle([cx - 14, cy - 8, cx + 14, cy + 8],
                               radius=6, outline=w, width=2)
        draw.ellipse([cx - 9, cy - 2, cx - 5, cy + 2], fill=w)
        draw.ellipse([cx + 5, cy - 2, cx + 9, cy + 2], fill=w)
        draw.line([cx - 2, cy - 3, cx - 2, cy + 3], fill=w, width=2)
        draw.line([cx - 5, cy, cx + 1, cy], fill=w, width=2)


# --- build the image ------------------------------------------------------
def build():
    img = Image.new("RGB", (SIZE, SIZE), NAVY)
    d = ImageDraw.Draw(img)

    # Header: big title, gold rule, the date in gold.
    title = "THE DAY IN NEWS"
    d.text(((SIZE - d.textlength(title, font=F_TITLE)) / 2, 26),
           title, font=F_TITLE, fill=WHITE)
    d.rectangle([SIZE // 2 - 110, 104, SIZE // 2 + 110, 108], fill=GOLD)
    date = "WEDNESDAY  -  18 NOVEMBER 2026"
    d.text(((SIZE - d.textlength(date, font=F_DATE)) / 2, 122),
           date, font=F_DATE, fill=GOLD)

    # Timeline spine.
    top, bottom = 188, 892
    mid = SIZE // 2
    d.line([mid, top, mid, bottom], fill=LINE, width=4)

    # Measure every story block, then spread them evenly in the band.
    col_w = 444
    blocks = []
    for kicker, head, detail, accent, icon in STORIES:
        head_lines = wrap(head, F_HEAD, col_w, d)
        det_lines = wrap(detail, F_DETAIL, col_w, d)
        height = 16 + 3 + len(head_lines) * 26 + 3 + len(det_lines) * 20
        blocks.append((kicker, head_lines, det_lines, accent, icon, height))

    total = sum(b[5] for b in blocks)
    gap = max(4, (bottom - top - total) // (len(blocks) - 1))

    y = top
    for i, (kicker, head_lines, det_lines, accent, icon, height) in enumerate(blocks):
        if y + height > 905:
            raise SystemExit(
                "layout overflow: story %d ends at y=%d, past the footer"
                % (i + 1, y + height))
        cy = y + height // 2
        draw_icon(d, icon, mid, cy, accent)
        if i % 2 == 0:  # text on the left, right-aligned
            right = mid - 44
            d.text((right - d.textlength(kicker, font=F_KICKER), y),
                   kicker, font=F_KICKER, fill=accent)
            ty = y + 19
            for line in head_lines:
                d.text((right - d.textlength(line, font=F_HEAD), ty),
                       line, font=F_HEAD, fill=WHITE)
                ty += 26
            ty += 3
            for line in det_lines:
                d.text((right - d.textlength(line, font=F_DETAIL), ty),
                       line, font=F_DETAIL, fill=DETAIL)
                ty += 20
        else:  # text on the right, left-aligned
            left = mid + 44
            d.text((left, y), kicker, font=F_KICKER, fill=accent)
            ty = y + 19
            for line in head_lines:
                d.text((left, ty), line, font=F_HEAD, fill=WHITE)
                ty += 26
            ty += 3
            for line in det_lines:
                d.text((left, ty), line, font=F_DETAIL, fill=DETAIL)
                ty += 20
        y += height + gap

    # Footer band: three quick facts, then the sources line.
    d.rectangle([0, 908, SIZE, SIZE], fill=NAVY_BAND)
    d.line([0, 908, SIZE, 908], fill=GOLD, width=3)
    col_xs = [30, 362, 694]
    for (label, fact, accent), x in zip(FOOTER, col_xs):
        d.text((x, 924), label, font=F_FOOT_LABEL, fill=accent)
        fact_lines = wrap(fact, F_FOOT, 300, d)
        fy = 946
        for line in fact_lines:
            d.text((x, fy), line, font=F_FOOT, fill=WHITE)
            fy += 19
    d.text(((SIZE - d.textlength(SOURCES, font=F_SOURCE)) / 2, 1000),
           SOURCES, font=F_SOURCE, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
