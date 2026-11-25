# Reescreve um roteiro na ESTRUTURA VIRAL aproveitando o VISUAL das cenas antigas (25/11).
#   python3 reescrever_viral.py <id> mostrar          -> lista as cenas antigas (bN, lugar, gente, objetos, frase)
#   python3 reescrever_viral.py <id> aplicar plano.json
# plano.json: {"gancho_tipo": "...", "gancho_cumprido": "...", "texto_gancho": "TEXTO NA TELA",
#              "cenas": [[bN_antigo, "bloco", "frase", "palavra-da-acao", {campos que mudam}], ...]}
# Guarda o roteiro antigo em videos/<id>/beats_v24.json (uma vez). A leitura (encena) de cada frase vem do plano.
import json, sys, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
id_, modo = sys.argv[1], sys.argv[2]
P = f'videos/{id_}/beats.json'; V = f'videos/{id_}/beats_v24.json'
B = json.load(open(V if os.path.exists(V) else P, encoding='utf-8'))
O = [b for b in B['beats'] if not b.get('_cta') and 'tema do próximo vídeo' not in b.get('say', '')]
VIS = ('shot', 'who', 'props', 'set', 'interior', 'crowd', 'mapa', 'mapa_at', 'fachada', 'text', 'titulo', 'batalha', 'tiros', 'fx', 'sfx', 'detalhe', 'interacao', 'acao', 'hora', 'light', 'regiao',
       'veiculo', 'montado', 'explica', 'hud', 'quadro_manual', 'cx', 'cz', 'h', 'd0', 'd1', 'objetos', 'tela', 'emus', 'animals', 'impact', 'tstyle', 'tscale', 'placa', 'tat', 'shot_lock')
if modo == 'mostrar':
    print(f"{id_}: {B.get('serie')} EP {B.get('ep')} - {B.get('title')} | ano {B.get('ano')} | heroi {B.get('heroi')}")
    for i, b in enumerate(O):
        lug = b.get('interior') and 'int:' + b['interior'] or b.get('set') or '-'
        ex = ' '.join(f'{k}={json.dumps(b[k], ensure_ascii=False)[:40]}' for k in ('mapa', 'text', 'batalha', 'explica', 'hud', 'veiculo', 'crowd') if b.get(k))
        print(f"b{i} [{lug}] who={b.get('who')} props={[p[0] for p in b.get('props') or []]} {ex}\n    \"{b.get('say')}\"")
    sys.exit(0)
if not os.path.exists(V): json.dump(B, open(V, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
PL = json.load(open(sys.argv[3], encoding='utf-8'))
N = []
for c in PL['cenas']:
    i, bloco, say = c[0], c[1], c[2]; na = c[3] if len(c) > 3 else say.split()[0]; mud = c[4] if len(c) > 4 else {}
    b = {k: json.loads(json.dumps(v)) for k, v in O[i].items() if k in VIS}
    for k, v in mud.items():
        if k == 'encena_antiga': continue
        if v is None: b.pop(k, None)
        else: b[k] = v
    b['bloco'] = bloco; b['say'] = say
    b.pop('encena_antiga', None)
    b['encena'] = (O[i].get('encena') if mud.get('encena_antiga') else None) or mud.get('encena') or {'sentido': 'afirmativa', 'passos': [{'faz': 'mostra', 'na': na}]}
    if mud.get('encena_antiga'): b.pop('encena_antiga', None)
    N.append(b)
if PL.get('texto_gancho'): N[0]['text'] = PL['texto_gancho']; N[0]['titulo'] = True
B['beats'] = N; B['gancho_tipo'] = PL['gancho_tipo']; B['gancho_cumprido'] = PL['gancho_cumprido']; B['loop_frase_ok'] = True
for k in ('max_wide', 'estrutura_ok', 'duracao_ok', 'gancho_ok', 'cta_texto'): B.pop(k, None)
json.dump(B, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{id_}: {len(N)} cenas escritas na estrutura viral')
