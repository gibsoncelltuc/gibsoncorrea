"""Personagem 2D cut-out em cena 3D (Blender): cabeça branca sombreada + contorno grosso, olhos de pálpebra pesada, sobrancelhas, bocas, suor,
corpo feijão com tecido, membros macarrão, mãos, chapéus/acessórios. Pose = função pura do tempo (ver anim.py). Espelha 'src/characters/Rig.tsx'.
Frame do personagem: X direita (tela), Z cima, Y para dentro (câmera em -Y). Unidade do rig U = 0.5 m."""
import bpy, math, numpy as np
from mathutils import Vector
from . import util, mats, texlib
U = 0.5
INK = (0.012, 0.010, 0.020, 1.0)
_mesh = {}; _mat = {}
def _m(key, build):
    if key not in _mesh: _mesh[key] = build()
    return _mesh[key]
def m_disc(n=40):
    def b():
        a = np.linspace(0, 2 * np.pi, n, endpoint=False); V = [(0, 0, 0)] + [(math.cos(t), 0, math.sin(t)) for t in a]; F = [(0, 1 + i, 1 + (i + 1) % n) for i in range(n)]
        me = bpy.data.meshes.new(f'disc{n}'); me.from_pydata(V, [], F); me.update(); return me
    return _m(('disc', n), b)
def m_box():
    def b():
        V = [(-.5, 0, -.5), (.5, 0, -.5), (.5, 0, .5), (-.5, 0, .5)]; me = bpy.data.meshes.new('bar'); me.from_pydata(V, [], [(0, 1, 2, 3)]); me.update(); return me
    return _m(('box',), b)
def m_tri():
    def b():
        V = [(-.5, 0, -.5), (.5, 0, -.5), (0, 0, .5)]; me = bpy.data.meshes.new('tri'); me.from_pydata(V, [], [(0, 1, 2)]); me.update(); return me
    return _m(('tri',), b)
def m_half(n=24):
    def b():
        a = np.linspace(0, np.pi, n + 1); V = [(0, 0, 0)] + [(math.cos(t), 0, math.sin(t)) for t in a]; F = [(0, 1 + i, 2 + i) for i in range(n)]
        me = bpy.data.meshes.new('half'); me.from_pydata(V, [], F); me.update(); return me
    return _m(('half', n), b)
def m_arc(t=0.12, arc=math.pi, n=24):
    def b():
        a = np.linspace(0, arc, n + 1); V = []; F = []
        for x in a: V += [((1 - t / 2) * math.cos(x), 0, (1 - t / 2) * math.sin(x)), ((1 + t / 2) * math.cos(x), 0, (1 + t / 2) * math.sin(x))]
        for i in range(n): k = i * 2; F.append((k, k + 1, k + 3, k + 2))
        me = bpy.data.meshes.new('arc'); me.from_pydata(V, [], F); me.update(); return me
    return _m(('arc', round(t, 3), round(arc, 3), n), b)
def m_stadium(w, h, n=14):
    def b():
        r = w / 2; hh = max(0, (h - w) / 2); a = np.linspace(0, np.pi, n); pts = [(r * math.cos(t), 0, hh + r * math.sin(t)) for t in a] + [(-r * math.cos(t), 0, -hh - r * math.sin(t)) for t in a]
        V = [(0, 0, 0)] + pts; F = [(0, 1 + i, 1 + (i + 1) % len(pts)) for i in range(len(pts))]; me = bpy.data.meshes.new('stad'); me.from_pydata(V, [], F); me.update()
        uv = me.uv_layers.new(name='UVMap')
        for li, loop in enumerate(me.loops): v = me.vertices[loop.vertex_index].co; uv.data[li].uv = (v.x / w + .5, v.z / h + .5)
        return me
    return _m(('stad', round(w, 3), round(h, 3)), b)
def m_capsule(r, L, seg=10, rings=3):
    def b():
        V = []; F = []; ring = lambda z, rr: [(rr * math.cos(t), rr * math.sin(t), z) for t in np.linspace(0, 2 * np.pi, seg, endpoint=False)]
        # topo (hemisfério) → cilindro → base (hemisfério); eixo -Z (pendurado)
        levels = []
        for k in range(rings): a = (math.pi / 2) * k / rings; levels.append((r * math.sin(a), r * math.cos(a)))   # (z, raio) subindo? usa de cima p/ baixo
        zs = [(+r * math.cos(math.pi / 2 * k / rings) * -1 + r * 0, 0)]
        rings_pts = []
        for k in range(rings + 1): a = math.pi / 2 * (1 - k / rings); rings_pts.append((r * math.sin(a), r * math.cos(a)))      # topo: z de r → 0
        for (z, rr) in rings_pts: V += ring(z, max(rr, 1e-4))
        for (z, rr) in reversed(rings_pts): V += ring(-L - z, max(rr, 1e-4))
        nl = (rings + 1) * 2
        for i in range(nl - 1):
            for j in range(seg): a, b2 = i * seg + j, i * seg + (j + 1) % seg; F.append((a, b2, b2 + seg, a + seg))
        me = bpy.data.meshes.new('capsule'); me.from_pydata(V, [], F); me.update()
        for p in me.polygons: p.use_smooth = True
        return me
    return _m(('cap', round(r, 4), round(L, 4)), b)
