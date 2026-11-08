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

# How far Bambu's supports reach past each part at any layer, from slicing it alone with the planner's settings
# (src/bambu-reach.tsv: path, printer, support reach, auto brim reach, skirt reach, warning). The packer keeps
# neighbours that far away, since supports, unlike brims, aren't trimmed around other parts.
reach = {}
rf = here / "bambu-reach.tsv"
if rf.exists():
    for line in rf.read_text().strip().split("\n"):
        c = line.split("\t")
        if len(c) > 2 and c[2]:
            reach[c[0]] = round(float(c[2]), 1)

rows = []
for line in pathlib.Path(foot).read_text().strip().split("\n"):
    p, bx, by, bz, vol, fa, fb, ang = line.split("\t")
    a, b = sorted((float(fa), float(fb)), reverse=True)
    # Round parts (keys, knobs, disks): turning them doesn't shrink their footprint, so keep them as exported
    if float(bx) * float(by) <= float(fa) * float(fb) * 1.03:
        a, b, ang = *sorted((float(bx), float(by)), reverse=True), "0"
    rows.append([p, a, b, float(bz), int(float(vol)), float(ang)] + thumbs.get(p, [0, 0]) + [1 if p in needs else 0, reach.get(p, -1)])

catalog = "window.VAULT_FILES=" + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";"
# Bambu Studio's own project settings per printer (src/bambu-settings/<printer id>.json, each saved by Bambu Studio itself).
# Keys every printer shares are stored once.
sets = {f.stem: json.loads(f.read_text()) for f in sorted((here / "bambu-settings").glob("*.json"))}
base = {k: v for k, v in next(iter(sets.values()), {}).items() if all(k in d and d[k] == v for d in sets.values())}
bambu = {"base": base, "per": {i: {k: v for k, v in d.items() if k not in base} for i, d in sets.items()}}
catalog += "window.BAMBU_SETTINGS=" + json.dumps(bambu, ensure_ascii=False, separators=(",", ":")) + ";"
# Bed sizes for the "My printer isn't listed" lookup (src/printer-beds.tsv, from OrcaSlicer's profiles by src/orca-beds.py)
beds = [l.split("\t") for l in (here / "printer-beds.tsv").read_text().splitlines() if l and not l.startswith("#")]
catalog += "window.PRINTER_BEDS=" + json.dumps([[b, m, int(w), int(d), int(h)] for b, m, w, d, h in beds], ensure_ascii=False, separators=(",", ":")) + ";"
html = (here / "template.html").read_text()
if public:
    catalog += "window.VAULT_PUBLIC=true;"
    html = re.sub(r'<script type="text/plain" id="py3mf">.*?</script>\n', "", html, flags=re.S)
    html = re.sub(r"const SRC_DEFAULT = '[^']*/", "const SRC_DEFAULT = '", html)
    # The VaultPrint helper and Terminal script only work on the author's Mac (the public template has them removed already)
    html = re.sub(r"  /\*MAC\*/.*?/\*END MAC\*/", "  const macPanel = () => '', bindMac = () => {};", html, flags=re.S)
# What's new (header button opens it): src/public/CHANGELOG.md, every date
def changelog_html():
    import html as h
    days, cur = [], None
    for line in (here / "public" / "CHANGELOG.md").read_text().splitlines():
        if line.startswith("## "):
            cur = [line[3:].strip(), []]; days.append(cur)
        elif line.startswith("- ") and cur:
            t = h.escape(line[2:].strip(), quote=False)
            t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
            t = re.sub(r"\[(.+?)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
            cur[1].append(f"<li>{t}</li>")
    day = lambda d: f'<h3>{d[0]}</h3><ul>{"".join(d[1])}</ul>'
    return "".join(day(d) for d in days)
html = html.replace("<!--CHANGELOG-->", changelog_html())
html = html.replace("/*CATALOG*/", catalog).replace("/*RULES*/", (here / "rules.js").read_text())
pathlib.Path(out).write_text(html)
print(f"{len(rows)} files -> {out} ({len(html) // 1024} KB)")
