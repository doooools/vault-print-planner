"""Battery 1's oracle with the rules the user confirmed after it was frozen (2026-11-12), written to expected_corrected.json.
expected.json itself stays as it was frozen. Rules:
- runners: 2 guides + 2 slides + 2 stoppers per F (48 mm level) of the module, whatever the drawers in it;
- hidden key: `Hidden Key Part 2` once per stack, with one `Key Cap` (the user: "add keycap, the manual tells the truth").
Run: python -I tests/battery/corrections.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, "expected.json"), encoding="utf-8"))
# F of the modules per config (drawer modules only): runners are 2 per F of each module
MODULE_F = {"C02": [2], "C03": [4], "C08": [1, 2], "C10": [2]}
log = []
for cid, fs in MODULE_F.items():
    want = 2 * sum(fs)
    for p in E[cid]["parts"]:
        if re.search(r"Runner (Guide|Slide)\.stl$|Runner Stopper\.stl$", p["file"]) and p["qty"] != want:
            log.append(f"{cid}: {p['file'].split('/')[-1]} {p['qty']} -> {want}")
            p["qty"], p["source"] = want, "user rule: 2 per F of the module"
for p in E["C05"]["parts"]:
    if re.search(r"Hidden Key Part 2|/Key Cap\.stl$", p["file"]) and p["qty"] != 1:
        log.append(f"C05: {p['file'].split('/')[-1]} {p['qty']} -> 1")
        p["qty"], p["source"] = 1, "user rule: one removable hidden key per stack, with its key cap"
json.dump(E, open(os.path.join(HERE, "expected_corrected.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(HERE, "corrections.md"), "w", encoding="utf-8").write("# Corrections to battery 1's oracle (user rules)\n\n" + "\n".join("- " + l for l in log) + "\n")
print("\n".join(log))

# Battery 2: the backbone column, as the user asked ("follow the manual"): 2F backbones over the base (as 1F) and the
# modules under the top one, a 1F for an odd remainder. D27 = base + S6 2F under the top 1F: 3F, so 1 x S2F + 1 x S1F.
E2 = json.load(open(os.path.join(HERE, "expected2.json"), encoding="utf-8"))
log2 = []
parts = E2["D27"]["parts"]
if not any(p["file"].endswith("S1F Backbone.stl") for p in parts):
    parts.append({"file": "03. MODIFICATIONS/Backbone/S1F Backbone.stl", "qty": 1, "source": "user rule: backbone column per the manual (base + 2F = 3F: 2F + 1F)", "confidence": "medium", "note": ""})
    log2.append("D27: + 1 x S1F Backbone.stl (column base + 2F = 3F)")
json.dump(E2, open(os.path.join(HERE, "expected2_corrected.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(os.path.join(HERE, "corrections.md"), "a", encoding="utf-8") as fh:
    fh.write("\n# Corrections to battery 2's oracle (backbone column, user: follow the manual)\n\n" + "\n".join("- " + l for l in log2) + "\n")
print("\n".join(log2))
