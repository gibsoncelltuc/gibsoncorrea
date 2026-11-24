#!/usr/bin/env python3
# ENQUADRAMENTO NA FONTE (ordem do Gibson 24/11): a folha de producao nao diz so' "submarino na cena" - ela DESCREVE, cena a cena,
# ONDE o objeto fica (fundo atras dos personagens / meio ao lado / frente entre eles), QUANTO da tela ele ocupa, a relacao de tamanho
# com os personagens e para onde a camera mira. E a ferramenta MONTA a cena a partir dessa descricao (posicao, escala e camera calculadas),
# em vez de jogar o objeto e torcer para aparecer. A checagem de visibilidade (visivel.mjs) continua so' como rede de seguranca.
#
# Roda antes do mkvideo (make_video.sh). Grava no beats.json:
#   "quadro": {"objeto", "classe", "lugar", "tela", "relacao", "camera", "motivo"}  (descricao legivel)  + posicao/escala/camera calculadas
# e escreve stories/<id>/folha2_enquadramento.md (a parte da folha 2 que explica ponto a ponto cada cena).
# Cena com "quadro_manual": true e' respeitada (so' descreve, nao recalcula).
import json, re, os, sys, math, struct, ast
ID = sys.argv[1]; P = f'videos/{ID}/beats.json'; B = json.load(open(P)); BT = B['beats']
SRC = open('mkvideo.py', encoding='utf-8').read()
TAM = ast.literal_eval(re.search(r'_TAM_REAL = (\(\(.*?\)\))\s', SRC, re.S).group(1)); KM = 1.35
DECOR = re.compile(r'picket_fence|haybale|scarecrow|bush|rocks|flowerbed|lamppost|bench|wheelbarrow|^barrel$|^crate$|kit/room|kit/porch|tree|cone_transito|barreira|palete|grade_evento|^mk/|kit/cross|kit/grave|tools/lantern|fishing_net')
HEROI = str(B.get('heroi') or '')
TANF = math.tan(math.radians(44 / 2))   # fov vertical padrao das cenas (44 graus)
PERS_H = 2.0                            # altura de um personagem em metros
def dims(a):
    for p in (f'web/assets/library/{a}.glb', f'web/assets/{a}.glb'):
        if not os.path.exists(p): continue
        try:
            d = open(p, 'rb').read(); l = struct.unpack('<I', d[12:16])[0]; j = json.loads(d[20:20 + l]); mn = [1e9] * 3; mx = [-1e9] * 3
            for ac in j.get('accessors', []):
                if len(ac.get('min', [])) == 3: mn = [min(mn[i], ac['min'][i]) for i in range(3)]; mx = [max(mx[i], ac['max'][i]) for i in range(3)]
            if mx[0] > -1e8: return mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2]
        except Exception: pass
    return None
def altura_real(a, s):   # altura e comprimento na tela em metros, com o tamanho real que o mkvideo aplica
    d = dims(a)
    if not d: return None, None, s
    for rx, m, eixo, modo in TAM:
        if re.search(rx, a):
            dim = d[1] if eixo == 'H' else max(d[0], d[2])
            if dim > 0:
                alvo = KM * m / dim
                if (modo == 'min' and s < 0.85 * alvo) or (modo == 'max' and s > 1.2 * alvo): s = alvo
            break
    return d[1] * s, max(d[0], d[2]) * s, s
def num(x): return round(float(x), 1)
linhas = ['# FOLHA 2 - ENQUADRAMENTO CENA A CENA (gerado por enquadrar.py)', '',
          'Para cada cena com objeto da historia: onde ele fica, quanto da tela ocupa, a relacao com os personagens e a mira da camera. A ferramenta monta a cena com estes numeros.', '']
