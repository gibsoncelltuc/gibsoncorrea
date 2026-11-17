#!/usr/bin/env python3
"""mkvideo.py <id>  -- FICHA DE CENAS (videos/<id>/beats.json) -> stories/<id>/{script.txt, spec.js, cues.py, meta.json}

O roteiro (frases narradas) e a ficha de cenas ficam num arquivo so'.  A ferramenta cuida do resto:
  voz (edge-tts) -> tempos por palavra -> spec.js (planos, camera, atores, textos) -> cues.py (musica + efeitos) -> ajuste de enquadramento -> gates -> render -> QA -> mp4.
Cada "beat" = uma frase narrada + o que aparece na tela durante ela.  Veja videos/_exemplo/beats.json e README.
"""
import json, sys, os, re

ID = sys.argv[1]
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
B = json.load(open(f'videos/{ID}/beats.json', encoding='utf-8'))
os.makedirs(f'stories/{ID}', exist_ok=True)

SET = B.get('set', 'countryside')
LIGHT = B.get('light', 'day')
MOOD = B.get('mood', 'playful')
SETS_X = {'outback': 2000, 'countryside': 1000, 'arctic': 7000, 'palace': 4000, 'harbor': 5000, 'mountain': 3000, 'medieval': 9000, 'jungle': 6000, 'hall': 8000, 'stadium': 11000, 'street': 12000}
SETX = SETS_X.get(SET, 1000) if 'x' not in B else B['x']
_neve = False
for _b in B['beats']:   # NEVE: enquanto estiver nevando, a cena vai para o cenario de neve (chao branco) se o roteiro nao fixar outro
    _t = re.sub(r'[^a-z]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode())
    if _b.get('clima') == 'neve' or re.search(r'neve|nevasca|nevava|nevando|inverno|congel|geada', _t): _neve = True
    elif _b.get('clima') or re.search(r'verao|primavera|calor|degelo|anosdepois|mesesdepois', _t): _neve = False
    if _neve and not _b.get('set') and not _b.get('interior') and 'arctic' in SETS_X and B.get('neve_cenario') is not False: _b['set'] = 'arctic'
for _b in B['beats']:
    if _b.get('interior') and not _b.get('set'): _b['set'] = 'hall'      # interior fica no cenario 'hall' (sem arbusto/pedrinha de area externa)
USED_SETS = [SET] + sorted({b['set'] for b in B['beats'] if b.get('set') and b['set'] != SET and b['set'] in SETS_X})   # cenario por cena: "set" dentro do beat
beats = B['beats']

# ---------- script.txt (uma frase por linha) ----------
with open(f'stories/{ID}/script.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(b['say'].strip() for b in beats) + '\n')
json.dump({'id': ID, 'title': B.get('title', ID), 'voice': B.get('voice', 'pt-BR-AntonioNeural'), 'rate': B.get('rate', '+10%'),
           'file': re.sub(r'[^A-Za-z0-9]+', '-', __import__('unicodedata').normalize('NFKD', B.get('title', ID)).encode('ascii', 'ignore').decode()).strip('-')},
          open(f'stories/{ID}/meta.json', 'w'), ensure_ascii=False)

# ---------- indices de palavras ----------
starts = []; n = 0
for b in beats:
    starts.append(n); n += len(b['say'].split())

# ---------- figurinos ----------
SKINS = ['#ffe2c2', '#f5c9a0', '#ecd0b6', '#c99067']
outfits_js = []
for name, o in B.get('outfits', {}).items():
    o = dict(o); mo = o.pop('moustache_on', None)
    hats = o.pop('hats', None); hairs = o.pop('hairs', None)   # "hats": [...] -> chapeu diferente por variante; sem chapeu -> cor/corte de cabelo por variante
    body = ', '.join(f'{k}: {json.dumps(v)}' for k, v in o.items())
    mou = f", ...(v % 2 ? {{ moustache: {json.dumps(mo)} }} : {{}})" if mo else ''
    hv = (f", hat: {json.dumps(hats)}[v % {len(hats)}]" if hats else '') + ('' if (hats or o.get('hat')) else f", hat: 'hair', hair: {json.dumps(hairs or ['#5a3b2a', '#2a2018', '#b8862f', '#8a8a86', '#7a3a1c'])}[v % {len(hairs or [1]*5)}], hairStyle: [null, null, 'long', null, 'bun'][v % 5]")
    outfits_js.append(f"{name}: (v = 0, e = {{}}) => ({{ _id: {json.dumps(name.lower())}, {body}, skin: {json.dumps(SKINS)}[v % 4]{hv}{mou}, ...(v % 7 === 4 ? {{ glasses: true }} : {{}}), ...(v % 7 === 5 || v % 7 === 6 ? {{ beard: ['#3a2a1f', '#6b4a2a', '#8a8a86'][v % 3] }} : {{}}), ...e }})")

# ---------- posicoes automaticas ----------
def slots(n):
    base = {1: [0.0], 2: [-1.15, 1.15], 3: [-2.1, 0.0, 2.1], 4: [-3.0, -1.0, 1.0, 3.0], 5: [-3.6, -1.8, 0, 1.8, 3.6], 6: [-3.8, -2.3, -0.8, 0.8, 2.3, 3.8]}
    if n in base: return base[n]
    return [(i - (n - 1) / 2) * 1.6 for i in range(n)]
ZS = [1.3, 1.0, 1.6, 1.1, 1.7, 1.4]   # no plano de foco da camera (antes 2.0-3.0: com a camera mais perto, alguem ficava colado na lente)
ZSW = [-0.4, 0.2, -0.8, 0.0, -0.2, 0.4]

TEMPL = {  # h = altura do alvo; d0/d1 = distancia da camera no inicio/fim; el = elevacao; fov
    'wide':  dict(h=2.4, d0=20, d1=16, el=5, fov=46),   # camera na altura do personagem (canal: 0,8x), nao de cima
    'two':   dict(h=2.3, d0=8.4, d1=7.4),
    'close': dict(h=2.4, d0=5.6, d1=4.9),
    'group': dict(h=2.5, d0=10.0, d1=8.8),
    'prop':  dict(h=1.4, d0=8.0, d1=6.0, el=8),
    'crowd': dict(h=2.4, d0=16.0, d1=12.5, el=6),
    'track': dict(h=2.2, d0=8.0, d1=8.0, el=3, fov=44),
    'low':   dict(h=1.6, d0=8.2, d1=7.2, el=2),
    'reveal': dict(h=2.4, d0=10.0, d1=22.0, el=6, fov=46),   # recua e revela o exercito inteiro
    'orbit':  dict(h=2.4, d0=19.0, d1=16.0, el=6, fov=46, az0=-38, az1=32),   # panoramica aberta em arco
}
WIDE = ('wide', 'crowd', 'reveal', 'orbit')
TXT = {'blue': ('#fff6e0', '#27408b'), 'brown': ('#fff6e0', '#7a3a1c'), 'red': ('#d8282f', '#fff6e0'), 'gold': ('#e8c45a', '#7a1c1c'), 'white': ('#ffffff', '#1c2a4a')}
TXT_CYCLE = ['brown', 'blue', 'red', 'gold']

def num(x): return json.dumps(round(x, 3))


import unicodedata
def nrm(t): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode())
MASS = re.compile(r'infantaria|batalh|exercito|soldados|milhares|dezenas|tropas|acampamento|regimento|multidao|todomundo|artilharia|canhoes|campocheio|panico|marcha|esquadrao|legiao|frota|armada|invasao|invadiu')
ARRIVE = re.compile(r'chegou|chegaram|apareceu|surgiu|avancou|avancaram|marchava|marcharam|invadiu|invadiram|desembarcou|cercou|cercaram')
CLOSE_OK = re.compile(r'gritou|olhou|sorriu|chorou|pensou|disse|perguntou|riu|ordenou')
KW = [  # (regex da palavra, efeito, golpe de camera) -- animacao nas palavras-chave da narracao
    (re.compile(r'^(tiro|tiros|disparou|dispararam|disparo|disparos|atirava|atiravam|atirou|atiraram|atirar|explodiu|explodiram|explosao|canhoes|canhao|fogo|bomba|bombas|metralhadora|metralhadoras|balas|bala|artilharia)$'), 'burst', 0.09),
    (re.compile(r'^(gritou|gritaram|socorro|ataque|atacar|atacaram|alarme)$'), 'ring', 0.06),
    (re.compile(r'^(panico|correu|correram|fugiu|fugiram|correria|debandada|fuga|retirada|recuou|recuaram|bateu|marchando|marchava|marcharam|perder)$'), 'dust', 0.07),
    (re.compile(r'^(festa|beberam|brindou|brindaram|comemoraram|venceu|venceram|ganhou|ganharam|vitoria|compraram|comprou|comprando|vendendo|vendeu|venderam|vender|dancar|dancou|dancando|danca|dancarinos|musica|musicos|rindo|riso|roubaram|roubou)$'), 'stars', 0.0),
    (re.compile(r'^(empurra|empurrouse|briga|brigar|brigaram|discussao|confusao|caos|desastre)$'), 'puff', 0.05),
    (re.compile(r'^(chegou|chegaram|apareceu|surgiu|invadiu|desabou|caiu|cairam|quebrou|quebraram|derrubou|afundou|tombou)$'), 'dust', 0.04),
    (re.compile(r'^(riu|riram|risada|gargalhou|gargalhada|gargalhadas|dinheiro|ouro|moedas|recompensa|pagou|pagar|pagaram|fortuna|premio|sino|tocou|tocar)$'), 'stars', 0.0),
    (re.compile(r'^(morreu|morreram|morto|mortos|baixas|derrota|derrotado|perdeu|perderam|desistiu|fracasso|faliu)$'), 'puff', 0.03),
    (re.compile(r'^(descobriu|descobriram|percebeu|perceberam|surpresa|segredo|impossivel|proibido|ilegal|absurdo)$'), 'ring', 0.03),
    (re.compile(r'^(incendio|incendiou|queimou|queimaram|chamas|pegou fogo)$'), 'burst', 0.06),
]
PLANO = []   # plano de acao por cena: o que o roteiro pede x o que o video mostra e toca (gravado em stories/<id>/plano.md)
IMPACT = re.compile(r'mirav|miraram|guerra|combate|tiro|atir|dispar|metralhador|canho|explod|explos|batalha|atacou|atacaram|ataque|fugi|fugir|correndo|correram|debandada|espalha|panico|invadi|carga|bombard')
SHOOT = re.compile(r'tiro|atir|dispar|metralhador|canho|balas|bombard')
def direct(beats):
    """DIRETOR AUTOMATICO: planos abertos, multidao e ritmo de camera. 'shot_lock': true no beat desliga; 'director': false no arquivo desliga tudo."""
    if B.get('director') is False: return
    run = 0; wide_n = 0; wrun = 0; impact_n = 0
    outs = list(B.get('outfits', {}))
    for k, b in enumerate(beats):
        if b.get('shot_lock'):
            run = 0 if b.get('shot', 'two') in WIDE else run + 1; continue
        if b.get('interior'):   # dentro de casa: sempre plano medio, sem multidao automatica
            b['shot'] = b.get('shot') if b.get('shot') in ('two', 'close', 'group', 'low') else 'two'; run += 1; wrun = 0; continue
        say = nrm(b['say']); words = [nrm(w) for w in b['say'].split()]
        mass = bool(MASS.search(say)); arrive = bool(ARRIVE.search(say))
        shot = b.get('shot', 'two'); first = (k == 0); last = (k == len(beats) - 1)
        if first: shot = shot if shot in ('two', 'close', 'group', 'low', 'track') else ('group' if len(b.get('who', [])) > 2 else 'two')   # MODO RICKS: abre em plano medio/fechado (18 de 20 videos do canal)
        elif mass and arrive: shot = 'reveal'
        elif mass: shot = 'orbit' if wide_n % 2 else 'crowd'
        elif last: shot = 'two'   # e termina em plano medio (16 de 20)
        elif run >= 4 and not CLOSE_OK.search(say): shot = 'orbit' if wide_n % 2 else 'wide'
        if shot in WIDE and not b.get('impact') and (wrun >= 2 or (wrun >= 1 and k == len(beats) - 2)) and not (first or last):   # nunca mais de 2 planos abertos seguidos: alterna com plano medio + multidao ao fundo
            shot = 'group' if mass else 'two'
        if b.get('batalha') or (not (first or last) and IMPACT.search(say) and impact_n < int(B.get('max_impact', 2)) and b.get('impact') is not False):
            impact_n += 1; b['impact'] = True; shot = ('crowd' if impact_n % 2 else 'orbit') if (b.get('batalha') or wrun < 1) else 'group'   # batalha marcada SEMPRE abre; impacto logo depois de outro aberto fica em plano medio com a tropa atras
            if wrun >= 1 and k > 0 and not beats[k - 1].get('impact') and not beats[k - 1].get('shot_lock') and k - 1 > 0: beats[k - 1]['shot'] = 'group'; wide_n -= 1; wrun = 0   # o aberto anterior (sem batalha) cede a vez   # dois abertos seguidos nao: o segundo fica em plano medio com a tropa atras   # MOMENTO-CHAVE: plano aberto de alto impacto (fora da cota de planos abertos)
        elif shot in WIDE and not (first or last) and wide_n >= int(B.get('max_wide', 2)): shot = 'group'   # MODO RICKS: personagem grande na maior parte do video
        wrun = wrun + 1 if shot in WIDE else 0
        b['shot'] = shot
        if shot in WIDE:
            wide_n += 1; run = 0
            if not b.get('crowd'):
                persons_out = [w.split(':')[0] for w in b.get('who', [])]
                army = persons_out[0] if persons_out else (outs[0] if outs else 'X')
                b['crowd'] = {'n': (12 if b.get('impact') else 5) if b.get('emus') else (18 if (b.get('impact') or (mass and (arrive or first))) else 10 if mass else 6), 'outfits': list(dict.fromkeys(persons_out + [army])), 'march': bool(arrive or first or (shot == 'reveal' and mass)) and not (b.get('impact') and SHOOT.search(say))}
            if not b.get('who'): b['who'] = [f"{b['crowd']['outfits'][0]}:0:neutral"]
        else:
            run += 1
            if b.get('impact') and not b.get('crowd') and b.get('who') and not b.get('emus'):
                b['crowd'] = {'n': 10, 'outfits': list(dict.fromkeys(w.split(':')[0] for w in b['who'])), 'march': False, 'expr': 'shock'}
            if mass and not b.get('crowd') and b.get('who') and not b.get('emus'):
                persons_out = [w.split(':')[0] for w in b['who']]
                b['crowd'] = {'n': 5, 'outfits': list(dict.fromkeys(persons_out)), 'march': False, 'expr': 'shock' if re.search('panico|tiro|gritou', say) else 'neutral'}

KICKS = []
AMB = {}
STATE = {}
KWSFX = []
direct(beats)
if B.get('director') is not False and not any(b.get('impact') for b in beats) and len(beats) > 4:
    _b = beats[int(len(beats) * 0.6)]
    if not _b.get('shot_lock'): _b['impact'] = True; _b['shot'] = 'orbit'; _b.setdefault('crowd', {'n': 12, 'outfits': [w.split(':')[0] for w in _b.get('who', [])] or list(B.get('outfits', {'X': 0}))[:1], 'march': False})
# RITMO DE FILMAGEM DO CANAL (pela funcao de cada cena na historia): gancho em plano medio na acao -> cena 2 ABRE para situar o lugar ->
# falas em plano mais fechado no personagem -> virada ("Acontece que") abre ou baixa a camera -> final fecha no rosto.
if B.get('director') is not False and B.get('ritmo') is not False and len(beats) >= 6:
    _lock = lambda _b: _b.get('shot_lock') or _b.get('interior') or _b.get('veiculo') or _b.get('impact') or _b.get('batalha')
    _nw = lambda: sum(1 for _b in beats if _b.get('shot') in WIDE)
    _b = beats[1]                                           # cena 2 = contexto: plano aberto de ambientacao (camera abrindo)
    if not _lock(_b) and _b.get('shot') not in WIDE and beats[2].get('shot') not in WIDE:
        _b['shot'] = 'reveal'; _b['aberto_auto'] = True
        if not _b.get('emus'): _b.setdefault('crowd', {'n': 8, 'outfits': list(dict.fromkeys([w.split(':')[0] for w in _b.get('who', [])] or list(B.get('outfits', {'X': 0}))[:1])), 'march': False})
    for _i, _b in enumerate(beats[2:-1], 2):
        _t = nrm(_b['say'])
        if _lock(_b) or _b.get('shot') in WIDE: continue
        if '"' in _b['say'] and len(_b.get('who', [])) <= 2: _b['perto'] = 0.84                      # fala: camera mais perto de quem fala
        elif re.match(r'aconteceque|naverdade|soque|oproblema', _t) and beats[_i - 1].get('shot') not in WIDE: _b['shot'] = 'low'; _b['perto'] = 0.92   # virada: camera baixa, dramatica
    _b = beats[-1]
    if not _lock(_b) and len(_b.get('who', [])) <= 1: _b['shot'] = 'close'                             # final: fecha no rosto
# REGRA RESTRITA (pedido do Gibson): TODO video tem no minimo 2 planos abertos de camera continua (ambientacao ampla: tropa, paisagem, batalha).
MIN_WIDE = int(B.get('min_wide', 2))
if B.get('director') is not False and len(beats) >= 5:
    _w = [i for i, _b in enumerate(beats) if _b.get('shot') in WIDE]
    _cand = sorted((i for i in range(1, len(beats) - 1) if i not in _w and not beats[i].get('shot_lock') and not beats[i].get('interior') and not beats[i].get('veiculo')), key=lambda i: (min(abs(i - j) for j in _w) if _w else 9, -abs(i - len(beats) * (0.35 if not _w else 0.7))), reverse=True)
    while len(_w) < MIN_WIDE and _cand:
        i = _cand.pop(0)
        if any(abs(i - j) <= 1 for j in _w) and _cand: continue
        _b = beats[i]; _b['shot'] = 'reveal' if len(_w) % 2 == 0 else 'orbit'; _b['aberto_auto'] = True
        _o = [w.split(':')[0] for w in _b.get('who', [])] or list(B.get('outfits', {'X': 0}))[:1]
        if not _b.get('emus'): _b.setdefault('crowd', {'n': 8, 'outfits': list(dict.fromkeys(_o)), 'march': False})
        _w.append(i)
    if len(_w) < MIN_WIDE: print(f'AVISO: so {len(_w)} plano(s) aberto(s); a regra pede {MIN_WIDE}. Tire shot_lock/interior de alguma cena.')


def build_beat(k, b):
    shot = b.get('shot', 'two'); T = dict(TEMPL.get(shot, TEMPL['two']))
    if b.get('impact') and shot in WIDE and b.get('caminhoes'): T.update(d0=13.0, d1=31.0, el=11, h=2.6); T.pop('az0', None); T.pop('az1', None)   # comeca na tropa subindo nos caminhoes e ABRE para a fazenda inteira
    elif b.get('impact') and shot in WIDE: T.update(d0=25.0, d1=19.0, el=11, h=2.6)   # BATALHA: visao ampla de verdade (cenario, tropa inteira, inimigo fugindo ao fundo)
    elif shot == 'reveal': T.update(d0=11.0, d1=27.0, el=10)
    if b.get('perto') and shot in ('two', 'group', 'low', 'close'): T['d0'] *= b['perto']; T['d1'] *= b['perto'] * 0.94
    _n = len(b.get('who', []))
    if shot in ('two', 'group', 'low') and _n >= 3: T['d0'] *= 1 + 0.13 * (_n - 2); T['d1'] *= 1 + 0.13 * (_n - 2)   # 3+ pessoas: abre o suficiente para caber todo mundo
    light = b.get('light')
    _sy = nrm(b['say']); global AMB
    # HORA DO DIA e CLIMA: campos "hora" (dia|tarde|pordosol|noite|amanhecer) e "clima" (sol|calor|chuva|tempestade|neve|neblina|vento|limpo), ou pelas palavras da narracao. Ficam valendo ate mudar.
    _h = b.get('hora') or ('noite' if re.search(r'noite|noescuro|madrugada|meianoite', _sy) else 'amanhecer' if re.search(r'amanhecer|manhaseguinte|nascerdosol|aurora|demanha', _sy) else 'pordosol' if re.search(r'pordosol|entardecer|anoitecer|fimdetarde|finaldetarde|fimdodia', _sy) else 'tarde' if re.search(r'atarde|detarde|natarde', _sy) else 'dia' if re.search(r'diaseguinte|diasdepois|semanasdepois|mesesdepois|anosdepois|meiodia|duranteodia', _sy) else None)
    _c = b.get('clima') or ('tempestade' if re.search(r'tempestade|temporal|trovao|raios', _sy) else 'chuva' if re.search(r'chuva|chovia|chovendo|choveu|aguaceiro', _sy) else 'neve' if re.search(r'neve|nevasca|nevava|nevando|inverno|congel|geada', _sy) else 'neblina' if re.search(r'neblina|nevoeiro|nevoa|cerracao', _sy) else 'calor' if re.search(r'calor|solforte|solquente|escaldante|seca|sedeinsuport', _sy) else 'vento' if re.search(r'ventania|vendaval|furacao|ventoforte', _sy) else None)
    if _h: AMB['hora'] = _h
    if _c: AMB['clima'] = None if _c in ('limpo', 'sol') else _c
    wx = {}
    if not light:
        light = {'noite': 'night', 'amanhecer': 'dawn', 'pordosol': 'dusk', 'tarde': 'golden'}.get(AMB.get('hora'), LIGHT)
        cl = AMB.get('clima')
        if cl in ('chuva', 'tempestade') and light != 'night': light = 'storm' if cl == 'tempestade' else 'overcast'
        elif cl == 'neve' and light not in ('night', 'dusk', 'dawn'): light = 'arctic'
        elif cl == 'neblina' and light not in ('night',): light = 'overcast'
        elif cl == 'calor' and light not in ('night', 'dusk', 'dawn'): light = 'desert'
    if not b.get('interior'):
        cl = AMB.get('clima')
        wx = {'chuva': {'rain': 0.8, 'wind': 0.8}, 'tempestade': {'rain': 1.0, 'wind': 1.4}, 'neve': {'snow': 0.85, 'wind': 0.5}, 'neblina': {'fog': 0.7, 'wind': 0.3}, 'vento': {'wind': 1.4, 'leaves': 0.7}}.get(cl, {})
    if 'wind' in b: wx['wind'] = b['wind']
    who = b.get('who', []); animals = b.get('animals', []); props = b.get('props', [])
    wide_pre = shot in WIDE
    if b.get('interior') and not b.get('light'): light = 'study'
    mv = b.get('move', 8 if shot == 'track' else 0)
    a, bb = f'A[{k}]', f'A[{k + 1}] - 1'
    # elenco de pessoas
    HOLDS = (('mug', r'beber|bebeu|bebia|brind|caneca|cerveja|cha\b'), ('bottle', r'garrafa|aguardente|vinho|bebida|rum|whisky|uisque'), ('paper', r'carta|jornal|imprensa|ordem|documento|mapa|contrato|telegrama|relatorio|lista|assinou|lei\b'), ('book', r'livro|biblia|diario'), ('lantern', r'lanterna|lampiao|lamparina'), ('torch', r'tocha|incendi'), ('flag', r'bandeira|rendeu|rendicao'), ('coin', r'dinheiro|moeda|ouro|recompensa|pagou|pagar|fortuna|salario|imposto'), ('bag', r'saco|mala|bagagem|sacola'), ('spyglass', r'luneta|avistou|avistaram|procurar|vigia|observ'))
    _say_sp = re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode())
    auto_hold = next((h for h, rx in HOLDS if re.search(rx, _say_sp)), None) if b.get('maos') is not False else None
    _acao = b.get('acao') or ('dancar' if re.search(r'\bdanc', _say_sp) else None)
    _px = ", pose: 'dance', acting: false" if _acao == 'dancar' else ''
    persons = []
    for w in who:
        p = w.split(':'); out = p[0]; v = int(p[1]) if len(p) > 1 and p[1] != '' else 0; ex = (p[2] if len(p) > 2 else '') or 'neutral'; hold = p[3] if len(p) > 3 else None   # 4o campo: objeto na mao
        if hold is None and auto_hold and not persons and not B.get('outfits', {}).get(out, {}).get('rifle'): hold = auto_hold   # o primeiro personagem da cena segura o objeto de que a narracao fala
        persons.append((out, v, ex, hold or None))
    n = len(persons); sl = slots(max(n, 1))
    acts = []
    for i, (out, v, ex, hold) in enumerate(persons):
        ov = f", over: {{ hold: {json.dumps(hold)} }}" if hold else ''
        dx, z = sl[i], (ZSW[i % len(ZSW)] if shot in WIDE else ZS[i % len(ZS)])
        if shot == 'track' or mv:
            d = mv if mv else 8
            acts.append(f"{{ outfit: {json.dumps(out)}, v: {v}, at: [X + {num(dx - d / 2)}, {num(z)}], move: [[X + {num(dx + d / 2)}, {num(z)}], {a}, {bb}, 'lin'], pose: {json.dumps('march' if B.get('outfits', {}).get(out, {}).get('rifle') else 'stroll')}, expr: {json.dumps(ex)}{ov} }}")   # soldado marcha; civil caminha solto
        else:
            acts.append(f"pp(X, {json.dumps(out)}, {v}, {num(dx)}, {num(z)}, {json.dumps(ex)}" + (f", {{ over: {{ hold: {json.dumps(hold)} }}{_px} }})" if hold else (f", {{ {_px[2:]} }})" if _px else ')')))
    # animais
    for j, an in enumerate(animals):
        sp = an[0]; dxa = an[1] if len(an) > 1 else 2.2 + j * 1.8; za = an[2] if len(an) > 2 else 0.6; st = an[3] if len(an) > 3 else 'stand'
        sc = an[4] if len(an) > 4 else {'horse': 0.7, 'bear': 1.0, 'emu': 1.6}.get(sp, 1.0)
        key = 'bird' if sp in ('emu', 'goose', 'duck', 'chicken', 'rooster', 'gull') else 'animal'
        fl = 'true' if dxa > 0 else 'false'
        if mv and key == 'animal' and sp in ('horse', 'bear'):
            acts.append(f"{{ {key}: {json.dumps(sp)}, at: [X + {num(dxa - mv / 2)}, {num(za)}], move: [[X + {num(dxa + mv / 2)}, {num(za)}], {a}, {bb}, 'lin'], state: 'trot', spd: 0.09, s: {num(sc)}, flip: {'false' if mv > 0 else 'true'}, seed: {j * 3 + 1} }}")
        else:
            acts.append(f"{{ {key}: {json.dumps(sp)}, at: [X + {num(dxa)}, {num(za)}], state: {json.dumps(st)}, s: {num(sc)}, flip: {fl}, seed: {j * 3 + 1} }}")
    # bando de emus: "emus": {"n":10, "mode":"stand|run|scatter", "x":3, "z":-1, "cols":4, "dir":1}
    em = b.get('emus'); DUST = []
    if em and b.get('impact'): em = {**em, 'n': max(int(em.get('n', 10)), 26), 'mode': 'scatter'}
    if em:
        import math as _m
        n_e = int(em.get('n', 8)); mode = em.get('mode', 'stand'); cols_e = int(em.get('cols', 4)); ex0 = em.get('x', 3.0); ez0 = em.get('z', -1.0); dr = em.get('dir', 1)
        for i in range(n_e):
            row, col = i // cols_e, i % cols_e
            x0 = ex0 + (col - (cols_e - 1) / 2) * 2.4 + (row % 2) * 1.1; z0 = ez0 - row * 2.6 + ((i * 53) % 7 - 3) * 0.15
            if mode == 'run':
                acts.append(f"{{ bird: 'emu', at: [X + {num(x0 - 11 * dr)}, {num(z0)}], move: [[X + {num(x0 + 11 * dr)}, {num(z0)}], {a}, {bb}, 'lin'], state: 'walk', spd: 0.09, s: 1.6, flip: {'false' if dr > 0 else 'true'}, seed: {i * 5 + 2} }}")
            elif mode == 'scatter':
                ang = (i / max(n_e, 1)) * 2 * _m.pi + 0.4; tx, tz = x0 + 11 * _m.cos(ang), z0 + 6 * _m.sin(ang)
                if b.get('impact'):
                    r1, r2, r3 = ((i * 37) % 17) / 16, ((i * 53) % 13) / 12, ((i * 29) % 11) / 10; sg = 1 if ex0 >= 0 else -1
                    x0, z0 = ex0 + sg * (-3 + 9 * r1), ez0 + (-2 + 9 * r2); ang = 0; tx, tz = x0 + sg * (5 + 9 * r3), z0 - (5 + 11 * r1)   # fogem PARA DENTRO da fazenda (rumo ao trigal e ao celeiro), a tomada inteira   # na frente da cerca, no terreiro, onde a camera ve
                    if i % 3 == 0: DUST.append((x0 + (tx - x0) * 0.4, z0 + (tz - z0) * 0.4, 14 + i * 9))   # na batalha os bichos fogem PARA LONGE da tropa, abrindo em leque
                acts.append(f"{{ bird: 'emu', at: [X + {num(x0)}, {num(z0)}], move: [[X + {num(tx)}, {num(tz)}], {a}, {bb}], state: 'walk', spd: 0.09, s: 1.6, flip: {'true' if tx < x0 else 'false'}, seed: {i * 5 + 2} }}")
            else:
                acts.append(f"{{ bird: 'emu', at: [X + {num(x0)}, {num(z0)}], state: {json.dumps('peck' if (i % 3 == 1 and em.get('peck', True)) else 'stand')}, s: 1.6, flip: {'true' if i % 2 == 0 else 'false'}, seed: {i * 5 + 2} }}")
    # multidao de fundo (varias fileiras, marchando ou parada)
    wide = shot in WIDE; crowd_pos = []
    if b.get('crowd'):
        c = b['crowd']; cnt = int(c.get('n', 8)); outs_c = c.get('outfits') or [c.get('outfit') or (persons[0][0] if persons else list(B.get('outfits', {'X': 0}))[0])]
        cols = 9 if wide else 5
        for i in range(cnt):
            row, col = i // cols, i % cols
            jx = ((i * 37) % 11 - 5) * 0.09; jz = ((i * 53) % 7 - 3) * 0.12
            x0 = (col - (cols - 1) / 2) * (1.9 if wide else 1.7) + (row % 2) * 0.9 + jx + (-6.5 if (b.get('impact') and b.get('emus') and wide) else 0); z0 = (1.2 if wide else -3.0) - row * 2.1 + jz
            out = outs_c[i % len(outs_c)]; ex = c.get('expr', 'neutral' if not c.get('march') else 'stern'); look = (-0.25, 0.25, 0.0, 0.15)[i % 4]
            crowd_pos.append((x0, z0))
            if c.get('march'):
                acts.append(f"{{ outfit: {json.dumps(out)}, v: {i % 4}, at: [X + {num(x0 - 9)}, {num(z0)}], move: [[X + {num(x0 + 3)}, {num(z0)}], {a}, {bb}, 'lin'], pose: 'march', speed: 0.034, expr: {json.dumps(ex)}, seed: {i % 4}, look: {look} }}")
            else:
                acts.append(f"pp(X, {json.dumps(out)}, {i % 4}, {num(x0)}, {num(z0)}, {json.dumps(ex)}, {{ look: {look}, seed: {i % 4 + (i * 3 if _px else 0)}{_px} }})")
    # BATALHA COM CAMINHOES: "caminhoes": 2 -> caminhoes atras da tropa com soldados em pe na carroceria, atirando
    truck_props = []
    if b.get('caminhoes') and b.get('crowd'):
        _oc = (b['crowd'].get('outfits') or [b['crowd'].get('outfit')])[0]
        for t_ in range(int(b['caminhoes'])):
            tx, tz = -9.0 + t_ * 7.5 + (-6.5 if b.get('emus') else 0) + 4.0, -5.6 - (t_ % 2) * 1.2
            truck_props.append(f"{{ asset: {json.dumps(b.get('caminhao', 'vehicles/truck'))}, at: [X + {num(tx)}, {num(tz)}], s: 1.0, ry: 1.5708, drop: false }}")
            for q_, dx_ in enumerate((-1.5, -0.3, 0.9)):
                # os soldados SOBEM na carroceria no comeco da tomada (um depois do outro) e so' entao atiram
                acts.append(f"pp(X, {json.dumps(_oc)}, {q_}, {num(tx + dx_)}, {num(tz + 0.15)}, 'stern', {{ y: (f) => {num(b.get('caminhao_y', 0.95))} * Math.min(1, Math.max(0, (f - ({a}) - {8 + q_ * 9 + t_ * 5}) / 16)), look: 0.3, seed: {q_ + t_ * 3} }})"); crowd_pos.append((tx + dx_, tz))
    # veiculo andando: "veiculo": {"asset":"vehicles/car","de":-9,"para":9,"z":0.6,"s":1.0,"motorista":"FARM:0:smile"}
    pr = list(truck_props)
    vc = b.get('veiculo')
    if vc:
        x0v, x1v, zv = vc.get('de', -9), vc.get('para', 9), vc.get('z', 0.6); ryv = 1.5708 if x1v >= x0v else -1.5708
        sv = vc.get('s', 1.0); dirv = 1 if x1v >= x0v else -1   # veiculo 1.6x: proporcional aos personagens (que tem ~3 m)
        pr.append(f"{{ asset: {json.dumps(vc.get('asset', 'vehicles/car'))}, at: [X + {num(x0v)}, {num(zv)}], move: [[X + {num(x1v)}, {num(zv)}], {a}, {bb}, 'lin'], s: {num(sv)}, bob: 0.03 }}")
        if vc.get('motorista'):   # motorista DENTRO do carro: carta cortada (cabeca e ombros) encostada na janela do lado da camera
            mo_ = vc['motorista'].split(':'); k_ = sv; zd = zv + 0.1 * sv; dxd = -0.45 * sv * dirv   # sentado no banco, dentro da cabine aberta
            acts.append(f"{{ outfit: {json.dumps(mo_[0])}, v: {int(mo_[1]) if len(mo_) > 1 and mo_[1] else 0}, at: [X + {num(x0v + dxd)}, {num(zd)}], move: [[X + {num(x1v + dxd)}, {num(zd)}], {a}, {bb}, 'lin'], pose: 'stand', acting: 'low', expr: {json.dumps(mo_[2] if len(mo_) > 2 else 'smile')}, s: {num(0.86 * k_)}, y: {num(-0.42 * k_)}, crop: 0.5, flip: {'false' if dirv > 0 else 'true'} }}")
    # INTERIOR: "interior": "madeira" | "pedra" | "loja"  -> sala com parede a ~5 m, janela, porta, quadros, chao com juntas + moveis
    it = b.get('interior')
    if it:
        kit = {'madeira': 'kit/room_wood', 'pedra': 'kit/room_stone', 'loja': 'kit/room_shop'}.get(it, 'kit/room_wood')
        pr.append(f"{{ asset: {json.dumps(kit)}, at: [X, 0], s: 1, drop: false }}")
        for nm_, dx_, z_, s_ in (b.get('moveis') or ([] if it == 'loja' else [('mk/Bookcase_2', 7.4, -3.4, 2.4), ('mk/Table_Large', -6.6, -1.6, 2.2), ('mk/Chair_1', -4.4, -1.2, 2.2), ('mk/Chest_Wood', 6.9, 0.6, 2.2)])):
            pr.append(f"{{ asset: {json.dumps(nm_)}, at: [X + {num(dx_)}, {num(z_)}], s: {num(s_)}, drop: false }}")
    # FACHADA: em plano medio ao ar livre, uma construcao logo atras dos personagens (canal: parede/fachada perto em 85% dos quadros)
    elif not wide_pre and b.get('fachada') is not False and not b.get('veiculo'):
        fb = {'countryside': ['buildings/house_small', 'buildings/barn'], 'outback': ['buildings/barn', 'buildings/windmill'], 'street': ['buildings/shop', 'buildings/house_two'], 'medieval': ['buildings/castle_tower', 'buildings/house_small'], 'harbor': ['buildings/shop', 'buildings/lighthouse']}.get(b.get('set', SET))
        if fb: pr.append(f"{{ asset: {json.dumps(fb[k % 2])}, at: [X + {num(4.5 if k % 2 else -4.5)}, -9.5], s: 1.25, ry: {num(-0.35 if k % 2 else 0.35)}, drop: false }}")
    for p in props:
        asset, dx, z, s = p[0], p[1] if len(p) > 1 else 0, p[2] if len(p) > 2 else 0.5, p[3] if len(p) > 3 else 1.0
        ex = p[4] if len(p) > 4 and isinstance(p[4], dict) else {}
        if asset.startswith(('kit/', 'buildings/')) and 'drop' not in ex: ex = {**ex, 'drop': False}   # peca de cenario nao cai do ceu
        extra = ''.join(f', {kk}: {json.dumps(vv)}' for kk, vv in ex.items())
        pr.append(f"{{ asset: {json.dumps(asset)}, at: [X + {num(dx)}, {num(z)}], s: {num(s)}{extra} }}")
    # textos / efeitos
    fx = []
    for dx_, dz_, t_ in locals().get('DUST', []): fx.append(f"{{ k: 'dust', a: {a} + {t_}, b: {a} + {t_ + 30}, at: [X + {num(dx_)}, DK + 0.4, {num(dz_)}], s: 2.4 }}")
    # MAPA DIDATICO: "mapa": "AUSTRALIA" (ou sozinho, na 1a vez que o texto cita um pais/cidade conhecido). Corta para o mapa por ~1,8 s.
    _mp = b.get('mapa')
    if _mp is None and B.get('mapas') is not False and not STATE.get('mapa'):
        _m = re.search(r'\b(Austrália|Brasil|França|Inglaterra|Japão|Alemanha|Rússia|China|Índia|Egito|Itália|Espanha|Portugal|Estados Unidos|México|Grécia|Turquia|Áustria|Holanda|Suécia|Noruega|Canadá|Argentina|Peru|Roma|Paris|Londres|Berlim|Moscou|Tóquio|Lisboa|Madri|Viena|Nova York|África|Europa|Ásia|Amazônia|Sibéria|Antártida)\b', b['say'])
        if _m: _mp = _m.group(1).upper(); _mw = len(b['say'][:_m.start()].split())
    if _mp:
        STATE['mapa'] = True; _mw = int(b.get('mapa_at', locals().get('_mw', 0)))
        fx.append(f"{{ k: 'map', a: WS({starts[k] + _mw}, -2), b: Math.min({bb}, WS({starts[k] + _mw}, -2) + {int(b.get('mapa_dur', 54))}), text: {json.dumps(str(_mp), ensure_ascii=False)} }}")
    if not b.get('interior') and light in ('day', 'noon', 'golden', 'dawn', 'dusk', 'desert') and not wx.get('rain') and not wx.get('snow') and b.get('passaros') is not False and (k % 2 == 0 or shot in WIDE):
        fx.append(f"{{ k: 'birds', a: {a}, b: {bb}, at: [X, DK + {num(4.5 + (k % 3) * 1.5)}, -30], n: {4 + k % 3}, dir: {1 if k % 4 < 2 else -1}, off: {8 + k * 7 % 14} }}")
    if b.get('text'):
        st = TXT[b.get('tstyle', TXT_CYCLE[k % 4])]
        off = int(b.get('tat', 0))
        up = {'close': 0.55, 'two': 0.46}.get(shot, 0.42)   # em plano fechado o texto sobe para nao cobrir o chapeu
        if b.get('titulo') or B.get('titulos') or shot in WIDE or b.get('veiculo') or k == len(beats) - 1 or len(b['text']) > 14:   # titulo flutuante so' a pedido ("titulo": true) ou em plano aberto
            fx.append(f"txt(X, WS({starts[k] + off}, -2), {bb}, {json.dumps(b['text'], ensure_ascii=False)}, '{st[0]}', '{st[1]}', {num(T['h'] + 2.2)}, {{ s: {b.get('tscale', 1.5)}, up: {up} }})")
        else:                                                                           # MODO RICKS: texto numa placa fincada na cena, ao lado dos personagens
            _sx = 0.0   # placa alta, atras e acima das cabecas, no centro do quadro
            fx.append(f"{{ k: 'text', a: {a}, b: {bb}, at: [X + {num(_sx)}, DK, {num(-1.3)}], text: {json.dumps(b['text'], ensure_ascii=False)}, s: {num(b.get('tscale', 1.5) * 1.75)}, col: '#3a2416', size: 120, board: {json.dumps(b.get('placa', True))} }}")
    for e in b.get('fx', []):
        kind, _, at = e.partition('@'); at = int(at) if at else 4
        if kind == 'burst': fx.append(f"{{ k: 'burst', a: {a} + {at}, at: [X + {num(sl[0] if n else 0)}, DK + 1.8, 3.2], s: 1.2 }}")
        elif kind in ('dust', 'puff', 'stars', 'splash', 'ring', 'creak'): fx.append(f"{{ k: {json.dumps(kind)}, a: {a} + {at}, b: {a} + {at + 26}, at: [X, DK + 0.5, 1.2], s: 1.1 }}")
    _armed = any(B.get('outfits', {}).get(o_, {}).get('rifle') for o_ in ([p_[0] for p_ in persons] + list((b.get('crowd') or {}).get('outfits') or [(b.get('crowd') or {}).get('outfit')])) if o_)
    if b.get('impact') and b.get('tiros') is not False and (SHOOT.search(nrm(b['say'])) or _armed or b.get('batalha')) and crowd_pos:   # fuzilaria cartunesca: clarões piscando pela tropa + som de tiro
        _off = 46 if b.get('caminhoes') else 8; _dur = int(len(b['say'].split()) / 2.7 * 30); _nf = max(8, min(40, (_dur - _off - 12) // 5))   # tiros durante a tomada INTEIRA (depois de a tropa subir nos caminhoes)
        for i in range(_nf):
            px, pz = crowd_pos[(i * 5 + 2) % len(crowd_pos)]; t0 = _off + i * 5 + (i * 7) % 4
            fx.append(f"{{ k: 'flash', a: {a} + {t0}, b: {a} + {t0 + 8}, at: [X + {num(px + 0.75)}, DK - 1.05 + {num(b.get('caminhao_y', 0.95) if pz < -5 and b.get('caminhoes') else 0)}, {num(pz + 0.4)}], s: {2.5 if wide else 2.0} }}")   # a carta do efeito ancora pela base: y baixo poe o clarao na altura do fuzil
        b.setdefault('sfx', []); b['sfx'] += [f'gun@{_off + i * 5 + (i * 7) % 4}' for i in range(_nf)]
    # animacao nas palavras-chave: golpe de camera + efeito no instante da palavra
    kfx = 0
    if b.get('kw') is not False:
        for j, w in enumerate(b['say'].split()):
            nw = nrm(w)
            for rx, kind, kick in KW:
                if rx.match(nw) and kfx < 3:
                    kfx += 1; wi = starts[k] + j; PLANO.append((k, w.strip('.,!?"'), kind)); KWSFX.append((wi, 'cannon' if re.match(r'canh|explo|bomb', nw) else {'burst': 'gun', 'ring': 'sting', 'dust': 'thump', 'puff': 'thump', 'stars': 'ding'}.get(kind, 'tick')))   # SOM na mesma palavra do efeito
                    px, pz = (crowd_pos[(j * 5) % len(crowd_pos)] if crowd_pos else (sl[0] if n else 0.0, 1.5))
                    if kind == 'burst': fx.append(f"{{ k: 'burst', a: WS({wi}), b: WS({wi}) + 22, at: [X + {num(px)}, DK + 1.8, {num(pz + 1.5)}], s: {1.7 if wide else 1.2} }}")
                    else: fx.append(f"{{ k: {json.dumps(kind)}, a: WS({wi}), b: WS({wi}) + 28, at: [X + {num(px)}, DK + 0.5, {num(pz + 1.0)}], s: {1.9 if wide else 1.1} }}")
                    if kick and kind == 'burst': KICKS.append(f"{{ f: WS({wi}), a: {round(kick * 0.35, 3)} }}")   # golpe de camera so' em impacto fisico e pequeno (canal: 0,23% da altura)
                    break
    opts = []
    if wide:
        T.setdefault('cx', 0.0); T.setdefault('cz', -1.5)
    elif b.get('crowd') and persons and not mv:   # plano medio com tropa atras: a camera mira nos PERSONAGENS PRINCIPAIS (a tropa marchando puxava a mira para o vazio)
        T.setdefault('cx', round(sum(sl[i] for i in range(len(persons))) / len(persons), 2)); T.setdefault('cz', 1.2)
    for kk in ('h', 'd0', 'd1', 'el', 'fov', 'az0', 'az1', 'cx', 'cz'):
        v = b.get(kk, T.get(kk))
        if v is not None: opts.append(f'{kk}: {num(v)}')
    if wx: opts.append('wx: ' + json.dumps(wx))
    if wide: opts.append("hero: { hero: 'none', wide: true }"); opts.append('vary: false'); opts.append('nocut: true')   # plano aberto = UMA tomada continua (camera abrindo/girando), sem sub-corte
    elif b.get('veiculo'): opts.append("hero: { hero: 'none' }")   # motorista fica atras do carro de proposito
    elif persons: opts.append("hero: { hero: 'any', frame: 'medium', minH: 0.07, main: %d }" % len(persons))
    if b.get('trans'): opts.append(f"trans: {json.dumps(b['trans'])}")
    elif k > 0: opts.append("trans: 'dissolve'")   # canal: quase sem corte seco; troca de cena por fusao curta
    if b.get('vary') is False and not wide: opts.append('vary: false')
    opts.append(f"actors: [{', '.join(acts)}]")
    if pr: opts.append(f"props: [{', '.join(pr)}]")
    if fx: opts.append(f"fx: [{', '.join(fx)}]")
    call = f"S('b{k}', {a}, {bb}, X, {json.dumps(light)}, {{ {', '.join(opts)} }})"
    if wide and not (shot == 'track' or mv):
        call = f"{{ ...{call}, nocut: true }}"
    if b.get('impact') and wide and not (shot == 'track' or mv) and b.get('grua') is not False:
        # SEQUENCIA DE ACAO (cobertura de batalha, varias cameras na MESMA encenacao):
        #   1) plano medio baixo na tropa se preparando (subindo nos caminhoes)  2) close de baixo nos fuzis atirando
        #   3) travelling lateral acompanhando quem foge pela fazenda            4) grua: sobe e recua ate a vista de cima do campo inteiro
        em_ = b.get('emus') or {}; tx_ = -6.5 if b.get('emus') else 0.0; ex_ = float(em_.get('x', 4.5)); ez_ = float(em_.get('z', 1.5))
        FR = lambda q: (a if q <= 0 else f"Math.round({a} + ({bb} + 1 - ({a})) * {q})")
        def part(i, q0, q1, k0, k1):
            pa, pb = FR(q0), (bb if q1 >= 1 else FR(q1) + ' - 1')
            c = call.replace(f"S('b{k}', {a}, {bb}, X,", f"S('b{k}{'' if i == 0 else '_' + str(i)}', {pa}, {pb}, X,", 1)
            if i: c = c.replace("trans: 'dissolve'", "trans: 'cut'")
            K = lambda f_, q: f"{{ f: {f_}, at: [X + {num(q[0])}, DK + {num(q[1])}, {num(q[2])}], d: {num(q[3])}, az: {num(q[4])}, el: {num(q[5])}, fov: {num(q[6])}{', ease: ' + json.dumps(q[7]) if len(q) > 7 else ''} }}"
            return f"{{ ...{c}, cam: [{K(pa, k0)}, {K(pb, k1)}], nocut: true, vary: false{', glide: true' if i else ''} }}"   # canal: quase nunca corta seco; a camera DESLIZA de um enquadramento ao outro
        if b.get('emus'):
            seq = [part(0, 0.0, 0.2, (tx_ + 1.5, 1.9, -2.5, 11, 24, 5, 44), (tx_ + 1.0, 1.9, -2.5, 9.2, 16, 5, 44)),
                   part(1, 0.2, 0.4, (tx_ - 0.5, 2.3, 0.8, 7.2, -30, 1, 44), (tx_ + 0.5, 2.3, 0.8, 6.4, -20, 2, 44)),
                   part(2, 0.4, 0.66, (ex_ + 0.5, 1.5, ez_ + 2.0, 12, 4, 6, 46), (ex_ + 7.5, 1.5, ez_ - 4.0, 13, -22, 8, 46, 'lin')),
                   part(3, 0.66, 1.0, (1.0, 1.4, 1.0, 17, 6, 13, 48), (3.0, 1.0, -2.0, 36, -18, 30, 48))]
        else:
            seq = [part(0, 0.0, 0.3, (0.0, 2.2, 0.5, 8.5, -26, 2, 44), (1.0, 2.2, 0.5, 7.4, -14, 3, 44)),
                   part(1, 0.3, 0.55, (-6.0, 1.8, 0.0, 11, 30, 5, 46), (4.0, 1.8, 0.0, 11, 18, 5, 46, 'lin')),
                   part(2, 0.55, 1.0, (0.0, 1.4, 0.0, 15, 8, 12, 48), (0.0, 1.0, -3.0, 34, -16, 30, 48))]
        call = ', '.join(seq)
    if shot == 'reveal' and not b.get('impact') and not mv and b.get('grua') is not False:
        _cx = T.get('cx', 0.0)
        cam = (f"cam: [{{ f: {a}, at: [X + {num(_cx)}, DK + 2.0, 0.5], d: 9, az: 10, el: 5, fov: 46 }}, "
               f"{{ f: {bb}, at: [X + {num(_cx)}, DK + 1.0, -2.0], d: 30, az: -14, el: 30, fov: 48 }}]")
        call = f"{{ ...{call}, {cam}, nocut: true }}"
    if shot == 'track' or mv:   # camera acompanha o grupo com velocidade constante (sem autocut)
        d = mv if mv else 8
        cam = (f"cam: [{{ f: {a}, at: [X + {num(-d / 2)}, DK + {num(T['h'])}, 1.5], d: {num(T['d0'])}, az: 6, el: {num(T.get('el', 3))}, fov: {num(T.get('fov', 44))} }}, "
               f"{{ f: {bb}, at: [X + {num(d / 2)}, DK + {num(T['h'])}, 1.5], d: {num(T['d1'])}, az: -8, el: {num(T.get('el', 3) + 1)}, fov: {num(T.get('fov', 44))}, ease: 'lin' }}]")
        call = f"{{ ...{call}, {cam}, nocut: true }}"
    if b.get('veiculo') and not b.get('cam_livre'):   # a camera acompanha o veiculo de lado, mostrando ele inteiro
        vc = b['veiculo']; x0v, x1v, zv = vc.get('de', -9), vc.get('para', 9), vc.get('z', 0.6); dd = vc.get('dist', 14.5)
        cam = (f"cam: [{{ f: {a}, at: [X + {num(x0v)}, DK + 1.9, {num(zv)}], d: {num(dd)}, az: {12 if x1v >= x0v else -12}, el: 7, fov: 40 }}, "
               f"{{ f: {bb}, at: [X + {num(x1v)}, DK + 1.9, {num(zv)}], d: {num(dd * 0.9)}, az: {-10 if x1v >= x0v else 10}, el: 8, fov: 40, ease: 'lin' }}]")
        call = f"{{ ...{call}, {cam}, nocut: true }}"
    if b.get('set') and b['set'] != SET and b['set'] in SETS_X: call = re.sub(r'\bX\b', 'X_' + b['set'], call)   # esta cena acontece em outro cenario
    return call

shots = [build_beat(k, b) for k, b in enumerate(beats)]
A_js = ', '.join(['0'] + [f"WS({starts[k]}, -3)" for k in range(1, len(beats))] + ['TOTAL_F()'])
assets = sorted(set(B.get('assets', []) + re.findall(r'asset: "([^"]+)"', ' '.join(shots)) + [p[0] for b in beats for p in b.get('props', [])] + [b['veiculo'].get('asset', 'vehicles/car') for b in beats if b.get('veiculo')]))

spec = f"""// {B.get('title', ID)} -- GERADO por mkvideo.py a partir de videos/{ID}/beats.json (edite o beats.json, nao este arquivo)
const X = {SETX}, DK = 6;{''.join(f' const X_{n} = {SETS_X[n]};' for n in USED_SETS[1:])}
const WS = (i, off = 0) => TIMING.words[Math.min(i, TIMING.words.length - 1)][0] + off;   // frame em que a palavra de indice i comeca
const A = [{A_js}];
const SPEC = {{
  id: {json.dumps(ID)}, {('exp: '+str(B['exp'])+', ') if 'exp' in B else ''}{('cinf: '+str(B['cinf'])+', ') if 'cinf' in B else ''}cutLen: 54, dissolveN: 7, glideN: 20, creep: 0.003, total: TOTAL_F(), sets: {json.dumps(USED_SETS)}, setx: {{ {SET}: X{''.join(f', {n}: X_{n}' for n in USED_SETS[1:])} }},
  outfits: {{ {(','+chr(10)+'    ').join(outfits_js)} }},
  assets: {json.dumps(assets)},
  kicks: [{', '.join(KICKS)}], flashes: [],
  shots: [
    {(','+chr(10)+'    ').join(shots)}
  ],
}};
"""
open(f'stories/{ID}/spec.js', 'w', encoding='utf-8').write(spec)

# ---------- cues.py (musica + efeitos) ----------
MUS = {
    'playful': lambda a, b: f"playful(F({a}), F({b}), 122)",
    'march':   lambda a, b: f"march(F({a}), F({b}), 112)",
    'tense':   lambda a, b: f"drone(F({a}), F({b}), 49); heartbeat(F({a}), F({b}), 72, 0.55)",
    'epic':    lambda a, b: f"march(F({a}), F({b}), 100); drone(F({a}), F({b}), 55)",
    'calm':    lambda a, b: f"harp(F({a}), F({b}))",
}
AMB = {'countryside': 'birds', 'outback': 'birds', 'medieval': 'birds', 'jungle': 'birds', 'harbor': 'sea', 'palace': 'birds', 'arctic': None, 'mountain': None, 'hall': None, 'stadium': None}
c1 = ["_W = lambda i: _WORDS[min(i, len(_WORDS) - 1)]['s'] * 30   # frame da palavra i", f"_A = [0] + [int(_W(i) - 3) for i in {starts[1:]}] + [FR]"]
k = 0
while k < len(beats):          # funde beats seguidos com o mesmo clima numa so' secao de musica (sem reiniciar o compasso)
    mood = beats[k].get('mood', MOOD); j = k
    while j + 1 < len(beats) and beats[j + 1].get('mood', MOOD) == mood: j += 1
    c1.append(MUS.get(mood, MUS['playful'])(f'_A[{k}]', f'_A[{j + 1}]')); k = j + 1
c2 = []
for k, b in enumerate(beats):
    a, e = f'_A[{k}]', f'_A[{k + 1}]'
    c2.append(f"whoosh(F({a}), 0.4, 0.35)")
    if AMB.get(SET) == 'birds' and b.get('light', LIGHT) in ('day', 'noon', 'dawn', 'golden', 'overcast', 'desert'): c2.append(f"birds(F({a}), F({e}), 6, 0.08)")
    if AMB.get(SET) == 'sea': c2.append(f"sea(F({a}), F({e}), 0.14); gulls(F({a}), F({e}), 3, 0.1)")
    if b.get('text'): c2.append(f"ding(F(int(_W({starts[k] + int(b.get('tat', 0))}) - 2)), 0.5, {[988, 1175, 880, 1319][k % 4]})")
    if b.get('move') or b.get('shot') == 'track': c2.append(f"steps(F({a}), F({e}), 0.12, 0.3)")
    for e2 in b.get('sfx', []):
        name, _, at = e2.partition('@'); at = int(at) if at else 4
        c2.append(f"{name}(F({a} + {at}))" if name not in ('steps', 'sea', 'gulls', 'birds') else f"{name}(F({a} + {at}), F({e}))")
for wi, nm in KWSFX: c2.append(f"{nm}(F(int(_W({wi}))))")
# ---------- PLANO DE ACAO: le o roteiro, separa os pontos-chave e confere se cada um tem acao + som ----------
_SOM = {'burst': 'tiro/explosao', 'ring': 'alerta', 'dust': 'impacto', 'puff': 'baque', 'stars': 'sino'}
_ACAO = re.compile(r'^(?!atirador|vendedor|chegar$)(atir|tiro|dispar|explod|canh|bomb|grit|berr|corr|fug|caiu|cairam|caindo|quebr|bateu|bateram|brig|lutou|lutaram|lutando|atac|invad|morre|matou|mataram|beb|brind|riu|riram|rindo|gargalh|chor|danc|cantou|cantaram|tocou|tocar|tocando|sino|pagou|pagar|compr|vend|roub|queim|incend|constru|cavou|cavar|enterr|naveg|afund|voou|voar|voando|nadou|nadar|marcha|cheg|descobr|perceb|assin|rende|vence|perde)')
_pl = ['# Plano de acao - ' + str(B.get('title', ID)), '', 'Cena | Plano | Luz/clima | O que aparece | Palavras-chave com efeito + som | Palavras de acao SEM efeito', '---|---|---|---|---|---']
_sem = 0
for k, b in enumerate(beats):
    _kw = [f"{w} ({kind} + som de {_SOM.get(kind, 'efeito')})" for kk, w, kind in PLANO if kk == k]; _ok = {nrm(w) for kk, w, kind in PLANO if kk == k}
    _falta = [] if (b.get('impact') or b.get('sfx') or b.get('fx')) else sorted({w.strip('.,!?"') for w in b['say'].split() if _ACAO.match(nrm(w)) and nrm(w) not in _ok and len(nrm(w)) > 3})[:4]
    _ap = [x for x in (('batalha aberta com tiros' if b.get('impact') else ''), ('tropa' if b.get('crowd') else ''), ('animais' if b.get('emus') or b.get('animals') else ''), ('interior' if b.get('interior') else ''), ('veiculo' if b.get('veiculo') or b.get('caminhoes') else ''), ('placa: ' + str(b['text']) if b.get('text') else ''), ('mapa' if b.get('mapa') else ''), ('objeto na mao' if any(len(w.split(':')) > 3 for w in b.get('who', [])) else '')) if x]
    _sem += len(_falta)
    _pl.append(f"b{k} | {b.get('shot')} | {b.get('hora') or b.get('light') or '-'} {b.get('clima') or ''} | {', '.join(_ap) or '-'} | {'; '.join(_kw) or '-'} | {', '.join(_falta) or '-'}")
open(f'stories/{ID}/plano.md', 'w', encoding='utf-8').write('\n'.join(_pl) + '\n')
print(f'plano de acao: {len(PLANO)} palavras-chave com efeito + som; {_sem} palavra(s) de acao sem efeito (veja stories/{ID}/plano.md e ponha "fx"/"sfx"/objeto/batalha na cena)')
open(f'stories/{ID}/cues.py', 'w', encoding='utf-8').write('\n'.join(c1) + '\n#--SFX--\n' + '\n'.join(c2) + '\n')
print(f'{ID}: {len(beats)} cenas, {n} palavras narradas -> stories/{ID}/spec.js, cues.py')
