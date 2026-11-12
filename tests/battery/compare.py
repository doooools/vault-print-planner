"""Compare the frozen oracle (tests/battery/expected.json) with the planner captures (tests/battery/planner/*.json).

Planner quantities include the planner's own +10 % spares on small loose parts ("incl. N spare" in the label): the
comparison uses the quantity without them (base) and shows the spares apart.
Run: python -I tests/battery/compare.py [1c|2|2c] -> tests/battery/comparison_raw.md (comparison2_raw.md for the second battery)
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.environ.get("VAULT_DOWNLOAD", "")  # the 261021_VAULT_USSA_S folder: only used to flag paths not on disk
CAPTURE = {"C01": "C01", "C02": "C02", "C03": "C03", "C04": "C04", "C05": "C05", "C06": "C06", "C07": "C07", "C08": "C08",
           "C09": "C09", "C10": "C10", "C11": "C11", "C12": "C12", "C13": "C13", "C14": "C14"}


def norm(p):
    # the download spells "²" as the mojibake "┬▓" in its folder and file names; the page matches both
    p = p.replace("┬▓", "²")
    return re.sub(r"\s+", " ", p.replace("\\", "/").strip().lower()).replace(" .stl", ".stl")


def planner_lines(d):
    out = {}
    for p in d["parts"]:
        m = re.search(r"incl\. (\d+) spare", p["label"])
        spare = int(m.group(1)) if m else 0
        k = norm(p["file"])
        e = out.setdefault(k, {"file": p["file"], "q": 0, "spare": 0, "label": re.sub(r"\s*incl\. \d+ spare", "", p["label"])})
        e["q"] += p["q"] - spare
        e["spare"] += spare
    return out


def compare(exp, plan):
    rows = []
    for k in sorted(set(exp) | set(plan)):
        e, p = exp.get(k), plan.get(k)
        eq = e["qty"] if e else 0
        pq = p["q"] if p else 0
        rows.append({"file": (e or p)["file"], "exp": eq, "plan": pq, "spare": p["spare"] if p else 0, "ok": eq == pq,
                     "conf": e.get("confidence", "") if e else "", "src": e.get("source", "") if e else "", "note": e.get("note", "") if e else ""})
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    second = len(sys.argv) > 1 and sys.argv[1] in ("2", "2c")
    second_c = len(sys.argv) > 1 and sys.argv[1] == "2c"
    corrected = len(sys.argv) > 1 and sys.argv[1] == "1c"
    E = json.load(open(os.path.join(HERE, "expected2_corrected.json" if second_c else "expected2.json" if second else "expected_corrected.json" if corrected else "expected.json"), encoding="utf-8"))
    cap_map = {k: k for k in E if k.startswith("D")} if second else CAPTURE
    on_disk = set()
    for root, _, files in os.walk(VAULT):
        for f in files:
            on_disk.add(norm(os.path.relpath(os.path.join(root, f), VAULT)))
    out = ["# Oracle vs planner (raw)", ""]
    summary = {}
    for cid, cap in cap_map.items():
        d = json.load(open(os.path.join(HERE, "planner", cap + ".json"), encoding="utf-8"))
        ex = {}
        for p in E[cid]["parts"]:
            k = norm(p["file"])
            if k in ex:
                ex[k]["qty"] += p["qty"]
            else:
                ex[k] = dict(p)
        rows = compare(ex, planner_lines(d))
        bad = [r for r in rows if not r["ok"]]
        summary[cid] = {"files_exp": len(ex), "copies_exp": sum(v["qty"] for v in ex.values()), "files_plan": len(d["parts"]),
                        "copies_plan": sum(r["plan"] for r in rows), "gaps": len(bad)}
        out.append(f"## {cid} ({d['meta']['cfg']})")
        out.append(f"expected {summary[cid]['copies_exp']} copies / {summary[cid]['files_exp']} files; planner {summary[cid]['copies_plan']} copies (+ spares) / {summary[cid]['files_plan']} files; {len(bad)} gap(s)")
        out.append("")
        out.append("| file | expected | planner | spares | | oracle source / note |")
        out.append("|---|---|---|---|---|---|")
        for r in rows:
            miss = "" if not VAULT or norm(r["file"]) in on_disk else " (NOT ON DISK)"
            out.append(f"| {r['file']}{miss} | {r['exp']} | {r['plan']} | {r['spare'] or ''} | {'ok' if r['ok'] else '**GAP**'} | {r['conf']} {r['src']} {r['note']} |".replace("\n", " "))
        out.append("")
        if E[cid].get("notes"):
            out.append("Oracle notes: " + str(E[cid]["notes"]).replace("\n", " "))
            out.append("")
    out.insert(2, "| config | expected copies | planner copies | gaps |\n|---|---|---|---|\n" + "\n".join(
        f"| {k} | {v['copies_exp']} | {v['copies_plan']} | {v['gaps']} |" for k, v in summary.items()) + "\n")
    open(os.path.join(HERE, "comparison2c_raw.md" if second_c else "comparison2_raw.md" if second else "comparison1c_raw.md" if corrected else "comparison_raw.md"), "w", encoding="utf-8").write("\n".join(out))
    print("\n".join(out))


main()
