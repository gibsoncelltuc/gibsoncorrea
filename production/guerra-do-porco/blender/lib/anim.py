"""Animação determinística (função pura de t): easing, keyframes pose-a-pose, atuação (idle/walk/march/aim/shock/laugh/stop), câmera por chaves, timing real das palavras."""
import json, math, os
from . import util
ROOT = util.ROOT
def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def lerp(a, b, t): return a + (b - a) * t
def smoother(t): t = clamp(t); return t * t * t * (t * (t * 6 - 15) + 10)
def ease_out(t): return 1 - (1 - clamp(t)) ** 3
def ease_inout(t): t = clamp(t); return 4 * t * t * t if t < .5 else 1 - (-2 * t + 2) ** 3 / 2
def ease_out_back(t, s=1.9): t = clamp(t); c3 = s + 1; return 1 + c3 * (t - 1) ** 3 + s * (t - 1) ** 2
def keys(t, k, ease=ease_out_back):
    if t <= k[0][0]: return k[0][1]
    for i in range(1, len(k)):
        if t <= k[i][0]: t0, v0 = k[i - 1]; t1, v1 = k[i]; return lerp(v0, v1, ease((t - t0) / (t1 - t0)))
    return k[-1][1]
# ---------------- timing ----------------
T = json.load(open(os.path.join(ROOT, 'script', 'word-timings.json')))
def _norm(s):
    import re; return re.sub(r'[^\w]', '', s.lower())
def word_start(line, prefix, nth=0): return [w for w in T['words'] if w['line'] == line and _norm(w['text']).startswith(_norm(prefix))][nth]['start']
def word_end(line, prefix, nth=0): return [w for w in T['words'] if w['line'] == line and _norm(w['text']).startswith(_norm(prefix))][nth]['end']
def line_start(i): return [l for l in T['lines'] if l['id'] == i][0]['start']
TOTAL = T['total']; FPS = 30
BANG1 = word_start('L1', 'matou') + 0.1; BANG2 = word_start('L2', 'atirou') + 0.05; BANGS = [BANG1, BANG2]
DIS = 0.4
SHOT_STARTS = [('S1', 0.0), ('S2', line_start('L2') - .3), ('S3', line_start('L3') - .3), ('S4', line_start('L4') - .3), ('S5', line_start('L5') - .3), ('S6', word_start('L5', 'ninguém') - .3)]
SHOTS = {sid: (st, (SHOT_STARTS[i + 1][1] if i + 1 < len(SHOT_STARTS) else TOTAL)) for i, (sid, st) in enumerate(SHOT_STARTS)}
# ---------------- atuação (ângulos no mesmo referencial do rig TS: 0 = pendurado, + = para frente) ----------------
def blink_at(t, off=0.0): p = (t + off) % 3.1; return math.sin(p / .12 * math.pi) if p < .12 else 0.0
def P(**kw):
    d = dict(x=0, y=0, z=0, face=1, scale=1.0, bob=0.0, lean=0.0, tilt=0.0, armL=(0.1, 0.1), armR=(-0.1, 0.1), legL=(0, 0), legR=(0, 0), look=(0, 0), blink=0.0, lid=0.42, eye='lid', brows=(0, 0), angry=0.0, mouth='line', open=0.0, sweat=0.0, squash=0.0); d.update(kw); return d
def idle(t, x=0, y=0, z=0, face=1, off=0.0, scale=1.0):
    return P(x=x, y=y, z=z, face=face, scale=scale, bob=math.sin((t + off) * 2.1) * .022, lean=math.sin((t + off) * .9) * .012,
             armL=(.1 + math.sin((t + off) * 1.3) * .03, .12), armR=(-.1 - math.sin((t + off) * 1.3) * .03, .12), blink=blink_at(t, off), look=(math.sin((t + off) * .5) * .5, 0))
def walk(t, speed=1.7, off=0.0):
    ph = (t + off) * speed * math.pi * 2; s, c = math.sin(ph), math.cos(ph)
    return dict(bob=abs(c) * .09 - .03, legL=(s * .55, max(0, -c) * .6), legR=(-s * .55, max(0, c) * .6), armL=(-s * .5, .25), armR=(s * .5, .25), lean=-.04)
