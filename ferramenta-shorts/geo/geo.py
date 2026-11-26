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
VOO = 1.1
def camera(tt):
    k = max(i for i in range(NS) if SEG[i][0] <= tt or i == 0); a = SEG[k][0]
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

def desenhar_paises(img, codes, cor, a, lat0, lon0, s):
    if a <= 0 or not codes: return img
    cam = img.copy(); linhas = []
    for code in codes:
        for r in aneis(code):
            p, cc = projetar(r[:, 0], r[:, 1], lat0, lon0, s)
            if (cc < .05).any() or np.abs(p).max() > 60000: continue
            pts = np.round(p * 4).astype(np.int32); cv2.fillPoly(cam, [pts], cor, cv2.LINE_AA, 2); linhas.append(pts)
    img = cv2.addWeighted(cam, .38 * a, img, 1 - .38 * a, 0)
    brilho = np.zeros_like(img)
    for pts in linhas: cv2.polylines(brilho, [pts], True, (255, 255, 255), 9, cv2.LINE_AA, 2)
    brilho = cv2.GaussianBlur(brilho, (0, 0), 6)
    img = cv2.add(img, (brilho * (.8 * a)).astype(np.uint8))
    for pts in linhas: cv2.polylines(img, [pts], True, tuple(int(c * a + 255 * (1 - a)) for c in cor), 4, cv2.LINE_AA, 2)
    return img

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

def legenda(tt):   # 1 a 3 palavras por vez, a atual em amarelo
    for k in range(NS):
        a, b, d = SEG[k]; a0 = a + .0
        if a <= tt < b:
            pw = PAL[k]; i = max([j for j, w in enumerate(pw) if a0 + w[0] <= tt] or [0])
            gs = [[0]]
            for j in range(1, len(pw)):
                if len(gs[-1]) >= 3 or pw[j][0] - pw[j - 1][1] > .2: gs.append([j])
                else: gs[-1].append(j)
            gi = next(g for g in gs if i in g); g0 = gi[0]; grupo = [pw[j] for j in gi]
            if tt > a0 + pw[-1][1] + .25: return None
            return [(w[2], g0 + j == i) for j, w in enumerate(grupo)]
    return None

def sobrepor(img, tt):
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(pil)
    k = max(i for i in range(NS) if SEG[i][0] <= tt or i == 0); a = SEG[k][0]
    if k == 0:   # titulo do gancho
        f = fonte(FB, 118); linhas = quebrar(R['title'], f, W - 110)
        while max(f.getlength(l) for l in linhas) > W - 80: f = fonte(FB, f.size - 6); linhas = quebrar(R['title'], f, W - 110)
        y = 200 - (len(linhas) - 1) * f.size * .3
        for ln in linhas: texto_contorno(d, (W / 2, y), ln, f, (255, 214, 0), 12); y += f.size * 1.15
    else:
        it = R['items'][k - 1]; u = tt - a - VOO + .15
        if u > 0:
            pop = min(1, u / .25); esc = 1 + .25 * (1 - pop) * math.sin(pop * math.pi)
            # numero + texto grande no alto
            f = caber(it['big'], FB, int(104 * esc), W - 100); texto_contorno(d, (W / 2, 260), it['big'], f, (255, 214, 0), 12)
            fn = fonte(FB, 58); texto_contorno(d, (W / 2, 150), f'#{k}', fn, (255, 255, 255), 8)
            # bandeira + nome no ponto
            lat0, lon0, s = camera(tt)
            if 'pin' in it: la, lo = it['pin']
            else: p = PA[it['hl'][0]]['properties']; la, lo = p['LABEL_Y'], p['LABEL_X']
            pp, cc = projetar(np.array([lo]), np.array([la]), lat0, lon0, s); x, y = pp[0]
            x = min(max(x, 220), W - 220); y = min(max(y, 520), H - 760)
            if 'pin' in it:
                d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(230, 40, 40), outline=(255, 255, 255), width=5)
                for rr in range(3):
                    raio = 16 + ((tt * 40 + rr * 25) % 75); al = int(255 * (1 - (raio - 16) / 75))
                    d.ellipse([x - raio, y - raio, x + raio, y + raio], outline=(255, 255, 255, al), width=3)
            nome = it.get('label') or PA[it['hl'][0]]['properties']['NAME']
            fl = it['flag'] if 'flag' in it else ISO2.get(it['hl'][0], '')
            fnm = fonte(FX, int(52 * min(1, pop * 1.2))) if pop > .1 else None
            if fnm:
                tw = fnm.getlength(nome); by = y + 60
                d.rounded_rectangle([x - tw / 2 - 26, by - 40, x + tw / 2 + 26, by + 40], 40, fill=(255, 255, 255))
                d.text((x, by), nome, font=fnm, fill=(20, 20, 20), anchor='mm')
                if fl and os.path.exists(f'dados/flags/{fl}.png'):
                    bw = int(190 * pop); bh = int(bw * .75)
                    if bw > 10:
                        b = bandeira(fl).resize((bw, bh), Image.LANCZOS); fx, fy = int(x - bw / 2), int(y - 40 - bh)
                        d.rounded_rectangle([fx - 6, fy - 6, fx + bw + 6, fy + bh + 6], 10, fill=(255, 255, 255)); pil.paste(b, (fx, fy), b)
    lg = legenda(tt)
    if lg:
        f = fonte(FB, 92); txt = ' '.join(w for w, _ in lg)
        f = caber(txt, FB, 92, W - 100); x = W / 2 - f.getlength(txt) / 2; y = H - 560
        for w, at in lg:
            texto_contorno(d, (x, y), w, f, (255, 214, 0) if at else (255, 255, 255), 11, 'lm'); x += f.getlength(w + ' ')
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)

def quebrar(txt, f, maxw):
    ws = txt.split(); ls = ['']
    for w in ws:
        if f.getlength((ls[-1] + ' ' + w).strip()) > maxw: ls.append(w)
        else: ls[-1] = (ls[-1] + ' ' + w).strip()
    return ls

def quadro(fi):
    tt = fi / FPS; lat0, lon0, s = camera(tt); img = terra(lat0, lon0, s)
    k = max(i for i in range(NS) if SEG[i][0] <= tt or i == 0)
    if k > 0:
        it = R['items'][k - 1]; a = min(1, max(0, (tt - SEG[k][0] - VOO + .2) / .5))
        img = desenhar_paises(img, it.get('hl2', []), (60, 60, 235), a, lat0, lon0, s)
        img = desenhar_paises(img, it.get('hl', []), (0, 214, 255), a, lat0, lon0, s)
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
