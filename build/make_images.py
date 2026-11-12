#!/usr/bin/env python3
"""Renders app icons and the social share image (og.png) if they are missing.
Requires Pillow. Used by the GitHub Action so binary images never need to be committed by hand."""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
TARGETS = [os.path.join(IMG, n) for n in ("icon-192.png", "icon-512.png", "og.png")]

if all(os.path.exists(t) for t in TARGETS) and "--force" not in sys.argv:
    print("Images present; nothing to do.")
    sys.exit(0)

from PIL import Image, ImageDraw, ImageFont

INK, AMB, WHITE, MUTE = (11, 27, 43), (255, 183, 3), (255, 255, 255), (195, 209, 222)
BOLD = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
REG = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
       "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]


def font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def logo(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * .275), fill=INK)
    k = s / 40
    d.ellipse([8 * k, 8 * k, 28 * k, 28 * k], outline=AMB, width=max(2, int(3.2 * k)))
    d.line([(25.5 * k, 25.5 * k), (32 * k, 32 * k)], fill=AMB, width=max(2, int(3.6 * k)))
    bolt = [(19.6, 10.5), (13.8, 19), (18.2, 19), (16.6, 26.5), (22.8, 17.3), (18.3, 17.3)]
    d.polygon([(x * k, y * k) for x, y in bolt], fill=WHITE)
    return im


os.makedirs(IMG, exist_ok=True)
for n in (192, 512):
    logo(n).save(os.path.join(IMG, f"icon-{n}.png"))

W, H = 1200, 630
im = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(im)
for x in range(0, W, 44):
    d.line([(x, 0), (x, H)], fill=(22, 40, 58))
for y in range(0, H, 44):
    d.line([(0, y), (W, y)], fill=(22, 40, 58))
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g = ImageDraw.Draw(glow)
for r in range(320, 0, -8):
    g.ellipse([W - 260 - r, 80 - r, W - 260 + r, 80 + r], fill=(255, 183, 3, int(70 * (1 - r / 320))))
im = Image.alpha_composite(im.convert("RGBA"), glow)
d = ImageDraw.Draw(im)
L = logo(120)
im.paste(L, (80, 80), L)
f64 = font(BOLD, 64)
d.text((222, 98), "Express", font=f64, fill=WHITE)
d.text((222 + d.textlength("Express", font=f64), 98), "Find", font=f64, fill=AMB)
f76 = font(BOLD, 72)
d.text((80, 250), "Home emergency?", font=f76, fill=WHITE)
d.text((80, 340), "Find the right pro fast.", font=f76, fill=AMB)
d.text((80, 470), "Safety-first steps  ·  Honest cost guides  ·  Free quotes from up to 3 local pros", font=font(REG, 26), fill=MUTE)
d.text((80, 530), "US & Canada  ·  expressfind.com", font=font(REG, 24), fill=(140, 165, 190))
im.convert("RGB").save(os.path.join(IMG, "og.png"), optimize=True)
print("Images rendered.")
