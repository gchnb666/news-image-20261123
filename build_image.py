#!/usr/bin/env python3
"""Compose the 1024x1024 front-page image for news-image-20261123.

Renders all text with PIL (crisp, no garbled text) and crops a generated
editorial illustration (assets/cop31-hero.webp, an empty UN-style summit
hall with a glowing Earth) into the lead slot. Run: python3 build_image.py
Writes entry.png (1024x1024, under 1 MiB). Requires Pillow locally only;
the entry itself is shipped as entry.png and main.py just copies it.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (15, 42, 74)
AMBER = (245, 176, 65)
INK = (18, 18, 18)
GREY = (90, 90, 90)
RED = (178, 34, 34)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 96], fill=NAVY)
d.text((32, 12), "WORLD NEWS", font=font(SERIF_B, 56), fill="white")
d.text((32, 64), "MONDAY, 23 NOVEMBER 2026", font=font(SANS_B, 25), fill=AMBER)
d.text((W - 32, 20), "THE DAY IN", font=font(SANS_B, 23), fill="white", anchor="ra")
d.text((W - 32, 52), "ONE IMAGE", font=font(SANS_B, 23), fill="white", anchor="ra")

y = 96
# ---- lead kicker + headline (one line) ----
y += 14
d.text((32, y), "CLIMATE  •  TURKEY", font=font(SANS_B, 21), fill=RED)
y += 30
d.text((32, y), "COP31 climate talks collapse", font=font(SANS_B, 44), fill=INK)
y += 54
y += 8

# ---- hero image ----
hero = Image.open("assets/cop31-hero.webp").convert("RGB")
hero = hero.crop((0, 110, 1920, 710)).resize((W - 64, 290), Image.LANCZOS)
img.paste(hero, (32, y))
y += 290 + 10
# ---- lead summary ----
lead = "UN summit ends without agreement as nations split over fossil fuels; talks ran two days past schedule."
for line in wrap(d, lead, font(SANS, 25), W - 64):
    d.text((32, y), line, font=font(SANS, 25), fill=(40, 40, 40))
    y += 32
y += 8
d.line([(32, y), (W - 32, y)], fill=INK, width=2)
y += 14

# ---- secondary stories (headline + one-line summary each) ----
stories = [
    ("LIBYA", "Russian warship hit by suspected drone at Benghazi",
     "Fire rages at the port; UN calls for a probe into the attack."),
    ("UKRAINE", "Russian strikes kill 12 in Kyiv region",
     "Boy, 7, pulled alive from rubble as rescuers search for missing."),
    ("USA", "Democrats win biggest House majority since 1992",
     "North Carolina flip seals the majority after midterm gains."),
    ("ECONOMY", "South Korea exports top $1 trillion for first time",
     "AI chip demand drives a record year; fourth economy to pass $1tn."),
    ("EUROPE", "Lagarde to step down as ECB chief in February",
     "Central bank president ends her term early; successor race begins."),
]
for tag, head, summ in stories:
    d.text((32, y), tag, font=font(SANS_B, 19), fill=RED)
    d.text((165, y), head, font=font(SANS_B, 27), fill=INK)
    y += 32
    lines = wrap(d, summ, font(SANS, 21), W - 64 - 133)
    assert len(lines) == 1, (tag, lines)
    d.text((165, y), lines[0], font=font(SANS, 21), fill=GREY)
    y += 27
    y += 18

# ---- footer ----
d.line([(32, y + 2), (W - 32, y + 2)], fill=INK, width=2)
d.text((W // 2, y + 12), "23 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE IMAGE",
       font=font(SANS_B, 20), fill=GREY, anchor="ma")

# outer border
d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
