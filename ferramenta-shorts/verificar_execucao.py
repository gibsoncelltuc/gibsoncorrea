# VERIFICA A EXECUCAO (ordem do Gibson 19/11): o video faz EXATAMENTE o que a folha 3 catalogou e o cenario que o roteiro pediu?
# uso: python3 verificar_execucao.py [id ...]   (sem id = todos os roteiros)
# 1) ACOES: cada acao da folha 3 com instante (palavra) precisa ter a instrucao de animacao no spec.js NAQUELA palavra (WS(n)).
# 2) CENARIO: cada "set" / "interior" / "hora" pedido no roteiro (beats.json) precisa estar na cena correspondente do spec.js.
# Isso confere a PROGRAMACAO; se aparece bem na TELA quem confere e' a grade de acoes (./prechecar.sh <id> acoes) + o olho.
import json, re, sys, glob, os, unicodedata
nrm = lambda t: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode())
_SRC = open('mkvideo.py').read(); _ns = {}
for _nm in ('LUGARES',):
    _i = _SRC.index(_nm + ' = ['); _j = _SRC.index('\n]', _i) + 2; exec(_SRC[_i:_j], {'re': re}, _ns)
LUGARES = _ns['LUGARES']
LUZ = {'noite': ('night', 'study_dark', 'space'), 'espaco': ('space',), 'amanhecer': ('dawn',), 'pordosol': ('dusk',), 'tarde': ('golden',), 'dia': ('day', 'golden', 'study', 'overcast', 'noon', 'storm', 'arctic', 'desert')}   # 25/11: dia nublado/chuva/galpao de luz branca tambem e' dia

