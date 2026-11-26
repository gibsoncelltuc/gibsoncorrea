# Shorts de GUERRA no globo (estilo Age of Empires / Total War): satelite + paises com bandeira + FROTAS que navegam com rastro,
# ESQUADRILHAS de avioes, SETAS de avanco, EXPLOSOES com fogo/fumaca/tremor, navios afundando, placar "USA vs X" e contador.
# uso: python3 voz.py <id>  ->  python3 guerra.py <id> [t1 t2 ...]   (roteiro em guerras/<id>.json)
import json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
RID = sys.argv[1]; R = json.load(open(f'guerras/{RID}.json')); OUT = f'out/{RID}'
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'; FX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
dur = lambda p: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
GJ = json.load(open('dados/paises.geojson'))['features']; PA = {f['properties']['ADM0_A3']: f for f in GJ}
ISO2 = {k: v['properties']['ISO_A2_EH'].lower() for k, v in PA.items()}
def aneis(code):
    g = PA[code]['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    return [np.array(p[0], dtype=np.float64) for p in polys]
PAL = json.load(open(f'{OUT}/voz/palavras.json')); NS = len(PAL); GAP = .35; t = .25; SEG = []
for k in range(NS): d = dur(f'{OUT}/voz/s{k:02d}.mp3'); SEG.append((t, t + d + GAP, d)); t += d + GAP
TOTAL = t + .6
ITENS = [{'view': R.get('hook_view', [25, 140, 14000])}] + R['items']   # bloco 0 = gancho (globo)
def gt(k, f): a, b, d = SEG[k]; return a + f * (b - a)   # tempo global de uma fracao do bloco

# ---------- camera: cada bloco tem uma vista; transicao suave de 0,8 s ----------
def unit(lat, lon): la, lo = math.radians(lat), math.radians(lon); return np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
def latlon(v): v = v / np.linalg.norm(v); return math.degrees(math.asin(max(-1, min(1, v[2])))), math.degrees(math.atan2(v[1], v[0]))
def slerp(a, b, e):
    om = math.acos(max(-1, min(1, float(a @ b))))
    return a if om < 1e-6 else (math.sin((1 - e) * om) * a + math.sin(e * om) * b) / math.sin(om)
ease = lambda x: x * x * (3 - 2 * x)
def vista(k): la, lo, km = ITENS[k]['view']; return la, lo, W / (km / 6371)
TR = .8
def camera(tt):
    k = max(i for i in range(NS) if SEG[i][0] - .3 <= tt or i == 0)
    la1, lo1, s1 = vista(k)
    if k == 0: return la1, lo1 + 6 * tt, s1 * (1 + .04 * tt)
    u = (tt - (SEG[k][0] - .3)) / TR
    la0, lo0, s0 = vista(k - 1)
    if k - 1 == 0: lo0 += 6 * (SEG[k][0] - .3); s0 *= 1 + .04 * (SEG[k][0] - .3)
    drift = 1 + .025 * max(0, tt - SEG[k][0])
    if u >= 1: return la1, lo1, s1 * drift
    e = ease(max(0, u)); lat, lon = latlon(slerp(unit(la0, lo0), unit(la1, lo1), e)); s = math.exp(math.log(s0) + (math.log(s1) - math.log(s0)) * e)
    return lat, lon, s

# ---------- globo de satelite (o mesmo motor dos shorts de geografia) ----------
TEX = None
def carregar():
    global TEX
    t21 = cv2.imread('dados/earth21k.jpg'); t8 = cv2.imread('dados/earth8k.jpg'); t2 = cv2.resize(t8, (2048, 1024), interpolation=cv2.INTER_AREA)
    TEX = [(t2, 2048 / (2 * math.pi)), (t8, 8192 / (2 * math.pi)), (t21, 21600 / (2 * math.pi))]
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32); CX, CY = W / 2, H * .5
rng = np.random.default_rng(3); ESTRELAS = np.zeros((H, W, 3), np.uint8)
for _ in range(900):
    x, y = rng.integers(0, W), rng.integers(0, H); b = int(rng.integers(60, 230)); ESTRELAS[y, x] = (b, b, b)
