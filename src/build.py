"""Assemble vault-planner.html from template.html + rules.js + the STL measurement table.

usage: python3 -I build.py [--public] <foot.tsv> <out.html> [previews/index.tsv]
--public: the version for sharing. Leaves out the Mac-only VaultPrint helper and Terminal script, and this Mac's paths.
Leave out previews/index.tsv to build without part pictures.
foot.tsv columns: path, bbox dx, dy, dz, volume mm3, footprint a, footprint b, angle
index.tsv columns: path, sprite sheet number, cell in sheet (from the thumbnail packer)
"""
import json
import pathlib
import re
import sys

here = pathlib.Path(__file__).resolve().parent
public = "--public" in sys.argv
if public:
    sys.argv.remove("--public")
foot, out = sys.argv[1], sys.argv[2]
thumbs = {}
if len(sys.argv) > 3:
    for line in pathlib.Path(sys.argv[3]).read_text().strip().split("\n"):
        path, sheet, cell = line.split("\t")
        thumbs[path] = [int(sheet), int(cell)]

# Parts Bambu Studio warns about when sliced as exported without supports ("floating cantilever" and so on),
# from slicing every STL on its own: path, Bambu's warning (empty when it's happy)
needs = set()
audit = here / "bambu-support-audit.tsv"
if audit.exists():
    for line in audit.read_text().strip().split("\n"):
        path, _, msg = line.partition("\t")
        if "enable support" in msg:
            needs.add(path)

rows = []
for line in pathlib.Path(foot).read_text().strip().split("\n"):
    p, bx, by, bz, vol, fa, fb, ang = line.split("\t")
    a, b = sorted((float(fa), float(fb)), reverse=True)
    # Round parts (keys, knobs, disks): turning them doesn't shrink their footprint, so keep them as exported
    if float(bx) * float(by) <= float(fa) * float(fb) * 1.03:
        a, b, ang = *sorted((float(bx), float(by)), reverse=True), "0"
    rows.append([p, a, b, float(bz), int(float(vol)), float(ang)] + thumbs.get(p, [0, 0]) + [1 if p in needs else 0])

catalog = "window.VAULT_FILES=" + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";"
# Bambu Studio's own project settings per printer (src/bambu-settings/<printer id>.json, each saved by Bambu Studio itself).
# Keys every printer shares are stored once.
sets = {f.stem: json.loads(f.read_text()) for f in sorted((here / "bambu-settings").glob("*.json"))}
base = {k: v for k, v in next(iter(sets.values()), {}).items() if all(k in d and d[k] == v for d in sets.values())}
bambu = {"base": base, "per": {i: {k: v for k, v in d.items() if k not in base} for i, d in sets.items()}}
catalog += "window.BAMBU_SETTINGS=" + json.dumps(bambu, ensure_ascii=False, separators=(",", ":")) + ";"
html = (here / "template.html").read_text()
if public:
    catalog += "window.VAULT_PUBLIC=true;"
    html = re.sub(r'<script type="text/plain" id="py3mf">.*?</script>\n', "", html, flags=re.S)
    html = re.sub(r"const SRC_DEFAULT = '[^']*/", "const SRC_DEFAULT = '", html)
    # The VaultPrint helper and Terminal script only work on the author's Mac (the public template has them removed already)
    html = re.sub(r"  /\*MAC\*/.*?/\*END MAC\*/", "  const macPanel = () => '', bindMac = () => {};", html, flags=re.S)
html = html.replace("/*CATALOG*/", catalog).replace("/*RULES*/", (here / "rules.js").read_text())
pathlib.Path(out).write_text(html)
print(f"{len(rows)} files -> {out} ({len(html) // 1024} KB)")
