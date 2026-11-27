# thumbnails: 9:16 (shorts) e 16:9 (video normal) a partir de quadros do proprio video
# uso: python3 thumb.py <id>
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
RID = sys.argv[1]; R = json.load(open(f'roteiros/{RID}.json')); OUT = f'out/{RID}'
FB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
PAL = json.load(open(f'{OUT}/voz/palavras.json'))
def quadro(t, p):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', f'{OUT}/{RID}.mp4', '-frames:v', '1', p], check=True); return Image.open(p).convert('RGB')
dur = lambda p: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
# tempo do 1o item ja destacado (fim da 1a frase do item 1)
t = .3; segs = []
for k in range(len(PAL)): d = dur(f'{OUT}/voz/s{k:02d}.mp3'); segs.append(t); t += d + .45
def limpo(t):   # quadro sem legenda, direto do motor
    fi = int(t * 30); subprocess.run(['python3', 'geo.py', RID, str(t)], check=True, env={**os.environ, 'SEM_LEGENDA': '1'}, capture_output=True)
    return Image.open(f'{OUT}/q{fi:05d}.jpg').convert('RGB')
it1 = int(os.environ.get('THUMB_ITEM', '1'))
fundo = limpo(segs[it1] - .5 + .85 + 1.3); globo = limpo(1.0)
def quebrar(txt, f, maxw):
    ls = ['']
    for w in txt.split():
        if f.getlength((ls[-1] + ' ' + w).strip()) > maxw: ls.append(w)
        else: ls[-1] = (ls[-1] + ' ' + w).strip()
    return ls
def titulo(d, txt, caixa, n, cor1=(255, 214, 0)):
    x0, y0, x1, y1 = caixa; f = ImageFont.truetype(FB, n); ls = quebrar(txt, f, x1 - x0)
    while (len(ls) * n * 1.08 > y1 - y0 or max(f.getlength(l) for l in ls) > x1 - x0) and n > 40:
        n -= 4; f = ImageFont.truetype(FB, n); ls = quebrar(txt, f, x1 - x0)
    y = (y0 + y1) / 2 - len(ls) * n * 1.08 / 2 + n * .54
    for i, l in enumerate(ls):
        d.text(((x0 + x1) / 2, y), l, font=f, fill=cor1 if i % 2 == 0 else (255, 255, 255), anchor='mm', stroke_width=max(6, n // 10), stroke_fill=(0, 0, 0)); y += n * 1.08
# 9:16: quadro do pais destacado, mais contraste, titulo no alto
v = ImageEnhance.Contrast(ImageEnhance.Color(fundo).enhance(1.25)).enhance(1.1)
d = ImageDraw.Draw(v); d.rectangle([0, 0, 1080, 700], fill=None)
grad = Image.new('L', (1080, 1920), 0); gd = ImageDraw.Draw(grad)
for y in range(760): gd.line([(0, y), (1080, y)], fill=int(200 * (1 - y / 760)))
v = Image.composite(Image.new('RGB', v.size, (0, 0, 0)), v, grad); d = ImageDraw.Draw(v)
titulo(d, R['title'], (60, 70, 1020, 640), 150)
v.save(f'{OUT}/{RID}_thumb_9x16.jpg', quality=93)
# 16:9: globo a esquerda, pais destacado a direita (recortes), titulo grande
h = Image.new('RGB', (1280, 720), (0, 0, 0))
g = globo.crop((0, 300, 1080, 1500)).resize((600, 667)); h.paste(g, (-40, 30))
p = ImageEnhance.Color(fundo).enhance(1.25).crop((90, 420, 990, 1320)).resize((470, 470)); m = Image.new('L', (470, 470), 0); ImageDraw.Draw(m).ellipse([0, 0, 469, 469], fill=255)
h.paste(p, (770, 210), m.filter(ImageFilter.GaussianBlur(3))); d = ImageDraw.Draw(h)
d.ellipse([770, 210, 1240, 680], outline=(255, 214, 0), width=10)
titulo(d, R['title'], (470, 20, 1260, 220), 92)
h.save(f'{OUT}/{RID}_thumb_16x9.jpg', quality=93)
print('thumbs', RID)