ESTRELAS = cv2.GaussianBlur(ESTRELAS, (3, 3), 0) * 2
def terra(lat0, lon0, s, dx=0, dy=0):
    X = (XX - CX - dx) / s; Y = -(YY - CY - dy) / s; rho = np.sqrt(X * X + Y * Y); den = np.maximum(rho, 1e-9)
    dentro = rho < 1; c = np.arcsin(np.clip(rho, 0, 1)); sc, cc = np.sin(c), np.cos(c); f0 = math.radians(lat0); l0 = math.radians(lon0)
    lat = np.arcsin(np.clip(cc * math.sin(f0) + Y * sc * math.cos(f0) / den, -1, 1)); lon = l0 + np.arctan2(X * sc, rho * cc * math.cos(f0) - Y * sc * math.sin(f0))
    tex, tpr = TEX[-1]
    for tx, p in TEX:
        if p >= s * .9: tex, tpr = tx, p; break
    th, tw = tex.shape[:2]; mx = ((np.degrees(lon) + 180) % 360) / 360 * tw; my = (90 - np.degrees(lat)) / 180 * th
    img = cv2.remap(tex, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    if s < 3000: luz = np.clip(.45 + .55 * np.nan_to_num(cc) ** .6, 0, 1)[..., None]; img = (img * luz).astype(np.uint8)
    out = np.where(dentro[..., None], img, ESTRELAS)
    with np.errstate(over='ignore'): atm = np.clip(np.exp(-(rho - 1) * s / 22), 0, 1) * (rho >= .985)
    out = (out * (1 - atm[..., None] * .8) + np.array([255, 170, 90], np.float32) * atm[..., None] * .8).astype(np.uint8)
    # leve tom de "mapa de jogo": contraste e saturacao
    out = cv2.convertScaleAbs(out, alpha=1.12 if s < 3000 else 1.35, beta=-8 if s < 3000 else 12)
    if s >= 3000:   # oceano mais vivo (mapa de jogo)
        hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.int16); hsv[..., 1] = np.clip(hsv[..., 1] * 1.25, 0, 255); hsv[..., 2] = np.clip(hsv[..., 2] + 18, 0, 255); out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    return out
def proj(lat, lon, lat0, lon0, s, dx=0, dy=0):
    f, l = math.radians(lat), math.radians(lon); f0, l0 = math.radians(lat0), math.radians(lon0)
    cosc = math.sin(f0) * math.sin(f) + math.cos(f0) * math.cos(f) * math.cos(l - l0)
    x = CX + dx + s * math.cos(f) * math.sin(l - l0); y = CY + dy - s * (math.cos(f0) * math.sin(f) - math.sin(f0) * math.cos(f) * math.cos(l - l0))
    return x, y, cosc
def projv(lon, lat, lat0, lon0, s, dx=0, dy=0):
    f, l = np.radians(lat), np.radians(lon); f0, l0 = math.radians(lat0), math.radians(lon0)
    cosc = math.sin(f0) * np.sin(f) + math.cos(f0) * np.cos(f) * np.cos(l - l0)
    return np.stack([CX + dx + s * np.cos(f) * np.sin(l - l0), CY + dy - s * (math.cos(f0) * np.sin(f) - math.sin(f0) * np.cos(f) * np.cos(l - l0))], 1), cosc
FLAGBGR = {}
def flag_bgr(iso):
    if iso not in FLAGBGR:
        p = f'dados/flags/{iso}.png'; FLAGBGR[iso] = cv2.cvtColor(np.array(Image.open(p).convert('RGB')), cv2.COLOR_RGB2BGR) if os.path.exists(p) else None
    return FLAGBGR[iso]
