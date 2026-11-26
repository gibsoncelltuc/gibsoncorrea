import sys, os, numpy as np
from PIL import Image
a, b = sys.argv[1], sys.argv[2]; res = []
for f in sorted(os.listdir(a)):
    if not f.endswith('.jpg') or not os.path.exists(os.path.join(b, f)): continue
    x = np.asarray(Image.open(os.path.join(a, f)).convert('RGB'), np.float32); y = np.asarray(Image.open(os.path.join(b, f)).convert('RGB'), np.float32)
    mse = ((x - y) ** 2).mean(); psnr = 99 if mse == 0 else 10 * np.log10(255 ** 2 / mse); res.append((f, psnr, np.abs(x - y).mean()))
for f, p, m in res: print(f, 'PSNR %.1f dB  meanabs %.2f' % (p, m))
print('min PSNR %.1f  mean %.1f' % (min(r[1] for r in res), sum(r[1] for r in res) / len(res)))
