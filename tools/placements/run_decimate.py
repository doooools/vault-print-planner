"""Driver: split a set of STL files over N parallel Blender workers.

  python run_decimate.py <src_root> <dst_root> [--max 40000] [--jobs 6] [--filter SUBSTR ...]

Files already present in dst_root are skipped (so it can be resumed).
Writes dst_root/_decimate_log.jsonl (one line per file).
"""
import argparse, os, subprocess, sys, tempfile

BLENDER = os.environ.get("BLENDER", r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
HERE = os.path.dirname(os.path.abspath(__file__))

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--max", type=int, default=40000)
ap.add_argument("--jobs", type=int, default=6)
ap.add_argument("--filter", nargs="*", default=[], help="keep files whose relative path contains one of these")
ap.add_argument("--list", help="text file with relative paths to process (overrides scan)")
a = ap.parse_args()

if a.list:
    with open(a.list, encoding="utf-8") as f:
        rels = [l.strip() for l in f if l.strip()]
else:
    rels = []
    for root, _, files in os.walk(a.src):
        for fn in files:
            if fn.lower().endswith(".stl"):
                rels.append(os.path.relpath(os.path.join(root, fn), a.src))
    if a.filter:
        rels = [r for r in rels if any(s.lower() in r.replace("\\", "/").lower() for s in a.filter)]

todo = [r for r in rels if not os.path.exists(os.path.join(a.dst, r))]
# biggest first, dealt round-robin, so workers finish at about the same time
todo.sort(key=lambda r: -os.path.getsize(os.path.join(a.src, r)))
print(f"{len(rels)} files selected, {len(todo)} to do, {a.jobs} workers")
if not todo:
    sys.exit(0)

os.makedirs(a.dst, exist_ok=True)
log = os.path.join(a.dst, "_decimate_log.jsonl")
tmp = tempfile.mkdtemp(prefix="vault_dec_")
procs = []
for j in range(a.jobs):
    chunk = todo[j::a.jobs]
    if not chunk:
        continue
    lf = os.path.join(tmp, f"list_{j}.txt")
    with open(lf, "w", encoding="utf-8") as f:
        f.write("\n".join(chunk))
    wlog = os.path.join(tmp, f"log_{j}.jsonl")
    out = open(os.path.join(tmp, f"stdout_{j}.txt"), "w", encoding="utf-8")
    p = subprocess.Popen([BLENDER, "-b", "--factory-startup", "--python",
                          os.path.join(HERE, "blender_decimate.py"), "--",
                          lf, a.src, a.dst, str(a.max), wlog], stdout=out, stderr=subprocess.STDOUT)
    procs.append((p, wlog))
for p, _ in procs:
    p.wait()
with open(log, "a", encoding="utf-8") as L:
    for _, wlog in procs:
        if os.path.exists(wlog):
            L.write(open(wlog, encoding="utf-8").read())
print("finished, log:", log)