def pintar(img, codes, a, lat0, lon0, s, dx, dy, forca=.85):
    if a <= 0: return img
    out = img.copy(); linhas = []
    for code in codes:
        polys = []
        for r in aneis(code):
            p, cc = projv(r[:, 0], r[:, 1], lat0, lon0, s, dx, dy)
            if (cc < .05).any() or np.abs(p).max() > 60000: continue
            polys.append(np.round(p * 4).astype(np.int32))
        if not polys: continue
        linhas += polys; mask = np.zeros(img.shape[:2], np.uint8)
        for pts in polys: cv2.fillPoly(mask, [pts], 255, cv2.LINE_AA, 2)
        big = max(polys, key=lambda q: cv2.contourArea(q.astype(np.float32) / 4)); x, y, w, h = cv2.boundingRect((big / 4).astype(np.int32))
        fb = flag_bgr(ISO2.get(code, '')); camada = np.full_like(img, 128)
        if fb is not None and w > 2 and h > 2:
            fr = cv2.resize(fb, (w, h), interpolation=cv2.INTER_AREA); x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
            if x1 > x0 and y1 > y0: camada[y0:y1, x0:x1] = fr[y0 - y:y1 - y, x0 - x:x1 - x]
            fora = np.ones(img.shape[:2], bool); fora[y0:y1, x0:x1] = False; camada[fora] = fb.reshape(-1, 3).mean(0)
        m = (mask.astype(np.float32) / 255 * forca * a)[..., None]; out = (out * (1 - m) + camada * m).astype(np.uint8)
    brilho = np.zeros_like(out)
    for pts in linhas: cv2.polylines(brilho, [pts], True, (255, 255, 255), 10, cv2.LINE_AA, 2)
    out = cv2.add(out, (cv2.GaussianBlur(brilho, (0, 0), 7) * (.7 * a)).astype(np.uint8))
    for pts in linhas: cv2.polylines(out, [pts], True, (255, 255, 255), 3, cv2.LINE_AA, 2)
    return out

# ---------- linha do tempo das UNIDADES (frotas e esquadrilhas) ----------
def gcpt(a, b, e):   # ponto no grande circulo
    return latlon(slerp(unit(*a), unit(*b), e))
FROTAS = {}   # id -> lista de movimentos [(t0, t1, from, to)], lado, n
AFUND = {}    # (id, i) -> tempo do impacto
EVENTOS = []  # (tipo, t, dados)
for k, it in enumerate(ITENS):
    for ac in it.get('acts', []):
        if ac['type'] == 'fleet':
            F = FROTAS.setdefault(ac['id'], {'side': ac['side'], 'n': ac['n'], 'mov': [], 'kind': ac.get('kind', 'porta_avioes')}); F['mov'].append((gt(k, ac['f0']), gt(k, ac['f1']), ac['from'], ac['to']))
        elif ac['type'] == 'planes': EVENTOS.append(('planes', gt(k, ac['f0']), dict(ac, t1=gt(k, ac['f1']))))
        elif ac['type'] == 'arrow': EVENTOS.append(('arrow', gt(k, ac['f0']), dict(ac, t1=gt(k, ac['f1']), tfim=SEG[k][1])))
        elif ac['type'] == 'boom':
            EVENTOS.append(('boom', gt(k, ac['f']), ac))
            if 'ship' in ac: AFUND[tuple(ac['ship'])] = gt(k, ac['f'])
        elif ac['type'] == 'hud': EVENTOS.append(('hud', gt(k, ac['f']), ac))
def frota_pos(F, tt):
    pos = None; head = None
    for (t0, t1, a, b) in F['mov']:
        if tt < t0: break
        e = ease(min(1, (tt - t0) / max(.01, t1 - t0))); pos = gcpt(a, b, e); head = (a, b, e)
    return pos, head
def navios(F, tt):   # posicoes (lat, lon) de cada navio em formacao + rumo
    pos, head = frota_pos(F, tt)
    if pos is None: return []
    a, b, e = head; p2 = gcpt(a, b, min(1, e + .02)); ang = math.atan2(-(p2[0] - pos[0]), (p2[1] - pos[1]) * math.cos(math.radians(pos[0])) + 1e-9)
    return [(pos[0], pos[1], ang, i) for i in range(F['n'])]   # mesmo centro; a formacao e' aplicada na tela (FORM)
