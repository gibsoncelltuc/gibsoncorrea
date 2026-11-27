# "MAP MATES" (autoral): bolinhas-pais com bandeira, olhos e sobrancelhas, chapeus e rifles, num mapa chato colorido.
# Historia contada por cenas curtas (texto grande + baloes com emoji + efeitos sonoros). uso: python3 bolas.py <roteiro.json>
import json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
R = json.load(open(sys.argv[1])); RID = R['id']; OUT = f'out/{RID}'; os.makedirs(f'{OUT}/frames', exist_ok=True)
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
GJ = json.load(open('dados/paises.geojson'))['features']
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
def emoji(ch, tam):
    im = Image.new('RGBA', (170, 170)); ImageDraw.Draw(im).text((85, 85), ch.replace('️', ''), font=EMO, embedded_color=True, anchor='mm'); im = im.crop(im.getbbox())
    return im.resize((tam, max(1, int(tam * im.height / im.width))), Image.LANCZOS)
def fnt(n): return ImageFont.truetype(FB, n)
ease = lambda x: x * x * (3 - 2 * x)

# ---------- mapa chato (equiretangular) pre-desenhado em alta ----------
L0, L1, A0, A1 = R['mapa']   # lon0, lon1, lat0, lat1
MW = 2400; MH = int(MW * (A1 - A0) / (L1 - L0) / math.cos(math.radians((A0 + A1) / 2)) * 1.0)
def xy(lon, lat): return ((lon - L0) / (L1 - L0) * MW, (A1 - lat) / (A1 - A0) * MH)
mapa = Image.new('RGB', (MW, MH), (178, 214, 236)); dm = ImageDraw.Draw(mapa)
cores = R.get('cores', {})
for f in GJ:
    code = f['properties']['ADM0_A3']; g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    cor = tuple(cores.get(code, (222, 222, 222)))
    for p in polys:
        pts = [xy(x, y) for x, y in p[0]]
        if max(x for x, _ in pts) < -50 or min(x for x, _ in pts) > MW + 50: continue
        dm.polygon(pts, fill=cor, outline=(90, 90, 90))
for z in R.get('zonas', []):   # territorio disputado destacado
    x, y = xy(*z['ll']); r = z.get('r', 40); dm.ellipse([x - r, y - r * .7, x + r, y + r * .7], fill=tuple(z['cor']), outline=(0, 0, 0), width=4)

# ---------- personagem (bolinha) ----------
FLAG = {}
def bandeira(c):
    if c not in FLAG: FLAG[c] = Image.open(f'dados/flags/{c}.png').convert('RGBA')
    return FLAG[c]
