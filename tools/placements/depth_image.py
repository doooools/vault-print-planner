"""Turn a blender_probe depth map (.npy) into a PNG with a mm grid.  python depth_image.py <prefix>"""
import sys, json, numpy as np
from PIL import Image, ImageDraw
pre = sys.argv[1]
d = np.load(pre + "_depth.npy"); meta = json.load(open(pre + "_depth.json"))
v = d[~np.isnan(d)]; lo, hi = np.percentile(v, 1), np.percentile(v, 99)
t = np.clip((d - lo) / (hi - lo + 1e-9), 0, 1)
if meta["axis"][0] == "+": t = 1 - t
g = (40 + 215 * (1 - t)).astype(np.uint8)
rgb = np.stack([g, g, g], -1); rgb[np.isnan(d)] = (200, 30, 30)
im = Image.fromarray(rgb[::-1]).resize((d.shape[1] * 3, d.shape[0] * 3), Image.NEAREST)
dr = ImageDraw.Draw(im); s = meta["step"]; H = im.size[1]
for k in range(0, int(d.shape[1] * s), 10):
    x = int(k / s * 3); dr.line([(x, 0), (x, H)], fill=(0, 120, 255)); dr.text((x + 2, 2), f"{meta['u']}{meta['u0'] + k:.0f}", fill=(0, 200, 255))
for k in range(0, int(d.shape[0] * s), 5):
    y = H - int(k / s * 3); dr.line([(0, y), (im.size[0], y)], fill=(0, 90, 200)); dr.text((2, y - 12), f"{meta['w']}{meta['w0'] + k:.1f}", fill=(0, 200, 255))
im.save(pre + "_depth.png"); print("saved", pre + "_depth.png", im.size)
