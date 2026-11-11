"""Assemble many recipes with blender_assemble.py, in parallel Blender processes.

  python run_assemble.py <out_root> <recipe.json> [...] [--jobs 6] [--views iso secx secz:23.5]

Each recipe goes to <out_root>/<family>/<name>(.blend, _iso.png, ...), family = the name's first
part (S3_1F -> S3). Recipes whose .blend is newer than the recipe are skipped.
"""
import argparse, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

BLENDER = os.environ.get("BLENDER", r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
HERE = os.path.dirname(os.path.abspath(__file__))

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("recipes", nargs="+")
ap.add_argument("--jobs", type=int, default=6)
ap.add_argument("--views", nargs="*", default=["iso", "front", "secx", "secz:23.5"])
ap.add_argument("--force", action="store_true")
a = ap.parse_args()


def one(rec):
    name = os.path.basename(rec).replace("_assembly.json", "")
    fam = name.split("_")[0]
    d = os.path.join(a.out, fam)
    os.makedirs(d, exist_ok=True)
    pre = os.path.join(d, name)
    if not a.force and os.path.exists(pre + ".blend") and os.path.getmtime(pre + ".blend") > os.path.getmtime(rec):
        return name, "skip"
    p = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "blender_assemble.py"), "--",
                        rec, pre, *a.views], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = "ASSEMBLED" in p.stdout
    if not ok:
        open(pre + "_error.txt", "w", encoding="utf-8").write(p.stdout[-4000:] + p.stderr[-4000:])
    return name, "ok" if ok else "FAILED"


with ThreadPoolExecutor(a.jobs) as ex:
    for name, st in ex.map(one, a.recipes):
        print(st, name, flush=True)
