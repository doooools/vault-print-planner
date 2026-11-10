import sys
from PIL import Image, ImageDraw
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).convert("RGB") for f in files]
w, h = ims[0].size; cols = 3 if len(ims) > 4 else 2; rows = (len(ims) + cols - 1) // cols
s = 0.5; W, H = int(w*s), int(h*s)
M = Image.new("RGB", (W*cols, H*rows), (40, 40, 40)); d = ImageDraw.Draw(M)
for i, (im, f) in enumerate(zip(ims, files)):
    x, y = (i % cols)*W, (i//cols)*H
    M.paste(im.resize((W, H)), (x, y)); d.text((x+10, y+10), f.split("_")[-1], fill=(255, 255, 0))
M.save(out)