def verifica(i):
    sp = f'stories/{i}/spec.js'; f3 = f'stories/{i}/folha3_acao.md'
    if not (os.path.exists(sp) and os.path.exists(f3)): return None
    S = open(sp).read(); B = json.load(open(f'videos/{i}/beats.json')); SET0 = B.get('set', 'countryside')
    A = [int(x) for x in re.findall(r'WS\((\d+), -3\)', re.search(r'const A = \[(.*?)\];', S).group(1))]
    starts = [0] + A
    cenas = {}
    for m in re.finditer(r"S\('(b\d+)[^']*', [^,]+, [^,]+(?:\([^)]*\)[^,]*)?, (X(?:_[a-z]+)?), \"([a-z_]+)\"", S):
        cenas.setdefault(m.group(1), []).append((m.group(2), m.group(3)))
    # 1) acoes
    tot = ok = 0; falhas = []; cena = None
    for l in open(f3):
        m = re.match(r'## Cena b(\d+)', l)
        if m: cena = int(m.group(1)); continue
        r = re.match(r'\| \d+ \| (.+?) \(([\d.]+)s\) \| (.+?) \|', l)
        if not r or cena is None or cena >= len(B['beats']): continue
        w = nrm(r.group(1)); ws = [nrm(x) for x in B['beats'][cena]['say'].split()]
        js = [j for j, x in enumerate(ws) if x == w]
        if not js: continue
        tot += 1; idx = starts[cena] + js[0] if cena < len(starts) else None
        cena_txt = ' '.join(re.findall(rf"S\('b{cena}(?:[_~][^']*)?'.*", S))
        corre_tudo = re.search(r'(sai|corre|chega|anda|foge)', r.group(3)) and re.search(r'pose: "(run|march)"|move: \[\[', cena_txt)   # cena inteira correndo/andando (modo corrida) = acao feita
        if (idx is not None and re.search(rf'WS\({idx}\)|WS\({idx},|WS\({idx}\s*[-+]', S)) or corre_tudo: ok += 1
        else: falhas.append(f'b{cena} "{r.group(1)}" ({r.group(3)[:30]})')
    # 2) cenario
    ctot = cok = 0; cfal = []
    for k, b in enumerate(B['beats']):
        cs = cenas.get(f'b{k}', [])
        if not cs: continue
        if B.get('gancho_tipo') and b.get('bloco') == 'loop' and k == len(B['beats']) - 1:   # 25/11 Selfie: o LOOP copia o cenario da 1a cena (mkvideo); confere contra ela
            b = {**b}; b.pop('set', None); b.pop('interior', None); b.update({k2: B['beats'][0][k2] for k2 in ('set', 'interior') if k2 in B['beats'][0]})
        try: _rl = json.load(open(f'stories/{i}/orquestracao.json'))['cenas'][k]['cenario']
        except Exception: _rl = None
        if b.get('interior') and _rl and not _rl.startswith('interior'):   # 25/11 FILMAGEM CONTINUA: o mkvideo juntou a cena solta ao lugar das vizinhas; vale o cenario real da orquestracao
            b = {**b, 'set': _rl}; b.pop('interior')
        if b.get('interior'):
            ctot += 1; (cok := cok + 1) if any(x == 'X_hall' for x, _ in cs) else cfal.append(f'b{k} interior')
        elif b.get('set'):
            # v13: o cenario REAL da cena vem da orquestracao (o mkvideo troca cenario tematico fora de lugar por locacao limpa; comparar com o beats.json dava falso alarme)
            try:
                _o = json.load(open(f'stories/{i}/orquestracao.json')); _real = _o['cenas'][k]['cenario']; _m = re.search(r'setx: \{ (\w+): X', S); _base = _m.group(1) if _m else SET0
                alvo = 'X' if _real == _base else f"X_{_real}"
            except Exception: alvo = 'X' if b['set'] == SET0 else f"X_{b['set']}"
            (cok := cok + 1) if any(x == alvo for x, _ in cs) else cfal.append(f"b{k} set {b['set']} (veio {cs[0][0]})")
        say_ = re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode())
        if not b.get('interior') and b.get('objetos') is not False and not b.get('veiculo'):   # LUGAR CITADO na narracao (fazenda, igreja, floresta, castelo...) -> cenografia do lugar na cena
            for rx_, itens_ in LUGARES:
                if re.search(rx_, say_) and not re.search(r'(preco|valor|custou)\w* de uma casa|trocad\w* a casa|banco do motorista|conta no banco|dinheiro no banco|casa branca', say_):
                    ctot += 1; bloco_ = ' '.join(re.findall(rf"S\('b{k}(?:[_~][^']*)?'.*", S))
                    (cok := cok + 1) if any(a_ in bloco_ for a_, *_ in itens_) or re.search(r'kit/marco_|kit/white_house|X_hall|kit/room', bloco_) else cfal.append(f'b{k} lugar citado sem cenografia')
                    break
        if b.get('hora') in LUZ:
            ctot += 1; (cok := cok + 1) if any(l_ in LUZ[b['hora']] for _, l_ in cs) else cfal.append(f"b{k} hora {b['hora']} (veio {cs[0][1]})")
    # 3) v9: auditoria anti-falso-positivo (detecta Object.assign sobrescrevendo gests/poses/over)
    if re.search(r'Object\.assign\([^)]*gests:[^)]*\),\s*\{\s*gests:', S):
        falhas.append('CONFLITO: Object.assign sobrescrevendo gests!')
    return tot, ok, falhas, ctot, cok, cfal

ids = sys.argv[1:] or sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob('videos/*/beats.json') if 'teste' not in p)
T = [0] * 4; ruins = []
for i in ids:
    r = verifica(i)
    if not r: continue
    tot, ok, fal, ct, co, cf = r; T[0] += tot; T[1] += ok; T[2] += ct; T[3] += co
    if fal or cf: ruins.append((i, fal, cf))
    print(f'{i:18} acoes {ok:3}/{tot:<3} cenario {co:2}/{ct:<2}' + ('' if not (fal or cf) else '  <- ' + '; '.join((fal + cf)[:4])))
print(f'\nTOTAL: acoes programadas na palavra certa {T[1]}/{T[0]} ({100 * T[1] / max(1, T[0]):.1f}%) | cenario/hora/interior do roteiro {T[3]}/{T[2]} ({100 * T[3] / max(1, T[2]):.1f}%)')
sys.exit(1 if ruins else 0)
