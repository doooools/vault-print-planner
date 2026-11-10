"""Bambu Lab's PLA and PETG colours (Basic and Matte) for the planner's colour picker -> src/bambu-colors.tsv

Which colours: the ones on sale, read from the store's product pages. Their hex codes: Bambu's own table, the one
Bambu Studio and the AMS use (BambuStudio resources/profiles/BBL/filament/filaments_color_codes.json), matched by
the 5-digit colour code the store prints after each name ("Jade White (10100)"). A colour with no code or no hex in
Bambu's table is reported and left out, never guessed.

usage: python -I tools/bambu_colors.py src/bambu-colors.tsv
"""
import collections, json, re, sys, time, urllib.request

STORE = "https://eu.store.bambulab.com/products/"
CODES = "https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/filaments_color_codes.json"
LINES = [("pla-basic-filament", "PLA Basic"), ("pla-matte", "PLA Matte"), ("petg-basic", "PETG Basic"), ("petg-matte", "PETG Matte")]
# Colour options as the store's page data lists them: \"value\":\"Jade White (10100)\",\"newFlag
VALUE = re.compile(r'\\"value\\":\\"([^"\\]+?) ?\((\d{5})\)\\",\\"newFlag')


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (vault-print-planner colour list)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def main(out):
    sys.stdout.reconfigure(encoding="utf-8")
    by = collections.defaultdict(list)
    for x in json.loads(get(CODES))["data"]:
        by[x["fila_color_code"]].append(x)
    rows, problems = [], []
    for page, line in LINES:
        found = list(dict.fromkeys(VALUE.findall(get(STORE + page))))
        if not found:
            problems.append(f"{line}: no colours found on {STORE + page} (the page layout may have changed)")
        for name, code in found:
            hit = [x for x in by.get(code, []) if x["fila_type"] == line] or by.get(code, [])
            if not hit:
                problems.append(f"{line} {name} ({code}): not in Bambu's colour table")
                continue
            rows.append([line, code, name, ",".join(c[:7].upper() for c in hit[0]["fila_color"])])
        print(f"{line}: {len(found)} colours")
        time.sleep(1)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Bambu Lab PLA and PETG colours on sale (eu.store.bambulab.com), with the hex codes from Bambu's own table\n"
                "# (BambuStudio filaments_color_codes.json), matched by colour code. Made by tools/bambu_colors.py.\n"
                "# line\tcode\tname\thex (several for multicolour filament)\n")
        f.writelines("\t".join(r) + "\n" for r in rows)
    print(f"{len(rows)} colours -> {out}")
    for p in problems:
        print("  !", p)


if __name__ == "__main__":
    main(sys.argv[1])