def m_lens(n=14, p=.55):
    """traço de pincel afilado (sobrancelha/boca): grosso no meio e pontudo nas pontas, largura 1 × altura 1 (escalar no objeto)"""
    def b():
        xs = np.linspace(-.5, .5, n); top = [(float(x), 0, float(.5 * max(1e-4, 1 - (2 * x) ** 2) ** p)) for x in xs]; bot = [(float(x), 0, float(-.5 * max(1e-4, 1 - (2 * x) ** 2) ** p)) for x in xs[::-1]]
        V = top + bot[1:-1]; me = bpy.data.meshes.new('lens'); me.from_pydata(V, [], [tuple(range(len(V)))]); me.update(); return me
    return _m(('lens', n, round(p, 3)), b)
# ---------------- contorno de tinta irregular (look "feito à mão" do canal) ----------------
# Medido nos quadros nativos das gravações: a espessura varia ao longo da linha — fina do lado da luz (alto-esquerda), 2–3× mais grossa no lado oposto (baixo-direita),
# com lobos suaves e trechos ("pedaços") de espessura diferente. g(φ) tem média ≈ 1; a espessura real é t_médio * g(φ_normal).
import zlib
def seed_of(*parts): return zlib.crc32(':'.join(str(x) for x in parts).encode()) & 0x7fffffff
_G = {}
def ink_g(seed, bias=0.55, light_deg=135.0, pieces=5):
    key = (seed, round(bias, 3), round(light_deg, 1), pieces)
    if key in _G: return _G[key]
    r = np.random.default_rng(seed); N = 720; ph = np.linspace(0, 2 * np.pi, N, endpoint=False)
    base = 1 - bias * np.cos(ph - np.radians(light_deg))
    for k, a in ((2, .10), (3, .09), (5, .07)): base = base + r.uniform(.5, 1.0) * a * np.cos(k * ph + r.uniform(0, 2 * np.pi))
    nb = int(r.integers(max(3, pieces - 1), pieces + 2)); br = np.sort(r.uniform(0, 2 * np.pi, nb)); mu = r.uniform(.80, 1.30, nb)
    step = np.ones(N)
    for i in range(nb):
        a0, a1 = br[i], br[(i + 1) % nb] + (2 * np.pi if i == nb - 1 else 0)
        m = ((ph >= a0) & (ph < a1)) | ((ph + 2 * np.pi >= a0) & (ph + 2 * np.pi < a1)); step[m] = mu[i]
    k = np.exp(-0.5 * ((np.minimum(ph, 2 * np.pi - ph)) / 0.10) ** 2); k /= k.sum()                  # suaviza os degraus (σ≈6°) por convolução circular
    step = np.real(np.fft.ifft(np.fft.fft(step) * np.fft.fft(k)))
    g = np.clip(base * step, .28, 2.6); g = g / g.mean()
    def f(phi): return np.interp(np.mod(phi, 2 * np.pi), np.append(ph, 2 * np.pi), np.append(g, g[0]))
    _G[key] = f; return f
_ink = {}
FACE_DZ = .085   # feições sobem .085 U (medido: olhos a +0,12 D e boca a −0,06 D do centro da cabeça nos quadros nativos)
INK_K = 1.2   # fator global de espessura (calibrado nos quadros nativos: lado grosso ≈ 6 % do diâmetro da cabeça, lado fino ≈ 2 %)
def ink_poly(pts, t, seed, bias=0.6, light=135.0, pieces=5, name='inkp'):
    """malha 'gêmea de tinta' de um polígono convexo (N,2) no plano XZ: pontos deslocados pela normal * t * g(φ). Sombreamento em leque a partir da origem."""
    key = (name, round(float(t), 4), seed, round(bias, 3), round(light, 1), pieces, len(pts), round(float(np.abs(pts).max()), 4))
    if key in _ink: return _ink[key]
    P = np.asarray(pts, float); d = np.roll(P, -1, 0) - np.roll(P, 1, 0); nr = np.stack([d[:, 1], -d[:, 0]], 1); nr /= np.linalg.norm(nr, axis=1, keepdims=True) + 1e-9
    phi = np.arctan2(nr[:, 1], nr[:, 0]); out = P + nr * (t * INK_K * ink_g(seed, bias, light, pieces)(phi))[:, None]
    V = [(0, 0, 0)] + [(float(x), 0, float(z)) for x, z in out]; n = len(out); F = [(0, 1 + i, 1 + (i + 1) % n) for i in range(n)]
    me = bpy.data.meshes.new(name); me.from_pydata(V, [], F); me.update(); _ink[key] = me; return me
