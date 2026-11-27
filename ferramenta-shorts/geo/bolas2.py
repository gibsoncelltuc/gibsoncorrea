# MAP MATES v2 (autoral): bolinhas-pais GRANDES com caras exageradas, acao o tempo todo
# (tiro com coice, clarao, rastro, impacto POW, empurrao, explosao, pulo, tremor de raiva, entrada com quique),
# mapa 3D do Blender ao fundo, musica (Kevin MacLeod, CC BY) + efeitos CC0. uso: python3 bolas2.py <roteiro.json> [tempos de teste]
import json, math, os, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30; SS = 2
R = json.load(open(sys.argv[1])); RID = R['id']; OUT = f'out/{RID}'; os.makedirs(f'{OUT}/frames', exist_ok=True)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
EMOF = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ts' if False else '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
_EC = {}
def emoji(ch, tam):
    k = (ch, int(tam))
    if k not in _EC:
        im = Image.new('RGBA', (170, 170)); ImageDraw.Draw(im).text((85, 85), ch.replace('️', ''), font=EMOF, embedded_color=True, anchor='mm'); im = im.crop(im.getbbox())
        _EC[k] = im.resize((int(tam), max(1, int(tam * im.height / im.width))), Image.LANCZOS)
    return _EC[k]
_FC = {}
def fnt(n):
    if n not in _FC: _FC[n] = ImageFont.truetype(FB, n)
    return _FC[n]
clamp = lambda x, a=0., b=1.: max(a, min(b, x))
ease = lambda x: x * x * (3 - 2 * x)
def back(x):   # saida com quique (overshoot)
    x = clamp(x); c = 2.2; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------------- fundo: mapa 3D (Blender) ----------------
L0, L1, A0, A1 = R['mapa']; K = math.cos(math.radians((A0 + A1) / 2))
MAPA = Image.open(R['mapa_png']).convert('RGB'); MW, MH = MAPA.size
def xy(lon, lat): return ((lon - L0) / (L1 - L0) * MW, (A1 - lat) / (A1 - A0) * MH)
def fundo_ilha():
    im = Image.new('RGBA', (W, H), (96, 196, 236, 255)); d = ImageDraw.Draw(im); rng = np.random.default_rng(1)
    for k in range(60): x, y = rng.uniform(0, W), rng.uniform(0, H); d.arc([x - 50, y, x + 50, y + 26], 200, 340, fill=(150, 220, 248), width=6)
    pts = [(W / 2 + math.cos(a) * W * (.66 + .05 * math.sin(a * 5)), H * .56 + math.sin(a) * H * (.27 + .03 * math.cos(a * 3))) for a in np.linspace(0, 2 * math.pi, 120)]
    d.polygon([(x, y + 26) for x, y in pts], fill=(214, 190, 130)); d.polygon(pts, fill=(124, 200, 92)); d.line(pts + [pts[0]], fill=(60, 120, 40), width=10)
    for _ in range(110): x, y = rng.uniform(.04, .96) * W, rng.uniform(.33, .8) * H; c = (88, 160, 64); d.line([x, y, x - 7, y - 20], fill=c, width=5); d.line([x, y, x + 7, y - 20], fill=c, width=5)
    for x, y in ((.1, .36), (.9, .37), (.08, .76), (.92, .77), (.5, .32)): e = emoji('🌲', 170); im.alpha_composite(e, (int(x * W - 85), int(y * H - 140)))
    return im.filter(ImageFilter.GaussianBlur(1.2))
ILHA = fundo_ilha() if any(c.get('fundo') == 'ilha' for c in R['cenas']) else None

# ---------------- personagem ----------------
FLAG = {}
def bandeira(c):
    if c not in FLAG: FLAG[c] = Image.open(f'dados/flags/{c}.png').convert('RGBA')
    return FLAG[c]
