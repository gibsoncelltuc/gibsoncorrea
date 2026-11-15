"""Vestir os cenários: posiciona os objetos de cena (dress.py) em cada plano, pensando no que a câmera enxerga. Coordenadas de mundo (fazenda: jardim x∈[-6,6], y∈[-3.4,4.6]; cabana (-11.5,7.5); placa (8.2,-1.8))."""
import math, bpy, numpy as np
from . import dress as D, props, nature, util, mats
class Smoke:
    """fumaça contínua da chaminé: n baforadas em ciclo (função pura de t)"""
    def __init__(self, pos, n=9, period=4.2): self.pos = pos; self.n = n; self.T = period; self.puffs = [props.Puff() for _ in range(n)]
    def update(self, t):
        for i, p in enumerate(self.puffs):
            ph = i * self.T / self.n; k = math.floor((t - ph) / self.T); p.set(t, ph + k * self.T, self.pos, self.T * 1.15, .22, 2.6, (1.4, .35))
def chimney(): return Smoke((-9.3, 6.9, float(nature.height(-11.5, 7.5)) + 5.5))
def farm_common(chickens=True):
    """tudo que cerca o jardim e é visto de todos os planos de fazenda"""
    D.barn(-10.5, 17.0, .35); D.well(-7.6, 10.2, .2); D.firewood(-9.4, 5.3, .15); D.barrel(-8.4, 3.2, label='H.B.CO.\nFLOUR', seed=2); D.barrel(-7.6, 3.5, h=.9, r=.38, rz=.5, label='RAIN', seed=3)
    D.clothesline(-13.2, 11.5, .25); D.wagon(-4.2, 13.5, -.45); D.haystack(9.6, 5.0, 1.3, 2.0); D.hay_bale(7.6, 3.5, .3); D.hay_bale(8.2, 4.1, -.2, (1.0, .5, .5)); D.hay_bale(7.9, 3.8, .1, (1.0, .5, .5))
    D.scarecrow(-2.4, 1.9); D.wheelbarrow(3.8, -2.4, .55, 'cabbage'); D.crate(-5.2, -3.9, label='CABBAGES', fill='cabbage', seed=4); D.crate(-4.2, -3.7, (.8, .6, .6), .25, label='H.B.CO.', seed=5); D.crate(-5.0, -3.8, (.7, .55, .55), .1, None, seed=6) if False else None
    D.barrel(-6.5, -3.4, label='FLOUR', seed=7); D.tool('rake', (6.05, 2.2), (6.2, 2.45, 1.6)); D.tool('hoe', (6.05, 2.7), (6.15, 2.9, 1.55)); D.tool('fork', (6.05, 3.2), (6.1, 3.35, 1.8))
    D.bucket(6.5, -2.9); D.stump(7.3, -3.4); D.rock(-4.4, -5.2, .42, 3); D.rock(10.4, -1.2, .34, 5); D.rock(-8.0, -2.0, .4, 6); D.rock(2.0, 7.5, .35, 8)
    for i, (x, y, rz) in enumerate([(2.5, 9.5, .3), (4.2, 10.6, 2.4), (6.0, 9.2, 4.0), (3.4, 12.0, 1.0), (7.6, 11.2, 5.2), (11.4, 9.0, 2.0)]): D.sheep(x, y, rz, seed=20 + i, grazing=(i % 2 == 0))
    if chickens:
        for i, (x, y, rz, w) in enumerate([(-7.2, -.6, .6, True), (-6.6, .4, 2.4, False), (-7.6, 1.0, 4.2, True), (-3.2, 8.6, 1.6, False), (-2.4, 9.2, 3.0, True), (8.9, 1.6, 5.0, False)]): D.chicken(x, y, rz, w, seed=30 + i)
    D.path_decals([(6.2, .9), (7.4, -.6), (8.2, -3.0), (7.4, -7.0)], 1.7, 3); D.path_decals([(-8.4, 2.4), (-6.8, 0.9), (-6.2, .5)], 1.4, 4); D.path_decals([(-8.4, 2.4), (-9.5, 5.0), (-10, 7.0)], 1.3, 5)
    D.ground_scatter('straw', (6.0, 11.0, 2.0, 6.0), 7, 11); D.ground_scatter('leaves', (-6.8, -3.0, -4.6, -2.4), 5, 12); D.ground_scatter('chips', (6.5, 8.3, -4.0, -2.2), 4, 13); D.ground_scatter('straw', (-10.5, -7.0, 1.0, 5.0), 4, 14)