FORM = [(.62, -.5), (.62, .5), (-.62, -.5), (-.62, .5), (0, -1.0), (0, 1.0)]   # (ao longo do rumo, de lado) em comprimentos de navio
def forma(x, y, ang, i, esc):
    L = 230 * esc * .62 * .76; a, b = FORM[i % len(FORM)]; a *= L * 1.15; b *= L * .7
    return x + a * math.cos(ang) - b * math.sin(ang), y + a * math.sin(ang) + b * math.cos(ang)

# ---------- desenho dos tokens (estilo jogo de estrategia) ----------
def cor_lado(sd): return tuple(R['sides'][sd]['cor'])
def poli(d, pts, x, y, ang, esc, fill, outline=None, w=3):
    ca, sa = math.cos(ang), math.sin(ang); P = [(x + (px * ca - py * sa) * esc, y + (px * sa + py * ca) * esc) for px, py in pts]
    d.polygon(P, fill=fill, outline=outline, width=w)
CASCO = [(-36, -11), (30, -11), (42, 0), (30, 11), (-36, 11)]; CONVES = [(-32, -7), (28, -7), (35, 0), (28, 7), (-32, 7)]; ILHA = [(4, -10), (16, -10), (16, -5), (4, -5)]
AVIAO = [(18, 0), (4, -3), (0, -16), (-5, -16), (-3, -3), (-14, -2), (-17, -8), (-20, -8), (-18, 0), (-20, 8), (-17, 8), (-14, 2), (-3, 3), (-5, 16), (0, 16), (4, 3)]
SPR = {}
def sprite(nome, k, tam, escuro=0.0):
    chave = (nome, k, tam, round(escuro, 1))
    if chave not in SPR:
        im = Image.open(f'dados/sprites/{nome}_{k:02d}.png').convert('RGBA'); im = im.resize((tam, tam), Image.LANCZOS)
        if escuro > 0:
            r, g, b, a = im.split(); f = 1 - .6 * escuro; im = Image.merge('RGBA', (r.point(lambda v: int(v * f)), g.point(lambda v: int(v * f * .9)), b.point(lambda v: int(v * f * .8)), a))
        SPR[chave] = im
    return SPR[chave]
def rumo(ang): return int(round(ang / (math.pi / 8))) % 16
def blit(cam, im, x, y, sombra=True):
    if sombra:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').point(lambda v: int(v * .45))); cam.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (int(x - im.width / 2 + 10), int(y - im.height / 2 + 14)))
    cam.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
def navio3d(cam, x, y, ang, kind, esc, dano):
    tam = int(230 * esc * .62 * (1 - .2 * dano)); blit(cam, sprite(kind, rumo(ang), max(20, tam), min(1, dano)), x, y)
def aviao3d(cam, x, y, ang, flag, esc):
    nome = f'aviao_{flag}' if os.path.exists(f'dados/sprites/aviao_{flag}_00.png') else 'aviao_us'; blit(cam, sprite(nome, rumo(ang), int(105 * esc / 2.4)), x, y)
def desenha_navio(d, x, y, ang, sd, esc=1.0, dano=0.0):
    poli(d, [(px + 2, py + 3) for px, py in CASCO], x, y, ang, esc, (0, 0, 0, 90))
    poli(d, CASCO, x, y, ang, esc, (70, 74, 80, 255), cor_lado(sd) + (255,), 3)
    poli(d, CONVES, x, y, ang, esc, (120, 105, 80, 255) if dano < .5 else (60, 40, 30, 255))
    poli(d, ILHA, x, y, ang, esc, (200, 200, 205, 255))
def desenha_aviao(d, x, y, ang, sd, esc=1.0):
    poli(d, [(px + 3, py + 5) for px, py in AVIAO], x, y, ang, esc, (0, 0, 0, 80))
    poli(d, AVIAO, x, y, ang, esc, (225, 228, 232, 255), cor_lado(sd) + (255,), 2)
