#!/usr/bin/env python3
# FICHA DE CENA NA FONTE (ordem do Gibson 24/11): a folha de producao nao diz so' "submarino na cena". Para CADA cena ela descreve,
# ponto a ponto, tudo o que a ferramenta precisa para montar a animacao sem "adivinhar":
#   LOCAL (onde: cais, praia, gelo, sala...; hora; clima) | CAMERA (tipo de plano, altura, distancia, mira)
#   PERSONAGENS (quem, posicao esquerda/centro/direita, expressao, acao) | OBJETOS (cada um: lugar fundo/meio/frente e lado,
#   tamanho real e na tela, relacao com os personagens, ESTADO parado/chegando/indo embora) | EFEITOS (tipo, onde acontece, quando)
#   | TEXTO NA TELA (o que, onde, em que palavra).
# E a cena e' MONTADA com esses numeros (posicao, escala, movimento e camera calculados pelo tamanho real de cada modelo 3D).
# Os "olhos" (visivel.mjs) depois medem na tela se o que a ficha planejou apareceu (lugar e tamanho) - se nao, a cena volta.
# Roda antes do mkvideo (make_video.sh). Grava "quadro" em cada cena do beats.json e escreve stories/<id>/folha2_enquadramento.md.
# Cena com "quadro_manual": true: so' descreve, nao recalcula.
import json, re, os, sys, math, struct, ast, unicodedata
ID = sys.argv[1]; P = f'videos/{ID}/beats.json'; B = json.load(open(P)); BT = B['beats']
SRC = open('mkvideo.py', encoding='utf-8').read()
TAM = ast.literal_eval(re.search(r'_TAM_REAL = (\(\(.*?\)\))\s', SRC, re.S).group(1)); KM = 1.35
DECOR = re.compile(r'picket_fence|haybale|scarecrow|bush|rocks|flowerbed|lamppost|bench|wheelbarrow|^barrel$|^crate$|kit/room|kit/porch|tree|cone_transito|barreira|palete|grade_evento|^mk/|tools/lantern|fishing_net')
VEIC = re.compile(r'navio|ship|boat|barco|submarino|vehicles/|aviao|airplane|tanque|tank|trem|locomotiv|carro|car_|truck|caminh|helicop|balloon|balao|roadster|onibus')
HEROI = str(B.get('heroi') or ''); SET0 = B.get('set', 'countryside'); OUT = B.get('outfits', {})
TANF = math.tan(math.radians(44 / 2)); PERS_H = 2.0
n_ = lambda s: unicodedata.normalize('NFD', str(s).lower()).encode('ascii', 'ignore').decode()
fam = lambda x: re.sub(r'_(red|yellow|purple|striped)$', '', str(x))
LOCAL = {'harbor': 'cais de madeira na beira do mar (agua e horizonte ao fundo)', 'arctic': 'campo de gelo e neve (mar congelado, rochas)', 'countryside': 'vila rural (casas, cercas, campo)',
         'street': 'rua de cidade (predios dos dois lados)', 'jungle': 'mata tropical (arvores, cabanas)', 'palace': 'praia / palacio', 'mountain': 'encosta de montanha', 'medieval': 'vila medieval',
         'hall': 'salao', 'stadium': 'estadio', 'outback': 'fazenda aberta', 'desert': 'deserto'}
INTER = {'madeira': 'sala de madeira', 'pedra': 'sala de pedra (governo/castelo)', 'loja': 'loja / taverna', 'galpao': 'galpao', 'hospital': 'hospital'}
PLANO = {'two': 'plano medio, 2 personagens de corpo inteiro', 'wide': 'plano aberto (cenario inteiro)', 'close': 'close (rosto e ombros)', 'group': 'plano de grupo (3+ pessoas)', 'crowd': 'plano de multidao',
         'low': 'camera baixa olhando para cima', 'reveal': 'revelacao (camera sobe e abre)', 'track': 'travelling (camera acompanha andando)', 'prop': 'plano do objeto'}
FXD = {'burst': 'clarao/explosao', 'dust': 'poeira nos pes', 'puff': 'nuvem de fumaca nos pes', 'stars': 'estrelinhas sobre a cabeca (susto/tontura)', 'ring': 'anel de impacto', 'splash': 'respingo', 'creak': 'rangido'}
FXL = {'burst': 'na frente, na altura do peito do 1o personagem', 'dust': 'no chao, aos pes', 'puff': 'no chao, aos pes', 'stars': 'acima da cabeca', 'ring': 'acima da cabeca', 'splash': 'no chao', 'creak': '-'}
CHEGA = r'\b(cheg\w*|aproxim\w*|navegav\w*|avanc\w*|apareceu|apareceram|desembarc\w*|invadi\w*|atac\w*)\b'
SAI = r'\b(foi embora|foram embora|partiu|partiram|fugiu|fugiram|levaram embora|zarp\w*|se afast\w*|retir\w*)\b'
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
def real(a, s):   # altura e comprimento em metros com o tamanho real que o mkvideo aplica
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
def lado(x): return 'centro' if abs(x) < 1.2 else ('direita' if x > 0 else 'esquerda')
linhas = ['# FOLHA 2 - FICHA DE CENA (gerada por enquadrar.py; a ferramenta monta cada cena com estes dados)', '',
          'Cada cena: LOCAL, CAMERA, PERSONAGENS, OBJETOS (lugar, tamanho real e na tela, estado), EFEITOS e TEXTO. Os olhos da ferramenta conferem na tela se o planejado apareceu.', '']
