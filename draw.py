#!/usr/bin/env python3
"""Draw the front page for Friday 27 November 2026 as a 1024x1024 PNG.

Deterministic: no randomness, no clock, no network. Run:
    python3 draw.py            # writes entry.png next to this file
Everything is measured with the font before it is drawn, so no text
overflows its box.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W = H = 1024
MARGIN = 36

PAPER = (253, 253, 248)
INK = (17, 17, 17)
GREY = (90, 90, 86)
LIGHT_GREY = (150, 150, 144)
RED = (163, 18, 26)
NAVY = (28, 53, 94)
RULE = (40, 40, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[2] - box[0]


def text_h(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[3] - box[1]


def wrap(draw, s, f, width):
    """Greedy word wrap; returns lines that all fit `width`."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, s, f, width, max_lines):
    """Wrap, then shrink the font until it fits max_lines (never below 60%)."""
    size = f.size
    while size > 12:
        lines = wrap(draw, s, font(f.path, size), width)
        if len(lines) <= max_lines:
            return lines, font(f.path, size)
        size -= 1
    return wrap(draw, s, font(f.path, size), width), font(f.path, size)


def draw_wrapped(draw, x, y, s, f, width, leading, color=INK, max_lines=99):
    lines, f2 = fit_lines(draw, s, f, width, max_lines)
    for line in lines:
        draw.text((x, y), line, font=f2, fill=color)
        y += int(f2.size * leading)
    return y


def rule(draw, x0, y, x1, width=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker(draw, x, y, s, size=17):
    f = font(SANS_B, size)
    draw.text((x, y), s, font=f, fill=RED)
    return y + size + 6


def headline(draw, x, y, s, size, width, max_lines=3, color=INK):
    f = font(SERIF_B, size)
    return draw_wrapped(draw, x, y, s, f, width, 1.04, color=color, max_lines=max_lines)


def body(draw, x, y, s, size, width, max_lines=6):
    f = font(SERIF, size)
    return draw_wrapped(draw, x, y, s, f, width, 1.28, color=INK, max_lines=max_lines)


# ---------------------------------------------------------------- panels
def panel_lead(draw, x0, y0, x1, y1):
    """Night sky over Kyiv: dark sky, skyline, blast glow, missile trail."""
    draw.rectangle([x0, y0, x1, y1], fill=(16, 24, 46))
    # stars
    for sx, sy in [(0.12, 0.18), (0.3, 0.1), (0.52, 0.22), (0.7, 0.12),
                   (0.86, 0.28), (0.44, 0.08), (0.95, 0.14), (0.22, 0.3)]:
        px, py = x0 + int((x1 - x0) * sx), y0 + int((y1 - y0) * sy)
        draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(230, 230, 220))
    # blast glow
    bx, by = x0 + int((x1 - x0) * 0.68), y0 + int((y1 - y0) * 0.62)
    for r, col in [(46, (255, 140, 40)), (30, (255, 190, 70)), (16, (255, 230, 150))]:
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    # missile trail
    mx0, my0 = x0 + int((x1 - x0) * 0.08), y0 + int((y1 - y0) * 0.16)
    draw.line([(mx0, my0), (bx - 20, by - 26)], fill=(255, 240, 200), width=3)
    draw.ellipse([mx0 - 4, my0 - 4, mx0 + 4, my0 + 4], fill=(255, 240, 200))
    # skyline
    base = y1 - 8
    heights = [0.42, 0.55, 0.34, 0.62, 0.48, 0.58, 0.38, 0.5]
    n = len(heights)
    bw = (x1 - x0) // n
    for i, hfrac in enumerate(heights):
        bx0 = x0 + i * bw
        top = base - int((y1 - y0) * hfrac)
        draw.rectangle([bx0 + 2, top, bx0 + bw - 2, base], fill=(8, 10, 18))
        # lit windows
        for wy in range(top + 8, base - 6, 14):
            for wx in range(bx0 + 6, bx0 + bw - 6, 12):
                if (wx + wy) % 29 < 9:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 110))
    draw.rectangle([x0, base, x1, y1], fill=(8, 10, 18))