def bola(img, x, y, r, flag, humor='normal', olhar=(0, 0), chapeu=None, rifle=None, flip=False, t=0.0):
    tam = int(r * 2); b = bandeira(flag).resize((int(tam * 1.33), tam)).crop((int(tam * .165), 0, int(tam * .165) + tam, tam))
    m = Image.new('L', (tam, tam), 0); ImageDraw.Draw(m).ellipse([0, 0, tam - 1, tam - 1], fill=255)
    sh = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, tam - 1, tam - 1], fill=(0, 0, 0, 90)); img.alpha_composite(sh, (int(x - r + 8), int(y - r + 12)))
    img.paste(b, (int(x - r), int(y - r)), m)
    d = ImageDraw.Draw(img); d.ellipse([x - r, y - r, x + r, y + r], outline=(0, 0, 0), width=max(4, int(r * .09)))
    # olhos (brancos, sem boca, pupila olhando) + sobrancelha conforme humor
    s = -1 if flip else 1; ex = r * .36; ey = -r * .1; er = r * .22
    for k in (-1, 1):
        cx, cy = x + k * ex + s * r * .08, y + ey
        if humor == 'feliz': d.arc([cx - er, cy - er, cx + er, cy + er], 200, 340, fill=(0, 0, 0), width=int(r * .08)); continue
        d.ellipse([cx - er, cy - er * 1.15, cx + er, cy + er * 1.15], fill=(255, 255, 255), outline=(0, 0, 0), width=int(r * .05))
        pr = er * .45; px, py = cx + olhar[0] * er * .45 + s * er * .2, cy + olhar[1] * er * .45
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(0, 0, 0))
        if humor in ('bravo', 'mira'): d.line([cx - er * 1.1, cy - er * (1.0 if k * s < 0 else 1.6), cx + er * 1.1, cy - er * (1.6 if k * s < 0 else 1.0)], fill=(0, 0, 0), width=int(r * .09))
        if humor == 'triste': d.line([cx - er * 1.1, cy - er * (1.6 if k * s < 0 else 1.0), cx + er * 1.1, cy - er * (1.0 if k * s < 0 else 1.6)], fill=(0, 0, 0), width=int(r * .07))
        if humor == 'choque': d.ellipse([cx - er * 1.25, cy - er * 1.4, cx + er * 1.25, cy + er * 1.4], outline=(0, 0, 0), width=int(r * .05))
    if humor == 'choque': d.ellipse([x - r * .12, y + r * .38, x + r * .12, y + r * .62], fill=(0, 0, 0))
    if chapeu == 'cartola':   # britanico
        d.rectangle([x - r * .55, y - r * 1.55, x + r * .55, y - r * .85], fill=(20, 20, 20)); d.rectangle([x - r * .55, y - r * 1.0, x + r * .55, y - r * .88], fill=(170, 20, 30)); d.ellipse([x - r * .85, y - r * .98, x + r * .85, y - r * .78], fill=(20, 20, 20))
    if chapeu == 'cowboy':    # americano
        d.ellipse([x - r * .95, y - r * 1.0, x + r * .95, y - r * .75], fill=(120, 80, 40)); d.chord([x - r * .5, y - r * 1.5, x + r * .5, y - r * .6], 180, 360, fill=(140, 95, 50))
    if rifle is not None:     # rifle (angulo em graus, 0 = aponta para o lado do olhar)
        ang = math.radians(rifle); L = r * 2.2; bx, by = x + s * r * .55, y + r * .35
        def P(u, v): return (bx + s * (u * math.cos(ang) - v * math.sin(ang)), by + (u * math.sin(ang) + v * math.cos(ang)))
        d.polygon([P(-L * .35, -r * .06), P(L * .05, -r * .07), P(L * .05, r * .1), P(-L * .35, r * .2)], fill=(110, 70, 35), outline=(0, 0, 0))   # coronha
        d.polygon([P(L * .05, -r * .05), P(L * .75, -r * .04), P(L * .75, r * .03), P(L * .05, r * .05)], fill=(40, 40, 45), outline=(0, 0, 0))     # cano
        return P(L * .78, 0)
    return None

def bang(img, x, y, u):   # clarao + texto BANG
    if u < 0 or u > 1: return
    d = ImageDraw.Draw(img); r = 30 + 90 * u ** .5
    pts = [(x + math.cos(k * math.pi / 6) * (r if k % 2 else r * .5), y + math.sin(k * math.pi / 6) * (r if k % 2 else r * .5)) for k in range(12)]
    d.polygon(pts, fill=(255, 220, 60, int(255 * (1 - u))), outline=(255, 120, 0, int(255 * (1 - u))))
def balao(img, x, y, conteudo, u, lado=1):
    if u <= 0: return
    pop = min(1, u / .15); esc = .6 + .4 * pop + .15 * math.sin(min(1, u / .15) * math.pi)
    d = ImageDraw.Draw(img); w, h = max(260, fnt(64).getlength(conteudo) + 70 if conteudo.isascii() else 0) * esc, 170 * esc; bx, by = x + lado * 40, y - 220 * esc
    d.rounded_rectangle([bx - w / 2, by - h / 2, bx + w / 2, by + h / 2], 40, fill=(255, 255, 255), outline=(0, 0, 0), width=6)
    d.polygon([(bx - lado * 30, by + h / 2 - 4), (bx - lado * 70, by + h / 2 + 50), (bx + lado * 10, by + h / 2 - 4)], fill=(255, 255, 255)); d.line([(bx - lado * 30, by + h / 2), (bx - lado * 70, by + h / 2 + 50), (bx + lado * 10, by + h / 2)], fill=(0, 0, 0), width=6)
    if conteudo.isascii(): f = fnt(int(64 * esc)); d.text((bx, by), conteudo, font=f, fill=(0, 0, 0), anchor='mm')
    else: e = emoji(conteudo, int(110 * esc)); img.alpha_composite(e, (int(bx - e.width / 2), int(by - e.height / 2)))
