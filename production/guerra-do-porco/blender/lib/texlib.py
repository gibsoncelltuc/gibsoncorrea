"""Texturas pintadas por código (numpy/PIL) — brush strokes, grão de madeira, tecidos, bandeiras, letreiros, notas. Salvas em blender/tex/."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from . import util
TEX = util.TEX; os.makedirs(TEX, exist_ok=True)
def _rng(s): return np.random.default_rng(s)
def fbm(h, w, octaves=5, seed=0, base=4, aspect=(1, 1)):
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0.0
    for o in range(octaves):
        gx = max(2, int(base * aspect[0] * 2 ** o)); gy = max(2, int(base * aspect[1] * 2 ** o))
        g = _rng(seed * 31 + o).random((gy + 1, gx + 1)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC); out += amp * np.asarray(im, np.float32) / 255; tot += amp; amp *= 0.5
    return out / tot
def _save(a, name):
    p = os.path.join(TEX, name); Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).save(p); return p
def _hex(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)
def exists(name): return os.path.exists(os.path.join(TEX, name))

def strokes(img, seed, n=900, color=None, alpha=.18, length=(10, 40), width=(2, 6)):
    """pinceladas semitransparentes sobre a imagem (look pintado à mão)"""
    r = _rng(seed); im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)); H, W = img.shape[:2]
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = r.random() * W, r.random() * H; l = r.uniform(*length); a = r.uniform(-.6, .6); w = int(r.uniform(*width))
        c = tuple(int(v * 255) for v in (color if color is not None else np.clip(img[int(y) % H, int(x) % W] * r.uniform(.8, 1.2), 0, 1)))
        d.line([x, y, x + l * np.cos(a), y + l * np.sin(a)], fill=c + (int(alpha * 255),), width=w)
    ov = ov.filter(ImageFilter.GaussianBlur(.8)); im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); return np.asarray(im, np.float32) / 255

def wood_planks(name='wood_planks.png', seed=3, base='#b98a55', dark='#5a3a26', size=1024, n=8, vertical=False):
    if exists(name): return os.path.join(TEX, name)
    r = _rng(seed); H = W = size; a = np.zeros((H, W, 3), np.float32); ph = H // n; cb, cd = _hex(base), _hex(dark)
    gr = fbm(H, W, 5, seed, 3, aspect=(1, 24))               # veios esticados
    gr2 = fbm(H, W, 4, seed + 7, 8, aspect=(1, 40))
    for i in range(n):
        tone = 0.78 + 0.4 * r.random(); y0, y1 = i * ph, (i + 1) * ph
        sh = (gr[y0:y1] * .6 + gr2[y0:y1] * .4)
        col = cb[None, None, :] * (tone * (.72 + .5 * sh[..., None]))
        col = col * (1 - .25 * np.abs(np.linspace(-1, 1, ph))[:, None, None] ** 4)          # borda da tábua mais escura
        a[y0:y1] = col
        a[y0:y0 + 3] = cd * .55; a[y1 - 3:y1] = cd * .55                                        # fresta
        for k in range(r.integers(1, 3)): x = int(r.random() * W); a[y0:y1, x:x + 2] = cd * .6       # junta de topo
        for k in range(r.integers(0, 3)):                                                              # nós
            cx, cy = r.random() * W, y0 + r.random() * ph; yy, xx = np.mgrid[y0:y1, 0:W]; d = ((xx - cx) / 18) ** 2 + ((yy - cy) / 9) ** 2
            a[y0:y1] = np.where((d < 1)[..., None], cd * (.5 + .5 * d[..., None]), a[y0:y1])
    a = strokes(a, seed + 1, 1400, alpha=.14, length=(30, 90), width=(2, 5)); a = np.clip(a * (.85 + .3 * fbm(H, W, 3, seed + 2, 2)[..., None]), 0, 1)
    if vertical: a = np.rot90(a)
    return _save(a, name)
def grass_ground(name='grass_ground.png', seed=5, c1='#7a8a3a', c2='#d9bf5a', c3='#4f6a2e', size=1024):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; n1 = fbm(H, W, 6, seed, 3); n2 = fbm(H, W, 4, seed + 3, 10)
    a = _hex(c1)[None, None] * (1 - n1[..., None]) + _hex(c2)[None, None] * n1[..., None]; a = a * (1 - .3 * (n2[..., None] > .62)) + _hex(c3)[None, None] * .3 * (n2[..., None] > .62)
    a = strokes(a, seed + 2, 5200, alpha=.22, length=(6, 22), width=(1, 3)); return _save(np.clip(a, 0, 1), name)
def soil(name='soil.png', seed=8, size=512):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; n = fbm(H, W, 6, seed, 5); a = _hex('#6b4630')[None, None] * (.65 + .7 * n[..., None]); a = strokes(a, seed, 1800, alpha=.2, length=(8, 26), width=(2, 4)); return _save(np.clip(a, 0, 1), name)
def sand(name='sand.png', seed=9, size=512):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; n = fbm(H, W, 6, seed, 6); a = _hex('#e2c98c')[None, None] * (.8 + .35 * n[..., None]); a = strokes(a, seed, 900, alpha=.16); return _save(np.clip(a, 0, 1), name)
def logs(name='logs.png', seed=11, size=512):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; n = 6; ph = H // n; a = np.zeros((H, W, 3), np.float32); gr = fbm(H, W, 5, seed, 3, aspect=(1, 18))
    for i in range(n):
        t = np.linspace(0, 1, ph)[:, None]; shade = .55 + .75 * np.sin(t * np.pi) ** .6; col = _hex('#b27a4a')[None, None] * shade[..., None] * (.8 + .4 * gr[i * ph:(i + 1) * ph, :, None]); a[i * ph:(i + 1) * ph] = col
        a[(i + 1) * ph - 4:(i + 1) * ph] = _hex('#3a2418')
    a = strokes(a, seed, 1500, alpha=.16, length=(30, 100)); return _save(np.clip(a, 0, 1), name)
def shingles(name='shingles.png', seed=12, c1='#7a4a3a', c2='#a86a4a', size=512):
    if exists(name): return os.path.join(TEX, name)
    r = _rng(seed); H = W = size; a = np.zeros((H, W, 3), np.float32); n = 8; ph = H // n; sw = 42
    for i in range(n):
        for k in range(-1, W // sw + 2):
            x0 = k * sw + (i % 2) * sw // 2; col = _hex(c1) * (1 - (t := r.random())) + _hex(c2) * t; col = col * (.85 + .3 * r.random())
            a[i * ph:(i + 1) * ph - 2, max(0, x0):min(W, x0 + sw - 2)] = col
        a[(i + 1) * ph - 3:(i + 1) * ph] = .12
    a = strokes(a, seed, 900, alpha=.14); return _save(np.clip(a, 0, 1), name)
def sail(name='sail.png', seed=13, size=512):
    if exists(name): return os.path.join(TEX, name)
    H = W = size; n = fbm(H, W, 5, seed, 4); a = _hex('#f1e6c8')[None, None] * (.86 + .22 * n[..., None])
    for i in range(1, 8): a[i * (H // 8) - 1:i * (H // 8) + 1] *= .8
    a[int(H * .8):] *= .93; a = strokes(a, seed, 800, alpha=.1, length=(40, 120), width=(2, 4)); return _save(np.clip(a, 0, 1), name)
def hull(name='hull.png', seed=14, w=1024, h=256):
    if exists(name): return os.path.join(TEX, name)
    r = _rng(seed); a = np.ones((h, w, 3), np.float32) * _hex('#1d1a2a'); gold = _hex('#e8b440')
    a[int(h * .30):int(h * .38)] = gold; a[int(h * .62):int(h * .70)] = gold
    nports = 12
    for i in range(nports):
        x0 = int((i + .5) * w / nports) - 30; a[int(h * .38):int(h * .62), x0:x0 + 60] = gold; a[int(h * .43):int(h * .58), x0 + 6:x0 + 54] = _hex('#15121c')
    a = a * (.85 + .3 * fbm(h, w, 5, seed, 8, aspect=(4, 1))[..., None]); a = strokes(a, seed, 600, alpha=.1, length=(40, 120)); return _save(np.clip(a, 0, 1), name)
def flag_us(name='flag_us.png', w=512, h=320):
    if exists(name): return os.path.join(TEX, name)
    im = Image.new('RGB', (w, h), (251, 246, 238)); d = ImageDraw.Draw(im); sh = h / 13
    for i in range(13):
        if i % 2 == 0: d.rectangle([0, i * sh, w, (i + 1) * sh], fill=(190, 40, 48))
    d.rectangle([0, 0, w * .42, sh * 7], fill=(38, 53, 107))
    for y in range(5):
        for x in range(6): cx = w * .42 * (x + .6) / 6.2 + (y % 2) * 8; cy = sh * 7 * (y + .6) / 5.2; d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(251, 246, 238))
    p = os.path.join(TEX, name); im.save(p); return p
def flag_uk(name='flag_uk.png', w=512, h=320):
    if exists(name): return os.path.join(TEX, name)
    im = Image.new('RGB', (w, h), (29, 47, 111)); d = ImageDraw.Draw(im)
    d.line([0, 0, w, h], fill=(251, 246, 238), width=60); d.line([w, 0, 0, h], fill=(251, 246, 238), width=60); d.line([0, 0, w, h], fill=(200, 55, 47), width=20); d.line([w, 0, 0, h], fill=(200, 55, 47), width=20)
    d.rectangle([w / 2 - 50, 0, w / 2 + 50, h], fill=(251, 246, 238)); d.rectangle([0, h / 2 - 50, w, h / 2 + 50], fill=(251, 246, 238)); d.rectangle([w / 2 - 30, 0, w / 2 + 30, h], fill=(200, 55, 47)); d.rectangle([0, h / 2 - 30, w, h / 2 + 30], fill=(200, 55, 47))
    p = os.path.join(TEX, name); im.save(p); return p
def note(label, name=None, tint=(207, 227, 180)):
    name = name or f"note_{label.strip('$')}.png"
    if exists(name): return os.path.join(TEX, name)
    im = Image.new('RGB', (512, 256), tint); d = ImageDraw.Draw(im); d.rectangle([12, 12, 500, 244], outline=(58, 90, 58), width=8); d.rectangle([32, 32, 480, 224], outline=(58, 90, 58), width=3)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 128)
    except Exception: f = ImageFont.load_default()
    d.text((256, 132), label, font=f, fill=(47, 74, 48), anchor='mm'); p = os.path.join(TEX, name); im.save(p); return p
def sign(text, name=None):
    name = name or f"sign_{text.replace(chr(10), '_').replace(' ', '')}.png"
    if exists(name): return os.path.join(TEX, name)
    w, h = 512, 256; a = np.zeros((h, w, 3), np.float32); gr = fbm(h, w, 5, 21, 3, aspect=(1, 14)); a[:] = _hex('#a8774a') * (.75 + .5 * gr[..., None]); a = strokes(a, 4, 700, alpha=.14, length=(30, 100))
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im); d.rectangle([6, 6, w - 6, h - 6], outline=(70, 44, 30), width=10)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72 if '\n' in text else 84)
    except Exception: f = ImageFont.load_default()
    d.multiline_text((w / 2, h / 2), text, font=f, fill=(244, 230, 192), anchor='mm', align='center', spacing=10); p = os.path.join(TEX, name); im.save(p); return p
def fabric(kind, c1, c2, name=None, size=256, seed=1):
    name = name or f"fab_{kind}_{c1.strip('#')}_{c2.strip('#')}.png"
    if exists(name): return os.path.join(TEX, name)
    a = np.zeros((size, size, 3), np.float32); a[:] = _hex(c1); H = W = size; r = _rng(seed)
    if kind == 'plaid':
        for i in range(4): a[:, i * 64 + 24:i * 64 + 40] = a[:, i * 64 + 24:i * 64 + 40] * .45 + _hex(c2) * .55; a[i * 64 + 24:i * 64 + 40] = a[i * 64 + 24:i * 64 + 40] * .45 + _hex(c2) * .55
        for i in range(4): a[:, i * 64 + 6:i * 64 + 9] *= .55; a[i * 64 + 6:i * 64 + 9] *= .55
    elif kind == 'stripes':
        for i in range(8): a[:, i * 32:i * 32 + 12] = _hex(c2)
    elif kind == 'tweed':
        n = r.random((H, W)); a = a * (.8 + .4 * n[..., None]); a = np.where((n > .85)[..., None], _hex(c2), a)
    elif kind == 'denim':
        a = a * (.85 + .3 * fbm(H, W, 4, seed, 30, aspect=(1, 1))[..., None])
    elif kind == 'uniform':
        a = a * (.9 + .2 * fbm(H, W, 4, seed, 12)[..., None])
    return _save(np.clip(a, 0, 1), name)
def paint_noise(name='paint.png', seed=2, size=512, tone=.5):
    if exists(name): return os.path.join(TEX, name)
    a = np.ones((size, size, 3), np.float32) * tone; a = strokes(a, seed, 1500, color=None, alpha=.18); n = fbm(size, size, 5, seed, 4); a = a * (.85 + .3 * n[..., None]); return _save(np.clip(a, 0, 1), name)