def march(t, off=0.0):
    ph = (t + off) * 1.9 * math.pi * 2; s, c = math.sin(ph), math.cos(ph)
    return dict(bob=abs(c) * .07, legL=(s * .62, max(0, -c) * .8), legR=(-s * .62, max(0, c) * .8), armL=(-s * .25 + .2, .9), armR=(s * .25 + .2, .9), lean=0)
def aim_up(t, t0, tfire): return keys(t, [(t0, 0), (tfire - .12, 1)], ease_inout)
def aim_fire(t, base, t0, tfire):
    up = aim_up(t, t0, tfire); rec = math.exp(-(t - tfire) * 7) if t >= tfire else 0.0
    d = dict(base); d.update(armR=(lerp(-.1, 1.5, up) + rec * .35, lerp(.12, .18, up)), armL=(lerp(.1, 1.55, up) + rec * .3, lerp(.12, .35, up)), lean=-.04 * up + rec * .16, bob=base['bob'] - .04 * up, tilt=.1 * up - rec * .1,
             lid=lerp(.42, .78 - rec * .5, up), brows=(-.2 * up, -.2 * up), angry=.35 * up, mouth='line'); return d
def smug(b): d = dict(b); d.update(eye='lid', lid=.55, brows=(.35, -.4), mouth='smirk', tilt=b['tilt'] + .04); return d
def shock(t, b, t0):
    u = clamp((t - t0) / .18); pop = ease_out_back(u, 2.5); d = dict(b)
    d.update(eye='wide' if u > 0 else b['eye'], brows=(.9, .9), mouth='oh' if u > 0 else b['mouth'], open=.5, sweat=(t - t0) * 1.2 if u > 0 else 0, squash=.1 * math.sin(u * math.pi) * (1 - u * .2), bob=b['bob'] + .08 * math.sin(pop * math.pi * .5), lean=b['lean'] * (1 - u)); return d
def laugh(t, b, amp=1.0):
    sh = math.sin(t * 24) * .5 + .5; d = dict(b); d.update(eye='arc', mouth='laugh', open=.4 + .6 * sh, brows=(.7, .7), bob=b['bob'] + abs(math.sin(t * 12)) * .08 * amp, lean=.1 + math.sin(t * 12) * .03 * amp, tilt=-.12 + math.sin(t * 6) * .05, armL=(.9, 1.5), armR=(-.6, 1.6)); return d
def stop_hand(t, b, t0):
    up = keys(t, [(t0, 0), (t0 + .3, 1)], ease_out_back); shake = math.sin((t - t0 - .2) * 10) * .08 * math.exp(-(t - t0 - .2) * 1.2) if t > t0 + .2 else 0.0
    d = dict(b); d.update(armR=(lerp(-.1, 2.55, up), lerp(.12, -.15, up)), tilt=b['tilt'] + shake, eye='lid', lid=.6, brows=(.1, .1), mouth='line'); return d
def point(t, b, t0, side='R', up=1.45):
    u = keys(t, [(t0, 0), (t0 + .25, 1)], ease_out_back); a = lerp(.1, up, u); d = dict(b); d['armL' if side == 'L' else 'armR'] = (a, lerp(.1, .05, u)); return d
# ---------------- câmera ----------------
def cam_at(t, ks, bangs=BANGS):
    """ks = [dict(t, pos, look, fov, roll)] — smootherstep entre chaves + arco + sway + tremor de tiro."""
    i = 0
    while i < len(ks) - 2 and t > ks[i + 1]['t']: i += 1
    a = ks[i]; b = ks[min(i + 1, len(ks) - 1)]; u = 1.0 if b['t'] == a['t'] else smoother((t - a['t']) / (b['t'] - a['t']))
    pos = [lerp(a['pos'][k], b['pos'][k], u) for k in range(3)]; look = [lerp(a['look'][k], b['look'][k], u) for k in range(3)]; fov = lerp(a['fov'], b['fov'], u); roll = lerp(a.get('roll', 0), b.get('roll', 0), u)
    arc = math.sin(math.pi * u) * .06; pos[2] += arc + math.sin(t * .9 + 1) * .018; pos[0] += math.sin(t * .7) * .025
    for bg in bangs:
        d = t - bg
        if 0 <= d < .7: e = math.exp(-d * 9); pos[0] += math.sin(d * 70) * .09 * e; pos[2] += math.cos(d * 63) * .07 * e; fov -= 3.0 * e
    return dict(pos=pos, look=look, fov=fov, roll=roll)
