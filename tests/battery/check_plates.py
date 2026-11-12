"""Plate checks on the planner captures (tests/battery/planner/*.json), without the oracle.

For every capture: copies on the plates = list quantity for each file (nothing dropped, nothing duplicated), every
drawn part inside its bed and out of the no-print corner, no two parts overlapping, one drawn shape per copy, an
oversized part flagged, and the Design tab's level lists against the Print tab's list.
Run: python -I tests/battery/check_plates.py  -> tests/battery/plate_checks.md
"""
import json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "planner")


def fname(p):
    # whitespace collapsed: the plate rows are read as text, which folds "XL3  Roof.stl" (two spaces, as on disk)
    return re.sub(r"\s+", " ", p.rsplit("/", 1)[-1])


def check(d):
    issues, info = [], []
    parts = d["parts"]
    by_name = defaultdict(list)
    for p in parts:
        by_name[fname(p["file"])].append(p)
    listed = Counter()
    for p in parts:
        listed[p["file"]] += p["q"]
    on_plates = Counter()
    for pl in d["plates"]:
        rows_sum = sum(r["count"] for r in pl["rows"])
        if pl["shapes"] != rows_sum:
            issues.append(f"plate {pl['n']}: {pl['shapes']} shapes drawn for {rows_sum} copies listed")
        if pl["out_of_bed"]:
            issues.append(f"plate {pl['n']}: {len(pl['out_of_bed'])} shape(s) past the bed edge {pl['bed']}")
        if pl.get("in_noprint"):
            issues.append(f"plate {pl['n']}: {len(pl['in_noprint'])} shape(s) in the no-print corner")
        if pl["clashes"]:
            issues.append(f"plate {pl['n']}: shapes overlap {pl['clashes']}")
        for r in pl["rows"]:
            c = by_name.get(r["file"], [])
            if len(c) != 1:
                issues.append(f"plate {pl['n']}: row file {r['file']!r} matches {len(c)} list lines")
                key = r["file"]
            else:
                key = c[0]["file"]
            on_plates[key] += r["count"]
    bad_fit = [p for p in parts if any(t in ("Doesn't fit", "Only fits tipped over") for t in p["tags"])]
    for p in parts:
        want = 0 if p in bad_fit else p["q"]
        got = on_plates.get(p["file"], 0)
        if got != want:
            issues.append(f"{fname(p['file'])}: list {p['q']}{' (does not fit: 0 expected on plates)' if p in bad_fit else ''}, plates {got}")
    for k in on_plates:
        if k not in listed and k not in by_name:
            issues.append(f"{k}: on plates ({on_plates[k]}) but not in the list")
    if bad_fit:
        flagged = any(re.search(r"no longer fit|left out of the plates|won.t fit|doesn.t fit", a, re.I) for a in d["alerts"])
        info.append(f"oversized: {', '.join(fname(p['file']) + ' ' + p['dims'] for p in bad_fit)}; Print alert shown: {'yes' if flagged else 'NO'}")
        if not flagged:
            issues.append("oversized parts have no visible alert in Print")
    warn = [p for p in parts if any(t.startswith("Fits diag") or "angle" in t for t in p["tags"])]
    if warn:
        info.append("placed turned: " + ", ".join(fname(p["file"]) + " (" + "/".join(t for t in p["tags"] if t.startswith("Fits")) + ")" for p in warn))
    # Design tab level lists vs the Print list (roof and stack parts are listed apart in Design)
    lv = Counter()
    seen_units = set()
    for L in d.get("levels", []):
        if "parts" not in L:
            continue
        sig = (L["unit"], L["head"])
        if sig in seen_units:
            info.append(f"Design list of '{L['unit']}' read once (two modules share the name)")
            continue
        seen_units.add(sig)
        for p in L["parts"]:
            if p["file"]:
                lv[p["file"]] += p["q"]
    if lv:
        diff = []
        for k in sorted(set(lv) | set(listed)):
            if lv.get(k, 0) != listed.get(k, 0):
                diff.append(f"{fname(k)}: Design {lv.get(k, 0)} / Print {listed.get(k, 0)}")
        if diff:
            info.append("Design level lists vs Print: " + "; ".join(diff))
    return issues, info


def main():
    names = sorted(f for f in os.listdir(SRC) if f.endswith(".json") and not f.startswith("_"))
    out = ["# Plate checks (planner captures, no oracle)", "",
           "Each capture: copies on plates = list quantity per file; shapes inside the bed, outside the no-print corner, not overlapping; one shape per copy; oversized parts flagged; Design level lists vs Print list.", ""]
    for n in names:
        d = json.load(open(os.path.join(SRC, n), encoding="utf-8"))
        issues, info = check(d)
        pr = d.get("printer") or {}
        total = sum(p["q"] for p in d["parts"])
        out.append(f"## {n[:-5]} ({pr.get('id')}, {pr.get('v')}) - {d['meta'].get('cfg')}")
        out.append(f"- list: {len(d['parts'])} files, {total} copies; plates: {len(d['plates'])}; {d['top']}")
        for a in d["alerts"]:
            out.append(f"- Print alert: {a[:300]}")
        for i in info:
            out.append(f"- note: {i}")
        out.append("- **OK**" if not issues else "- **PROBLEMS**:")
        for i in issues:
            out.append(f"  - {i}")
        out.append("")
    open(os.path.join(HERE, "plate_checks.md"), "w", encoding="utf-8").write("\n".join(out))
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(out))


main()