def texto(img, s, y, n, cor, u=1.0):
    if u <= 0: return
    d = ImageDraw.Draw(img); f = fnt(n)
    while f.getlength(s) > W - 80 and n > 40: n -= 4; f = fnt(n)
    d.text((W / 2, y), s, font=f, fill=cor, anchor='mm', stroke_width=max(6, n // 9), stroke_fill=(0, 0, 0))

# ---------- linha do tempo ----------
CENAS = R['cenas']; t = 0.0
for c in CENAS: c['a'] = t; t += c['dur']; c['b'] = t
TOTAL = t
def ilha():   # cenario desenhado: mar + ilha verde com capim e arvores (cenas de perto)
    im = Image.new('RGBA', (W, H), (120, 190, 235, 255)); d = ImageDraw.Draw(im)
    for k in range(40): y = 80 + k * 47; d.arc([(k * 137) % W - 60, y, (k * 137) % W + 60, y + 30], 200, 340, fill=(170, 215, 245), width=5)
    pts = [(W / 2 + math.cos(a) * W * (.62 + .05 * math.sin(a * 5)), H * .5 + math.sin(a) * H * (.3 + .03 * math.cos(a * 3))) for a in np.linspace(0, 2 * math.pi, 90)]
    d.polygon([(x + 14, y + 18) for x, y in pts], fill=(90, 150, 200)); d.polygon(pts, fill=(118, 190, 90), outline=(40, 80, 30)); d.line(pts + [pts[0]], fill=(40, 80, 30), width=8)
    rng = np.random.default_rng(1)
    for _ in range(70): x, y = rng.uniform(.05, .95) * W, rng.uniform(.25, .72) * H; d.line([x, y, x - 6, y - 16], fill=(80, 150, 60), width=4); d.line([x, y, x + 6, y - 16], fill=(80, 150, 60), width=4)
    for x, y in ((.12, .28), (.88, .3), (.1, .66), (.9, .68)): e = emoji('🌲', 150); im.alpha_composite(e, (int(x * W - 75), int(y * H - 120)))
    return im
ILHA = ilha()
def pos(nome, c, tt):
    a = c['atores'][nome]; p0 = a.get('de', a['em']); p1 = a['em']; u = ease(min(1, max(0, (tt - c['a']) / .45)))
    f = (lambda p: (p[0] * W, p[1] * H)) if c.get('fundo') else (lambda p: xy(*p))
    (x0, y0), (x1, y1) = f(p0), f(p1)
    return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
def quadro(fi):
    tt = fi / FPS; c = next(cc for cc in CENAS if cc['a'] <= tt < cc['b'] or cc is CENAS[-1]); u = tt - c['a']
    # camera: centro + zoom (com leve 'punch' no inicio da cena)
    cx, cy = xy(*c['cam'][:2]); z = c['cam'][2] * (1 + .06 * math.exp(-u * 6))
    vw, vh = W / z, H / z; box = (int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))
    if c.get('fundo'):
        zz = 1 + .06 * math.exp(-u * 6); bw, bh = W / zz, H / zz; img = ILHA.crop((int((W - bw) / 2), int((H - bh) / 2), int((W + bw) / 2), int((H + bh) / 2))).resize((W, H))
        tx = lambda X, Y: (W / 2 + (X - W / 2) * zz, H / 2 + (Y - H / 2) * zz)
    else:
        img = mapa.crop(box).resize((W, H), Image.BILINEAR).convert('RGBA')
        tx = lambda X, Y: ((X - box[0]) * z, (Y - box[1]) * z)
    tremor = sum(max(0, 1 - (u - e['t']) / .3) * 14 for e in c.get('tiros', []) if 0 <= u - e['t'] < .3)
    for nome, a in c.get('atores', {}).items():
        X, Y = pos(nome, c, tt); X, Y = tx(X, Y); bob = 6 * math.sin(tt * 6 + hash(nome) % 7)
        for k in reversed(range(a.get('n', 1))):   # n > 1 = tropa: lider na frente, resto em fileiras atras
            j = k - 1; ox = 0 if k == 0 else ((j % 4) + 1) * a.get("esp", 70) * (1 if a.get("flip") else -1) + (j // 4 % 2) * 35; oy = 0 if k == 0 else (j // 4 - 1) * 75
            mira = bola(img, X + ox + (tremor * math.sin(tt * 80) if a.get('atira') else 0), Y + oy + bob, a.get('r', 110) * (1 if k == 0 or a.get('n', 1) == 1 else .55),
                        a['flag'], a.get('humor', 'normal'), tuple(a.get('olhar', (1, 0))), a.get('chapeu'), a.get('rifle'), a.get('flip', False), tt)
            if a.get('atira') and mira:
                for e in c.get('tiros', []): bang(img, *mira, (u - e['t']) / .35)
        for bl in a.get('baloes', []):
            balao(img, X, Y - a.get('r', 110) * .4, bl['c'], u - bl.get('t', .2), -1 if a.get('flip') else 1)
    for ob in c.get('objetos', []):
        X, Y = tx(ob['ll'][0] * W, ob['ll'][1] * H) if c.get('fundo') else tx(*xy(*ob['ll'])); vis = ob.get('ate', 99) > u >= ob.get('de', 0)
        if vis:
            e = emoji(ob['e'], ob.get('tam', 150)); rot = ob.get('rot', 0) if u > ob.get('rot_t', 99) else 0
            e = e.rotate(rot, expand=True); img.alpha_composite(e, (int(X - e.width / 2), int(Y - e.height / 2 + 4 * math.sin(tt * 8))))
    # textos: ano grande + legenda da cena
    if c.get('ano'): texto(img, c['ano'], 230, 150, (255, 255, 255))
    if c.get('txt'): texto(img, c['txt'], H * .78, 76, (255, 214, 0) if c.get('destaque') else (255, 255, 255), u)
    if c.get('sub'): texto(img, c['sub'], H * .78 + 95, 56, (255, 255, 255), u - .3)
    if c.get('titulo'): texto(img, c['titulo'][0], 300, 120, (255, 214, 0)); texto(img, c['titulo'][1], 430, 120, (255, 255, 255))
    fad = min(1, tt / .2, (TOTAL - tt) / .3)
    rgb = img.convert('RGB')
    return Image.eval(rgb, lambda v: int(v * fad)) if fad < 1 else rgb

# ---------- som ----------
def som():
    SR = 48000; n = int(TOTAL * SR); tt = np.arange(n) / SR; rng = np.random.default_rng(3); out = np.zeros(n)
    bpm = 132; beat = 60 / bpm   # musica leve: baixo saltitante + caixa + assobio de flauta (cartoon)
    notas = [55, 55, 65.4, 73.4, 82.4, 73.4, 65.4, 61.7]
    for i in range(int(TOTAL / (beat / 2))):
        a = int(i * beat / 2 * SR); L = int(beat / 2 * .9 * SR); f = notas[i % 8] * 2; x = np.arange(L) / SR
        out[a:a + L] += .12 * np.sign(np.sin(2 * np.pi * f * x)) * np.exp(-x * 9)[:max(0, min(L, n - a))] if a + L <= n else 0
        if i % 4 == 2: k = rng.standard_normal(int(.1 * SR)) * np.exp(-np.arange(int(.1 * SR)) / SR * 40) * .15; out[a:a + len(k)] += k[:max(0, n - a)]
    for c in CENAS:
        a0 = c['a']
        for e in c.get('tiros', []):   # tiro de rifle: estalo + eco
            a = int((a0 + e['t']) * SR); L = int(1.2 * SR); x = np.arange(L) / SR
            s = rng.standard_normal(L) * (np.exp(-x * 30) * 1.2 + np.exp(-x * 4) * .25); s += np.sin(2 * np.pi * 70 * x) * np.exp(-x * 12) * .8
            out[a:a + L] += s[:max(0, n - a)] * .6
        for e in c.get('sons', []):
            a = int((a0 + e['t']) * SR); x = np.arange(int(.5 * SR)) / SR
            if e['s'] == 'boing': s = np.sin(2 * np.pi * (300 + 200 * np.sin(x * 40) * np.exp(-x * 6)) * x) * np.exp(-x * 5) * .35
            elif e['s'] == 'oink': s = np.sign(np.sin(2 * np.pi * (180 + 60 * np.sin(x * 30)) * x)) * np.exp(-x * 7) * .25
            elif e['s'] == 'tambor': x = np.arange(int(2 * SR)) / SR; s = rng.standard_normal(len(x)) * (.5 + .5 * np.sin(2 * np.pi * 18 * x) ** 2) * np.minimum(1, x * 2) * .12
            else: s = np.sin(2 * np.pi * 880 * x) * np.exp(-x * 8) * .3   # ding
            out[a:a + len(s)] += s[:max(0, n - a)]
    out *= np.minimum(1, np.minimum(tt / .3, (TOTAL - tt) / .5)); out = out / (np.abs(out).max() + 1e-9) * .85
    w = wave.open(f'{OUT}/audio.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()

if __name__ == '__main__':
    N = int(TOTAL * FPS); so = [float(x) for x in sys.argv[2:]]
    if so:
        for x in so: quadro(int(x * FPS)).save(f'{OUT}/q{int(x * FPS):05d}.jpg', quality=90)
        sys.exit()
    import multiprocessing as mp
    def job(i): quadro(i).save(f'{OUT}/frames/f{i:05d}.jpg', quality=92)
    with mp.get_context('fork').Pool(4) as pool: pool.map(job, range(N), chunksize=20)
    som()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{OUT}/frames/f%05d.jpg', '-i', f'{OUT}/audio.wav', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', f'{OUT}/{RID}.mp4'], check=True)
    print('pronto', f'{OUT}/{RID}.mp4', round(TOTAL, 1))
