"""Check the repository the way the CI does on every pull request (.github/workflows/check.yml).

usage: python -I tools/check.py

1. index.html is the build of src/ (rebuilt in a temporary file and compared, line ends ignored).
2. src/validate.js finds no problem, run on the download's file list (the paths in src/stl-measurements.tsv).
3. Every <script> of index.html parses (node, without running it).
4. No USSA geometry in the repository (STL, 3MF, .blend and other mesh files).

Needs Python 3 and Node.js on the PATH. Prints one line per check and exits 1 if any failed.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

root = pathlib.Path(__file__).resolve().parent.parent
src = root / "src"
failed = []


def report(name, ok, detail=""):
    print(("ok    " if ok else "FAIL  ") + name)
    if detail:
        print("      " + detail.strip().replace("\n", "\n      "))
    if not ok:
        failed.append(name)


def run(args, **kw):
    return subprocess.run(args, cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)

    # 1. The published page is the build of src/
    built = tmp / "index.html"
    b = run([sys.executable, "-I", str(src / "build.py"), "--public", str(src / "stl-measurements.tsv"), str(built),
             str(root / "previews" / "index.tsv")])
    if b.returncode:
        report("build.py runs", False, b.stdout + b.stderr)
    else:
        norm = lambda p: p.read_bytes().replace(b"\r\n", b"\n")
        have, want = norm(root / "index.html"), norm(built)
        detail = ""
        if have != want:
            hl, wl = have.split(b"\n"), want.split(b"\n")
            n = next((i for i, (x, y) in enumerate(zip(hl, wl)) if x != y), min(len(hl), len(wl)))
            detail = (f"index.html differs from the build of src/ from line {n + 1}. Rebuild it and commit it:\n"
                      "python -I src/build.py --public src/stl-measurements.tsv index.html previews/index.tsv")
        report("index.html is the build of src/", have == want, detail)

    # 2. The rules against the download's file list
    paths = [line.split("\t", 1)[0] for line in (src / "stl-measurements.tsv").read_text(encoding="utf-8").strip().split("\n")]
    files = tmp / "files.txt"
    files.write_text("\n".join(paths) + "\n", encoding="utf-8")
    v = run(["node", str(src / "validate.js"), str(files)])
    out = (v.stdout + v.stderr).split("\nUNUSED FILES:")[0]
    report("validate.js", v.returncode == 0, out if v.returncode else "")

    # 3. The page's scripts parse (vm.Script compiles a classic script without running it)
    page = (root / "index.html").read_text(encoding="utf-8")
    bad = []
    for i, m in enumerate(re.finditer(r"<script>(.*?)</script>", page, re.S)):
        js = tmp / f"script{i}.js"
        # pad with the lines before it, so an error's line number is index.html's
        js.write_text("\n" * page.count("\n", 0, m.start(1)) + m.group(1), encoding="utf-8")
        s = run(["node", "-e", "const f = process.argv[1]; new (require('vm').Script)(require('fs').readFileSync(f, 'utf8'), { filename: 'index.html' })", str(js)])
        if s.returncode:
            bad.append(s.stderr.strip().split("\n\n")[0])
    report("the page's scripts parse", not bad, "\n".join(bad))

# 4. No USSA geometry committed (CLAUDE.md, hard rules): only numbers measured from the files may be in the repository
MESH = re.compile(r"\.(stl|3mf|blend\d*|obj|ply|glb|gltf|fbx|step|stp|amf|drc)$", re.I)
g = run(["git", "ls-files", "-z"])
listed = g.stdout.split("\0") if g.returncode == 0 else [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
mesh = [p for p in listed if MESH.search(p)]
report("no mesh files in the repository", not mesh, "\n".join(mesh[:20]))

print(f"\n{len(failed)} check{'s' if len(failed) != 1 else ''} failed" if failed else "\nAll checks passed")
sys.exit(1 if failed else 0)