mud = 0
for k, b in enumerate(BT):
    say = b.get('say', ''); t = n_(say)
    linhas.append(f'## b{k}: "{say}"')
    if b.get('explica'):
        e = b['explica'] if isinstance(b['explica'], dict) else {}
        linhas += ['- LOCAL: estudio de explicacao (fundo azul quadriculado, sem personagens)', f'- OBJETO: {e.get("objeto", HEROI)} no centro, manobra "{e.get("manobra", "parado")}"', f'- PASSOS NA TELA: {" -> ".join(e.get("passos", [])) or "-"}', '']
        continue
    who = [str(w).split(':') for w in (b.get('who') or [])]; n_p = len(who)
    objs = [p for p in (b.get('props') or []) if isinstance(p, list) and p and not DECOR.search(str(p[0]))]
    principal = next((q for q in objs if HEROI and fam(q[0]) == fam(HEROI)), None) or next((q for q in objs if re.sub(r'[^a-z]', '', str(q[0]).split('/')[-1])[:5] in re.sub(r'[^a-z]', '', t)), None) or (objs[0] if objs else None)
    fichas = []; cena = {}; plano_extra = None
    manual = b.get('quadro_manual') or b.get('veiculo') or b.get('montado')
    usados_x = []
    for p in sorted(objs, key=lambda q: q is not principal):
        a = str(p[0]); s0 = float(p[3]) if len(p) > 3 else 1.0; ex = dict(p[4]) if len(p) > 4 and isinstance(p[4], dict) else {}
        if ex.get('carregado'): fichas.append((a, 'na mao do personagem', '-', 'carregado', None)); continue
        H, L, s = real(a, s0)
        if H is None: fichas.append((a, 'sem medida (modelo nao encontrado)', '-', 'parado', None)); continue
        eh_p = p is principal; grande = max(H, L) > 4.0; medio = not grande and max(H, L) > 1.0
        estado = 'parado'
        if VEIC.search(a) and re.search(CHEGA, t): estado = 'chegando'
        elif VEIC.search(a) and re.search(SAI, t): estado = 'indo embora'
        if grande:
            lugar = 'FUNDO'; z = -max(8.0, L * 0.35 + 4.0) - (0 if eh_p else 6.0); x = 0.0 if eh_p else (7.0 if 7.0 not in usados_x else -7.0)
            Hv = H * (0.6 if re.search(r'navio|ship|boat|barco|submarino', a) else 1.0)   # navio/submarino: parte do casco fica dentro d'agua
            tela = 0.30 if eh_p else 0.18   # tela em pe (9:16): objeto comprido aparece de lado, com a ponta podendo sair do quadro; altura visivel ~30%
            if eh_p:
                D_obj = Hv / (2 * TANF * tela) + 2.0; cz = round(z * 0.45, 1); d = max(10.0, D_obj - abs(z - cz)); h = round(min(max(H * 0.35, 2.4), 6.0), 1)
                cena = {'shot': 'wide', 'cx': 0.0, 'cz': cz, 'h': h, 'd0': num(d * 1.05), 'd1': num(d), 'fachada': False, 'crowd': {'n': 0}}
                plano_extra = f'plano aberto mirando o {a.split("/")[-1]} (alvo z {cz}, camera a {num(d)} m, altura {h} m), sem multidao na frente'
            rel = f'{num(H)} m de altura x {num(L)} m: ATRAS dos personagens, de lado, ocupando a largura do quadro (a ponta pode sair da tela); personagens na frente, menores'
        elif medio:
            lugar = 'MEIO'; x = (2.4 if n_p <= 1 else 0.0) if eh_p else (3.6 if 3.6 not in usados_x else -3.6); z = (-1.2 if n_p > 1 else 0.2) if eh_p else -2.0
            tela = 0.32
            if eh_p:
                d = max(8.0 if n_p <= 1 else 11.5, min(22.0, max(H, PERS_H) / (2 * TANF * 0.62))); cena = {'cx': round(x * 0.5, 1), 'cz': round(z * 0.5, 1), 'd0': num(d * 1.05), 'd1': num(d)}
                plano_extra = f'plano medio enquadrando personagens e {a.split("/")[-1]} juntos (camera a {num(d)} m)'
            rel = f'{num(H)} m: {"ao lado do personagem" if n_p <= 1 else "entre e um pouco atras dos personagens"}, mesmo plano, tamanho de uma pessoa'
        else:
            lugar = 'FRENTE'; alvo_h = 0.75 if HEROI and fam(a) == fam(HEROI) else 0.55
            if H < alvo_h: s = s * alvo_h / H; H = alvo_h
            x = (0.0 if n_p != 1 else 1.0) if eh_p else (-1.6 if -1.6 not in usados_x else 1.6); z = 1.0 if eh_p else 0.8; tela = round(H / (2 * TANF * 9.0), 2)
            rel = f'objeto pequeno ampliado para {num(H)} m (le de longe): NA FRENTE, {"entre os personagens" if eh_p else "ao lado"}, sem tapar rosto'
        usados_x.append(x)
        if estado == 'chegando': ex['mover'] = [num(x), num(z)]; x0, z0 = x - 16.0, z
        elif estado == 'indo embora': ex['mover'] = [num(x + 16.0), num(z)]; x0, z0 = x, z
        else: ex.pop('mover', None); x0, z0 = x, z
        if not manual:
            novo = [a, num(x0), num(z0), round(s, 2), {**{kk: vv for kk, vv in ex.items() if kk != 'fixo'}, 'fixo': True}]
            b['props'] = [novo if q_ is p else q_ for q_ in b['props']]
        fichas.append((a, f'{lugar}, {lado(x)}{" (objeto principal da cena)" if eh_p else ""}', f'{int(tela * 100)}% da altura da tela', estado, rel))
    if not manual and principal is not None:
        for kk in ('cx', 'cz', 'h', 'd0', 'd1', '_auto_vis', '_who_lado'): b.pop(kk, None)
        b.update(cena)
        if cena.get('shot') == 'wide': b['detalhe'] = False
        if n_p > 1 and cena.get('shot') == 'wide': b['who'] = b['who'][:1]; who = who[:1]; n_p = 1   # cena do objeto grande: 1 personagem no centro olhando (os angulos variados da camera cortavam o 2o na borda)
        mud += 1
    # ---- descricao completa da cena ----
    loc = INTER.get(b.get('interior'), str(b.get('interior'))) if b.get('interior') else LOCAL.get(b.get('set', SET0), str(b.get('set', SET0)))
    hora = b.get('hora') or b.get('light') or B.get('light', 'dia'); clima = b.get('clima', '')
    shot = b.get('shot', 'two')
    pos = ['centro'] if n_p == 1 else ['esquerda', 'direita'] if n_p == 2 else ['esquerda', 'centro', 'direita'] + ['fundo'] * 8
    pers = '; '.join(f'{w[0]}{" (" + OUT.get(w[0], {}).get("profissao", "") + ")" if OUT.get(w[0], {}).get("profissao") else ""} na {pos[i]}, expressao {w[2] if len(w) > 2 else "neutra"}{", segura " + w[3] if len(w) > 3 else ""}' for i, w in enumerate(who)) or 'nenhum'
    cr = b.get('crowd') or {}; multid = f'multidao de {cr.get("n")} ({", ".join(cr.get("outfits") or [])}){" marchando" if cr.get("march") else ""} ATRAS dos principais' if cr.get('n') else 'sem multidao'
    acao = b.get('acao') or b.get('interacao') or ('batalha' if b.get('batalha') else 'fala/gesto')
    linhas += [f'- LOCAL: {loc}; hora: {hora}{"; clima: " + clima if clima else ""}',
               f'- CAMERA: {PLANO.get(shot, shot)}' + (f'; {plano_extra}' if plano_extra else ''),
               f'- PERSONAGENS: {pers}; {multid}; acao: {acao}']
    for a, lg, tl, est, rel in fichas:
        linhas.append(f'- OBJETO {a}: {lg}; tamanho na tela: {tl}; estado: {est.upper()}' + (f'; {rel}' if rel else ''))
    if not fichas: linhas.append('- OBJETOS: so cenario (nenhum objeto da historia nesta cena)')
    for e in b.get('fx', []) or []:
        kd, _, at = str(e).partition('@'); linhas.append(f'- EFEITO {FXD.get(kd, kd)}: {FXL.get(kd, "-")}; entra no quadro +{at or 4} da cena')
    for snd in b.get('sfx', []) or []: linhas.append(f'- SOM: {snd}')
    if b.get('text'): linhas.append(f'- TEXTO NA TELA: "{b["text"]}" {"flutuando no alto" if (b.get("titulo") or shot in ("wide", "crowd", "reveal")) else "numa placa atras dos personagens"}, na palavra {int(b.get("tat", 0)) + 1} da frase')
    if b.get('mapa'): linhas.append(f'- MAPA: {b["mapa"]} (cobre a tela 1-2 s)')
    linhas.append('')
    if fichas: b['quadro'] = {'local': loc, 'camera': PLANO.get(shot, shot) + (f'; {plano_extra}' if plano_extra else ''), 'objetos': [{'objeto': a, 'lugar': lg, 'tela': tl, 'estado': est} for a, lg, tl, est, _ in fichas]}
json.dump(B, open(P, 'w'), ensure_ascii=False, indent=1)
os.makedirs(f'stories/{ID}', exist_ok=True); open(f'stories/{ID}/folha2_enquadramento.md', 'w').write('\n'.join(linhas) + '\n')
print(f'FICHA DE CENA: {len(BT)} cenas descritas, {mud} montadas a partir da ficha -> stories/{ID}/folha2_enquadramento.md')
