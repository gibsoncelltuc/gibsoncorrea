"""Teste de movimento do piloto, SEM renderizar (rubrica V2 "Animação e atuação: teste de movimento, contato, expressões, continuidade").
Percorre cada edição da EDL quadro a quadro (30 fps), lê as posições de MUNDO de cabeça/mãos/pés de todos os personagens e mede:
  • pops: maior deslocamento de um ponto entre dois quadros seguidos (teletransporte/estalo);
  • contato: pé abaixo do chão (penetração) e "voo" (nenhum pé de soldado perto do chão) durante a marcha;
  • vida: nenhum personagem principal parado por mais de 0,5 s;
  • continuidade: nos cortes entre plano aberto e insert, a posição de todos os personagens/porco no instante do corte é idêntica nas duas cenas.
Uso: python motion_test.py [edit_id ...]  → qa/motion-report.json"""
import sys, os, json, math, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view
from lib import util, renderlib, shots, anim
from lib.char import U
ROOT = util.ROOT; FPS = anim.FPS
only = sys.argv[1:] or [e[0] for e in anim.EDL]
def tracked():
    """objetos de interesse por personagem: {nome: dict(root, head, handL/R, footL/R)}"""
    objs = bpy.data.objects; out = {}
    for o in objs:
        m = re.match(r'^(.+)_body$', o.name)
        if m and o.type == 'EMPTY':
            n = m.group(1); g = lambda s: objs.get(f'{n}_{s}')
            if g('footL') and g('head'): out[n] = dict(root=objs.get(n), head=g('head'), handL=g('handL'), handR=g('handR'), footL=g('footL'), footR=g('footR'))
    return out
def pos(o): return np.array(o.matrix_world.translation, np.float64)
res = {'edicoes': {}, 'continuidade': [], 'camera': {}, 'versao': 'motion_test v2'}; t_start = time.time(); snaps = {}
MAIN = {'cutlar', 'griffin', 'baynes', 'aide'}
for eid in only:
    util.reset(); sc = renderlib.setup((135, 240), samples=1, bounces=1)
    shot = shots.SHOT_CLASSES[eid]({'grass': 400}); shot.build(); tr = tracked(); a, b = anim.EDIT[eid]
    times = [f / FPS for f in shot.frames()]; CAM = {'t': [], 'pos': [], 'fov': [], 'sujeitos_no_quadro': []}; keys = shot.keys_() if hasattr(shot, 'keys_') else {}; P = {n: {k: [] for k in ('head', 'handL', 'handR', 'footL', 'footR', 'root')} for n in tr}
    for t in times:
        shot.update(t); bpy.context.view_layer.update()
        CAM['t'].append(round(t, 4)); CAM['pos'].append([round(float(v), 4) for v in shot.cam.matrix_world.translation]); CAM['fov'].append(round(math.degrees(shot.cam.data.angle), 3))
        CAM['sujeitos_no_quadro'].append({k: [round(float(c), 3) for c in world_to_camera_view(sc, shot.cam, o.matrix_world.translation)[:2]] for k, o in keys.items()})
        for n, d in tr.items():
            for k in P[n]:
                if d.get(k) is not None: P[n][k].append(pos(d[k]))
    # snapshot no(s) instante(s) de corte para a checagem de continuidade
    for tc in (a, b):
        shot.update(tc); bpy.context.view_layer.update(); snaps.setdefault(round(tc, 3), {})[eid] = {n: [round(float(v), 5) for v in pos(d['root'])] for n, d in tr.items() if d.get('root') is not None}
    e = {'quadros': len(times), 'personagens': len(tr), 'pops': {}, 'contato': {}, 'vida': {}}
    worst = (0.0, None, None, None)
    for n, d in P.items():
        for k, arr in d.items():
            if k == 'root' or len(arr) < 2: continue
            A = np.array(arr); step = np.linalg.norm(np.diff(A, axis=0), axis=1)
            if step.max() > worst[0]: worst = (float(step.max()), n, k, round(times[int(step.argmax()) + 1], 3))
    e['pops'] = {'max_deslocamento_m_por_quadro': round(worst[0], 3), 'onde': {'personagem': worst[1], 'ponto': worst[2], 't': worst[3]},
                 'p99_m_por_quadro': round(float(np.percentile(np.concatenate([np.linalg.norm(np.diff(np.array(d[k]), axis=0), axis=1) for d in P.values() for k in ('head', 'handL', 'handR', 'footL', 'footR') if len(d[k]) > 1]), 99)), 4)}
    # contato: altura do pé relativa ao root do próprio personagem (root.z = chão); repouso = 0,18·U
    rest = 0.18 * U; pen = 0; fly = 0; tot = 0; clear = []
    for n, d in P.items():
        if len(d['footL']) < 2 or len(d['root']) < 2: continue
        hl = np.array([f[2] - r[2] - rest for f, r in zip(d['footL'], d['root'])]); hr = np.array([f[2] - r[2] - rest for f, r in zip(d['footR'], d['root'])])
        pen += int(((hl < -0.03) | (hr < -0.03)).sum()); low = np.minimum(hl, hr); tot += len(low); fly += int((low > 0.08).sum()); clear.append(float(np.median(low)))
    e['contato'] = {'quadros_com_pe_abaixo_do_chao_>3cm': pen, 'quadros_sem_nenhum_pe_a_<8cm_do_chao': fly, 'quadros_avaliados': tot, 'folga_mediana_do_pe_mais_baixo_m': round(float(np.median(clear)), 3) if clear else None}
    # vida: personagens principais presentes — deslocamento acumulado de cabeça+mãos em janelas de 0,5 s
    for n in tr:
        if n not in MAIN or len(P[n]['head']) < 16: continue
        mv = np.array([sum(np.linalg.norm(np.array(P[n][k][i + 15]) - np.array(P[n][k][i])) for k in ('head', 'handL', 'handR')) for i in range(len(P[n]['head']) - 15)]); e['vida'][n] = {'janelas_0.5s_paradas_(<5mm)': int((mv < 0.005).sum()), 'janelas': int(len(mv)), 'movimento_mediano_m_por_0.5s': round(float(np.median(mv)), 3)}
    res['camera'][eid] = CAM; res['edicoes'][eid] = e; print(eid, e['quadros'], 'quadros', e['pops'], e['contato'], flush=True)
# continuidade entre edições que compartilham o mesmo instante de corte
sc_of = anim.EDIT_CLASS
for i in range(len(anim.EDL) - 1):
    a, b = anim.EDL[i][0], anim.EDL[i + 1][0]
    if a not in only or b not in only or shots.SHOT_CLASSES[a].id != shots.SHOT_CLASSES[b].id: continue   # só cortes dentro da MESMA cena (plano aberto ↔ insert)
    tc = round(anim.EDIT[a][1], 3); A = snaps.get(tc, {}).get(a); B = snaps.get(tc, {}).get(b)
    if not A or not B: continue
    common = [n for n in A if n in B]; d = max((np.linalg.norm(np.array(A[n]) - np.array(B[n])) for n in common), default=0.0)
    res['continuidade'].append({'corte': f'{a} → {b}', 't': tc, 'personagens_comuns': len(common), 'max_diferenca_m': round(float(d), 5)})
res['tempo_s'] = round(time.time() - t_start)
json.dump(res, open(os.path.join(ROOT, 'qa', 'motion-report.json'), 'w'), ensure_ascii=False, indent=1); print('FIM', res['tempo_s'], 's'); print(json.dumps(res['continuidade'], ensure_ascii=False))