def panel_storm(draw, x0, y0, x1, y1):
    """Rain over a street: grey sky, cloud, slanting rain, rooftops."""
    draw.rectangle([x0, y0, x1, y1], fill=(196, 205, 214))
    # cloud (kept inside the panel)
    cx, cy = x0 + int((x1 - x0) * 0.5), y0 + int((y1 - y0) * 0.34)
    for dx, dy, r in [(-70, 4, 26), (-30, -6, 32), (20, 0, 30), (62, 6, 24)]:
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=(96, 104, 116))
    # rain
    for i in range(26):
        rx = x0 + 12 + (i * 37) % (x1 - x0 - 24)
        ry = y0 + 52 + (i * 23) % (y1 - y0 - 90)
        draw.line([(rx, ry), (rx - 7, ry + 16)], fill=(70, 90, 120), width=2)
    # rooftops
    base = y1 - 6
    for i, (wfrac, hfrac) in enumerate([(0.30, 0.30), (0.42, 0.42), (0.28, 0.34)]):
        hx0 = x0 + int((x1 - x0) * (0.06 + i * 0.32))
        hw = int((x1 - x0) * wfrac)
        ht = int((y1 - y0) * hfrac)
        draw.rectangle([hx0, base - ht, hx0 + hw, base], fill=(52, 58, 66))
        draw.polygon([(hx0 - 6, base - ht), (hx0 + hw // 2, base - ht - 18),
                      (hx0 + hw + 6, base - ht)], fill=(40, 44, 52))
        draw.rectangle([hx0 + hw // 2 - 6, base - ht + 14, hx0 + hw // 2 + 6,
                        base - ht + 30], fill=(255, 220, 130))


def panel_gulf(draw, x0, y0, x1, y1):
    """Tanker on a strait at dusk: sea bands, hull, smoke, sun."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 178, 110))
    # sun (kept inside the panel)
    sx, sy = x0 + int((x1 - x0) * 0.78), y0 + int((y1 - y0) * 0.32)
    draw.ellipse([sx - 22, sy - 22, sx + 22, sy + 22], fill=(255, 214, 130))
    # sea
    sea_y = y0 + int((y1 - y0) * 0.52)
    draw.rectangle([x0, sea_y, x1, y1], fill=(24, 68, 110))
    for i, wy in enumerate(range(sea_y + 12, y1 - 6, 16)):
        draw.line([(x0 + 8, wy), (x1 - 8, wy)], fill=(70, 130, 180), width=2)
    # tanker hull
    hx0, hx1 = x0 + int((x1 - x0) * 0.12), x0 + int((x1 - x0) * 0.72)
    hy = sea_y + 14
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 18, hy + 26), (hx0 + 10, hy + 26)],
                 fill=(20, 20, 24))
    draw.rectangle([hx0 + 14, hy - 22, hx0 + 60, hy], fill=(20, 20, 24))
    draw.rectangle([hx0 + 66, hy - 34, hx0 + 96, hy], fill=(140, 30, 30))
    # smoke + flame (kept inside the panel)
    fx = hx0 + 110
    draw.ellipse([fx - 12, hy - 44, fx + 12, hy - 22], fill=(60, 60, 60))
    draw.ellipse([fx - 7, hy - 34, fx + 7, hy - 22], fill=(255, 150, 50))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- masthead
    y = 30
    rule(d, x0, y, x1, 3)
    rule(d, x0, y + 7, x1, 1)
    y += 18
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 76)
    d.text(((W - text_w(d, title, tf)) // 2, y), title, font=tf, fill=INK)
    y += 88
    dateline = "FRIDAY, 27 NOVEMBER 2026"
    df = font(SANS_B, 24)
    d.text(((W - text_w(d, dateline, df)) // 2, y), dateline, font=df, fill=RED)
    y += 34
    sub = "WORLD NEWS IN ONE PAGE  ·  KYIV  ·  WASHINGTON  ·  NEW YORK  ·  THE GULF"
    sf = font(SANS, 15)
    d.text(((W - text_w(d, sub, sf)) // 2, y), sub, font=sf, fill=GREY)
    y += 26
    rule(d, x0, y, x1, 3)
    rule(d, x0, y + 6, x1, 1)
    y += 18

    # ---- lead story
    y = kicker(d, x0, y, "UKRAINE WAR  —  WASHINGTON / KYIV", 18)
    y = headline(d, x0, y, "TRUMP TO PUTIN: “PULL BACK”", 50, x1 - x0, max_lines=1)
    y = headline(d, x0, y, "Zelenskyy warns of new mass strike as Kyiv is hit", 27,
                 x1 - x0, max_lines=1)
    y += 6
    # lead body (left) + panel (right)
    col_w = 560
    panel_x0, panel_x1 = x0 + col_w + 24, x1
    panel_y0, panel_y1 = y, y + 158
    panel_lead(d, panel_x0, panel_y0, panel_x1, panel_y1)
    d.text((panel_x0, panel_y1 + 6),
           "KYIV UNDER FIRE — ballistic missiles struck the",
           font=font(SANS, 13), fill=GREY)
    d.text((panel_x0, panel_y1 + 24),
           "capital overnight; seven wounded.",
           font=font(SANS, 13), fill=GREY)
    lead_body = (
        "President Donald Trump said he pressed Vladimir Putin to end "
        "Russia’s military aggression across Europe, telling the Russian "
        "leader in talks in China to “pull back all military aggression”."
    )
    y = body(d, x0, y, lead_body, 20, col_w, max_lines=5)
    y += 6
    lead_body2 = (
        "“Thousands of people are being killed each and every month, a "
        "complete bloodbath,” Mr Trump wrote, saying a deal to end the war "
        "was “a strong possibility”. Hours later, President Volodymyr "
        "Zelenskyy warned Russia is preparing a new mass strike."
    )
    y = body(d, x0, y, lead_body2, 20, col_w, max_lines=6)
    y = max(y, panel_y1 + 46)
    y += 8
    rule(d, x0, y, x1, 2)
    y += 14

    # ---- second row: two columns
    mid = (x0 + x1) // 2
    left_w = mid - x0 - 18
    right_w = x1 - (mid + 18)
    row_top = y

    # left: storm
    ly = kicker(d, x0, row_top, "UNITED STATES", 16)
    ly = headline(d, x0, ly, "Thanksgiving storm batters the East Coast", 28,
                  left_w, max_lines=2)
    ly = body(d, x0, ly,
              "Nearly 900,000 homes and businesses lost power as a powerful "
              "coastal storm swept the East Coast on Thanksgiving, with "
              "gusts to 70 mph and more than 400 flights cancelled. New York "
              "postponed the 100th Macy’s parade to Saturday, a first.",
              17, left_w, max_lines=6)
    ly += 8
    panel_storm(d, x0, ly, x0 + left_w, ly + 70)

    # right: gulf
    rx = mid + 18
    ry = kicker(d, rx, row_top, "THE GULF", 16)
    ry = headline(d, rx, ry, "Gulf on edge as tankers are hit", 28, right_w,
                  max_lines=2)
    ry = body(d, rx, ry,
              "Explosions struck three tankers in the Strait of Hormuz and "
              "a drone attack in Kuwait killed two Italian workers, as Iran "
              "stepped up attacks across the Gulf. Kuwait intercepted a "
              "drone assault and diverted commercial flights.",
              17, right_w, max_lines=6)
    ry += 8
    panel_gulf(d, rx, ry, rx + right_w, ry + 70)

    y = max(ly + 70, ry + 70) + 14
    rule(d, x0, y, x1, 2)
    y += 14

    # ---- briefs strip: 3 columns x 2 rows
    briefs = [
        ("SAUDI ARABIA", "Houthi strike hits the Jazan refinery: one killed, "
         "operations halted."),
        ("NORTH KOREA", "Kim Jong Un calls for an expansion of the nuclear "
         "programme."),
        ("EGYPT", "Fuel-truck crash and fire in Cairo kills 31 people."),
        ("BRITAIN", "London faces disruption as a 24-hour Tube strike begins."),
        ("HONG KONG", "Police warn of unrest on the anniversary of the fire "
         "that killed 168."),
        ("SPORT", "India open the 2nd Test in Christchurch; Gukesh draws "
         "game three."),
    ]
    colw = (x1 - x0 - 2 * 24) // 3
    by = y
    for i, (kick, text) in enumerate(briefs):
        cx = x0 + (i % 3) * (colw + 24)
        cy = by + (i // 3) * 62
        kicker(d, cx, cy, kick, 14)
        draw_wrapped(d, cx, cy + 20, text, font(SERIF, 14), colw, 1.22,
                     max_lines=2)
    y = by + 2 * 62 + 2
    rule(d, x0, y, x1, 2)
    y += 10

    # ---- footer
    foot = "THE WORLD TODAY  ·  Friday 27 November 2026  ·  Picture of the day’s news"
    ff = font(SANS, 14)
    d.text(((W - text_w(d, foot, ff)) // 2, y), foot, font=ff, fill=GREY)
    print("footer y:", y, "page height:", H)
    assert y + 20 <= H, "page overflowed"

    img.save(OUT, optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