_BC = {}
def sprite(flag, r, humor, chapeu, olha):
    k = (flag, r, humor, chapeu, olha)
    if k in _BC: return _BC[k]
    R2 = r * SS; T = int(R2 * 3.2); im = Image.new('RGBA', (T, T), (0, 0, 0, 0)); cx = cy = T / 2; d = ImageDraw.Draw(im)
    tam = int(R2 * 2); f = bandeira(flag); fw = int(tam * f.width / f.height); b = f.resize((fw, tam), Image.LANCZOS).crop(((fw - tam) // 2, 0, (fw - tam) // 2 + tam, tam))
    m = Image.new('L', (tam, tam), 0); ImageDraw.Draw(m).ellipse([0, 0, tam - 1, tam - 1], fill=255)
    # volume: escurece embaixo-direita, brilho em cima-esquerda
    yy, xx = np.mgrid[0:tam, 0:tam] / tam - .5; sh = np.clip((xx * .5 + yy * .9) * 1.3, 0, 1) * 95
    bb = np.array(b).astype(float); bb[..., :3] *= (1 - sh[..., None] / 255); b = Image.fromarray(bb.clip(0, 255).astype(np.uint8))
    im.paste(b, (int(cx - R2), int(cy - R2)), m)
    gl = Image.new('RGBA', (tam, tam)); ImageDraw.Draw(gl).ellipse([tam * .16, tam * .1, tam * .5, tam * .3], fill=(255, 255, 255, 110)); gl = gl.filter(ImageFilter.GaussianBlur(tam * .03))
    im.alpha_composite(gl, (int(cx - R2), int(cy - R2)))
    lw = int(R2 * .075); d.ellipse([cx - R2, cy - R2, cx + R2, cy + R2], outline=(0, 0, 0), width=lw)
    s = olha; ex, ey, er = R2 * .34, -R2 * .1, R2 * .27; B = (0, 0, 0); WH = (255, 255, 255); lw2 = int(R2 * .045)
    def olho(kx, aberto=1., pup=.42, py=0.):
        x0 = cx + kx * ex + s * R2 * .13; y0 = cy + ey
        d.ellipse([x0 - er, y0 - er * 1.2 * aberto, x0 + er, y0 + er * 1.2], fill=WH, outline=B, width=lw2)
        pr = er * pup; px = x0 + s * er * .38; pyy = y0 + er * .15 + py * er
        d.ellipse([px - pr, pyy - pr, px + pr, pyy + pr], fill=B); d.ellipse([px - pr * .35 + s * pr * .2, pyy - pr * .7, px + pr * .05 + s * pr * .2, pyy - pr * .3], fill=WH)
        return x0, y0
    def sobrancelha(kx, x0, y0, ang, grossa=.13):   # ang>0 = bravo (desce para o centro)
        L = er * 1.25; inner = -kx; yc = y0 - er * 1.35
        p1 = (x0 - inner * L, yc - ang * er * .5); p2 = (x0 + inner * L * .9, yc + ang * er * .6)
        d.line([p1, p2], fill=B, width=int(R2 * grossa))
    def boca(tipo):
        mx, my = cx + s * R2 * .14, cy + R2 * .45; w = R2 * .32
        if tipo == 'sorriso': d.chord([mx - w, my - w * .9, mx + w, my + w * .7], 0, 180, fill=B); d.ellipse([mx - w * .45, my + w * .1, mx + w * .45, my + w * .6], fill=(230, 90, 100))
        if tipo == 'grito': d.ellipse([mx - w * .55, my - w * .35, mx + w * .55, my + w * .75], fill=B); d.ellipse([mx - w * .3, my + w * .25, mx + w * .3, my + w * .65], fill=(230, 90, 100))
        if tipo == 'dentes': d.rounded_rectangle([mx - w * .8, my - w * .2, mx + w * .8, my + w * .35], int(w * .15), fill=WH, outline=B, width=lw2); d.line([mx - w * .8, my + w * .07, mx + w * .8, my + w * .07], fill=B, width=lw2 // 2)
        if tipo == 'triste': d.arc([mx - w * .6, my, mx + w * .6, my + w * .8], 200, 340, fill=B, width=lw2)
        if tipo == 'reto': d.line([mx - w * .4, my + w * .2, mx + w * .4, my + w * .1], fill=B, width=lw2)
        if tipo == 'zig': d.line([(mx - w * .6 + i * w * .2, my + (w * .12 if i % 2 else -w * .05)) for i in range(7)], fill=B, width=lw2)
        if tipo == 'sorrisinho': d.arc([mx - w * .6, my - w * .5, mx + w * .6, my + w * .3], 20, 150, fill=B, width=lw2)
    h = humor
    if h in ('feliz', 'riso'):
        for kx in (-1, 1): x0 = cx + kx * ex + s * R2 * .13; d.arc([x0 - er, cy + ey - er * .6, x0 + er, cy + ey + er * 1.1], 200, 340, fill=B, width=int(R2 * .07))
        boca('sorriso')
    elif h in ('dor', 'morto'):
        for kx in (-1, 1):
            x0 = cx + kx * ex + s * R2 * .13; y0 = cy + ey; q = er * .8
            if h == 'morto': d.line([x0 - q, y0 - q, x0 + q, y0 + q], fill=B, width=int(R2 * .07)); d.line([x0 - q, y0 + q, x0 + q, y0 - q], fill=B, width=int(R2 * .07))
            else: d.line([(x0 - kx * q, y0 - q), (x0 + kx * q, y0), (x0 - kx * q, y0 + q)], fill=B, width=int(R2 * .07))
        boca('zig' if h == 'dor' else 'reto')
    elif h == 'mira':
        x0, y0 = olho(1 * s, 1, .32); sobrancelha(1 * s, x0, y0, 1.2)
        x1 = cx - s * ex + s * R2 * .13; d.line([x1 - er, cy + ey, x1 + er, cy + ey], fill=B, width=int(R2 * .07)); boca('reto')
    else:
        aberto = .55 if h == 'convencido' else 1.; pup = {'choque': .2, 'bravo': .3, 'furioso': .26}.get(h, .42)
        for kx in (-1, 1):
            x0, y0 = olho(kx, aberto, pup)
            if h in ('bravo', 'furioso'): sobrancelha(kx, x0, y0, 1.4 if h == 'furioso' else 1.0, .15)
            if h == 'triste': sobrancelha(kx, x0, y0, -1.0, .09)
            if h == 'convencido': d.chord([x0 - er, y0 - er * 1.25, x0 + er, y0 + er * .2], 180, 360, fill=B)
            if h == 'choque': d.arc([x0 - er * 1.1, y0 - er * 1.9, x0 + er * 1.1, y0 - er * 1.2], 200, 340, fill=B, width=int(R2 * .05))
        boca({'bravo': 'dentes', 'furioso': 'dentes', 'choque': 'grito', 'triste': 'triste', 'convencido': 'sorrisinho'}.get(h, None) or '')
        if h == 'triste':
            for kx in (-1, 1): x0 = cx + kx * ex + s * R2 * .13; d.ellipse([x0 - er * .25, cy + ey + er * 1.1, x0 + er * .25, cy + ey + er * 1.7], fill=(90, 170, 255), outline=B, width=lw2 // 2)
    # chapeus (desenhados, autorais)
    top = cy - R2 * .82
    if chapeu == 'cartola':
        d.rectangle([cx - R2 * .5, top - R2 * .85, cx + R2 * .5, top + R2 * .05], fill=(24, 24, 28), outline=B, width=lw2); d.rectangle([cx - R2 * .5, top - R2 * .2, cx + R2 * .5, top - R2 * .05], fill=(180, 20, 35))
        d.ellipse([cx - R2 * .85, top - R2 * .05, cx + R2 * .85, top + R2 * .2], fill=(24, 24, 28), outline=B, width=lw2)
    if chapeu == 'cowboy':
        d.ellipse([cx - R2 * 1.05, top - R2 * .02, cx + R2 * 1.05, top + R2 * .3], fill=(140, 92, 48), outline=B, width=lw2)
        d.chord([cx - R2 * .55, top - R2 * .7, cx + R2 * .55, top + R2 * .35], 180, 360, fill=(160, 106, 56), outline=B, width=lw2); d.rectangle([cx - R2 * .53, top - R2 * .04, cx + R2 * .53, top + R2 * .06], fill=(90, 50, 25))
    if chapeu == 'quepe':
        d.rounded_rectangle([cx - R2 * .55, top - R2 * .45, cx + R2 * .55, top + R2 * .12], int(R2 * .1), fill=(40, 60, 120), outline=B, width=lw2)
        d.chord([cx + s * R2 * .1 - R2 * .55, top, cx + s * R2 * .1 + R2 * .55, top + R2 * .3], 0, 180, fill=(20, 20, 24))
    if chapeu == 'bicorne':
        d.chord([cx - R2 * 1.0, top - R2 * .6, cx + R2 * 1.0, top + R2 * .35], 180, 360, fill=(22, 26, 44), outline=B, width=lw2); d.line([cx - R2 * .9, top - R2 * .1, cx + R2 * .9, top - R2 * .1], fill=(230, 190, 60), width=lw2)
        d.ellipse([cx - R2 * .13, top - R2 * .45, cx + R2 * .13, top - R2 * .18], fill=(240, 240, 240), outline=B, width=lw2 // 2)
    if chapeu == 'pontudo':   # capacete com ponta
        d.chord([cx - R2 * .62, top - R2 * .5, cx + R2 * .62, top + R2 * .45], 180, 360, fill=(30, 30, 30), outline=B, width=lw2)
        d.polygon([(cx - R2 * .1, top - R2 * .45), (cx, top - R2 * .95), (cx + R2 * .1, top - R2 * .45)], fill=(200, 170, 60), outline=B); d.rectangle([cx - R2 * .62, top - R2 * .02, cx + R2 * .62, top + R2 * .1], fill=(200, 170, 60))
    out = im.resize((T // SS, T // SS), Image.LANCZOS); _BC[k] = out; return out

_RC = {}
def rifle_spr(r):
    if r in _RC: return _RC[r]
    L = int(r * 2.3 * SS); h = int(r * .5 * SS); im = Image.new('RGBA', (L, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); B = (0, 0, 0); lw = int(r * .035 * SS)
    d.polygon([(0, h * .35), (L * .3, h * .3), (L * .32, h * .62), (L * .05, h * .95), (0, h * .9)], fill=(150, 92, 44), outline=B, width=lw)   # coronha
    d.rectangle([L * .28, h * .3, L * .62, h * .6], fill=(126, 78, 36), outline=B, width=lw)
    d.rectangle([L * .55, h * .36, L * .99, h * .5], fill=(52, 54, 60), outline=B, width=lw); d.rectangle([L * .4, h * .55, L * .46, h * .8], fill=(40, 40, 44), outline=B, width=lw // 2)
    d.rectangle([L * .9, h * .22, L * .94, h * .37], fill=(40, 40, 44))
    out = im.resize((L // SS, h // SS), Image.LANCZOS); _RC[r] = out; return out

def estrela(d, x, y, r1, r2, n, cor, borda=None, rot=0, w=6):
    pts = [(x + math.cos(rot + k * math.pi / n) * (r1 if k % 2 == 0 else r2), y + math.sin(rot + k * math.pi / n) * (r1 if k % 2 == 0 else r2)) for k in range(2 * n)]
    d.polygon(pts, fill=cor, outline=borda);
    if borda: d.line(pts + [pts[0]], fill=borda, width=w)
def texto(img, s, x, y, n, cor, ang=0, esc=1.):
    if not s or esc <= 0: return
    n = int(n * esc); f = fnt(max(10, n))
    while f.getlength(s) > W - 70 and n > 30: n -= 4; f = fnt(n)
    if not ang: ImageDraw.Draw(img).text((x, y), s, font=f, fill=cor, anchor='mm', stroke_width=max(5, n // 8), stroke_fill=(0, 0, 0)); return
    tw = int(f.getlength(s) + n); t = Image.new('RGBA', (tw, int(n * 1.8))); ImageDraw.Draw(t).text((tw / 2, n * .9), s, font=f, fill=cor, anchor='mm', stroke_width=max(5, n // 8), stroke_fill=(0, 0, 0))
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC); x = clamp(x, t.width / 2 + 10, W - t.width / 2 - 10); img.alpha_composite(t, (int(x - t.width / 2), int(y - t.height / 2)))
def balao(img, x, y, c, u, lado):
    if u <= 0: return
    esc = back(u / .25); d = ImageDraw.Draw(img); txt = c.isascii(); f = fnt(int(62 * esc)) if txt else None
    w = (max(240, f.getlength(c) + 80) if txt else 250) * esc; h = 160 * esc; bx = clamp(x + lado * 70, w / 2 + 20, W - w / 2 - 20); by = y
    d.rounded_rectangle([bx - w / 2, by - h / 2, bx + w / 2, by + h / 2], int(46 * esc), fill=(255, 255, 255), outline=(0, 0, 0), width=7)
    tx = x + lado * 10; d.polygon([(tx - 26, by + h / 2 - 6), (x - lado * 20, by + h / 2 + 60 * esc), (tx + 30, by + h / 2 - 6)], fill=(255, 255, 255))
    d.line([(tx - 26, by + h / 2), (x - lado * 20, by + h / 2 + 60 * esc), (tx + 30, by + h / 2)], fill=(0, 0, 0), width=7)
    if txt: d.text((bx, by), c, font=f, fill=(0, 0, 0), anchor='mm')
    else: e = emoji(c, int(115 * esc)); img.alpha_composite(e, (int(bx - e.width / 2), int(by - e.height / 2)))

# ---------------- cena / linha do tempo ----------------
CENAS = R['cenas']; t = 0.
for c in CENAS: c['a'] = t; t += c['dur']; c['b'] = t
TOTAL = t
FORA = {'esq': (-.45, 0), 'dir': (1.45, 0), 'cima': (0, -.4), 'baixo': (0, 1.4)}
def lugar(c, nome, u):
    """posicao (x,y px), rotacao, sx, sy, humor, flash para o ator/objeto 'nome' no instante u da cena"""
    a = c['ents'][nome]; x, y = a['em'][0] * W, a['em'][1] * H; rot = 0.; sx = sy = 1.; humor = a.get('humor', 'normal'); flash = 0.; vis = True
    if a.get('entra'):
        t0 = a.get('t_in', 0); p = (u - t0) / .5
        if p < 0: vis = False
        fx, fy = FORA[a['entra']]; x0 = fx * W if fx else x; y0 = fy * H if fy else y; q = back(p)
        x, y = x0 + (x - x0) * q, y0 + (y - y0) * q
        if 0 < p < 1.2: sy = 1 - .18 * math.sin(clamp(p) * math.pi) * (1 if a['entra'] == 'cima' else .5); sx = 2 - sy
    if a.get('sai'):
        t0 = a.get('t_out', c['dur'] - .5); p = ease(clamp((u - t0) / .45)); fx, fy = FORA[a['sai']]
        x += ((fx * W if fx else x) - x) * p; y += ((fy * H if fy else y) - y) * p
    # respiracao / quique continuo (nunca parado)
    if a.get('tipo') != 'emoji' or a.get('vivo', True):
        ph = u * a.get('ritmo', 5.5) + hash(nome) % 7; b = abs(math.sin(ph)); y -= b * a.get('quique', 16); sy *= 1 + .045 * math.cos(2 * ph); sx *= 1 - .045 * math.cos(2 * ph)
    for e in c.get('acoes', []):
        dt = u - e['t']
        if dt < 0: continue
        tp = e['tipo']
        if e.get('a') == nome:
            if tp == 'humor': humor = e['h']
            if tp == 'tiro' and dt < .35: x -= a.get('olha', 1) * 40 * math.exp(-dt * 12); rot += a.get('olha', 1) * 8 * math.exp(-dt * 10)
            if tp == 'soco' and dt < .5:
                bx = c['ents'][e['b']]['em'][0] * W; k = math.sin(clamp(dt / .45) * math.pi); x += (bx - x) * .55 * k
            if tp == 'pulo' and dt < .6: k = math.sin(clamp(dt / .55) * math.pi); y -= 190 * k; sy *= 1 + .15 * k; sx *= 1 - .1 * k
            if tp == 'treme' and dt < e.get('d', 1.): x += 9 * math.sin(dt * 90); y += 5 * math.cos(dt * 70)
            if tp == 'cai': p = ease(clamp(dt / .35)); rot += e.get('rot', 180) * p; sy *= 1 - .25 * p; y += 20 * p
            if tp == 'nao' and dt < 1.: x += 26 * math.sin(dt * 28) * (1 - dt)
            if tp == 'some' and dt > 0: vis = False
            if tp == 'aparece': vis = dt >= 0
        if e.get('b') == nome and tp in ('tiro', 'soco'):
            di = dt - (.12 if tp == 'tiro' else .22)
            if di >= 0 and di < .7:
                lado = 1 if c['ents'][e['a']]['em'][0] < a['em'][0] else -1; k = math.exp(-di * 6)
                x += lado * 70 * k; rot -= lado * 16 * k; flash = max(flash, clamp(1 - di / .18)); humor = e.get('h', 'dor') if di < .6 else humor
                if a.get('tipo') != 'emoji': sx *= 1 + .12 * k; sy *= 1 - .12 * k
    if any(e['tipo'] == 'aparece' and e.get('a') == nome and u < e['t'] for e in c.get('acoes', [])): vis = False
    return x, y, rot, sx, sy, humor, flash, vis

def cola(img, spr, x, y, rot, sx, sy, flash):
    w, h = max(2, int(spr.width * sx)), max(2, int(spr.height * sy)); s = spr.resize((w, h), Image.BILINEAR)
    if flash > 0:
        wht = Image.new('RGBA', s.size, (255, 255, 255, 0)); wht.putalpha(s.getchannel('A').point(lambda v: int(v * flash * .85))); s = Image.alpha_composite(s, wht)
    if rot: s = s.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2)))

def quadro(fi):
    tt = fi / FPS; c = next((cc for cc in CENAS if cc['a'] <= tt < cc['b']), CENAS[-1]); u = tt - c['a']
    # tremor de camera e soco de zoom nas acoes fortes
    sh = 0.; pz = 0.
    for e in c.get('acoes', []):
        dt = u - e['t'] - (.12 if e['tipo'] == 'tiro' else 0)
        if 0 <= dt < .45 and e['tipo'] in ('tiro', 'explode', 'canhao', 'soco', 'pancada'): k = math.exp(-dt * 9) * (2. if e['tipo'] in ('explode', 'canhao') else 1.); sh += 22 * k; pz += .05 * k
    jx, jy = sh * math.sin(tt * 97), sh * math.cos(tt * 83)
    if c.get('fundo') == 'ilha':
        z = 1.04 + .03 * u / c['dur'] + pz; bw, bh = W / z, H / z; img = ILHA.crop((int((W - bw) / 2 + jx), int((H - bh) / 2 + jy), int((W + bw) / 2 + jx), int((H + bh) / 2 + jy))).resize((W, H), Image.BILINEAR)
    else:
        lon, lat, z0 = c['cam']; cx, cy = xy(lon, lat); z = z0 * (1 + .05 * u / c['dur'] + pz); vw, vh = W / z, H / z
        img = MAPA.crop((int(cx - vw / 2 + jx), int(cy - vh / 2 + jy), int(cx + vw / 2 + jx), int(cy + vh / 2 + jy))).resize((W, H), Image.BILINEAR).convert('RGBA')
    d = ImageDraw.Draw(img)
    # sombras no chao + personagens/objetos (de tras para frente pelo y)
    ents = sorted(c.get('ents', {}).items(), key=lambda kv: kv[1]['em'][1])
    pos = {}
    for nome, a in ents:
        x, y, rot, sx, sy, humor, flash, vis = lugar(c, nome, u); pos[nome] = (x, y, a)
        if not vis: continue
        r = a.get('r', 230) if a.get('tipo') != 'emoji' else a.get('tam', 300) / 2
        sw = Image.new('RGBA', (int(r * 2), int(r * .5))); ImageDraw.Draw(sw).ellipse([0, 0, int(r * 2) - 1, int(r * .5) - 1], fill=(0, 0, 0, 70)); img.alpha_composite(sw, (int(x - r), int(a['em'][1] * H + r * .82)))
        if a.get('tipo') == 'emoji':
            spr = emoji(a['e'], a.get('tam', 300)); spr = spr.transpose(Image.FLIP_LEFT_RIGHT) if a.get('vira') else spr
            cola(img, spr, x, y, rot, sx, sy, flash)
        else:
            olha = a.get('olha', 1); r = a.get('r', 230)
            if a.get('arma') == 'rifle':   # rifle atras do corpo na mao do lado que olha
                tiro = [e for e in c.get('acoes', []) if e['tipo'] == 'tiro' and e.get('a') == nome and 0 <= u - e['t'] < .35]
                kick = math.exp(-(u - tiro[0]['t']) * 10) if tiro else 0
                ang = a.get('mira', 0) + 14 * kick; rs = rifle_spr(r); rs = rs if olha > 0 else rs.transpose(Image.FLIP_LEFT_RIGHT)
                rr = rs.rotate(ang * olha, expand=True, resample=Image.BICUBIC); gx = x + olha * (r * .55 - 30 * kick); gy = y + r * .42
                img.alpha_composite(rr, (int(gx - rr.width / 2), int(gy - rr.height / 2)))
                pos[nome + ':cano'] = (gx + olha * rs.width * .5 * math.cos(math.radians(ang)), gy - rs.width * .5 * math.sin(math.radians(ang)) - r * .05)
            cola(img, sprite(a['flag'], r, humor, a.get('chapeu'), olha), x, y, rot, sx, sy, flash)
    # efeitos
    for e in c.get('acoes', []):
        dt = u - e['t']; tp = e['tipo']
        if dt < 0: continue
        if tp == 'tiro' and e['a'] + ':cano' in pos and dt < .5:
            mx, my = pos[e['a'] + ':cano']; bx, by, _ = pos[e['b']]
            if dt < .1: estrela(d, mx, my, 120, 55, 8, (255, 236, 90), (255, 130, 0), rot=dt * 20); estrela(d, mx, my, 55, 25, 8, (255, 255, 255))
            if dt < .14: p = clamp(dt / .12); d.line([mx + (bx - mx) * max(0, p - .35), my + (by - my) * max(0, p - .35), mx + (bx - mx) * p, my + (by - my) * p], fill=(255, 240, 120), width=12)
            for k in range(4):   # fumaca do cano
                q = dt * 1.5; rr = 22 + 50 * q + k * 8; a_ = int(170 * (1 - clamp(dt / .5)))
                if a_ > 0: d.ellipse([mx - rr + k * 18, my - rr - 60 * q - k * 12, mx + rr + k * 18, my + rr - 60 * q - k * 12], fill=(230, 230, 230, a_))
        if tp in ('tiro', 'soco') and e.get('b') in pos:
            di = dt - (.12 if tp == 'tiro' else .22); bx, by, b = pos[e['b']]
            if 0 <= di < .5:
                rr = b.get('r', b.get('tam', 300) / 2)
                if di < .16: estrela(d, bx, by, rr * 1.1 * (.6 + di * 3), rr * .5, 10, (255, 250, 200), (255, 180, 40))
                texto(img, e.get('som', 'BAM!' if tp == 'tiro' else 'POW!'), bx + (40 if hash(e['b']) % 2 else -40), by - rr * 1.05, 120, (255, 220, 40), ang=12 if tp == 'tiro' else -10, esc=back(di / .2))
            if .3 <= di < 1.5 and e.get('tontura', True):   # estrelinhas girando
                rr = b.get('r', b.get('tam', 300) / 2)
                for k in range(3):
                    an = di * 7 + k * 2.1; st = emoji('⭐', 70); img.alpha_composite(st, (int(bx + math.cos(an) * rr * .9 - 35), int(by - rr * .95 + math.sin(an) * rr * .25 - 35)))
        if tp in ('explode', 'canhao'):
            ex, ey = (e['em'][0] * W, e['em'][1] * H) if 'em' in e else pos[e['b']][:2]
            if dt < .9:
                p = clamp(dt / .9); R0 = e.get('tam', 260) * (.4 + 1.1 * ease(clamp(dt / .3)))
                for k, cor in enumerate(((90, 80, 80), (255, 120, 30), (255, 200, 60), (255, 250, 210))):
                    rr = R0 * (1 - k * .2) * (1 - .5 * p if k else 1)
                    if rr > 2:
                        lay = Image.new('RGBA', (W, H)); dl = ImageDraw.Draw(lay)
                        for j in range(7): an = j * 0.9 + k; dl.ellipse([ex + math.cos(an) * rr * .35 - rr * .65, ey + math.sin(an) * rr * .3 - rr * .65 - 120 * p * (k == 0), ex + math.cos(an) * rr * .35 + rr * .65, ey + math.sin(an) * rr * .3 + rr * .65 - 120 * p * (k == 0)], fill=(*cor, int(255 * (1 - p * (k > 0)))))
                        img.alpha_composite(lay)
                if dt < .5: texto(img, e.get('som', 'BOOM!'), ex, ey - R0 * .9, 140, (255, 90, 40), ang=-8, esc=back(dt / .2))
        if tp == 'fumaca' and dt < 1.2:   # vapor de raiva saindo da cabeca
            bx, by, b = pos[e['a']]; rr = b.get('r', 230)
            for k in (-1, 1):
                for j in range(3):
                    q = (dt * 2 + j * .33) % 1; d.ellipse([bx + k * rr * (.6 + .3 * q) - 30 - 30 * q, by - rr * (1. + .8 * q) - 30 - 30 * q, bx + k * rr * (.6 + .3 * q) + 30 + 30 * q, by - rr * (1. + .8 * q) + 30 + 30 * q], fill=(245, 245, 245, int(220 * (1 - q))))
        if tp == 'suor' and dt < 2:
            bx, by, b = pos[e['a']]; rr = b.get('r', 230); q = (dt * 1.3) % 1
            sw = emoji('💦', 90); img.alpha_composite(sw, (int(bx + rr * .7), int(by - rr * .9 + q * 60)))
        if tp == 'halo':
            bx, by, b = pos[e['a']]; rr = b.get('r', b.get('tam', 300) / 2); hy = by - rr * 1.05 + 8 * math.sin(u * 6)
            d.ellipse([bx - rr * .6, hy - rr * .14, bx + rr * .6, hy + rr * .14], outline=(255, 225, 60), width=16)
    for bl in c.get('baloes', []):
        bx, by, b = pos[bl['a']]; rr = b.get('r', b.get('tam', 300) / 2)
        if u < bl.get('ate', 99): balao(img, bx, by - rr * 1.55, bl['c'], u - bl.get('t', .2), 1 if bx < W / 2 else -1)
    # textos (parte de cima, fora da interface do Shorts)
    if c.get('ano'): texto(img, c['ano'], W / 2, 200, 170, (255, 255, 255), esc=back(u / .3))
    y0 = 360 if c.get('ano') else 250
    if c.get('titulo'): texto(img, c['titulo'][0], W / 2, 250, 150, (255, 214, 0), esc=back(u / .3)); texto(img, c['titulo'][1], W / 2, 400, 110, (255, 255, 255), esc=back((u - .15) / .3))
    if c.get('txt'): texto(img, c['txt'], W / 2, y0, 84, (255, 214, 0) if c.get('destaque') else (255, 255, 255), esc=back(u / .25))
    if c.get('sub'): texto(img, c['sub'], W / 2, y0 + 110, 96, (255, 214, 0), esc=back((u - .35) / .25))
    fad = min(1, tt / .15, (TOTAL - tt) / .25)
    rgb = img.convert('RGB')
    return Image.eval(rgb, lambda v: int(v * fad)) if fad < 1 else rgb

# ---------------- som: musica + efeitos ----------------
SR = 48000
def ler(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768
SFX = {}
def sfx(nome):
    fs = sorted(f for f in os.listdir('dados/sfx') if f.startswith(nome) and not f.endswith('.md'))
    if nome not in SFX: SFX[nome] = [ler('dados/sfx/' + f) for f in fs]
    return random.choice(SFX[nome])
def som():
    random.seed(7); n = int(TOTAL * SR); fx = np.zeros(n)
    def put(s, t, g=1.):
        a = int(t * SR)
        if a < n: L = min(len(s), n - a); fx[a:a + L] += s[:L] * g
    tt = np.arange(int(.5 * SR)) / SR
    for c in CENAS:
        for nome, a in c.get('ents', {}).items():
            if a.get('entra'): put(sfx('swish'), c['a'] + a.get('t_in', 0), .6)
        for e in c.get('acoes', []):
            t0 = c['a'] + e['t']; tp = e['tipo']
            if tp == 'tiro': put(sfx('tiro'), t0, .9); put(sfx('pancada'), t0 + .12, .7)
            if tp == 'soco': put(sfx('swish'), t0, .6); put(sfx('soco'), t0 + .22, 1.)
            if tp in ('explode', 'canhao'): put(sfx('canhao' if tp == 'canhao' else 'explosao'), t0, 1.)
            if tp == 'pulo': put(sfx('pulo'), t0, .7)
            if tp == 'pancada': put(sfx('pancada'), t0, 1.); put(sfx('queda'), t0, .8)
            if tp == 'cai': put(sfx('queda'), t0 + .2, .9)
            if tp == 'oink': s = np.sign(np.sin(2 * np.pi * (220 + 90 * np.sin(tt * 32)) * tt)) * np.exp(-tt * 7) * .35; put(s, t0); put(s * .8, t0 + .22)
            if tp == 'treme' or tp == 'fumaca': put(np.random.default_rng(1).standard_normal(int(.6 * SR)) * np.linspace(.15, 0, int(.6 * SR)), t0, .5)
            if tp == 'nao': put(sfx('pizzi'), t0, .8)
            if tp == 'aparece': put(sfx('pizzi'), t0, .7)
            if tp == 'vitoria': put(sfx('nes'), t0, .8)
        for bl in c.get('baloes', []): put(sfx('pizzi'), c['a'] + bl.get('t', .2), .45)
    mus = ler(R['musica']); off = int(R.get('musica_ini', 0) * SR); mus = np.tile(mus, 3)[off:off + n]
    env = np.minimum(1, np.minimum(np.arange(n) / (SR * .3), (n - np.arange(n)) / (SR * 1.2)))
    duck = np.convolve(np.abs(fx), np.ones(4800) / 4800, 'same'); duck = 1 - .5 * np.clip(duck * 6, 0, 1)
    out = mus * .55 * duck * env + fx * env; out = np.tanh(out * 1.3) / np.tanh(1.3)
    w = wave.open(f'{OUT}/audio.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

if __name__ == '__main__':
    so = [float(x) for x in sys.argv[2:]]
    if so:
        for x in so: quadro(int(x * FPS)).save(f'{OUT}/q{int(x * FPS):05d}.jpg', quality=88)
        sys.exit()
    N = int(TOTAL * FPS)
    import multiprocessing as mp
    def job(i): quadro(i).save(f'{OUT}/frames/f{i:05d}.jpg', quality=92)
    with mp.get_context('fork').Pool(4) as pool: pool.map(job, range(N), chunksize=15)
    som()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{OUT}/frames/f%05d.jpg', '-i', f'{OUT}/audio.wav', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p',
                    '-af', 'loudnorm=I=-14:TP=-1.5', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', f'{OUT}/{RID}.mp4'], check=True)
    print('pronto', f'{OUT}/{RID}.mp4', round(TOTAL, 1))
