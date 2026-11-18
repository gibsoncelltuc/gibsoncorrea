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
for _b in B['beats']:   # PORTO: cena pequena que fala de navio/porto/marinha acontece no cais (cenario 'harbor', com navio e mar)
    _t = re.sub(r'[^a-z ]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode())
    if re.search(r'\bnavios?\b|\bportos?\b|\bfrota\b|\bmarinha\b|\bcais\b|desembarc|zarp|esquadra', _t) and not _b.get('set') and not _b.get('interior') and SET != 'palace' and _b.get('shot') in (None, 'two', 'close', 'group', 'low', 'reveal') and not _b.get('batalha') and B.get('porto_cenario') is not False: _b['set'] = 'harbor'
_VEIC = ((r'\bcaminhao\b|\bcaminhoes\b', 'vehicles/truck'), (r'\bcarroca\b|\bcarrocas\b|\bcharrete', 'vehicles/wagon'), (r'\bmoto\b|motocicleta', 'vehicles/motorcycle'), (r'\bbicicleta', 'vehicles/bicycle'), (r'\btaxi\b', 'vehicles/taxi'), (r'\bjipe\b', 'vehicles/jeep'), (r'\btanque\b|\bblindado', 'vehicles/tank'), (r'\bcarro\b|\bcarros\b|\bautomovel', 'vehicles/car'))
for _b in B['beats']:   # DIRIGIR: "dirigiu/dirigindo/foi de carro/pilotou" -> o veiculo atravessa a tela com o 1o personagem ao volante
    _t = re.sub(r'[^a-z ]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode())
    if _b.get('veiculo') is None and _b.get('who') and not _b.get('interior') and not _b.get('batalha') and re.search(r'\bdirig|\bde carro\b|\bde caminhao\b|\bde carroca\b|\bde moto\b|\bpilotou|\bpilotava|\bao volante|\bpedalou|\bpedalava', _t):
        _as = next((as_ for rx_, as_ in _VEIC if re.search(rx_, _t)), 'vehicles/car')
        _b['veiculo'] = {'asset': _as, 'motorista': _b['who'][0], 'de': -11, 'para': 11}; _b.setdefault('shot', 'two')
for _b in B['beats']:   # NAVIO CHEGANDO/PARTINDO: plano aberto no cais para ver o navio andar na agua
    _t = re.sub(r'[^a-z ]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode())
    if _b.get('set', SET) in ('harbor', 'palace') and not _b.get('interior') and not _b.get('shot_lock') and re.search(r'\bnavios?\b|\bbarcos?\b|\bfrota\b|\besquadra\b|\bcaravela', _t) and re.search(r'cheg|desembarc|aport|atrac|zarp|partiu|partiram', _t): _b['shot'] = 'reveal'; _b['shot_lock'] = True
for _b in B['beats']:   # MONTANHA: cena que fala de colina/montanha/morro acontece no cenario de montanha
    _t = re.sub(r'[^a-z ]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode())
    if re.search(r'\bcolinas?\b|\bmontanhas?\b|\bmorros?\b|\bserra\b|\bpenhasco\b|\bencosta\b', _t) and not _b.get('set') and not _b.get('interior') and B.get('montanha_cenario') is not False: _b['set'] = 'mountain'
for _b in B['beats']:
    if _b.get('interior') and not _b.get('set'): _b['set'] = 'hall'      # interior fica no cenario 'hall' (sem arbusto/pedrinha de area externa)
USED_SETS = [SET] + sorted({b['set'] for b in B['beats'] if b.get('set') and b['set'] != SET and b['set'] in SETS_X})   # cenario por cena: "set" dentro do beat
if B.get('serie') and B.get('ep'): B['titulo_base'] = B.get('titulo_base') or B.get('title', ID); B['title'] = f"{B['serie']} EP {int(B['ep']):02d} - {B['titulo_base']}"   # serie com episodio numerado no titulo e no nome do arquivo
beats = B['beats']
for _b0 in beats: _b0['_crowd_roteiro'] = 'crowd' in _b0   # multidao escrita no roteiro; as outras sao do diretor

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
PROFISSOES = {  # "profissao" no figurino -> roupa, chapeu e tracos tipicos (o que o roteiro puser por cima vale mais)
    'padeiro': {'jacket': '#f6f0e6', 'pants': '#3b3f52', 'boots': '#2a2218', 'hat': 'bonnet', 'sash': '#f6f0e6', 'build': 'stout', 'moustache': '#4a3020'},
    'agricultor': {'jacket': '#7a9ac2', 'pants': '#6a4a2a', 'boots': '#2a2218', 'hat': 'straw', 'beard': '#6b4a2a'},
    'nobre': {'jacket': '#5a2a6a', 'pants': '#2a2a30', 'boots': '#1b1b1f', 'hat': 'tophat', 'tie': '#d9a630', 'buttons': '#e8c45a'},
    'politico': {'jacket': '#22252c', 'pants': '#22252c', 'boots': '#1b1b1f', 'hat': 'hair', 'hair': '#8a8a86', 'tie': '#c0262d', 'glasses': True},
    'empresario': {'jacket': '#2a3a5a', 'pants': '#2a3a5a', 'boots': '#1b1b1f', 'hat': 'bowler', 'tie': '#2f6fd0', 'build': 'stout'},
    'rei': {'jacket': '#5a2a8a', 'pants': '#2a2a30', 'boots': '#1b1b1f', 'hat': 'crown', 'sash': '#e8c45a', 'beard': '#6b4a2a', 'build': 'stout'},
    'general': {'jacket': '#22306a', 'pants': '#f1efe6', 'boots': '#1b1b1f', 'hat': 'shako_tall', 'buttons': '#e8c45a', 'sash': '#e8c45a', 'moustache': '#2a201a'},
    'soldado': {'jacket': '#27408b', 'pants': '#7d9fd0', 'boots': '#2a2218', 'hat': 'shako', 'belt': '#f1efe6', 'rifle': True},
    'marinheiro': {'jacket': '#2f5f6a', 'pants': '#e8e0c8', 'boots': '#1b1b1f', 'hat': 'beret', 'cap': '#27408b', 'beard': '#3a2a1f'},
    'cientista': {'jacket': '#f4f1e8', 'pants': '#3b3f52', 'boots': '#1b1b1f', 'hat': 'hair', 'hair': '#8a8a86', 'glasses': True, 'tie': '#3b3f52'},
    'medico': {'jacket': '#f4f1e8', 'pants': '#f4f1e8', 'boots': '#2a2218', 'hat': 'hair', 'hair': '#3a2a1f', 'glasses': True},
    'comerciante': {'jacket': '#8a5a34', 'pants': '#3b2a1a', 'boots': '#1b1b1f', 'hat': 'slouch', 'cap': '#3b2a1a', 'moustache': '#3a2a1f', 'build': 'stout'},
    'pescador': {'jacket': '#e8b46a', 'pants': '#3b3f52', 'boots': '#2a2218', 'hat': 'straw', 'beard': '#8a8a86'},
    'padre': {'jacket': '#1b1b1f', 'pants': '#1b1b1f', 'boots': '#1b1b1f', 'hat': 'hair', 'hair': '#8a8a86', 'sash': '#f4f1e8'},
    'camponesa': {'jacket': '#b0524a', 'pants': '#6a4a2a', 'boots': '#2a2218', 'hat': 'bonnet'},
    'jornalista': {'jacket': '#6a5a8a', 'pants': '#3b3f52', 'boots': '#1b1b1f', 'hat': 'bowler', 'glasses': True, 'tie': '#1b1b1f'},
}
_FAMHAIR = {str(o_.get('hair', '')).lower() for o_ in B.get('outfits', {}).values() if o_.get('pele')} - {''}
for _k, _o in B.get('outfits', {}).items():   # SEM SOSIA (ordem do Gibson): em video com famoso, ninguem mais usa a cor de cabelo dele (loiro do Trump so no Trump)
    if not _o.get('pele') and str(_o.get('hair', '')).lower() in _FAMHAIR: _o['hair'] = '#5a3a22'
for name, o in B.get('outfits', {}).items():
    o = {**PROFISSOES.get(str(o.get('profissao', '')).lower(), {}), **{k_: v_ for k_, v_ in o.items() if k_ != 'profissao'}}
    o = dict(o); mo = o.pop('moustache_on', None)
    hats = o.pop('hats', None); hairs = o.pop('hairs', None)
    jackets = o.pop('jackets', None) or ([c_ for c_ in ['#3f6fb5', '#6a4a2a', '#2a5a3a', '#8a3a2a', '#3a4a6a', '#7a6a3a', '#5a5a62', '#b0524a'] if c_ not in {str(v_.get('jacket', '')).lower() for k_, v_ in B.get('outfits', {}).items() if k_ not in ('POV', 'POVO')}] if name in ('POV', 'POVO') else None)   # povo: casaco de cor diferente por variante (multidao sem clones)   # "hats": [...] -> chapeu diferente por variante; sem chapeu -> cor/corte de cabelo por variante
    body = ', '.join(f'{k}: {json.dumps(v)}' for k, v in o.items())
    mou = f", ...(v % 2 ? {{ moustache: {json.dumps(mo)} }} : {{}})" if mo else ''
    hv = (f", jacket: {json.dumps(jackets)}[v % {len(jackets)}]" if jackets else '') + (f", hat: {json.dumps(hats)}[v % {len(hats)}]" if hats else '') + ('' if (hats or o.get('hat')) else f", hat: 'hair', hair: {json.dumps(hairs or ['#5a3b2a', '#2a2018', '#b8862f', '#8a8a86', '#7a3a1c'])}[v % {len(hairs or [1]*5)}], hairStyle: [null, null, 'long', null, 'bun'][v % 5]")
    _fixo = bool(o.get('pele') or o.get('fixo')); _mulher = o.get('hairStyle') in ('bun', 'long') or bool(o.get('mulher'))   # pessoa real (caricatura com "pele") ou "fixo": true -> sem oculos/barba/bigode sorteados (Trump nao ganha barba)
    outfits_js.append(f"{name}: (v = 0, e = {{}}) => ({{ _id: {json.dumps(name.lower())}, {body}, skin: {json.dumps(SKINS)}[v % 4]{hv}{mou}, ...(((v + {sum(ord(c) for c in name)}) % 6 === 4 && {json.dumps('glasses' not in o and not _fixo)}) ? {{ glasses: true }} : {{}}), ...(([1, 5].includes((v + {sum(ord(c) for c in name)}) % 6) && {json.dumps('beard' not in o and not o.get('rifle') and not _fixo and not _mulher)}) ? {{ beard: ['#3a2a1f', '#6b4a2a', '#8a8a86'][(v + {len(name)}) % 3] }} : {{}}), ...((((v + {sum(ord(c) for c in name)}) % 6 === 3) && {json.dumps('moustache' not in o and not mo and not _fixo and not _mulher)}) ? {{ moustache: ['#4a3020', '#2a201a', '#8a8a86'][v % 3] }} : {{}}), ...e }})")   # IDENTIDADE: cada personagem (nome + variante) ganha barba, bigode ou oculos proprios; soldado de fuzil fica sem barba

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
def nodrop(c): return re.sub(r'(asset: "[^"]+", at: \[[^\]]*\], s: [\d.]+)(?![\d.])(?!, drop)', r'\1, drop: false', c)   # nas partes seguintes da mesma cena os objetos ja estao no chao (nao caem de novo)


import unicodedata
def nrm(t): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode())
MASS = re.compile(r'infantaria|batalh|exercito|soldados|milhares|dezenas|tropas|acampamento|regimento|multidao|todomundo|artilharia|canhoes|campocheio|panico|marcha|esquadrao|legiao|frota|armada|invasao|invadiu')
ARRIVE = re.compile(r'chegou|chegaram|apareceu|surgiu|avancou|avancaram|marchava|marcharam|invadiu|invadiram|desembarcou|cercou|cercaram')
CLOSE_OK = re.compile(r'gritou|olhou|sorriu|chorou|pensou|disse|perguntou|riu|ordenou')
OBJ_DICT = [  # (palavra na narracao, objeto 3D da biblioteca, escala, grande?) -- usado para por objetos em cena e na pre-producao
    (r'\bbarril\b|\bbarris\b|aguardente|cerveja|\bvinho\b|\brum\b', 'barrel', 1.1, False), (r'caixote|\bcaixas\b|\bcarga\b|mercadoria', 'crate', 1.0, False), (r'\bcanhao\b|\bcanhoes\b|artilharia', 'cannon', 1.0, False),
    (r'\bbaldes?\b|\bpoco\b', 'tools/bucket', 1.8, False), (r'\bfonte\b|chafariz', 'nature/fountain', 1.2, False), (r'\bbandeiras?\b|estandarte', 'war/flagpole', 1.3, False), (r'\btambor\b|\btambores\b', 'war/drum', 1.4, False),
    (r'trincheira|barricada|sacos de areia', 'war/sandbags', 1.2, False), (r'\bescudos?\b', 'war/shield', 1.5, False), (r'\bfeno\b|trigo|plantac|colheita', 'nature/haybale', 1.1, False), (r'espantalho', 'nature/scarecrow', 1.2, False),
    (r'lanterna|lampiao|lamparina', 'tools/lantern', 1.2, False), (r'\bescadas?\b', 'tools/ladder', 1.2, False), (r'carrinho de mao', 'tools/wheelbarrow', 1.2, False), (r'ferreiro|bigorna', 'tools/anvil', 1.3, False),
    (r'\btulipas?\b|\bbulbos?\b|\bflor\b|\bflores\b', 'kit/tulip_red', 1.3, False), (r'\bcova\b|tumulo|enterr|caixao|cemiterio', 'kit/grave', 1.0, False), (r'\bbatatas?\b|\bhorta\b|\blegumes?\b', 'nature/flowerbed', 1.2, False),
    (r'\bbola\b|futebol|\bgol\b|partida|estadio', 'kit/ball', 1.0, False), (r'\bchaleira\b|\bpanelas?\b|\bsopa\b|caldeirao', 'kit/kettle', 1.0, False), (r'\bcerca\b|cercado|curral|fazenda|\bhorta\b', 'nature/picket_fence', 1.2, False),
    (r'\bbolos?\b|\bdoces?\b|confeit|padaria|\bpastel\b|\bpasteis\b', 'kit/cake_table', 1.0, False), (r'\btrono\b|coroad', 'kit/throne', 1.0, 'in'), (r'fogueira|acampamento|acamparam', 'kit/campfire', 1.2, False),
    (r'\btenda|barraca de campanha|acampamento', 'kit/tent', 1.3, True), (r'\bbau\b|tesouro|\bcofre', 'kit/chest', 1.2, False), (r'\bfeira\b|\bmercado\b|\bbarracas?\b|\bvendedor\b', 'kit/stall', 1.0, False),
    (r'\btrem\b|locomotiva|ferrovia', 'vehicles/locomotive', 1.3, True), (r'\bcarrocas?\b', 'vehicles/wagon', 1.2, True), (r'tanque de guerra|blindado', 'vehicles/tank', 1.2, True),
    (r'\btorres?\b|\bmuralhas?\b|\bcastelo\b|\bfortaleza\b|\bpalacio\b', 'buildings/castle_tower', 1.3, True), (r'\bmoinhos?\b', 'buildings/windmill', 1.2, True), (r'\bigreja\b|\bcatedral\b', 'buildings/church', 1.2, True), (r'\bfarol\b', 'buildings/lighthouse', 1.2, True), (r'\bponte\b', 'buildings/bridge', 1.2, True),
]
LUGARES = [  # (palavra na narracao, [(modelo, x, z, escala), ...]) -- cenografia de fundo do lugar citado
    (r'fazenda|fazendeiro|sitio|\bhorta\b|plantac|lavoura|celeiro|curral', [('buildings/barn', 5.5, -10.0, 1.2), ('nature/picket_fence', -3.4, -2.6, 1.3), ('nature/haybale', 3.6, -1.4, 1.1), ('nature/scarecrow', -4.6, -4.5, 1.2)]),
    (r'\bcasa\b|\bcasas\b|vizinho|aldeia|vila\b|vilarejo', [('buildings/house_small', -5.5, -10.0, 1.25), ('nature/picket_fence', 3.4, -2.8, 1.3), ('nature/tree_oak', 6.5, -7.0, 1.3)]),
    (r'\bigreja\b|\bcatedral\b|\bpadre\b|\bsino\b', [('buildings/church', 5.5, -11.0, 1.2)]),
    (r'\bmercado\b|\bfeira\b|\bloja\b|comerciante|\bvendedor\b', [('buildings/shop', -5.0, -9.5, 1.25), ('kit/stall', 3.6, -2.6, 1.0)]),
    (r'\bflorestas?\b|\bmata\b|\bbosque\b|\bselva\b', [('nature/tree_pine', -4.0, -5.0, 1.5), ('nature/tree_oak', 4.5, -6.0, 1.5), ('nature/tree_pine', 6.5, -3.5, 1.3), ('nature/bush', -5.5, -2.0, 1.2)]),
    (r'\bacampamento\b|acamparam|\bbarracas\b', [('kit/tent', -4.5, -5.0, 1.3), ('kit/tent', 5.0, -6.5, 1.3), ('kit/campfire', 3.0, -1.2, 1.2)]),
    (r'\bcastelo\b|\bfortaleza\b|\bforte\b|\bmuralhas?\b|\bpalacio\b', [('buildings/castle_tower', 6.0, -10.5, 1.3)]),
    (r'\bcartorio\b|\bprefeitura\b|\btribunal\b|\bbanco\b|\bescritorio\b|\bconsulado\b|\bembaixada\b', [('buildings/house_two', -5.0, -9.5, 1.3), ('nature/lamppost', 3.4, -2.6, 1.2), ('nature/bench', -3.6, -2.2, 1.2)]),
    (r'\bmoinhos?\b', [('buildings/windmill', 6.0, -11.0, 1.2)]), (r'\bfarol\b', [('buildings/lighthouse', 6.5, -11.0, 1.2)]),
    (r'\bcidades?\b|\bcapital\b|\bhotel\b|\bpredios?\b', [('buildings/apartment', -6.0, -12.0, 1.2), ('buildings/house_two', 6.0, -11.0, 1.2), ('nature/lamppost', 3.2, -2.4, 1.2)]),
    (r'\bpracas?\b|\bfonte\b', [('nature/fountain', 0.0, -4.5, 1.2), ('nature/bench', -3.6, -2.2, 1.2)]),
]
# OBJETOS NOVOS de cada sessao ficam em obj_dict.d/<sessao>.json ([[regex, modelo, escala, grande?], ...]) -- cada sessao edita SO o seu arquivo, assim o merge entre sessoes nunca apaga objeto de ninguem
for _rx, _mod in (B.get('objetos_do_video') or {}).items(): OBJ_DICT.insert(0, (_rx, _mod, 1.0, False))   # palavra->modelo que vale SO neste video (ex.: "\\bradio\\b": "kit/curie_box" na Marie Curie; noutro video radio e' aparelho)
for _f in sorted(__import__('glob').glob('obj_dict.d/*.json')):
    try:
        for _e in json.load(open(_f, encoding='utf-8')):
            if not any(_e[1] == x[1] for x in OBJ_DICT): OBJ_DICT.append((_e[0], _e[1], float(_e[2]), _e[3] if len(_e) > 3 else False))
    except Exception as _x: print(f'AVISO: {_f} invalido ({_x})')
FALTA_MODELAR = r'\b(pao|paes|queijo|peixe|peixes|piano|relogio|estatua|guilhotina|balanca|telefone|radio|bicicleta)\b'
def _sem_modelo(ws): return sorted(w_ for w_ in set(ws) if not any(re.search(o_[0], w_) for o_ in OBJ_DICT))   # palavra que ja tem modelo no OBJ_DICT (ex.: radio = elemento quimico da Marie Curie) nao e' falta
def _heroi():   # OBJETO HEROI do video: "heroi" no topo do roteiro, ou o objeto do titulo, ou o objeto mais citado na narracao
    if 'heroi' in B: return B['heroi'] or None
    nz = lambda t: re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode())
    tt = nz(str(B.get('title', ''))); allt = ' '.join(nz(b['say']) for b in B['beats'])
    for rx_, as_, sc_, big_ in OBJ_DICT:
        if big_ is False and re.search(rx_, tt): return as_
    best = max(((len(re.findall(rx_, allt)), as_) for rx_, as_, sc_, big_ in OBJ_DICT if big_ is False), default=(0, None))
    return best[1] if best[0] >= 2 else None
KW = [  # (regex da palavra, efeito, golpe de camera) -- animacao nas palavras-chave da narracao
    (re.compile(r'^(tiro|tiros|disparou|dispararam|disparo|disparos|atirava|atiravam|atirou|atiraram|atirar|explodiu|explodiram|explosao|canhoes|canhao|fogo|bomba|bombas|metralhadora|metralhadoras|balas|bala|artilharia)$'), 'burst', 0.09),
    (re.compile(r'^(gritou|gritaram|gritava|gritavam|berrou|berrava|socorro|ataque|atacar|atacaram|alarme)$'), 'ring', 0.06),
    (re.compile(r'^(panico|correu|correram|fugiu|fugiram|correria|debandada|fuga|retirada|recuou|recuaram|bateu|marchando|marchava|marcharam|perder)$'), 'dust', 0.07),
    (re.compile(r'^(festa|beberam|brindou|brindaram|comemoraram|venceu|venceram|ganhou|ganharam|vitoria|compraram|comprou|comprando|comprador|compradores|vendendo|vendeu|venderam|vender|dancar|dancou|dancando|danca|dancarinos|musica|musicos|rindo|riso|roubaram|roubou)$'), 'stars', 0.0),
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
        if b.get('shot') == 'track' and not b.get('batalha'): b['shot_lock'] = True   # o roteiro pediu gente andando/correndo: o diretor nao troca por multidao parada
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
        _tropa = mass or any(B.get('outfits', {}).get(w_.split(':')[0], {}).get('rifle') for w_ in b.get('who', []))   # batalha automatica so' com tropa em cena (um civil que da' um tiro nao vira multidao de clones)
        if b.get('batalha') or (not (first or last) and _tropa and any(IMPACT.match(w_) for w_ in words) and impact_n < int(B.get('max_impact', 2)) and b.get('impact') is not False):
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
                b['crowd'] = {'n': (12 if b.get('impact') else 5) if b.get('emus') else (18 if (b.get('impact') or (mass and (arrive or first))) else 10 if mass else 6), 'outfits': list(dict.fromkeys(persons_out + [army])), 'march': bool(arrive or first or (shot == 'reveal' and mass)) and not (b.get('impact') and any(SHOOT.match(w_) for w_ in words))}
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
HEROI = _heroi()
STATE = {'mapa': any(_b.get('mapa') for _b in B['beats'])}   # mapa pedido no roteiro: nao cria outro automatico
KWSFX = []
direct(beats)
if B.get('director') is not False and not any(b.get('impact') for b in beats) and len(beats) > 4:
    _b = beats[int(len(beats) * 0.6)]
    if not _b.get('shot_lock'): _b['impact'] = True; _b['shot'] = 'orbit'; _b.setdefault('crowd', {'n': 12, 'outfits': [w.split(':')[0] for w in _b.get('who', [])] or list(B.get('outfits', {'X': 0}))[:1], 'march': False})
# DOIS GRANDES MOMENTOS (ordem do Gibson): todo video tem 2 pontos de impacto encenados em plano aberto com multidao, efeito e som. Se o roteiro so' rendeu 1, a virada ("Acontece que") ou a cena a 1/3 do video vira o segundo.
if B.get('director') is not False and len(beats) > 6 and sum(1 for b in beats if b.get('impact')) < int(B.get('min_momentos', 2)):
    _im = [i for i, b in enumerate(beats) if b.get('impact')]
    _cand = [i for i, b in enumerate(beats) if 0 < i < len(beats) - 1 and not b.get('impact') and not b.get('shot_lock') and not b.get('interior') and not b.get('veiculo') and all(abs(i - j) > 1 for j in _im)]
    _vir = [i for i in _cand if re.match(r'acontece que|na verdade|so que|o problema', re.sub(r'[^a-z ]', '', unicodedata.normalize('NFKD', beats[i]['say'].lower()).encode('ascii', 'ignore').decode()))]
    _pick = (_vir or sorted(_cand, key=lambda i: abs(i - (len(beats) * (0.3 if (_im and _im[0] > len(beats) / 2) else 0.7)))) or [None])[0]
    if _pick is not None:
        _b = beats[_pick]; _b['impact'] = True; _b['_momento_auto'] = True; _b['shot'] = 'crowd'; _povo = [k_ for k_ in B.get('outfits', {}) if k_ in ('POV', 'POVO', 'SOL', 'TRO') or B['outfits'][k_].get('hats')]; _b.setdefault('crowd', {'n': 12, 'outfits': _povo or [w.split(':')[0] for w in _b.get('who', [])] or list(B.get('outfits', {'X': 0}))[:1], 'march': False, 'expr': 'shock'})
        _b.setdefault('fx', []); _b.setdefault('sfx', [])
        if not _b['fx']: _b['fx'] = ['ring@12', 'dust@40']
        if not _b['sfx']: _b['sfx'] = ['sting@10', 'thump@40']
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
# MULTIDAO SEM CLONES (ordem do Gibson): multidao criada pelo diretor usa o figurino de POVO; rei, nobre, cientista, medico, padre, general... sao pessoas unicas e nao viram 12 copias
_POVO = [k_ for k_, o_ in B.get('outfits', {}).items() if k_ in ('POV', 'POVO') or o_.get('hats')]
_UNICO = {k_ for k_, o_ in B.get('outfits', {}).items() if str(o_.get('profissao', '')).lower() in ('rei', 'nobre', 'general', 'cientista', 'medico', 'padre', 'politico', 'empresario', 'jornalista') or o_.get('hat') == 'crown' or (k_ not in _POVO and not str(o_.get('profissao', '')).lower() in ('soldado', 'marinheiro', 'agricultor', 'camponesa', 'pescador', 'comerciante', 'padeiro') and not B.get('serie', '').lower().startswith('guerras'))}
for _b in beats:
    if _b.get('crowd') and not _b.get('_crowd_roteiro') and _POVO:
        _ok = [o_ for o_ in _b['crowd'].get('outfits', []) if o_ not in _UNICO]
        _b['crowd']['outfits'] = list(dict.fromkeys(_ok + _POVO))


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
    _c = b.get('clima') or ('tempestade' if re.search(r'tempestade|temporal|trovao|raios', _sy) else 'chuva' if re.search(r'chuva|chovia|chovendo|choveu|aguaceiro', _sy) else 'neve' if re.search(r'neve|nevasca|nevava|nevando|inverno|congel|geada|muitofrio|friointenso|frioextremo|gelado|gelada', _sy) else 'neblina' if re.search(r'neblina|nevoeiro|nevoa|cerracao', _sy) else 'calor' if re.search(r'calor|solforte|solquente|escaldante|\\bseca\\b|sedeinsuport|muitoquente|deserto', _sy) else 'vento' if re.search(r'ventania|vendaval|furacao|ventoforte|\\bvento\\b|ventava|ventando', _sy) else None)
    AMB['hora'] = B.get('hora'); AMB['clima'] = None if B.get('clima') in (None, 'limpo', 'sol') else B.get('clima')   # hora/clima valem SO na cena onde aparecem (campo ou narracao); fora disso, o padrao do topo do roteiro -- a noite/neve de uma cena nao vaza para o resto do video
    if _h: AMB['hora'] = _h
    if _c: AMB['clima'] = None if _c in ('limpo', 'sol') else _c
    b['_frio'] = AMB.get('clima') == 'neve'; b['_calor'] = AMB.get('clima') == 'calor'   # frio: os personagens tremem; calor: suam (luz de deserto)
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
    HOLDS = (('mug', r'beber|bebeu|bebia|brind|caneca|cerveja|cha\b'), ('bottle', r'garrafa|aguardente|vinho|bebida|rum|whisky|uisque'), ('paper', r'carta|jornal|imprensa|ordem|documento|mapa|contrato|telegrama|relatorio|lista|assinou|lei\b'), ('book', r'livro|biblia|diario'), ('lantern', r'lanterna|lampiao|lamparina'), ('torch', r'tocha|incendi'), ('flag', r'bandeira|rendeu|rendicao'), ('sword', r'\bespadas?\b|\bduelo\b|\bduelaram\b|esgrima|\bsabre\b'), ('money', r'dolar|dolares|libras|notas|cedulas|\\bpago\\b'), ('coin', r'dinheiro|moeda|ouro|recompensa|pagou|pagar|fortuna|salario|imposto'), ('shovel', r'cavou|cavaram|cavando|cavar|trincheira|enterrou|enterraram|\\bcova\\b'), ('bag', r'saco|mala|bagagem|sacola'), ('spyglass', r'luneta|avistou|avistaram|procurar|vigia|observ'), ('tulip', r'tulipa|bulbo|flor\b|flores'))
    _say_sp = re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode())
    auto_hold = next((h for h, rx in HOLDS if re.search(rx, _say_sp)), None) if b.get('maos') is not False else None
    _acao = b.get('acao') or ('dancar' if re.search(r'\bdanc', _say_sp) else 'discutir' if (re.search(r'discut|brig|exigi|respondeu|gritou|ameac|insult', _say_sp) and len(b.get('who', [])) >= 2) else None)
    if not _acao: _acao = 'comemorar' if not IMPACT.search(_say_sp) and re.search(r'\bfesta|comemor|venceu|venceram|vitoria|\bbrind|gargalh|\briu\b|\briram\b|\brindo\b', _say_sp) else 'conversar' if '"' in b['say'] else None
    if _acao == 'nenhuma': _acao = None
    b['_acao'] = _acao
    _px = {'dancar': ", pose: 'dance', acting: false", 'discutir': ", pose: 'argue'", 'comemorar': ", pose: 'cheer'", 'conversar': ", pose: 'talk'"}.get(_acao, '')   # "acao": "discutir" -> os personagens gesticulam um para o outro
    _chega = b.get('chega') if 'chega' in b else bool(re.search(r'chegou|chegaram|entrou|entraram|apareceu|apareceram|veio|vieram|correu para|correram para', _say_sp))
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
            acts.append(f"{{ outfit: {json.dumps(out)}, v: {v}, at: [X + {num(dx - d / 2)}, {num(z)}], move: [[X + {num(dx + d / 2)}, {num(z)}], {a}, {bb}, 'lin'], pose: {json.dumps('run' if re.search(r'corre|correu|correram|fugi|fuga|disparou em|debandada|persegui', _say_sp) else 'march' if B.get('outfits', {}).get(out, {}).get('rifle') else 'stroll')}, expr: {json.dumps(ex)}{ov} }}")   # correu/fugiu: CORRE; soldado marcha; civil caminha solto
        else:
            _pp = _px if _px else (", pose: 'react'" if ex in ('shock', 'nervous') else '' if (hold or shot in WIDE or b.get('acao') == 'nenhuma') else ", pose: 'talk'")   # ninguem fica so piscando: sem acao marcada, gesticula de leve
            if _pp and not _px: b['_acao'] = b.get('_acao') or ('reagir' if 'react' in _pp else 'conversar')
            if _chega and i == len(persons) - 1 and len(persons) >= 2 and shot not in WIDE:   # CHEGADA: entra andando pela lateral e para no lugar
                sd_ = 1 if dx >= 0 else -1; b['_chega'] = True
                acts.append(f"{{ outfit: {json.dumps(out)}, v: {v}, at: [X + {num(dx + sd_ * 2.4)}, {num(z - 1.6)}], move: [[X + {num(dx)}, {num(z)}], {a}, Math.round({a} + Math.min(48, ({bb} - ({a})) * 0.3)), 'lin'], arrive: true, walk: {json.dumps('march' if B.get('outfits', {}).get(out, {}).get('rifle') else 'stroll')}, look: {num(-0.4 if dx > 0 else 0.4)}, expr: {json.dumps(ex)}{ov} }}")
            else:
                acts.append(f"pp(X, {json.dumps(out)}, {v}, {num(dx)}, {num(z)}, {json.dumps(ex)}" + (f", {{ over: {{ hold: {json.dumps(hold)} }}{_pp} }})" if hold else (f", {{ {_pp[2:]} }})" if _pp else ')')))
    # animais
    for j, an in enumerate(animals):
        sp = an[0]; dxa = an[1] if len(an) > 1 else 2.2 + j * 1.8; za = an[2] if len(an) > 2 else 0.6; st = an[3] if len(an) > 3 else 'stand'
        sc = an[4] if len(an) > 4 else {'horse': 0.7, 'bear': 1.0, 'emu': 1.6}.get(sp, 1.0)
        key = 'bird' if sp in ('emu', 'goose', 'duck', 'chicken', 'rooster', 'gull') else 'animal'
        fl = 'true' if dxa > 0 else 'false'
        if mv and key == 'animal': dxa = max(-1.1, min(1.1, dxa)); za = max(za, 1.6)   # andando: animal perto do centro e a frente (nao sai cortado na borda)
        if mv and key == 'animal':   # cena andando/correndo: TODO animal anda junto (3D cavalo/urso; 2D cachorro, vaca, ovelha... olham para a esquerda -> flip ao ir para a direita)
            _fl = ('false' if mv > 0 else 'true') if sp in ('horse', 'bear') else ('true' if mv > 0 else 'false')
            acts.append(f"{{ {key}: {json.dumps(sp)}, at: [X + {num(dxa - mv / 2)}, {num(za)}], move: [[X + {num(dxa + mv / 2)}, {num(za)}], {a}, {bb}, 'lin'], state: 'trot', spd: 0.09, s: {num(sc)}, flip: {_fl}, seed: {j * 3 + 1} }}")
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
                acts.append(f"pp(X, {json.dumps(out)}, {i % 7}, {num(x0)}, {num(z0)}, {json.dumps(ex)}, {{ look: {look}, seed: {i % 4 + (i * 3 if _px else 0)}{_px} }})")   # 7 variantes: multidao com cores, chapeus e rostos variados
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
        fb = {'countryside': ['buildings/house_small', 'buildings/house_two'], 'outback': ['buildings/house_small', 'buildings/windmill'], 'street': ['buildings/shop', 'buildings/house_two'], 'medieval': ['buildings/castle_tower', 'buildings/house_small'], 'harbor': ['buildings/shop', 'buildings/lighthouse']}.get(b.get('set', SET))
        if fb: pr.append(f"{{ asset: {json.dumps(fb[k % 2])}, at: [X + {num(4.8 if k % 2 else -4.8)}, -11.0], s: 1.05, ry: {num(-0.35 if k % 2 else 0.35)}, drop: false }}")
    # OBJETOS DA HISTORIA: o que a narracao cita e existe na biblioteca entra em cena sozinho (ate 2 por cena)
    if b.get('objetos') is not False and not b.get('veiculo'):
        tem_ = {str(p_[0]) for p_ in props}; n_auto = 0
        _fam = lambda x_: re.sub(r'_(red|yellow|purple|striped)$', '', str(x_))
        if HEROI and (k == 0 or k == len(beats) - 1) and not wide_pre and not any(_fam(t_) == _fam(HEROI) for t_ in tem_):   # o objeto heroi abre e fecha o video
            props = props + ([[HEROI, 0.0, 2.0, 1.15]] if len(b.get('who', [])) == 2 else [[HEROI, (1.7 if k % 2 else -1.7), -0.5, 1.3]])   # entre os dois, a frente (a placa do ano fica atras); tem_.add(HEROI); b.setdefault('_auto_obj', []).append(HEROI)
        for rx_, as_, sc_, big_ in OBJ_DICT:
            if n_auto >= 2 or as_ in tem_ or any(_fam(t_) == _fam(as_) for t_ in tem_) or not re.search(rx_, _say_sp): continue
            if (big_ is True and (b.get('interior') or wide_pre)) or (big_ == 'in' and not b.get('interior')): continue
            if as_ == 'kit/throne': props = props + [[as_, 0, -2.6, sc_]]; tem_.add(as_); n_auto += 1; b.setdefault('_auto_obj', []).append(as_); continue
            if big_ is True: props = props + [[as_, (6.0 if k % 2 else -6.0), -9.5, sc_]]; b['fachada'] = False
            elif as_.startswith('kit/') and as_ != 'kit/grave' and 'tulip' not in as_: props = props + [[as_, (0.25 if shot == 'close' else 0.0) + (1.7 if (k + n_auto) % 2 else -1.7) * (0.0 if len(b.get('who', [])) == 2 else 1.0), -2.3, sc_]]   # movel/objeto grande da historia: atras dos personagens, dentro do quadro
            else: props = props + [[as_, (3.1 if (k + n_auto) % 2 else -3.1), 0.2 + 0.3 * n_auto, sc_]]
            tem_.add(as_); n_auto += 1; b.setdefault('_auto_obj', []).append(as_)
    if re.search(r'navio|frota|marinha|esquadra|encouracado', _say_sp) and wide_pre and not b.get('interior') and b.get('set', SET) in ('palace', 'harbor') and b.get('objetos') is not False:
        props = props + [['ship', -13, -34, 0.8], ['ship', 12, -40, 0.7]]; b.setdefault('_auto_obj', []).append('navios ao fundo')
    # FOGO (seguir a risca): "queimaram", "tacaram fogo", "em chamas", "incendio" -> labaredas 3D em cena, perto do que queima, e clarao
    if re.search(r'queim|incendi|\bfogo\b|em chamas|\bchamas\b|fogueira nao', _say_sp) and not re.search(r'abriram fogo|abriu fogo|fogo amigo|cessar fogo|arma de fogo|lanca ?chamas|extintor|tiro', _say_sp) and b.get('fogo') is not False and not b.get('interior'):
        props = props + [['kit/fire', -2.6, -2.2, 1.5], ['kit/fire', 2.9, -3.0, 1.9], ['kit/fire', 0.3, -5.0, 2.4]] + ([['kit/fire', -6, -7, 2.6], ['kit/fire', 6.5, -8, 2.8]] if wide_pre else [])
        b.setdefault('_auto_obj', []).append('kit/fire'); b['_fogo'] = True; b.setdefault('fx', []); b['fx'] = list(b['fx']) + ['puff@20', 'puff@60']; b.setdefault('sfx', []); b['sfx'] = list(b['sfx']) + ['whoosh@18']
    if re.search(r'decol|levantou voo|lancad|lancou|subiu ao ceu|subiu para o ceu|foi para o espaco|rumo ao espaco', _say_sp):   # objetos que entraram sozinhos tambem decolam
        props = [[{'kit/rocket': 'kit/falcon_air', 'kit/balloon': 'kit/balloon_air'}.get(str(p_[0]), p_[0])] + list(p_[1:]) for p_ in props]
    # LUGAR CITADO = LUGAR EM CENA (seguir o roteiro A RISCA): fazenda, casa, igreja, mercado, floresta, acampamento... entram como cenografia de fundo
    if b.get('objetos') is not False and not b.get('interior') and not b.get('veiculo'):
        tem2_ = {str(p_[0]) for p_ in props}; sd2_ = 1 if k % 2 else -1
        for rx_, itens_ in LUGARES:
            if not re.search(rx_, _say_sp): continue
            novos_ = [it_ for it_ in itens_ if it_[0] not in tem2_]
            for as_, x_, z_, sc_ in novos_: props = props + [[as_, x_ * sd2_, z_ - (4 if wide_pre else 0), sc_]]; tem2_.add(as_)
            if novos_: b.setdefault('_auto_obj', []).extend(a_[0] for a_ in novos_); b['fachada'] = False
            break
    if re.search(r'\bnavios?\b|\bbarcos?\b|\bfrota\b|\besquadra\b|\bcaravela', _say_sp) and re.search(r'cheg|desembarc|aport|atracou|atracaram|apareceu|apareceram|surgiu|vinham|navegou|navegaram|zarp|partiu|partiram', _say_sp) and not b.get('interior') and b.get('set', SET) in ('harbor', 'palace') and b.get('objetos') is not False:
        _parte = bool(re.search(r'zarp|partiu|partiram', _say_sp))   # NAVIO EM MOVIMENTO: chegando (do mar para o cais) ou partindo
        props = props + [['ship', -6 if _parte else -42, -24 if _parte else -34, 0.8, {'mover': [-44, -36] if _parte else [-7, -23]}], ['boat', 9 if _parte else 30, -14 if _parte else -22, 1.0, {'mover': [32, -24] if _parte else [8, -13]}]]
        b.setdefault('_auto_obj', []).append('navio em movimento')
    for p in props:
        asset, dx, z, s = p[0], p[1] if len(p) > 1 else 0, p[2] if len(p) > 2 else 0.5, p[3] if len(p) > 3 else 1.0
        ex = p[4] if len(p) > 4 and isinstance(p[4], dict) else {}
        if asset.startswith(('kit/', 'buildings/')) and 'drop' not in ex: ex = {**ex, 'drop': False}   # peca de cenario nao cai do ceu
        extra = ''.join(f', {kk}: {json.dumps(vv)}' for kk, vv in ex.items() if kk not in ('alto', 'mover', 'carregado') and not (kk == 'y' and ex.get('carregado'))) + (f", y: DK + {num(ex.get('y', 0.7))}, move: [[X + {num(dx + mv / 2)}, {num(z)}], {a}, {bb}, 'lin'], drop: false" if ex.get('carregado') and mv else '')   # OBJETO CARREGADO: ["kit/sink", dx_do_personagem + 0.5, z, escala, {"carregado": true}] em cena "track": anda junto na altura das maos + (f", move: [[X + {num(ex['mover'][0])}, {num(ex['mover'][1])}], {a}, Math.round({a} + ({bb} - ({a})) * 0.85), 'sm'], drop: false" if ex.get('mover') else '')
        pr.append(f"{{ asset: {json.dumps(asset)}, at: [X + {num(dx - (mv / 2 if ex.get('carregado') else 0))}, {num(z)}], s: {num(s)}{extra} }}")
    # textos / efeitos
    fx = []
    for dx_, dz_, t_ in locals().get('DUST', []): fx.append(f"{{ k: 'dust', a: {a} + {t_}, b: {a} + {t_ + 30}, at: [X + {num(dx_)}, DK + 0.4, {num(dz_)}], s: 0.85 }}")
    # MAPA DIDATICO: "mapa": "AUSTRALIA" (ou sozinho, na 1a vez que o texto cita um pais/cidade conhecido). Corta para o mapa por ~1,8 s.
    _mp = b.get('mapa')
    if _mp is None and B.get('mapas') is not False and not STATE.get('mapa'):
        _m = re.search(r'\b(Austrália|Brasil|França|Inglaterra|Japão|Alemanha|Rússia|China|Índia|Egito|Itália|Espanha|Portugal|Estados Unidos|México|Grécia|Turquia|Áustria|Holanda|Suécia|Noruega|Canadá|Argentina|Peru|Roma|Paris|Londres|Berlim|Moscou|Tóquio|Lisboa|Madri|Viena|Nova York|África|Europa|Ásia|Amazônia|Sibéria|Antártida)\b', b['say'])
        if _m: _mp = _m.group(1).upper(); _mw = len(b['say'][:_m.start()].split())
    if _mp:
        STATE['mapa'] = True; b['passaros'] = False; _mw = int(b.get('mapa_at', locals().get('_mw', 0)))
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
    if b.get('impact') and b.get('tiros') is not False and (any(SHOOT.match(nrm(w_)) for w_ in b['say'].split()) or _armed or b.get('batalha')) and crowd_pos:   # fuzilaria cartunesca: clarões piscando pela tropa + som de tiro
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
                    _rif = [i_ for i_, pe_ in enumerate(persons) if B.get('outfits', {}).get(pe_[0], {}).get('rifle') or PROFISSOES.get(str(B.get('outfits', {}).get(pe_[0], {}).get('profissao', '')).lower(), {}).get('rifle')]
                    if kind == 'burst' and _rif and not re.match(r'canh|explo|bomb|artilh', nw) and not crowd_pos:   # TIRO: o clarao sai do cano da arma de quem atira
                        ri_ = _rif[0]; _sd = 1 if sl[ri_] <= 0 else -1; b.setdefault('_shots', []).append(f"WS({wi})")
                        if shot == 'track' or mv: fx.append(f"{{ k: 'flash', a: WS({wi}), b: WS({wi}) + 8, follow: {ri_}, dx: 1.7, at: [0, DK - 0.55, 0], s: 1.6 }}"); fx.append(f"{{ k: 'puff', a: WS({wi}) + 3, b: WS({wi}) + 20, follow: {ri_}, dx: 1.9, at: [0, DK + 1.9, 0], s: 0.5 }}")   # correndo e atirando: o clarao acompanha o cano
                        else: fx.append(f"{{ k: 'flash', a: WS({wi}), b: WS({wi}) + 8, at: [X + {num(sl[ri_] + 1.55 * _sd)}, DK - 0.55, {num(ZS[ri_ % len(ZS)] + 0.4)}], s: 1.6 }}"); fx.append(f"{{ k: 'puff', a: WS({wi}) + 3, b: WS({wi}) + 24, at: [X + {num(sl[ri_] + 1.8 * _sd)}, DK + 1.9, {num(ZS[ri_ % len(ZS)] + 0.4)}], s: 0.5 }}")
                    elif kind == 'burst': fx.append(f"{{ k: 'burst', a: WS({wi}), b: WS({wi}) + 22, at: [X + {num(px)}, DK + 1.8, {num(pz + 1.5)}], s: {1.7 if wide else 1.2} }}")
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
    # INTERACAO FISICA: em cena media com 2+ pessoas, os dois principais agem um SOBRE o outro (nao so' falam para a camera). Escolhida pelo texto; sem pista no texto, roda uma lista sem repetir (comeca num ponto diferente em cada video).
    if not wide and len(persons) >= 2 and b.get('interacao') is not False and not b.get('veiculo') and not (shot == 'track' or mv) and len(acts) >= 2:
        if b.get('interacao'): pair = {'empurrar': ('shove', 'stagger'), 'discutir': ('lunge', 'lunge'), 'cochichar': ('lean', 'lean'), 'entregar': ('step', 'nod'), 'susto': ('lean', 'recoil'), 'reverencia': ('nod', 'bow'), 'pular': ('hop', 'hop'), 'abracar': ('hug', 'hug'), 'tremer': ('shiver', 'shiver')}.get(b['interacao'], ('lean', 'nod')); nome = b['interacao']
        elif re.search(r'abrac', _say_sp): pair, nome = ('hug', 'hug'), 'abracar'
        elif re.search(r'beberam|brindaram|brinde|beb(e|i)am juntos', _say_sp): pair, nome = ('hop', 'hop'), 'brindar'
        elif b.get('_frio'): pair, nome = ('shiver', 'shiver'), 'tremem de frio'
        elif re.search(r'empurr|\bsoco|socou|\bbateu|agred|chutou|derrubou|expuls|arranc|tomou d', _say_sp): pair, nome = ('shove', 'stagger'), 'empurrar'
        elif _acao == 'discutir': pair, nome = ('lunge', 'lunge'), 'discutir'
        elif re.search(r'cochich|segredo|\bplano\b|combin|\btrato|acordo|negoci|sussurr', _say_sp): pair, nome = ('lean', 'lean'), 'cochichar'
        elif re.search(r'entreg|pagou|pagar|\bdeu\b|vendeu|comprou|ofereceu|cobrou|\bconta\b|presente|emprest|trocou', _say_sp): pair, nome = ('step', 'nod'), 'entregar'
        elif re.search(r'curvou|reverenc|obedec|ordenou|majestade|ajoelh', _say_sp): pair, nome = ('nod', 'bow'), 'reverencia'
        elif _acao == 'comemorar': pair, nome = ('hop', 'hop'), 'pular'
        elif persons[1][2] in ('shock', 'nervous', 'pained'): pair, nome = ('lean', 'recoil'), 'susto'
        else:
            POOL = [(('lean', 'nod'), 'aproxima-se'), (('step', 'recoil'), 'avanca e o outro recua'), (('nod', 'lean'), 'o outro se aproxima'), (('lunge', 'nod'), 'insiste'), (('step', 'nod'), 'vai ate o outro')]
            pair, nome = POOL[(sum(ord(c) for c in ID) + STATE.get('inter_n', 0)) % len(POOL)]; STATE['inter_n'] = STATE.get('inter_n', 0) + 1
        _ALLI = [(('lean', 'nod'), 'aproxima-se'), (('step', 'recoil'), 'avanca e o outro recua'), (('lunge', 'lunge'), 'discutir'), (('nod', 'lean'), 'o outro se aproxima'), (('shove', 'stagger'), 'empurrar'), (('step', 'nod'), 'vai ate o outro'), (('lean', 'lean'), 'cochichar'), (('lean', 'recoil'), 'susto'), (('lunge', 'nod'), 'insiste'), (('nod', 'bow'), 'reverencia')]
        _used = STATE.setdefault('inter_used', [])
        if nome in _used and not b.get('interacao'):   # cada video usa interacoes DIFERENTES de cena para cena
            _h = sum(ord(c) for c in ID); _alt = [_ALLI[(_h + j) % len(_ALLI)] for j in range(len(_ALLI))]
            _alt = [x for x in _alt if x[1] not in _used and (x[1] not in ('empurrar', 'reverencia') or _acao == 'discutir')] or [x for x in _alt if x[1] not in _used]
            if _alt: pair, nome = _alt[0]
        _used.append(nome)
        for i_ in (0, 1):
            if not acts[i_].startswith('pp(') or (b.get('_chega') and i_ == len(persons) - 1): continue
            dir_ = 1 if sl[1 - i_] > sl[i_] else -1
            it_ = f"inter: {{ k: '{pair[i_]}', a: Math.round({a} + ({bb} - ({a})) * {0.12 if i_ == 0 else 0.2}), b: Math.round({a} + ({bb} - ({a})) * {0.82 if i_ == 0 else 0.9}), dir: {dir_}, n: 2, ph: {0 if i_ == 0 else 3.14} }}"
            acts[i_] = (acts[i_][:-3].rstrip() + ', ' + it_ + ' })') if acts[i_].endswith('})') else (acts[i_][:-1] + ', { ' + it_ + ' })')
        b['_inter'] = nome
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
            if i: c = nodrop(c.replace("trans: 'dissolve'", "trans: 'cut'"))
            K = lambda f_, q: f"{{ f: {f_}, at: [X + {num(q[0])}, DK + {num(q[1])}, {num(q[2])}], d: {num(q[3])}, az: {num(q[4])}, el: {num(q[5])}, fov: {num(q[6])}{', ease: ' + json.dumps(q[7]) if len(q) > 7 else ''} }}"
            return f"{{ ...{c}, cam: [{K(pa, k0)}, {K(pb, k1)}], nocut: true, vary: false{', glide: true' if (i and not (b.get('emus') and i == 2)) else ''} }}"   # canal: quase nunca corta seco; a camera DESLIZA de um enquadramento ao outro
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
    # DETALHE DE OBJETO (canal: 5-15% do video e' close no objeto da historia): no meio da cena a camera desliza ate o objeto ou a placa e volta
    _cands = [p_ for p_ in props if not str(p_[0]).startswith(('kit/room', 'kit/porch', 'kit/grave', 'kit/cross', 'kit/tulip_bed', 'buildings/', 'vehicles/', 'ship', 'nature/picket_fence', 'nature/haybale', 'nature/scarecrow', 'nature/bush', 'nature/rocks', 'nature/tree'))]
    _cands = [p_ for p_ in _cands if (float(p_[2]) if len(p_) > 2 else 0.5) > -3.0 and not str(p_[0]) in ('kit/volcano', 'kit/tower', 'kit/tower_catch', 'kit/booster_air', 'kit/prison', 'kit/white_house', 'kit/mountain_bunker', 'kit/miners', 'kit/falcon_air', 'kit/falcon9_land', 'kit/b2_air', 'kit/balloon_air', 'kit/helicopter_air', 'kit/iceberg')]   # close de detalhe so em objeto pequeno e perto (objeto gigante ao fundo = tela vazia)
    _fam2 = lambda x_: re.sub(r'_(red|yellow|purple|striped)$', '', str(x_))
    _obj = next((p_ for p_ in _cands if HEROI and _fam2(p_[0]) == _fam2(HEROI)), None); _eh = _obj is not None
    _obj = _obj or next(iter(_cands), None)
    _placa = bool(b.get('text')) and "board:" in call
    if (b.get('detalhe') is not False and not wide and not b.get('impact') and not b.get('veiculo') and not (shot == 'track' or mv) and (k > 0 or _eh) and k < len(beats) - 1
            and (_obj or _placa) and len(b['say'].split()) >= (8 if _eh else 11) and (STATE.get('detalhes', 0) < int(B.get('max_detalhes', 3)) or (_eh and not STATE.get('det_heroi')))):
        if _eh: STATE['det_heroi'] = STATE.get('det_heroi', 0) + 1; b['_det_heroi'] = True
        Fq = lambda q: f"Math.round({a} + ({bb} + 1 - ({a})) * {q})"
        if _obj:
            ox, oz, os_ = (float(_obj[1]) if len(_obj) > 1 else 0.0), (float(_obj[2]) if len(_obj) > 2 else 0.5), (float(_obj[3]) if len(_obj) > 3 else 1.0)
            oy_ = float(_obj[4].get('alto', 0.75)) if len(_obj) > 4 and isinstance(_obj[4], dict) else (1.62 if 'tulip' in str(_obj[0]) else 1.2 if str(_obj[0]) in ('kit/cake_table', 'kit/throne') else 0.75)   # altura do centro do objeto ("alto" no 5o campo do prop)
            k0 = (ox, oy_ * os_, oz, (5.6 if oy_ > 1.5 else 5.0) if oy_ > 1 else 4.2, 14 if ox < 0 else -14, 6 if oy_ > 1 else 10, 44); k1 = (ox, oy_ * os_, oz, (4.7 if oy_ > 1.5 else 4.2) if oy_ > 1 else 3.4, 8 if ox < 0 else -8, 5 if oy_ > 1 else 9, 44)
        else: k0 = (0.0, 3.1, -1.3, 9.6, 6, -3, 44); k1 = (0.0, 3.1, -1.3, 8.6, -4, -3, 44)   # close na placa: mais longe, a placa cabe INTEIRA no quadro
        Kc = lambda f_, q: f"{{ f: {f_}, at: [X + {num(q[0])}, DK + {num(q[1])}, {num(q[2])}], d: {num(q[3])}, az: {num(q[4])}, el: {num(q[5])}, fov: {num(q[6])} }}"
        base = call; pid = f"S('b{k}', {a}, {bb}, X,"
        if pid in base:
            STATE['detalhes'] = STATE.get('detalhes', 0) + 1; b['_detalhe'] = True
            p0 = base.replace(pid, f"S('b{k}', {a}, {Fq(0.36)} - 1, X,", 1)
            p1 = re.sub(r"hero: \{[^}]*\}", "hero: { hero: 'none', detalhe: true }", base.replace(pid, f"S('b{k}_d', {Fq(0.36)}, {Fq(0.6)} - 1, X,", 1).replace("trans: 'dissolve'", "trans: 'cut'"), count=1)
            p2 = base.replace(pid, f"S('b{k}_v', {Fq(0.6)}, {bb}, X,", 1).replace("trans: 'dissolve'", "trans: 'cut'")
            p1, p2 = nodrop(p1), nodrop(p2)
            p1 = re.sub(r", inter: \{[^}]*\}", "", p1).replace("pose: 'argue'", "pose: 'stand'").replace("pose: 'talk'", "pose: 'stand'")   # durante o close no objeto ninguem avanca/gesticula na frente da lente
            call = f"{p0}, {{ ...{p1}, cam: [{Kc(Fq(0.36), k0)}, {Kc(Fq(0.6) + ' - 1', k1)}], nocut: true, vary: false, glide: true, glideN: 34 }}, {{ ...{p2}, glide: true, glideN: 34 }}"   # ida e volta do detalhe mais lentas (o controle de camera reprova deslize brusco)
    if b.get('_shots'): call = call.replace(', actors: [', f", shots: [{', '.join(b['_shots'])}], actors: [")   # quadros dos tiros: o soldado de fuzil aponta a arma nesses instantes
    if b.get('set') and b['set'] != SET and b['set'] in SETS_X: call = ''.join(pt_ if i_ % 2 else re.sub(r'\bX\b', 'X_' + b['set'], pt_) for i_, pt_ in enumerate(re.split(r'("(?:[^"\\]|\\.)*")', call)))   # esta cena acontece em outro cenario (troca X so' no codigo, nunca dentro de texto: "RAIO X" ficava "RAIO X_hall")
    return call

_ANIM_OK = {'cavalo': 'horse', 'cavalos': 'horse', 'urso': 'bear', 'ursos': 'bear', 'porco': 'pig', 'porcos': 'pig', 'galinha': 'chicken', 'galinhas': 'chicken', 'emu': 'emus', 'emus': 'emus', 'ganso': 'chicken', 'gansos': 'chicken', 'vaca': 'cow', 'vacas': 'cow', 'boi': 'cow', 'bois': 'cow', 'cachorro': 'dog', 'cachorros': 'dog', 'cao': 'dog', 'caes': 'dog', 'gato': 'cat', 'gatos': 'cat', 'ovelha': 'sheep', 'ovelhas': 'sheep', 'cabra': 'goat', 'cabras': 'goat', 'bode': 'goat', 'burro': 'donkey', 'burros': 'donkey', 'jumento': 'donkey', 'veado': 'deer', 'veados': 'deer', 'cervo': 'deer', 'cervos': 'deer', 'raposa': 'fox', 'raposas': 'fox', 'lobo': 'wolf', 'lobos': 'wolf', 'coelho': 'rabbit', 'coelhos': 'rabbit', 'leao': 'lion', 'leoes': 'lion', 'elefante': 'elephant', 'elefantes': 'elephant', 'pato': 'duck', 'patos': 'duck', 'galo': 'rooster', 'galos': 'rooster', 'gaivota': 'gull', 'gaivotas': 'gull'}   # todos os modelos de web/assets/animals/catalog.json
_ANIM_ALL = r'\b(cavalo|cavalos|vaca|vacas|boi|bois|cachorro|cachorros|cao|caes|gato|gatos|ovelha|ovelhas|galinha|galinhas|porco|porcos|emu|emus|ganso|gansos|urso|ursos|lobo|lobos|elefante|elefantes|camelo|camelos|burro|burros|jumento|pato|patos|galo|galos|gaivota|gaivotas|cabra|cabras|bode|veado|veados|cervo|cervos|raposa|raposas|leao|leoes|coelho|coelhos|rato|ratos|pombo|pombos)\b'
_nz0 = lambda t: re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode())
for _b in beats:   # ANIMAL CITADO = ANIMAL 3D EM CENA, sozinho (biblioteca web/assets/animals + aves 2D); nunca modelar animal que ja existe
    if _b.get('animals') or _b.get('emus') or _b.get('animais') is False or _b.get('mapa'): continue
    _sp = list(dict.fromkeys(_ANIM_OK[a_] for a_ in re.findall(_ANIM_ALL, _nz0(_b['say'])) if a_ in _ANIM_OK))
    if 'emus' in _sp: _b['emus'] = True; _sp.remove('emus')
    if _sp: _b['animals'] = [[sp_, (1.9, -2.3, 2.9)[n_], (0.8, 1.1, 1.5)[n_]] for n_, sp_ in enumerate(_sp[:3])]
for _b in beats:   # DECOLAGEM A RISCA: "decolou/lancado/subiu ao ceu" com foguete/balao em cena -> troca pela versao JA NO AR (com chamas/subindo)
    if re.search(r'decol|levantou voo|lancad|lancou|subiu ao ceu|subiu para o ceu|foi para o espaco|rumo ao espaco', _nz0(_b['say'])):
        for _p in _b.get('props', []):
            _air = {'kit/rocket': 'kit/falcon_air', 'kit/balloon': 'kit/balloon_air', 'kit/tower': 'kit/booster_air'}.get(str(_p[0]))
            if _air and os.path.exists(f'web/assets/library/{_air}.glb'): _p[0] = _air
shots = [build_beat(k, b) for k, b in enumerate(beats)]
A_js = ', '.join(['0'] + [f"WS({starts[k]}, -3)" for k in range(1, len(beats))] + ['TOTAL_F()'])
assets = sorted(set(B.get('assets', []) + re.findall(r'asset: "([^"]+)"', ' '.join(shots)) + [p[0] for b in beats for p in b.get('props', [])] + [b['veiculo'].get('asset', 'vehicles/car') for b in beats if b.get('veiculo')]))

spec = f"""// {B.get('title', ID)} -- GERADO por mkvideo.py a partir de videos/{ID}/beats.json (edite o beats.json, nao este arquivo)
const X = {SETX}, DK = 6;{''.join(f' const X_{n} = {SETS_X[n]};' for n in USED_SETS[1:])}
const WS = (i, off = 0) => TIMING.words[Math.min(i, TIMING.words.length - 1)][0] + off;   // frame em que a palavra de indice i comeca
const A = [{A_js}];
const SPEC = {{
  id: {json.dumps(ID)}, {('exp: '+str(B['exp'])+', ') if 'exp' in B else ''}{('cinf: '+str(B['cinf'])+', ') if 'cinf' in B else ''}vseed: {sum(ord(c) for c in ID) % 6}, cutLen: 54, dissolveN: 7, glideN: 20, creep: 0.003, total: TOTAL_F(), sets: {json.dumps(USED_SETS)}, setx: {{ {SET}: X{''.join(f', {n}: X_{n}' for n in USED_SETS[1:])} }},
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
    # SOM DA INTERACAO: fala de desenho alternando duas vozes (dialogo/discussao), baque no empurrao, risada na comemoracao
    _it = b.get('_inter'); _ac = b.get('_acao'); _q = lambda q_: f"F({a} + int(({e} - {a}) * {q_}))"
    if _it == 'empurrar': c2.append(f"gibber({_q(0.15)}, 5, 250, 0.2); whoosh({_q(0.43)}, 0.3, 0.4); thump({_q(0.47)}, 0.8); gibber({_q(0.62)}, 4, 170, 0.2)")
    elif _it == 'discutir' or _ac == 'discutir': c2.append(f"gibber({_q(0.12)}, 6, 250, 0.2); gibber({_q(0.38)}, 6, 165, 0.2); gibber({_q(0.62)}, 5, 270, 0.22); gibber({_q(0.82)}, 4, 160, 0.2)")
    elif _it == 'cochichar': c2.append(f"gibber({_q(0.25)}, 5, 330, 0.1); gibber({_q(0.6)}, 5, 300, 0.1)")
    elif _ac == 'comemorar' or _it == 'pular': c2.append(f"laughs({_q(0.2)}); laughs({_q(0.6)}, 5, 360)")
    elif _it or _ac == 'conversar': c2.append(f"gibber({_q(0.2)}, 4, {[230, 200, 260][k % 3]}, 0.12); gibber({_q(0.58)}, 4, {[170, 290, 185][k % 3]}, 0.12)")
    if b.get('_chega'): c2.append(f"steps(F({a}), F({a} + 40), 0.12, 0.3)")
    for e2 in b.get('sfx', []):
        name, _, at = e2.partition('@'); at = int(at) if at else 4
        c2.append(f"{name}(F({a} + {at}))" if name not in ('steps', 'sea', 'gulls', 'birds') else f"{name}(F({a} + {at}), F({e}))")
for wi, nm in KWSFX: c2.append(f"{nm}(F(int(_W({wi}))))")
# ---------- PRE-PRODUCAO: o que o roteiro pede ANTES de animar (cenario, personagens, objetos, plano e acao de cada cena; o que falta modelar) ----------
_lib = lambda as_: as_ in ('barrel', 'crate', 'cannon') or as_.startswith('mk/') or os.path.exists(f'web/assets/library/{as_}.glb')
_pre = ['# Pre-producao - ' + str(B.get('title', ID)), '', 'Leia ANTES de renderizar. Tudo que estiver em "FALTA" deve ser modelado no Blender (blender/make_*.py) ou trocado no roteiro.', '',
        'Cena | Cenario | Plano | Personagens | Acao dos personagens | Objetos em cena | Na mao | Falta', '---|---|---|---|---|---|---|---']
_falt_all = set()
for k, b in enumerate(beats):
    sp_ = re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode())
    objs = [str(p_[0]) for p_ in b.get('props', [])] + b.get('_auto_obj', []) + [a_[0] for a_ in b.get('animals', [])] + (['emus'] if b.get('emus') else []) + ([b['veiculo'].get('asset', 'carro')] if b.get('veiculo') else [])
    falta = sorted(set(_sem_modelo(re.findall(FALTA_MODELAR, sp_))) | {o_ for o_ in objs if '/' in o_ and not _lib(o_)}); _falt_all |= set(falta)
    maos = [w.split(':')[3] for w in b.get('who', []) if len(w.split(':')) > 3]
    acao = ', '.join(x for x in ((b.get('_acao') or ''), ('INTERAGEM: ' + b['_inter'] if b.get('_inter') else ''), ('alguem chega andando' if b.get('_chega') else ''), ('andando' if b.get('shot') == 'track' or b.get('move') else ''), ('batalha' if b.get('impact') else '')) if x) or ('usa o objeto da mao' if maos else 'parados (so fala e pisca)')
    npers = len(b.get('who', [])) + int((b.get('crowd') or {}).get('n', 0))
    _pre.append(f"b{k} | {'interior ' + str(b['interior']) if b.get('interior') else b.get('set', SET)} | {b.get('shot')} | {npers} | {acao} | {', '.join(dict.fromkeys(objs)) or '-'} | {', '.join(maos) or '-'} | {', '.join(falta) or '-'}")
_par = sum(1 for l_ in _pre if 'parados (so fala e pisca)' in l_)
_nm = sum(1 for b in beats if b.get('impact')); _nh = sum(1 for b in beats if HEROI and (HEROI in [str(p_[0]) for p_ in b.get('props', [])] + b.get('_auto_obj', []) or any(re.sub(r'_(red|yellow|purple|striped)$', '', str(p_[0])) == re.sub(r'_(red|yellow|purple|striped)$', '', HEROI) for p_ in b.get('props', [])))); _nd = sum(1 for b in beats if b.get('_det_heroi'))
_pre += ['', f'OBJETO HEROI: {HEROI or "nenhum achado (ponha \"heroi\": \"kit/...\" no topo do roteiro)"}' + (f' - aparece em {_nh} cena(s), close nele em {_nd}' + ('  << AVISO: sem close no objeto heroi' if not _nd else '') if HEROI else ''), f'GRANDES MOMENTOS (plano aberto com multidao, efeito e som): {_nm}' + ('  << AVISO: menos de 2' if _nm < 2 else '') + ' -> ' + ', '.join(f'b{i}' for i, b in enumerate(beats) if b.get('impact')), 'Interacoes entre personagens: ' + (', '.join(f"b{i} {b['_inter']}" for i, b in enumerate(beats) if b.get('_inter')) or 'nenhuma')]
_pre += ['', f'Cenas com personagens parados: {_par} de {len(beats)}' + (' -> ponha "acao": "conversar|discutir|comemorar|dancar", um objeto na mao ou alguem chegando' if _par > len(beats) // 3 else ''), 'FALTA MODELAR: ' + (', '.join(sorted(_falt_all)) if _falt_all else 'nada')]
open(f'stories/{ID}/preproducao.md', 'w', encoding='utf-8').write('\n'.join(_pre) + '\n')
print(f"pre-producao: {_par} cena(s) com personagens parados de {len(beats)}; falta modelar: {', '.join(sorted(_falt_all)) or 'nada'} (stories/{ID}/preproducao.md)")
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
_tw = sum(len(b['say'].split()) for b in beats) or 1; _mx = {'close': 0.0, 'medio': 0.0, 'aberto': 0.0, 'detalhe': 0.0}
for b in beats:
    w_ = len(b['say'].split()) / _tw; sh_ = b.get('shot')
    if b.get('_detalhe'): _mx['detalhe'] += w_ * 0.24; w_ *= 0.76
    if b.get('impact') and sh_ in WIDE: _mx['close'] += w_ * 0.2; _mx['medio'] += w_ * 0.46; _mx['aberto'] += w_ * 0.34   # sequencia de acao: preparo, close, travelling, grua
    elif sh_ in WIDE: _mx['aberto'] += w_ * (0.6 if sh_ == 'reveal' else 1.0); _mx['medio'] += w_ * (0.4 if sh_ == 'reveal' else 0.0)
    elif sh_ == 'close' or b.get('perto'): _mx['close'] += w_
    else: _mx['medio'] += w_
_mix = ' | '.join(f"{k_} {round(v_ * 100)}%" for k_, v_ in _mx.items()); _nw = sum(1 for b in beats if b.get('shot') in WIDE)
_av = [m for c, m in ((_mx['aberto'] > 0.38, 'aberto demais (personagem pequeno por muito tempo)'), (_nw < int(B.get('min_wide', 2)), 'menos de 2 planos abertos'), (_mx['close'] < 0.06, 'quase sem close (ponha "shot": "close" numa fala ou reacao)'), (_mx['detalhe'] < 0.02 and len(beats) >= 8, 'sem detalhe de objeto (ponha um objeto em "props" ou um "text" numa cena de 11+ palavras)')) if c]
_pl += ['', f'Mistura de planos: {_mix}  (canal: close 10% | medio+corpo 67% | aberto 19% | detalhe 5-15%)', f'Planos abertos: {_nw}' + (' | AVISOS: ' + '; '.join(_av) if _av else ' | dentro do padrao do canal')]
print('mistura de planos:', _mix, ('| AVISO: ' + '; '.join(_av)) if _av else '| ok')
open(f'stories/{ID}/plano.md', 'w', encoding='utf-8').write('\n'.join(_pl) + '\n')
print(f'plano de acao: {len(PLANO)} palavras-chave com efeito + som; {_sem} palavra(s) de acao sem efeito (veja stories/{ID}/plano.md e ponha "fx"/"sfx"/objeto/batalha na cena)')
open(f'stories/{ID}/cues.py', 'w', encoding='utf-8').write('\n'.join(c1) + '\n#--SFX--\n' + '\n'.join(c2) + '\n')
print(f'{ID}: {len(beats)} cenas, {n} palavras narradas -> stories/{ID}/spec.js, cues.py')

# ---------- DUAS FOLHAS (ordem do Gibson): folha1_roteiro.md = historia, narracao, som e efeitos; folha2_producao.md = coordenadas de producao (cenario, camera, personagens, objetos, interacao) + RISCOS de cada cena e como corrigir NO ROTEIRO ----------
_nz = lambda t: re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode())
_CAM = {'two': 'plano medio nos dois; camera empurra devagar e muda de angulo a cada ~2 s', 'close': 'close no rosto; empurra devagar', 'group': 'plano de grupo (corpo inteiro); angulo muda a cada ~2 s', 'low': 'camera baixa, dramatica (virada)', 'reveal': 'ABERTO: grua subindo e abrindo para mostrar o lugar (tomada continua)', 'crowd': 'ABERTO: multidao; em batalha vira sequencia de 4 cameras (preparo, close das armas, travelling, grua)', 'orbit': 'ABERTO: camera girando em volta da acao (tomada continua)', 'track': 'travelling lateral acompanhando quem anda', 'wide': 'ABERTO fixo'}
def _redondo(as_):   # objeto do kit feito com blender/formas.py (malha 'red_...') = formato bonito; senao e' objeto montado com caixas (estilo Minecraft)
    f_ = f'web/assets/library/{as_}.glb'
    if not as_.startswith('kit/') or not os.path.exists(f_): return True
    if re.search(r'kit/(room_|porch|grave|cross|throne|stall|microwave|tulip_bed$)', as_): return True   # movel/construcao: quadrado e' o formato normal
    try:
        d_ = open(f_, 'rb').read(); n_ = int.from_bytes(d_[12:16], 'little'); j_ = json.loads(d_[20:20 + n_].decode('utf-8', 'ignore'))
        return any(str(m_.get('name', '')).startswith('red_') for m_ in j_.get('meshes', []))
    except Exception: return True
_VARN = ['frente', '3/4 pela direita, mais perto e mais baixo', '3/4 pela esquerda, mais alto e aberto', 'leve direita, perto', 'esquerda alta, aberto', 'direita baixa']
_STOPW = set('guerra causa vezes tempo coisa hora horas dias anos meses semanas noite manha tarde vida nada tudo todo toda todos todas mesmo mesma outro outra outros outras nome meio parte lado fim final verdade volta ideia ordem resposta historia mundo pais paises primeiro segundo terceiro ultimo unica unico dele dela deles delas quem qual onde quando para pelo pela entre sobre depois antes ainda apenas quase muito pouco mais menos maior menor inteiro inteira troca conta hoje nunca sempre'.split())
def _riscos(k, b):
    t = _nz(b['say']); nw = len(b['say'].split()); sh = b.get('shot'); R = []; cen = b.get('set', SET)
    if re.search(r'desembarc|barcos? cheg|navios? cheg|chegaram? de (barco|navio)|atravess\w* o (rio|mar|lago|canal)|ancor|zarp', t) and sh not in WIDE: R.append(('chegada/travessia pela agua em plano fechado: nao da para ver barco nem desembarque', '"shot": "reveal", "set": "harbor" nesta cena (plano aberto no cais, navios ao fundo)'))
    if re.search(r'\b(rio|lago|mar|praia|ilha|costa|porto|cais|oceano)\b', t) and cen not in ('harbor', 'palace') and not b.get('interior') and not b.get('mapa'): R.append((f'a narracao cita agua e o cenario "{cen}" nao tem agua', '"set": "harbor" (cais com mar e navio) ou "set": "palace" (praia), ou "mapa" para so situar'))
    an = sorted(set(re.findall(_ANIM_ALL, t)))
    for a_ in an:
        if a_ not in _ANIM_OK: R.append((f'animal sem modelo: {a_}', 'modelar o animal antes, ou tirar da narracao desta cena, ou mostrar so a reacao das pessoas'))
        elif not (b.get('animals') or b.get('emus')): R.append((f'{a_} citado e nao esta em cena', '"animals": [["' + _ANIM_OK[a_] + '", 1.6, 0.6]]' if _ANIM_OK[a_] != 'emus' else '"emus": true'))
    m_ = re.findall(r'\b(nadou|nadaram|nadando|cavalg\w+|montou|montaram|escalou|escalaram|mergulh\w+|voou|voaram|ajoelh\w+|deitou|dormiu|dormiam|sentou|sentaram|subiu|subiram|pulou no|cavou|cavaram)\b', t)
    if m_ and not b.get('impact') and not b.get('caminhoes'): R.append((f'acao sem animacao propria: {", ".join(sorted(set(m_)))}', 'mostrar o RESULTADO (objeto em cena, reacao, efeito + som) ou reescrever a frase com acao que a ferramenta faz (andar, chegar, discutir, empurrar, entregar, comemorar, atirar, fugir)'))
    # SEGUIR O ROTEIRO A RISCA (ordem do Gibson: 100% do que a narracao diz acontece na tela) -- cada familia de palavra EXIGE a acao correspondente
    if re.search(r'queim|incendi|\bfogo\b|em chamas|\bchamas\b', t) and not re.search(r'abriram fogo|abriu fogo|fogo amigo|cessar fogo|arma de fogo|lanca ?chamas|extintor', t) and not b.get('_fogo'): R.append(('a narracao fala de FOGO e nao ha fogo em cena', 'tirar "interior"/"fogo": false desta cena (as labaredas entram sozinhas em cena externa) e por tocha na mao de quem ateia: "who": ["GAU:0:angry:torch", ...]'))
    if re.search(r'\bbatalha|\blutaram|\blutou|\batacaram|\batacou|\bataque\b|\bcombate|\binvadiram|\binvadiu|\binvadido|bombarde|\bguerrearam|tiroteio', t) and not (b.get('impact') or b.get('batalha')): R.append(('a narracao fala de BATALHA/ATAQUE e a cena nao encena a luta', '"batalha": true nesta cena (tropa dos dois lados no "crowd", tiros/golpes e gente fugindo); cada batalha citada no roteiro = uma cena com "batalha": true'))
    if re.search(r'explodi|explos|\bbomba', t) and not (b.get('impact') or any(str(e_).startswith('burst') for e_ in b.get('fx', [])) or (re.search(r'\bbomba', t) and not re.search(r'explodi|explos', t) and any('bomb' in str(p_[0]) for p_ in b.get('props', [])))): R.append(('a narracao fala de EXPLOSAO e nao ha explosao', '"fx": ["burst@30"], "sfx": ["cannon@30"] (acerte o numero para o quadro da palavra)'))
    if re.search(r'\bfugiu|\bfugiram|\bcorreu|\bcorreram|debandada|\bfuga\b|bateu em retirada|recuaram', t) and not (b.get('impact') or b.get('shot') == 'track' or b.get('move') or b.get('_chega')): R.append(('a narracao fala de FUGA/CORRERIA e ninguem corre', '"shot": "track" (os personagens atravessam a tela andando/correndo) ou "batalha": true (a tropa foge no plano aberto)'))
    _hats = {str({**PROFISSOES.get(str(B.get('outfits', {}).get(w.split(':')[0], {}).get('profissao', '')).lower(), {}), **B.get('outfits', {}).get(w.split(':')[0], {})}.get('hat', '')) for w in b.get('who', [])}
    for rx_, ok_, pr_ in ((r'\brei\b|\brainha\b|imperador|imperatriz|\bsultao\b|\bprincipe\b', ('crown', 'turban'), 'rei'), (r'\bgeneral\b|almirante|\bcoronel\b|comandante|\bcapitao\b|marechal', ('shako_tall', 'shako', 'helmet'), 'general'), (r'campones|fazendeiro|agricultor|lavrador', ('straw', 'bonnet', 'slouch'), 'agricultor')):
        if re.search(rx_, t) and b.get('who') and not (_hats & set(ok_)) and (b.get('shot') not in WIDE): R.append((f'a narracao cita "{re.search(rx_, t).group(0)}" e ninguem em cena esta vestido a carater', f'por no "who" um personagem com "profissao": "{pr_}" no figurino (coroa/farda/chapeu proprios)'))
    if nw > 26: R.append((f'cena longa ({nw} palavras, ~{round(nw / 2.9)} s no mesmo lugar)', 'dividir em duas cenas com planos diferentes'))
    if nw < 6 and 0 < k < len(beats) - 1: R.append((f'cena curta ({nw} palavras): nao da tempo de ler a acao', 'juntar com a cena vizinha'))
    if len(b.get('who', [])) > 4 and sh not in WIDE: R.append((f'{len(b.get("who", []))} personagens em plano fechado: alguem sai cortado', 'no maximo 3 no "who" (o resto vai em "crowd") ou "shot": "group"'))
    if b.get('interior') and (b.get('batalha') or (b.get('crowd') or {}).get('n', 0) > 6): R.append(('multidao/batalha dentro de sala: nao cabe', 'tirar "interior" desta cena (faz na rua/campo) ou reduzir o "crowd"'))
    if re.search(r'\b(caminhao|caminhoes|trem|carro|carros|carroca|carrocas|aviao|avioes|tanque de guerra|bicicleta)\b', t) and not (b.get('veiculo') or b.get('caminhoes') or any(str(p_[0]).startswith(('vehicles/', 'kit/roadster', 'kit/b2', 'kit/helicopter', 'kit/falcon', 'kit/rocket', 'kit/booster', 'kit/tower', 'kit/balloon')) for p_ in b.get('props', []))): R.append(('veiculo citado e nao aparece', '"veiculo": {"asset": "vehicles/truck"} (ou wagon, locomotive, car, tank, airplane) ou "caminhoes": true na batalha'))
    if k >= 2 and all(not x.get('interior') and x.get('set', SET) == cen and x.get('shot') == sh and [w.split(':')[0] for w in x.get('who', [])] == [w.split(':')[0] for w in b.get('who', [])] for x in (beats[k - 1], beats[k - 2])) and sh not in WIDE: R.append(('3a cena seguida com o mesmo plano, lugar e personagens: fica repetitivo', 'trocar o "shot", levar para "interior" ou trocar quem aparece'))
    fal = _sem_modelo(re.findall(FALTA_MODELAR, t))
    if fal: R.append((f'objeto sem modelo 3D: {", ".join(fal)}', 'modelar em blender/make_objetos.py e por no OBJ_DICT, ou trocar a palavra'))
    if not (b.get('_acao') or b.get('_inter') or b.get('_chega') or b.get('impact') or sh in WIDE or sh == 'track' or any(len(w.split(':')) > 3 for w in b.get('who', []))): R.append(('personagens parados (so falam e piscam)', '"acao": "conversar|discutir|comemorar", "interacao": "empurrar|cochichar|entregar|susto", objeto na mao (4o campo do "who") ou "chega": true'))
    return R
_f1 = ['# FOLHA 1 - ROTEIRO: ' + str(B.get('title', ID)), '', f'Voz: {B.get("voice", "pt-BR-AntonioNeural")} {B.get("rate", "")} | Clima do video: {B.get("mood", "-")} | Cenario base: {SET} | {len(beats)} cenas, {sum(len(b["say"].split()) for b in beats)} palavras (~{round(sum(len(b["say"].split()) for b in beats) / 2.9)} s)', '']
_f2 = ['# FOLHA 2 - PRODUCAO: ' + str(B.get('title', ID)), '', 'Coordenadas de cada cena para modelagem, animacao e camera, com os RISCOS que o roteiro pode causar e a correcao (campo a por em videos/' + ID + '/beats.json). Resolva todos os riscos ANTES de renderizar; depois rode `python3 mkvideo.py ' + ID + '` de novo ate esta folha sair sem risco.', '']
_tot_r = 0; _allr = []
for k, b in enumerate(beats):
    nw = len(b['say'].split()); cen = ('interior ' + str(b['interior'])) if b.get('interior') else b.get('set', SET)
    kw = [f"{w} -> {kind} + som de {_SOM.get(kind, 'efeito')}" for kk, w, kind in PLANO if kk == k]
    _f1 += [f'## Cena b{k}  (~{round(nw / 2.9, 1)} s)', f'- Narracao: {b["say"]}', f'- Som ambiente: {AMB.get(b.get("set", SET)) or "silencio/sala"}' + (' | batalha: tiros e gritos a cena inteira' if b.get('impact') and b.get('tiros') is not False else ''),
            f'- Efeitos sonoros marcados: {", ".join(b.get("sfx", [])) or "-"}', f'- Efeito + som nas palavras-chave: {"; ".join(kw) or "-"}', f'- Efeito visual marcado: {", ".join(b.get("fx", [])) or "-"}',
            f'- Texto na tela: {b.get("text") or "-"}' + (f' | mapa: {b["mapa"]}' if b.get('mapa') else ''), f'- Funcao na historia: {"GANCHO" if k == 0 else "FECHO/PIADA FINAL" if k == len(beats) - 1 else "GRANDE MOMENTO" if b.get("impact") else "VIRADA" if re.match(r"acontece que|na verdade|so que|o problema", _nz(b["say"])) else "desenvolvimento"}', '']
    objs = list(dict.fromkeys([str(p_[0]) for p_ in b.get('props', [])] + b.get('_auto_obj', []) + [a_[0] for a_ in b.get('animals', [])] + (['emus'] if b.get('emus') else []) + ([b['veiculo'].get('asset', 'carro')] if b.get('veiculo') else [])))
    pers = [f"{w.split(':')[0]} (variante {w.split(':')[1] if len(w.split(':')) > 1 else 0}, expressao {w.split(':')[2] if len(w.split(':')) > 2 else 'smile'}" + (f", segura {w.split(':')[3]}" if len(w.split(':')) > 3 else '') + ')' for w in b.get('who', [])]
    R = [] if b.get('riscos_ok') else _riscos(k, b); _tot_r += len(R); _allr += [(k, r) for r in R]
    _f2 += [f'## Cena b{k} - {b["say"][:70]}{"..." if len(b["say"]) > 70 else ""}', f'- Cenario: {cen} | luz: {b.get("hora") or b.get("light") or B.get("light", "day")} | clima: {b.get("clima") or "limpo"}',
            f'- Camera: {b.get("shot")} = {_CAM.get(b.get("shot"), "-")}' + (' + CLOSE NO OBJETO no meio da cena (vai e volta)' if b.get('_detalhe') else '') + (' [momento criado pela ferramenta]' if b.get('_momento_auto') else ''),
            '- Takes: ' + ('4 cameras em sequencia: (1) tropa se preparando, plano medio; (2) close das armas/rostos; (3) travelling lateral pela linha; (4) grua subindo e abrindo com clarao, poeira e som' if b.get('impact') and b.get('shot') in WIDE else '1 tomada continua, sem corte (camera abre/gira devagar)' if b.get('shot') in WIDE else f'{max(1, round(len(b["say"].split()) / 2.9 * 30 / 54))} take(s) de ~1,8 s, deslizando de um para o outro: ' + ' -> '.join(_VARN[(sum(ord(c) for c in ID) % 6 + j) % 6] for j in range(max(1, round(len(b['say'].split()) / 2.9 * 30 / 54))))) + (' | no meio: desliza ate o objeto (close), segura ~1,5 s e volta' if b.get('_detalhe') else ''),
            f'- Personagens principais ({len(b.get("who", []))}): {"; ".join(pers) or "-"}' + (f' | multidao: {b["crowd"].get("n")} de {"/".join(b["crowd"].get("outfits", []))}' if b.get('crowd') else ''),
            f'- Animacao: {b.get("_acao") or "-"}' + (f' | interacao: {b["_inter"]}' if b.get('_inter') else '') + (' | o ultimo personagem ENTRA andando' if b.get('_chega') else '') + (' | batalha encenada' if b.get('impact') else ''),
            f'- Objetos/modelos: {", ".join(o + ("" if _lib(o) or "/" not in o else " (FALTA MODELAR)") for o in objs) or "-"}',
            '- CONFERIR NA FOLHA DE CONTATO (o que a narracao cita tem que aparecer): ' + (', '.join(sorted({w_ for a_, w_ in re.findall(r'\b(um|uma|o|a|os|as|do|da|dos|das|no|na|nos|nas|de|com) ([a-z]{4,})\b', _nz(b['say'])) if w_ not in _STOPW})[:10]) or '-'),
            '- RISCOS: ' + ('nenhum' if not R else ''), *[f'  - {r} -> CORRECAO: {c}' for r, c in R], '']
_glob = []
if not any(b.get('mapa') for b in beats): _glob.append(('nenhum mapa no video (o canal situa o lugar com mapa rapido)', '"mapa": "NOME DO LUGAR" na cena 1 ou 2'))
if sum(1 for b in beats if b.get('impact')) < 2: _glob.append(('menos de 2 grandes momentos', '"batalha": true (ou "impact": true) em duas cenas de acao'))
if HEROI and not any(b.get('_det_heroi') for b in beats): _glob.append((f'objeto heroi ({HEROI}) sem close de camera', 'por o objeto em "props" de uma cena media de 8+ palavras'))
if not HEROI and 'heroi' not in B: _glob.append(('video sem objeto heroi', '"heroi": "kit/<objeto>" no topo do roteiro (modele se nao existir)'))
_cx = sorted({o_ for b in beats for o_ in [str(p_[0]) for p_ in b.get('props', [])] + b.get('_auto_obj', []) if '/' in str(o_) and not _redondo(str(o_))})
if _cx: _glob.append((f'objeto montado com caixas (estilo Minecraft): {", ".join(_cx)}', 'refazer com formas redondas: blender/objetos_<sessao>.py usando blender/formas.py (cil, bola, torno, tubo, arco), mesmo nome de arquivo; rodar o blender e este roteiro de novo'))
if _sem: _glob.append((f'{_sem} palavra(s) de acao sem efeito + som', 'ver plano.md e por "fx"/"sfx" na cena'))
# PARA O BLENDER: tudo que o video precisa em 3D, com o que ja existe e o que tem de ser modelado ANTES de renderizar
_usados = {}
for k, b in enumerate(beats):
    for o_ in dict.fromkeys([str(p_[0]) for p_ in b.get('props', [])] + [x for x in b.get('_auto_obj', []) if '/' in x or x in ('barrel', 'crate', 'cannon', 'ship')] + [a_[0] for a_ in b.get('animals', [])] + (['emu'] if b.get('emus') else []) + ([b['veiculo'].get('asset', 'vehicles/car')] if b.get('veiculo') else [])): _usados.setdefault(o_, []).append(f'b{k}')
_pal = {}
for k, b in enumerate(beats):
    for w_ in _sem_modelo(re.findall(FALTA_MODELAR, _nz(b['say']))) + [a_ for a_ in re.findall(_ANIM_ALL, _nz(b['say'])) if a_ not in _ANIM_OK]: _pal.setdefault(w_, []).append(f'b{k}')
_f2 += ['## PARA O BLENDER (objetos 3D deste video)', 'Regra: todo objeto, utensilio, veiculo e animal que aparece e\' modelo 3D feito no Blender; a ferramenta so\' poe em cena, pinta o contorno e anima. Nada de objeto "quadradao": use `blender/formas.py` (cil, bola, torno, tubo, arco, caixa com chanfro).', '',
        'Objeto | Cenas | Situacao | O que fazer', '---|---|---|---',
        *[f"{o_} | {', '.join(c_)} | {('pronto' if _redondo(o_) else 'CAIXOTE: refazer com formas.py') if (_lib(o_) or '/' not in o_) else 'FALTA'}{' (HEROI: aparece em close)' if HEROI and o_ == HEROI else ''} | {'conferir na folha de contato se le bem; se parecer caixote, refazer com formas.py' if (_lib(o_) or '/' not in o_) else 'modelar antes de renderizar'}" for o_, c_ in _usados.items()],
        *[f"{w_} (citado na narracao) | {', '.join(c_)} | FALTA | pesquisar referencia (referencias/LEIA.md) e modelar: `blender/objetos_<sessao>.py` com formas.py -> `kit/{w_}.glb` (altura real em metros; cores chapadas; partes redondas com cil/bola/torno); cadastrar em `obj_dict.d/<sessao>.json`; `blender -b --python blender/objetos_<sessao>.py`; `python3 capacidades.py`; depois rodar este roteiro de novo" for w_, c_ in _pal.items()],
        '' if (_usados or _pal) else '(nenhum objeto 3D neste video: confira se o roteiro nao esta pobre de elementos)', '']
_f2 += ['## Video inteiro', f'- Objeto heroi: {HEROI or "-"} | grandes momentos: {", ".join(f"b{i}" for i, b in enumerate(beats) if b.get("impact")) or "-"} | planos abertos: {_nw} | mistura: {_mix}', f'- Interacoes: {", ".join(f"b{i} {b[chr(95) + chr(105) + chr(110) + chr(116) + chr(101) + chr(114)]}" for i, b in enumerate(beats) if b.get("_inter")) or "-"}',
         '- RISCOS GERAIS: ' + ('nenhum' if not _glob else ''), *[f'  - {r} -> CORRECAO: {c}' for r, c in _glob], '',
         f'## RESUMO: {_tot_r + len(_glob)} risco(s) em aberto' + ('' if _tot_r + len(_glob) else ' - pode renderizar'), *[f'- b{k}: {r}' for k, (r, c) in _allr], *[f'- geral: {r}' for r, c in _glob], '',
         '## Reparos depois do render', '- Defeito em poucas cenas e narracao igual: corrija o beats.json e `./refazer.sh ' + ID + ' bN bM` (so essas cenas).', '- Mudou narracao, ferramenta ou muitas cenas: `./refazer_tudo.sh ' + ID + '` (render completo).',
         '- Personagem cortado: tire gente do "who" ou use "shot": "group". Cena vazia: confira "who". Objeto fora do quadro: ponha em "props" com x entre -2 e 2. Luz estourada: "hora"/"clima" na cena.']
_f1 += (['', '## Fontes (fatos conferidos)'] + [f'- {u_}' for u_ in B['fontes']]) if B.get('fontes') else []   # "fontes": ["https://...", ...] no topo do beats.json
open(f'stories/{ID}/folha1_roteiro.md', 'w', encoding='utf-8').write('\n'.join(_f1) + '\n'); open(f'stories/{ID}/folha2_producao.md', 'w', encoding='utf-8').write('\n'.join(_f2) + '\n')
print(f'DUAS FOLHAS: stories/{ID}/folha1_roteiro.md (historia e som) e stories/{ID}/folha2_producao.md (producao) -> {_tot_r + len(_glob)} RISCO(S) em aberto' + (': ' + '; '.join([f'b{k} {r}' for k, (r, c) in _allr] + [r for r, c in _glob])[:600] if _tot_r + len(_glob) else ''))

open(f'stories/{ID}/riscos.txt', 'w').write(str(_tot_r + len(_glob) + _sem) + '\n')   # lido por novo_video.sh e conferir.sh
