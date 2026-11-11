"""Index the Vault download: triangle count and bounding box of every STL, as downloaded.

  python stl_index.py <vault_download> <out.jsonl>

One JSON line per file: {"file", "tris", "bbox_min", "bbox_max", "mb"}. Paths use "/" and are
relative to the download, like stl-measurements.tsv. Reads binary STL with numpy (memory-mapped),
so a full pass over the 733 files takes a few minutes. Numbers only, no geometry.
"""
import json, os, sys
import numpy as np

REC = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def bbox(path):
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        head = f.read(84)
    n = int.from_bytes(head[80:84], "little")
    if 84 + 50 * n == size:
        recs = np.memmap(path, dtype=REC, mode="r", offset=84, shape=(n,))
        v = recs["v"].reshape(-1, 3)
        lo, hi = np.empty(3), np.empty(3)
        step = 2_000_000
        lo[:] = np.inf
        hi[:] = -np.inf
        for i in range(0, len(v), step):
            c = np.asarray(v[i:i + step], dtype=np.float64)
            lo = np.minimum(lo, c.min(0))
            hi = np.maximum(hi, c.max(0))
        del recs
        return n, lo, hi
    # ASCII STL
    pts = []
    with open(path, "r", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s.startswith("vertex"):
                pts.append([float(x) for x in s.split()[1:4]])
    p = np.array(pts)
    return len(p) // 3, p.min(0), p.max(0)


def main():
    src, out = sys.argv[1], sys.argv[2]
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["file"] for l in open(out, encoding="utf-8")}
    with open(out, "a", encoding="utf-8") as o:
        for root, _, files in os.walk(src):
            for fn in sorted(files):
                if not fn.lower().endswith(".stl"):
                    continue
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, src).replace("\\", "/")
                if rel in done:
                    continue
                n, lo, hi = bbox(full)
                o.write(json.dumps({"file": rel, "tris": n, "bbox_min": [round(x, 3) for x in lo],
                                    "bbox_max": [round(x, 3) for x in hi],
                                    "mb": round(os.path.getsize(full) / 1e6, 1)}, ensure_ascii=False) + "\n")
                o.flush()


if __name__ == "__main__":
    main()
