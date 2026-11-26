# Shorts de GEOGRAFIA (estilo nicho EUA): Terra do espaco -> zoom de satelite no pais, destaque, bandeira, legenda palavra a palavra em ingles.
# uso: python3 geo.py <id> [quadro_unico]   (antes: python3 voz.py <id>)
import json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
RID = sys.argv[1]; R = json.load(open(f'roteiros/{RID}.json')); OUT = f'out/{RID}'
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'; FX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
dur = lambda p: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)

# ---------- paises ----------
GJ = json.load(open('dados/paises.geojson'))['features']; PA = {f['properties']['ADM0_A3']: f for f in GJ}
def aneis(code):
    g = PA[code]['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    return [np.array(p[0], dtype=np.float64) for p in polys]

# ---------- tempos (voz) ----------
PAL = json.load(open(f'{OUT}/voz/palavras.json')); NS = len(PAL); GAP = .45; t = .3; SEG = []
for k in range(NS):
    d = dur(f'{OUT}/voz/s{k:02d}.mp3'); SEG.append((t, t + d + GAP, d)); t += d + GAP
TOTAL = t + .4

# ---------- vistas (camera) ----------
def vista(it):
    if 'pin' in it: lat, lon = it['pin']
    else: p = PA[it['hl'][0]]['properties']; lat, lon = p['LABEL_Y'], p['LABEL_X']
    larg = 900.0                                                   # km mostrados na largura
    if it.get('hl') and 'pin' not in it:
        a = max(aneis(it['hl'][0]), key=len); x0, x1 = a[:, 0].min(), a[:, 0].max(); y0, y1 = a[:, 1].min(), a[:, 1].max()
        wk = (x1 - x0) * 111 * math.cos(math.radians((y0 + y1) / 2)); hk = (y1 - y0) * 111
        larg = max(wk * 1.7, hk * 1.7 * W / (H * .55), 700)
    if 'pin' in it and it.get('hl') and len(aneis(it['hl'][0])) and it.get('zoom'): larg = it['zoom']
    larg = min(larg, 9000)
    s = W / (larg / 6371)                                          # px por raio da Terra
    return lat, lon, s
GLOBO_S = W * .42
VISTAS = [(20.0, -40.0, GLOBO_S)] + [vista(i) for i in R['items']]

def unit(lat, lon): la, lo = math.radians(lat), math.radians(lon); return np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
def latlon(v): v = v / np.linalg.norm(v); return math.degrees(math.asin(max(-1, min(1, v[2])))), math.degrees(math.atan2(v[1], v[0]))
def slerp(a, b, e):
    om = math.acos(max(-1, min(1, float(a @ b))))
    if om < 1e-6: return a
    return (math.sin((1 - e) * om) * a + math.sin(e * om) * b) / math.sin(om)
ease = lambda x: x * x * (3 - 2 * x)
VOO = .85; ANT = .5
def camera(tt):
    k = max(i for i in range(NS) if SEG[i][0] - ANT <= tt or i == 0); a = SEG[k][0] - ANT
    if k == 0:   # gancho: globo girando
        return 18.0, -60.0 + 14 * tt, GLOBO_S * (1 + .05 * tt)
    la0, lo0, s0 = VISTAS[k - 1]; la1, lo1, s1 = VISTAS[k]
    if k - 1 == 0: lo0 = -60.0 + 14 * a; s0 = GLOBO_S * (1 + .05 * a)
    else: s0 *= 1 + .05 * (SEG[k - 1][1] - SEG[k - 1][0] - VOO)
    u = (tt - a) / VOO
    if u >= 1:
        return la1, lo1, s1 * (1 + .05 * (tt - a - VOO))   # chegou: leve aproximacao
    e = ease(max(0, u)); A, B = unit(la0, lo0), unit(la1, lo1); dang = math.acos(max(-1, min(1, float(A @ B))))
    lat, lon = latlon(slerp(A, B, e))
    smid = min(s0, s1, W * .45 / max(.05, math.sin(min(dang, 2.6) / 2) + .25))
    l0, l1, lm = math.log(s0), math.log(s1), math.log(smid)
    lm2 = 2 * lm - (l0 + l1) / 2
    ls = (1 - e) ** 2 * l0 + 2 * e * (1 - e) * min(lm2, (l0 + l1) / 2) + e * e * l1
    return lat, lon, math.exp(ls)

# ---------- texturas ----------
TEX = None
def carregar():
    global TEX
    t21 = cv2.imread('dados/earth21k.jpg'); t8 = cv2.imread('dados/earth8k.jpg'); t2 = cv2.resize(t8, (2048, 1024), interpolation=cv2.INTER_AREA)
    TEX = [(t2, 2048 / (2 * math.pi)), (t8, 8192 / (2 * math.pi)), (t21, 21600 / (2 * math.pi))]
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
CX, CY = W / 2, H * .47
rng = np.random.default_rng(3); ESTRELAS = np.zeros((H, W, 3), np.uint8)
for _ in range(900):
    x, y = rng.integers(0, W), rng.integers(0, H); b = int(rng.integers(60, 230)); ESTRELAS[y, x] = (b, b, b)
ESTRELAS = cv2.GaussianBlur(ESTRELAS, (3, 3), 0) * 2

def terra(lat0, lon0, s):
    X = (XX - CX) / s; Y = -(YY - CY) / s; rho = np.sqrt(X * X + Y * Y); den = np.maximum(rho, 1e-9)
    dentro = rho < 1; c = np.arcsin(np.clip(rho, 0, 1)); sc, cc = np.sin(c), np.cos(c)
    f0 = math.radians(lat0); l0 = math.radians(lon0)
    lat = np.arcsin(np.clip(cc * math.sin(f0) + Y * sc * math.cos(f0) / den, -1, 1))
    lon = l0 + np.arctan2(X * sc, rho * cc * math.cos(f0) - Y * sc * math.sin(f0))
    tex, tpr = TEX[-1]
    for tx, p in TEX:
        if p >= s * .9: tex, tpr = tx, p; break
    th, tw = tex.shape[:2]
    mx = ((np.degrees(lon) + 180) % 360) / 360 * tw; my = (90 - np.degrees(lat)) / 180 * th
    img = cv2.remap(tex, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    if s < 3000:   # borda do globo: escurece e atmosfera
        luz = np.clip(.45 + .55 * cc ** .6, 0, 1)[..., None]; img = (img * luz).astype(np.uint8)
    out = np.where(dentro[..., None], img, ESTRELAS)
    atm = np.clip(np.exp(-(rho - 1) * s / 22), 0, 1) * (rho >= .985)
    cor = np.array([255, 170, 90], np.float32)   # BGR azul claro
    out = (out * (1 - atm[..., None] * .8) + cor * atm[..., None] * .8).astype(np.uint8)
    return out

def projetar(lon, lat, lat0, lon0, s):
    f, l = np.radians(lat), np.radians(lon); f0, l0 = math.radians(lat0), math.radians(lon0)
    cosc = math.sin(f0) * np.sin(f) + math.cos(f0) * np.cos(f) * np.cos(l - l0)
    x = CX + s * np.cos(f) * np.sin(l - l0); y = CY - s * (math.cos(f0) * np.sin(f) - math.sin(f0) * np.cos(f) * np.cos(l - l0))
    return np.stack([x, y], 1), cosc

FLAGBGR = {}
def flag_bgr(code):
    iso = ISO2.get(code, '')
    if iso not in FLAGBGR:
        pth = f'dados/flags/{iso}.png'
        FLAGBGR[iso] = cv2.cvtColor(np.array(Image.open(pth).convert('RGB')), cv2.COLOR_RGB2BGR) if os.path.exists(pth) else None
    return FLAGBGR[iso]
def desenhar_paises(img, codes, cor, a, lat0, lon0, s, forca=.9):
    # pinta o pais com a PROPRIA BANDEIRA (como nos videos virais), contorno branco com brilho
    if a <= 0 or not codes: return img
    out = img.copy(); linhas = []
    for code in codes:
        polys = []
        for r in aneis(code):
            p, cc = projetar(r[:, 0], r[:, 1], lat0, lon0, s)
            if (cc < .05).any() or np.abs(p).max() > 60000: continue
            polys.append(np.round(p * 4).astype(np.int32))
        if not polys: continue
        linhas += polys
        mask = np.zeros(img.shape[:2], np.uint8)
        for pts in polys: cv2.fillPoly(mask, [pts], 255, cv2.LINE_AA, 2)
        # a bandeira cobre o maior pedaco do pais (bbox do maior poligono), esticada
        big = max(polys, key=lambda q: cv2.contourArea(q.astype(np.float32) / 4))
        x, y, w, h = cv2.boundingRect((big / 4).astype(np.int32))
        fb = flag_bgr(code)
        if fb is None or w < 2 or h < 2: camada = np.full_like(img, cor)
        else:
            camada = np.full_like(img, cor); fr = cv2.resize(fb, (w, h), interpolation=cv2.INTER_AREA)
            x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
            if x1 > x0 and y1 > y0: camada[y0:y1, x0:x1] = fr[y0 - y:y1 - y, x0 - x:x1 - x]
            # outros pedacos (ilhas) fora do bbox: cor media da bandeira
            media = fb.reshape(-1, 3).mean(0); fora = np.ones(img.shape[:2], bool); fora[y0:y1, x0:x1] = False; camada[fora] = media
        m = (mask.astype(np.float32) / 255 * forca * a)[..., None]
        out = (out * (1 - m) + camada * m).astype(np.uint8)
    brilho = np.zeros_like(out)
    for pts in linhas: cv2.polylines(brilho, [pts], True, (255, 255, 255), 10, cv2.LINE_AA, 2)
    brilho = cv2.GaussianBlur(brilho, (0, 0), 7)
    out = cv2.add(out, (brilho * (.7 * a)).astype(np.uint8))
    for pts in linhas: cv2.polylines(out, [pts], True, (255, 255, 255), 3, cv2.LINE_AA, 2)
    return out

# ---------- textos ----------
def fonte(p, n): return ImageFont.truetype(p, n)
def texto_contorno(d, xy, txt, f, cor=(255, 255, 255), borda=10, anchor='mm'):
    d.text(xy, txt, font=f, fill=cor, anchor=anchor, stroke_width=borda, stroke_fill=(0, 0, 0))
def caber(txt, path, n, maxw):
    f = fonte(path, n)
    while f.getlength(txt) > maxw and n > 30: n -= 4; f = fonte(path, n)
    return f
FLAGS = {}
def bandeira(c):
    if c not in FLAGS: FLAGS[c] = Image.open(f'dados/flags/{c}.png').convert('RGBA')
    return FLAGS[c]
ISO2 = {k: v['properties']['ISO_A2_EH'].lower() for k, v in PA.items()}

def legenda(tt):   # UMA palavra por vez, branca, no meio (como os videos de referencia)
    if os.environ.get('SEM_LEGENDA'): return None
    for k in range(NS):
        a, b, d = SEG[k]
        if a <= tt < b:
            pw = PAL[k]
            if tt > a + pw[-1][1] + .2: return None
            i = max([j for j, w in enumerate(pw) if a + w[0] <= tt] or [0])
            return pw[i][2]
    return None
EMOJI = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109); EMO = {}
def emoji(ch, tam):
    if ch not in EMO:
        im = Image.new('RGBA', (160, 160)); ImageDraw.Draw(im).text((80, 80), ch.replace('\ufe0f', ''), font=EMOJI, embedded_color=True, anchor='mm'); EMO[ch] = im.crop(im.getbbox())
    e = EMO[ch]; return e.resize((tam, int(tam * e.height / e.width)), Image.LANCZOS)

def sobrepor(img, tt):
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA'); d = ImageDraw.Draw(pil)
    k = max(i for i in range(NS) if SEG[i][0] - ANT <= tt or i == 0); a = SEG[k][0] - ANT
    if k > 0:
        it = R['items'][k - 1]; u = tt - a - VOO + .1
        if u > 0:
            pop = min(1, u / .3); esc = 1 + .3 * math.sin(min(1, u / .3) * math.pi) * (1 - min(1, u / .3)) + .15 * math.sin(min(1, u / .3) * math.pi)
            lat0, lon0, s = camera(tt)
            if 'pin' in it: la, lo = it['pin']
            else: p = PA[it['hl'][0]]['properties']; la, lo = p['LABEL_Y'], p['LABEL_X']
            pp, cc = projetar(np.array([lo]), np.array([la]), lat0, lon0, s); x, y = pp[0]
            x = min(max(x, 230), W - 230); y = min(max(y, 480), H - 760)
            if 'pin' in it:
                for rr in range(3):
                    raio = 16 + ((tt * 40 + rr * 25) % 75); al = int(255 * (1 - (raio - 16) / 75))
                    d.ellipse([x - raio, y - raio, x + raio, y + raio], outline=(255, 255, 255, al), width=4)
                d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=(230, 40, 40), outline=(255, 255, 255), width=5)
            nome = (it.get('label') or PA[it['hl'][0]]['properties']['NAME']).upper()
            fnm = fonte(FX, 46); tw = fnm.getlength(nome); by = y + 70
            al = int(255 * pop)
            d.rounded_rectangle([x - tw / 2 - 24, by - 34, x + tw / 2 + 24, by + 34], 12, fill=(255, 255, 255, al), outline=(30, 30, 30, al), width=3)
            d.text((x, by), nome, font=fnm, fill=(25, 25, 25, al), anchor='mm')
            fl = it['flag'] if 'flag' in it else (ISO2.get(it['hl'][0], '') if it.get('hl') else '')
            if 'pin' in it and fl and os.path.exists(f'dados/flags/{fl}.png'):   # cartao com a bandeira acima do nome
                bw = int(150 * pop); bh = int(bw * .75)
                if bw > 10:
                    b = bandeira(fl).resize((bw, bh), Image.LANCZOS); fx, fy = int(x - bw / 2), int(y - 40 - bh)
                    d.rounded_rectangle([fx - 6, fy - 6, fx + bw + 6, fy + bh + 6], 10, fill=(255, 255, 255, 255)); pil.alpha_composite(b, (fx, fy))
            if it.get('icon'):   # icone do fato, ao lado do pais
                tam = int(190 * esc * pop) if pop > .05 else 0
                if tam > 8:
                    e = emoji(it['icon'], tam); ex = int(min(W - e.width - 40, x + (115 if 'pin' in it else 70))); ey = int(max(380, y - e.height - 60))
                    sombra = Image.new('RGBA', e.size, (0, 0, 0, 0)); sombra.putalpha(e.getchannel('A').point(lambda v: int(v * .5)))
                    pil.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(8)), (ex + 8, ey + 12)); pil.alpha_composite(e, (ex, ey))
                    if it.get('nao'):   # proibido: circulo vermelho cortado
                        r0 = max(e.width, e.height) * .62; cx0, cy0 = ex + e.width / 2, ey + e.height / 2; lw = max(6, int(tam * .07))
                        d.ellipse([cx0 - r0, cy0 - r0, cx0 + r0, cy0 + r0], outline=(225, 30, 30, 255), width=lw)
                        q = r0 * .7071; d.line([cx0 - q, cy0 - q, cx0 + q, cy0 + q], fill=(225, 30, 30, 255), width=lw)
    w = legenda(tt)
    if w:
        f = caber(w, FB, 96, W - 120); texto_contorno(d, (W / 2, H * .68), w, f, (255, 255, 255), 9)
    return cv2.cvtColor(np.array(pil.convert('RGB')), cv2.COLOR_RGB2BGR)

