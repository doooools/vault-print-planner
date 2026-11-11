"""Keep one connected piece of an imported mesh (Blender side of vault_geom.pieces).

Some Vault files hold several parts printed side by side: both leaves of a case hinge, both
racks of a drawer, two hinge tops, two rods. A placement then names one piece by a point
{"piece": [x, y, z]} in the file's own coordinates: the piece (vertices welded at 1e-3 mm) whose
bounding-box centre is nearest to that point.
"""
import bmesh, mathutils


def keep_piece(me, pick, offset=(0.0, 0.0, 0.0)):
    """Delete every face of `me` that is not in the piece nearest to `pick`.
    offset: file coordinates = mesh coordinates + offset (the assembler recentres meshes)."""
    off = mathutils.Vector(offset)
    pick = mathutils.Vector(pick)
    bm = bmesh.new()
    bm.from_mesh(me)

    def key(co):
        return (round(co.x * 1000), round(co.y * 1000), round(co.z * 1000))

    parent = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for v in bm.verts:
        k = key(v.co)
        parent.setdefault(k, k)
    for f in bm.faces:
        ks = [find(key(v.co)) for v in f.verts]
        for k in ks[1:]:
            ra, rb = find(ks[0]), find(k)
            if ra != rb:
                parent[rb] = ra
    groups = {}
    for f in bm.faces:
        groups.setdefault(find(key(f.verts[0].co)), []).append(f)

    def centre(fs):
        cos = [v.co for f in fs for v in f.verts]
        return mathutils.Vector([(min(c[i] for c in cos) + max(c[i] for c in cos)) / 2 for i in range(3)]) + off

    best = min(groups.values(), key=lambda fs: (centre(fs) - pick).length)
    keep = set(best)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f not in keep], context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.to_mesh(me)
    bm.free()
    me.update()
    return len(groups)
