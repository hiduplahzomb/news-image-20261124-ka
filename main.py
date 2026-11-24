#!/usr/bin/env python3
"""News Image 20261124 — "The Tuesday Herald" front page (KA entry).

Writes one 1024x1024 PNG to /output/entry.png summing up Tuesday
24 November 2026's world news, researched from live headlines:
lead story NATO deploys AWACS to Poland after three Russian Kh-101
missiles landed there; Ukraine sinks a Russian warship in Libya;
Indonesia factory fire kills 24; COP31 talks collapse; Nvidia's
Jensen Huang returns as CEO (+31%); Verstappen wins the Las Vegas GP.

A newspaper front page: masthead, dateline, dominant lead story with
a drawn radar-plane illustration, two illustrated secondary stories,
and a briefs strip. All artwork is drawn with PIL on clipped layers
(no photos, no overflow past panel edges).
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 32, 44)
GREY = (110, 110, 108)
LIGHT = (226, 220, 208)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def fit_font(draw, text, name, size, max_w):
    """Shrink font until text fits max_w; return (font, width)."""
    while size > 10:
        f = font(name, size)
        if draw.textlength(text, font=f) <= max_w:
            return f, draw.textlength(text, font=f)
        size -= 2
    f = font(name, 10)
    return f, draw.textlength(text, font=f)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def layer(w, h):
    img = Image.new("RGB", (w, h), (0, 0, 0))
    return img, ImageDraw.Draw(img)


def draw_awacs(x0, y0, x1, y1):
    """Radar-plane illustration on its own clipped layer."""
    w, h = x1 - x0, y1 - y0
    img, d = layer(w, h)
    d.rectangle([0, 0, w - 1, h - 1], fill=(16, 34, 64))
    cx, cy = w // 2, h // 2
    for r, col in ((80, (40, 80, 140)), (55, (60, 105, 175)), (32, (90, 140, 210))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
    d.line([(cx - 88, cy), (cx + 88, cy)], fill=(60, 105, 175), width=1)
    d.line([(cx, cy - 88), (cx, cy + 88)], fill=(60, 105, 175), width=1)
    for mx, my in ((55, 28), (105, 62), (185, 38)):
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=RED)
        d.text((mx + 10, my - 9), "Kh-101", font=font(SANS_B, 15), fill=(255, 120, 120))
    px, py = cx, cy
    body = [(px - 95, py), (px - 60, py - 14), (px + 55, py - 14), (px + 105, py - 4),
            (px + 95, py + 4), (px + 40, py + 10), (px - 70, py + 10)]
    d.polygon(body, fill=(240, 240, 235))
    d.ellipse([px - 28, py - 34, px + 28, py - 20], fill=(240, 240, 235))
    d.line([(px - 6, py - 20), (px - 6, py - 13)], fill=(240, 240, 235), width=4)
    d.line([(px + 6, py - 20), (px + 6, py - 13)], fill=(240, 240, 235), width=4)
    d.polygon([(px - 72, py - 12), (px - 90, py - 38), (px - 54, py - 12)],
              fill=(240, 240, 235))  # vertical stabilizer at the rear
    d.text((14, h - 30), "POLAND  •  NATO EASTERN FLANK",
           font=font(SANS_B, 16), fill=(200, 210, 235))
    return img


def draw_warship(x0, y0, x1, y1):
    """Warship at sea with drone dots and an explosion flash."""
    w, h = x1 - x0, y1 - y0
    img, d = layer(w, h)
    d.rectangle([0, 0, w - 1, h - 1], fill=(20, 44, 78))
    # sea waves
    for i, yy in enumerate(range(h - 42, h - 4, 12)):
        d.arc([8 + (i % 2) * 26, yy, 78 + (i % 2) * 26, yy + 10],
              200, 340, fill=(90, 140, 200), width=2)
    # ship hull — lighter grey so it reads against the dark sea
    sx, sy = 30, h - 62
    hull = [(sx, sy), (sx + 190, sy), (sx + 222, sy + 20), (sx + 8, sy + 20)]
    d.polygon(hull, fill=(58, 66, 80))
    d.rectangle([sx + 66, sy - 24, sx + 112, sy], fill=(58, 66, 80))
    d.rectangle([sx + 120, sy - 36, sx + 129, sy], fill=(58, 66, 80))
    d.line([(sx + 124, sy - 36), (sx + 124, sy - 48)], fill=(58, 66, 80), width=3)
    # explosion flash sitting on the ship's deck
    ex, ey = sx + 148, sy - 52
    for (dx, dy, r) in ((0, 0, 24), (-17, 8, 13), (17, 9, 14), (0, -15, 12)):
        d.ellipse([ex + dx - r, ey + dy - r, ex + dx + r, ey + dy + r],
                  fill=(255, 176, 32))
    d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=(255, 230, 120))
    # drones
    for dx, dy in ((26, 24), (62, 44), (w - 34, 28)):
        d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(220, 220, 220))
        d.line([(dx - 9, dy), (dx + 9, dy)], fill=(220, 220, 220), width=2)
    return img


def draw_fire(x0, y0, x1, y1):
    """Factory building with flames and smoke."""
    w, h = x1 - x0, y1 - y0
    img, d = layer(w, h)
    d.rectangle([0, 0, w - 1, h - 1], fill=(52, 40, 36))
    # smoke puffs
    for (sx, sy, r) in ((70, 34, 20), (125, 20, 25), (185, 30, 18)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 148, 145))
    # factory block occupies lower 2/3 of the panel
    top = h - 78
    d.rectangle([24, top, w - 24, h - 6], fill=(24, 24, 26))
    d.rectangle([24, top, w - 24, top + 10], fill=(60, 58, 56))
    # lit windows inside the block
    for wx in range(44, w - 60, 34):
        d.rectangle([wx, top + 22, wx + 20, top + 42], fill=(255, 176, 32))
    # flames rising from the roof
    for fx in (70, 130, 190):
        d.polygon([(fx - 22, top + 4), (fx - 8, top - 32), (fx + 2, top - 12),
                   (fx + 12, top - 38), (fx + 24, top + 4)], fill=(255, 110, 20))
        d.polygon([(fx - 10, top + 4), (fx - 3, top - 16), (fx + 4, top - 4),
                   (fx + 11, top + 4)], fill=(255, 210, 60))
    return img


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 44
    x0, x1 = M, W - M
    cw = x1 - x0  # content width = 936

    # --- top dateline bar ---
    d.text((x0, 24), "TUESDAY, 24 NOVEMBER 2026", font=font(SANS_B, 19), fill=INK)
    right = "No. 328  •  FREE"
    d.text((x1 - d.textlength(right, font=font(SANS, 19)), 24),
           right, font=font(SANS, 19), fill=GREY)
    hrule(d, x0, x1, 52, 3)

    # --- masthead (auto-fit) ---
    title = "THE TUESDAY HERALD"
    tf, tw = fit_font(d, title, SERIF_B, 82, cw)
    d.text(((W - tw) / 2, 58), title, font=tf, fill=INK)
    hrule(d, x0, x1, 148, 2)
    d.text((x0, 156), "THE WORLD IN ONE PAGE",
           font=font(SANS_B, 17), fill=RED)
    right2 = "ALL THE NEWS THAT FITS"
    d.text((x1 - d.textlength(right2, font=font(SANS_B, 17)), 156),
           right2, font=font(SANS_B, 17), fill=GREY)

    # --- lead story ---
    y = 186
    f1, _ = fit_font(d, "NATO SENDS AWACS TO POLAND", SERIF_B, 46, cw)
    d.text((x0, y), "NATO SENDS AWACS TO POLAND", font=f1, fill=INK)
    y += 52
    f2, _ = fit_font(d, "AFTER RUSSIAN MISSILES LAND ON ALLIANCE SOIL",
                    SERIF_B, 30, cw)
    d.text((x0, y), "AFTER RUSSIAN MISSILES LAND ON ALLIANCE SOIL",
           font=f2, fill=RED)
    y += 42
    img.paste(draw_awacs(x0, y, x1, y + 172), (x0, y))
    y += 172 + 10
    y = para(d, x0, y,
             "NATO will deploy an early-warning AWACS aircraft to Poland after "
             "three Russian Kh-101 missiles landed on the alliance's eastern "
             "flank on Friday, Warsaw said — the starkest spillover scare of "
             "the Ukraine war yet.",
             font(SERIF, 20), cw, 26)
    hrule(d, x0, x1, y + 6, 1, GREY)

    # --- two secondary stories ---
    y += 18
    mid = (x0 + x1) // 2
    col_w = mid - x0 - 14
    img_h = 148
    # left: warship
    d.text((x0, y), "UKRAINE SINKS RUSSIAN", font=font(SERIF_B, 24), fill=INK)
    d.text((x0, y + 28), "WARSHIP IN LIBYA", font=font(SERIF_B, 24), fill=INK)
    img.paste(draw_warship(x0, y + 60, mid - 14, y + 60 + img_h), (x0, y + 60))
    d.text((x0, y + 60 + img_h + 6), "LIBYAN PORT  •  MARITIME DRONES",
           font=font(SANS_B, 14), fill=GREY)
    yy = para(d, x0, y + 60 + img_h + 28,
              "Kyiv said maritime drones sank a Russian corvette in a Libyan "
              "port on Sunday — a day after a drone hit a Russian-linked cargo "
              "ship in the Gulf of Finland.",
              font(SERIF, 17), col_w, 22)
    # right: factory fire
    rx = mid + 14
    d.text((rx, y), "FACTORY FIRE KILLS 24", font=font(SERIF_B, 24), fill=INK)
    d.text((rx, y + 28), "IN INDONESIA", font=font(SERIF_B, 24), fill=INK)
    img.paste(draw_fire(rx, y + 60, x1, y + 60 + img_h), (rx, y + 60))
    d.text((rx, y + 60 + img_h + 6), "BANTEN, INDONESIA  •  24 DEAD",
           font=font(SANS_B, 14), fill=GREY)
    yy2 = para(d, rx, y + 60 + img_h + 28,
               "At least 24 people died and around 30 are missing after a fire "
               "at a candy factory in Banten province, as rescuers kept "
               "searching through the night.",
               font(SERIF, 17), col_w, 22)
    y = max(yy, yy2) + 8
    hrule(d, x0, x1, y, 1, GREY)

    # --- briefs strip ---
    y += 14
    briefs = [
        ("CLIMATE", "COP31 talks collapse in Antalya — no deal on fossil fuels."),
        ("BUSINESS", "Nvidia's Huang returns as CEO; shares surge 31% in a day."),
        ("SPORT", "Verstappen wins the Las Vegas Grand Prix; Alcaraz takes ATP Finals."),
    ]
    bw = (cw - 2 * 20) // 3
    for i, (tag, txt) in enumerate(briefs):
        bx = x0 + i * (bw + 20)
        d.text((bx, y), tag, font=font(SANS_B, 16), fill=RED)
        para(d, bx, y + 24, txt, font(SANS, 17), bw, 22)
        if i < 2:
            d.line([(bx + bw + 10, y), (bx + bw + 10, y + 62)], fill=LIGHT, width=1)
    y += 92
    hrule(d, x0, x1, y, 3)
    d.text((x0, y + 10), "THE TUESDAY HERALD  •  TUESDAY, 24 NOVEMBER 2026  •  PAGE 1",
           font=font(SANS, 15), fill=GREY)
    return img


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    # verify gate: PNG, <=1024x1024, <=1 MiB
    with Image.open(path) as chk:
        if chk.format != "PNG":
            print("entry.png is not PNG", file=sys.stderr)
            return 1
        if chk.size[0] > 1024 or chk.size[1] > 1024:
            print("entry.png too large:", chk.size, file=sys.stderr)
            return 1
    size = os.path.getsize(path)
    if size > 1024 * 1024:
        print("entry.png over 1 MiB:", size, file=sys.stderr)
        return 1
    print(f"wrote entry.png {img.size[0]}x{img.size[1]}, {size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