def ell_pts(a, b, n=48): th = np.linspace(0, 2 * np.pi, n, endpoint=False); return np.stack([a * np.cos(th), b * np.sin(th)], 1)
def stad_pts(w, h, n=14):
    r = w / 2; hh = max(0, (h - w) / 2); a = np.linspace(0, np.pi, n)
    return np.array([(r * math.cos(t), hh + r * math.sin(t)) for t in a] + [(-r * math.cos(t), -hh - r * math.sin(t)) for t in a])
def m_capsule_var(r, L, seed, vary=.22, seg=10, rings=3, nmid=6, name='capv'):
    """cápsula (pendurada em -Z) cujo raio ondula suavemente ao longo do comprimento — traço de macarrão com pressão variável"""
    key = ('capv', round(r, 4), round(L, 4), seed, round(vary, 3))
    def b():
        rr = np.random.default_rng(seed); ph = rr.uniform(0, 2 * np.pi, 2); f = lambda s: 1 + vary * (.6 * math.sin(2 * math.pi * 1.0 * s + ph[0]) + .4 * math.sin(2 * math.pi * 2.3 * s + ph[1]))
        V = []; F = []; ring = lambda z, rad: [(rad * math.cos(t), rad * math.sin(t), z) for t in np.linspace(0, 2 * np.pi, seg, endpoint=False)]
        top = [(r * math.sin(math.pi / 2 * (1 - k / rings)), r * math.cos(math.pi / 2 * (1 - k / rings)) * f(0)) for k in range(rings + 1)]; bot = [(-L - z, rad * f(1) / f(0)) for (z, rad) in reversed(top)]
        lv = [(z, max(rad, 1e-4)) for z, rad in top]; lv += [(-L * (i + 1) / (nmid + 1), r * f((i + 1) / (nmid + 1))) for i in range(nmid)]
        lv += [(-L - (r * math.sin(math.pi / 2 * (1 - k / rings))), max(r * math.cos(math.pi / 2 * (1 - k / rings)) * f(1), 1e-4)) for k in range(rings, -1, -1)]
        for z, rad in lv: V += ring(z, rad)
        for i in range(len(lv) - 1):
            for j in range(seg): a, b2 = i * seg + j, i * seg + (j + 1) % seg; F.append((a, b2, b2 + seg, a + seg))
        me = bpy.data.meshes.new(name); me.from_pydata(V, [], F); me.update()
        for pgn in me.polygons: pgn.use_smooth = True
        return me
    return _m(key, b)
def mat(name, color, kind='cutout', **kw):
    key = (name, tuple(color), kind, tuple(sorted(kw.items())))
    if key not in _mat: _mat[key] = (mats.cutout(name, color, **kw) if kind == 'cutout' else mats.ink(name) if kind == 'ink' else mats.cutout_img(name, color, **kw))
    return _mat[key]
def hexc(h): return util.hex_rgb(h)

