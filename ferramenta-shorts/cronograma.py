#!/usr/bin/env python3
"""cronograma.py <id> -- CRONOGRAMA DE EXECUCAO do video (stories/<id>/cronograma.md). Gerado pelo mkvideo.py junto com as 4 folhas e atualizado pela fila
a cada etapa. Mostra: (1) o PLANO DE CENAS (cada frase: classe, cenario, camera, quem, objetos, efeito) e (2) as ETAPAS em ordem, com o que confere em cada
uma e o estado (FEITO / PENDENTE / BLOQUEADO). E' a ordem de trabalho: nenhuma etapa comeca com a anterior pendente."""
import json, os, sys, glob, time
ID = sys.argv[1]; R = os.path.dirname(os.path.abspath(__file__)); os.chdir(R); S = f'stories/{ID}'
def J(p, d=None):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d
orq = J(f'{S}/orquestracao.json', {}) or {}; fol = J(f'{S}/folhas.json', {}) or {}; meta = J(f'{S}/meta.json', {}) or {}; pesq = J(f'referencias/{ID}/pesquisa.json'); plano = J(f'referencias/{ID}/plano_pesquisa.json', {}) or {}
ex = os.path.exists; st = lambda n: ex(f'{S}/stages/{n}')
riscos = int((open(f'{S}/riscos.txt').read().strip() or 0)) if ex(f'{S}/riscos.txt') else None
mp4 = glob.glob(f'out/{ID}/*.mp4'); gate = open(f'logs/gate_{ID}.txt').read() if ex(f'logs/gate_{ID}.txt') else ''
n_it = len(plano.get('itens', [])); n_ref = sum(1 for i in (pesq or {}).get('itens', []) if i.get('achados')) if pesq else 0
falta_modelo = [o for c in orq.get('cenas', []) for o in c.get('objetos', []) if '/' in o and not (ex(f'web/assets/library/{o}.glb') or ex(f'web/assets/library/megakit/{o[3:]}.gltf') or not o.startswith(('kit/', 'mk/')))]
E = [
 ('1', 'Roteiro e 4 folhas', 'folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase', ex(f'{S}/folha1_roteiro.md') and ex(f'{S}/folha4_pesquisa.md'), ''),
 ('2', 'Pesquisa de campo', f'cada item do raio-X com referencia; quadro de prints olhado ({n_ref}/{n_it} itens)', bool(pesq) and n_ref >= n_it - max(1, n_it // 3), f'python3 pesquisar.py {ID}'),
 ('3', 'Modelagem do que falta', 'todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real', not falta_modelo, 'modelar em blender/ (formas.py): ' + ', '.join(sorted(set(falta_modelo))) if falta_modelo else ''),
 ('4', 'Travas do roteiro', f'folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: {riscos})', riscos == 0, 'corrigir o roteiro conforme a folha 2'),
 ('5', 'Voz', 'narracao neural gerada e tempos por palavra', st('voice') and ex(f'{S}/voice.mp3'), ''),
 ('6', 'Estilo e enquadramento', 'autoajuste de luz/cor e ajuste de camera de cada tomada', st('style') and st('fit'), ''),
 ('7', 'Gates', 'camera OK, todas as tomadas OK, estilo OK', 'camera OK' in gate and 'ALL TAKES OK' in gate and 'STYLE OK' in gate and st('gate'), ''),
 ('8', 'Storyboard e grade de acoes', 'video inteiro em quadros + 1 quadro no instante de cada acao', ex(f'{S}/storyboard.jpg') and ex(f'{S}/grade_acoes.jpg'), ''),
 ('9', 'Revisao escrita e aprovacao', 'uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa', ex(f'{S}/STORYBOARD_OK') and open(f'{S}/STORYBOARD_OK').read().strip() == str(fol.get('hash_producao')), f'./aprovar_storyboard.sh {ID}'),
 ('10', 'Render', 'todos os quadros renderizados nesta versao das folhas', ex(f'{S}/DONE') or bool(mp4) and ex(f'{S}/DONE'), ''),
 ('11', 'Montagem e som', 'trechos + voz + musica + efeitos; volume normalizado', bool(mp4) and ex(f'{S}/DONE'), ''),
 ('12', 'Conferencia', 'conferir.sh sem falha e folha de contato olhada', ex(f'entregas/{ID}') and ex(f'{S}/DONE'), f'./conferir.sh {ID}'),
 ('13', 'Auditoria das acoes', '1 quadro do mp4 em cada palavra de acao', ex(f'/tmp/claude-0/aud/{ID}.jpg') or ex(f'{S}/auditoria_ok'), f'bash auditar_acoes.sh local {ID} <mp4>'),
 ('14', 'Entrega', 'mp4 original 1080x1920 enviado; commit e push', ex(f'{S}/ENTREGUE'), ''),
]
L = [f"# CRONOGRAMA - {meta.get('title', ID)}", '', f"Gerado em {time.strftime('%d/%m %H:%M')} | {len(orq.get('cenas', []))} cenas | metricas: " + ', '.join(f'{k} {v}%' for k, v in (orq.get('metricas') or {}).items()), '',
     '## 1. Plano de cenas (o que cada frase vai mostrar)', '', 'Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase', '---|---|---|---|---|---|---|---|---']
for c in orq.get('cenas', []):
    br = c.get('briefing') or {}
    L.append(f"{c['cena']} | {c['classe']} | {c.get('cenario', '-')} | {c.get('camera', '-')} | {', '.join(c.get('personagens', [])) or 'sem personagem'} | {c.get('multidao', 0) or '-'} | {', '.join(o.split('/')[-1] for o in c.get('objetos', [])) or '-'} | {'; '.join(f'{k}: {v}' for k, v in br.items())[:120] or '-'} | {c['frase'][:70]}")
L += ['', '## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)', '', 'N | Etapa | O que confere | Estado | Proximo passo', '---|---|---|---|---']
trav = False
for n, nome, conf, ok, prox in E:
    est = ('REFAZER (a etapa anterior mudou)' if ok else 'BLOQUEADO (etapa anterior pendente)') if trav else ('FEITO' if ok else 'PENDENTE'); L.append(f'{n} | {nome} | {conf} | {est} | {"" if (ok and not trav) else prox}')
    if not ok: trav = True
prim = next((f'{n}. {nome}' for n, nome, conf, ok, prox in E if not ok), 'tudo concluido')
L += ['', f'**Etapa atual:** {prim}', '']
open(f'{S}/cronograma.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print(f'cronograma: {S}/cronograma.md | etapa atual: {prim}')
