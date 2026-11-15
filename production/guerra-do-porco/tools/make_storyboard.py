#!/usr/bin/env python3
"""Gera storyboard/shots.json (lista de planos/inserts) a partir da EDL em blender/lib/anim.py — fonte única do ritmo da edição."""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(R, 'blender'))
from lib import anim
INFO = {
 'S1': ('GANCHO', 'Um homem mata um porco e dois países quase entram em guerra', 'baixa, fov 57 → sobe e revela a frota', 'porco come; Cutlar mira e atira ("matou"); porco capota; navios surgem', 'BANG1 + clarão + tremor', ['L1']),
 'S2a': ('SETUP', 'o porco do britânico invade a horta do americano', 'tilt-up na bandeira → placa SAN JUAN 1859 → push-in na horta', 'porco trota até a horta; Cutlar nota e mira', 'vento, galinhas', ['L2']),
 'I_eyes': ('TENSÃO (insert)', 'close no rosto do Cutlar: olhos se estreitam, TIRO acende o rosto', 'close frontal, empurra 1,75 → 1,2 m, tremor no tiro', 'pálpebra .42 → .9, sobrancelhas, suor, piscada no tiro', 'BANG2', ['L2']),
 'S3a': ('ZOMBADOR', 'cem dólares × dez: o dono exige, o americano reage', 'baixa, roll .13, push-in lento', 'Griffin exibe a nota $100 e ri; Cutlar suado', 'notas', ['L3']),
 'I_notes': ('PIADA (insert)', 'close nas duas notas: $100 enorme × $10 pequeno', 'close baixo com dutch', 'notas tremulam; Griffin gargalha', 'risada', ['L3']),
 'S4a': ('ESCALADA', 'centenas de soldados', 'baixa, acompanha a marcha', '80 soldados distintos marchando com fuzis e bandeira', 'marcha', ['L4']),
 'I_faces': ('ESCALA (insert)', 'rostos de três soldados, todos diferentes', 'close lateral acompanhando', 'cabeças balançam, olhares e expressões distintos', 'marcha', ['L4']),
 'S4b': ('ESCALADA', 'cinco navios de guerra', 'sobe e panorâmica sobre a tropa até a frota', 'frota em escalão', 'canhão', ['L4']),
 'S5a': ('RECUSA', 'o almirante recebe o aviso do auxiliar', 'baixa, roll -.1', 'auxiliar aponta a luneta', 'mar', ['L5']),
 'I_baynes': ('RECUSA (insert)', 'close no almirante: a mão de "pare"', 'close baixo, push-in', 'pálpebra pesada; mão entra no quadro em "recusou"', 'mar', ['L5']),
 'S6': ('PAGAMENTO + LOOP', 'Ninguém morreu. Só o porco.', 'pull-back até o enquadramento do quadro 0 (loop)', 'túmulo com cruz e flores; os dois tiram o chapéu', 'acorde final', ['L5']),
}
shots = []
for eid, cls, a, b in anim.EDL:
    p, purpose, cam, act, aud, lines = INFO[eid]; shots.append(dict(id=eid, scene=cls, start=round(a, 3), end=round(b, 3), dur=round(b - a, 3), lines=lines, beat=p, purpose=purpose, camera=cam, action=act, audio=aud))
json.dump({'edl': 'blender/lib/anim.py (_edl)', 'shot_count': len(shots), 'mean_shot_s': round(sum(s['dur'] for s in shots) / len(shots), 2), 'shots': shots}, open(os.path.join(R, 'storyboard', 'shots.json'), 'w'), indent=1, ensure_ascii=False)
print(len(shots), 'planos; duração média', round(sum(s['dur'] for s in shots) / len(shots), 2), 's')
