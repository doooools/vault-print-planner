"""Bolt shapes from their standard sizes, as the page makes them (src/template.html, hwProfile / hwRevolve).

Plain Python (no numpy), so Blender can use it too. A bolt's own frame: +Y from its tip to its head, origin on its
axis where the head bears (the top of a countersunk head), shank from y = 0 to y = -length. Threads aren't drawn;
the hex key hole is simplified.
"""
import math, re


def spec_size(spec, sizes):
    m = re.match(r"(M(\d+))(?:x([\d.]+))? (\w+)$", spec)
    if not m:
        return None
    sz = {"d": float(m.group(2))} if m.group(4) == "rod" else sizes.get(m.group(4), {}).get(m.group(1))
    return sz and {**sz, "L": float(m.group(3) or 0), "kind": m.group(4)}


def profile(s):
    """Rings from the tip up: (radius, y) or (radius, y, True) for a hexagon (radius = half across flats)."""
    rs, L, R = s["d"] / 2, s["L"], s.get("dk", 0) / 2
    c = min(0.4, rs * 0.2)
    tip = [(0, -L), (rs - c, -L), (rs, -L + c)]

    def key(y):
        return [(s["s"] * 0.6, y), (s["s"] / 2, y, True), (s["s"] / 2, y - s["t"], True), (0, y - s["t"] - s["s"] * 0.25)]
    k = s.get("k", 0)
    if s["kind"] == "button":
        dome = [(s["s"] * 0.6 + (R - s["s"] * 0.6) * math.cos(j / 6 * math.pi / 2), k * (0.18 + 0.82 * math.sin(j / 6 * math.pi / 2)))
                for j in range(6)]
        return tip + [(rs, 0), (R, 0)] + dome + key(k)
    if s["kind"] == "countersunk":
        return tip + [(rs, -(R - rs)), (R, 0)] + key(0)
    if s["kind"] == "socket":
        return tip + [(rs, 0), (R, 0), (R, k - 0.08 * s["dk"]), (R - 0.08 * s["dk"], k)] + key(k)
    if s["kind"] == "hex":
        return tip + [(rs, 0), (R, 0, True), (R, k, True), (0, k)]
    if s["kind"] == "nut":
        return [(rs, 0), (R, 0, True), (R, k, True), (rs, k), (rs, 0)]
    if s["kind"] == "rod":
        return [(0, -L), (rs, -L), (rs, 0), (0, 0)]
    return None


def revolve(prof, n=24):
    """Vertices and quads of the surface of revolution about +Y (n a multiple of 6: hexagon corners are vertices)."""
    verts, faces = [], []
    for ring in prof:
        r, y, hexa = ring[0], ring[1], len(ring) > 2 and ring[2]
        for i in range(n):
            a = 2 * math.pi * i / n
            rr = r / math.cos((a + math.pi / 6) % (math.pi / 3) - math.pi / 6) if hexa else r
            verts.append((rr * math.cos(a), y, -rr * math.sin(a)))
    for k in range(len(prof) - 1):
        for i in range(n):
            a, b = k * n + i, k * n + (i + 1) % n
            faces.append((a, b, b + n, a + n))
    return verts, faces

