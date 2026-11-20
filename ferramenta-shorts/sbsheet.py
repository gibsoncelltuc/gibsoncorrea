import sys, json, textwrap
from PIL import Image, ImageDraw, ImageFont
jf, out = sys.argv[1], sys.argv[2]; J = json.load(open(jf)); L = J['list']; story = J['id']
try: ph = json.load(open(f"stories/{story}/work/phrases.json")); P = ph.get('phrases') or []
except Exception: P = []
def narr(t):
    for p in P:
        a = p.get('s', p.get('start')); b = p.get('e', p.get('end'))
        if a is not None and b is not None and a <= t <= b: return p.get('text', '')
    return ''
cols = 6; tw = 270; th = 480; cap = 62
rows = (len(L) + cols - 1) // cols; sh = Image.new('RGB', (cols * tw, rows * (th + cap)), (24, 24, 24)); d = ImageDraw.Draw(sh)
try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11); fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
except Exception: fnt = fb = ImageFont.load_default()
for k, j in enumerate(L):
    x, y = (k % cols) * tw, (k // cols) * (th + cap); sh.paste(Image.open(j['file']).resize((tw, th)), (x, y))
    d.text((x + 4, y + th + 3), f"{j['id']}  f{j['f']}  {j['t']}s", fill=(255, 220, 90), font=fb)
    for i, ln in enumerate(textwrap.wrap(narr(float(j['t'])), 44)[:3]): d.text((x + 4, y + th + 19 + i * 13), ln, fill=(220, 220, 220), font=fnt)
sh.save(out, quality=84); print(out, sh.size)