def explosao(d, x, y, u, esc=1.0):   # u: 0..1 (1,4 s)
    if u < 0 or u > 1: return
    r = (30 + 140 * u ** .5) * esc
    if u < .15: d.ellipse([x - r * 1.3, y - r * 1.3, x + r * 1.3, y + r * 1.3], fill=(255, 255, 230, int(230 * (1 - u / .15))))
    for i in range(9):
        a = i * .7 + 1.3; rr = r * (.35 + .25 * ((i * 37) % 5) / 5); cx, cy = x + math.cos(a) * r * .45, y + math.sin(a) * r * .45 - u * 60 * esc
        al = int(255 * max(0, 1 - u * 1.2)); d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 140 + (i % 3) * 30, 30, al))
    for i in range(6):   # fumaca subindo
        rr = r * (.4 + .1 * i) * u; cy = y - u * (90 + 30 * i) * esc; d.ellipse([x - rr + i * 8, cy - rr, x + rr + i * 8, cy + rr], fill=(40, 40, 40, int(180 * u * (1 - u))))
def seta(d, pts, cor, prog, larg=26):
    if prog <= 0 or len(pts) < 2: return
    n = max(2, int(len(pts) * prog)); P = pts[:n]
    d.line(P, fill=(0, 0, 0, 120), width=larg + 10, joint='curve'); d.line(P, fill=cor + (235,), width=larg, joint='curve')
    (x1, y1), (x0, y0) = P[-1], P[-2]; ang = math.atan2(y1 - y0, x1 - x0)
    poli(d, [(26, 0), (-14, -28), (-6, 0), (-14, 28)], x1, y1, ang, 1.3, cor + (255,), (0, 0, 0, 255), 4)

def fonte(p, n): return ImageFont.truetype(p, n)
def tx(d, xy, s, f, cor=(255, 255, 255), b=10, anchor='mm'): d.text(xy, s, font=f, fill=cor, anchor=anchor, stroke_width=b, stroke_fill=(0, 0, 0))
FLAGPIL = {}
def bandeira(c, w):
    if c not in FLAGPIL: FLAGPIL[c] = Image.open(f'dados/flags/{c}.png').convert('RGBA')
    return FLAGPIL[c].resize((w, int(w * .75)), Image.LANCZOS)
EMOJI = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
def emoji(ch, tam):
    im = Image.new('RGBA', (160, 160)); ImageDraw.Draw(im).text((80, 80), ch.replace('️', ''), font=EMOJI, embedded_color=True, anchor='mm'); im = im.crop(im.getbbox())
    return im.resize((tam, int(tam * im.height / im.width)), Image.LANCZOS)
def quebrar(txt, f, maxw):
    ls = ['']
    for w in txt.split():
        if f.getlength((ls[-1] + ' ' + w).strip()) > maxw: ls.append(w)
        else: ls[-1] = (ls[-1] + ' ' + w).strip()
    return ls
def legenda(tt):
    for k in range(NS):
        a, b, d = SEG[k]
        if a <= tt < b:
            pw = PAL[k]
            if tt > a + pw[-1][1] + .2: return None
            i = max([j for j, w in enumerate(pw) if a + w[0] <= tt] or [0]); return pw[i][2]
    return None