mud = 0
for k, b in enumerate(BT):
    if b.get('explica'): continue
    props = [p for p in (b.get('props') or []) if isinstance(p, list) and p and not DECOR.search(str(p[0]))]
    if not props: continue
    fam = lambda x: re.sub(r'_(red|yellow|purple|striped)$', '', str(x))
    p = next((q for q in props if HEROI and fam(q[0]) == fam(HEROI)), None) or next((q for q in props if re.sub(r'[^a-z]', '', str(q[0]).split('/')[-1])[:5] in re.sub(r'[^a-z]', '', b['say'].lower())), None) or props[0]
    a = str(p[0]); s0 = float(p[3]) if len(p) > 3 else 1.0; ex = p[4] if len(p) > 4 and isinstance(p[4], dict) else {}
    if ex.get('carregado') or ex.get('mover') or b.get('veiculo') or b.get('montado'): continue
    H, L, s = altura_real(a, s0)
    if H is None: continue
    n_p = len(b.get('who') or [])
    grande = max(H, L) > 4.0
    if grande:   # FUNDO: o objeto inteiro atras dos personagens, camera aberta mirando nele
        classe, lugar, tela = 'grande', 'fundo', 0.42
        z = -max(8.0, L * 0.35 + 4.0); x = 0.0
        D_obj = max(H / (2 * TANF * tela), L / (2 * TANF * 0.56 * 1.6)) + 2.0   # cabe na altura (42%) e na largura (vertical 9:16)
        cz = round(z * 0.45, 1); d = max(10.0, D_obj - abs(z - cz)); h = round(min(max(H * 0.35, 2.4), 6.0), 1)
        cena = {'shot': 'wide', 'cx': 0.0, 'cz': cz, 'h': h, 'd0': num(d * 1.05), 'd1': num(d), 'fachada': False, 'crowd': {'n': 0}}   # sem multidao automatica na frente do objeto
        if n_p > 2: b['who'] = b['who'][:2]
        rel = f'objeto com ~{num(H)} m de altura e {num(L)} m de comprimento: fica ATRAS dos personagens, inteiro no quadro; os personagens ficam na frente, menores (~{int(100 * PERS_H / (2 * TANF * (d + cz - 0.6)))}% da tela)'
        cam = f'plano aberto mirando o objeto (alvo z {cz}, distancia {num(d)} m), sem multidao na frente'
    elif max(H, L) > 1.0:   # MEIO: ao lado dos personagens, no mesmo plano
        classe, lugar, tela = 'medio', 'meio', 0.32
        x = 2.4 if n_p <= 1 else 0.0; z = -1.2 if n_p > 1 else 0.2
        d = max(8.0 if n_p <= 1 else 11.5, min(22.0, max(H, PERS_H) / (2 * TANF * 0.62)))   # 2+ personagens + objeto: distancia para caber todos sem cortar a borda
        cena = {'cx': round(x * 0.5, 1), 'cz': round(z * 0.5, 1), 'd0': num(d * 1.05), 'd1': num(d)}
        rel = f'objeto com ~{num(H)} m: fica {"ao lado do personagem" if n_p <= 1 else "entre e um pouco atras dos personagens"}, mesmo plano, tamanho comparavel a uma pessoa'
        cam = f'plano medio enquadrando personagens e objeto juntos (distancia {num(d)} m)'
    else:   # FRENTE: objeto pequeno na frente, entre os personagens, ampliado para ser lido
        classe, lugar = 'pequeno', 'frente'
        alvo_h = 0.75 if HEROI and fam(a) == fam(HEROI) else 0.55
        if H < alvo_h: s = s * alvo_h / H; H = alvo_h
        tela = round(H / (2 * TANF * 9.0), 2); x = 0.0 if n_p != 1 else 1.0; z = 1.0
        cena = {}
        rel = f'objeto pequeno ampliado para ~{num(H)} m (le de longe): fica NA FRENTE, entre os personagens, sem tapar o rosto de ninguem'
        cam = 'plano medio dos personagens com o objeto no centro de baixo do quadro'
    q = {'objeto': a, 'classe': classe, 'lugar': lugar, 'tela': f'{int(tela * 100)}% da altura da tela', 'relacao': rel, 'camera': cam}
    if not b.get('quadro_manual'):
        np_ = [a, num(x), num(z), round(s, 2), {**{kk: vv for kk, vv in ex.items() if kk not in ('fixo',)}, 'fixo': True}]
        b['props'] = [np_ if q_ is p else q_ for q_ in b['props']]
        for kk in ('cx', 'cz', 'h', 'd0', 'd1', '_auto_vis', '_who_lado'): b.pop(kk, None)
        b.update(cena)
        if lugar == 'fundo': b['detalhe'] = False   # objeto grande no fundo: sem close que corte o casco
        mud += 1
    b['quadro'] = q
    linhas += [f'## b{k}: "{b["say"]}"', f'- objeto: {a} ({classe})', f'- lugar: {lugar.upper()}', f'- tamanho na tela: {q["tela"]}', f'- relacao com os personagens: {rel}', f'- camera: {cam}', '']
json.dump(B, open(P, 'w'), ensure_ascii=False, indent=1)
os.makedirs(f'stories/{ID}', exist_ok=True); open(f'stories/{ID}/folha2_enquadramento.md', 'w').write('\n'.join(linhas) + '\n')
print(f'ENQUADRAMENTO: {mud} cena(s) montadas a partir da descricao -> stories/{ID}/folha2_enquadramento.md')
