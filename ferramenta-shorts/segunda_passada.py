# 2a passada da ESTRUTURA VIRAL (25/11): troca so' o TEXTO das cenas do plano (planos_viral/<id>.json), mantendo o visual.
#   python3 segunda_passada.py lote.json  -> lote = {"<id>": {"says": [frase | null para tirar a cena, ...], "gancho_tipo": ..., "texto_gancho": ..., "cumprido": ..., "mod": {"<i>": {...}}}}
#   python3 segunda_passada.py --mostrar <id> ...  -> frases atuais do plano, numeradas
import json, sys, os, re, subprocess, unicodedata
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def n_(t): return unicodedata.normalize('NFKD', str(t).lower()).encode('ascii', 'ignore').decode()
if sys.argv[1] == '--mostrar':
    for id_ in sys.argv[2:]:
        P = json.load(open(f'planos_viral/{id_}.json')); print(f'== {id_} ({P["gancho_tipo"]})')
        for i, c in enumerate(P['cenas']): print(f'  {i} [{c[1]}] {c[2]}')
    sys.exit(0)
L = json.load(open(sys.argv[1]))
for id_, d in L.items():
    p = f'planos_viral/{id_}.json'; P = json.load(open(p)); C = P['cenas']
    says = d['says']; assert len(says) == len(C), f'{id_}: {len(says)} frases para {len(C)} cenas'
    novo = []
    for i, (c, s) in enumerate(zip(C, says)):
        if s is None: continue
        c = list(c); c[2] = s
        mud = dict(c[4]) if len(c) > 4 else {}
        mud.update(d.get('mod', {}).get(str(i), {}))
        na = c[3] if len(c) > 3 else s.split()[0]
        if n_(na) not in n_(s):   # palavra da acao sumiu da frase: pega a palavra mais parecida (mesma raiz) ou a maior
            ws = re.findall(r'[\wÀ-ú]+', s)
            na = max(ws, key=lambda w: (len(os.path.commonprefix([n_(w), n_(c[3] if len(c) > 3 else '')])), len(w)))
        enc = mud.get('encena')
        if enc:
            for ps in enc.get('passos', []):
                if ps.get('na') and n_(ps['na']) not in n_(s): ps['na'] = na
        c = c[:3] + [na, mud]
        novo.append(c)
    P['cenas'] = novo
    for k in ('gancho_tipo', 'texto_gancho'):
        if d.get(k): P[k] = d[k]
    if d.get('cumprido'): P['gancho_cumprido'] = d['cumprido']
    json.dump(P, open(p, 'w'), ensure_ascii=False, indent=1)
    r = subprocess.run(['python3', 'reescrever_viral.py', id_, 'aplicar', p], capture_output=True, text=True).stdout
    for l in r.splitlines():
        if 'ATENCAO' in l: print(id_, l)
    e = subprocess.run(['python3', 'estrutura_viral.py', id_], capture_output=True, text=True).stdout
    m = subprocess.run(['python3', 'mkvideo.py', id_], capture_output=True, text=True).stdout + ''
    risco = re.findall(r'\d+ RISCO.*', m)
    print(f'{id_}: ' + (e.splitlines()[0].replace('ESTRUTURA VIRAL ', '') if e else '?') + ' | ' + ' / '.join(l.strip() for l in e.splitlines() if 'FALHA' in l)[:400] + ' | ' + (risco[-1][:300] if risco else ''))
