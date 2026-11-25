#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news poster: one 1024x1024 PNG.

A newspaper front page on cream paper. The lead story is Ukraine
confirming drone strikes on Russian ships in the Gulf of Finland and
off Libya; below it, the COP31 climate summit ending with no deal and
the Houthi strike on Riyadh's tallest tower; then Gaza, Nvidia bringing
back Jensen Huang, and the Sarkozy trial in France; a ticker along the
bottom carries six more stories from the day. Every fact on the poster
was reported on Wednesday 25 November 2026.

Deterministic: no clock, no randomness, no network. Drawing the poster
twice produces byte-identical output.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
REG = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731

# Palette: cream broadsheet, black ink, one red lead accent.
PAPER = (250, 247, 238)
CARD = (255, 253, 247)
INK = (20, 20, 22)
INK_SOFT = (48, 48, 54)
MUTED = (104, 104, 110)
RED = (176, 34, 34)
RED_SOFT = (214, 74, 74)
BLUE = (27, 68, 128)
GOLD = (172, 128, 24)
TEAL = (14, 106, 98)
PURPLE = (86, 58, 148)
SEA = (64, 110, 148)
SAND = (222, 205, 164)
RULE = (196, 188, 172)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def card(draw, x, y, w, h, accent):
    """A white story card with a coloured top bar and a thin ink edge."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD,
                           outline=INK, width=2)
    draw.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=accent)
    draw.rectangle([x, y + 4, x + w, y + 8], fill=accent)


def kicker(draw, x, y, text, color):
    draw.text((x, y), text, font=BOLD(18), fill=color)


def burst(draw, cx, cy, r, color):
    """A small eight-point starburst."""
    pts = []
    for i in range(16):
        ang = 3.14159265 * i / 8.0
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * 1.0 * __import__("math").cos(ang),
                    cy + rr * __import__("math").sin(ang)))
    draw.polygon(pts, fill=color)


def draw_ship(draw, x0, y0):
    """Cargo ship on a strip of sea, a drone above it, a burst astern."""
    # sea
    draw.rectangle([x0, y0 + 118, x0 + 210, y0 + 150], fill=SEA)
    draw.line([x0, y0 + 118, x0 + 210, y0 + 118], fill=BLUE, width=3)
    # hull
    draw.polygon([(x0 + 8, y0 + 88), (x0 + 202, y0 + 88),
                  (x0 + 182, y0 + 118), (x0 + 28, y0 + 118)], fill=INK)
    # containers
    draw.rectangle([x0 + 30, y0 + 58, x0 + 78, y0 + 88], fill=RED)
    draw.rectangle([x0 + 84, y0 + 58, x0 + 132, y0 + 88], fill=GOLD)
    draw.rectangle([x0 + 138, y0 + 58, x0 + 176, y0 + 88], fill=TEAL)
    # bridge + mast
    draw.rectangle([x0 + 178, y0 + 40, x0 + 198, y0 + 88], fill=INK_SOFT)
    draw.line([x0 + 188, y0 + 40, x0 + 188, y0 + 18], fill=INK, width=3)
    draw.polygon([(x0 + 188, y0 + 18), (x0 + 206, y0 + 24),
                  (x0 + 188, y0 + 30)], fill=RED)
    # drone: body and four rotor arms
    dx, dy = x0 + 62, y0 + 8
    draw.line([dx - 22, dy - 8, dx + 22, dy + 8], fill=INK, width=3)
    draw.line([dx - 22, dy + 8, dx + 22, dy - 8], fill=INK, width=3)
    draw.ellipse([dx - 9, dy - 7, dx + 9, dy + 7], fill=INK)
    burst(draw, x0 + 196, y0 + 132, 16, GOLD)


def draw_globe(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                 outline=color, width=2)
    draw.line([cx, cy - r, cx, cy + r], fill=color, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=color, width=2)


def draw_tower(draw, x0, y0):
    """A tall tower with a pointed crown and a burst at its top."""
    draw.rectangle([x0 + 14, y0 + 34, x0 + 46, y0 + 120], fill=INK)
    draw.polygon([(x0 + 14, y0 + 34), (x0 + 46, y0 + 34),
                  (x0 + 30, y0 + 6)], fill=INK)
    for wy in (48, 66, 84, 102):
        draw.rectangle([x0 + 21, y0 + wy, x0 + 39, y0 + wy + 8],
                       fill=GOLD)
    burst(draw, x0 + 30, y0 + 2, 13, RED_SOFT)


def draw_chip(draw, x0, y0):
    draw.rectangle([x0 + 8, y0 + 8, x0 + 40, y0 + 40], fill=INK)
    draw.rectangle([x0 + 17, y0 + 17, x0 + 31, y0 + 31], fill=GOLD)
    for px in (14, 24, 34):
        draw.line([x0 + px, y0, x0 + px, y0 + 8], fill=INK, width=3)
        draw.line([x0 + px, y0 + 40, x0 + px, y0 + 48], fill=INK, width=3)
        draw.line([x0, y0 + px, x0 + 8, y0 + px], fill=INK, width=3)
        draw.line([x0 + 40, y0 + px, x0 + 48, y0 + px], fill=INK, width=3)


def draw_scales(draw, x0, y0):
    draw.line([x0 + 24, y0 + 4, x0 + 24, y0 + 44], fill=INK, width=3)
    draw.line([x0 + 6, y0 + 12, x0 + 42, y0 + 12], fill=INK, width=3)
    draw.polygon([(x0 + 2, y0 + 30), (x0 + 12, y0 + 30),
                  (x0 + 7, y0 + 20)], outline=INK, width=2)
    draw.polygon([(x0 + 36, y0 + 30), (x0 + 46, y0 + 30),
                  (x0 + 41, y0 + 20)], outline=INK, width=2)
    draw.line([x0 + 8, y0 + 44, x0 + 40, y0 + 44], fill=INK, width=3)


def draw_blocks(draw, x0, y0):
    """Two standing blocks and one fallen — a shelled street."""
    draw.rectangle([x0 + 4, y0 + 10, x0 + 20, y0 + 44], fill=INK)
    draw.rectangle([x0 + 24, y0 + 20, x0 + 40, y0 + 44], fill=INK_SOFT)
    draw.rectangle([x0 + 6, y0 + 44, x0 + 44, y0 + 48], fill=RED)


def masthead(draw):
    draw.text((28, 28), "THE WORLD IN ONE PAGE", font=BOLD(50), fill=INK)
    draw.text((28, 92), "WEDNESDAY 25 NOVEMBER 2026",
              font=BOLD(26), fill=RED)
    tag = "ONE DAY — SIX STORIES"
    tag_x = 1024 - 28 - draw.textlength(tag, font=BOLD(18))
    draw.text((tag_x, 98), tag, font=BOLD(18), fill=MUTED)
    draw.line([28, 130, 996, 130], fill=INK, width=3)
    draw.line([28, 136, 996, 136], fill=RULE, width=1)


def lead(draw):
    x, y, w, h = 28, 150, 968, 278
    card(draw, x, y, w, h, RED)
    kicker(draw, x + 20, y + 22, "UKRAINE  ·  THE BALTIC & LIBYA", RED)
    draw.text((x + 20, y + 52), "Kyiv confirms drone strikes",
              font=BOLD(40), fill=INK)
    draw.text((x + 20, y + 100), "on Russian ships",
              font=BOLD(40), fill=INK)
    para(draw, x + 20, y + 158,
         "Zelenskiy says Ukraine hit a cargo ship in the Gulf of Finland "
         "and sank a warship off Libya. Moscow calls the attacks "
         "“terrorism” and warns of consequences.",
         REG(21), INK_SOFT, 700, 28)
    draw_ship(draw, 756, y + 96)


def two_cards(draw):
    y, h, w = 444, 204, 472
    # COP31
    x = 28
    card(draw, x, y, w, h, TEAL)
    kicker(draw, x + 18, y + 20, "CLIMATE  ·  ANTALYA", TEAL)
    draw.text((x + 18, y + 48), "COP31 ends with", font=BOLD(30), fill=INK)
    draw.text((x + 18, y + 84), "no deal", font=BOLD(30), fill=INK)
    para(draw, x + 18, y + 124,
         "Oil and gas producers block fossil-fuel phase-out language; "
         "vulnerable nations leave without the finance they sought.",
         REG(18), INK_SOFT, 436, 24)
    draw_globe(draw, x + 408, y + 62, 34, TEAL)
    # Riyadh
    x = 524
    card(draw, x, y, w, h, RED)
    kicker(draw, x + 18, y + 20, "YEMEN  ·  SAUDI ARABIA", RED)
    draw.text((x + 18, y + 48), "Houthis strike Riyadh's", font=BOLD(30), fill=INK)
    draw.text((x + 18, y + 84), "tallest tower", font=BOLD(30), fill=INK)
    para(draw, x + 18, y + 124,
         "Eleven wounded in the capital; Houthi forces advance to within "
         "60 km of Aden, Yemen's temporary capital.",
         REG(18), INK_SOFT, 360, 24)
    draw_tower(draw, x + 388, y + 56)


def three_cards(draw):
    y, h, w = 664, 204, 312
    # Gaza
    x = 28
    card(draw, x, y, w, h, BLUE)
    kicker(draw, x + 16, y + 20, "GAZA", BLUE)
    draw.text((x + 16, y + 48), "Strike kills Hamas", font=BOLD(25), fill=INK)
    draw.text((x + 16, y + 78), "official", font=BOLD(25), fill=INK)
    para(draw, x + 16, y + 116,
         "Israel's strike kills a Hamas official in Gaza; the death toll "
         "reaches 74,746.",
         REG(17), INK_SOFT, 280, 22)
    # Nvidia
    x = 356
    card(draw, x, y, w, h, GOLD)
    kicker(draw, x + 16, y + 20, "TECH  ·  MARKETS", GOLD)
    draw.text((x + 16, y + 48), "Nvidia brings back", font=BOLD(25), fill=INK)
    draw.text((x + 16, y + 78), "Jensen Huang", font=BOLD(25), fill=INK)
    para(draw, x + 16, y + 116,
         "The board reinstates the chief executive days after accepting "
         "his resignation; Asian tech shares slide.",
         REG(17), INK_SOFT, 280, 22)
    # France
    x = 684
    card(draw, x, y, w, h, PURPLE)
    kicker(draw, x + 16, y + 20, "FRANCE", PURPLE)
    draw.text((x + 16, y + 48), "Sarkozy and Bruni", font=BOLD(25), fill=INK)
    draw.text((x + 16, y + 78), "to stand trial", font=BOLD(25), fill=INK)
    para(draw, x + 16, y + 116,
         "A court orders the corruption case against the former president "
         "and his wife to trial.",
         REG(17), INK_SOFT, 280, 22)


def ticker(draw):
    y, h = 884, 84
    draw.rectangle([28, y, 996, y + h], fill=INK)
    draw.text((44, y + 32), "ALSO TODAY", font=BOLD(18), fill=GOLD)
    items = ("China probes Shanghai party chief Chen Jining  ·  NATO vows "
             "space defence over a reported Russian nuclear satellite  ·  "
             "Huawei guilty of trade-secret theft  ·  South Korea's "
             "education minister quits over exam cheating  ·  "
             "Australia–Solomon Islands security pact")
    para(draw, 200, y + 10, items, REG(15), PAPER, 780, 19)


def footer(draw):
    note = ("Every fact on this page was reported on Wednesday "
            "25 November 2026.")
    draw.text(((1024 - draw.textlength(note, font=REG(15))) / 2, 978),
              note, font=REG(15), fill=MUTED)
    tag = "Drawn by program  ·  news-image-20261125  ·  make.fun"
    draw.text(((1024 - draw.textlength(tag, font=BOLD(14))) / 2, 998),
              tag, font=BOLD(14), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead(draw)
    two_cards(draw)
    three_cards(draw)
    ticker(draw)
    footer(draw)
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
