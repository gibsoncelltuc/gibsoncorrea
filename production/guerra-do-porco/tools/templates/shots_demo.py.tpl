"""Cenas e coreografia do vídeo '@TITLE@' (ESPECÍFICO DA HISTÓRIA). Exemplo mínimo e funcional: 1 cena (fazenda), 1 personagem e câmera em movimento.
Cada classe de cena: build() cria mundo/atores UMA vez; update(t) aplica poses/câmera como FUNÇÃO PURA do tempo absoluto t (s) → determinístico e permite inserts com a mesma coreografia.
Para uma história real: copie a estrutura de production/guerra-do-porco/blender/lib/shots.py (6 cenas + 4 inserts), crie uma classe por cena e registre-a em CLASSES."""
import bpy, math
from . import util, renderlib, farm, nature, char, sets
from .anim import *
LOOKS = {'heroi': dict(shirt='#ead9b4', pattern='plain', outfit='overalls', pants='#2f2a46', shoe='#5a3a2a', hat='straw', hatColor='#e8c068', hatBand='#3a6aa8', beard='#c9a06a', build=1.0, sleeve='#2f2a46')}
def gz(x, y): return float(nature.height(x, y))
def apply_cam(cam, spec, focus=None, fstop=3.2, dof=True):
    cam.data.dof.use_dof = dof; renderlib.place_camera(cam, spec['pos'], spec['look'], fov=spec['fov'], roll=spec.get('roll', 0), focus=focus if focus is not None else math.dist(spec['pos'], spec['look']), fstop=fstop)
class Base:
    eid = None
    def __init__(self, R): self.R = R; self.cam = renderlib.camera(56, dof=True, fstop=3.2, focus=6.0)
    def frames(self, fps=30, pad=.2):
        e = self.eid or self.id; a, b = EDIT[e]; first = e == EDL[0][0]; last = e == EDL[-1][0]
        return range(int(round((a - (0 if first else pad)) * fps)), int(round((b + (0 if last else pad)) * fps)))
class Cena1(Base):
    id = 'S1'
    def keys_(self): return {'heroi': self.h.head}
    def build(self): self.f = farm.build('golden', grass_n=self.R['grass']); self.h = char.Char('heroi', LOOKS['heroi']); sets.S1()
    def update(self, t):
        self.h.pose(idle(t, x=0.0, y=-2.5, z=gz(0.0, -2.5), face=1))
        a, b = EDIT[self.eid or self.id]
        spec = cam_at(t, [dict(t=a, pos=(1.2, -6.0, 0.9), look=(0.0, -2.0, 1.0), fov=57), dict(t=b, pos=(0.6, -5.0, 1.1), look=(0.0, -2.0, 1.2), fov=50)])
        apply_cam(self.cam, spec, focus=4.0, fstop=2.4)
CLASSES = {'S1': Cena1}      # classe de cena (campo "scene" de storyboard/shots.json) → classe Python
def _mk(cls, eid): return type(eid, (cls,), {'eid': eid})
SHOT_CLASSES = {eid: _mk(CLASSES[sc], eid) for eid, sc in EDIT_CLASS.items()}
