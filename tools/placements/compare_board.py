"""Side-by-side boards for checking assemblies against USSA's own renders, sized for a phone.

  python compare_board.py <board.json> <out.jpg>

board.json: {"title": "...", "rows": [{"left": "a.png", "left_crop": [x0, y0, x1, y1],
                                       "right": "b.png", "right_crop": [...],
                                       "left_text": "...", "right_text": "..."}, ...]}
Crops are fractions of the image (0-1). Each row: the reference on the left, our render on the right,
cropped to what matters and blown up, with a caption under each. Output ~1400 px wide JPEG.
The references are USSA's renders: keep the boards outside the repo.
"""
import json, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W, PAD, CW = 1400, 16, 684


def font(size):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def tile(path, crop):
    im = Image.open(path).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    return im.resize((CW, max(1, int(CW * im.size[1] / im.size[0]))), Image.LANCZOS)


cfg = json.load(open(sys.argv[1], encoding="utf-8"))
F_T, F_C = font(40), font(28)
blocks = []
for r in cfg["rows"]:
    a, b = tile(r["left"], r.get("left_crop")), tile(r["right"], r.get("right_crop"))
    h = max(a.size[1], b.size[1])
    la = textwrap.wrap(r.get("left_text", ""), 38)
    lb = textwrap.wrap(r.get("right_text", ""), 38)
    th = 36 * max(len(la), len(lb)) + 12
    blk = Image.new("RGB", (W, h + th + PAD), (255, 255, 255))
    blk.paste(a, (PAD // 2, (h - a.size[1]) // 2))
    blk.paste(b, (W // 2 + PAD // 2, (h - b.size[1]) // 2))
    d = ImageDraw.Draw(blk)
    d.line([(W // 2, 0), (W // 2, h + th)], fill=(200, 200, 200), width=3)
    for i, t in enumerate(la):
        d.text((PAD, h + 6 + 36 * i), t, font=F_C, fill=(30, 30, 30))
    for i, t in enumerate(lb):
        d.text((W // 2 + PAD, h + 6 + 36 * i), t, font=F_C, fill=(20, 60, 140))
    blocks.append(blk)
head = Image.new("RGB", (W, 70), (40, 40, 40))
ImageDraw.Draw(head).text((PAD, 12), cfg["title"], font=F_T, fill=(255, 255, 255))
H = 70 + sum(b.size[1] for b in blocks)
out = Image.new("RGB", (W, H), (255, 255, 255))
out.paste(head, (0, 0))
y = 70
for b in blocks:
    out.paste(b, (0, y))
    y += b.size[1]
out.save(sys.argv[2], quality=88)
print(sys.argv[2], out.size)
