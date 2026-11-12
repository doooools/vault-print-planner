"""Battery test server (run: VAULT_DOWNLOAD=<folder> python -I serve.py 8913): the page from the worktree, the Vault files read-only, and a save endpoint for results."""
import http.server, json, os, sys, urllib.parse

# the repo (index.html) is three folders up; the Vault download comes from VAULT_DOWNLOAD (the 261021_VAULT_USSA_S folder)
WT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
VAULT = os.environ.get("VAULT_DOWNLOAD") or sys.exit("Set VAULT_DOWNLOAD to your 261021_VAULT_USSA_S folder")
OUT = os.path.join(WT, "tests", "battery", "planner")


def listing():
    out = []
    for root, dirs, files in os.walk(VAULT):
        rel = os.path.relpath(root, VAULT).replace("\\", "/")
        if rel.startswith("_planner"):
            continue
        for f in files:
            if f.lower().endswith(".stl"):
                p = f if rel == "." else rel + "/" + f
                out.append([p, os.path.getsize(os.path.join(root, f))])
    return out


class H(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        p = urllib.parse.unquote(u.path)
        if p in ("/", "/index.html"):
            with open(os.path.join(WT, "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if p.startswith("/js/") and "/" not in p[4:] and p.endswith(".js"):
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), p[4:]), "rb") as f:
                return self._send(200, f.read(), "text/javascript")
        if p == "/vault-list.json":
            return self._send(200, json.dumps(listing()).encode(), "application/json")
        if p.startswith("/vault/"):
            rel = p[len("/vault/"):]
            full = os.path.normpath(os.path.join(VAULT, rel))
            if not full.startswith(os.path.normpath(VAULT)) or not os.path.isfile(full):
                return self._send(404, b"no", "text/plain")
            with open(full, "rb") as f:
                return self._send(200, f.read(), "application/octet-stream")
        return self._send(404, b"no", "text/plain")

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        if u.path != "/save":
            return self._send(404, b"no", "text/plain")
        name = urllib.parse.parse_qs(u.query)["name"][0]
        if "/" in name or "\\" in name or ".." in name:
            return self._send(400, b"bad", "text/plain")
        n = int(self.headers["Content-Length"])
        data = self.rfile.read(n)
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, name), "wb") as f:
            f.write(data)
        return self._send(200, b"ok", "text/plain")

    def log_message(self, *a):
        pass


http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8765), H).serve_forever()
