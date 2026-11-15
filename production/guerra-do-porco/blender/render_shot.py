"""Uso: python render_shot.py <SHOT> <res_w> <res_h> <samples> <out_dir> [every=1] [grass=60000] [frames=a:b]"""
import sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from lib import util, renderlib, shots, anim
sid = sys.argv[1]; W, H, S = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); out = sys.argv[5]; every = int(sys.argv[6]) if len(sys.argv) > 6 else 1; grass = int(sys.argv[7]) if len(sys.argv) > 7 else 60000
fr = sys.argv[8] if len(sys.argv) > 8 else None
util.reset(); sc = renderlib.setup((W, H), samples=S, bounces=int(os.environ.get('BOUNCES', 3)), view='Standard', look='None', exposure=float(os.environ.get('EXPO', -0.45)))
t0 = time.time(); shot = shots.SHOT_CLASSES[sid]({'grass': grass}); shot.build(); print('build', round(time.time() - t0, 1), 's', len(bpy.data.objects), 'objetos')
os.makedirs(out, exist_ok=True); frames = list(shot.frames())
if fr: a, b = fr.split(':'); frames = [f for f in frames if int(a) <= f < int(b)]
done = 0; tt = time.time()
for f in frames:
    if (f - frames[0]) % every != int(os.environ.get('OFFSET', 0)) % every: continue
    path = os.path.join(out, f'f{f:04d}.png')
    if os.path.exists(path): continue
    shot.update(f / anim.FPS); sc.render.filepath = path; bpy.ops.render.render(write_still=True); done += 1
    if done % 5 == 0: print(f'{sid} frame {f} ({done}) {round((time.time() - tt) / done, 1)} s/frame', flush=True)
print(sid, 'FIM', done, 'frames em', round(time.time() - tt, 1), 's', flush=True)