def quadro(fi):
    tt = fi / FPS; lat0, lon0, s = camera(tt); k = max(i for i in range(NS) if SEG[i][0] - .3 <= tt or i == 0); it = ITENS[k]
    # tremor de tela nas explosoes
    dx = dy = 0
    for (tp, t0, ac) in EVENTOS:
        if tp == 'boom' and 0 <= tt - t0 < .5: q = (1 - (tt - t0) / .5) * 14; dx += q * math.sin(tt * 90); dy += q * math.cos(tt * 77)
    img = terra(lat0, lon0, s, dx, dy)
    ap = min(1, max(0, (tt - SEG[k][0] + .1) / .4))
    if it.get('hl'): img = pintar(img, it['hl'], ap, lat0, lon0, s, dx, dy)
    if it.get('final'): img = pintar(img, ['USA'], ap, lat0, lon0, s, dx, dy)
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA'); cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    P = lambda ll: proj(ll[0], ll[1], lat0, lon0, s, dx, dy)
    # setas de avanco
    for (tp, t0, ac) in EVENTOS:
        if tp == 'arrow' and t0 <= tt <= ac['tfim'] + .3:
            pts = [];
            for j in range(40): la, lo = gcpt(ac['from'], ac['to'], j / 39); x, y, c = P((la, lo)); pts.append((x, y))
            al = 1 if tt < ac['tfim'] else max(0, 1 - (tt - ac['tfim']) / .3)
            seta(d, pts, cor_lado(ac['side']), min(1, (tt - t0) / max(.1, ac['t1'] - t0)))
    # pinos
    for pn in it.get('pins', []):
        x, y, c = P(pn['ll'])
        if c > 0:
            for rr in range(3):
                raio = 14 + ((tt * 40 + rr * 25) % 70); a2 = int(255 * (1 - (raio - 14) / 70)); d.ellipse([x - raio, y - raio, x + raio, y + raio], outline=(255, 255, 255, a2), width=4)
            d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=(240, 200, 40, 255), outline=(0, 0, 0, 255), width=4)
            f = fonte(FX, 40); w = f.getlength(pn['label']); d.rounded_rectangle([x - w / 2 - 20, y + 30, x + w / 2 + 20, y + 92], 12, fill=(255, 255, 255, 240), outline=(0, 0, 0, 255), width=3); d.text((x, y + 61), pn['label'], font=f, fill=(20, 20, 20), anchor='mm')
    # frotas (com rastro) e navios em chamas / afundando
    esc_nav = max(1.6, min(2.6, s / 3000))
    for fid, F in FROTAS.items():
        for (la, lo, ang, i) in navios(F, tt):
            ti = AFUND.get((fid, i)); dano = 0 if ti is None or tt < ti else min(1, (tt - ti) / 3)
            x, y, c = P((la, lo)); x, y = forma(x, y, ang, i, esc_nav)
            if c <= 0: continue
            pos, head = frota_pos(F, tt)
            if head and head[2] < 1:   # rastro de espuma
                for j in range(1, 9): r9 = max(1.5, 6 - j * .5); wx, wy = x - math.cos(ang) * j * 9 * esc_nav, y - math.sin(ang) * j * 9 * esc_nav; d.ellipse([wx - r9, wy - r9 * .8, wx + r9, wy + r9 * .8], fill=(255, 255, 255, 150 - j * 15))
            if dano > 0:
                for j in range(5): rr = (12 + j * 9) * esc_nav; cy = y - j * 26 * esc_nav - (tt * 30 % 20); d.ellipse([x - rr + j * 6, cy - rr, x + rr + j * 6, cy + rr], fill=(35, 35, 35, 170 - j * 25))
            navio3d(cam, x, y, ang, F.get('kind', 'porta_avioes'), esc_nav, dano)
            if dano > 0: d.ellipse([x - 16 * esc_nav, y - 16 * esc_nav, x + 16 * esc_nav, y + 16 * esc_nav], fill=(255, 120 + int(60 * math.sin(tt * 20)), 20, 220))
        pos, _ = frota_pos(F, tt)
        if pos:   # bandeirinha da frota
            x, y, c = P(pos)
            if c > 0: b = bandeira(R['sides'][F['side']]['flag'], 64); bx, by = int(x - 32), int(y - 120 * max(.7, esc_nav)); d.rectangle([bx - 4, by - 4, bx + 68, by + 52], fill=(255, 255, 255, 255)); cam.alpha_composite(b, (bx, by)); d.line([(x, by + 52), (x, y - 20)], fill=(255, 255, 255, 255), width=3)
    # esquadrilhas
    for (tp, t0, ac) in EVENTOS:
        if tp == 'planes' and t0 <= tt <= ac['t1']:
            e = (tt - t0) / max(.1, ac['t1'] - t0)
            for j in range(ac['n']):
                ej = max(0, min(1, e - (j // 3) * .09 - (j % 3 == 1) * .03)); la, lo = gcpt(ac['from'], ac['to'], ej); la2, lo2 = gcpt(ac['from'], ac['to'], min(1, ej + .02))
                x, y, c = P((la, lo)); x2, y2, _ = P((la2, lo2)); ang = math.atan2(y2 - y, x2 - x); off = ((j % 3) - 1) * 115; x += -math.sin(ang) * off; y += math.cos(ang) * off
                for q in range(1, 7): d.ellipse([x - math.cos(ang) * q * 12 - 3, y - math.sin(ang) * q * 12 - 3, x - math.cos(ang) * q * 12 + 3, y - math.sin(ang) * q * 12 + 3], fill=(255, 255, 255, 120 - q * 15))
                aviao3d(cam, x, y, ang, R['sides'][ac['side']]['flag'], 2.4)
    # explosoes
    for (tp, t0, ac) in EVENTOS:
        if tp == 'boom' and 0 <= tt - t0 <= 1.4:
            if 'ship' in ac:
                F = FROTAS[ac['ship'][0]]; nv = [q for q in navios(F, tt) if q[3] == ac['ship'][1]]
                if nv: x, y, c = P(nv[0][:2]); x, y = forma(x, y, nv[0][2], ac['ship'][1], esc_nav); explosao(d, x, y, (tt - t0) / 1.4, 1.1)
            else:
                for j in range(ac.get('n', 1)): x, y, c = P(ac['at']); explosao(d, x + (j - 1) * 50, y + (j % 2) * 30, (tt - t0 - j * .2) / 1.4, .9)
    pil.alpha_composite(cam); d = ImageDraw.Draw(pil)
    # icone do fato
    if it.get('icon') and tt > SEG[k][0] + .2:
        e2 = emoji(it['icon'], 230); pil.alpha_composite(e2, (W // 2 - e2.width // 2 + 220, int(H * .3)))
    # placar USA vs X (estilo jogo)
    if k > 0:
        a, b = R['sides']; f = fonte(FB, 46); y0 = 70
        d.rounded_rectangle([40, y0 - 10, W - 40, y0 + 120], 24, fill=(10, 12, 18, 200), outline=(255, 214, 0, 255), width=4)
        pil.alpha_composite(bandeira(a['flag'], 96), (66, y0 + 18)); pil.alpha_composite(bandeira(b['flag'], 96), (W - 162, y0 + 18))
        tx(d, (190, y0 + 55), a['name'], f, (255, 255, 255), 6, 'lm'); tx(d, (W - 190, y0 + 55), b['name'], f, (255, 255, 255), 6, 'rm'); tx(d, (W / 2, y0 + 40), 'VS', fonte(FB, 52), (255, 214, 0), 6)
        tx(d, (W / 2, y0 + 92), R['year'], fonte(FX, 30), (200, 210, 220), 5)
        val = 0
        for (tp, t0, ac) in EVENTOS:
            if tp == 'hud' and tt >= t0: val = ac['value']; th = t0
        if val:
            pop = min(1, (tt - th) / .25); esc2 = 1 + .35 * (1 - pop); f2 = fonte(FB, int(44 * esc2)); txt = f"{R['hud']['label']}: {val}/{R['hud']['total']}"
            w = f2.getlength(txt); d.rounded_rectangle([W / 2 - w / 2 - 26, 230, W / 2 + w / 2 + 26, 300], 16, fill=(160, 20, 20, 235), outline=(0, 0, 0, 255), width=4); tx(d, (W / 2, 265), txt, f2, (255, 255, 255), 5)
    else:   # gancho: titulo grande
        f = fonte(FB, 90); ls = quebrar(R['title'], f, W - 100)
        while max(f.getlength(l) for l in ls) > W - 70: f = fonte(FB, f.size - 6); ls = quebrar(R['title'], f, W - 100)
        y = 150
        for i2, l in enumerate(ls): tx(d, (W / 2, y), l, f, (255, 214, 0) if i2 % 2 == 0 else (255, 255, 255), 12); y += f.size * 1.12
    if it.get('final') and tt > SEG[k][0] + .3:   # placar final
        f = fonte(FB, 70); d.rounded_rectangle([90, H * .58, W - 90, H * .58 + 250], 26, fill=(10, 12, 18, 225), outline=(255, 214, 0, 255), width=5)
        for i3, (txt3, sd3) in enumerate(R.get('placar', [])): tx(d, (W / 2, H * .58 + 70 + i3 * 105), txt3, f if f.getlength(txt3) < W - 220 else fonte(FB, 54), tuple(min(255, c + 60) for c in cor_lado(sd3)), 8)
    w = legenda(tt)
    if w: f = fonte(FB, 92); f = f if f.getlength(w) < W - 120 else fonte(FB, 70); tx(d, (W / 2, H * .8), w, f, (255, 255, 255), 10)
    img = cv2.cvtColor(np.array(pil.convert('RGB')), cv2.COLOR_RGB2BGR)
    fad = min(1, tt / .25, (TOTAL - tt) / .4)
    return (img * fad).astype(np.uint8) if fad < 1 else img

def trabalho(args):
    for fi in range(*args):
        p = f'{OUT}/frames/f{fi:05d}.jpg'
        if not os.path.exists(p): cv2.imwrite(p, quadro(fi), [cv2.IMWRITE_JPEG_QUALITY, 92])

if __name__ == '__main__':
    carregar(); os.makedirs(f'{OUT}/frames', exist_ok=True); N = int(TOTAL * FPS)
    if len(sys.argv) > 2:
        for x in sys.argv[2:]: cv2.imwrite(f'{OUT}/q{int(float(x) * FPS):05d}.jpg', quadro(int(float(x) * FPS)))
        sys.exit()
    import multiprocessing as mp
    with mp.get_context('fork').Pool(4) as pool: list(pool.imap_unordered(trabalho, [(i, min(N, i + 30)) for i in range(0, N, 30)]))
    import audio_geo; audio_geo.montar(OUT, SEG, TOTAL)
    # explosoes e motores no audio
    SR = 48000; n = int(TOTAL * SR); fx = np.zeros(n); rr = np.random.default_rng(2)
    for (tp, t0, ac) in EVENTOS:
        if tp == 'boom':
            for j in range(ac.get('n', 1)):
                a = int((t0 + j * .2) * SR); L = int(1.6 * SR); tt2 = np.arange(L) / SR; b = rr.standard_normal(L) * np.exp(-tt2 * 3.2); b = np.convolve(b, np.ones(40) / 40, 'same') * 3 + np.sin(2 * np.pi * (45 + 40 * np.exp(-tt2 * 8)) * tt2) * np.exp(-tt2 * 4)
                fx[a:a + L] += b[:max(0, n - a)] * .5
        if tp == 'planes':
            a = int(t0 * SR); L = int((ac['t1'] - t0) * SR); tt2 = np.arange(L) / SR; env = np.sin(np.pi * tt2 / max(.1, tt2[-1])) ; b = rr.standard_normal(L); b = np.convolve(b, np.ones(12) / 12, 'same') * env * (1 + .3 * np.sin(2 * np.pi * 90 * tt2))
            fx[a:a + L] += b[:max(0, n - a)] * .25
    import wave
    w = wave.open(f'{OUT}/fx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(fx, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/audio.wav', '-i', f'{OUT}/fx.wav', '-filter_complex', '[1]volume=0.9[f];[0][f]amix=2:normalize=0,alimiter=limit=0.95[o]', '-map', '[o]', f'{OUT}/audio2.wav'], check=True)
    nome = f'{OUT}/{RID}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{OUT}/frames/f%05d.jpg', '-i', f'{OUT}/audio2.wav', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', nome], check=True)
    print('pronto', nome, round(TOTAL, 1), 's')
