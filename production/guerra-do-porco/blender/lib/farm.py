"""Cena da fazenda (ilha de San Juan, 1859): terreno, horta, cerca, cabana, placa, árvores, nuvens, mar, montanhas, sol/céu, neblina."""
import bpy, math, numpy as np
from . import util, mats, texlib, renderlib, nature
from .nature import height
ENVS = {
  'golden': dict(sun_el=24, sun_az=252, sun_col=(1.0, 0.72, 0.42), sun_str=5.0, sky_str=0.85, haze=(0.62, 0.74, 0.92, 1), haze0=120, haze1=900, hs=0.8, exposure=0.0,
                 sky=[(0.0, (0.98, 0.78, 0.55, 1)), (0.12, (0.62, 0.66, 0.84, 1)), (0.34, (0.16, 0.38, 0.86, 1)), (1.0, (0.035, 0.12, 0.55, 1))], glow=0.9),
  'bright': dict(sun_el=50, sun_az=215, sun_col=(1.0, 0.9, 0.78), sun_str=5.2, sky_str=0.9, haze=(0.72, 0.84, 0.96, 1), haze0=140, haze1=1000, hs=0.7, exposure=0.0,
                 sky=[(0.0, (0.86, 0.90, 0.95, 1)), (0.12, (0.5, 0.70, 0.94, 1)), (0.4, (0.12, 0.36, 0.86, 1)), (1.0, (0.03, 0.12, 0.55, 1))], glow=0.45),
  'dusk':   dict(sun_el=6, sun_az=232, sun_col=(1.0, 0.45, 0.22), sun_str=3.6, sky_str=0.8, haze=(0.80, 0.42, 0.55, 1), haze0=80, haze1=700, hs=0.8, exposure=0.0,
                 sky=[(0.0, (1.0, 0.55, 0.28, 1)), (0.10, (0.92, 0.32, 0.5, 1)), (0.30, (0.42, 0.2, 0.62, 1)), (1.0, (0.06, 0.07, 0.34, 1))], glow=1.2),
}
def build(env='golden', seed=1, grass_n=95000, trees_n=12, quality='full', grass_areas=None, sea=True):
    E = ENVS[env]; mats.HAZE.update(color=E['haze'], start=E['haze0'], end=E['haze1'], strength=E['hs'])
    renderlib.world_gradient(E['sky'], renderlib.sun_vec(E['sun_el'], E['sun_az']), E['sun_col'], E['glow'], strength=E['sky_str']); sun = renderlib.sun(E['sun_el'], E['sun_az'], E['sun_col'], E['sun_str'], angle_deg=3.0)
    objs = {'sun': sun}; objs['terrain'] = nature.terrain(seed)
    ex = [(-5.6, 5.6, -1.6, 5.0)]
    gblades = nature.grass(grass_n, (-16, 16, -9.5, 22), seed + 1, exclude=ex, hmax=.34); objs['grass'] = gblades; objs['grass2'] = [nature.grass(n_, a_, seed + 20 + i, name=f'grass_x{i}', hmax=.30) for i, (a_, n_) in enumerate((grass_areas or []) + ([((-9, 9, -8, 9), int(grass_n * .9))] if sea else []))]; objs['flowers'] = nature.flowers(1800 if quality == 'full' else 600, (-14, 14, -8.5, 20), seed + 3)
    objs['garden'] = nature.garden(-5.0, 5.0, -1.0, 4.4, 6, seed + 6, clear=[(1.1, -0.35, .95)])
    objs['fence'] = nature.fence([(-6.2, -3.4), (-6.2, 4.6), (6.2, 4.6), (6.2, -3.4)], gap=(6.2, 0.9, 1.35), seed=seed + 7)
    objs['cabin'] = nature.cabin((-11.5, 7.5), seed=seed + 8); objs['sign'] = nature.sign((8.2, -1.8), 'SAN JUAN\n1859', 0.32)
    objs['trees'] = nature.trees(trees_n, seed + 5); objs['sea'] = nature.sea(); objs['baker'] = nature.mountain((150, 720, SEA_BASE()), (300, 230, 250), 3, name='baker'); objs['range'] = nature.mountain((-300, 760, SEA_BASE()), (360, 170, 130), 5, snow=.97, name='range')
    objs['hills'] = [nature.hill((hx, hy), (hs, hs * .6, hh), sd, f'hill{i}') for i, (hx, hy, hs, hh, sd) in enumerate([(-170, 330, 150, 34, 21), (-20, 400, 190, 40, 22), (190, 360, 160, 36, 23), (80, 520, 220, 52, 24)])]
    rr = util.rng(seed + 11); objs['clouds'] = [nature.cloud((float(rr.uniform(-380, 380)), float(rr.uniform(380, 900)), float(rr.uniform(75, 190))), float(rr.uniform(70, 160)), int(rr.integers(1, 99)), f'cloud{i}') for i in range(9)]
    return objs
def SEA_BASE(): return nature.SEA_Z - 6