def S1(): farm_common()
def S2(): farm_common()
def S3(): farm_common()
def S6():
    farm_common(chickens=False)
    D.picket_fence([(.25, -1.3), (2.0, -1.3), (2.0, .55), (.25, .55), (.25, -1.3)], .5, .14, 12); D.lantern(2.15, .6); D.lantern(.1, -1.4)
def S4(R=None):
    D.campfire(-29.0, 33.0); D.wagon(-17.5, 40.5, .7, True); D.crate(-13.5, 37.0, (.9, .7, .65), .2, label='U.S.\nARMY', seed=15); D.crate(-12.6, 37.4, (.8, .6, .6), -.3, label='POWDER', seed=16); D.barrel(-12.0, 36.2, label='POWDER', seed=8)
    D.rifle_stack(-26.0, 32.2); D.rifle_stack(-20.0, 38.0); D.cannonballs(-23.2, 35.3, 0); D.lantern(-29.8, 31.9); D.haystack(-10.0, 41.0, 1.4, 2.0); D.rock(-31.6, 31.0, .4, 9)
    D.firewood(-32.0, 35.0, .3, 5, 3); D.barrel(-24.5, 40.2, label='RUM', seed=9)
def S5():
    D.ship_wheel(-2.6, 4.3, .12); D.barrel(2.7, 4.5, label='H.M.S.\nGANGES', seed=21); D.barrel(3.4, 4.1, h=.9, r=.38, rz=.5, label='POWDER', seed=22); D.rope_coil(-1.2, 3.0, 0, .45); D.rope_coil(2.0, 3.2, 0, .4)
    D.cannonballs(1.2, 4.7, 0, 3, .09); D.cannonballs(-3.9, 3.0, 0, 2, .09); D.bell(-4.5, 4.7, 1.2); D.lantern(0.6, 4.9, 1.15); D.ladder(4.2, 3.2, 0, 1.6, .0); D.crate(-3.4, 1.8, (.8, .6, .6), .2, label='H.M.S.', seed=23)
SET = {'S1': S1, 'S2': S2, 'S3': S3, 'S4': S4, 'S5': S5, 'S6': S6}

class Birds:
    """bando de pássaros distantes: cada um = V de duas asas que batem (função pura de t), voando em arco no céu"""
    def __init__(self, n=7, seed=3, base=(-60, 150, 55), spread=(50, 40, 14)):
        r = np.random.default_rng(seed); self.items = []; mat = mats.flat('bird_m', (.08, .07, .1, 1), rough=1.0, haze=False)
        for i in range(n):
            me = bpy.data.meshes.new('bird'); me.from_pydata([(0, 0, 0), (-1, .1, .2), (-.5, 0, -.05), (0, 0, 0), (1, .1, .2), (.5, 0, -.05)], [], [(0, 1, 2), (3, 5, 4)]); me.materials.append(mat); o = bpy.data.objects.new('bird', me); util.link(o); o.visible_shadow = False
            self.items.append((o, np.array(base) + r.uniform(-1, 1, 3) * np.array(spread), r.uniform(0, 6.28), r.uniform(7, 11)))
    def update(self, t, v=(3.2, .4, .1)):
        for o, p0, ph, fr in self.items:
            o.location = (p0[0] + v[0] * t, p0[1] + v[1] * t, p0[2] + v[2] * t + math.sin(t * .8 + ph) * .6); f = math.sin(t * fr + ph); o.scale = (2.2, 2.2, 2.2); o.rotation_euler = (f * .55, 0, 0.1)
def drift_clouds(objs, t, speed=1.3):
    """nuvens derivam lentamente no vento (posição-base guardada na 1ª chamada)"""
    for i, c in enumerate(objs.get('clouds', [])):
        if 'x0' not in c: c['x0'] = c.location.x
        c.location.x = c['x0'] + t * speed * (1 + .12 * (i % 4))