def quebrar(txt, f, maxw):
    ws = txt.split(); ls = ['']
    for w in ws:
        if f.getlength((ls[-1] + ' ' + w).strip()) > maxw: ls.append(w)
        else: ls[-1] = (ls[-1] + ' ' + w).strip()
    return ls

def quadro(fi):
    tt = fi / FPS; lat0, lon0, s = camera(tt); img = terra(lat0, lon0, s)
    k = max(i for i in range(NS) if SEG[i][0] - ANT <= tt or i == 0)
    if k > 0:
        it = R['items'][k - 1]; a = min(1, max(0, (tt - SEG[k][0] + ANT - VOO + .1) / .35))
        # ponto (pin): pais grande demais para a tela -> so' contorno (a bandeira vai num cartao ao lado do nome)
        fp = 0 if 'pin' in it else 1
        img = desenhar_paises(img, it.get('hl2', []), (90, 90, 90), a, lat0, lon0, s, .55 * fp)
        img = desenhar_paises(img, it.get('hl', []), (0, 214, 255), a, lat0, lon0, s, .9 * fp)
    img = sobrepor(img, tt)
    fad = min(1, tt / .3, (TOTAL - tt) / .3)
    if fad < 1: img = (img * fad).astype(np.uint8)
    return img

def trabalho(args):
    f0, f1 = args
    for fi in range(f0, f1):
        p = f'{OUT}/frames/f{fi:05d}.jpg'
        if not os.path.exists(p): cv2.imwrite(p, quadro(fi), [cv2.IMWRITE_JPEG_QUALITY, 92])

if __name__ == '__main__':
    carregar(); os.makedirs(f'{OUT}/frames', exist_ok=True); N = int(TOTAL * FPS)
    if len(sys.argv) > 2:
        for x in sys.argv[2:]: cv2.imwrite(f'{OUT}/q{int(float(x) * FPS):05d}.jpg', quadro(int(float(x) * FPS)))
        sys.exit()
    import multiprocessing as mp
    lotes = [(i, min(N, i + 30)) for i in range(0, N, 30)]
    with mp.get_context('fork').Pool(4) as pool: list(pool.imap_unordered(trabalho, lotes))
    # audio: voz + trilha + whoosh
    import audio_geo; audio_geo.montar(OUT, SEG, TOTAL)
    nome = f'{OUT}/{RID}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{OUT}/frames/f%05d.jpg', '-i', f'{OUT}/audio.wav', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', nome], check=True)
    print('pronto', nome, round(TOTAL, 1), 's')