class Char:
    """Personagem: constrói a hierarquia uma vez; apply_pose(...) atualiza juntas/expressões por frame."""
    def __init__(self, name, look, col=None):
        self.name = name; self.look = look; self.b = look.get('build', 1.0); self.col = col; self.objs = []; self.var = {}
        self.light = look.get('inkLight', 135.0 + (seed_of(name, 'light') % 51) - 25)   # direção (° no plano XZ) do lado em que o contorno é mais fino
        self.root = util.empty(name, col=col)
        self.body = util.empty(name + '_body', parent=self.root, col=col)
        b = self.b
        white = hexc('#fbf8ff'); shade = hexc('#d4d0ee'); ink = 'ink'; M_INK = mat('ink', INK, 'ink'); M_W = mat('head_w', white, emit=.62); M_SH = mat('head_s', shade, emit=.45)
        self.M_INK, self.M_W = M_INK, M_W
        sl = hexc(look.get('sleeve', '#2f2a46')); self.sleeve = sl
        # pernas
        self.leg = {}
        for side, sx, dy in (('L', -.2 * b, .06), ('R', .2 * b, -.01)):
            hip = util.empty(f'{name}_hip{side}', (sx * U, dy * U, 1.38 * U), self.body, col)
            self.limb(hip, .56, .045, hexc(look.get('pants', '#2f2a46')), dy)
            knee = util.empty(f'{name}_knee{side}', (0, 0, -.58 * U), hip, col); self.limb(knee, .55, .045, hexc(look.get('pants', '#2f2a46')), dy)
            foot = util.empty(f'{name}_foot{side}', (0, 0, -.62 * U), knee, col); self.ink(foot, .16 * U, .08 * U, .0375 * U, (.1 * U, dy * U + .002, .02 * U), 20, key='foot' + side); self.flat(foot, m_disc(20), (.16 * U, 1, .08 * U), (.1 * U, dy * U - .002, .02 * U), mat('shoe', hexc(look.get('shoe', '#2a2030')), emit=.2))
            self.leg[side] = (hip, knee)
        # tronco
        self.torso = util.empty(name + '_torso', (0, 0, 1.38 * U), self.body, col)
        tw, th = .9 * b * U, 1.4 * U; torso_fill = m_stadium(tw, th)
        self.ink(self.torso, 0, 0, .05 * U, (0, .004, .55 * U), key='torso', poly=stad_pts(tw, th))
        pat = look.get('pattern', 'plain'); shirt = hexc(look['shirt'])
        if pat != 'plain': tex = texlib.fabric(pat, look['shirt'], look.get('shirt2', '#ffffff')); M_T = mats.cutout_img(f'fab_{name}', tex, emit=.28)
        else: M_T = mat('shirt_' + look['shirt'], shirt, emit=.28)
        self.flat(self.torso, torso_fill, (1, 1, 1), (0, 0, .55 * U), M_T)
        self.outfit(look, tw, th)
        # braços
        self.arm = {}
        for side, sx, dy in (('L', -.45 * b, .05), ('R', .45 * b, -.07)):
            sh = util.empty(f'{name}_sh{side}', (sx * U, dy * U, .95 * U), self.torso, col)
            self.limb(sh, .5, .04, sl, dy); el = util.empty(f'{name}_el{side}', (0, 0, -.52 * U), sh, col); self.limb(el, .46, .04, sl, dy)
            hand = util.empty(f'{name}_hand{side}', (0, 0, -.5 * U), el, col); self.ink(hand, .088 * U, .088 * U, .037 * U, (0, -.0, -.07 * U), 20, key='hand' + side); self.flat(hand, m_disc(20), (.088 * U, 1, .088 * U), (0, -.004, -.07 * U), M_W)
            self.arm[side] = (sh, el, hand)
        # cabeça
        self.head = util.empty(name + '_head', (0, -.10 * U, 1.79 * U), self.torso, col)
        hs = look.get('headScale', 1.0); R = .56 * U * hs
        self.ink(self.head, R, R, .047 * U, (0, .004, 0), 56, key='head'); self.flat(self.head, m_disc(56), (R, 1, R), (0, 0, 0), M_SH); self.flat(self.head, m_disc(56), (R - .052 * U, 1, R - .052 * U), (.04 * U, -.003, .045 * U), M_W)
        n0 = len(self.objs); self.face(look, R)
        for o in self.objs[n0:]:
            if o.parent == self.head: o.location.z += FACE_DZ * U
        self.hat(look)
    # ---------- construção ----------
    def add(self, parent, me, scale, loc, material, rot=(0, 0, 0), name='p'):
        o = bpy.data.objects.new(f'{self.name}_{name}', me); o.parent = parent; o.location = loc; o.scale = scale; o.rotation_euler = rot
        if material is not None:
            if len(o.data.materials) == 0: o.data.materials.append(None)          # meshes compartilhados: o material fica no OBJETO, não na malha
            o.material_slots[0].link = 'OBJECT'; o.material_slots[0].material = material
        util.link(o, self.col); self.objs.append(o); return o
    def flat(self, parent, me, scale, loc, material, rot=(0, 0, 0)): return self.add(parent, me, scale, loc, material, rot)
    def ink(self, parent, a, b, t, loc, n=40, key='x', rot=(0, 0, 0), poly=None):
        """gêmea de tinta irregular de um preenchimento elíptico (semi-eixos a,b) ou polígono `poly`; t = espessura média"""
        pts = ell_pts(a, b, n) if poly is None else poly
        return self.add(parent, ink_poly(pts, t, seed_of(self.name, key), light=self.light), (1, 1, 1), loc, self.M_INK, rot=rot, name='ink')
    def limb(self, parent, L, r, color, dy):
        """membro "macarrão" do canal: traço de tinta (preto arroxeado) de espessura ≈ 7 % do diâmetro da cabeça, com leve ondulação de pressão; sem preenchimento colorido"""
        self.add(parent, m_capsule_var(.042 * U, L * U, seed_of(self.name, 'limb', len(self.objs)), vary=.12), (1, 1, 1), (0, dy * U, 0), self.M_INK, name='limb')
    def outfit(self, look, tw, th):
        o = look.get('outfit', 'plain'); b = self.b; T = self.torso; gold = mat('gold', hexc('#f0c250'), emit=.4)
        if o == 'overalls':
            bl = mat('denim', hexc('#3a62a8'), emit=.22); self.flat(T, m_box(), (.62 * b * U, 1, .62 * U), (0, -.006, .42 * U), bl)
            for s in (-1, 1): self.flat(T, m_box(), (.07 * U, 1, .5 * U), (s * .2 * b * U, -.007, .98 * U), bl); self.flat(T, m_disc(12), (.05 * U, 1, .05 * U), (s * .2 * b * U, -.009, .74 * U), gold)
            self.flat(T, m_box(), (.22 * U, 1, .2 * U), (.12 * U, -.009, .36 * U), mat('patch', hexc('#d8b06a'), emit=.25))
        elif o == 'waistcoat':
            self.flat(T, m_tri(), (.86 * b * U, 1, .96 * U), (0, -.006, .55 * U), mat('vest', hexc(look.get('trim', '#8a6a3a')), emit=.25), rot=(0, math.pi, 0))
            for z in (.05, .27): self.flat(T, m_disc(10), (.045 * U, 1, .045 * U), (0, -.01, z * U), gold)
            self.flat(T, m_box(), (.1 * U, 1, .34 * U), (0, -.01, .8 * U), mat('tie', hexc('#b9363a'), emit=.25))
        elif o in ('uniform', 'admiral'):
            self.flat(T, m_box(), (.1 * U, 1, 1.2 * U), (0, -.006, .55 * U), mat('trim_' + look.get('trim', '#f0c250'), hexc(look.get('trim', '#f0c250')), emit=.3))
            for z in (.95, .72, .49, .26, .03): self.flat(T, m_disc(12), (.052 * U, 1, .052 * U), (0, -.01, z * U), gold)
            if o == 'uniform': self.flat(T, m_box(), (.15 * U, 1, 1.15 * U), (0, -.011, .55 * U), mat('belt', hexc('#f6f1e6'), emit=.3), rot=(0, 0, .7))
            else:
                for s in (-1, 1): self.flat(T, m_disc(16), (.17 * U, 1, .09 * U), (s * .38 * b * U, -.01, 1.13 * U), M_INK_ := self.M_INK, rot=(0, 0, s * -.2)); self.flat(T, m_disc(16), (.145 * U, 1, .07 * U), (s * .38 * b * U, -.012, 1.13 * U), gold, rot=(0, 0, s * -.2))
                self.flat(T, m_disc(14), (.075 * U, 1, .075 * U), (.22 * b * U, -.012, .82 * U), mat('medal', hexc('#c8372f'), emit=.3)); self.flat(T, m_box(), (.78 * b * U, 1, .07 * U), (0, -.011, .2 * U), mat('sash', hexc('#c8372f'), emit=.3))
    def face(self, look, R):
        H = self.head; M_INK = self.M_INK; U_ = U; sc = lambda v: v * U_
        eye = {}
        for side in (-1, 1):
            g = util.empty(f'{self.name}_eye{side}', (side * sc(.145), -.012, sc(.03)), H, self.col); self.objs.append(g)
            pup = self.add(g, m_disc(14), (sc(.057), 1, sc(.064)), (0, -.002, 0), M_INK, name='pupil'); lid = self.add(g, m_box(), (sc(.22), 1, sc(.042)), (0, -.004, sc(.05)), M_INK, name='lid')
            lash = self.add(g, m_arc(.14, math.pi * .7), (sc(.085), 1, sc(.085)), (0, -.001, sc(-.015)), M_INK, rot=(0, 0, 0), name='lash'); lash.rotation_euler[1] = 0
            wo = self.add(g, m_disc(22), (sc(.125), 1, sc(.125)), (0, -.002, 0), M_INK, name='wide_o'); wi = self.add(g, m_disc(22), (sc(.1), 1, sc(.1)), (0, -.003, 0), self.M_W, name='wide_i'); wp = self.add(g, m_disc(12), (sc(.03), 1, sc(.03)), (0, -.004, 0), M_INK, name='wide_p')
            ar = self.add(g, m_arc(.3, math.pi), (sc(.085), 1, sc(.085)), (0, -.003, sc(-.03)), M_INK, name='arc')
            x1 = self.add(g, m_box(), (sc(.17), 1, sc(.035)), (0, -.003, 0), M_INK, rot=(0, .8, 0), name='x1'); x2 = self.add(g, m_box(), (sc(.17), 1, sc(.035)), (0, -.003, 0), M_INK, rot=(0, -.8, 0), name='x2')
            brow = self.add(H, m_lens(14, .5), (sc(.23), 1, sc(.055)), (side * sc(.15), -.013, sc(.21)), M_INK, name='brow')
            eye[side] = dict(g=g, pup=pup, lid=lid, lash=lash, wide=(wo, wi, wp), arc=ar, x=(x1, x2), brow=brow)
        self.eye = eye
        # bocas
        m = {}
        m['line'] = [self.add(H, m_lens(14, .6), (sc(.24), 1, sc(.045)), (0, -.012, sc(-.21)), M_INK)]
        m['smirk'] = [self.add(H, m_arc(.18, math.pi * .75), (sc(.13), 1, sc(.13)), (sc(.05), -.012, sc(-.15)), M_INK, rot=(0, math.pi + .3, 0))]
        m['smile'] = [self.add(H, m_arc(.16, math.pi), (sc(.15), 1, sc(.15)), (0, -.012, sc(-.14)), M_INK, rot=(0, math.pi, 0))]
        m['frown'] = [self.add(H, m_arc(.18, math.pi), (sc(.13), 1, sc(.13)), (0, -.012, sc(-.3)), M_INK)]
        def teeth(w, h, cols, z):
            out = [self.add(H, m_box(), (sc(w + .05), 1, sc(h + .05)), (0, -.012, sc(z)), M_INK), self.add(H, m_box(), (sc(w), 1, sc(h)), (0, -.014, sc(z)), self.M_W)]
            for i in range(cols - 1): out.append(self.add(H, m_box(), (sc(.012), 1, sc(h)), (-sc(w) / 2 + (i + 1) * sc(w) / cols, -.016, sc(z)), M_INK))
            out.append(self.add(H, m_box(), (sc(w), 1, sc(.012)), (0, -.016, sc(z)), M_INK)); return out
        m['teeth'] = teeth(.3, .1, 5, -.22); m['grin'] = [self.add(H, m_arc(.18, math.pi), (sc(.2), 1, sc(.2)), (0, -.012, sc(-.12)), M_INK, rot=(0, math.pi, 0))] + teeth(.26, .07, 4, -.21)
        m['laugh'] = [self.add(H, m_half(), (sc(.26), 1, sc(.2)), (0, -.012, sc(-.14)), M_INK, rot=(0, math.pi, 0)), self.add(H, m_box(), (sc(.38), 1, sc(.07)), (0, -.014, sc(-.16)), self.M_W), self.add(H, m_disc(14), (sc(.12), 1, sc(.06)), (0, -.014, sc(-.3)), mat('tongue', hexc('#e0646a'), emit=.3))]
        m['oh'] = [self.add(H, m_disc(18), (sc(.07), 1, sc(.08)), (0, -.012, sc(-.22)), M_INK)]; m['shout'] = [self.add(H, m_disc(22), (sc(.13), 1, sc(.16)), (0, -.012, sc(-.24)), M_INK)]
        self.mouth = m
        # detalhes do rosto
        if look.get('blush'):
            for s in (-1, 1): self.add(H, m_disc(16), (sc(.075), 1, sc(.055)), (s * sc(.36), -.012, sc(-.1)), mat('blush', hexc('#f3a2ae'), emit=.35))
        if look.get('sideburns'):
            for s in (-1, 1): self.add(H, m_disc(16), (sc(.06), 1, sc(.16)), (s * sc(.49), -.010, sc(-.04)), mat('sb_' + look['sideburns'], hexc(look['sideburns']), emit=.3), rot=(0, s * -.15, 0))
        if look.get('beard'): self.add(H, m_half(), (sc(.36), 1, sc(.28)), (0, -.008, sc(-.16)), mat('beard_' + look['beard'], hexc(look['beard']), emit=.45), rot=(0, math.pi, 0))
        if look.get('mustache'):
            for s in (-1, 1): self.add(H, m_disc(16), (sc(.12), 1, sc(.05)), (s * sc(.1), -.016, sc(-.085)), mat('mu_' + look['mustache'], hexc(look['mustache']), emit=.3), rot=(0, s * -.3, 0))
        if look.get('glasses'):
            for s in (-1, 1): self.add(H, m_arc(.12, math.pi * 2), (sc(.115), 1, sc(.115)), (s * sc(.2), -.018, sc(.04)), M_INK)
        # suor
        self.sweat = []
        for s, (x, z) in enumerate([(.46, .2), (-.5, .12)]):
            g = util.empty(f'{self.name}_sweat{s}', (sc(x), -.02, sc(z)), H, self.col); self.add(g, m_disc(16), (sc(.06), 1, sc(.06)), (0, 0, -sc(.03)), mat('drop', hexc('#a9dcff'), emit=.5)); self.add(g, m_tri(), (sc(.1), 1, sc(.12)), (0, .001, sc(.04)), mat('drop', hexc('#a9dcff'), emit=.5)); self.sweat.append(g)
    def hat(self, look):
        H = self.head; h = look.get('hat'); sc = lambda v: v * U; M_INK = self.M_INK
        if not h: return
        col = look.get('hatColor', '#e8c068'); M = mat('hat_' + col, hexc(col), emit=.28)
        if h == 'straw':
            g = util.empty(f'{self.name}_hat', (0, -.02, sc(.47)), H, self.col); self.ink(g, sc(.81), sc(.165), sc(.0425), (0, .004, 0), 40, key='brim'); self.add(g, m_disc(40), (sc(.81), 1, sc(.165)), (0, 0, 0), M)
            self.ink(g, sc(.4), sc(.3), sc(.04), (0, .003, sc(.2)), 28, key='crown'); self.add(g, m_disc(28), (sc(.4), 1, sc(.3)), (0, 0, sc(.2)), M); self.add(g, m_box(), (sc(.74), 1, sc(.08)), (0, -.004, sc(.06)), mat('band', hexc(look.get('hatBand', '#3a6aa8')), emit=.3))
        elif h == 'kepi':
            g = util.empty(f'{self.name}_hat', (0, -.02, sc(.46)), H, self.col); g.rotation_euler[1] = -.06; self.ink(g, sc(.46), sc(.235), sc(.0375), (sc(.02), .004, sc(.08)), 30, key='kcap'); self.add(g, m_disc(30), (sc(.46), 1, sc(.235)), (sc(.02), 0, sc(.08)), M)
            self.ink(g, sc(.3), sc(.05), sc(.0325), (sc(.36), .004, -sc(.07)), 20, key='kvisor'); self.add(g, m_disc(20), (sc(.3), 1, sc(.05)), (sc(.36), 0, -sc(.07)), mat('visor', hexc('#1f2f55'), emit=.25)); self.add(g, m_disc(14), (sc(.07), 1, sc(.07)), (0, -.004, sc(.08)), mat('gold', hexc('#f0c250'), emit=.4))
        elif h == 'flatcap':
            g = util.empty(f'{self.name}_hat', (0, -.02, sc(.42)), H, self.col); tex = texlib.fabric('tweed', col, '#b9a27a'); Mt = mats.cutout_img('tweed_' + self.name, tex, emit=.28)
            self.ink(g, sc(.575), sc(.262), sc(.0415), (0, .004, sc(.07)), 30, key='fcap'); self.add(g, m_disc(30), (sc(.575), 1, sc(.262)), (0, 0, sc(.07)), Mt); self.ink(g, sc(.26), sc(.045), sc(.0325), (sc(.42), .004, -sc(.06)), 20, key='fvisor'); self.add(g, m_disc(20), (sc(.26), 1, sc(.045)), (sc(.42), 0, -sc(.06)), M)
        elif h == 'bicorn':
            g = util.empty(f'{self.name}_hat', (0, -.02, sc(.5)), H, self.col); blk = mat('bicorn', hexc('#1c1a2c'), emit=.2); gold = mat('gold', hexc('#f0c250'), emit=.4)
            self.ink(g, sc(.73), sc(.22), sc(.045), (0, .004, sc(.05)), 40, key='bicap'); self.add(g, m_disc(40), (sc(.73), 1, sc(.22)), (0, 0, sc(.05)), blk)
            for s in (-1, 1): self.add(g, m_disc(14), (sc(.15), 1, sc(.18)), (s * sc(.62), .004, sc(.1)), M_INK)
            self.add(g, m_box(), (sc(.95), 1, sc(.04)), (0, -.004, 0), gold); self.add(g, m_disc(14), (sc(.07), 1, sc(.07)), (0, -.006, sc(.1)), mat('cockade', hexc('#c8372f'), emit=.3))
        elif h == 'peaked':
            g = util.empty(f'{self.name}_hat', (0, -.02, sc(.44)), H, self.col); self.ink(g, sc(.52), sc(.245), sc(.0375), (0, .004, sc(.08)), 30, key='pcap'); self.add(g, m_disc(30), (sc(.52), 1, sc(.245)), (0, 0, sc(.08)), M)
            self.add(g, m_box(), (sc(.78), 1, sc(.09)), (0, -.004, -sc(.02)), mat('band_w', hexc('#f6f1e6'), emit=.3)); self.add(g, m_disc(20), (sc(.3), 1, sc(.07)), (sc(.38), .004, -sc(.08)), mat('visor2', hexc('#1a1a2a'), emit=.2)); self.add(g, m_disc(14), (sc(.07), 1, sc(.07)), (0, -.006, sc(.04)), mat('gold', hexc('#f0c250'), emit=.4))
    # ---------- pose por frame ----------
    def pose(self, P):
        """P: dict com x,y,z (metros, mundo), face(±1), scale, bob, lean, tilt, armL/armR[2], legL/legR[2], look[2], blink, lid, eye, brows[2], angry, mouth, open, sweat, squash"""
        r = self.root; r.location = (P.get('x', 0), P.get('y', 0), P.get('z', 0)); sc = P.get('scale', 1.0); r.scale = (P.get('face', 1) * sc, 1, sc * (1 - P.get('squash', 0) * .5)); r.rotation_euler = (0, 0, P.get('rotz', 0))
        self.body.location = (0, 0, P.get('bob', 0) * U); self.torso.rotation_euler = (0, -P.get('lean', 0), 0); self.head.rotation_euler = (0, -P.get('tilt', 0), 0)
        for side, key in (('L', 'legL'), ('R', 'legR')): a = P.get(key, (0, 0)); hip, knee = self.leg[side]; hip.rotation_euler = (0, -a[0], 0); knee.rotation_euler = (0, -a[1], 0)
        for side, key in (('L', 'armL'), ('R', 'armR')): a = P.get(key, (0.1, 0.1)); sh, el, hd = self.arm[side]; sh.rotation_euler = (0, -a[0], 0); el.rotation_euler = (0, -a[1], 0)
        lid = min(1.0, P.get('lid', .42) + P.get('blink', 0) * .9); eyev = P.get('eye', 'lid'); lx, ly = P.get('look', (0, 0)); ang = P.get('angry', 0); brows = P.get('brows', (0, 0))
        for side in (-1, 1):
            e = self.eye[side]; vis = lambda o, v: setattr(o, 'hide_render', not v) or setattr(o, 'hide_viewport', not v)
            vis(e['pup'], eyev == 'lid' and lid < .92); vis(e['lid'], eyev == 'lid'); vis(e['lash'], False); [vis(o, eyev == 'wide') for o in e['wide']]; vis(e['arc'], eyev == 'arc'); [vis(o, eyev == 'x') for o in e['x']]
            e['pup'].location = (lx * .03 * U, -.002, (-.012 + ly * .02) * U); e['lid'].location = (0, -.004, (.085 - lid * .07) * U); e['lid'].rotation_euler = (0, side * ang * .2, 0)
            e['wide'][2].location = (lx * .03 * U, -.004, ly * .03 * U); b = brows[0 if side == -1 else 1]; e['brow'].location = (side * .15 * U, -.013, (.21 + FACE_DZ + b * .07) * U); e['brow'].rotation_euler = (0, -(side * ang * .5), 0)
        mo = P.get('mouth', 'line'); 
        for k, objs in self.mouth.items():
            for o in objs: o.hide_render = (k != mo); o.hide_viewport = (k != mo)
        sw = P.get('sweat', 0)
        for i, g in enumerate(self.sweat):
            on = sw > 0; g.hide_viewport = g.hide_render = not on
            for c in g.children: c.hide_render = c.hide_viewport = not on
            f = (((sw + .5 * i) % 1) + 1) % 1; g.location.z = ((.2 if i == 0 else .12) + FACE_DZ) * U - f * .35 * U; g.scale = (1 - f * .4,) * 3
    def attach(self, side, obj, loc=(0, 0, -.07), rot=(0, 0, 0), scale=1.0):
        """prende um objeto à mão (L/R)"""
        hd = self.arm[side][2]; obj.parent = hd; obj.location = (loc[0] * U, loc[1], loc[2] * U); obj.rotation_euler = rot; obj.scale = (scale,) * 3
