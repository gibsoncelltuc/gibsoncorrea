"""Texturas pintadas à mão (numpy/PIL) para objetos de cena: tábuas com pregos, aduelas, palha, celeiro, corda, ferro, lona, pedra, decalques com letras estampadas,
caminho de terra. Pinceladas visíveis, variação de cor, desgaste e sujeira — o nível de detalhe dos cenários do canal. Determinístico (seed fixo); salvo em blender/tex/."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from . import texlib
from .texlib import fbm, strokes, _hex, _save, exists, _rng, TEX
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def _font(sz):
    try: return ImageFont.truetype(FONT, sz)
    except Exception: return ImageFont.load_default()
def _finish(a, seed, n=1200, alpha=.12, length=(24, 80), width=(2, 6), warm=0.0):
    """acabamento "pintado": pinceladas + modulação suave + leve virada quente nos claros"""
    a = strokes(np.clip(a, 0, 1), seed + 101, n, alpha=alpha, length=length, width=width); H, W = a.shape[:2]
    a = a * (.88 + .24 * fbm(H, W, 3, seed + 102, 2)[..., None])
    if warm: a = a + warm * np.array([.05, .02, -.03], np.float32) * (a.mean(2, keepdims=True) > .5)
    return np.clip(a, 0, 1)
def planks(name, seed, base='#c4975c', dark='#4a2f1e', n=4, vertical=False, nails=True, size=1024, tone=(.8, 1.15)):
    """tábuas com veios, nós, frestas escuras e (opcional) cabeças de prego nas pontas — base de caixotes, celeiro, portas"""
    if exists(name): return os.path.join(TEX, name)
    r = _rng(seed); H = W = size; a = np.zeros((H, W, 3), np.float32); ph = H // n; cb, cd = _hex(base), _hex(dark)
    g1 = fbm(H, W, 5, seed, 3, aspect=(1, 26)); g2 = fbm(H, W, 4, seed + 7, 9, aspect=(1, 44))
    for i in range(n):
        y0, y1 = i * ph, (i + 1) * ph; t = r.uniform(*tone); sh = g1[y0:y1] * .6 + g2[y0:y1] * .4
        col = cb[None, None, :] * (t * (.70 + .55 * sh[..., None])); col = col * (1 - .28 * np.abs(np.linspace(-1, 1, ph))[:, None, None] ** 5); a[y0:y1] = col
        a[y0:y0 + 3] = cd * .5; a[y1 - 3:y1] = cd * .5; a[y0 + 3:y0 + 7] = np.clip(a[y0 + 3:y0 + 7] * 1.25, 0, 1)      # fresta + brilho de borda
        for _ in range(r.integers(0, 3)):                                                                              # nós
            cx, cy = r.random() * W, y0 + r.random() * ph; yy, xx = np.mgrid[y0:y1, 0:W]; d = ((xx - cx) / 20) ** 2 + ((yy - cy) / 10) ** 2
            a[y0:y1] = np.where((d < 1)[..., None], cd * (.45 + .55 * d[..., None]), a[y0:y1])
        if nails:
            for x in (26, W - 26):
                yy, xx = np.mgrid[y0:y1, 0:W]; cy = (y0 + y1) / 2 + r.normal(0, 4); d = ((xx - x) ** 2 + (yy - cy) ** 2) ** .5
                a[y0:y1] = np.where((d < 7)[..., None], cd * .35, a[y0:y1]); a[y0:y1] = np.where(((d >= 7) & (d < 9))[..., None], cd * .7, a[y0:y1])
    a = _finish(a, seed, 1500, .14, (30, 100), (2, 5), warm=.6)
    if vertical: a = np.rot90(a)
    return _save(a, name)
def staves(name='barrel_staves.png', seed=31, base='#b3824b', dark='#3d2616', n=10):
    return planks(name, seed, base, dark, n, vertical=True, nails=False)
def straw(name='straw.png', seed=41, size=1024):
    """palha/feno: milhares de fios dourados em ângulos próximos, com sombras e brilhos"""
    if exists(name): return os.path.join(TEX, name)
    H = W = size; base = _hex('#d6ad52'); a = np.ones((H, W, 3), np.float32) * base * (.8 + .35 * fbm(H, W, 5, seed, 4, aspect=(1, 6))[..., None])
    r = _rng(seed); im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im, 'RGBA')
    pal = [(240, 207, 122), (201, 153, 63), (168, 122, 44), (226, 184, 86), (120, 86, 34)]
    for _ in range(5200):
        x, y = r.random() * W, r.random() * H; l = r.uniform(60, 220); ang = r.normal(0.05, 0.22); c = pal[r.integers(0, len(pal))]
        d.line([x, y, x + l * np.cos(ang), y + l * np.sin(ang)], fill=c + (int(r.uniform(60, 150)),), width=int(r.uniform(2, 5)))
    return _save(_finish(np.asarray(im, np.float32) / 255, seed, 300, .1), name)
def barn_red(name='barn_red.png', seed=51, size=1024):
    """celeiro: tábuas verticais vermelhas desbotadas, manchas de umidade, descascados"""
    if exists(name): return os.path.join(TEX, name)
    p = planks('_barn_raw.png', seed, '#a6402f', '#3a1812', 8, vertical=True, nails=False, tone=(.75, 1.1)); a = np.asarray(Image.open(p).convert('RGB'), np.float32) / 255; H, W = a.shape[:2]
    streak = fbm(H, W, 4, seed, 12, aspect=(14, 1)); a = a * (.85 + .3 * streak[..., None]); chips = fbm(H, W, 6, seed + 5, 8) > .72; a = np.where(chips[..., None], a * .55 + _hex('#c9b690') * .45, a)
    return _save(_finish(a, seed, 900, .12), name)
def rope(name='rope.png', seed=61, size=512):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; yy, xx = np.mgrid[0:H, 0:W]; ph = ((xx + yy * .6) / 18.0) % 1.0; s = np.where(ph < .5, 1.0, .62)[..., None]; a = _hex('#b98d52')[None, None, :] * s * (.85 + .3 * fbm(H, W, 4, seed, 20)[..., None])
    return _save(_finish(a, seed, 400, .1, (8, 24), (1, 3)), name)
def iron(name='iron.png', seed=71, size=512):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; a = _hex('#2b2a31')[None, None, :] * (.7 + .6 * fbm(H, W, 5, seed, 5)[..., None]); rust = (fbm(H, W, 5, seed + 3, 7) > .68)[..., None]; a = np.where(rust, a * .4 + _hex('#8a4a22') * .6, a)
    return _save(_finish(a, seed, 600, .12, (12, 50), (1, 4)), name)
def canvas(name='canvas.png', seed=81, base='#e6d8b6', size=1024):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; yy, xx = np.mgrid[0:H, 0:W]; weave = (.93 + .07 * (np.sin(xx * .9) * np.sin(yy * .9)))[..., None]; a = _hex(base)[None, None, :] * weave * (.82 + .3 * fbm(H, W, 5, seed, 3)[..., None])
    stain = (fbm(H, W, 5, seed + 9, 3) > .66)[..., None]; a = np.where(stain, a * .82, a); a[:, ::256] *= .78; a[::256, :] *= .8                                  # costuras
    return _save(_finish(a, seed, 900, .1, (30, 110), (3, 8), warm=.5), name)
def stone(name='stone.png', seed=91, size=1024):
    if exists(name): return os.path.join(TEX, name)
    r = _rng(seed); H = W = size; a = np.ones((H, W, 3), np.float32) * _hex('#4a453f'); im = Image.fromarray((a * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    y = 0
    while y < H:
        h = int(r.uniform(70, 120)); x = -int(r.uniform(0, 90))
        while x < W:
            w = int(r.uniform(90, 200)); c = int(r.uniform(.55, 1.0) * 190); col = (int(c * .93), int(c * .88), int(c * .8)); d.rounded_rectangle([x + 5, y + 5, x + w - 5, y + h - 5], 18, fill=col); x += w
        y += h
    a = np.asarray(im, np.float32) / 255; a = a * (.82 + .3 * fbm(H, W, 5, seed, 6)[..., None]); return _save(_finish(a, seed, 800, .12, (20, 60), (2, 6)), name)
def rock(name='rock.png', seed=95, size=512):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; a = _hex('#85807a')[None, None, :] * (.65 + .6 * fbm(H, W, 6, seed, 4, aspect=(3, 1))[..., None]); a = np.where((fbm(H, W, 4, seed + 2, 9) > .7)[..., None], a * .8 + _hex('#a8a04a') * .2, a)
    return _save(_finish(a, seed, 600, .12), name)
def cloth(name, color, seed=1, size=256):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; yy, xx = np.mgrid[0:H, 0:W]; a = _hex(color)[None, None, :] * (.9 + .1 * np.sin(xx * 1.1) * np.sin(yy * 1.1))[..., None] * (.85 + .3 * fbm(H, W, 4, seed, 3)[..., None])
    return _save(_finish(a, seed, 200, .1, (10, 30), (2, 5)), name)
def stencil(text, name=None, color=(36, 26, 22), size=(512, 256), sz=120, angle=0.0, distress=True):
    """decalque RGBA (fundo transparente) com letras estampadas e tinta desgastada — para caixotes, barris, sacos, placas"""
    name = name or 'stencil_' + ''.join(c for c in text if c.isalnum()) + '.png'
    if exists(name): return os.path.join(TEX, name)
    W, H = size; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = _font(sz)
    while sz > 20 and d.multiline_textbbox((0, 0), text, font=f, align='center')[2] > W * .92: sz -= 6; f = _font(sz)
    d.multiline_text((W / 2, H / 2), text, font=f, fill=color + (235,), anchor='mm', align='center', spacing=8)
    a = np.asarray(im, np.float32) / 255
    if distress: n = fbm(H, W, 5, 5, 8); a[..., 3] *= np.clip((n - .22) * 5.0, 0, 1) * .85 + .15
    if angle: im = Image.fromarray((a * 255).astype(np.uint8)).rotate(angle, expand=False, resample=Image.BICUBIC); a = np.asarray(im, np.float32) / 255
    p = os.path.join(TEX, name); Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), 'RGBA').save(p); return p
def dirt_path(name='dirt_path.png', seed=111, W=1024, H=256):
    """faixa de terra batida com bordas irregulares, sulcos de roda e pedrinhas (RGBA) — decalque de caminho"""
    if exists(name): return os.path.join(TEX, name)
    r = _rng(seed); yy, xx = np.mgrid[0:H, 0:W]; cy = H / 2 + 14 * np.sin(xx / 140.0) ; dist = np.abs(yy - cy) / (H * .46)
    edge = dist + .22 * (fbm(H, W, 5, seed, 6, aspect=(4, 1)) - .5); alpha = np.clip((1 - edge) * 3.2, 0, 1)
    base = _hex('#9a7248')[None, None, :] * (.8 + .4 * fbm(H, W, 5, seed + 1, 5, aspect=(4, 1))[..., None])
    for off in (-.28, .28): rut = np.exp(-(((yy - cy) / (H * .46) - off) / .06) ** 2)[..., None]; base = base * (1 - .32 * rut)
    for _ in range(220): x, y = r.integers(0, W), r.integers(int(H * .25), int(H * .75)); rr = r.integers(2, 6); base[max(0, y - rr):y + rr, max(0, x - rr):x + rr] *= r.uniform(.7, 1.25)
    a = _finish(base, seed, 700, .12, (30, 90), (3, 7)); rgba = np.concatenate([a, alpha[..., None]], 2)
    p = os.path.join(TEX, name); Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), 'RGBA').save(p); return p
def scatter(name, kind, seed, size=512, n=60):
    """decalque RGBA de detalhes espalhados no chão: 'straw' (fios de palha), 'leaves' (folhas de repolho), 'chips' (lascas de madeira)"""
    if exists(name): return os.path.join(TEX, name)
    r = _rng(seed); im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = r.random() * size, r.random() * size; a = r.uniform(0, 6.28)
        if kind == 'straw': l = r.uniform(18, 46); d.line([x, y, x + l * np.cos(a), y + l * np.sin(a)], fill=(222, 182, 88, 230), width=2)
        elif kind == 'leaves': rx, ry = r.uniform(10, 22), r.uniform(7, 14); d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=(int(r.uniform(90, 150)), int(r.uniform(140, 190)), int(r.uniform(60, 90)), 235), outline=(60, 90, 40, 255))
        else: l = r.uniform(8, 18); d.line([x, y, x + l * np.cos(a), y + l * np.sin(a)], fill=(176, 128, 78, 240), width=3)
    p = os.path.join(TEX, name); im.filter(ImageFilter.GaussianBlur(.6)).save(p); return p

def rings(name='rings.png', seed=121, size=512):
    """topo de tora/toco: anéis de crescimento concêntricos (tons de madeira clara), borda de casca escura, rachaduras"""
    if exists(name): return os.path.join(TEX, name)
    H = W = size; yy, xx = np.mgrid[0:H, 0:W]; r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)); wob = fbm(H, W, 4, seed, 3) * .08
    ph = np.sin((r + wob) * 46.0) * .5 + .5; a = _hex('#d2a96c')[None, None, :] * (.78 + .3 * ph[..., None]) * (.9 + .2 * fbm(H, W, 4, seed + 1, 8)[..., None])
    a = np.where((r > .86)[..., None], _hex('#4a3020')[None, None, :] * (.7 + .5 * fbm(H, W, 5, seed + 2, 10)[..., None]), a)
    ang = np.arctan2(yy - H / 2, xx - W / 2); crack = (np.abs(np.sin(ang * 3 + 1.1)) < .03) & (r < .8) & (r > .1); a = np.where(crack[..., None], a * .45, a)
    return _save(_finish(a, seed, 300, .1, (10, 40), (1, 3)), name)

def bulwark(name='bulwark.png', seed=131, W=1024, H=512):
    """amurada de fragata: casco preto, faixa ocre e portinholas brancas/vermelhas (tábuas horizontais por baixo da tinta)"""
    if exists(name): return os.path.join(TEX, name)
    p = planks('_bw_raw.png', seed, '#3a3340', '#0e0c12', 6, vertical=False, nails=False, tone=(.8, 1.1)); a = np.asarray(Image.open(p).convert('RGB').resize((W, H)), np.float32) / 255
    a = a * .55; yy = np.arange(H)[:, None]; stripe = ((yy > H * .42) & (yy < H * .56)); a = np.where(stripe[..., None], _hex('#d7a63a')[None, None, :] * (.7 + .4 * fbm(H, W, 4, seed, 6)[..., None]), a)
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    for cx in (W * .25, W * .75): d.rectangle([cx - 78, H * .12, cx + 78, H * .40], fill=(34, 26, 30)); d.rectangle([cx - 70, H * .15, cx + 70, H * .37], fill=(176, 40, 34)); d.rectangle([cx - 78, H * .12, cx + 78, H * .40], outline=(240, 236, 226), width=6)
    a = np.asarray(im, np.float32) / 255; return _save(_finish(a, seed, 700, .1, (30, 90), (2, 5)), name)
