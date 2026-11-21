#!/usr/bin/env python3
"""Render the news-image-20261121 front page (1024x1024 PNG).

Draws at 2x (2048x2048) with Pillow and downscales with LANCZOS for
clean text and lines. Build-time only; the graded main.py is stdlib-only.
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W = H = 1024 * S
PAPER = (246, 241, 231)
INK = (20, 20, 20)
NAVY = (19, 38, 77)
NAVY_DARK = (13, 27, 55)
GOLD = (232, 200, 90)
RED = (179, 32, 44)
GRAY = (110, 105, 95)
CARD = (255, 255, 255)
BORDER = (200, 192, 172)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * S)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, lines, fnt, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def starburst(d, cx, cy, r_out, r_in, n=12, fill=(255, 200, 40)):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def star5(d, cx, cy, r_out, r_in, fill):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / 5 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill, outline=(120, 85, 10), width=4 * S)


def dashed_line(d, p0, p1, fill, width=4, dash=18, gap=12):
    x0, y0, x1, y1 = p0[0], p0[1], p1[0], p1[1]
    dist = math.hypot(x1 - x0, y1 - y0)
    n = int(dist / (dash + gap))
    for i in range(n + 1):
        t0, t1 = i * (dash + gap) / dist, min(1.0, (i * (dash + gap) + dash) / dist)
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
               fill=fill, width=width * S)


# ---------------------------------------------------------------- illustrations
def ill_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(29, 53, 87))
    land = [(x0 + 90, y0 + 70), (x0 + 300, y0 + 34), (x0 + 520, y0 + 66),
            (x0 + 640, y0 + 150), (x0 + 600, y0 + 250), (x0 + 690, y0 + 330),
            (x0 + 560, y0 + 400), (x0 + 380, y0 + 430), (x0 + 190, y0 + 400),
            (x0 + 70, y0 + 300), (x0 + 46, y0 + 180)]
    d.polygon(land, fill=(232, 228, 213))
    # missile arcs from the east
    dashed_line(d, (x1 - 30, y0 + 120), (x0 + 520, y0 + 285), (255, 120, 90), 5)
    dashed_line(d, (x1 - 30, y0 + 90), (x0 + 310, y0 + 195), (255, 120, 90), 5)
    # Kyiv burst
    starburst(d, x0 + 520, y0 + 285, 46, 20, fill=(255, 190, 40))
    d.ellipse([x0 + 505, y0 + 270, x0 + 535, y0 + 300], fill=(179, 32, 44))
    d.text((x0 + 575, y0 + 262), "KYIV", font=font(SANS_B, 24), fill=(19, 38, 77))
    # Poland burst
    starburst(d, x0 + 310, y0 + 195, 40, 17, fill=(255, 140, 40))
    d.ellipse([x0 + 298, y0 + 183, x0 + 322, y0 + 207], fill=(179, 32, 44))
    d.text((x0 + 120, y0 + 100), "POLAND", font=font(SANS_B, 26), fill=(19, 38, 77))
    d.text((x0 + 430, y0 + 340), "UKRAINE", font=font(SANS_B, 24), fill=(19, 38, 77))


def ill_chart(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    for i in range(5):
        gy = y0 + 30 + i * ((y1 - y0 - 60) // 4)
        d.line([(x0 + 20, gy), (x1 - 20, gy)], fill=(230, 230, 230), width=2 * S)
    pts = [(x0 + 40, y0 + 34), (x0 + 190, y0 + 62), (x0 + 330, y0 + 52),
           (x0 + 470, y0 + 100), (x0 + 580, y0 + 118)]
    d.line(pts, fill=(179, 32, 44), width=7 * S, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 26, ey - 6), (ex - 8, ey - 26)], fill=(179, 32, 44))
    d.text((x0 + 30, y0 + 138), "S&P 500  \u22123.7%", font=font(SANS_B, 30),
           fill=(179, 32, 44))


def ill_climate(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(216, 236, 243))
    # sun
    sx, sy = x1 - 80, y0 + 56
    d.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=(245, 200, 60))
    # globe
    gx, gy, gr = x0 + 140, y0 + 138, 62
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(58, 123, 213))
    d.ellipse([gx - 38, gy - 30, gx + 4, gy + 4], fill=(86, 170, 90))
    d.ellipse([gx - 8, gy + 16, gx + 40, gy + 46], fill=(86, 170, 90))
    # factory with smoke
    fx, fy = x0 + 380, y1 - 30
    d.rectangle([fx, fy - 60, fx + 140, fy], fill=(120, 120, 120))
    d.rectangle([fx + 155, fy - 100, fx + 182, fy], fill=(100, 100, 100))
    for i, (dx, dy, r) in enumerate(((168, -120, 16), (178, -140, 19),
                                     (190, -158, 22))):
        d.ellipse([fx + dx - r, fy + dy - r, fx + dx + r, fy + dy + r],
                  fill=(150, 150, 150))
    d.rectangle([x0, y1 - 24, x1, y1], fill=(120, 160, 110))
    d.text((x0 + 24, y0 + 14), "ANTALYA, TURKEY", font=font(SANS_B, 20),
           fill=(60, 80, 100))
    d.text((x0 + 24, y0 + 52), "DEADLOCK", font=font(SANS_B, 20), fill=(179, 32, 44))


def ill_quake(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(239, 230, 212))
    # mountains
    d.polygon([(x0 + 20, y1 - 40), (x0 + 220, y0 + 60), (x0 + 420, y1 - 40)],
              fill=(122, 106, 88))
    d.polygon([(x0 + 190, y0 + 82), (x0 + 220, y0 + 60), (x0 + 252, y0 + 84),
               (x0 + 236, y0 + 96), (x0 + 220, y0 + 84), (x0 + 204, y0 + 96)],
              fill=(255, 255, 255))
    d.polygon([(x0 + 330, y1 - 40), (x0 + 500, y0 + 100), (x0 + 620, y1 - 40)],
              fill=(96, 84, 70))
    d.polygon([(x0 + 478, y0 + 118), (x0 + 500, y0 + 100), (x0 + 524, y0 + 120),
               (x0 + 512, y0 + 130), (x0 + 500, y0 + 120), (x0 + 488, y0 + 130)],
              fill=(255, 255, 255))
    d.rectangle([x0, y1 - 40, x1, y1], fill=(150, 130, 105))
    # seismograph zigzag
    pts, px = [], x0 + 30
    ys = [y0 + 130, y0 + 118, y0 + 142, y0 + 96, y0 + 168, y0 + 120, y0 + 140,
          y0 + 108, y0 + 152, y0 + 124, y0 + 138, y0 + 128]
    for yy in ys:
        pts.append((px, yy))
        px += 52
    d.line(pts, fill=(179, 32, 44), width=5 * S, joint="curve")
    d.rounded_rectangle([x0 + 24, y0 + 14, x0 + 196, y0 + 76], radius=8,
                        fill=(179, 32, 44))
    d.text((x0 + 40, y0 + 24), "M 6.9", font=font(SANS_B, 24), fill=(255, 255, 255))


def ill_capture(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(236, 229, 211))
    cx, cy = x0 + 180, y0 + 105
    star5(d, cx, cy, 92, 40, fill=(232, 190, 60))
    d.text((cx - 52, cy - 16), "FBI", font=font(SANS_B, 34), fill=(120, 85, 10))
    # handcuffs
    for hx in (x0 + 400, x0 + 520):
        d.ellipse([hx - 42, y0 + 110, hx + 42, y0 + 194], outline=(40, 40, 40),
                  width=10 * S)
        d.ellipse([hx - 14, y0 + 138, hx + 14, y0 + 166], outline=(40, 40, 40),
                  width=6 * S)
    for i in range(3):
        lx = x0 + 452 + i * 20
        d.ellipse([lx - 9, y0 + 138, lx + 9, y0 + 156], outline=(40, 40, 40),
                  width=5 * S)
    d.text((x0 + 452, y0 + 24), "WANTED", font=font(SANS_B, 20),
           fill=(179, 32, 44))


def ill_fire(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(38, 34, 31))
    # glow
    gx, gy = x0 + 320, y0 + 110
    d.ellipse([gx - 130, gy - 80, gx + 130, gy + 80], fill=(120, 60, 20))
    # cooling tower
    tx = x0 + 400
    d.polygon([(tx, y0 + 110), (tx + 150, y0 + 110), (tx + 130, y0 + 190),
               (tx + 170, y1 - 10), (tx - 20, y1 - 10), (tx + 20, y0 + 190)],
              fill=(110, 108, 105))
    d.rectangle([tx - 6, y0 + 96, tx + 156, y0 + 112], fill=(140, 138, 135))
    # flames
    for fx, fh, col in ((gx - 70, 90, (255, 140, 30)), (gx - 10, 130, (255, 190, 40)),
                        (gx + 55, 80, (255, 120, 20))):
        d.polygon([(fx, gy + 20), (fx + 34, gy - fh), (fx + 68, gy + 20)],
                  fill=col)
    # smoke
    for i, (dx, dy, r) in enumerate(((-60, 34, 14), (0, 24, 18), (60, 34, 14))):
        d.ellipse([gx + dx - r, y0 + dy - r, gx + dx + r, y0 + dy + r],
                  fill=(90, 88, 85))
    d.text((x0 + 24, y1 - 38), "HARTHA PLANT", font=font(SANS_B, 20),
           fill=(255, 220, 160))


def ill_pill(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(228, 239, 228))
    # capsule on its own layer, rotated
    cap = Image.new("RGBA", (260, 110), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cap)
    cd.rounded_rectangle([8, 24, 252, 86], radius=31, fill=(255, 255, 255),
                         outline=(150, 40, 40), width=5)
    cd.rounded_rectangle([8, 24, 130, 86], radius=31, fill=(192, 57, 43))
    cd.rounded_rectangle([122, 24, 252, 86], radius=31, fill=(255, 255, 255))
    cd.rounded_rectangle([8, 24, 252, 86], radius=31, outline=(120, 30, 30),
                         width=5)
    cap = cap.rotate(-15, resample=Image.BICUBIC, expand=True)
    img.paste(cap, (x0 + 80, y0 + 36), cap)
    # shrinking tumour dots
    cy = y1 - 40
    for i, r in enumerate((26, 18, 11)):
        d.ellipse([x0 + 400 + i * 52 - r, cy - r, x0 + 400 + i * 52 + r, cy + r],
                  fill=(179, 32, 44) if i == 0 else (200, 90, 90) if i == 1
                  else (220, 170, 170))
    d.text((x0 + 24, y0 + 14), "TUMOURS SHRINK", font=font(SANS_B, 20),
           fill=(50, 90, 50))


# ---------------------------------------------------------------- page
def main():
    global img
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 148 * S], fill=NAVY)
    d.rectangle([0, 148 * S, W, 152 * S], fill=GOLD)
    d.text((W // 2, 14 * S), "ONE DAY  \u00b7  SEVEN STORIES  \u00b7  THE WORLD IN ONE IMAGE",
           font=font(SANS_B, 13), fill=GOLD, anchor="ma")
    d.text((W // 2, 36 * S), "THE WORLD TODAY", font=font(SERIF_B, 58),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 104 * S), "SATURDAY, 21 NOVEMBER 2026",
           font=font(SANS_B, 30), fill=GOLD, anchor="ma")

    # ---- lead story
    lx0, ly0, lx1, ly1 = 24 * S, 164 * S, 1000 * S, 424 * S
    d.rectangle([lx0, ly0, lx1, ly1], fill=CARD, outline=BORDER, width=2 * S)
    ix0, iy0, ix1, iy1 = lx0 + 12 * S, ly0 + 12 * S, lx0 + 412 * S, ly1 - 12 * S
    ill_map(d, ix0, iy0, ix1, iy1)
    tx = lx0 + 436 * S
    tw = lx1 - 12 * S - tx
    d.text((tx, ly0 + 16 * S), "WAR IN UKRAINE \u2014 LEAD STORY",
           font=font(SANS_B, 15), fill=RED)
    y = draw_text_block(
        d, tx, ly0 + 40 * S,
        wrap(d, "Russian missiles fall in Poland as barrage hits Kyiv",
             font(SERIF_B, 31), tw), font(SERIF_B, 31), INK, 36 * S)
    y += 8 * S
    draw_text_block(
        d, tx, y,
        wrap(d, "More than 400 drones and 110 missiles fired overnight; "
                "at least 8 killed in Kyiv. Warsaw calls the strikes on "
                "its soil a deliberate provocation.",
             font(SANS, 16), tw), font(SANS, 16), (60, 55, 45), 22 * S)

    # ---- six-card grid
    cards = [
        ("MARKETS", "AI sell-off drags S&P 500 into correction",
         "S&P 500 falls 3.7%; Nasdaq drops 5.3%, wiping out its 2026 gains.",
         ill_chart),
        ("CLIMATE \u00b7 COP31", "Climate talks deadlocked over fossil fuels",
         "Summit in Antalya, Turkey, runs past its deadline as nearly 200 "
         "nations fail to agree.", ill_climate),
        ("PERU", "Magnitude 6.9 quake shakes the Andes",
         "Tremors felt in Lima; no damage or casualties reported at first.",
         ill_quake),
        ("MEXICO", "FBI's most wanted drug lord captured",
         "\u201cChapo Isidro\u201d seized in a joint US\u2013Mexico raid; "
         "gunfight erupts in Sinaloa.", ill_capture),
        ("IRAQ", "Fire at Basra power plant kills at least 4",
         "Blaze at the Hartha station injures 30 and halts power output.",
         ill_fire),
        ("HEALTH", "Cancer pill clears tumours in 1 in 12",
         "Daraxonrasib plus chemotherapy shrank tumours in 6 in 10 patients "
         "in a small trial.", ill_pill),
    ]
    gx0, gy0 = 24 * S, 440 * S
    cw, ch, gap = 317 * S, 250 * S, 12 * S
    for i, (kicker, head, deck, ill) in enumerate(cards):
        cx0 = gx0 + (i % 3) * (cw + gap)
        cy0 = gy0 + (i // 3) * (ch + gap)
        cx1, cy1 = cx0 + cw, cy0 + ch
        d.rectangle([cx0, cy0, cx1, cy1], fill=CARD, outline=BORDER, width=2 * S)
        ill(d, cx0 + 8 * S, cy0 + 8 * S, cx1 - 8 * S, cy0 + 120 * S)
        tx = cx0 + 12 * S
        tw = cw - 24 * S
        y = cy0 + 128 * S
        d.text((tx, y), kicker, font=font(SANS_B, 13), fill=RED)
        y += 20 * S
        y = draw_text_block(
            d, tx, y, wrap(d, head, font(SERIF_B, 20), tw),
            font(SERIF_B, 20), INK, 24 * S)
        y += 4 * S
        draw_text_block(
            d, tx, y, wrap(d, deck, font(SANS, 14), tw),
            font(SANS, 14), (60, 55, 45), 18 * S)

    # ---- footer
    d.text((W // 2, 968 * S),
           "Sources: CNN \u00b7 Reuters \u00b7 USGS \u00b7 OncLive \u00b7 Medindia  \u2014  "
           "All stories reported Saturday, 21 November 2026",
           font=font(SANS, 13), fill=GRAY, anchor="ma")

    out = img.resize((1024, 1024), Image.LANCZOS)
    out.save("news.png", optimize=True)
    print("saved news.png")


if __name__ == "__main__":
    main()
