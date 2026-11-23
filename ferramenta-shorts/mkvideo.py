#!/usr/bin/env python3
"""mkvideo.py <id>  -- FICHA DE CENAS (videos/<id>/beats.json) -> stories/<id>/{script.txt, spec.js, cues.py, meta.json}

O roteiro (frases narradas) e a ficha de cenas ficam num arquivo so'.  A ferramenta cuida do resto:
  voz (edge-tts) -> tempos por palavra -> spec.js (planos, camera, atores, textos) -> cues.py (musica + efeitos) -> ajuste de enquadramento -> gates -> render -> QA -> mp4.
Cada "beat" = uma frase narrada + o que aparece na tela durante ela.  Veja videos/_exemplo/beats.json e README.
"""
import json, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapas')); import mapas as _MAPAS   # mapa de verdade (contorno real do pais)

ID = sys.argv[1]
MODO_CLI = None
if '--modo' in sys.argv:
    _mi = sys.argv.index('--modo')
    if _mi + 1 < len(sys.argv): MODO_CLI = int(sys.argv[_mi + 1])
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
B = json.load(open(f'videos/{ID}/beats.json', encoding='utf-8'))
# CHAMADA FINAL (ordem do Gibson 23/11): TODO video termina com o narrador pedindo o comentario com o tema do proximo video (cena propria, close no personagem principal apontando para quem assiste)
CTA_TXT = B.get('cta_texto') or 'Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?'
if B.get('cta') is not False and B.get('beats') and not any(b_.get('_cta') or 'tema do próximo vídeo' in b_.get('say', '') for b_ in B['beats']):
    _w0 = next((w_ for b_ in B['beats'] for w_ in b_.get('who', []) if not w_.startswith(('POV', 'SOL', 'TRO', 'POVO'))), (B['beats'][0].get('who') or ['X:0'])[0])
    _p0 = _w0.split(':')
    _lb = B['beats'][-1]
    B['beats'].append({'who': [f"{_p0[0]}:{_p0[1] if len(_p0) > 1 else 0}:grin"], 'shot': 'close', 'say': CTA_TXT, 'text': 'COMENTE!', '_cta': True, 'detalhe': False, 'mapa': None,
                       **({'interior': _lb['interior']} if _lb.get('interior') else {'set': _lb.get('set', B.get('set', 'countryside'))}), **({'hora': _lb['hora']} if _lb.get('hora') else {})})
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
    if _b.get('veiculo') is None and _b.get('who') and not _b.get('interior') and not _b.get('batalha') and re.search(r'\bdirig|\bde carro\b|\bde caminhao\b|\bde carroca\b|\bde moto\b|\bpilotou|\bpilotava|\bao volante|\bpedalou|\bpedalava|entr\w* no carro|pegou o carro|no carro\b|de carro\b|subiu no carro|de moto\b|na moto\b|no caminhao\b', _t):
        _as = next((as_ for rx_, as_ in _VEIC if re.search(rx_, _t)), 'kit/carro_redondo')   # carro redondo conversivel (o 'vehicles/car' era quadradao)
        _b['veiculo'] = {'asset': _as, 'motorista': _b['who'][0], 'de': -11, 'para': 11}; _b.setdefault('shot', 'two')
for _b in B['beats']:   # MONTADO (23/11, Gibson: "o soldado correu em cima de um cavalo e atirou"): o personagem da frase vai EM CIMA do cavalo, galopando pela cena
    _t = ' ' + re.sub(r'[^a-z ]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode()) + ' '
    if _b.get('montado') is None and _b.get('who') and not _b.get('interior') and not _b.get('veiculo') and re.search(r'em cima d[eo]s? (um |uma |o |a |seu |sua )?(cavalo|egua|camelo|mula|burro|jumento|elefante|ponei)|a cavalo|montad[oa]s? (n|em)|\bcavalg\w*|\bgalop\w*|no lombo|sobre (um |o |seu )?cavalo', _t):
        _an = 'camel' if 'camelo' in _t else 'elephant' if 'elefante' in _t else 'donkey' if re.search(r'mula|burro|jumento', _t) else 'horse_sela'
        _b['montado'] = {'animal': _an}; _b['correr'] = False; _b.setdefault('shot', 'two')
for _b in B['beats']:   # CORREU/FUGIU (seguir o roteiro): a cena vira plano em movimento e os personagens CORREM
    _t = re.sub(r'[^a-z ]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode())
    if re.search(r'\b(correu|correram|correndo|fugiu|fugiram|fugindo|disparou a correr|sairam correndo|saiu correndo|perseguiu|perseguiram|perseguindo)\b', _t) and _b.get('shot') in (None, 'two', 'group', 'close') and not _b.get('shot_lock') and not _b.get('interior') and not _b.get('veiculo') and _b.get('correr') is not False: _b['shot'] = 'track'
for _b in B['beats']:   # NAVIO CHEGANDO/PARTINDO: plano aberto no cais para ver o navio andar na agua
    _t = re.sub(r'[^a-z ]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode())
    if _b.get('set', SET) in ('harbor', 'palace') and not _b.get('interior') and not _b.get('shot_lock') and re.search(r'\bnavios?\b|\bbarcos?\b|\bfrota\b|\besquadra\b|\bcaravela', _t) and re.search(r'cheg|desembarc|aport|atrac|zarp|partiu|partiram', _t): _b['shot'] = 'reveal'; _b['shot_lock'] = True
for _b in B['beats']:   # MONTANHA: cena que fala de colina/montanha/morro acontece no cenario de montanha
    _t = re.sub(r'[^a-z ]', '', __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode())
    if re.search(r'\bcolinas?\b|\bmontanhas?\b|\bmorros?\b|\bserra\b|\bpenhasco\b|\bencosta\b', _t) and not _b.get('set') and not _b.get('interior') and B.get('montanha_cenario') is not False: _b['set'] = 'mountain'

# ===== VEICULOS (23/11): tamanho real e animacao =====
_VEIC_RX = re.compile(r'(^|/)(carro|car|roadster|cybertruck|truck|taxi|jeep|caminhao|onibus|bus|motorcycle|moto|carro_[a-z0-9]+)')
_EH_VEIC = lambda a_: bool(_VEIC_RX.search(str(a_))) and not re.search(r'carroca|wagon|cart|carrinho|falcon|rocket', str(a_))
_GLEN = {}
_FRENTE = {'carro_redondo': 1, 'carro_50': 1, 'carro_antigo': 1, 'roadster': -1, 'roadster26': -1, 'cybertruck': -1, 'roadster_air': -1, 'roadster26_air': -1}   # frente do modelo: +x ou -x (olhado no Blender 23/11)
_ryv = lambda a_, sg_: 0.0 if _FRENTE.get(str(a_).split('/')[-1], 1) == sg_ else 3.1416   # gira o carro para a FRENTE apontar para onde ele anda
def _glb_len(a_):
    if a_ in _GLEN: return _GLEN[a_]
    L = None
    try:
        import struct as _st
        for pth in (f'web/assets/library/{a_}.glb',):
            if not os.path.exists(pth): continue
            d_ = open(pth, 'rb').read(); l_ = _st.unpack('<I', d_[12:16])[0]; j_ = json.loads(d_[20:20 + l_])
            mn = [1e9] * 3; mx = [-1e9] * 3
            for ac in j_.get('accessors', []):
                if len(ac.get('min', [])) == 3: mn = [min(mn[i], ac['min'][i]) for i in range(3)]; mx = [max(mx[i], ac['max'][i]) for i in range(3)]
            L = max(mx[0] - mn[0], mx[2] - mn[2]) if mx[0] > -1e8 else None
    except Exception: L = None
    _GLEN[a_] = L; return L
# ===== VARIEDADE DE CENARIO (ordem do Gibson 19/11: "cada video tem que ter cenarios diferentes") =====
# 1) a narracao escolhe o lugar da cena; 2) nenhum lugar ocupa mais da metade do video e todo video tem pelo menos 3 lugares
_EXPL = {i_ for i_, b_ in enumerate(B['beats']) if b_.get('set') or b_.get('interior')}   # o que o roteiro fixou nao muda
_LUGAR = ((r'desert|areia|egito|egipci|piramide|arabia|saara|australia|faraó|farao|seca\b|caravana', 'set', 'outback'),
          (r'florest|selva|amazon|\bmata\b|tribo|aldeia|indigena', 'set', 'jungle'),
          (r'castelo|cavaleir|medieval|reino\b|rainha|imperador|\bcorte\b|trono', 'set', 'medieval'),
          (r'estadio|torcida|futebol|\bpartida\b|ringue|\bluta\b|campeonato|\bcopa\b|lutador|luta livre|\barena\b|plateia|nocaute', 'set', 'stadium'),
          (r'fazenda|\bcampo\b|plantac|colheit|lavoura|agricult|\bsitio\b|pasto', 'set', 'countryside'),
          (r'palacio|congresso|parlamento|\bonu\b|assembleia|tribunal|senado|discurso|coletiva|casa branca|gabinete', 'interior', 'pedra'),
          (r'hospital|enfermaria|pronto.socorro|\buti\b|internad|cirurgia|\bmaca\b|leito|maternidade|clinica|paciente|enfermeir|parteir|\bparto\b', 'interior', 'hospital'),
          (r'galpao|hangar|armazem|oficina|base de testes|linha de montagem|fabrica de foguete', 'interior', 'galpao'),
          (r'escritorio|empresa\b|reuniao|laboratorio|\bloja\b|mercado|padaria|\bbanco\b|restaurante|bar\b|fabrica\b|fabricas\b', 'interior', 'loja'),
          (r'(?<!para )\bcasa\b|\bsala\b|quarto|cozinha|familia|jantar', 'interior', 'madeira'),
          (r'\bpraia\b|\bareia\b|\bcosta\b|desembarc|\bcais\b|\bporto\b|navios?\b', 'set', 'harbor'),
          (r'\bcidade\b|\bruas?\b|predio|avenida|transito|metro\b|bairro', 'set', 'street'))
for i_, _b in enumerate(B['beats']):
    if i_ in _EXPL or _b.get('mapa') or B.get('variar_cenario') is False: continue
    _t = __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode()
    for rx_, k_, v_ in _LUGAR:
        if re.search(rx_, _t):
            _b['_lug_ok'] = True   # a narracao CITOU o lugar: a variedade nunca tira a cena dele (estadio lotado continua no estadio)
            if k_ == 'interior' and (_b.get('shot') in ('reveal', 'crowd', 'orbit', 'track') or _b.get('batalha') or _b.get('veiculo') or _b.get('crowd')): continue
            if k_ == 'set' and v_ == SET: break
            if _b.get(k_) is False: break   # o roteiro proibiu (interior: false): o lugar citado nao manda a cena para dentro
            _b[k_] = v_; break
_tema = __import__('unicodedata').normalize('NFKD', ' '.join(b_['say'] for b_ in B['beats'][:3]).lower()).encode('ascii', 'ignore').decode()
if re.search(r'hospital|maternidade|enfermaria|clinica', _tema) and B.get('hospital') is not False:   # historia que se passa num hospital: as salas sao o hospital (branco, macas), nao a sala marrom
    for b_ in B['beats']:
        if b_.get('interior') in ('madeira', 'pedra'): b_['interior'] = 'hospital'
_ALT = {'street': ['interior loja', 'harbor', 'countryside', 'interior madeira', 'interior pedra'], 'harbor': ['street', 'interior madeira', 'countryside', 'interior loja'],
        'countryside': ['mountain', 'interior madeira', 'street', 'harbor', 'interior pedra'], 'outback': ['mountain', 'interior pedra', 'countryside', 'street'],
        'palace': ['interior pedra', 'street', 'harbor', 'countryside'], 'jungle': ['harbor', 'mountain', 'interior madeira', 'countryside'], 'medieval': ['interior pedra', 'countryside', 'mountain', 'interior madeira'],
        'arctic': ['harbor', 'interior madeira', 'mountain', 'interior pedra'], 'mountain': ['countryside', 'interior madeira', 'outback', 'street'], 'stadium': ['street', 'interior loja', 'countryside', 'interior madeira'],
        'hall': ['street', 'interior pedra', 'harbor', 'countryside']}
_lug = lambda b_: ('interior ' + str(b_['interior'])) if b_.get('interior') else b_.get('set', SET)
_N = len(B['beats'])
_MINL = 4 if _N >= 9 else 3; _MAXD = max(2, -(-_N // 3)) if _N >= 9 else _N // 2   # 23/11 (Gibson: "cenario repetindo pra caramba"): >=4 lugares e nenhum em mais de 1/3 do video
if _N >= 6 and B.get('variar_cenario') is not False:
    for _volta in range(6):
        _cont = __import__('collections').Counter(_lug(b_) for b_ in B['beats'])
        _dom, _qt = _cont.most_common(1)[0]
        if len(_cont) >= _MINL and _qt <= _MAXD: break
        _livres = [i_ for i_, b_ in enumerate(B['beats']) if _lug(b_) == _dom and i_ not in _EXPL and not b_.get('_lug_ok') and i_ not in (0, _N - 1) and not b_.get('mapa')]
        _opc = [o_ for o_ in _ALT.get(_dom.replace('interior ', ''), _ALT['street']) if o_ not in _cont] or _ALT.get(SET, _ALT['street'])
        _bl = [_livres[j_:j_ + 2] for j_ in range(0, len(_livres), 2)]
        _bl = _bl[1::2] + _bl[0::2]   # blocos de 2 cenas seguidas, primeiro um sim um nao (o lugar muda junto com a historia)
        for n_, bl_ in enumerate(_bl):
            if _cont[_dom] <= _MAXD and len(_cont) >= _MINL: break
            o_ = _opc[n_ % len(_opc)]
            for i_ in bl_:
                b_ = B['beats'][i_]
                _o = o_
                if _o.startswith('interior') and (b_.get('shot') in ('reveal', 'crowd', 'orbit', 'track') or b_.get('batalha') or b_.get('veiculo') or b_.get('crowd') or b_.get('props')):
                    _o = next((x_ for x_ in _opc if not x_.startswith('interior')), 'harbor')
                if _o.startswith('interior'): b_['interior'] = _o.split()[1]
                else: b_['set'] = _o
                _cont[_dom] -= 1; _cont[_o] += 1
for _b in B['beats']:
    if _b.get('interior') and not _b.get('set'): _b['set'] = 'hall'      # interior fica no cenario 'hall' (sem arbusto/pedrinha de area externa)
USED_SETS = [SET] + sorted({b['set'] for b in B['beats'] if b.get('set') and b['set'] != SET and b['set'] in SETS_X})   # cenario por cena: "set" dentro do beat
# ===== CIDADE DA REGIAO (ordem do Gibson 19/11): os predios de fundo seguem o pais/epoca da historia =====
# "regiao" no topo do roteiro (europa, franca, holanda, eua, oriente, colonial, japao, russia, africa, classico) ou deduzida do "mapa"/titulo/narracao.
_REG_PAIS = (('franca', r'franc|paris'), ('holanda', r'holand|amsterd|paises baixos'),
    ('eua', r'estados unidos|\beua\b|america\b|nova york|california|texas|florida|maine|chicago|los angeles|washington|hollywood|las vegas|ohio|michigan|toledo|detroit|nova jersey|boston|filadelfia|virginia|georgia|alabama|kansas|nebraska|iowa|oregon|montana|colorado|arizona|nevada|novo mexico|alasca|havai|pensilvania|massachusetts|tennessee|kentucky|missouri|minnesota|wisconsin|illinois|indiana|carolina|louisiana|mississippi|oklahoma|utah|idaho'),
    ('oriente', r'egito|egipc|\bira\b|\birao\b|iraque|arabia|marrocos|turquia|israel|palestin|dubai|siria|jordania|persia|babilon|meca|cairo'),
    ('colonial', r'brasil|pernambuco|recife|bahia|rio de janeiro|sao paulo|minas|mexic|el salvador|peru|argentin|colombia|cuba|venezuel|chile|portugal|lisboa|espanha|madri|bolivia|paraguai|uruguai|honduras|guatemala'),
    ('japao', r'japa|toquio|china|chines|coreia|pequim|xangai'), ('russia', r'russi|ucrani|moscou|sibéria|siberia|soviet'),
    ('africa', r'africa|zanzibar|quenia|nigeria|gana|mali|etiopia|congo|angola|mocambique|somalia|sudao|tanzania'),
    ('classico', r'roma antiga|grecia antiga|romanos|imperio romano|atenas|esparta|cesar\b|gladiador'),
    ('europa', r'polon|alemanh|hungri|austri|romeni|belgic|inglaterr|londres|escoci|irland|italia|suic|bulgari|grecia|servia|croacia|tchec|europa|prussia|suecia|noruega|dinamarca|finland|bosnia|islandia|escandinav|viking|medieval'))
_REG_BASE = {'buildings/house_small': 1, 'buildings/house_two': 2, 'buildings/house_blue': 1, 'buildings/shop': 3, 'buildings/apartment': 1, 'buildings/church': 3, 'buildings/barn': 1}
_REG_N = {'europa': 3, 'franca': 3, 'holanda': 3, 'eua': 3, 'oriente': 3, 'colonial': 3, 'japao': 3, 'russia': 2, 'africa': 2, 'classico': 2}
_REG_CHAO = {'europa': '#b9a99a', 'franca': '#cfc6b6', 'holanda': '#b07a62', 'eua': '#8a8c93', 'oriente': '#e6c99a', 'colonial': '#d2b892', 'japao': '#bdb5a6', 'russia': '#a8a39a', 'africa': '#c98e5a', 'classico': '#e2d8c4'}
REGIAO = B.get('regiao')
if REGIAO is None:
    _rt = __import__('unicodedata').normalize('NFKD', (' '.join(str(b_.get('mapa') or '') for b_ in B['beats']) + ' ' + B.get('title', '') + ' ' + ' '.join(b_['say'] for b_ in B['beats'][:4])).lower()).encode('ascii', 'ignore').decode()
    REGIAO = next((r_ for r_, rx_ in _REG_PAIS if re.search(rx_, _rt)), None)
    _ano = re.search(r'(?<![0-9])(1[0-9]{3}|20[0-9]{2})(?![0-9])', B.get('title', '') + ' ' + ID)   # 19/11: 'toledo1835' nao casava com \b (cidade de 1835 ganhava predio moderno dos EUA)
    if REGIAO == 'eua' and _ano and int(_ano.group(1)) < 1850: REGIAO = 'colonial'
    if REGIAO in ('europa', None) and _ano and int(_ano.group(1)) < 500 and re.search(r'roma|grec|cesar|gladiad', _rt): REGIAO = 'classico'
_regmap = {}
if REGIAO in _REG_N:
    _ks = [f'kit/rg_{REGIAO}_{i}' for i in range(1, _REG_N[REGIAO] + 1)]
    for b_, i_ in _REG_BASE.items(): _regmap[b_] = _ks[i_ - 1:] + _ks[:i_ - 1]
    _regmap['buildings/castle_tower'] = [_ks[-1]]
    if REGIAO not in ('holanda', 'europa'): _regmap['buildings/windmill'] = [_ks[0]]
# ===== MARCOS DO LUGAR (19/11): a historia no Egito tem as piramides ao fundo, no Cabo Canaveral a plataforma de lancamento... =====
_MARCOS = ((r'cabo canaveral|plataforma de lancamento|base de lancamento|kennedy space|falcon|foguete da spacex', 'kit/marco_canaveral', 16, -42, 1.0),
           (r'starbase|boca chica|mechazilla|base de testes? da spacex', 'kit/tower', 18, -60, 4.0),
           (r'alexandria|eratostenes', 'kit/marco_alexandria', 20, -80, 1.0),
           (r'piramide|egito|egipc|\bgize\b|farao|\bcairo\b|esfinge', 'kit/marco_piramides', 22, -78, 1.6),
           (r'londres|big ben|tamisa', 'kit/marco_bigben', 16, -58, 1.0),
           (r'versalhes|versailles|maria antonieta|luis xvi|montgolfier', 'kit/marco_versalhes', 0, -90, 1.0),
           (r'\bparis\b|torre eiffel', 'kit/marco_eiffel', 18, -66, 1.1), (r'\bparis\b|notre.dame', 'kit/marco_notredame', 18, -70, 1.0),
           (r'\bonu\b|nacoes unidas', 'kit/marco_onu', 20, -110, 0.7),
           (r'trump tower|o aprendiz', 'kit/marco_trumptower', 18, -90, 0.8),
           (r'nova york|estatua da liberdade|manhattan', 'kit/marco_liberdade', 20, -70, 1.0), (r'\broma\b|coliseu|gladiador', 'kit/marco_coliseu', 0, -82, 1.0),
           (r'rio de janeiro|cristo redentor|corcovado', 'kit/marco_cristo', 24, -96, 1.2),
           (r'casa branca|washington|presidente dos estados unidos|presidente americano|biden|obama', 'kit/marco_casabranca', 18, -70, 1.0),
           (r'capitolio|congresso americano', 'kit/marco_capitolio', 18, -80, 1.0), (r'hollywood|los angeles|california|hawthorne', 'kit/marco_hollywood', 0, -110, 1.0),
           (r'sao francisco|san francisco|golden gate|vale do silicio|palo alto|twitter', 'kit/marco_goldengate', 0, -120, 1.0), (r'\bberlim|brandemburgo', 'kit/marco_brandemburgo', 18, -70, 1.0),
           (r'\bpisa\b|toscana|florenca', 'kit/marco_pisa', 20, -70, 1.0), (r'modena|bolonha', 'kit/marco_ghirlandina', 20, -70, 1.0),
           (r'\bviena\b|austria|estrasburgo|\bgante\b|\bgent\b|catedral gotica', 'kit/marco_viena', 20, -80, 1.0), (r'bruxelas', 'kit/marco_atomium', 20, -80, 1.0), (r'waterloo', 'kit/marco_waterloo', 0, -110, 1.0),
           (r'suica|\balpes\b|genebra|zurique|alasca|kiska', 'kit/marco_alpes', 0, -110, 1.0), (r'\bmaias?\b|chichen|yucatan', 'kit/marco_chichenitza', 20, -80, 1.0),
           (r'veracruz|ulua', 'kit/marco_ulua', 0, -100, 1.0), (r'el salvador|san salvador|vulcao', 'kit/volcano', 0, -120, 9.0),
           (r'moscou|kremlin|praca vermelha', 'kit/marco_saobasilio', 20, -80, 1.0), (r'sydney', 'kit/marco_operasydney', 0, -100, 1.0), (r'zanzibar', 'kit/marco_zanzibar', 18, -80, 1.0),
           (r'teera|\bira\b|\birao\b|istambul|constantinopla|mesquita', 'kit/marco_mesquita', 20, -80, 1.0), (r'olinda|recife|pernambuco', 'kit/marco_olinda', 20, -90, 1.0),
           (r'\btexas\b', 'kit/marco_texas', 20, -90, 1.0), (r'\bmexico\b|mexicano|tequila', 'kit/marco_mexico', 20, -90, 1.0), (r'detroit', 'kit/marco_detroit', 0, -120, 1.0),
           (r'wurzburg|rontgen|roentgen', 'kit/marco_wurzburg', 0, -100, 1.0), (r'rostock|tycho', 'kit/marco_rostock', 20, -90, 1.0),
           (r'amsterd|holand|paises baixos|den helder|\btexel\b', 'kit/marco_amsterdam', 0, -70, 1.0), (r'\byap\b|pedras? rai', 'kit/marco_yap', 0, -40, 1.0))   # 3a leva (19/11): blender/objetos_marcos3.py
# o marco so' aparece se JA EXISTIA no ano da historia (Torre Eiffel 1889, Estatua da Liberdade 1886, Golden Gate 1937...); o Farol de Alexandria caiu em 1323
_MARCO_ANO = {'kit/marco_detroit': (1977, 9999), 'kit/marco_texas': (1888, 9999), 'kit/marco_mexico': (1791, 9999), 'kit/marco_wurzburg': (1744, 9999), 'kit/marco_amsterdam': (1631, 9999), 'kit/marco_rostock': (1290, 9999), 'kit/marco_eiffel': (1889, 9999), 'kit/marco_liberdade': (1886, 9999), 'kit/marco_goldengate': (1937, 9999), 'kit/marco_hollywood': (1923, 9999), 'kit/marco_atomium': (1958, 9999),
              'kit/marco_operasydney': (1973, 9999), 'kit/marco_cristo': (1931, 9999), 'kit/marco_brandemburgo': (1791, 9999), 'kit/marco_bigben': (1859, 9999), 'kit/marco_canaveral': (1950, 9999),
              'kit/marco_casabranca': (1800, 9999), 'kit/marco_capitolio': (1800, 9999), 'kit/marco_onu': (1952, 9999), 'kit/marco_trumptower': (1983, 9999), 'kit/marco_versalhes': (1682, 9999),
              'kit/marco_waterloo': (1826, 9999), 'kit/marco_zanzibar': (1883, 9999), 'kit/marco_alexandria': (-300, 1323), 'kit/marco_notredame': (1260, 9999), 'kit/tower': (2019, 9999)}
_mt = __import__('unicodedata').normalize('NFKD', (B.get('title', '') + ' ' + ' '.join(str(b_.get('mapa') or '') for b_ in B['beats']) + ' ' + ' '.join(b_['say'] for b_ in B['beats'][:3])).lower()).encode('ascii', 'ignore').decode()   # so o LUGAR da historia (titulo, mapa, comeco), nao qualquer citacao
_anoM2 = re.search(r'(?<!\d)(1[0-9]{3}|20[0-9]{2})(?!\d)', ' '.join([str(B.get('ano', '')), B.get('title', ''), ID] + [str(b_.get('text', '')) for b_ in B['beats'][:4]])); _ANO_M = int(_anoM2.group(1)) if _anoM2 else (int(B['ano']) if str(B.get('ano', '')).lstrip('-').isdigit() else None)
MARCO = None if B.get('marco') is False else (B.get('marco') or next(((a_, dx_, z_, s_) for rx_, a_, dx_, z_, s_ in _MARCOS if re.search(rx_, _mt) and (_ANO_M is None or _MARCO_ANO.get(a_, (-9999, 9999))[0] <= _ANO_M <= _MARCO_ANO.get(a_, (-9999, 9999))[1])), None))
if MARCO and isinstance(MARCO, str): MARCO = next(((a_, dx_, z_, s_) for rx_, a_, dx_, z_, s_ in _MARCOS if a_ == MARCO), (MARCO, 18, -70, 1.0))
if MARCO:
    for k_, b_ in enumerate(B['beats']):
        if b_.get('interior') or b_.get('marco') is False or b_.get('set', SET) in ('hall', 'arctic', 'stadium'): continue
        b_['props'] = list(b_.get('props', [])) + [[MARCO[0], MARCO[1] * (1 if k_ % 2 else -1), MARCO[2], MARCO[3]]]
_hosp = next((b_ for b_ in B['beats'] if b_.get('interior') == 'hospital' and not b_.get('text')), None)
if _hosp is not None and not any(b_.get('text') == 'HOSPITAL' for b_ in B['beats']): _hosp['text'] = 'HOSPITAL'
_REG_JS = f"globalThis.REGMAP = {json.dumps(_regmap)}; globalThis.REGCHAO = {json.dumps(_REG_CHAO.get(REGIAO))};\n" if _regmap else "globalThis.REGMAP = null; globalThis.REGCHAO = null;\n"

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
    'lutador': {'shirtless': True, 'trunks': '#d8282f', 'trunkBand': '#f4f4f2', 'gloves': '#d8282f', 'pants': '#d8282f', 'boots': '#f4f4f2', 'hat': 'hair'},
    'boxeador': {'shirtless': True, 'trunks': '#27408b', 'trunkBand': '#e8c45a', 'gloves': '#d8282f', 'pants': '#27408b', 'boots': '#1b1b1f', 'hat': 'hair'},
    'juiz de luta': {'jacket': '#f4f4f2', 'stripes': True, 'pants': '#1b1b1f', 'boots': '#1b1b1f', 'tie': '#1b1b1f'},
    'soldado': {'jacket': '#27408b', 'pants': '#7d9fd0', 'boots': '#2a2218', 'hat': 'shako', 'belt': '#f1efe6', 'rifle': True},
    'marinheiro': {'jacket': '#2f5f6a', 'pants': '#e8e0c8', 'boots': '#1b1b1f', 'hat': 'beret', 'cap': '#27408b', 'beard': '#3a2a1f'},
    'cientista': {'jacket': '#f4f1e8', 'pants': '#3b3f52', 'boots': '#1b1b1f', 'hat': 'hair', 'hair': '#8a8a86', 'glasses': True, 'tie': '#3b3f52'},
    'medico': {'jacket': '#f4f1e8', 'pants': '#f4f1e8', 'boots': '#2a2218', 'hat': 'hair', 'hair': '#3a2a1f', 'glasses': True},
    'comerciante': {'jacket': '#8a5a34', 'pants': '#3b2a1a', 'boots': '#1b1b1f', 'hat': 'slouch', 'cap': '#3b2a1a', 'moustache': '#3a2a1f', 'build': 'stout'},
    'pescador': {'jacket': '#e8b46a', 'pants': '#3b3f52', 'boots': '#2a2218', 'hat': 'straw', 'beard': '#8a8a86'},
    'padre': {'jacket': '#1b1b1f', 'pants': '#1b1b1f', 'boots': '#1b1b1f', 'hat': 'hair', 'hair': '#8a8a86', 'sash': '#f4f1e8'},
    'camponesa': {'jacket': '#b0524a', 'pants': '#6a4a2a', 'boots': '#2a2218', 'hat': 'bonnet'},
    'jornalista': {'jacket': '#6a5a8a', 'pants': '#3b3f52', 'boots': '#1b1b1f', 'hat': 'bowler', 'glasses': True, 'tie': '#1b1b1f'},
    # PATENTES E CARGOS (19/11: distinguir quem e quem)
    'coronel': {'jacket': '#2f3a5a', 'pants': '#2a2d33', 'boots': '#1b1b1f', 'hat': 'shako', 'epaulets': '#e8c45a', 'medals': 2, 'buttons': '#e8c45a', 'moustache': '#3a2a1f'},
    'capitao': {'jacket': '#2f3a5a', 'pants': '#2a2d33', 'boots': '#1b1b1f', 'hat': 'shako', 'epaulets': '#d4d4d8', 'medals': 1, 'buttons': '#d4d4d8'},
    'imperador': {'jacket': '#1f2f6a', 'pants': '#f1efe6', 'boots': '#1b1b1f', 'hat': 'crown', 'collar': '#f4f1e8', 'sash': '#c8302a', 'epaulets': '#e8c45a', 'medals': 3, 'buttons': '#e8c45a', 'build': 'stout'},
    'rainha': {'jacket': '#7a2a5a', 'pants': '#7a2a5a', 'boots': '#1b1b1f', 'hat': 'crown', 'hairStyle': 'bun', 'collar': '#f4f1e8', 'dress': True, 'medals': 1},
    'presidente': {'jacket': '#1f2a44', 'pants': '#1f2a44', 'boots': '#1b1b1f', 'hat': 'hair', 'tie': '#c0262d', 'collar': '#f4f4f2', 'medals': 0},
    'funcionario': {'jacket': '#dfe8f0', 'pants': '#3b3f52', 'boots': '#1b1b1f', 'hat': 'hair', 'tie': '#2f4a6a', 'collar': '#f4f4f2'},
    'operario': {'jacket': '#d9822b', 'pants': '#3a4a6a', 'boots': '#2a2218', 'hat': 'helmet', 'cap': '#f2c84a', 'belt': '#2b2b30'},
    'policial': {'jacket': '#1f2a44', 'pants': '#1f2a44', 'boots': '#1b1b1f', 'hat': 'cap', 'cap': '#1f2a44', 'belt': '#1b1b1f', 'epaulets': '#1f2a44', 'buttons': '#d4d4d8'},
    'carcereiro': {'jacket': '#3a3f48', 'pants': '#2a2d33', 'boots': '#1b1b1f', 'hat': 'cap', 'cap': '#2a2d33', 'belt': '#1b1b1f', 'buttons': '#d4d4d8'},
    'enfermeira': {'jacket': '#f4f8f8', 'pants': '#f4f8f8', 'boots': '#f4f4f2', 'hat': 'bonnet', 'cap': '#f4f8f8', 'hairStyle': 'bun', 'sash': '#c8302a'},
    'engenheiro': {'jacket': '#3a5a8a', 'pants': '#2a2d33', 'boots': '#2a2218', 'hat': 'helmet', 'cap': '#f2c84a', 'glasses': True},
    'astronauta': {'jacket': '#f4f4f2', 'pants': '#f4f4f2', 'boots': '#d4d4d8', 'hat': 'helmet', 'cap': '#f4f4f2', 'sash': '#2f6fd0'},
}
PROFISSOES['general'].update({'epaulets': '#e8c45a', 'medals': 4}); PROFISSOES['rei'].update({'collar': '#f4f1e8', 'medals': 2}); PROFISSOES['empresario'].update({'collar': '#f4f4f2'}); PROFISSOES['politico'].update({'collar': '#f4f4f2'})
# UNIFORME DA EPOCA (19/11: soldado de 1600, 1915 e 2020 nao usam a mesma roupa) -- "ano" no topo do roteiro ou o ano do titulo/id
def _ano_por_extenso(t_):   # "mil setecentos e oitenta e oito" -> 1788 (a narracao escreve o ano por extenso)
    t_ = __import__('unicodedata').normalize('NFKD', t_.lower()).encode('ascii', 'ignore').decode()
    m_ = re.search(r'\b(mil|dois mil)( e)? ?(cento|duzentos|trezentos|quatrocentos|quinhentos|seiscentos|setecentos|oitocentos|novecentos)?( e)? ?(dez|onze|doze|treze|quatorze|catorze|quinze|dezesseis|dezessete|dezoito|dezenove|vinte|trinta|quarenta|cinquenta|sessenta|setenta|oitenta|noventa)?( e)? ?(um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito|nove)?\b', t_)
    if not m_ or not (m_.group(3) or m_.group(1) == 'dois mil'): return None
    C = dict(cento=100, duzentos=200, trezentos=300, quatrocentos=400, quinhentos=500, seiscentos=600, setecentos=700, oitocentos=800, novecentos=900)
    D = dict(dez=10, onze=11, doze=12, treze=13, quatorze=14, catorze=14, quinze=15, dezesseis=16, dezessete=17, dezoito=18, dezenove=19, vinte=20, trinta=30, quarenta=40, cinquenta=50, sessenta=60, setenta=70, oitenta=80, noventa=90)
    U = dict(um=1, uma=1, dois=2, duas=2, tres=3, quatro=4, cinco=5, seis=6, sete=7, oito=8, nove=9)
    return (2000 if m_.group(1) == 'dois mil' else 1000) + C.get(m_.group(3) or '', 0) + D.get(m_.group(5) or '', 0) + U.get(m_.group(7) or '', 0)
_anoM = re.search(r'(?<!\d)(1[0-9]{3}|20[0-9]{2})(?!\d)', ' '.join([str(B.get('ano', '')), B.get('title', ''), ID] + [str(b_.get('text', '')) for b_ in B['beats'][:4]]))
ANO = int(_anoM.group(1)) if _anoM else next((a_ for a_ in (_ano_por_extenso(b_['say']) for b_ in B['beats'][:4]) if a_), None)
# FARDA POR EPOCA E EXERCITO (19/11, referencias reais de museu/foto): chapeu/capacete, cor do casaco e da calca. Pais do personagem: "pais" no figurino,
# ou o codigo (ALE, FRA, ING, EUA, RUS, JAP, PRU, AUS, ITA, TUR, BRA, GRE, BUL, ESP, CON=confederado...), ou "pais" no topo do roteiro.
_PAIS_COD = {'ale': 'alemanha', 'ger': 'alemanha', 'pru': 'alemanha', 'naz': 'alemanha', 'fra': 'franca', 'ing': 'inglaterra', 'bri': 'inglaterra', 'uk': 'inglaterra', 'eua': 'eua', 'ame': 'eua', 'usa': 'eua', 'uni': 'eua', 'yan': 'eua',
             'con': 'confederados', 'sul': 'confederados', 'rus': 'russia', 'sov': 'russia', 'urs': 'russia', 'jap': 'japao', 'ita': 'italia', 'aus': 'austria', 'tur': 'turquia', 'oto': 'turquia', 'bra': 'brasil', 'par': 'paraguai',
             'gre': 'grecia', 'bul': 'bulgaria', 'esp': 'espanha', 'por': 'portugal', 'chi': 'china', 'mex': 'mexico', 'arg': 'argentina', 'pol': 'polonia', 'zan': 'zanzibar', 'emu': 'australia', 'aut': 'austria', 'hab': 'austria', 'hun': 'austria', 'osm': 'turquia'}
def _pais_de(k_, o_):
    p_ = str(o_.get('pais') or '').lower()
    if p_: return p_
    if k_.lower().startswith('aus'): return 'australia' if (ANO or 0) >= 1900 else 'austria'
    for c_, v_ in _PAIS_COD.items():
        if k_.lower().startswith(c_): return v_
    return str(B.get('pais') or '').lower()
#                  (ate o ano, {pais: (chapeu soldado, chapeu oficial, casaco, calca, cor do chapeu)})   '*' = demais paises
_FARDA = [
 (1699, {'*': ('slouch', 'slouch', '#7a3a2a', '#4a3a2a', '#3a2a1f')}),
 (1795, {'inglaterra': ('tricorn', 'tricorn', '#b8282c', '#ece8dc', None), 'franca': ('tricorn', 'tricorn', '#e8e4d8', '#ece8dc', None), 'eua': ('tricorn', 'tricorn', '#2a3a6a', '#ece8dc', None),
         'alemanha': ('tricorn', 'tricorn', '#2a3a6a', '#ece8dc', None), 'austria': ('tricorn', 'tricorn', '#ece8dc', '#ece8dc', None), 'turquia': ('turban', 'turban', '#b5333a', '#ece8dc', '#f1ece0'), 'russia': ('tricorn', 'tricorn', '#2f5a3a', '#ece8dc', None), 'espanha': ('tricorn', 'tricorn', '#e8e4d8', '#ece8dc', None), '*': ('tricorn', 'tricorn', '#2a3a6a', '#ece8dc', None)}),
 (1815, {'franca': ('shako_tall', 'bicorne', '#2a3a7a', '#ece8dc', None), 'inglaterra': ('shako', 'bicorne', '#b8282c', '#ece8dc', None), 'russia': ('shako_tall', 'bicorne', '#2f5a3a', '#ece8dc', None),
         'alemanha': ('shako', 'bicorne', '#22304a', '#3a3a42', None), 'austria': ('shako', 'bicorne', '#ece8dc', '#ece8dc', None), 'eua': ('shako', 'bicorne', '#2a3a6a', '#ece8dc', None), '*': ('shako', 'bicorne', '#2a3a7a', '#ece8dc', None)}),
 (1860, {'inglaterra': ('shako', 'quepe', '#b8282c', '#2a2a30', None), 'eua': ('kepi', 'kepi', '#2a3a6a', '#7a8fb5', '#2a3a6a'), 'franca': ('kepi', 'kepi', '#2a3a7a', '#b8282c', '#b8282c'), 'russia': ('quepe', 'quepe', '#2f5a3a', '#2f5a3a', '#2f5a3a'),
         'alemanha': ('pickelhaube', 'pickelhaube', '#22304a', '#2a2a30', None), 'austria': ('shako', 'quepe', '#ece8dc', '#7a8fb5', None), '*': ('shako', 'quepe', '#2a3a6a', '#7a8fb5', None)}),
 (1865, {'eua': ('kepi', 'kepi', '#2a3a6a', '#7a8fb5', '#2a3a6a'), 'confederados': ('kepi', 'slouch', '#8a8a86', '#8a8a86', '#8a8a86'), 'franca': ('kepi', 'kepi', '#2a3a7a', '#b8282c', '#b8282c'),
         'alemanha': ('pickelhaube', 'pickelhaube', '#22304a', '#2a2a30', None), 'brasil': ('kepi', 'kepi', '#2a3a6a', '#ece8dc', '#2a3a6a'), 'paraguai': ('kepi', 'kepi', '#b8282c', '#ece8dc', '#b8282c'), '*': ('kepi', 'quepe', '#2a3a6a', '#7a8fb5', '#2a3a6a')}),
 (1913, {'alemanha': ('pickelhaube', 'pickelhaube', '#22304a', '#2a2a30', None), 'franca': ('kepi', 'kepi', '#2a3a7a', '#b8282c', '#b8282c'), 'inglaterra': ('colonial', 'colonial', '#b8282c', '#2a2a30', '#efe6cc'),
         'eua': ('slouch', 'slouch', '#2a3a6a', '#7a8fb5', '#8a7a50'), 'russia': ('quepe', 'quepe', '#e8e4d8', '#2a2a30', '#2f5a3a'), 'japao': ('kepi', 'kepi', '#22304a', '#22304a', '#22304a'), 'zanzibar': ('turban', 'turban', '#ece8dc', '#ece8dc', '#ece8dc'),
         'brasil': ('kepi', 'kepi', '#2a3a6a', '#ece8dc', '#2a3a6a'), '*': ('kepi', 'quepe', '#2a3a6a', '#3a3a42', '#2a3a6a')}),
 (1918, {'alemanha': ('stahlhelm', 'quepe', '#6a6e5a', '#5a5e4e', '#5d6355'), 'austria': ('stahlhelm', 'quepe', '#7a8288', '#6a7278', '#6a7278'), 'franca': ('adrian', 'kepi', '#7a8aa8', '#7a8aa8', '#7a8aa8'),
         'inglaterra': ('brodie', 'quepe', '#7a7052', '#7a7052', '#6a6a4a'), 'eua': ('brodie', 'quepe', '#6a6040', '#6a6040', '#6a6a4a'), 'russia': ('quepe', 'quepe', '#7a7a52', '#5a5a42', '#7a7a52'),
         'italia': ('adrian', 'quepe', '#7a7a62', '#7a7a62', '#6a6a52'), 'turquia': ('bibico', 'quepe', '#8a7a4a', '#7a6a42', '#8a7a4a'), 'australia': ('slouch', 'slouch', '#7a7052', '#7a7052', '#7a6a4a'), '*': ('adrian', 'quepe', '#7a7052', '#7a7052', '#6a6a4a')}),
 (1940, {'alemanha': ('stahlhelm', 'quepe', '#6a6e5a', '#5a5e4e', '#5d6355'), 'franca': ('adrian', 'kepi', '#8a7a52', '#8a7a52', '#7a7a52'), 'inglaterra': ('brodie', 'quepe', '#7a7052', '#7a7052', '#6a6a4a'),
         'eua': ('brodie', 'quepe', '#6a6040', '#6a6040', '#6a6a4a'), 'russia': ('m1', 'quepe', '#7a7a52', '#5a5a42', '#55593a'), 'japao': ('m1', 'quepe', '#8a7a4a', '#8a7a4a', '#7a7a4a'), 'italia': ('adrian', 'quepe', '#7a7a62', '#7a7a62', '#6a6a52'),
         'grecia': ('adrian', 'quepe', '#7a7052', '#7a7052', '#6a6a4a'), 'bulgaria': ('stahlhelm', 'quepe', '#5d6a4e', '#5d6a4e', '#55603f'), 'polonia': ('adrian', 'quepe', '#6a6e5a', '#6a6e5a', '#5d6355'), 'australia': ('slouch', 'slouch', '#7a7052', '#7a7052', '#7a6a4a'), '*': ('brodie', 'quepe', '#7a7052', '#7a7052', '#6a6a4a')}),
 (1945, {'alemanha': ('stahlhelm', 'quepe', '#6a6e5a', '#5a5e4e', '#5d6355'), 'eua': ('m1', 'quepe', '#5e5a3a', '#6a6040', '#4f5338'), 'brasil': ('m1', 'quepe', '#5e5a3a', '#6a6040', '#4f5338'), 'inglaterra': ('brodie', 'quepe', '#7a7052', '#7a7052', '#6a6a4a'),
         'russia': ('m1', 'quepe', '#7a7a52', '#5a5a42', '#55593a'), 'japao': ('m1', 'quepe', '#8a7a4a', '#8a7a4a', '#7a7a4a'), 'italia': ('adrian', 'quepe', '#7a7a62', '#7a7a62', '#6a6a52'), 'australia': ('slouch', 'slouch', '#7a7052', '#7a7052', '#7a6a4a'), '*': ('m1', 'quepe', '#5e5a3a', '#6a6040', '#4f5338')}),
 (1959, {'*': ('m1', 'quepe', '#5e5a3a', '#5e5a3a', '#4f5338'), 'russia': ('m1', 'quepe', '#6a6a4a', '#5a5a42', '#4a5a3a')}),
 (1999, {'*': ('m1', 'quepe', '#6a7a4a', '#5a6a3a', '#4a5a3a', 'camo'), 'eua': ('m1', 'quepe', '#6a7a4a', '#5a6a3a', '#4a5a3a', 'camo')}),
 (9999, {'*': ('m1', 'beret', '#8a7f62', '#7a705a', '#7a705a', 'camo')}),
]
_OFICIAL = ('general', 'coronel', 'capitao', 'tenente', 'major', 'marechal', 'comandante', 'oficial', 'almirante', 'sargento')
for _k, _o in B.get('outfits', {}).items():
    _pf = str(_o.get('profissao', '')).lower()
    _milh = _o.get('hat') in ('shako', 'shako_tall', 'helmet') and not _o.get('pele') and not _k.lower().startswith('hus') and not (_k.lower().startswith(('ast', 'cos', 'bomb', 'mine', 'pil')) or str(_o.get('jacket', '')).lower() in ('#f4f4f2', '#e8e8e8', '#ffffff') or _pf in ('astronauta', 'bombeiro', 'mineiro', 'piloto'))   # capacete de astronauta/bombeiro/mineiro nao e' farda; chapeu militar generico = militar (hussardo fica com a barretina alta)
    if not (_o.get('rifle') or _milh or _pf in ('soldado', 'cavaleiro', 'cavalaria') + _OFICIAL) or _o.get('uniforme_fixo') or ANO is None: continue
    _pa = _pais_de(_k, _o); _tab = next(t_ for a_, t_ in _FARDA if ANO <= a_); _f = _tab.get(_pa) or _tab['*']
    if not _pa and _o.get('hat') in ('fez', 'turban', 'slouch', 'straw', 'beret', 'crown', 'bowler', 'tophat'): continue   # exercito sem tabela (guarda do sultao, milicia): fica com o chapeu proprio
    _of = (_pf in _OFICIAL and _pf != 'sargento') or bool(re.match(r'(off|ofi|gen|cor|cap|ten|maj|com|mar|alm)', _k.lower())) or bool(_o.get('sword') and not _o.get('rifle'))
    _o.update({'hat': _f[1] if _of else _f[0], 'jacket': _f[2], 'pants': _f[3], 'boots': '#2a2218'})
    if _f[4]: _o['cap'] = _f[4]
    else: _o.pop('cap', None)
    if len(_f) > 5 and _f[5] == 'camo': _o['camo'] = '#3e4a2e' if ANO < 2000 else '#6a604a'
    if _of and _o['hat'] == 'quepe': _o['cap'] = _o.get('cap') or _f[2]; _o['capBand'] = '#e8c45a' if _pf in ('general', 'marechal', 'almirante', 'coronel') else _o.get('capBand')
    if ANO < 1870 and not _of: _o.setdefault('belt', '#f1efe6')   # correias brancas cruzadas ate 1870
    elif ANO >= 1870: _o.pop('belt', None) if _o.get('belt') == '#f1efe6' else None
    if re.search(r'paraquedis|boina|forcas especiais|comando', ' '.join(b_['say'].lower() for b_ in B['beats'])) and not _of and ANO >= 1940: _o['hat'] = 'beret'; _o['cap'] = '#8a2b2b'

# ===== VEGETACAO, FLORES E CHAO DO LUGAR E DA EPOCA (19/11) =====
# arvores/arbustos/canteiros genericos da biblioteca viram as plantas do lugar; rua moderna (1930+) vira asfalto, antiga fica de pedra/terra.
_vt = __import__('unicodedata').normalize('NFKD', (' '.join(str(b_.get('mapa') or '') for b_ in B['beats']) + ' ' + B.get('title', '') + ' ' + ' '.join(b_['say'] for b_ in B['beats'][:5])).lower()).encode('ascii', 'ignore').decode()
_VEG = ((r'mexic|arizona|nevada|texas|deserto|las vegas|novo mexico', {'nature/tree_oak': ['kit/veg_cacto', 'nature/tree_palm'], 'nature/bush': ['kit/veg_cacto'], 'nature/flowerbed': ['kit/veg_cacto']}),
        (r'brasil|pernambuco|recife|bahia|rio de janeiro|el salvador|zanzibar|caribe|cuba|haiti|jamaica|tropical|amazon|colombia|venezuel|tailand|indonesia|filipinas|havai|panama|honduras|guatemala|nicaragua', {'nature/tree_oak': ['kit/veg_bananeira', 'nature/tree_palm'], 'nature/bush': ['kit/veg_hibisco'], 'nature/flowerbed': ['kit/veg_hibisco']}),
        (r'japa|toquio|kyoto', {'nature/tree_oak': ['kit/veg_cerejeira', 'nature/tree_pine'], 'nature/bush': ['kit/veg_bambu'], 'nature/flowerbed': ['kit/veg_cerejeira']}),
        (r'china|chines|pequim|xangai|vietna|coreia', {'nature/tree_oak': ['kit/veg_bambu', 'kit/veg_cerejeira'], 'nature/bush': ['kit/veg_bambu']}),
        (r'africa|quenia|tanzania|nigeria|etiopia|congo|angola|mocambique|somalia|sudao|savana', {'nature/tree_oak': ['kit/veg_acacia', 'kit/veg_baoba'], 'nature/bush': ['nature/bush'], 'nature/flowerbed': ['nature/rocks']}),
        (r'australia|emus', {'nature/tree_oak': ['kit/veg_acacia', 'nature/tree_oak'], 'nature/flowerbed': ['nature/rocks']}),
        (r'egito|egipc|arabia|iraque|\bira\b|\birao\b|dubai|marrocos|persia|babilon|israel|palestin|siria|jordania|\bindia\b', {'nature/tree_oak': ['nature/tree_palm'], 'nature/bush': ['nature/bush'], 'nature/flowerbed': ['nature/rocks']}),
        (r'italia|roma|grecia|atenas|esparta|espanha|madri|portugal|lisboa|turquia|croacia|sicilia|mediterr|romanos|gladiad', {'nature/tree_oak': ['kit/veg_oliveira', 'kit/veg_cipreste'], 'nature/flowerbed': ['kit/veg_lavanda']}),
        (r'\bfranc|paris|provenc', {'nature/tree_oak': ['nature/tree_oak', 'kit/veg_cipreste'], 'nature/flowerbed': ['kit/veg_lavanda']}),
        (r'holand|amsterd|paises baixos', {'nature/flowerbed': ['kit/tulip_bed']}),
        (r'russi|moscou|siberia|soviet|ucrani|finland|suecia|noruega|canada|alasca|suica|alpes|escandinav', {'nature/tree_oak': ['nature/tree_pine', 'nature/tree_birch'], 'nature/flowerbed': ['nature/bush']}),
        (r'kansas|fazenda americana|nebraska|iowa|ucrania', {'nature/flowerbed': ['kit/veg_girassol']}))
if B.get('vegetacao') is not False:
    for rx_, mp_ in _VEG:
        if re.search(rx_, _vt):
            for k_, v_ in mp_.items(): _regmap.setdefault(k_, v_)
            break
if ANO and B.get('veiculos_epoca') is not False:   # VEICULOS DA EPOCA (19/11): tanque, aviao, caminhao e navio do ano da historia (Mark I em 1917, caca na 2a Guerra, navio a vapor em 1900...)
    _regmap.setdefault('vehicles/tank', ['kit/tanque_ww1' if ANO < 1925 else 'kit/tanque_ww2' if ANO < 1955 else 'kit/tanque_moderno'])
    if ANO < 1955: _regmap.setdefault('vehicles/airplane', ['kit/biplano' if ANO < 1936 else 'kit/aviao_ww2'])
    if ANO < 1950: _regmap.setdefault('vehicles/truck', ['kit/caminhao_antigo'])
    if ANO < 1820: _regmap.setdefault('kit/navio_vapor', ['kit/navio_vela'])   # 23/11: antes do vapor so' existe navio a vela
    if 1840 <= ANO < 1955: _regmap.setdefault('ship', ['kit/navio_vapor'])
    elif ANO >= 1955: _regmap.setdefault('ship', ['kit/navio_moderno'])
_CHAO = _REG_CHAO.get(REGIAO)
if ANO and ANO >= 1930 and SET in ('street', 'stadium', 'hall'): _CHAO = '#6a6a70'   # rua moderna: asfalto cinza (antes de 1930 fica a pedra/terra da regiao)
elif ANO and ANO < 1800 and not _CHAO: _CHAO = '#b49a78'                               # rua antiga: terra batida
_ASF = bool(ANO and (ANO >= 1950 or (ANO >= 1925 and REGIAO == "eua")) and B.get("asfalto") is not False)   # rua asfaltada com faixa e calcada (cidade moderna); antes disso pedra/terra
_PRAIA = B.get("praia", bool(re.search(r"\bpraia|\bareia\b|desembarc", " ".join(__import__("unicodedata").normalize("NFKD", b_["say"].lower()).encode("ascii", "ignore").decode() for b_ in B["beats"]))))   # praia de areia em vez do cais de madeira
_REG_JS = f"globalThis.REGMAP = {json.dumps(_regmap)}; globalThis.REGCHAO = {json.dumps(_CHAO)}; globalThis.ASFALTO = {json.dumps(_ASF)}; globalThis.PRAIA = {json.dumps(bool(_PRAIA))}; globalThis.SEM_NAVIO = {json.dumps(B.get('navio') is False or bool(ANO and ANO >= 1990 and not re.search(r'navio|marinha|frota|porto|barco', ' '.join(b_['say'].lower() for b_ in B['beats']))))};\n"
_FAMHAIR = {str(o_.get('hair', '')).lower() for o_ in B.get('outfits', {}).values() if o_.get('pele')} - {''}
for _k, _o in B.get('outfits', {}).items():   # SEM SOSIA (ordem do Gibson): em video com famoso, ninguem mais usa a cor de cabelo dele (loiro do Trump so no Trump)
    if not _o.get('pele') and str(_o.get('hair', '')).lower() in _FAMHAIR: _o['hair'] = '#5a3a22'
for _k, _o in B.get('outfits', {}).items():   # terno com gravata tem colarinho branco (Trump, politicos, empresarios)
    if _o.get('tie') and not _o.get('collar'): _o['collar'] = '#f4f4f2'
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
    base = {1: [0.0], 2: [-1.0, 1.0], 3: [-2.1, 0.0, 2.1], 4: [-3.0, -1.0, 1.0, 3.0], 5: [-3.6, -1.8, 0, 1.8, 3.6], 6: [-3.8, -2.3, -0.8, 0.8, 2.3, 3.8]}
    if n in base: return base[n]
    return [(i - (n - 1) / 2) * 1.6 for i in range(n)]
ZS = [1.3, 1.0, 1.6, 1.1, 1.7, 1.4]   # no plano de foco da camera (antes 2.0-3.0: com a camera mais perto, alguem ficava colado na lente)
ZSW = [-0.4, 0.2, -0.8, 0.0, -0.2, 0.4]

TEMPL = {  # h = altura do alvo; d0/d1 = distancia da camera no inicio/fim; el = elevacao; fov
    'wide':  dict(h=2.4, d0=20, d1=16, el=5, fov=46),   # camera na altura do personagem (canal: 0,8x), nao de cima
    'two':   dict(h=2.3, d0=9.8, d1=8.8),
    'close': dict(h=2.4, d0=6.4, d1=5.6),
    'group': dict(h=2.5, d0=11.4, d1=10.2),
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
# GRAVIDADE (ordem do Gibson): tudo que sobe e cai segue a fisica. Boneco ~3,15 m representa pessoa de 1,75 m -> escala 1,8 -> g da cena = 9,8 x 1,8 = 17,6 m/s2
GRAV = 17.6
GVOO_T = 1.6   # soldado arremessado pela explosao: 1,6 s no ar, sobe ~5,6 m (cena) e cai acelerando
GPULO_H = 1.2; GPULO_V0 = (2 * GRAV * GPULO_H) ** 0.5; GPULO_T = 2 * GPULO_V0 / GRAV          # pulo: sobe 1,2 m (cena) e volta em ~0,74 s
def grav_js(f0, T, y0, y1):   # trajetoria de projetil: sai de y0 no quadro f0 e chega em y1 depois de T segundos (sobe e cai pela gravidade)
    v0 = (y1 - y0 + 0.5 * GRAV * T * T) / T
    return f"(f) => {{ const t = Math.max(0, Math.min({T:.3f}, (f - ({f0})) / 30)); return DK + {y0:.3f} + {v0:.3f} * t - {0.5 * GRAV:.3f} * t * t; }}"
# ENCENACAO: verbo da narracao -> (gesto, tipo de acao). Ordem importa (o primeiro que casa).
_NEGW = {'nao', 'ninguem', 'nenhum', 'nenhuma', 'sem', 'nunca', 'jamais', 'nem'}
def _neg_idx(say):   # NEGACAO (19/11): "ninguem deu um tiro", "sem dar um unico tiro", "nao atacou" -> as 4 palavras seguintes NAO sao encenadas
    ws_ = [re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', w_.lower()).encode('ascii', 'ignore').decode()) for w_ in say.split()]; out_ = set()
    for i_, w_ in enumerate(ws_):
        if w_ in _NEGW: out_.update(range(i_ + 1, min(len(ws_), i_ + 5)))
    return out_
def _idiom_idx(say):   # EXPRESSOES (19/11): "o panico tomou o acampamento", "a noticia correu o mundo", "o preco caiu" -> nao sao beber/correr/cair
    ws_ = say.split(); out_ = set(); n_ = lambda t: re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode())
    for j_, w_ in enumerate(ws_):
        nw_ = n_(w_); ant_ = n_(' '.join(ws_[max(0, j_ - 2):j_])); dep_ = n_(' '.join(ws_[j_ + 1:j_ + 4]))
        if (re.match(r'^(tomou|tomaram|tomava)$', nw_) and not re.search(r'cafe|cha|agua|vinho|cerveja|remedio|leite|sopa|suco|aguardente|rum|whisky|uisque|tequila|cachaca|veneno|pocao|gole|banho', dep_)) \
           or (re.match(r'^(correu|correram|corria|corre)$', nw_) and re.search(r'noticia|fama|boato|rumor|tempo|historia|sangue|dinheiro|agua|lagrima|suor|risco|perigo|video|mensagem', ant_ + dep_)) \
           or (re.match(r'^(caiu|cairam)$', nw_) and re.search(r'preco|venda|bolsa|acoes|ficha|noite|chuva|neve|valor|audiencia|popularidade', ant_ + dep_)) \
           or (re.match(r'^(entrou|entraram|entrava|entraria|entrariam)$', nw_) and re.match(r'^(para|em|na|no)(a|o)?(historia|guerra|moda|panico|acordo|crise|falencia|vigor|campo|conflito|greve|colapso)', dep_)):
            out_.add(j_)
    return out_
ENC = [(r'^(misturou|misturaram|misturando|mistura|misturar|mexeu|mexendo|mexia|combinou|batia|bateu a massa|cozinhou|cozinhava)$', 'stir', 'mistura'),
       (r'^(caiu|cairam|derrubou|derrubaram|derramou|jogou|jogaram|atirou o|despejou|despejaram|lancou|deixou)$', 'throw', 'cai'),
       (r'^(esquentou|aqueceu|aquecer|esquentar|ferveu|ferver|fervendo|quente|aquecido|queimou|assou|fogao|forno|fogo|chamas?)$', 'reach', 'calor'),
       (r'^(virou|viraram|transformou|transformaram|endureceu|endureceram|firme|elastica|elastico|solidificou|nasceu|nasciam|surgiu|criou|criaram|inventou|inventaram|derreteu|pronto|pronta)$', 'up', 'vira'),
       (r'^(construir|construimos|construida|construido|construcoes|construcao|construiu|construiram|montou|montaram|fabricou|fabricaram|ergueu|ergueram|soldou|martelou|consertou|consertar)$', 'hammer', 'constroi'),
       (r'^(examinou|observou|observava|analisou|estudou|estudava|mediu|medir|pesou|microscopio|lupa|investigou)$', 'think', 'examina'),
       (r'^(quimico|quimicos|quimica|acido|reagente|formula|experiencia|experiencias|experimento|experimentos|laboratorio|substancia)$', 'pour', 'quimico'),   # 'solucao' saiu: quase sempre e' 'a resposta' (a solucao: mandar bichos), nao liquido
       (r'^(escreveu|escreveram|anotou|anotava|assinou|assinaram|desenhou|rabiscou|calculou)$', 'write', 'escreve'),
       (r'^(socou|soco|socos|socando|nocauteou|chutou|chute|esmurrou)$', 'punch', 'golpe'),
       (r'^(cortavam|cortava|cortou|cortaram|cortar|serrou|serravam|machado|lenhadores|lenhador|derrubavam)$', 'hammer', 'corta'),
       (r'^(votou|votaram|votar|votavam|urnas?|eleitores|eleicao|eleicoes)$', 'reach', 'voto'),
       (r'^(rachou|racharam|quebrou|quebraram|quebrar|estilhacou|despedacou|trincou|arrebentou)$', 'throw', 'quebra'),
       (r'^(desabou|desabaram|desmoronou|ruiu|ruiram|cairiam|caindo|desabariam|afundou|afundaram|afundar|afundando|explodiu|explodiram)$', None, 'desaba'),
       (r'^(pensou|pensava|pensando|imaginou|imaginava|ideia|calculou|calculava|percebeu|entendeu|raciocinou|desconfiou)$', 'think', 'pensa'),
       (r'^(protestaram|protestavam|criticaram|denunciaram|reclamaram|manifestantes|protesto|protestos|vaiaram)$', 'up', 'protesto'),
       (r'^(explicou|anunciou|apresentou|prometeu|declarou|discursou|mostrou|ensinou|avisou|ordenou|mandou)$', 'point', 'fala'),
       (r'^(olhou|olhando|olhavam|apontou|apontando|observou|viu|viram|vendo|enxergou|avistou|espiou|assistiu|assistiram)$', 'point', 'olha'),
       (r'^(embora|partiu|partiram|retiraram|recuaram|abandonaram|sairam|saiu|fugiram|zarparam)$', None, 'sai'),
       (r'^(chao|nocauteado|nocaute|desmaiou|desmaiaram|tombou|tropecou|escorregou|derrubado|derrubada|derrubados)$', None, 'tomba'),
       (r'^(dormiam|dormia|dormindo|dormiu|cochilou|cochilavam|adormeceu|adormeceram)$', None, 'dorme'),
       (r'^(sentou|sentaram|sentado|sentada|sentados)$', None, 'senta'),
       (r'^(morreu|morreram|morriam|morria|faleceu|faleceram|faleciam)$', None, 'morre'),   # 19/11: quem morre CAI (ou tumulo, se 'morreu em <ano>')
       (r'^(raspar|raspou|rasparam|raspada|raspado|careca|tosquiou)$', 'reach', 'raspa'),
       (r'^(enfrentou|enfrentaram|lutou|lutaram|lutando|brigaram|brigou|brigando|brigavam|golpe|golpes)$', 'punch', 'golpe'),
       (r'^(capturado|capturada|capturaram|capturou|preso|presa|presos|prenderam|prendeu|algemado|algemaram|detido|detidos)$', 'push', 'prende'),
       (r'^(escalaram|escalou|subiram|subiu|treparam|trepou)$', 'lift', 'escala'),
       (r'^(espetado|espetou|esfaqueou|esfaqueado|furou|cutucou|feriu|ferido)$', 'punch', 'espeta'),
       (r'^(chutou|chute|gol|gols|bola|partida|jogos|jogo)$', 'throw', 'bola'),
       (r'^(comprou|compraram|comprar|compra|compras|comprava|vendeu|venderam|vender|venda|vendas|vendidos|vendida|vendido|vendia|pagou|pagaram|leilao|leiloou)$', 'reach', 'negocio'),
       (r'^(tirou|tiraram|tirar|fotografou|fotos?|selfie|filmou|filmaram|gravou)$', 'lift', 'tira'),
       (r'^(rendeu|renderam|rendendo|rendicao|renderam-se|rendeu-se)$', 'up', 'rende'),
       (r'^(voarem|voar|voou|voando|decolou|decolaram|decolar|levantou voo|subiu ao ceu)$', 'point', 'voa'),
       (r'^(descobrir|descobriu|descobriram|descoberta)$', 'think', 'examina'),
       (r'^(encontrou|encontraram|achou|acharam|flagrou|pegou no flagra)$', 'point', 'olha'),
       (r'^(cavar|cavou|cavaram|cavando|escavou|escavaram)$', 'hammer', 'cava'),
       (r'^(venceu|venceram|vencedor|vencedora|vitoria|ganhou|ganharam|campeao)$', 'up', 'vence'),
       (r'^(perdeu|perderam|perdesse|perderia|perderiam|perdedor|perdedora|fracassou|falhou)$', 'facepalm', 'perde'),
       (r'^(tocou|tocaram|tocava|tocavam|sirenes?|sinos?|tocando)$', None, 'toca'),
       (r'^(queimado|queimada|queimou|queimaram|incendiou|incendiaram|pegou fogo)$', None, 'queima'),
       (r'^(gritar|gritou|gritaram|gritando|berrou)$', 'up', 'grita'),
       (r'^(assinar|assinou|assinaram|assinatura)$', 'write', 'escreve'),
       (r'^(brinde|brindou|brindaram)$', 'lift', 'pega'),
       (r'^(atirou|atiraram|atirando|atirava|atiravam|disparou|dispararam|disparando|disparava|fuzilaram)$', None, 'atira'),
       (r'^(correu|correram|correndo|corria|corriam|correr|corresse|correm|saiu correndo|fugiu|fugiram|fugindo|fugia|fugir|escapou|escaparam|debandaram)$', None, 'corre'),
       (r'^(pulou|pularam|pulando|pulava|pulavam|pular|pulasse|pulassem|pulam|pula|pulem|saltou|saltaram|saltando|saltar|saltasse|pulo|pulos|saltos?|quicou)$', None, 'pula'),
       (r'^(acenou|acenaram|acenando|tchau|despediu|despediram)$', 'wave2', 'acena'),
       (r'^(empurrou|empurraram|empurrando|puxou|puxaram|puxando|arrastou|arrastaram|arrastando)$', 'push', 'empurra'),
       (r'^(deitou|deitaram|deitado|deitada)$', None, 'senta'), (r'^(ajoelhou|ajoelharam|ajoelhado|ajoelhada|ajoelhados|joelhos|implorou|imploravam|implorava|suplicou|suplicavam)$', 'plead', 'ajoelha'),
       (r'^(levantou-se|levantaram-se|levantou|ergueu-se)$', 'lift', 'pega'),
       (r'^(bebeu|beberam|bebendo|bebia|bebiam|tomou|tomaram|tomando|goles?|engoliu)$', 'lift', 'x_bebe'),
       (r'^(comeu|comeram|comendo|comia|comiam|almocou|jantou|devorou|mastigou)$', 'eat', 'x_come'), (r'^(provou|provaram|comprovou|demonstrou)$', 'point', 'fala'),   # provou que/os microbios = demonstrou (nao e' comer)
       (r'^(chorou|choraram|chorando|chorava|lagrimas|soluco|solucou)$', 'facepalm', 'x_chora'),
       (r'^(cantou|cantaram|cantando|cantava|cantavam|musica|hino|cancao)$', 'up', 'x_canta'),
       (r'^(leu|leram|lendo|lia|liam|ler|jornal|carta|livro)$', 'think', 'x_le'),
       (r'^(telefonou|ligou|ligaram|ligando|telefone|celular|mensagem|twittou|postou|publicou|tuitou)$', 'lift', 'x_fone'),
       (r'^(lavou|lavaram|lavar|lavando|limpou|limparam|esfregou)$', 'stir', 'x_lava'),
       (r'^(beijou|beijaram|beijo)$', None, 'x_beija'),
       (r'^(plantou|plantaram|plantar|plantando|semeou|regou|regaram|colheu|colheram|colheita)$', 'hammer', 'x_planta'),
       (r'^(pescou|pescaram|pescar|pescando|pescador|anzol)$', 'lift', 'x_pesca'),   # 'rede' saiu: 'rede X', 'rede social' viravam pescaria
       (r'^(costurou|costurar|costurando|tricotou|bordou)$', 'write', 'x_costura'),
       (r'^(pintou|pintaram|pintar|pintando|desenhou|desenhar|rabiscou)$', 'write', 'x_pinta'),
       (r'^(cozinhou|cozinhar|cozinhando|assou|fritou|temperou)$', 'stir', 'mistura'),
       (r'^(bateu|bateram|batendo|batia)$', 'punch', 'x_bate'),
       (r'^(procurou|procuraram|procurando|procurava|buscou|buscaram|vasculhou|investigaram)$', 'think', 'x_procura'),
       (r'^(vigiava|vigiavam|vigiar|guardava|guardavam|patrulhava|patrulhavam|sentinela)$', 'cross', 'x_vigia'),
       (r'^(continencia|saudou|saudaram|saudacao|bateu continencia)$', 'salute', 'x_saluda'),
       (r'^(rezou|rezaram|rezando|orou|oraram|rezava)$', 'think', 'x_reza'),
       (r'^(aplaudiu|aplaudiram|aplausos?|aplaudindo|palmas)$', 'up', 'x_aplaude'),
       (r'^(abracou|abracaram|abraco|abracando)$', None, 'x_abraca'),
       (r'^(acordou|acordaram|despertou|acordar)$', 'up', 'x_acorda'),
       (r'^(esperou|esperaram|esperando|esperava|esperavam|aguardou|aguardaram)$', 'cross', 'x_espera'),
       (r'^(tremeu|tremeram|tremendo|tremia|arrepiou|congelou)$', None, 'x_treme'),
       (r'^(espirrou|tossiu|tossia|tossindo|espirrando)$', 'facepalm', 'x_tosse'),
       (r'^(mergulhou|mergulharam|nadou|nadaram|nadando|nadar|afogou)$', 'up', 'x_nada'),
       (r'^(riu|riram|rindo|ria|riam|gargalhou|gargalhada)$', 'up', 'x_ri'),
       (r'^(abriu|abriram|abrindo|fechou|fecharam|trancou|destrancou)$', 'push', 'x_abre'),
       (r'^(soltou|soltaram|libertou|libertaram|liberou)$', 'up', 'x_solta'),
       (r'^(entregou|entregaram|deu|deram|ofereceu|ofereceram|recebeu|receberam)$', 'reach', 'x_entrega'),
       (r'^(contou|contaram|contava)$', 'point', 'fala'),   # contou o sonho/a historia = falou (contar numeros e' raro)
       (r'^(mediu|mediram|pesou|calculou)$', 'think', 'examina'),
       (r'^(apresentou|mostrou|exibiu|revelou|lancou|anunciou)$', 'point', 'fala'),
       (r'^(brilhar|brilhou|brilhava|brilhando|brilho|acendeu|acenderam|acendia|reluzia|reluziu|iluminou|cintilou|faiscas?|faiscava)$', 'point', 'brilha'),
       (r'^(pegou|pegaram|segurou|ergueu|levantou|levantaram|carregou|carregaram)$', 'lift', 'pega'),
       # 19/11 (ordem do Gibson: acao especifica nao pode sair so com efeito): CORPO para as familias que ficavam so com efeito+som
       (r'^(pagar|pagou|pagaram|pago|pagava|dinheiro|moeda|moedas|ouro|fortuna|vendeu|venderam|vendendo|vender|comprando|comprador|comprou|compraram|roubaram|roubou|recompensa)$', 'reach', 'paga'),
       (r'^(chegou|chegaram|apareceu|apareceram|invadiu|invadiram|entrou|entraram)$', 'point', 'chega'),
       (r'^(atirar|tiro|tiros|bala|balas|canhao|canhoes|artilharia|metralhadora|metralhadoras|bomba|bombas|ataque|ataques)$', None, 'atira'),
       (r'^(brigar|briga|brigas|atacar|atacou|atacaram|discussao)$', 'punch', 'golpe'),
       (r'^(perder|derrotado|derrotados|derrota|fracasso|desistiu|desistiram|retirada|baixas)$', 'facepalm', 'perde'),
       (r'^(gritava|gritavam|socorro|panico|alarme|correria|caos|surpresa)$', 'up', 'grita'),
       (r'^(festa|festas|comemoraram|comemorou|comemorando|comemorar|premio|ganhou)$', 'up', 'vence'),
       (r'^(danca|dancando|dancar|dancou|dancaram|dancava|dancavam|dancam|dancarinos|musicos|tocar|tocava)$', 'up', 'danca'),
       (r'^(segredo|segredos|cochichou|sussurrou)$', 'think', 'pensa'),
       (r'^(impossivel|absurdo|ilegal|ninguemacreditou)$', 'shrug', 'duvida'),
       (r'^(fogo|incendio|chamas)$', 'scared', 'queima')]
# ===== DICIONARIO UNIVERSAL DE ACOES (23/11, Gibson: "o que a narracao fala acontece no video", qualquer roteiro) =====
# Cada verbo e' reconhecido pela RAIZ em qualquer conjugacao (pegou/pegava/pegaram/pegando/pega...). Fica DEPOIS das regras especificas acima (elas tem prioridade).
_SUF = ('ear', 'eou', 'earam', 'eava', 'eavam', 'eando', 'eia', 'eiam', 'eado', 'eada', 'ar', 'ou', 'aram', 'ava', 'avam', 'ando', 'a', 'am', 'ado', 'ada', 'ados', 'adas', 'ara', 'er', 'eu', 'eram', 'ia', 'iam', 'endo', 'ido', 'ida', 'ir', 'iu', 'iram', 'indo', 'e', 'em', 'ei', 'aria', 'ariam')
_RAIZ = [  # (raizes, gesto, tipo, sufixos proibidos: viram substantivo/outro sentido)
    (('apert',), 'reach', 'x_aperta', ('a', 'e', 'o')),
    (('desc', 'pous', 'aterriss', 'baix'), 'point', 'x_desce', ('a', 'e', 'o', 'ar', 'em', 'ado', 'ada', 'ia', 'iam')),
    (('espalh', 'dispers', 'debAND', 'ocup', 'lot', 'reun', 'aglomer', 'agrup'), 'point', 'chega', ('a', 'e', 'o')),
    (('defend', 'proteg', 'resist', 'bloquei'), 'cross', 'x_defende', ('a', 'e', 'o', 'ido', 'ida')),
    (('troc', 'divid', 'repart', 'compartilh', 'escolh', 'selecion', 'aplic'), 'reach', 'x_entrega', ('a', 'e', 'o', 'ido', 'ida')),
    (('convers', 'dialog', 'cochich', 'fofoc', 'comb'), 'point', 'fala', ('a', 'e', 'o', 'inado', 'inada')),
    (('ensai', 'treinA', 'trein', 'exercit'), 'up', 'danca', ('a', 'e', 'o')),
    (('obedec', 'saud', 'continenc'), 'salute', 'x_saluda', ('a', 'e', 'o', 'ia', 'iam')),
    (('dirig', 'pilot', 'aceler', 'freou', 'estacion'), 'point', 'x_dirige', ('a', 'e', 'o', 'ido', 'ida')),
    (('sangr', 'feriu', 'machuc'), 'facepalm', 'x_chora', ('a', 'e', 'o')),
    (('volt', 'regress', 'retorn', 'atravess', 'cruz', 'avanc', 'desembarc', 'aproxim', 'march', 'caminh', 'and', 'entr', 'invad', 'adentr'), 'point', 'chega', ('a', 'e', 'em')),
    (('cerc', 'rode', 'sitio'), 'point', 'chega', ('a', 'am', 'e', 'em')),
    (('corr', 'fug', 'escap', 'persegu', 'galop', 'dispar a corr'), None, 'corre', ('e', 'a')),
    (('retir', 'abandon', 'recu', 'evacu', 'debAND'), None, 'sai', ()),
    (('segur', 'agarr', 'carreg', 'apanh', 'colet', 'junt', 'ench', 'coloc', 'instal', 'guard', 'recolh', 'peg', 'ergu', 'levant', 'empilh', 'arrast', 'pux'), 'lift', 'pega', ('a', 'e')),
    (('lev',), 'lift', 'pega', ('e', 'a', 'ado', 'ada', 'ados', 'adas', 'ar', 'em')),
    (('entreg', 'distribu', 'ofere', 'devolv', 'empres', 'vend', 'doa', 'repass', 'pass a'), 'reach', 'x_entrega', ('a', 'e')),
    (('acert', 'ating', 'mord', 'abat', 'rasg', 'destru', 'derrub', 'chut', 'soc', 'esmurr', 'atac', 'agred', 'espanc', 'lut', 'brig', 'enfrent', 'golpe', 'esfaque', 'apunhal', 'estrangul'), 'punch', 'golpe', ('a', 'e', 'o')),
    (('tomb', 'despenc', 'afund', 'desmai', 'trope', 'escorreg', 'desmoron', 'capot'), None, 'tomba', ('a', 'e')),
    (('dorm', 'cochil', 'adormec'), None, 'dorme', ()),
    (('tranc', 'fech', 'trav', 'bloque', 'lacr', 'empurr'), 'push', 'empurra', ('a', 'e', 'o')),
    (('apag', 'deslig', 'desliga'), 'push', 'empurra', ('a', 'e')),
    (('varr', 'limp', 'esfreg', 'lav', 'escov'), 'stir', 'x_lava', ('a', 'e', 'o')),
    (('enterr', 'cav', 'plant', 'semE', 'aduB'), 'hammer', 'x_planta', ('a', 'e', 'o')),
    (('desenh', 'rabisc', 'assin', 'anot', 'escrev', 'registr', 'redig', 'copi'), 'write', 'escreve', ('a', 'e', 'o')),
    (('brinc', 'zomb', 'deboch', 'gargalh', 'caçO'), 'up', 'x_ri', ('a', 'e', 'o')),
    (('discut', 'debat', 'ameac', 'ofend', 'xing', 'reclam', 'insult', 'brigA', 'berr', 'acus', 'disput', 'discut'), 'point', 'x_discute', ('a', 'e', 'o')),
    (('cobr',), 'point', 'x_discute', ('a', 'e', 'o', 'iu', 'ia', 'iam', 'ir', 'iram', 'indo')),
    (('coment', 'mostr', 'apont', 'explic', 'ensin', 'avis', 'anunci', 'respond', 'pergunt', 'cham', 'ped', 'promet', 'convenc', 'convid', 'mand', 'orden', 'declar', 'conv', 'propus', 'propo', 'negoci', 'apresent'), 'point', 'fala', ('a', 'e', 'o', 'ido', 'ida')),
    (('olh', 'observ', 'repar', 'espi', 'assist', 'contempl', 'encar', 'avist', 'enxerg'), 'point', 'olha', ('a', 'e', 'o')),
    (('test', 'examin', 'estud', 'analis', 'investig', 'pesquis', 'experiment', 'med'), 'think', 'examina', ('a', 'e', 'o', 'ia', 'iam', 'ida', 'ido')),
    (('bombard', 'metralh', 'alvej', 'fuzil', 'canhone', 'atir'), None, 'atira', ('a', 'e', 'o')),
    (('constru', 'fabric', 'invent', 'mont', 'martel', 'conserta', 'consert', 'soldA', 'erigi'), 'hammer', 'constroi', ('a', 'e', 'o')),
    (('devor', 'mastig', 'almoc', 'jant'), 'eat', 'x_come', ('a', 'e', 'o')),
    (('com',), 'eat', 'x_come', ('a', 'e', 'o', 'ar', 'em', 'ido', 'ida', 'ando', 'ado', 'ada')),
    (('ajud', 'socorr', 'salv', 'resgat', 'carreg'), 'reach', 'x_entrega', ('a', 'e', 'o')),
    (('segu',), 'point', 'chega', ('a', 'e', 'o', 'ro', 'ra')),
    (('trem', 'trepid', 'trem'), None, 'x_treme', ('a', 'e', 'o', 'ar', 'ia', 'iam')),
    (('comemor', 'celebr', 'festej', 'vibr', 'ganh', 'venc', 'triunf', 'conquist'), 'up', 'vence', ('a', 'e', 'o', 'ia', 'iam')),
    (('chor', 'solu', 'lament', 'lastim'), 'facepalm', 'x_chora', ('a', 'e', 'o')),
    (('danc', 'rebol', 'requebr', 'bail', 'sapate'), 'up', 'danca', ('a', 'e', 'o')),
    (('pesc',), 'lift', 'x_pesca', ('a', 'e', 'o')),
    (('costur', 'tric', 'bord'), 'write', 'x_costura', ('a', 'e', 'o')),
    (('cozinh', 'mex', 'misturA', 'fritA', 'assA'), 'stir', 'mistura', ('a', 'e', 'o')),
    (('abrac',), 'reach', 'x_abraca', ('a', 'e', 'o')),
    (('beij',), 'reach', 'x_beija', ('a', 'e', 'o')),
    (('solt', 'libert', 'larg'), 'up', 'x_solta', ('a', 'e', 'o')),
    (('aplaud', 'ovacion'), 'up', 'x_aplaude', ('a', 'e', 'o')),
    (('pul', 'salt'), 'up', 'pula', ('a', 'e', 'o')),
    (('acen',), 'up', 'acena', ('a', 'e', 'o')),
    (('ajoelh',), None, 'ajoelha', ('a', 'e', 'o')),
    (('escal', 'trep'), 'lift', 'escala', ('a', 'e', 'o')),
    (('rez', 'or', 'suplic'), 'think', 'x_reza', ('a', 'e', 'o', 'ar', 'am', 'ia', 'iam', 'ado', 'ada')),
    (('grit', 'brad', 'urr'), 'up', 'grita', ('a', 'e', 'o')),
    (('perd', 'fracass', 'falh'), 'facepalm', 'perde', ('a', 'e', 'o', 'ido', 'ida')),
    (('quebr', 'estilhac', 'despedac', 'arrebent', 'estour'), 'throw', 'quebra', ('a', 'e', 'o')),
    (('jog', 'lanc', 'arremess', 'despej', 'derram'), 'throw', 'cai', ('a', 'e', 'o')),
    (('pens', 'imagin', 'calcul', 'planej', 'refletiu'), 'think', 'pensa', ('a', 'e', 'o')),
]
for _rz, _ge, _tp, _proib in _RAIZ:
    _rz = tuple(r_.lower() for r_ in _rz if ' ' not in r_)
    _sf = '|'.join(x_ for x_ in _SUF if x_ not in _proib)
    ENC.append((r'^(' + '|'.join(_rz) + r')(' + _sf + r')$', _ge, _tp))
ENC_MAT = [(r'borracha|latex|seiva|goma|gosma|massa|pasta|cola|mistura', 'kit/gosma'), (r'enxofre|polvora|\bpo\b', 'kit/enxofre'), (r'quimic|acido|liquido|reagente', 'kit/frasco'), (r'ovo', 'kit/egg'), (r'chocolate', 'kit/chocolate')]
ENC_RES = [(r'borracha|elastic|firme|couro|vulcaniz', 'kit/borracha'), (r'pneu', 'kit/tires'), (r'\bbola\b', 'kit/ball'), (r'pipoca', 'kit/popcorn'), (r'chocolate', 'kit/chocolate'),
           (r'post.?it|bilhete', 'kit/postit'), (r'velcro|carrapicho', 'kit/burr'), (r'penicilina|mofo|bolor|placa', 'kit/petri'), (r'raio.?x|radiograf', 'kit/xray_plate'), (r'vacina|seringa', 'kit/syringe'),
           (r'foguete', 'kit/rocket'), (r'balao', 'kit/balloon'), (r'para.?raio', 'kit/lightning_rod'), (r'microondas', 'kit/microwave'), (r'telefone|celular', 'kit/phone'), (r'televis', 'kit/tv'), (r'moeda|bitcoin', 'kit/bitcoin')]
_DANCA_OUTRO = r'(atomos|moleculas|cobras|chamas|estrelas|folhas|ondas|particulas|letras|numeros)\s*(\w{0,12}\s*)?danc|danc\w*\s*como|sonho'   # quem danca e' a coisa (sonho, atomos...), nao o personagem
OBJ_DICT = [  # (palavra na narracao, objeto 3D da biblioteca, escala, grande?) -- usado para por objetos em cena e na pre-producao
    (r'\bbarril\b|\bbarris\b|aguardente|cerveja|\bvinho\b|\brum\b', 'barrel', 1.1, False), (r'caixote|\bcaixas\b|\bcarga\b|mercadoria', 'crate', 1.0, False), (r'\bcanhao\b|\bcanhoes\b|artilharia', 'cannon', 1.0, False),
    (r'\bbaldes?\b|\bpoco\b', 'tools/bucket', 1.8, False), (r'\bfonte\b|chafariz', 'nature/fountain', 1.2, False), (r'\bbandeiras?\b|estandarte', 'war/flagpole', 1.3, False), (r'\btambor\b|\btambores\b', 'war/drum', 1.4, False),
    (r'trincheira|barricada|sacos de areia', 'war/sandbags', 1.2, False), (r'\bescudos?\b', 'war/shield', 1.5, False), (r'\bfeno\b|trigo|plantac|colheita', 'nature/haybale', 1.1, False), (r'espantalho', 'nature/scarecrow', 1.2, False),
    (r'lanterna|lampiao|lamparina', 'tools/lantern', 1.2, False), (r'\bescadas?\b', 'tools/ladder', 1.2, False), (r'carrinho de mao', 'tools/wheelbarrow', 1.2, False), (r'ferreiro|bigorna', 'tools/anvil', 1.3, False),
    (r'\btulipas?\b|\bbulbos?\b|\bflor\b|\bflores\b', 'kit/tulip_red', 1.3, False), (r'\bcova\b|tumulo|enterr|caixao|cemiterio', 'kit/grave', 1.0, False), (r'\bbatatas?\b|\bhorta\b|\blegumes?\b', 'nature/flowerbed', 1.2, False),
    (r'\bbola\b|futebol|\bgol\b|partida|estadio', 'kit/ball', 1.0, False), (r'\bchaleira\b|\bpanelas?\b|\bsopa\b|caldeirao', 'kit/kettle', 1.0, False), (r'\bcerca\b|cercado|curral|fazenda|\bhorta\b', 'nature/picket_fence', 1.2, False),
    (r'\bbolos?\b|\bdoces?\b|confeit|padaria|\bpastel\b|\bpasteis\b', 'kit/cake_table', 1.0, False), (r'\btrono\b|coroad', 'kit/throne', 1.0, 'in'), (r'fogueira|acampamento|acamparam', 'kit/campfire', 1.2, False),
    (r'\btenda|barraca de campanha|acampamento', 'kit/tent', 1.3, True), (r'\bbau\b|tesouro|\bcofre', 'kit/chest', 1.2, False), (r'\bfeira\b|\bmercado\b|\bbarracas?\b|\bvendedor\b', 'kit/stall', 1.0, False),
    (r'lareira', 'kit/fireplace', 1.3, False), (r'\bcadeira\b|poltrona', 'mk/Chair_1', 1.2, False), (r'\btrem\b|locomotiva|ferrovia', 'vehicles/locomotive', 1.3, True), (r'\bcarrocas?\b', 'vehicles/wagon', 1.2, True), (r'tanque de guerra|blindado', 'vehicles/tank', 1.2, True), (r'\baviao\b|\bavioes\b|biplano|bombardeiro|aeronave', 'vehicles/airplane', 1.2, True),
    (r'\btorres?\b|\bmuralhas?\b|\bcastelo\b|\bfortaleza\b|\bpalacio\b', 'buildings/castle_tower', 1.3, True), (r'\bmoinhos?\b', 'buildings/windmill', 1.2, True), (r'\bigreja\b|\bcatedral\b', 'buildings/church', 1.2, True), (r'\bfarol\b', 'buildings/lighthouse', 1.2, True), (r'\bponte\b', 'buildings/bridge', 1.2, True),
]
LUGARES = [  # (palavra na narracao, [(modelo, x, z, escala), ...]) -- cenografia de fundo do lugar citado
    (r'fazenda|fazendeiro|sitio|\bhorta\b|plantac|lavoura|celeiro|curral', [('buildings/barn', 5.5, -10.0, 1.2), ('nature/picket_fence', -3.4, -2.6, 1.3), ('nature/haybale', 3.6, -1.4, 1.1), ('nature/scarecrow', -4.6, -4.5, 1.2)]),
    (r'\bcasa\b|\bcasas\b|vizinho|aldeia|vila\b|vilarejo', [('buildings/house_small', -5.5, -10.0, 1.25), ('nature/picket_fence', 3.4, -2.8, 1.3), ('nature/tree_oak', 6.5, -7.0, 1.3)]),
    (r'\bigreja\b|\bcatedral\b|\bpadre\b|\bsino\b', [('buildings/church', 5.5, -11.0, 1.2)]),
    (r'\bmercado\b|\bfeira\b|\bloja\b|comerciante|\bvendedor\b', [('buildings/shop', -5.0, -9.5, 1.25), ('kit/stall', 3.6, -2.6, 1.0)]),
    (r'\bflorestas?\b|\bmata\b|\bbosque\b|\bselva\b', [('nature/tree_pine', -5.5, -8.5, 1.5), ('nature/tree_oak', 5.0, -9.0, 1.5), ('nature/tree_pine', 8.0, -7.5, 1.3), ('nature/bush', -6.5, -4.5, 1.2)]),
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
        say = nrm(b['say']); _ng = _neg_idx(b['say']); words = [nrm(w) for i_, w in enumerate(b['say'].split()) if i_ not in _ng]   # palavra negada nao vira batalha
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
            if b.get('crowd') is None:
                persons_out = [w.split(':')[0] for w in b.get('who', [])]
                army = persons_out[0] if persons_out else (outs[0] if outs else 'X')
                b['crowd'] = {'n': (12 if b.get('impact') else 5) if b.get('emus') else (18 if (b.get('impact') or (mass and (arrive or first))) else 10 if mass else 6), 'outfits': list(dict.fromkeys(persons_out + [army])), 'march': bool(arrive or first or (shot == 'reveal' and mass)) and not (b.get('impact') and any(SHOOT.match(w_) for w_ in words))}
            if not b.get('who'): b['who'] = [f"{b['crowd']['outfits'][0]}:0:neutral"]
            _sy = __import__('unicodedata').normalize('NFKD', b.get('say', '').lower()).encode('ascii', 'ignore').decode()
            if re.search(r'multid|milhares|milhoes|\bmil pessoas|lotad|lotou|lotaram|centenas|todo mundo|populac|\bpovo\b|torcida|plateia|publico|cheio de gente|aglomer|protesto|manifesta|fila enorme', _sy) and not b.get('emus'):
                b['crowd']['n'] = max(int(b['crowd'].get('n', 0)), 30); b['crowd']['lotado'] = True   # "varias pessoas" na narracao: encher a tela de gente (ordem do Gibson 19/11)
        else:
            run += 1
            if b.get('impact') and b.get('crowd') is None and b.get('who') and not b.get('emus'):
                b['crowd'] = {'n': 10, 'outfits': list(dict.fromkeys(w.split(':')[0] for w in b['who'])), 'march': False, 'expr': 'shock'}
            if mass and b.get('crowd') is None and b.get('who') and not b.get('emus'):
                persons_out = [w.split(':')[0] for w in b['who']]
                b['crowd'] = {'n': 5, 'outfits': list(dict.fromkeys(persons_out)), 'march': False, 'expr': 'shock' if re.search('panico|tiro|gritou', say) else 'neutral'}

# ===== MODO DE ACAO (ordem do Gibson 19/11): a frase diz o que acontece -> a cena mostra =====
# desembarque de navio na praia, batalhao esperando (com o nome na placa), dois exercitos indo um contra o outro, gente voando na explosao,
# generais conversando, aperto de mao/paz, voltar para casa. Cada regra marca a cena; o build encena.
_EXERC = [k_ for k_, o_ in B.get('outfits', {}).items() if o_.get('rifle') or str(o_.get('profissao', '')).lower() == 'soldado']
_PAISES = {}
for k_ in _EXERC: _PAISES.setdefault(str(B['outfits'][k_].get('pais') or k_[:3]).lower(), k_)
_LADOS = list(_PAISES.values())[:2] if len(_PAISES) >= 2 else None
for _ib, _b in enumerate(B['beats']):
    if _b.get('modo_acao') is False: continue
    _s = __import__('unicodedata').normalize('NFKD', _b['say'].lower()).encode('ascii', 'ignore').decode()
    if re.search(r'desembarc|navios? .{0,30}(chegou|chegaram|atracou|atracaram|aportou|apareceram)|(chegou|chegaram|vieram|veio) .{0,25}(de navio|de barco|pelo mar|na praia)|aportaram|atracaram', _s):
        _b['desembarque'] = True; _b.setdefault('set', 'harbor'); _b['shot'] = 'wide'; _b['shot_lock'] = True
        _o = [w_.split(':')[0] for w_ in _b.get('who', [])] or _EXERC[:1]
        if _o: _b.setdefault('crowd', {'n': 12, 'outfits': list(dict.fromkeys(_o)), 'march': True})
    if re.search(r'esperando|aguardava|aguardavam|de tocaia|emboscada|escondid[oa]s? atras|a espera', _s) and re.search(r'batalh|tropa|exercito|soldad|regiment|inimig', _s):
        _b['esperando'] = True; _b['impact'] = False; _b['batalha'] = False; _b['shot'] = 'group'; _b['shot_lock'] = True
        _o = [w_.split(':')[0] for w_ in _b.get('who', [])] or _EXERC[-1:]
        if _o: _b.setdefault('crowd', {'n': 12, 'outfits': list(dict.fromkeys(_o)), 'march': False, 'expr': 'stern'})
    _nm = re.search(r'(?:batalh[aã]o|regimento|brigada)s? (?:\w+ )?(?:do|da|de) (?:general |coronel |capit[aã]o |marechal |almirante )?([A-ZÁÉÍÓÚ][\wÀ-ú]+)', _b['say'])
    if _nm and not _b.get('text'): _b['text'] = ('BATALHÃO ' + _nm.group(1)).upper()
    if _LADOS and re.search(r'um contra o outro|uns contra os outros|se enfrentaram|frente a frente|avancaram|atacaram|comecou a batalha|comecou a guerra|lutaram|combate|batalha comecou', _s) and not _b.get('esperando'):
        _b['batalha'] = True; _b['lados'] = _LADOS
    if re.search(r'voaram|voou pelos ares|pelos ares|arremessad|lancados longe|jogados longe|explodiu|explodiram|explosao|explosoes|bomba|granada|canhao|canhoes|canhonaços|artilharia|morteiro|bombarde', _s) and (_EXERC or _b.get('batalha')):
        _b['voando'] = 3 if re.search(r'voaram|pelos ares|arremess|lancados|jogados', _s) else 2
        if _LADOS: _b['lados'] = _LADOS
    if re.search(r'conversar|conversaram|conversavam|dialog|negoci|reuniram|reuniao|discutiram|combinaram|sentaram para', _s) and len(_b.get('who', [])) >= 2 and not _b.get('acao'):
        _b['acao'] = 'conversar'
    if re.search(r'apertaram as maos|aperto de mao|apertou a mao|cumprimentaram|fizeram as pazes|fizeram a paz|selaram a paz|acordo de paz|tratado de paz|assinaram a paz', _s) and len(_b.get('who', [])) >= 2:
        _b['interacao'] = 'apertar'; _b['shot'] = 'two'; _b['shot_lock'] = True
    if re.search(r'(voltou|voltaram|foram|foi|retornaram|retornou) (embora )?para casa', _s): _b['para_casa'] = True; _b.pop('interior', None)
    if _b.get('desembarque') or _b.get('esperando') or _b.get('lados') or _b.get('voando'):   # batalha/desembarque/tropa esperando: ao ar livre, no lugar da historia (nunca numa sala ou num cenario sorteado)
        _b.pop('interior', None)
        if not _b.get('_lug_ok') and _ib not in _EXPL: _b['set'] = SET
        _b['_lug_ok'] = True
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
    _cand = [i for i, b in enumerate(beats) if 0 < i < len(beats) - 1 and not re.search(r'ninguemdeu|ninguematirou|semdar|nenhumtiro|naoatir|semtiro|empaz|festa', nrm(b['say'])) and not b.get('interacao') and b.get('shot') not in ('low', 'close') and not b.get('impact') and not b.get('shot_lock') and not b.get('interior') and not b.get('veiculo') and all(abs(i - j) > 1 for j in _im)]
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
# VARIEDADE DE CAMERA (23/11, Gibson: "a camera, os angulos, os closes"): duas cenas seguidas nunca com o mesmo enquadramento nem o mesmo lado de camera.
if B.get('director') is not False and B.get('variar_camera') is not False:
    _AZ = ((-6, 8), (-26, -12), (16, 30), (-14, 4), (24, 10), (-32, -18))
    _lk = lambda _b: _b.get('shot_lock') or _b.get('veiculo') or _b.get('impact') or _b.get('batalha') or _b.get('mapa')
    _plug = lambda _b: ('i' + str(_b['interior'])) if _b.get('interior') else _b.get('set', SET)
    _na = 0
    for _i, _b in enumerate(beats):
        _sh = _b.get('shot', 'two')
        if _i > 0 and not _lk(_b) and _sh not in WIDE and _sh == beats[_i - 1].get('shot', 'two') and _plug(_b) == _plug(beats[_i - 1]):
            _nw_ = len(_b.get('who', []))
            _b['shot'] = {'two': 'close' if _nw_ <= 1 else 'group', 'close': 'two', 'group': 'two', 'low': 'two'}.get(_sh, _sh)   # close so' com 1 pessoa (2 no close saiam cortados)
        if _b.get('shot', 'two') not in WIDE and not _b.get('veiculo') and 'az0' not in _b and 'az1' not in _b:
            _k_ = 0.4 if _b.get('interior') else 1.0; _b['az0'], _b['az1'] = (round(_AZ[_na % len(_AZ)][0] * _k_), round(_AZ[_na % len(_AZ)][1] * _k_)); _na += 1   # sala: angulo menor (nao mostrar o vazio atras da parede)
# CAVALARIA AUTOMATICA (ordem do Gibson 19/11): ate 1918 tropa chegando/atacando vem com soldados a cavalo; a narracao citar cavalo/cavalaria sempre poe.
_CAVW = re.compile(r'cavalari|a cavalo|montad|galop|cavaleiros|hussard|lanceiro|dragoes|cossaco|cavalos')
if B.get('cavalaria') is not False and ANO and ANO <= 1918:
    _ncav = 0
    for _k, _b in enumerate(beats):
        if _b.get('cavalaria') is not None or _b.get('interior') or _b.get('veiculo') or _b.get('set', SET) in ('harbor', 'arctic', 'palace'): continue   # mar/porto: nao tem cavalaria
        _sy = nrm(_b['say'])
        _mil = any(B.get('outfits', {}).get(w_.split(':')[0], {}).get('rifle') for w_ in _b.get('who', []))
        if _CAVW.search(_sy) or (_mil and _ncav < 2 and (_b.get('impact') or (MASS.search(_sy) and ARRIVE.search(_sy)))):
            _b['cavalaria'] = {'n': 4 if _b.get('shot') in WIDE else 2}; _ncav += 1
# ENCENACAO: cena que narra um PROCESSO (misturou, caiu no fogao, virou, construiu...) fica em plano medio para o objeto e as maos aparecerem
for _b in beats:
    if _b.get('encena') is False or _b.get('shot') in WIDE or _b.get('veiculo'): continue
    _tem_mat = any(re.search(r_, nrm(_b['say'])) for r_, a_ in ENC_MAT + ENC_RES) or any(re.search(r'stove|panela|kettle|bancada', str(p_[0])) for p_ in (_b.get('props') or []))
    if any(re.match(rx_, nrm(w_)) for w_ in _b['say'].split() for rx_, g_, t_ in ENC if t_ in ('mistura', 'constroi', 'quimico', 'examina') or (t_ in ('vira', 'cai', 'calor') and _tem_mat)):
        _b['_enc'] = True
        if _b.get('shot') in ('close', None): _b['shot'] = 'two'
        _n = len(_b.get('who', [])); _sl = slots(max(_n, 1))
        for _p in (_b.get('props') or []):   # o fogao/panela do processo fica NA FRENTE de quem faz (nunca em cima de outro personagem)
            if re.search(r'stove|fire|campfire|panela|kettle|bancada|wash_basin', str(_p[0])) and len(_p) > 2 and any(abs(float(_p[1]) - x_) < 1.5 for x_ in _sl[1:]):
                _sd = (1 if _sl[0] <= 0 else -1) if _n > 1 else 1; _p[1] = round(_sl[0] + _sd * 1.1, 2); _p[2] = round(ZS[0] + 0.7, 2); _p[3:] = [min(float(_p[3]) if len(_p) > 3 else 1.0, 0.9)]
for _b in beats:   # "entraram escondidos" -> alguem chega andando; "as luzes se apagaram" -> fica de noite
    _sy = nrm(_b['say'])
    if 'chega' not in _b and (re.search(r'escondid|sorrateir|pontadospes|invadiu|invadiram|invadia|entraram|entrou|chegado|chegava|chegou|chegaram', _sy) or re.search(r'\bchega\b|\bchegam\b', _b['say'].lower())): _b['chega'] = True
    if re.search(r'marchav|marcharam|marchou|marchando|desfil', _sy) and _EXERC and not _b.get('crowd'): _b['crowd'] = {'n': 10, 'outfits': [([w_.split(':')[0] for w_ in _b.get('who', []) if w_.split(':')[0] in _EXERC] or _EXERC)[0]], 'march': True}
    if re.search(r'danca|dancav|dancaram|dancou', _sy) and not _b.get('acao') and not re.search(_DANCA_OUTRO, _sy): _b['acao'] = 'dancar'
    if 'hora' not in _b and re.search(r'apagar|apagou|apagaram|escuridao|breu|semluz|blecaute|apagao', _sy): _b['hora'] = 'noite'
for _b in beats:   # ESPACO (19/11): "no espaco/em orbita/na lua" -> chao lunar (arctic acinzentado) + ceu preto estrelado
    if not _b.get('interior') and re.search(r'noespaco|emorbita|naorbita|nalua|superficiedalua|estacaoespacial|gravidadezero|semgravidade', nrm(_b['say'])):
        _b.setdefault('set', 'arctic'); _b.setdefault('hora', 'espaco')
_noite_ = 0   # CONTINUIDADE DA NOITE (19/11): "numa noite..." vale para as frases seguintes do mesmo episodio, ate a narracao mudar o tempo
for _b in beats:
    _sy = nrm(_b['say'])
    if re.search(r'diasdepois|anosdepois|mesesdepois|semanasdepois|horasdepois|diaseguinte|amanhec|demanha|manhaseguinte|nascerdosol|aodia|durante odia|duranteodia|maistarde|tempodepois|ateh?oje|atehoje', _sy) or _b.get('hora') not in (None, 'noite') or _b.get('light') or _b.get('mapa'): _noite_ = 0
    elif re.search(r'numanoite|naquelanoite|anoite|denoite|aquelanoite|madrugada|noescuro', _sy): _noite_ = 6
    elif _noite_ > 0 and 'hora' not in _b and not _b.get('interior'): _b['hora'] = 'noite'; _noite_ -= 1
# EMOCAO EM CLOSE + PEDIDO EM PLANO DE AMBIENTE (ordem do Gibson 19/11): "se a narracao diz que ele esta muito preocupado, close no personagem mostrando que esta preocupado";
# "quando for fazer um pedido, mostrar a ambientacao com ele fazendo o pedido". 'emocao_close': false no beat (ou no arquivo) desliga.
_EMO = re.compile(r'preocup|aflit|ansios|nervos|desconfi|suspeit|desesper|apavor|assust|triste|tristeza|chorou|choro|lagrima|furios|raiva|irritad|indignad|insatisf|frustr|decepcion|alegr|feliz|contente|emocion|orgulh|aliviad|surpres|chocad|espantad|determinad|decidid|envergonh|humilh|com medo|medo de|ciume|inveja')
_PED = re.compile(r'\bpediu|\bpedir|\bpedindo|\bpediram|implor|suplic|\bpedido|ajuda|socorro|por favor|convenc|oferec')
if B.get('director') is not False and B.get('emocao_close') is not False:
    _seq = 0
    for _k, _b in enumerate(beats):
        _sy = nrm(_b['say'])
        _livre = not (_b.get('acao') in ('conversar', 'discutir') or _b.get('interacao') or _b.get('_enc') or _b.get('shot_lock') or _b.get('impact') or _b.get('batalha') or _b.get('veiculo') or _b.get('mapa') or _b.get('emocao_close') is False or _b.get('shot') in WIDE or _b.get('crowd', {}).get('n', 0) > 6)
        if _livre and _PED.search(_sy) and len(_b.get('who', [])) >= 2:
            _b['shot'] = 'two'; _b.setdefault('interacao', 'pedir'); _b['_pedido'] = True; _seq = 0
            _w0 = _b['who'][0].split(':'); _w0 += [''] * (3 - len(_w0))
            if _w0[2] in ('', 'neutral', 'smile', 'stern'): _w0[2] = 'pleading'; _b['who'][0] = ':'.join(_w0)
            PLANO.append((_k, 'pedido: plano medio dos dois, um pede ao outro', 'shot'))
        elif _livre and _EMO.search(_sy) and _seq < 2 and _k > 0:
            _b['shot'] = 'close'; _b['_emo_close'] = True; _b.pop('perto', None); _seq += 1
            if len(_b.get('who', [])) > 1: _b['_who_todo'] = list(_b['who']); _b['who'] = _b['who'][:1]   # o close e' de quem sente: so' ele no quadro, centralizado
        else: _seq = 0
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
    if b.get('_emo_close') and shot == 'close': T.update(d0=3.5, d1=2.9, h=2.55)   # EMOCAO: camera chega no rosto (a cara diz o que ele sente)
    if b.get('perto') and shot in ('two', 'group', 'low', 'close'): T['d0'] *= b['perto']; T['d1'] *= b['perto'] * 0.94
    _n = len(b.get('who', []))
    if shot in ('two', 'group', 'low') and _n >= 3: T['d0'] *= 1 + 0.13 * (_n - 2); T['d1'] *= 1 + 0.13 * (_n - 2)   # 3+ pessoas: abre o suficiente para caber todo mundo
    light = b.get('light')
    _sy = nrm(b['say']); global AMB
    # HORA DO DIA e CLIMA: campos "hora" (dia|tarde|pordosol|noite|amanhecer) e "clima" (sol|calor|chuva|tempestade|neve|neblina|vento|limpo), ou pelas palavras da narracao. Ficam valendo ate mudar.
    _h = b.get('hora') or ('espaco' if re.search(r'noespaco|noespacosideral|emorbita|naorbita|nalua|superficiedalua|estacaoespacial|gravidadezero|semgravidade|flutuavam|flutuando', _sy) and not b.get('interior') else None) or ('noite' if re.search(r'noite|noescuro|madrugada|meianoite', _sy) else 'amanhecer' if re.search(r'amanhecer|manhaseguinte|nascerdosol|aurora|demanha', _sy) else 'pordosol' if re.search(r'pordosol|entardecer|anoitecer|fimdetarde|finaldetarde|fimdodia', _sy) else 'tarde' if re.search(r'atarde|detarde|natarde', _sy) else 'dia' if re.search(r'diaseguinte|diasdepois|semanasdepois|mesesdepois|anosdepois|meiodia|duranteodia', _sy) else None)
    _c = b.get('clima') or ('tempestade' if re.search(r'tempestade|temporal|trovao|raios', _sy) else 'chuva' if re.search(r'chuva|chovia|chovendo|choveu|aguaceiro', _sy) else 'neve' if re.search(r'neve|nevasca|nevava|nevando|inverno|congel|geada|muitofrio|friointenso|frioextremo|gelado|gelada', _sy) else 'neblina' if re.search(r'neblina|nevoeiro|nevoa|cerracao', _sy) else 'calor' if re.search(r'calor|solforte|solquente|escaldante|\\bseca\\b|sedeinsuport|muitoquente|deserto', _sy) else 'vento' if re.search(r'ventania|vendaval|furacao|ventoforte|\\bvento\\b|ventava|ventando', _sy) else None)
    AMB['hora'] = B.get('hora'); AMB['clima'] = None if B.get('clima') in (None, 'limpo', 'sol') else B.get('clima')   # hora/clima valem SO na cena onde aparecem (campo ou narracao); fora disso, o padrao do topo do roteiro -- a noite/neve de uma cena nao vaza para o resto do video
    if _h: AMB['hora'] = _h
    if _c: AMB['clima'] = None if _c in ('limpo', 'sol') else _c
    b['_frio'] = AMB.get('clima') == 'neve'; b['_calor'] = AMB.get('clima') == 'calor'   # frio: os personagens tremem; calor: suam (luz de deserto)
    wx = {}
    if not light:
        light = {'noite': 'night', 'espaco': 'space', 'amanhecer': 'dawn', 'pordosol': 'dusk', 'tarde': 'golden'}.get(AMB.get('hora'), LIGHT)
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
    if b.get('interior') and not b.get('light'): light = 'study_dark' if (b.get('hora') == 'noite' or re.search(r'apagou a luz|apagaram a luz|apagou as luzes|no escuro|escurid|luz apagada|a noite toda|madrugada|de noite|\bnoites?\b', b['say'].lower())) else 'study'   # dentro de casa a noite/luz apagada: sala na penumbra
    if b.get('interior') == 'galpao' and not b.get('light'): light = 'overcast'   # galpao iluminado: luz branca fria (nao a luz amarela de sala)
    mv = b.get('move', 8 if shot == 'track' else 0)
    a, bb = f'A[{k}]', f'A[{k + 1}] - 1'
    # elenco de pessoas
    HOLDS = (('rifle', r'espingarda|fuzil|mosquete|carabina|pegou a arma|sacou a arma'), ('mug', r'beber|bebeu|bebia|brind|caneca|cerveja|\bcha\b'), ('bottle', r'garrafa|aguardente|vinho|bebida|\brum\b|whisky|uisque'), ('paper', r'carta|jornal|imprensa|ordem|documento|mapa|contrato|telegrama|relatorio|\blista\b|assinou|lei\b'), ('book', r'livro|biblia|diario'), ('lantern', r'lanterna|lampiao|lamparina'), ('torch', r'tocha|incendi'), ('flag', r'bandeira|\brendeu\b|\brenderam\b|\brendicao\b'), ('sword', r'\bespadas?\b|\bduelo\b|\bduelaram\b|esgrima|\bsabre\b'), ('money', r'dolar|dolares|libras|notas|cedulas|\\bpago\\b'), ('coin', r'dinheiro|moeda|\bouro\b|recompensa|pagou|pagar|fortuna|salario|imposto'), ('shovel', r'cavou|cavaram|cavando|cavar|trincheira|enterrou|enterraram|\\bcova\\b'), ('bag', r'saco|mala|bagagem|sacola'), ('spyglass', r'luneta|avistou|avistaram|procurar|vigia|observ'), ('tulip', r'tulipa|bulbo|flor\b|flores'))
    _say_sp = re.sub(r'[^a-z0-9 ]', '', unicodedata.normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode())
    auto_hold = next((h for h, rx in HOLDS if re.search(rx, _say_sp)), None) if b.get('maos') is not False else None
    _acao = b.get('acao') or ('dancar' if re.search(r'\bdanc', _say_sp) and not re.search(_DANCA_OUTRO, _say_sp) else 'discutir' if (re.search(r'discut|brig|exigi|respondeu|gritou|ameac|insult', _say_sp) and len(b.get('who', [])) >= 2) else None)
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
    # ROSTO NA PALAVRA (sincronismo, ordem do Gibson): "gritou", "chorou", "riu", "assustou"... -> a cara muda NO INSTANTE da palavra
    _WEX = ((r'^(gritou|gritaram|gritava|berrou|berraram|socorro)$', 'shout'), (r'^(chorou|choraram|chorava|lagrimas|choro)$', 'cry'), (r'^(riu|riram|gargalhou|gargalhada|gargalhadas|risada|risadas)$', 'laugh'),
            (r'^(assustou|assustaram|assustado|assustados|medo|apavorado|apavorados|panico|pavor)$', 'scared'), (r'^(chocado|chocou|espantado|espanto|surpreso|surpresa|incrivel|impossivel)$', 'shock'),
            (r'^(raiva|furioso|furiosos|irritado|irritou|bravo|odio|indignado)$', 'angry'), (r'^(comemorou|comemoraram|vitoria|venceu|venceram|festa|conseguiu|conseguiram)$', 'laugh'),
            (r'^(triste|tristeza|morreu|morreram|perdeu|perderam|luto)$', 'sad'), (r'^(nervoso|nervosa|nervosos|ansioso|ansiosa|tenso|tensa)$', 'nervous'), (r'^(aliviado|alivio|salvos|salvou)$', 'relief'),
            (r'^(preocupado|preocupada|preocupados|preocupadas|preocupacao|aflito|aflita|angustiado|angustia)$', 'worried'), (r'^(desconfiado|desconfiada|desconfiou|desconfianca|suspeitou|suspeita|duvidou)$', 'distrust'),
            (r'^(insatisfeito|insatisfeita|insatisfeitos|reclamou|reclamaram|frustrado|frustrada|decepcionado|decepcionada|chateado|chateada)$', 'annoyed'),
            (r'^(decidiu|decidiram|determinado|determinada|resolver|resolveu|enfrentar|jurou)$', 'determined'), (r'^(feliz|felizes|alegre|alegria|contente|animado|animada|empolgado)$', 'happy'),
            (r'^(pediu|pediram|implorou|imploraram|suplicou|ajuda|socorro|favor)$', 'pleading'))
    _wxs = []
    if b.get('rosto_palavra') is not False:
        _ngE = _neg_idx(b['say'])
        for j_, w_ in enumerate(b['say'].split()):
            if j_ in _ngE: continue
            nw_ = nrm(w_); hit_ = next((e_ for rx_, e_ in _WEX if re.match(rx_, nw_)), None)
            if hit_ and j_ >= 1 and (not _wxs or _wxs[-1][1] != hit_): _wxs.append((starts[k] + j_, hit_))
    def _exj(e0):
        seq_ = [(wi_, ex_) for wi_, ex_ in _wxs if ex_ != e0]
        if not seq_: return json.dumps(e0)
        return "((f) => " + ''.join(f"f >= WS({wi_}) - 4 ? {json.dumps(ex_)} : " for wi_, ex_ in reversed(seq_)) + json.dumps(e0) + ")"
    for _, _eh in _wxs: PLANO.append((k, '(rosto) ' + _eh, 'expr'))
    for i, (out, v, ex, hold) in enumerate(persons):
        ov = f", over: {{ hold: {json.dumps(hold)} }}" if hold else ''
        dx, z = sl[i], (ZSW[i % len(ZSW)] if shot in WIDE else ZS[i % len(ZS)])
        if shot == 'track' or mv:
            d = mv if mv else 8
            acts.append(f"{{ outfit: {json.dumps(out)}, v: {v}, at: [X + {num(dx - d / 2)}, {num(z)}], move: [[X + {num(dx + d / 2)}, {num(z)}], {a}, {bb}, 'lin'], pose: {json.dumps('run' if re.search(r'corre|correu|correram|fugi|fuga|disparou em|debandada|persegui', _say_sp) else 'march' if B.get('outfits', {}).get(out, {}).get('rifle') else 'stroll')}, expr: {_exj(ex)}{ov} }}")   # correu/fugiu: CORRE; soldado marcha; civil caminha solto
        else:
            _pp = _px if _px else (", pose: 'react'" if ex in ('shock', 'nervous') else '' if (hold or shot in WIDE or b.get('acao') == 'nenhuma') else ", pose: 'talk'")   # ninguem fica so piscando: sem acao marcada, gesticula de leve
            if _pp and not _px: b['_acao'] = b.get('_acao') or ('reagir' if 'react' in _pp else 'conversar')
            if _chega and i == len(persons) - 1 and len(persons) >= 2 and shot not in WIDE:   # CHEGADA: entra andando pela lateral e para no lugar
                sd_ = 1 if dx >= 0 else -1; b['_chega'] = True
                acts.append(f"{{ outfit: {json.dumps(out)}, v: {v}, at: [X + {num(dx + sd_ * 2.4)}, {num(z - 1.6)}], move: [[X + {num(dx)}, {num(z)}], {a}, Math.round({a} + Math.min(48, ({bb} - ({a})) * 0.3)), 'lin'], arrive: true, walk: {json.dumps('march' if B.get('outfits', {}).get(out, {}).get('rifle') else 'stroll')}, look: {num(-0.4 if dx > 0 else 0.4)}, expr: {_exj(ex)}{ov} }}")
            else:
                acts.append(f"pp(X, {json.dumps(out)}, {v}, {num(dx)}, {num(z)}, {_exj(ex)}" + (f", {{ over: {{ {'rifle: true' if hold == 'rifle' else 'hold: ' + json.dumps(hold)} }}{_pp} }})" if hold else (f", {{ {_pp[2:]} }})" if _pp else ')')))
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
            # ACOES DO ANIMAL NA PALAVRA (ordem do Gibson: "o porco entrando na fazenda caminhando... o fazendeiro atirando no porco")
            _aw = b['say'].split(); _ngA = _neg_idx(b['say']); _af = lambda rx_: next((starts[k] + j_ for j_, w_ in enumerate(_aw) if j_ not in _ngA and re.match(rx_, nrm(w_))), None)
            _w_come = _af(r'^(comendo|comeu|comia|comiam|fucando|fucava|pastando|pastava|bicando|roendo|devorou|mastigando)$')
            _w_entra = _af(r'^(entrando|entrou|invadiu|invadindo|chegou|chegando|apareceu|caminhava|caminhando|andava|andando|passeava|fugido|escapou|soltou)$')
            _w_foge = _af(r'^(fugiu|fugindo|correu|correndo|disparou|sumiu)$')
            _w_tiro = _af(r'^(atirou|matou|mataram|morreu|baleado|abatido|abateu|tiro)$') if re.search(r'porco|animal|bicho|vaca|cachorro|cao|lobo|urso|cavalo|ganso|galinha|emu|ovelha|cabra|ave|veado', nrm(b['say'])) else None
            _w_alert = _af(r'^(assustou|assustado|assustada|espantou|latiu|latia|grunhiu|mugiu|berrou|uivou)$')
            _seq = sorted([(w_, s_) for w_, s_ in ((_w_come, 'root' if key == 'animal' else 'peck'), (_w_tiro, 'fall'), (_w_alert, 'alert'), (_w_foge, 'trot')) if w_ is not None])
            if _w_tiro is not None: _seq = [x_ for x_ in _seq if x_[0] <= _w_tiro or x_[1] == 'fall']
            _onde_ = (b.get('set') or SET, bool(b.get('interior')))
            if _w_tiro is not None: STATE.setdefault('mortos', set()).add(sp); STATE.setdefault('morto_onde', {})[sp] = _onde_   # o animal que levou o tiro fica caido nas cenas seguintes (coerencia da historia)
            elif sp in STATE.get('mortos', set()):
                if STATE.get('morto_onde', {}).get(sp, _onde_) != _onde_: continue   # morto fica ONDE morreu: em outro lugar (gabinete, porto) ele nao aparece
                _seq = []; _w_entra = _w_foge = None; st = 'fall'
            _st0 = 'trot' if _w_entra is not None else st
            _stjs = json.dumps(_st0) if not _seq else "(f) => " + ''.join(f"f >= WS({w_}) ? {json.dumps(s_)} : " for w_, s_ in sorted(_seq, reverse=True)) + (f"f >= WS({_w_entra}) + 40 ? 'stand' : 'trot'" if _w_entra is not None else json.dumps(st))
            _mvjs = ''
            if _w_entra is not None: _mvjs = f", at: [X + {num(dxa + 9 * (1 if dxa >= 0 else -1))}, {num(za - 1.0)}], move: [[X + {num(dxa)}, {num(za)}], WS({_w_entra}), WS({_w_entra}) + 40, 'lin'], flip: {'false' if dxa >= 0 else 'true'}"
            elif _w_foge is not None: _mvjs = f", at: [X + {num(dxa)}, {num(za)}], move: [[X + {num(dxa + 12 * (1 if dxa >= 0 else -1))}, {num(za - 2)}], WS({_w_foge}), WS({_w_foge}) + 45, 'lin'], flip: {'true' if dxa >= 0 else 'false'}"
            if _w_tiro is not None: b.setdefault('_anfx', []).append(f"{{ k: 'stars', a: WS({_w_tiro}) + 4, b: WS({_w_tiro}) + 40, at: [X + {num(dxa)}, DK + 1.6, {num(za)}], s: 0.7 }}")
            for w_, d_ in ((_w_come, 'come'), (_w_entra, 'entra caminhando'), (_w_foge, 'foge correndo'), (_w_tiro, 'leva o tiro e cai'), (_w_alert, 'se assusta')):
                if w_ is not None: PLANO.append((k, f'animal: {sp} {d_}', 'acao')); b.setdefault('_enc_words', []).append(nrm(b['say'].split()[w_ - starts[k]]))
            acts.append(f"{{ {key}: {json.dumps(sp)}" + (_mvjs if _mvjs else f", at: [X + {num(dxa)}, {num(za)}]") + f", state: {_stjs}, s: {num(sc)}" + ('' if _mvjs else f", flip: {fl}") + f", seed: {j * 3 + 1} }}")
    # CAVALARIA (ordem do Gibson 19/11): soldados A CAVALO cruzando a cena (cavalo 3D com sela + cavaleiro da tropa montado). "cavalaria": {"n": 4, "outfit": "OFF", "dir": 1}
    cav = b.get('cavalaria')
    if cav:
        cav = cav if isinstance(cav, dict) else {'n': int(cav) if not isinstance(cav, bool) else 4}
        _mil = [w_.split(':')[0] for w_ in b.get('who', []) if B.get('outfits', {}).get(w_.split(':')[0], {}).get('rifle') or B.get('outfits', {}).get(w_.split(':')[0], {}).get('hat') in ('shako', 'shako_tall', 'tricorn', 'bicorne', 'kepi', 'pickelhaube', 'quepe', 'colonial', 'stahlhelm', 'adrian', 'brodie')]
        _co = cav.get('outfit') or (_mil[0] if _mil else ((b.get('crowd') or {}).get('outfits') or [None])[0]) or (persons[0][0] if persons else list(B.get('outfits', {'X': 0}))[0])
        _dr = cav.get('dir', 1 if k % 2 == 0 else -1); _wide_c = shot in WIDE
        for i_ in range(int(cav.get('n', 4))):
            zc = (-3.6 if not _wide_c else -2.0) - (i_ % 2) * 2.6 - (i_ // 2) * 0.4; off = i_ * 3.4
            xa, xb = (-15.0 - off, 9.0 - off) if _dr > 0 else (15.0 + off, -9.0 + off)
            acts.append(f"{{ animal: 'horse_sela', at: [X + {num(xa)}, {num(zc)}], move: [[X + {num(xb)}, {num(zc)}], {a}, {bb}, 'lin'], state: 'trot', s: 0.85, seed: {i_ * 5 + 2} }}")
            acts.append(f"{{ outfit: {json.dumps(_co)}, v: {i_ % 4}, at: [X + {num(xa + 0.15 * _dr)}, {num(zc + 0.05)}], move: [[X + {num(xb + 0.15 * _dr)}, {num(zc + 0.05)}], {a}, {bb}, 'lin'], pose: 'stand', acting: 'low', expr: {json.dumps(['stern', 'shout', 'determined', 'stern'][i_ % 4])}, s: 0.86, y: (f) => {num(cav.get('y', 1.62))} + 0.07 * Math.abs(Math.sin(f * 0.55 + {i_})), crop: 0.52, flip: {'false' if _dr > 0 else 'true'}, seed: {i_ + 1} }}")
        PLANO.append((k, f'cavalaria: {int(cav.get("n", 4))} soldados a cavalo ({_co})', 'acao'))
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
    _cidx0 = len(acts)
    if b.get('crowd'):
        c = b['crowd']; cnt = int(c.get('n', 8)); outs_c = c.get('outfits') or [c.get('outfit') or (persons[0][0] if persons else list(B.get('outfits', {'X': 0}))[0])]
        cols = 9 if wide else 5
        if b.get('lados') and (b.get('impact') or b.get('batalha')):   # DOIS EXERCITOS indo um contra o outro (cada lado com a sua farda)
            _L = b['lados']; cnt = max(cnt, 16)
            for i in range(cnt):
                sd_ = -1 if i % 2 == 0 else 1; r_ = (i // 2) % 4; q_ = (i // 8)
                x0 = sd_ * (7.5 + q_ * 1.8 + (r_ % 2) * 0.9); z0 = (1.0 if wide else -2.5) - r_ * 1.9
                out = _L[0] if sd_ < 0 else _L[1]; crowd_pos.append((x0 * 0.45, z0))
                acts.append(f"{{ outfit: {json.dumps(out)}, v: {i % 4}, at: [X + {num(x0)}, {num(z0)}], move: [[X + {num(sd_ * (1.4 + q_ * 1.2))}, {num(z0)}], {a}, Math.round({a} + ({bb} - ({a})) * 0.75), 'lin'], pose: 'run', expr: {json.dumps(['shout', 'angry'][i % 2])}, seed: {i % 5}, flip: {'false' if sd_ < 0 else 'true'} }}")
            cnt = 0
        for i in range(cnt):
            row, col = i // cols, i % cols
            jx = ((i * 37) % 11 - 5) * 0.09; jz = ((i * 53) % 7 - 3) * 0.12
            x0 = (col - (cols - 1) / 2) * (1.9 if wide else 1.7) + (row % 2) * 0.9 + jx + (-6.5 if (b.get('impact') and b.get('emus') and wide) else 0); z0 = (1.2 if wide else -3.0) - row * 2.1 + jz
            out = outs_c[i % len(outs_c)]; ex = c.get('expr', ('neutral' if not c.get('lotado') else ['shout', 'laugh', 'surprised', 'grin', 'shock', 'smile'][(i * 5) % 6]) if not c.get('march') else 'stern'); look = (-0.25, 0.25, 0.0, 0.15)[i % 4]
            crowd_pos.append((x0, z0))
            if c.get('march'):
                acts.append(f"{{ outfit: {json.dumps(out)}, v: {i % 4}, at: [X + {num(x0 - 9)}, {num(z0)}], move: [[X + {num(x0 + 3)}, {num(z0)}], {a}, {bb}, 'lin'], pose: 'march', speed: 0.034, expr: {_exj(ex)}, seed: {i % 4}, look: {look} }}")
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
        _va = vc.get('asset', 'kit/carro_redondo'); _va = 'kit/carro_redondo' if _va == 'vehicles/car' else _va
        if _va == 'kit/carro_redondo' and ANO and ANO < 1935: _va = 'kit/carro_antigo'      # CARRO DA EPOCA
        elif _va == 'kit/carro_redondo' and ANO and ANO < 1975: _va = 'kit/carro_50'
        pr.append(f"{{ asset: {json.dumps(_va)}, at: [X + {num(x0v)}, {num(zv)}], move: [[X + {num(x1v)}, {num(zv)}], {a}, {bb}, 'lin'], s: {num(sv * (0.85 if _va in ('kit/carro_redondo', 'kit/carro_antigo', 'kit/carro_50') else 1))}, bob: 0.03{', ry: ' + ('-1.5708' if _FRENTE.get(_va.split('/')[-1], 1) == 1 else '1.5708') if _va.split('/')[-1] in _FRENTE else ''} }}")
        _tvv = ' ' + re.sub(r'[^a-z ]', ' ', unicodedata.normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode()) + ' '
        _wsv = b['say'].split(); _jvv = next((j_ for j_, w_ in enumerate(_wsv) if re.match(r'(voou|voaram|voando|voa$|decol|levantou|alcou)', nrm(w_))), None)
        _yv = ''
        if _jvv is not None:   # o carro que esta andando DECOLA na palavra e sobe voando (motorista junto)
            _t0v = f"WS({starts[k] + _jvv}) - 8"; _yv = f"3.2 * Math.pow(Math.min(1, Math.max(0, (f - ({_t0v})) / 40)), 1.5)"
            pr[-1] = pr[-1][:-2] + f", y: (f) => DK + {_yv} }}"
            b['_anfx'] = b.get('_anfx', []) + [f"{{ k: 'dust', a: {_t0v}, b: {_t0v} + 30, at: [X, DK + 0.3, {num(zv)}], s: 1.8, follow: -1 }}"]
            KWSFX.append((starts[k] + _jvv, 'whoosh')); b.setdefault('_veic_anim', []).append('o carro decola andando e sobe voando')
        if vc.get('motorista'):   # motorista DENTRO do carro: carta cortada (cabeca e ombros) encostada na janela do lado da camera
            mo_ = vc['motorista'].split(':'); k_ = sv; zd = zv + 0.1 * sv; dxd = -0.45 * sv * dirv   # sentado no banco, dentro da cabine aberta
            acts.append(f"{{ outfit: {json.dumps(mo_[0])}, v: {int(mo_[1]) if len(mo_) > 1 and mo_[1] else 0}, at: [X + {num(x0v + dxd)}, {num(zd)}], move: [[X + {num(x1v + dxd)}, {num(zd)}], {a}, {bb}, 'lin'], pose: 'stand', acting: 'low', expr: {json.dumps(mo_[2] if len(mo_) > 2 else 'smile')}, s: {num(0.86 * k_)}, y: {('(f) => ' + num(-0.42 * k_) + ' + ' + _yv) if _yv else num(-0.42 * k_)}, crop: 0.5, flip: {'false' if dirv > 0 else 'true'} }}")
    # TORCIDA: a arquibancada do estadio ja vem LOTADA (centenas de torcedores pulando, web/sets/more.js); nada a fazer aqui
    # INTERIOR: "interior": "madeira" | "pedra" | "loja"  -> sala com parede a ~5 m, janela, porta, quadros, chao com juntas + moveis
    it = b.get('interior')
    if it:
        _tp = {'madeira': 'wood', 'pedra': 'stone', 'loja': 'shop', 'hospital': 'hospital', 'galpao': 'galpao'}.get(it, 'wood')
        _rr = REGIAO if REGIAO in _REG_N else ['azul', 'verde', 'rosa', 'europa', 'colonial'][sum(map(ord, ID)) % 5]   # sala da regiao (ou uma cor por video): nunca a mesma sala marrom em todos
        # 23/11 (Gibson: "cenario repetindo"): cada VOLTA para dentro de casa e' outra sala (outra cor de parede e outros moveis), nunca a mesma sala o video todo
        if k > 0 and beats[k - 1].get('interior') != it: STATE['sala_n'] = STATE.get('sala_n', -1) + 1
        elif 'sala_n' not in STATE: STATE['sala_n'] = 0
        _sn = STATE['sala_n']
        _cores = list(dict.fromkeys(([_rr] if _rr else []) + ['europa', 'verde', 'azul', 'rosa', 'colonial', 'classico']))
        _rr = _cores[_sn % len(_cores)]
        kit = 'kit/room_hospital' if it == 'hospital' else 'kit/room_galpao' if it == 'galpao' else f'kit/room_{_rr}_{_tp}' if os.path.exists(f'web/assets/library/kit/room_{_rr}_{_tp}.glb') else {'madeira': 'kit/room_wood', 'pedra': 'kit/room_stone', 'loja': 'kit/room_shop'}.get(it, 'kit/room_wood')
        pr.append(f"{{ asset: {json.dumps(kit)}, at: [X, 0], s: 1, drop: false }}")
        for nm_, dx_, z_, s_ in (b.get('moveis') or ([('kit/maca', 4.2, -3.2, 1.4), ('kit/maca', -4.4, -3.0, 1.4), ('kit/maca', 8.0, -2.6, 1.4)] if it == 'hospital' else [] if it == 'loja' else [('mk/Crate_Metal', -6.8, -2.6, 2.4), ('mk/Workbench', 6.8, -2.8, 2.2), ('mk/Crate_Wooden', 7.6, 0.4, 2.0), ('mk/Barrel', -7.6, 0.6, 2.0)] if it == 'galpao' else [[('mk/Bookcase_2', 7.4, -3.4, 2.4), ('mk/Table_Large', -6.6, -1.6, 2.2), ('mk/Chair_1', -4.4, -1.2, 2.2), ('mk/Chest_Wood', 6.9, 0.6, 2.2)],
            [('mk/Cabinet', -7.2, -3.3, 2.3), ('mk/Bed_Twin1', 7.0, -2.4, 2.1), ('mk/Nightstand_Shelf', 4.6, -3.2, 2.2), ('mk/CandleStick_Stand', -4.8, -2.8, 2.2), ('mk/Barrel', -7.4, 0.8, 2.0)],
            [('mk/Workbench_Drawers', 7.0, -3.0, 2.2), ('mk/Shelf_Small_Bottles', -6.8, -3.4, 2.4), ('mk/Stool', 4.8, -1.4, 2.2), ('mk/Crate_Wooden', -7.0, 0.4, 2.0), ('mk/Vase_2', 0.0, -3.6, 2.2)],
            [('mk/Shelf_Arch', 6.8, -3.4, 2.4), ('mk/Bench', -6.4, -2.0, 2.2), ('mk/Table_Large', 6.6, -0.8, 2.0), ('mk/Vase_4', -7.6, 0.6, 2.2), ('mk/CandleStick_Triple', -4.2, -3.0, 2.2)]][STATE.get('sala_n', 0) % 4])):
            pr.append(f"{{ asset: {json.dumps(nm_)}, at: [X + {num(dx_)}, {num(z_)}], s: {num(s_)}, drop: false }}")
    # FACHADA: em plano medio ao ar livre, uma construcao logo atras dos personagens (canal: parede/fachada perto em 85% dos quadros)
    elif not wide_pre and b.get('fachada') is not False and not b.get('veiculo') and not any(str(p_[0]).startswith('kit/marco_') for p_ in (b.get('props') or [])):   # marco no roteiro = ele e' o fundo (sem fachada tapando)
        fb = {'countryside': ['buildings/house_small', 'buildings/house_two'], 'outback': ['buildings/house_small', 'buildings/windmill'], 'street': ['buildings/shop', 'buildings/house_two'], 'medieval': ['buildings/castle_tower', 'buildings/house_small'], 'harbor': ['buildings/shop', 'buildings/lighthouse']}.get(b.get('set', SET))
        if fb: pr.append(f"{{ asset: {json.dumps(fb[k % 2])}, at: [X + {num(4.8 if k % 2 else -4.8)}, -11.0], s: 1.05, ry: {num(-0.35 if k % 2 else 0.35)}, drop: false }}")
    # OBJETOS DA HISTORIA: o que a narracao cita e existe na biblioteca entra em cena sozinho (ate 2 por cena)
    if b.get('objetos') is not False and not b.get('veiculo'):
        tem_ = {str(p_[0]) for p_ in props}; n_auto = 0
        _fam = lambda x_: re.sub(r'_(red|yellow|purple|striped)$', '', str(x_))
        if HEROI and (k == 0 or k == len(beats) - 1) and not wide_pre and not any(_fam(t_) == _fam(HEROI) for t_ in tem_):   # o objeto heroi abre e fecha o video
            props = props + ([[HEROI, 0.0, -3.6, 1.0]] if _EH_VEIC(HEROI) or (_glb_len(HEROI) or 0) > 2.2 else [[HEROI, 0.0, 2.0, 1.15]] if len(b.get('who', [])) == 2 else [[HEROI, (1.7 if k % 2 else -1.7), -0.5, 1.3]])   # objeto GRANDE (carro...) fica atras dos personagens, inteiro no quadro   # entre os dois, a frente (a placa do ano fica atras); tem_.add(HEROI); b.setdefault('_auto_obj', []).append(HEROI)
        for rx_, as_, sc_, big_ in OBJ_DICT:
            if n_auto >= 2 or as_ in tem_ or any(_fam(t_) == _fam(as_) for t_ in tem_) or not re.search(rx_, _say_sp): continue
            if _EH_VEIC(as_) and any(_EH_VEIC(t_) for t_ in tem_): continue   # ja tem um carro na cena: nao poe outro carro por cima (roteiro do Roadster 2026 ganhava o Roadster 2018 junto)
            if (big_ is True and (b.get('interior') or wide_pre)) or (big_ == 'in' and not b.get('interior')): continue
            if as_ == 'buildings/castle_tower' and any(str(t_).startswith('kit/marco_') for t_ in tem_): continue   # marco do roteiro ja e' o castelo/palacio
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
    if b.get('objetos') is not False and not b.get('interior'):   # 23/11: cena com carro andando tambem mostra o lugar citado (cerca, igreja...), mais ao fundo para nao ficar no caminho
        tem2_ = {str(p_[0]) for p_ in props}; sd2_ = 1 if k % 2 else -1
        for rx_, itens_ in LUGARES:
            if not re.search(rx_, _say_sp): continue
            novos_ = [it_ for it_ in itens_ if it_[0] not in tem2_ and not (it_[0] == 'buildings/castle_tower' and any(t_.startswith('kit/marco_') for t_ in tem2_))]   # o marco do roteiro ja e' o castelo: sem torre generica na frente
            if ANO and ANO < 1900: novos_ = [(('buildings/house_two',) + tuple(it_[1:])) if it_[0] == 'buildings/apartment' else it_ for it_ in novos_]   # 19/11 ZERO RESSALVA: cidade antiga nao tem predio de apartamento moderno
            for as_, x_, z_, sc_ in novos_: props = props + [[as_, x_ * sd2_, z_ - (4 if wide_pre or b.get('veiculo') else 0), sc_]]; tem2_.add(as_)
            if novos_: b.setdefault('_auto_obj', []).extend(a_[0] for a_ in novos_); b['fachada'] = False
            break
    if re.search(r'\bnavios?\b|\bbarcos?\b|\bfrota\b|\besquadra\b|\bcaravela', _say_sp) and re.search(r'cheg|desembarc|aport|atracou|atracaram|apareceu|apareceram|surgiu|vinham|navegou|navegaram|zarp|partiu|partiram', _say_sp) and not b.get('interior') and b.get('set', SET) in ('harbor', 'palace') and b.get('objetos') is not False:
        _parte = bool(re.search(r'zarp|partiu|partiram', _say_sp))   # NAVIO EM MOVIMENTO: chegando (do mar para o cais) ou partindo
        props = props + [['ship', -6 if _parte else -42, -24 if _parte else -34, 0.8, {'mover': [-44, -36] if _parte else [-7, -23]}], ['boat', 9 if _parte else 30, -14 if _parte else -22, 1.0, {'mover': [32, -24] if _parte else [8, -13]}]]
        b.setdefault('_auto_obj', []).append('navio em movimento')
    _ppos = [(sl[i], (ZSW[i % len(ZSW)] if shot in WIDE else ZS[i % len(ZS)])) for i in range(len(persons))]
    for p in props:
        asset, dx, z, s = p[0], p[1] if len(p) > 1 else 0, p[2] if len(p) > 2 else 0.5, p[3] if len(p) > 3 else 1.0
        # NADA NA FRENTE DE PERSONAGEM (ordem do Gibson): objeto solto (fogueira, barril, caixa...) que cairia em cima/na frente de alguem vai para o lado livre
        if _ppos and not str(asset).startswith(('kit/room', 'kit/marco', 'kit/rg_', 'buildings/', 'vehicles/', 'kit/ring', 'kit/hospital_ext', 'kit/prison', 'kit/porch', 'mk/')) and float(z) > -2.6 and not (len(p) > 4 and isinstance(p[4], dict) and (p[4].get('carregado') or p[4].get('fixo'))):
            if any(abs(float(dx) - px_) < 1.35 and float(z) > pz_ - 1.6 for px_, pz_ in _ppos):
                _xs = [px_ for px_, pz_ in _ppos]; dx = round((max(_xs) + 2.0) if float(dx) >= sum(_xs) / len(_xs) else (min(_xs) - 2.0), 2); z = min(float(z), min(pz_ for px_, pz_ in _ppos) - 0.4)
        ex = p[4] if len(p) > 4 and isinstance(p[4], dict) else {}
        if asset.startswith(('kit/', 'buildings/')) and 'drop' not in ex: ex = {**ex, 'drop': False}   # peca de cenario nao cai do ceu
        extra = ''.join((f', y: DK + {num(vv)}' if kk == 'y' else f', {kk}: {json.dumps(vv)}') for kk, vv in ex.items() if kk not in ('alto', 'mover', 'carregado') and not (kk == 'y' and ex.get('carregado')))   # 19/11: 'y' do roteiro e' altura acima do chao (DK +) + (f", y: DK + {num(ex.get('y', 0.7))}, move: [[X + {num(dx + mv / 2)}, {num(z)}], {a}, {bb}, 'lin'], drop: false" if ex.get('carregado') and mv else '')   # OBJETO CARREGADO: ["kit/sink", dx_do_personagem + 0.5, z, escala, {"carregado": true}] em cena "track": anda junto na altura das maos + (f", move: [[X + {num(ex['mover'][0])}, {num(ex['mover'][1])}], {a}, Math.round({a} + ({bb} - ({a})) * 0.85), 'sm'], drop: false" if ex.get('mover') else '')
        # VEICULO DE VERDADE (23/11, Gibson: "carro do tamanho correto", "carro voador saindo do chao e voando", "nada de carro parado no ceu")
        if _EH_VEIC(asset) and not ex.get('fixo') and not ex.get('carregado'):
            _L = _glb_len(asset); _alvo = 6.2 if re.search(r'truck|caminh|onibus|bus', str(asset)) else 5.0
            if _ppos and float(z) > -3.0 and not ex.get('perto'): dx, z = (0.0 if shot not in WIDE else dx), -3.4   # carro nunca em cima/no meio dos personagens: estaciona ATRAS deles, inteiro no quadro ("perto": true no prop desliga)
            if _L and float(s) * _L < 0.85 * _alvo: s = round(_alvo / _L, 2)   # carro proporcional aos personagens (~3 m): nunca carrinho de brinquedo
            _tv = ' ' + re.sub(r'[^a-z0-9 ]', ' ', unicodedata.normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode()) + ' '
            _xa = dx - 4.5 if float(dx) <= 0 else dx + 4.5
            _sgF = _FRENTE.get(str(asset).split('/')[-1], 1); _RL = 5.5; _ws0 = b['say'].split()
            _jx = lambda rx_: next((j_ for j_, w_ in enumerate(_ws0) if re.match(rx_, nrm(w_))), None)
            if re.search(r' rampa', _tv) and re.search(r'cabeca para baixo|ponta cabeca| loop|rampa curva|curva gigante', _tv) and 'y' not in ex:   # SOBE A RAMPA CURVA ate ficar de cabeca para baixo (sem cortar: rampa 3D + carro no caminho da curva)
                _j0 = _jx(r'(acelerou|subiu|arrancou|rampa)'); _T0 = (f"WS({starts[k] + _j0}) - 10" if _j0 is not None else f"({a}) + 10"); _rx0 = 0.0
                pr.append(f"{{ asset: 'kit/rampa_curva', at: [X + {num(_rx0)}, {num(z)}], s: 1, drop: false{', ry: 3.1416' if _sgF < 0 else ''} }}")
                _th = f"Math.PI * Math.min(1, Math.max(0, (f - ({_T0}) - 24) / 40))"
                extra += (f", xf: (f) => {{ const u = Math.min(1, Math.max(0, (f - ({_T0})) / 24)); return u < 1 ? X + {num(_rx0 - _sgF * 9)} + {num(_sgF * 9)} * u : X + {num(_rx0)} + {num(_sgF * _RL)} * Math.sin({_th}); }}"
                          f", y: (f) => DK + 0.28 + {num(_RL)} - {num(_RL)} * Math.cos({_th}), rz: (f) => {num(_sgF)} * {_th}, move: [[X + {num(_rx0)}, {num(z)}], {a}, {bb}, 'lin'], align: false")
                b['_anfx'] = b.get('_anfx', []) + [f"{{ k: 'dust', a: {_T0}, b: {_T0} + 30, at: [X + {num(_rx0 - _sgF * 8)}, DK + 0.3, {num(z)}], s: 1.6 }}"]
                if _j0 is not None: KWSFX.append((starts[k] + _j0, 'whoosh'))
                STATE['loop_top'] = (_rx0, float(z), _sgF, k); b['detalhe'] = False
                b.setdefault('_veic_anim', []).append('acelera e sobe a rampa curva gigante ate ficar de cabeca para baixo')
            elif STATE.get('loop_top') and STATE['loop_top'][3] == k - 1 and re.search(r' (soltou|se soltou|voou|girou|gira|pousou|aterriss)', _tv) and 'y' not in ex:   # DO TOPO DA RAMPA: se solta, voa girando (barrel roll) com os propulsores soltando fumaca e pousa numa nuvem branca
                _rx0, _zr, _sgF, _ = STATE.pop('loop_top'); z = _zr
                pr.append(f"{{ asset: 'kit/rampa_curva', at: [X + {num(_rx0)}, {num(_zr)}], s: 1, drop: false{', ry: 3.1416' if _sgF < 0 else ''} }}")
                _j0 = _jx(r'(soltou|voou|girou|gira)'); _T0 = (f"WS({starts[k] + _j0}) - 6" if _j0 is not None else f"({a}) + 8"); _TF = 54; _DX = -_sgF * 10.0
                _u = f"Math.min(1, Math.max(0, (f - ({_T0})) / {_TF}))"
                extra += (f", xf: (f) => X + {num(_rx0)} + {num(_DX)} * {_u}, y: (f) => {{ const u = {_u}; return DK + 0.28 + {num(2 * _RL)} * (1 - u) * (1 - u) + 2.5 * u * (1 - u); }}"
                          f", rz: (f) => {num(_sgF)} * Math.PI * (1 + {_u}), rx: (f) => 2 * Math.PI * {_u} * {_u} * (3 - 2 * {_u}), move: [[X + {num(_rx0)}, {num(_zr)}], {a}, {bb}, 'lin'], align: false")
                _fx_ = []
                for i_ in range(0, _TF, 6):   # fumacinha dos propulsores saindo de baixo do carro durante o voo
                    u_ = i_ / _TF; x_ = _rx0 + _DX * u_; y_ = 0.28 + 2 * _RL * (1 - u_) ** 2 + 2.5 * u_ * (1 - u_)
                    _fx_.append(f"{{ k: 'puff', a: {_T0} + {i_}, b: {_T0} + {i_ + 22}, at: [X + {num(x_)}, DK + {num(max(0.3, y_ - 0.7))}, {num(_zr)}], s: 0.9 }}")
                for i_, dx_ in enumerate((-1.6, 0.0, 1.6, -0.8, 0.8)):   # pouso: nuvem de fumaca branca
                    _fx_.append(f"{{ k: 'puff', a: {_T0} + {_TF - 4 + i_ * 3}, b: {_T0} + {_TF + 40 + i_ * 3}, at: [X + {num(_rx0 + _DX + dx_)}, DK + {num(0.5 + 0.3 * (i_ % 2))}, {num(_zr + 0.4)}], s: 2.2 }}")
                _fx_.append(f"{{ k: 'dust', a: {_T0} + {_TF - 2}, b: {_T0} + {_TF + 30}, at: [X + {num(_rx0 + _DX)}, DK + 0.3, {num(_zr)}], s: 2.0 }}")
                b['_anfx'] = b.get('_anfx', []) + _fx_; b['detalhe'] = False
                if _j0 is not None: KWSFX.append((starts[k] + _j0, 'whoosh'))
                _jp = _jx(r'(pousou|aterriss|desceu)')
                if _jp is not None: KWSFX.append((starts[k] + _jp, 'thump'))
                b.setdefault('_veic_anim', []).append('se solta do topo, voa girando com fumaca dos propulsores e pousa numa nuvem branca')
            elif re.search(r' (espaco|orbita|starman|marte|gravidade zero)|ao redor do sol', _tv) and 'move' not in ex and 'y' not in ex:   # NO ESPACO: flutua, gira devagar e atravessa a cena (nunca parado)
                extra += f", y: (f) => DK + 1.6 + 0.35 * Math.sin((f - ({a})) / 22), spinY: 0.35, move: [[X + {num(dx + 3.5)}, {num(z)}], {a}, {bb}, 'io'], align: false"
                b.setdefault('_veic_anim', []).append('flutua no espaco girando')
            elif re.search(r' (pul\w*|salt\w*|voa|voam|voou|voaram|voando|voar|decol\w*|levantou voo|alcou voo|planou|sobrevo\w*|saiu do chao|subiu aos ceus|desceu|pousou|aterriss\w*)\b', _tv) and 'y' not in ex:
                _ws_ = b['say'].split(); _nv = lambda w_: re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', w_.lower()).encode('ascii', 'ignore').decode())
                _jw = lambda rx_: next((j_ for j_, w_ in enumerate(_ws_) if re.match(rx_, _nv(w_))), None)
                _jp, _jv, _jd = _jw(r'(pul|salt)'), _jw(r'(voa$|voam$|voou|voaram|voando|voar$|decol|levantou|alcou|planou|sobrevo|subiu)'), _jw(r'(desceu|pousou|aterriss)')
                _T = lambda j_: f"WS({starts[k] + j_})"
                _mvx = 3.0 if float(dx) <= 0 else -3.0
                if _jd is not None and _jp is None and (_jv is None or _jv > _jd):   # DESCE/POUSA: comeca no ar e desce ate as rodas tocarem o chao (girando se a frase diz que girou)
                    t0 = _T(_jd) + " - 10"; extra += f", y: (f) => DK + 3.0 * (1 - Math.pow(Math.min(1, Math.max(0, (f - ({t0})) / 34)), 1.5)), spinY: {2.2 if re.search(r' gir', _tv) else 0}"
                    b['_anfx'] = b.get('_anfx', []) + [f"{{ k: 'dust', a: {t0} + 32, b: {t0} + 62, at: [X + {num(dx)}, DK + 0.3, {num(z)}], s: 1.7 }}"]; KWSFX.append((starts[k] + _jd, 'thump'))
                    b.setdefault('_veic_anim', []).append('desce do ar e pousa nas rodas')
                elif _jp is not None and (_jv is None or _jp <= _jv):   # PULOU/SALTOU: arranca, sobe em arco e cai do outro lado (na palavra)
                    t0 = _T(_jp) + " - 14"; extra += f", y: (f) => DK + 3.4 * Math.sin(Math.PI * Math.min(1, Math.max(0, (f - ({t0})) / 44)))"
                    if 'move' not in ex: extra += f", move: [[X + {num(dx + 2 * _mvx)}, {num(z)}], {t0} - 16, {t0} + 50, 'io'], align: false" + ('' if 'ry' in ex else f", ry: {_ryv(asset, 1 if float(dx) <= 0 else -1)}")
                    b['_anfx'] = b.get('_anfx', []) + [f"{{ k: 'dust', a: {t0}, b: {t0} + 26, at: [X + {num(dx)}, DK + 0.3, {num(z)}], s: 1.5 }}", f"{{ k: 'dust', a: {t0} + 42, b: {t0} + 72, at: [X + {num(dx + 2 * _mvx)}, DK + 0.3, {num(z)}], s: 1.5 }}"]; KWSFX.append((starts[k] + _jp, 'whoosh'))
                    b.setdefault('_veic_anim', []).append('pula em arco e cai do outro lado')
                else:   # VOOU/DECOLOU: comeca no chao, decola com poeira na palavra e sobe voando para o lado
                    t0 = (_T(_jv) + " - 8") if _jv is not None else f"({a}) + 14"
                    extra += f", y: (f) => DK + 3.0 * Math.pow(Math.min(1, Math.max(0, (f - ({t0})) / 46)), 1.6) + (f > ({t0}) + 20 ? 0.12 * Math.sin((f - ({t0})) / 6) : 0)"
                    if 'move' not in ex: extra += f", move: [[X + {num(dx + _mvx)}, {num(z - 1.0)}], {t0} + 10, {bb}, 'in'], align: false" + ('' if 'ry' in ex else f", ry: {_ryv(asset, 1 if float(dx) <= 0 else -1)}")
                    b['_anfx'] = b.get('_anfx', []) + [f"{{ k: 'dust', a: {t0} - 2, b: {t0} + 30, at: [X + {num(dx)}, DK + 0.3, {num(z)}], s: 1.6 }}", f"{{ k: 'puff', a: {t0}, b: {t0} + 24, at: [X + {num(dx)}, DK + 0.4, {num(z)}], s: 1.3 }}"]
                    b['_anfx'] += [f"{{ k: 'puff', a: {t0} + {i_}, b: {t0} + {i_ + 22}, at: [X + {num(dx + _mvx * min(1, max(0, (i_ - 10) / 40)) ** 2)}, DK + {num(max(0.3, 3.0 * min(1, i_ / 46) ** 1.6 - 0.6))}, {num(z - min(1, i_ / 46))}], s: 0.8 }}" for i_ in range(4, 50, 6)]   # fumacinha dos propulsores debaixo do carro enquanto sobe
                    if _jv is not None: KWSFX.append((starts[k] + _jv, 'whoosh'))
                    b.setdefault('_veic_anim', []).append('decola do chao com poeira e sobe voando')
            elif re.search(r' (dirig\w*|acelerou|arrancou|andou|andava|correu|corria|passou|desfil\w*|estrada|avenida|percorr\w*|viajou|rodou|chegou|lancad\w*|lancou|pilot\w*)\b', _tv) and 'move' not in ex:   # ANDANDO: atravessa a cena rodando
                extra += f", move: [[X + {num(dx + (6.0 if float(dx) <= 0 else -6.0))}, {num(z)}], {a}, {bb}, 'io'], align: false, bob: 0.03" + ('' if 'ry' in ex else f", ry: {_ryv(asset, 1 if float(dx) <= 0 else -1)}")
                b.setdefault('_veic_anim', []).append('anda pela cena')
        pr.append(f"{{ asset: {json.dumps(asset)}, at: [X + {num(dx - (mv / 2 if ex.get('carregado') else 0))}, {num(z)}], s: {num(s)}{extra} }}")
    # textos / efeitos
    fx = list(b.pop('_anfx', []))
    if HEROI and not wide and b.get('heroi_brilho') is not False:   # OBJETO HEROI EM DESTAQUE: brilho de estrelinhas quando entra em cena (o olho vai direto nele)
        for p in props:
            if re.sub(r'_(red|yellow|purple|striped)$', '', str(p[0])) == re.sub(r'_(red|yellow|purple|striped)$', '', HEROI):
                fx.append(f"{{ k: 'stars', a: {a} + 6, b: {a} + 40, at: [X + {num(p[1] if len(p) > 1 else 0)}, DK + 1.6, {num((p[2] if len(p) > 2 else 0.5) + 0.5)}], s: 0.8 }}"); break
    for dx_, dz_, t_ in locals().get('DUST', []): fx.append(f"{{ k: 'dust', a: {a} + {t_}, b: {a} + {t_ + 30}, at: [X + {num(dx_)}, DK + 0.4, {num(dz_)}], s: 0.85 }}")
    # MAPA DIDATICO: "mapa": "AUSTRALIA" (ou sozinho, na 1a vez que o texto cita um pais/cidade conhecido). Corta para o mapa por ~1,8 s.
    _mp = b.get('mapa')
    if _mp is None and B.get('mapas') is not False and not STATE.get('mapa'):
        _m = re.search(r'\b(Austrália|Brasil|França|Inglaterra|Japão|Alemanha|Rússia|China|Índia|Egito|Itália|Espanha|Portugal|Estados Unidos|México|Grécia|Turquia|Áustria|Holanda|Suécia|Noruega|Canadá|Argentina|Peru|Roma|Paris|Londres|Berlim|Moscou|Tóquio|Lisboa|Madri|Viena|Nova York|África|Europa|Ásia|Amazônia|Sibéria|Antártida)\b', b['say'])
        if _m: _mp = _m.group(1).upper(); _mw = len(b['say'][:_m.start()].split()); b['mapa'] = _mp
    if _mp:
        STATE['mapa'] = True; b['passaros'] = False; _mw = int(b.get('mapa_at', locals().get('_mw', 0)))
        fx.append(f"{{ k: 'map', a: WS({starts[k] + _mw}, -2), b: Math.min({bb}, WS({starts[k] + _mw}, -2) + {int(b.get('mapa_dur', 54))}), text: {json.dumps(str(_mp), ensure_ascii=False)}, geo: {json.dumps(_MAPAS.geo(str(_mp)))} }}")
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
        if b.get('_enc') and kind in ('puff', 'dust', 'splash'): continue   # cena de processo: a fumaca sai do objeto (encenacao), nao uma nuvem na frente do personagem
        if kind == 'burst': fx.append(f"{{ k: 'burst', a: {a} + {at}, at: [X + {num(sl[0] if n else 0)}, DK + 1.8, 3.2], s: 1.2 }}")
        elif kind in ('dust', 'puff'): fx.append(f"{{ k: {json.dumps(kind)}, a: {a} + {at}, b: {a} + {at + 26}, at: [X + 0.9, DK + 0.12, 1.0], s: 0.75 }}")   # nos pes, nao na frente do rosto
        elif kind in ('stars', 'splash', 'ring', 'creak'): fx.append(f"{{ k: {json.dumps(kind)}, a: {a} + {at}, b: {a} + {at + 26}, at: [X, DK + 0.5, 1.2], s: 1.1 }}")
    _armed = any(B.get('outfits', {}).get(o_, {}).get('rifle') for o_ in ([p_[0] for p_ in persons] + list((b.get('crowd') or {}).get('outfits') or [(b.get('crowd') or {}).get('outfit')])) if o_)
    if b.get('impact') and b.get('tiros') is not False and (any(SHOOT.match(nrm(w_)) for w_ in b['say'].split()) or _armed or b.get('batalha')) and crowd_pos:   # fuzilaria cartunesca: clarões piscando pela tropa + som de tiro
        _off = 46 if b.get('caminhoes') else 8; _dur = int(len(b['say'].split()) / 2.7 * 30); _nf = max(8, min(40, (_dur - _off - 12) // 5))   # tiros durante a tomada INTEIRA (depois de a tropa subir nos caminhoes)
        for i in range(_nf):
            px, pz = crowd_pos[(i * 5 + 2) % len(crowd_pos)]; t0 = _off + i * 5 + (i * 7) % 4
            fx.append(f"{{ k: 'flash', a: {a} + {t0}, b: {a} + {t0 + 8}, at: [X + {num(px + 0.75)}, DK - 1.05 + {num(b.get('caminhao_y', 0.95) if pz < -5 and b.get('caminhoes') else 0)}, {num(pz + 0.4)}], s: {2.5 if wide else 2.0} }}")   # a carta do efeito ancora pela base: y baixo poe o clarao na altura do fuzil
        b.setdefault('sfx', []); b['sfx'] += [f'gun@{_off + i * 5 + (i * 7) % 4}' for i in range(_nf)]
        # NOS TIROS, SOLDADOS CAEM NO CHAO (ordem do Gibson): alguns da tropa caem sentados/deitados ao longo da batalha, cada um num tiro
        _cid = [i_ for i_ in range(_cidx0, len(acts)) if 'outfit' in acts[i_] or acts[i_].startswith('pp(')]
        _semq = b.get('sem_mortos') or re.search(r'ninguem (acertou|morreu|se feriu|ficou ferido)|nenhum (morto|ferido)|para o alto|ninguem foi atingido|sem mortos', re.sub(r'[^a-z0-9 ]', '', __import__('unicodedata').normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode()))   # 19/11 ZERO RESSALVA: 'tiros para o alto, ninguem acertou ninguem' nao derruba soldado
        for q_, i_ in enumerate([] if _semq else _cid[2::3][:5]):
            t_ = _off + 14 + q_ * 17
            acts[i_] = f"Object.assign({acts[i_]}, {{ poses: [[{a} + {t_}, {bb}, 'fall']] }})"
            fx.append(f"{{ k: 'dust', a: {a} + {t_}, b: {a} + {t_ + 20}, at: [X + {num(crowd_pos[min(i_ - _cidx0, len(crowd_pos) - 1)][0])}, DK + 0.1, {num(crowd_pos[min(i_ - _cidx0, len(crowd_pos) - 1)][1] + 0.3)}], s: 0.6 }}")
        if _cid: PLANO.append((k, f'tiros: {min(5, len(_cid[2::3]))} soldados caem no chao', 'acao'))
    # animacao nas palavras-chave: golpe de camera + efeito no instante da palavra
    kfx = 0
    if b.get('kw') is not False:
        _ngK = _neg_idx(b['say'])
        for j, w in enumerate(b['say'].split()):
            nw = nrm(w)
            if j in _ngK or j in _idiom_idx(b['say']): continue   # "ninguem deu um tiro" / "a noticia correu": sem efeito de acao
            for rx, kind, kick in KW:
                if rx.match(nw) and kfx < 7 and not (b.get('_enc') and kind in ('puff', 'dust', 'splash')):
                    kfx += 1; wi = starts[k] + j; PLANO.append((k, w.strip('.,!?"'), kind)); KWSFX.append((wi, 'cannon' if re.match(r'canh|explo|bomb', nw) else {'burst': 'gun', 'ring': 'sting', 'dust': 'thump', 'puff': 'thump', 'stars': 'ding'}.get(kind, 'tick')))   # SOM na mesma palavra do efeito
                    px, pz = (crowd_pos[(j * 5) % len(crowd_pos)] if crowd_pos else (sl[0] if n else 0.0, 1.5))
                    _rif = [i_ for i_, pe_ in enumerate(persons) if pe_[3] == 'rifle' or B.get('outfits', {}).get(pe_[0], {}).get('rifle') or PROFISSOES.get(str(B.get('outfits', {}).get(pe_[0], {}).get('profissao', '')).lower(), {}).get('rifle')]
                    if kind == 'burst' and _rif and not re.match(r'canh|explo|bomb|artilh', nw) and not crowd_pos:   # TIRO: o clarao sai do cano da arma de quem atira
                        ri_ = _rif[0]; _sd = 1 if sl[ri_] <= 0 else -1; b.setdefault('_shots', []).append(f"WS({wi})")
                        if shot == 'track' or mv: fx.append(f"{{ k: 'flash', a: WS({wi}), b: WS({wi}) + 8, follow: {ri_}, dx: 1.7, at: [0, DK - 0.55, 0], s: 1.6 }}"); fx.append(f"{{ k: 'puff', a: WS({wi}) + 3, b: WS({wi}) + 20, follow: {ri_}, dx: 1.9, at: [0, DK + 1.9, 0], s: 0.5 }}")   # correndo e atirando: o clarao acompanha o cano
                        else: fx.append(f"{{ k: 'flash', a: WS({wi}), b: WS({wi}) + 8, at: [X + {num(sl[ri_] + 1.55 * _sd)}, DK - 0.55, {num(ZS[ri_ % len(ZS)] + 0.4)}], s: 1.6 }}"); fx.append(f"{{ k: 'puff', a: WS({wi}) + 3, b: WS({wi}) + 24, at: [X + {num(sl[ri_] + 1.8 * _sd)}, DK + 1.9, {num(ZS[ri_ % len(ZS)] + 0.4)}], s: 0.5 }}")
                    elif kind == 'burst': fx.append(f"{{ k: 'burst', a: WS({wi}), b: WS({wi}) + 22, at: [X + {num(px)}, DK + 1.8, {num(pz + 1.5)}], s: {1.7 if wide else 1.2} }}")
                    elif kind in ('dust', 'puff'): fx.append(f"{{ k: {json.dumps(kind)}, a: WS({wi}), b: WS({wi}) + 28, at: [X + {num(px + 0.9)}, DK + 0.12, {num(pz + 0.2)}], s: {1.3 if wide else 0.7} }}")   # poeira/fumaca NOS PES, de lado (nunca uma nuvem na frente do rosto)
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
        if b.get('interacao'): pair = {'empurrar': ('shove', 'stagger'), 'discutir': ('lunge', 'lunge'), 'cochichar': ('lean', 'lean'), 'entregar': ('step', 'nod'), 'susto': ('lean', 'recoil'), 'reverencia': ('nod', 'bow'), 'pular': ('hop', 'hop'), 'abracar': ('hug', 'hug'), 'tremer': ('shiver', 'shiver'), 'pedir': ('lean', 'nod'), 'apertar': ('step', 'step')}.get(b['interacao'], ('lean', 'nod')); nome = b['interacao']
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
    # ===== ENCENACAO DA NARRACAO (ordem do Gibson 19/11: "pega frase por frase e aplica no video: ele pegou o produto, jogou, virou pasta -> tem que mostrar") =====
    # cada verbo de acao da frase vira: gesto do personagem NA PALAVRA + objeto do processo + efeito + som. Tabela ENC (topo do arquivo). "encena": false no beat desliga.
    if b.get('encena') is not False and persons and not b.get('veiculo'):
        _ws = b['say'].split(); _gst = {}; _st = STATE.setdefault('enc', {})
        _alvo = next(((p_[1], p_[2], str(p_[0])) for p_ in (b.get('props') or []) if re.search(r'stove|fire|campfire|panela|kettle|bancada|well|sink|wash_basin|bathtub', str(p_[0]))), None)
        _side = (1 if sl[0] <= 0 else -1) if len(persons) > 1 else 1
        _z0 = ZS[0]; _hx = sl[0] + _side * 1.25
        _tx, _tz = (_alvo[0], _alvo[1]) if _alvo else (sl[0] + _side * 2.3, _z0 + 0.9)
        _feitos = set(); _encs = []; _mesmos = []
        _negi = _neg_idx(b['say'])
        # v10 TIMELINE EXPLICITA: se o beat define "acoes": [{"palavra": "...", "quem": 0, "alvo": 1, "tipo": "golpe|empurra|atira|tomba|pula|vence|grita|..."}], executa com 100% de precisao sem depender de regex!
        _EXP_MAP = {'golpe': 'punch', 'empurra': 'push', 'grita': 'up', 'vence': 'up', 'x_ri': 'up', 'pega': 'lift', 'chega': 'point', 'fala': 'point', 'olha': 'point', 'pensa': 'think', 'perde': 'facepalm', 'rende': 'up', 'ajoelha': 'plead', 'mistura': 'stir', 'cai': 'throw', 'constroi': 'hammer', 'escreve': 'write', 'atira': None, 'tomba': None, 'corre': None, 'pula': None, 'desaba': None, 'dorme': None, 'senta': None}
        _exp_targets = {}
        if b.get('acoes'):
            for _ea in b['acoes']:
                _pw = nrm(str(_ea.get('palavra', '')))
                _tp = _ea.get('tipo', 'fala')
                _jmatch = next((jj_ for jj_, ww_ in enumerate(_ws) if nrm(ww_) == _pw or (_pw and _pw in nrm(ww_))), 0)
                _wi = starts[k] + _jmatch
                if b.get('interacao') == 'apertar' and _tp == 'fala' and re.search(r'apert|maos|paz|tratado|acordo', _pw): continue
                _g = _ea.get('gesto', _EXP_MAP.get(_tp, 'point'))
                _encs.append((_wi, _g, _tp, _jmatch))
                _exp_targets[(_wi, _tp)] = (_ea.get('quem', 0), _ea.get('alvo', 1 if len(persons) > 1 else 0))
        else:
          for j_, w_ in enumerate(_ws):
              nw_ = nrm(w_); wi_ = starts[k] + j_
              if j_ in _negi: b.setdefault('_enc_words', []).append(nw_); continue   # acao NEGADA na frase: nao encena (e nao conta como falta)
              if j_ in _idiom_idx(b['say']): b.setdefault('_enc_words', []).append(nw_); continue   # EXPRESSAO: "o panico tomou", "a noticia correu", "o preco caiu"
              for rx_, gest_, tipo_ in ENC:
                  if not re.match(rx_, nw_): continue
                  if tipo_ in _feitos and any(t__ == tipo_ and (j_ - jj__) < 4 for _, _, t__, jj__ in _encs): _mesmos.append((tipo_, nw_)); break
                  _feitos.add(tipo_); _encs.append((wi_, gest_, tipo_, j_)); break
        _resto = lambda j0: nrm(' '.join(_ws[j0:j0 + 7]))
        if _st.get('dorme') and not any(t_ in ('dorme', 'x_acorda') for _, _, t_, _ in _encs):   # SONO CONTINUA (cochilou -> "no sonho..." -> acordou): segue deitado dormindo
            _gst.setdefault(('poses', 0), []).append(f"[{a}, {bb}, 'sleep']")
        if any(t_ == 'x_acorda' for _, _, t_, _ in _encs): _st['dorme'] = False
        _sy_ = nrm(b['say']); _mat_ok = bool(_alvo) or any(re.search(r_, _sy_) for r_, a_ in ENC_MAT + ENC_RES) or bool(_st.get('mat'))
        _ok = {'cai': _mat_ok, 'vira': _mat_ok, 'calor': _mat_ok or bool(re.search(r'fogao|forno|panela|ferv|aquec|esquent|caldeir', _sy_)), 'golpe': bool(re.search(r'ringue|luta|boxe|lutador|briga|soco|golpe|enfrent', _sy_)), 'bola': bool(re.search(r'futebol|\bcopa\b|\bbola\b|\bgol\b|estadio|chut', _sy_)), 'raspa': bool(re.search(r'cabeca|cabelo|careca|maquina|barba', _sy_)), 'x_come': not (b.get('animals') and re.search(r'porco|vaca|cavalo|cachorro|gato|galinha|ganso|emu|ovelha|cabra|bicho|animal|rato|passaro', _sy_))}
        _encs = [e_ for e_ in _encs if _ok.get(e_[2], True)]
        b.setdefault('_enc_words', []).extend(w__ for t__, w__ in _mesmos if _ok.get(t__, True) and t__ in {e_[2] for e_ in _encs})   # "o imperio caiu", "abriram fogo", "a luta virou bagunca" NAO sao processo fisico
        _punches = []
        for n_e, (wi_, gest_, tipo_, j_) in enumerate(_encs[:8]):
            b.setdefault('_enc_words', []).append(nrm(_ws[j_]))
            _nxt = f"WS({_encs[n_e + 1][0]}) - 5" if n_e + 1 < len(_encs[:8]) else f"WS({wi_}) + 46"
            _ate = f"Math.max(WS({wi_}) + 14, {_nxt})" if n_e + 1 < len(_encs[:8]) else _nxt   # v9: janela minima garantida para cada acao aparecer clara na tela
            if tipo_ == 'corta' and re.search(r'dedo|bisturi|faca|tesoura|navalha|semachucou|mao|nariz|orelha|espada', _sy_): gest_ = 'reach'
            if tipo_ == 'danca' and re.search(_DANCA_OUTRO, _sy_): gest_ = None
            if tipo_ == 'pega' and (persons[0][3] == 'rifle' or B.get('outfits', {}).get(persons[0][0], {}).get('rifle')): b.setdefault('_shots', []).append(f"WS({wi_}) + 4")
            if tipo_ in ('golpe', 'atira', 'empurra', 'quebra', 'desaba', 'tomba', 'x_bate'): _punches.append(f"{{ f: WS({wi_}), amt: {0.16 if tipo_ in ('golpe', 'atira', 'desaba') else 0.11}, dur: 20 }}")
            if gest_ and not (persons[0][3] == 'rifle' and tipo_ in ('pega', 'golpe')):
                _qm_ = _exp_targets.get((wi_, tipo_), (0, 1))[0]; _gst.setdefault(_qm_, []).append(f"[WS({wi_}) - 8, {_ate}, '{gest_}']")   # v9: antecipacao de 8 frames para o pico bater NA palavra
                if len(persons) >= 2 and tipo_ in ('vence', 'x_ri', 'grita', 'danca', 'rende', 'x_aplaude'):
                    _gst.setdefault(1, []).append(f"[WS({wi_}) - 6, {_ate}, '{gest_}']")   # v9: acoes coletivas (riram, comemoraram) animam os dois personagens
            mat_ = next((a_ for rx2_, a_ in ENC_MAT if re.search(rx2_, _resto(j_) + ' ' + nrm(b['say']))), None)
            if tipo_ == 'mistura':
                if not _alvo: _tx, _tz = sl[0] + _side * 1.2, _z0 + 0.3; pr.append(f"{{ asset: 'kit/panela', a: WS({wi_}) - 8, b: {bb}, at: [X + {num(_tx)}, {num(_tz)}], s: 0.55, drop: false }}"); _alvo = (_tx, _tz, 'kit/panela')
                elif re.search('stove|bancada', _alvo[2]): pr.append(f"{{ asset: 'kit/panela', a: WS({wi_}) - 8, b: {bb}, at: [X + {num(_tx)}, {num(_tz)}], y: DK + 0.92, s: 0.5, drop: false }}")   # panela EM CIMA do fogao/mesa
                if re.search(r'enxofre|polvora|\bpo\b|farinha|acucar|\bsal\b', nrm(b['say'])): pr.append(f"{{ asset: 'kit/enxofre', a: WS({wi_}) - 8, b: {bb}, at: [X + {num(_tx + _side * 1.4)}, {num(_tz)}], s: 0.6, drop: false }}")
                for q_ in range(3): fx.append(f"{{ k: 'puff', a: WS({wi_}) + {q_ * 12}, b: WS({wi_}) + {q_ * 12 + 22}, at: [X + {num(_tx)}, DK + 1.6, {num(_tz + 0.1)}], s: 0.45 }}")
                _st['mat'] = mat_ or 'kit/gosma'; KWSFX.append((wi_, 'tick'))
            elif tipo_ == 'cai':
                m_ = mat_ or _st.get('mat') or 'kit/gosma'; ty_ = 0.95 if _alvo and re.search('stove|kettle|bancada', _alvo[2]) else 0.05
                pr.append(f"{{ asset: {json.dumps(m_)}, a: Math.max({a} + 4, WS({wi_}) - 30), b: {bb}, at: [X + {num(_hx)}, {num(_z0 + 0.5)}], move: [[X + {num(_tx)}, {num(_tz + 0.1)}], WS({wi_}), WS({wi_}) + 16, 'lin'], align: false, y: {grav_js(f'WS({wi_})', 16 / 30, 1.5, ty_)}, s: 0.55, drop: false }}")   # cai pela gravidade
                fx.append(f"{{ k: 'splash', a: WS({wi_}) + 15, b: WS({wi_}) + 40, at: [X + {num(_tx)}, DK + {num(ty_ + 0.3)}, {num(_tz + 0.4)}], s: 0.9 }}"); KWSFX.append((wi_, 'thump'))
                _st['mat'] = m_; _st['mat_em'] = (_tx, _tz + 0.1, ty_, k)
            elif tipo_ == 'calor':
                if not _alvo and re.search(r'fogao|forno', nrm(b['say'])): pr.append(f"{{ asset: 'kit/stove', a: WS({wi_}) - 10, b: {bb}, at: [X + {num(_tx)}, {num(_tz)}], s: 1.0, drop: false }}"); _alvo = (_tx, _tz, 'kit/stove')
                elif not _alvo: pr.append(f"{{ asset: 'kit/campfire', a: WS({wi_}) - 10, b: {bb}, at: [X + {num(_tx)}, {num(_tz)}], s: 0.8, drop: false }}"); _alvo = (_tx, _tz, 'kit/campfire')
                for q_ in range(4): fx.append(f"{{ k: 'puff', a: WS({wi_}) + {q_ * 10}, b: WS({wi_}) + {q_ * 10 + 24}, at: [X + {num(_tx)}, DK + 1.6, {num(_tz + 0.2)}], s: 0.7 }}")
                KWSFX.append((wi_, 'creak'))
            elif tipo_ == 'vira':
                res_ = next((a_ for rx2_, a_ in ENC_RES if re.search(rx2_, _resto(j_) + ' ' + nrm(b['say']))), None)
                if not res_ and not _st.get('mat'): continue   # "a luta virou bagunca" nao e' processo: so' transforma quando ha material/produto
                res_ = res_ or (HEROI if HEROI and HEROI != (_alvo or (0, 0, ''))[2] else None) or 'kit/borracha'
                px_, pz_, py_ = (_st['mat_em'][0], _st['mat_em'][1], _st['mat_em'][2]) if _st.get('mat_em') and _st['mat_em'][3] == k and not _alvo else (_tx, _tz + 0.1, 0.95 if re.search('stove|kettle|bancada', _alvo[2]) else 0.05) if _alvo else (_tx, _tz + 0.1, 0.75 if _alvo and re.search('stove|kettle|bancada', _alvo[2]) else 0.05)
                if _st.get('mat') and not any(_st['mat'] in p__ for p__ in pr): pr.append(f"{{ asset: {json.dumps(_st['mat'])}, b: WS({wi_}) - 1, at: [X + {num(px_)}, {num(pz_)}], y: DK + {num(py_)}, s: 0.55, drop: false }}")
                else: pr[:] = [p__.replace(f"a: WS(", f"b: WS({wi_}) - 1, a: WS(", 1).replace(f"b: {bb},", "", 1) if _st.get('mat') and json.dumps(_st['mat']) in p__ else p__ for p__ in pr]
                rx_, rz_ = px_ * 0.6 + sl[0] * 0.4, max(pz_, _z0) + 0.9   # o RESULTADO sobe do processo e vem para a frente, entre o personagem e o objeto, na altura do peito (destaque)
                pr.append(f"{{ asset: {json.dumps(res_)}, a: WS({wi_}), at: [X + {num(px_)}, {num(pz_)}], move: [[X + {num(rx_)}, {num(rz_)}], WS({wi_}) + 4, WS({wi_}) + 22, 'lin'], align: false, y: (f) => DK + {num(py_)} + {num(1.5 - py_)} * Math.min(1, Math.max(0, (f - WS({wi_})) / 18)) + 0.08 * Math.sin(f * 0.15), spinY: 0.9, s: (f) => {num(1.25)} * Math.min(1, 0.2 + (f - WS({wi_})) / 10) * (1 + 0.15 * Math.max(0, 1 - (f - WS({wi_})) / 20)), drop: false }}")
                if HEROI and re.sub(r'_(red|yellow|purple|striped)$', '', res_) == re.sub(r'_(red|yellow|purple|striped)$', '', HEROI): b['_det_heroi'] = True   # o produto do processo surge em destaque na frente da camera = close do objeto heroi
                fx.append(f"{{ k: 'ring', a: WS({wi_}), b: WS({wi_}) + 30, at: [X + {num(px_)}, DK + {num(py_ + 0.6)}, {num(pz_ + 0.4)}], s: 1.2 }}"); fx.append(f"{{ k: 'stars', a: WS({wi_}) + 4, b: WS({wi_}) + 40, at: [X + {num(px_)}, DK + {num(py_ + 1.0)}, {num(pz_ + 0.4)}], s: 1.0 }}"); KWSFX.append((wi_, 'ding'))
                _st['mat'] = None; _st['mat_em'] = None
            elif tipo_ == 'constroi':
                obj_ = next((a_ for rx2_, a_ in ENC_RES if re.search(rx2_, nrm(b['say']))), None)
                if obj_: pr.append(f"{{ asset: {json.dumps(obj_)}, a: WS({wi_}), at: [X + {num(_tx)}, {num(_tz)}], s: (f) => Math.min(1, 0.15 + (f - WS({wi_})) / 50), drop: false }}")
                for q_ in range(3): fx.append(f"{{ k: 'dust', a: WS({wi_}) + {q_ * 14}, b: WS({wi_}) + {q_ * 14 + 20}, at: [X + {num(_tx)}, DK + 0.4, {num(_tz + 0.5)}], s: 0.7 }}")
                KWSFX.append((wi_, 'thump'))
            elif tipo_ == 'examina':
                ins_ = 'kit/microscopio' if re.search(r'microsc|celula|bacter|germe|lamina', nrm(b['say'])) else 'kit/balanca' if re.search(r'pes|balanca', nrm(b['say'])) else 'kit/lupa'
                pr.append(f"{{ asset: {json.dumps(ins_)}, a: Math.max({a} + 4, WS({wi_}) - 30), b: {bb}, at: [X + {num(_hx + _side * (0.3 if ins_ == 'kit/lupa' else 0.15))}, {num(_z0 + (0.7 if ins_ == 'kit/lupa' else 0.35))}], y: DK + {1.9 if ins_ == 'kit/lupa' else 0}, s: {0.4 if ins_ == 'kit/lupa' else 1.05}, drop: false }}"); KWSFX.append((wi_, 'tick'))   # lupa NA MAO, na altura do rosto
            elif tipo_ == 'quimico':
                pr.append(f"{{ asset: 'kit/frasco', a: Math.max({a} + 4, WS({wi_}) - 30), b: {bb}, at: [X + {num(_hx)}, {num(_z0 + 0.6)}], s: 0.6, drop: false }}"); pr.append(f"{{ asset: 'kit/tubos', a: Math.max({a} + 4, WS({wi_}) - 30), b: {bb}, at: [X + {num(_hx + _side * 1.1)}, {num(_z0 + 0.3)}], s: 0.6, drop: false }}")
                fx.append(f"{{ k: 'puff', a: WS({wi_}) + 6, b: WS({wi_}) + 30, at: [X + {num(_hx)}, DK + 1.3, {num(_z0 + 0.8)}], s: 0.6 }}"); KWSFX.append((wi_, 'tick'))
            elif tipo_ == 'golpe':
                fx.append(f"{{ k: 'burst', a: WS({wi_}), b: WS({wi_}) + 20, at: [X + {num(sl[1] if len(sl) > 1 else sl[0] + _side * 1.6)}, DK + 2.1, {num(_z0 + 0.5)}], s: 1.15 }}"); KWSFX.append((wi_, 'thump'))
                if len(persons) >= 2:
                    _d0 = 1 if sl[1] > sl[0] else -1
                    _gst.setdefault(('inters', 0), []).append(f"{{ k: 'shove', a: WS({wi_}) - 8, b: WS({wi_}) + 18, dir: {_d0}, n: 1, ph: 0 }}")
                    _gst.setdefault(('inters', 1), []).append(f"{{ k: 'stagger', a: WS({wi_}) - 4, b: WS({wi_}) + 26, dir: {_d0}, n: 1, ph: 0 }}")
            elif tipo_ == 'corta' and re.search(r'dedo|bisturi|faca|tesoura|navalha|semachucou|mao|nariz|orelha|espada', _sy_):   # corte pequeno (dedo, bisturi): susto + estrelinhas na mao, sem machado nem toras
                fx.append(f"{{ k: 'stars', a: WS({wi_}) + 2, b: WS({wi_}) + 26, at: [X + {num(sl[0] + 0.4)}, DK + 1.4, {num(_z0 + 0.3)}], s: 0.5 }}"); KWSFX.append((wi_, 'sting'))
            elif tipo_ == 'corta':
                if 'kit/logs' not in ' '.join(pr): pr.append(f"{{ asset: 'kit/logs', a: Math.max({a} + 4, WS({wi_}) - 30), b: {bb}, at: [X + {num(_tx)}, {num(_tz)}], s: 0.8, drop: false }}")
                for q_ in range(3): fx.append(f"{{ k: 'dust', a: WS({wi_}) + {q_ * 9}, b: WS({wi_}) + {q_ * 9 + 16}, at: [X + {num(_tx)}, DK + 0.2, {num(_tz + 0.4)}], s: 0.5 }}")
                KWSFX.append((wi_, 'thump'))
            elif tipo_ == 'voto':
                pr.append(f"{{ asset: 'kit/ballot_box', a: Math.max({a} + 4, WS({wi_}) - 30), b: {bb}, at: [X + {num(_hx + _side * 0.4)}, {num(_z0 + 0.6)}], s: 0.7, drop: false }}"); KWSFX.append((wi_, 'tick'))
            elif tipo_ == 'quebra':
                fx.append(f"{{ k: 'burst', a: WS({wi_}) + 2, b: WS({wi_}) + 20, at: [X + {num(_tx)}, DK + 1.6, {num(_tz + 0.3)}], s: 1.1 }}"); fx.append(f"{{ k: 'stars', a: WS({wi_}) + 4, b: WS({wi_}) + 30, at: [X + {num(_tx)}, DK + 1.8, {num(_tz + 0.3)}], s: 0.8 }}"); KWSFX.append((wi_, 'thump')); KICKS.append(f"{{ f: WS({wi_}) + 2, a: 0.04 }}")
            elif tipo_ == 'desaba':
                for q_ in range(4): fx.append(f"{{ k: 'dust', a: WS({wi_}) + {q_ * 6}, b: WS({wi_}) + {q_ * 6 + 30}, at: [X + {num(-3 + q_ * 2)}, DK + 0.3, -4], s: 1.6 }}")
                KWSFX.append((wi_, 'cannon')); KICKS.append(f"{{ f: WS({wi_}) + 3, a: 0.06 }}")
            elif tipo_ == 'pensa':
                fx.append(f"{{ k: 'ring', a: WS({wi_}) + 6, b: WS({wi_}) + 34, at: [X + {num(sl[0])}, DK + 3.6, {num(_z0 + 0.2)}], s: 0.7 }}"); KWSFX.append((wi_, 'ding'))
            elif tipo_ == 'protesto':
                fx.append(f"{{ k: 'stars', a: WS({wi_}), b: WS({wi_}) + 26, at: [X + {num(sl[0])}, DK + 3.2, {num(_z0)}], s: 0.6 }}"); KWSFX.append((wi_, 'sting'))
            elif tipo_ == 'sai' and acts and acts[0].startswith(('pp(', 'Object.assign(pp(')):
                _gst.setdefault('sai', []).append(f"move: [[X + {num(sl[0] - _side * 9)}, {num(_z0 - 0.6)}], WS({wi_}) + 2, WS({wi_}) + 70, 'lin'], walk: 'stroll'")
            elif tipo_ == 'morre':
                if re.search(r'porco|cavalo|vaca|cachorro|\bcao\b|animal|bicho|galinha|emu|urso|lobo|ovelha|cabra|boi|ganso', _sy_): pass   # animal morrendo: o bloco dos animais cuida
                elif re.search(r'(morreu|faleceu)\s+(em|no ano)\s+(mil|\d)', unicodedata.normalize('NFKD', b['say'].lower()).encode('ascii', 'ignore').decode()):   # morte anos depois: tumulo com cruz e flores
                    pr.append(f"{{ asset: 'kit/lapide', a: {a}, b: {bb}, at: [X + {num(sl[0] + _side * 1.3)}, -1.2], s: 1.0, ry: 0.2, drop: false }}")   # ao lado e atras do personagem (na frente tapava a cena); KWSFX.append((wi_, 'sting'))
                else:
                    _gst.setdefault(('poses', 0), []).append(f"[WS({wi_}) + 2, {bb}, 'fall']"); fx.append(f"{{ k: 'dust', a: WS({wi_}) + 4, b: WS({wi_}) + 30, at: [X + {num(sl[0] + 0.6)}, DK + 0.1, {num(_z0 + 0.3)}], s: 0.8 }}"); KWSFX.append((wi_, 'thump'))
            elif tipo_ in ('tomba', 'dorme', 'senta', 'ajoelha'):
                _who_ = _exp_targets[(wi_, tipo_)][0] if (wi_, tipo_) in _exp_targets else (1 if (tipo_ == 'tomba' and len(persons) > 1 and re.search(r'derrub|nocaute|golpe|soco|socou|empurr|bateu|rival|outro|inimigo', _sy_) and not re.search(r'\bele foi ao chao', _sy_)) else 0)
                _ini_ = f"WS({wi_}) + 2" if tipo_ == 'tomba' else f"Math.max({a} + 6, WS({wi_}) - 36)"   # dormir/sentar comeca antes da palavra (palavra no fim da frase sumia)
                _gst.setdefault(('poses', _who_), []).append(f"[{_ini_}, {bb}, '{ {'tomba': 'fall', 'dorme': 'sleep', 'senta': 'sit', 'ajoelha': 'kneel'}[tipo_] }']")
                if tipo_ == 'dorme' and _who_ == 0: _st['dorme'] = True
                if tipo_ == 'ajoelha' and (b.get('crowd') or re.search(r'(ajoelharam|imploravam|suplicavam|ajoelhados|todos|elas|eles|mulheres|homens|maes|soldados|pessoas)', _sy_)): _gst['todos_pose'] = f"[{_ini_}, {bb}, 'kneel']"   # plural: todo mundo de joelhos   # continua dormindo nas proximas frases ate 'acordou'
                if tipo_ == 'tomba': fx.append(f"{{ k: 'dust', a: WS({wi_}) + 4, b: WS({wi_}) + 30, at: [X + {num(sl[_who_] + 0.6)}, DK + 0.1, {num(_z0 + 0.3)}], s: 0.8 }}"); KWSFX.append((wi_, 'thump'))
            elif tipo_ == 'raspa':
                if HEROI and 'clip' in HEROI: pr.append(f"{{ asset: {json.dumps(HEROI)}, a: WS({wi_}) - 4, b: {bb}, at: [X + {num(_hx)}, {num(_z0 + 0.4)}], y: DK + 2.4, s: 0.45, drop: false }}")
                for q_ in range(3): fx.append(f"{{ k: 'puff', a: WS({wi_}) + {q_ * 10}, b: WS({wi_}) + {q_ * 10 + 18}, at: [X + {num(sl[-1])}, DK + 2.9, {num(_z0 + 0.2)}], s: 0.35 }}")
                KWSFX.append((wi_, 'creak'))
            elif tipo_ == 'golpe' or tipo_ == 'espeta':
                fx.append(f"{{ k: 'burst', a: WS({wi_}) + 4, b: WS({wi_}) + 22, at: [X + {num(sl[-1] if len(sl) > 1 else sl[0] + _side * 1.6)}, DK + 2.0, {num(_z0 + 0.5)}], s: {0.9 if tipo_ == 'golpe' else 0.6} }}"); KWSFX.append((wi_, 'thump'))
            elif tipo_ == 'bola':
                pr.append(f"{{ asset: 'kit/ball', a: WS({wi_}) - 4, b: {bb}, at: [X + {num(_hx)}, {num(_z0 + 0.6)}], move: [[X + {num(_hx + _side * 6)}, {num(_z0 - 3)}], WS({wi_}) + 2, WS({wi_}) + 22, 'lin'], align: false, y: {grav_js(f'WS({wi_}) + 2', 20 / 30, 0.2, 0.2)}, spinY: 3, s: 0.35, drop: false }}")   # bola em parabola (gravidade); KWSFX.append((wi_, 'thump'))
            elif tipo_ == 'negocio':
                pr.append(f"{{ asset: 'kit/coin', a: WS({wi_}) - 2, b: WS({wi_}) + 50, at: [X + {num(_hx)}, {num(_z0 + 0.6)}], y: (f) => DK + 1.5 + 0.25 * Math.sin(f * 0.2), spinY: 2, s: 0.35, drop: false }}"); KWSFX.append((wi_, 'ding'))
            elif tipo_ == 'tira':
                if re.search(r'foto|selfie|fotograf|film|grav|celular', _sy_): pr.append(f"{{ asset: 'kit/phone', a: WS({wi_}) - 4, b: {bb}, at: [X + {num(_hx)}, {num(_z0 + 0.5)}], y: DK + 2.0, s: 0.35, drop: false }}"); fx.append(f"{{ k: 'flash', a: WS({wi_}) + 6, b: WS({wi_}) + 12, at: [X + {num(_hx)}, DK + 0.8, {num(_z0 + 0.7)}], s: 1.2 }}")
                KWSFX.append((wi_, 'tick'))
            elif tipo_ == 'rende':
                fx.append(f"{{ k: 'stars', a: WS({wi_}) + 4, b: WS({wi_}) + 34, at: [X + {num(sl[0])}, DK + 3.0, {num(_z0)}], s: 0.6 }}"); KWSFX.append((wi_, 'sting'))
            elif tipo_ == 'voa':
                for q_ in range(2): fx.append(f"{{ k: 'dust', a: WS({wi_}) + {q_ * 8}, b: WS({wi_}) + {q_ * 8 + 24}, at: [X + {num(_tx)}, DK + 0.2, {num(_tz)}], s: 0.9 }}")
                KWSFX.append((wi_, 'sting'))
            elif tipo_ == 'cava':
                for q_ in range(3): fx.append(f"{{ k: 'dust', a: WS({wi_}) + {q_ * 9}, b: WS({wi_}) + {q_ * 9 + 18}, at: [X + {num(_hx)}, DK + 0.15, {num(_z0 + 0.6)}], s: 0.6 }}")
                KWSFX.append((wi_, 'thump'))
            elif tipo_ in ('vence', 'grita'):
                fx.append(f"{{ k: 'stars', a: WS({wi_}) + 2, b: WS({wi_}) + 30, at: [X + {num(sl[0])}, DK + 3.2, {num(_z0)}], s: 0.7 }}"); KWSFX.append((wi_, 'ding' if tipo_ == 'vence' else 'sting'))
            elif tipo_ == 'toca':
                fx.append(f"{{ k: 'ring', a: WS({wi_}), b: WS({wi_}) + 30, at: [X, DK + 3.4, -1], s: 1.0 }}"); KWSFX.append((wi_, 'ding'))
            elif tipo_ == 'queima':
                pr.append(f"{{ asset: 'kit/fire', a: WS({wi_}) - 2, b: {bb}, at: [X + {num(_tx)}, {num(_tz)}], s: 0.8, drop: false }}")
                for q_ in range(3): fx.append(f"{{ k: 'puff', a: WS({wi_}) + {q_ * 10}, b: WS({wi_}) + {q_ * 10 + 26}, at: [X + {num(_tx)}, DK + 2.0, {num(_tz)}], s: 0.7 }}")
                KWSFX.append((wi_, 'creak'))
            elif tipo_ == 'danca' and re.search(_DANCA_OUTRO, _sy_):   # quem danca e' a coisa (atomos/cobras no sonho): brilhos rodando no ar em volta do objeto da cena
                for q_ in range(3): fx.append(f"{{ k: 'stars', a: WS({wi_}) + {q_ * 10}, b: WS({wi_}) + {q_ * 10 + 34}, at: [X + {num(_tx + (q_ - 1) * 0.7)}, DK + {1.4 + 0.4 * q_}, {num(_tz)}], s: 0.7 }}")
                KWSFX.append((wi_, 'ding'))
            elif tipo_ == 'paga':   # dinheiro/pagar/vender: moedas na mao estendida + brilho
                pr.append(f"{{ asset: 'kit/coin', a: Math.max({a} + 4, WS({wi_}) - 20), b: {bb}, at: [X + {num(_hx + _side * 0.25)}, {num(_z0 + 0.5)}], y: DK + 1.25, s: 0.32, drop: false }}"); KWSFX.append((wi_, 'ding'))
            elif tipo_ == 'chega' and j_ <= 4 and not re.search(r'(entrou|entraram)(para|na|em|no)(a)?(historia|guerra|moda|panico|acordo|crise|falencia|vigor|campo)|apareceu(na|no)(tv|televisao|jornal|foto)', _sy_) and acts and not b.get('_chega') and not (shot == 'track' or mv) and 'move:' not in acts[0] and acts[0].startswith(('pp(', 'Object.assign(pp(')):   # chegou/apareceu: entra andando pela lateral e para no lugar
                _gst.setdefault('sai', []).append(f"at: [X + {num(sl[0] + _side * 6)}, {num(_z0 - 0.8)}], move: [[X + {num(sl[0])}, {num(_z0)}], Math.max({a}, WS({wi_}) - 30), WS({wi_}) + 20, 'lin'], walk: 'stroll'")
            elif tipo_ == 'atira':
                if not (persons[0][3] == 'rifle' or B.get('outfits', {}).get(persons[0][0], {}).get('rifle')) and acts: acts[0] = f"_MA({acts[0]}, {{ over: {{ rifle: true }} }})"
                b.setdefault('_shots', []).append(f"WS({wi_})")
                fx.append(f"{{ k: 'flash', a: WS({wi_}), b: WS({wi_}) + 10, at: [X + {num(sl[0] + 1.55 * _side)}, DK - 0.55, {num(_z0 + 0.4)}], s: 1.6 }}"); KWSFX.append((wi_, 'gun'))
            elif tipo_ == 'corre' and acts and len(persons) >= 1 and not (shot == 'track' or mv):
                _gst.setdefault('sai', []).insert(0, f"move: [[X + {num(sl[0] - _side * 11)}, {num(_z0 - 0.4)}], WS({wi_}) + 2, WS({wi_}) + 40, 'lin'], pose: 'run'")
                fx.append(f"{{ k: 'dust', a: WS({wi_}) + 2, b: WS({wi_}) + 24, at: [X + {num(sl[0])}, DK + 0.1, {num(_z0 + 0.3)}], s: 0.7 }}"); KWSFX.append((wi_, 'thump'))
            elif tipo_ == 'pula':   # PULO COM GRAVIDADE: sobe 1,2 m e volta acelerando (g = 9,8 m/s2 na escala do boneco), 2 pulos seguidos
                _gst.setdefault('y', []).append(f"(f) => {{ const t = (f - WS({wi_})) / 30; if (t < 0 || t > {num(2 * GPULO_T)}) return 0; const u = t % {num(GPULO_T)}; return Math.max(0, {num(GPULO_V0)} * u - 0.5 * {num(GRAV)} * u * u); }}")
                fx.append(f"{{ k: 'dust', a: WS({wi_}) + {int(GPULO_T * 30)}, b: WS({wi_}) + {int(GPULO_T * 30) + 14}, at: [X + {num(sl[0])}, DK + 0.05, {num(_z0 + 0.3)}], s: 0.5 }}"); KWSFX.append((wi_, 'thump'))
                if re.search(r'todomundo|todos|multidao|populac|bilh|milh|pessoas|gente|juntos', _sy_):   # "todo mundo pula": a multidao inteira pula junto (cada um com um atraso pequeno)
                    for i_ in range(len(persons), len(acts)):
                        if 'outfit' in acts[i_] or acts[i_].startswith('pp('):
                            d_ = (i_ * 3) % 7; acts[i_] = f"Object.assign({acts[i_]}, {{ y: (f) => {{ const t = (f - WS({wi_}) - {d_}) / 30; if (t < 0 || t > {num(2 * GPULO_T)}) return 0; const u = t % {num(GPULO_T)}; return Math.max(0, {num(GPULO_V0)} * u - 0.5 * {num(GRAV)} * u * u); }} }})" 
            elif tipo_ == 'acena': KWSFX.append((wi_, 'tick'))
            elif tipo_ == 'empurra':
                KWSFX.append((wi_, 'thump'))
                if len(persons) >= 2 and len(acts) >= 2:
                    _d0 = 1 if sl[1] > sl[0] else -1
                    _gst.setdefault(('inters', 0), []).append(f"{{ k: 'shove', a: WS({wi_}) - 10, b: WS({wi_}) + 24, dir: {_d0}, n: 1, ph: 0 }}")
                    _gst.setdefault(('inters', 1), []).append(f"{{ k: 'stagger', a: WS({wi_}) - 6, b: WS({wi_}) + 32, dir: {_d0}, n: 1, ph: 0 }}")
                    fx.append(f"{{ k: 'puff', a: WS({wi_}), b: WS({wi_}) + 20, at: [X + {num((sl[0] + sl[1]) / 2)}, DK + 1.8, {num(_z0 + 0.4)}], s: 0.9 }}")
            elif tipo_.startswith('x_'):   # ACOES GERAIS: gesto + objeto/efeito + som na palavra
                _X = {'x_bebe': ('tick', None, 'kit/kettle' if 0 else None), 'x_come': ('tick', 'stars', None), 'x_chora': ('sting', 'splash', None), 'x_canta': ('ding', 'ring', None), 'x_le': ('tick', None, 'kit/scroll'),
                      'x_fone': ('ding', 'ring', 'kit/phone'), 'x_lava': ('creak', 'splash', 'kit/wash_basin'), 'x_beija': ('ding', 'stars', None), 'x_planta': ('thump', 'dust', None), 'x_pesca': ('tick', 'splash', None),
                      'x_costura': ('tick', None, None), 'x_pinta': ('tick', 'stars', None), 'x_bate': ('thump', 'burst', None), 'x_procura': ('tick', None, 'kit/lupa'), 'x_vigia': ('tick', None, None), 'x_saluda': ('sting', None, None),
                      'x_reza': ('ding', 'stars', None), 'x_aplaude': ('ding', 'stars', None), 'x_abraca': ('ding', 'stars', None), 'x_acorda': ('ding', 'stars', None), 'x_espera': ('tick', None, None), 'x_treme': ('creak', None, None),
                      'x_tosse': ('thump', 'puff', None), 'x_nada': ('creak', 'splash', None), 'x_ri': ('laughs', 'stars', None), 'x_abre': ('creak', None, None), 'x_solta': ('ding', 'stars', None), 'x_entrega': ('tick', None, None), 'x_discute': ('sting', None, None), 'x_aperta': ('ding', 'stars', None), 'x_desce': ('thump', 'dust', None), 'x_defende': ('thump', 'ring', None), 'x_dirige': ('tick', 'dust', None)}.get(tipo_, ('tick', None, None))
                if _X[2] and _X[2] not in ' '.join(pr): pr.append(f"{{ asset: {json.dumps(_X[2])}, a: WS({wi_}) - 4, b: {bb}, at: [X + {num(_hx)}, {num(_z0 + 0.6)}], y: DK + {1.9 if _X[2] in ('kit/phone', 'kit/scroll', 'kit/lupa') else 0}, s: {0.35 if _X[2] in ('kit/phone', 'kit/scroll', 'kit/lupa') else 0.6}, drop: false }}")
                if _X[1]: fx.append(f"{{ k: {json.dumps(_X[1])}, a: WS({wi_}) + 3, b: WS({wi_}) + 30, at: [X + {num(sl[0] + (0.6 if _X[1] in ('splash', 'puff') else 0))}, DK + {2.6 if _X[1] in ('stars', 'ring') else 1.6}, {num(_z0 + 0.4)}], s: 0.6 }}")
                if tipo_ == 'x_treme' and acts: _gst.setdefault('inter', []).append(f"inter: {{ k: 'shiver', a: WS({wi_}), b: WS({wi_}) + 50, dir: 1, n: 3, ph: 0 }}")
                if tipo_ in ('x_beija', 'x_abraca') and len(persons) > 1 and not b.get('interacao'): b['interacao'] = 'abracar'
                if tipo_ == 'x_discute' and len(persons) > 1 and not b.get('interacao'): b['interacao'] = 'discutir'
                if tipo_ == 'x_aperta' and len(persons) > 1 and not b.get('interacao'): b['interacao'] = 'apertar'   # apertaram as maos: aperto de mao de verdade
                if tipo_ == 'x_acorda': _gst.setdefault(('poses', 0), []).append(f"[{a}, WS({wi_}), 'sleep']")
                KWSFX.append((wi_, _X[0]))
            elif tipo_ == 'brilha':   # o objeto da cena (heroi ou o que estiver em props) brilha na palavra
                _po = next((p_ for p_ in (b.get('props') or []) if not str(p_[0]).startswith(('kit/room', 'kit/marco', 'buildings/', 'mk/'))), None)
                _bx, _bz = (float(_po[1]), float(_po[2])) if _po else (_tx, _tz)
                for q_ in range(3): fx.append(f"{{ k: {json.dumps(['ring', 'stars', 'ring'][q_])}, a: WS({wi_}) + {q_ * 10}, b: WS({wi_}) + {q_ * 10 + 30}, at: [X + {num(_bx)}, DK + 1.4, {num(_bz + 0.4)}], s: {num(1.1 - q_ * 0.2)} }}")
                KWSFX.append((wi_, 'ding'))
            PLANO.append((k, f'encena: {tipo_}' + (f' ({gest_})' if gest_ else '') + f' @{j_}', 'acao'))   # @j = palavra exata executada (a folha 3 mostra ESTA palavra)
        if _encs or (persons and persons[0][3]): b['_acao'] = b.get('_acao') or ('atira' if persons[0][3] == 'rifle' else 'encena')   # quem faz o processo / segura o objeto NAO esta parado
        for _w in (0, 1):
            if _gst.get(_w) and len(acts) > _w and len(persons) > _w: acts[_w] = f"_MA({acts[_w]}, {{ gests: [{', '.join(_gst[_w])}] }})"
            if _gst.get(('inters', _w)) and len(acts) > _w and len(persons) > _w: acts[_w] = f"_MA({acts[_w]}, {{ inters: [{', '.join(_gst[('inters', _w)])}] }})"
            if _gst.get(('poses', _w)) and len(acts) > _w and len(persons) > _w: acts[_w] = f"_MA({acts[_w]}, {{ poses: [{', '.join(_gst[('poses', _w)])}] }})"
        if _gst.get('sai') and acts: acts[0] = f"_MA({acts[0]}, {{ {_gst['sai'][0]} }})"
        if _gst.get('y') and acts: acts[0] = f"_MA({acts[0]}, {{ yFns: [{', '.join(_gst['y'])}] }})"
        if _gst.get('inter') and acts: acts[0] = f"_MA({acts[0]}, {{ {_gst['inter'][0]} }})"
        if _punches: opts.append(f"punches: [{', '.join(_punches)}]")
        if _gst.get('todos_pose'):
            for _w in range(len(acts)):
                if acts[_w].startswith(('pp(', 'Object.assign(pp(')) and 'poses:' not in acts[_w]: acts[_w] = f"Object.assign({acts[_w]}, {{ poses: [{_gst['todos_pose']}] }})"
        if _encs and not wide: opts.append('vary: false')   # a acao acontece numa tomada so' (sem sub-corte no meio do processo)
    # MODO DE ACAO no build: soldados voando na explosao, navios chegando, aperto de mao, voltando para casa
    _wsay = b['say'].split(); _wi_of = lambda rx_: next((starts[k] + j_ for j_, w_ in enumerate(_wsay) if re.search(rx_, nrm(w_))), starts[k])
    if b.get('voando'):
        _wb = _wi_of(r'explod|bomba|voaram|ares|explos'); _ls = b.get('lados') or [persons[0][0] if persons else list(B.get('outfits'))[0]]
        fx.append(f"{{ k: 'burst', a: WS({_wb}), b: WS({_wb}) + 26, at: [X, DK + 1.4, -1.0], s: 2.4 }}"); KWSFX.append((_wb, 'cannon')); KICKS.append(f"{{ f: WS({_wb}), a: 0.08 }}")
        for q_ in range(int(b['voando'])):
            sx_ = (-1) ** q_ * (1.2 + q_ * 1.1); t0_ = q_ * 3
            acts.append(f"{{ outfit: {json.dumps(_ls[q_ % len(_ls)])}, v: {q_ % 4}, at: [X + {num(sx_ * 0.3)}, -1.2], move: [[X + {num(sx_ * 2.6)}, {num(-1.6 - q_)}], WS({_wb}) + {t0_}, WS({_wb}) + {t0_ + int(GVOO_T * 30)}, 'lin'], a: WS({_wb}) + {t0_}, b: WS({_wb}) + {t0_ + int(GVOO_T * 30) + 4}, pose: 'stand', acting: 'low', expr: 'shock', y: (f) => {{ const t = Math.max(0, Math.min({GVOO_T:.2f}, (f - WS({_wb}) - {t0_}) / 30)); return {GVOO_T * GRAV / 2:.2f} * t - {GRAV / 2:.2f} * t * t; }}, roll: (f) => (f - WS({_wb})) * {num(0.32 * (-1) ** q_)}, shadow: false, seed: {q_} }}")
        PLANO.append((k, f"explosao: {int(b['voando'])} soldados voando girando (GRAVIDADE: {GVOO_T} s no ar, sobem {GVOO_T * GVOO_T * GRAV / 8:.1f} m e caem acelerando)", 'acao'))
    if b.get('desembarque'):
        _wb = _wi_of(r'chegar|navio|desembarc|atrac|aport')
        for q_, (x0_, z0_) in enumerate(((-34, -9), (-46, -12))):
            pr.append(f"{{ asset: 'ship', at: [X + {num(x0_)}, {num(z0_)}], move: [[X + {num(-7 - q_ * 9)}, {num(z0_)}], {a}, WS({_wb}) + 30, 'lin'], s: 1.3, drop: false }}")
        PLANO.append((k, 'desembarque: navios chegando e tropa descendo na praia', 'acao'))
    if b.get('interacao') == 'apertar' and len(acts) >= 2 and len(persons) >= 2:
        _wb = _wi_of(r'apert|maos|pazes|paz|cumpriment|tratado|acordo')
        _w_after = next((starts[k] + j_ for j_, w_ in enumerate(_wsay) if starts[k] + j_ > _wb + 1 and any(re.match(rx_, nrm(w_)) for rx_, g_, _ in ENC if g_)), None)
        _end_ap = f"WS({_w_after}) - 6" if _w_after is not None else bb
        for i_ in (0, 1): acts[i_] = f"_MA({acts[i_]}, {{ gests: [[WS({_wb}) - 6, {_end_ap}, 'reach']] }})"
        fx.append(f"{{ k: 'stars', a: WS({_wb}) + 6, b: WS({_wb}) + 40, at: [X, DK + 2.0, {num(ZS[0] + 0.3)}], s: 0.9 }}"); KWSFX.append((_wb, 'ding'))
        PLANO.append((k, 'aperto de mao', 'acao'))
    if b.get('para_casa') and acts and not wide:
        _wb = _wi_of(r'voltou|voltaram|foram|foi|retorn')
        for i_ in range(min(2, len(persons), len(acts))):
            _d = -1 if sl[i_] <= 0 else 1; _z = ZS[i_ % len(ZS)]
            acts[i_] = f"Object.assign({acts[i_]}, {{ move: [[X + {num(sl[i_] + _d * 9)}, {num(_z - 0.6)}], WS({_wb}) + 4, WS({_wb}) + 70, 'lin'], walk: 'stroll' }})"
        PLANO.append((k, 'voltam para casa (saem andando)', 'acao'))
    if wide: opts.append("hero: { hero: 'none', wide: true }"); opts.append('vary: false'); opts.append('nocut: true')   # plano aberto = UMA tomada continua (camera abrindo/girando), sem sub-corte
    elif b.get('veiculo'): opts.append("hero: { hero: 'none' }")   # motorista fica atras do carro de proposito
    elif persons: opts.append("hero: { hero: 'any', frame: 'medium', minH: 0.07, main: %d }" % len(persons))
    if b.get('trans'): opts.append(f"trans: {json.dumps(b['trans'])}")
    elif k > 0: opts.append("trans: 'dissolve'")   # canal: quase sem corte seco; troca de cena por fusao curta
    if b.get('vary') is False and not wide: opts.append('vary: false')
    mt_ = b.get('montado')
    if mt_ and acts and persons:
        _dr = int(mt_.get('dir', 1 if k % 2 == 0 else -1)); _zm = float(mt_.get('z', 0.6)); _x0m, _x1m = (-8.5, 8.5) if _dr > 0 else (8.5, -8.5)
        _arm = bool(re.search(r'atir|espingard|rifle|fuzil|arma|mosquet|pistol|dispar|carabin', nrm(b['say'])))
        acts[0] = f"_MA({acts[0]}, {{ at: [X + {num(_x0m + 0.15 * _dr)}, {num(_zm + 0.05)}], move: [[X + {num(_x1m + 0.15 * _dr)}, {num(_zm + 0.05)}], {a}, {bb}, 'lin'], moves: null, y: (f) => 1.84 + 0.08 * Math.abs(Math.sin(f * 0.55)), crop: 0.52, flip: {'false' if _dr > 0 else 'true'}, pose: 'stand', walk: 'stand', sideWalk: false, nocol: true{', over: { rifle: true }' if _arm else ''} }})"
        _sc = {'elephant': 0.7, 'camel': 0.9, 'donkey': 0.9}.get(mt_.get('animal'), 0.95)
        acts.append(f"{{ animal: {json.dumps(mt_.get('animal', 'horse_sela'))}, at: [X + {num(_x0m)}, {num(_zm)}], move: [[X + {num(_x1m)}, {num(_zm)}], {a}, {bb}, 'lin'], state: 'trot', s: {num(_sc)}, seed: 7 }}")
        b['_galope'] = True; PLANO.append((k, f"montado: {persons[0][0]} galopando em cima do animal ({mt_.get('animal', 'horse_sela')}) atravessando a cena" + (' com a arma na mao' if _arm else ''), 'acao'))
    opts.append(f"actors: [{', '.join(acts)}]")
    if pr:   # 19/11 ZERO RESSALVA: o mesmo objeto grande (balao, foguete, navio) nao aparece duplicado na cena (roteiro + automatico)
        _vis = set(); _pr2 = []
        for _p in pr:
            _m = re.search(r"asset: [\"']kit/(balloon\w*|rocket\w*|booster\w*|falcon\w*|navio\w*|roadster\w*|cybertruck\w*|aviao\w*|jato\w*|biplano\w*|helicopter\w*)", _p)
            if _m and _m.group(1) in _vis: continue
            if _m: _vis.add(_m.group(1))
            _pr2.append(_p)
        pr = _pr2
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
    if b.get('montado') and persons and not b.get('cam_livre'):   # a camera acompanha o cavaleiro de lado (cavalo e cavaleiro inteiros)
        _dr = int(b['montado'].get('dir', 1 if k % 2 == 0 else -1)); _zm = float(b['montado'].get('z', 0.6)); _x0m, _x1m = (-8.5, 8.5) if _dr > 0 else (8.5, -8.5)
        cam = (f"cam: [{{ f: {a}, at: [X + {num(_x0m + 2.2 * _dr)}, DK + 2.1, {num(_zm)}], d: 12.5, az: {10 * _dr}, el: 6, fov: 42 }}, "
               f"{{ f: {bb}, at: [X + {num(_x1m - 2.2 * _dr)}, DK + 2.1, {num(_zm)}], d: 11.5, az: {-8 * _dr}, el: 7, fov: 42, ease: 'lin' }}]")
        call = f"{{ ...{call}, {cam}, nocut: true }}"
        call = call.replace("k: 'flash',", f"k: 'flash', follow: 0, dx: 1.5,")   # o clarao do tiro sai da arma do cavaleiro (acompanha o galope)
    if b.get('veiculo') and not b.get('cam_livre'):   # a camera acompanha o veiculo de lado, mostrando ele inteiro
        vc = b['veiculo']; x0v, x1v, zv = vc.get('de', -9), vc.get('para', 9), vc.get('z', 0.6); dd = vc.get('dist', 14.5)
        cam = (f"cam: [{{ f: {a}, at: [X + {num(x0v)}, DK + 1.9, {num(zv)}], d: {num(dd)}, az: {12 if x1v >= x0v else -12}, el: 7, fov: 40 }}, "
               f"{{ f: {bb}, at: [X + {num(x1v)}, DK + 1.9, {num(zv)}], d: {num(dd * 0.9)}, az: {-10 if x1v >= x0v else 10}, el: 8, fov: 40, ease: 'lin' }}]")
        call = f"{{ ...{call}, {cam}, nocut: true }}"
    # DETALHE DE OBJETO (canal: 5-15% do video e' close no objeto da historia): no meio da cena a camera desliza ate o objeto ou a placa e volta
    _cands = [p_ for p_ in props if not str(p_[0]).startswith(('kit/room', 'kit/porch', 'kit/grave', 'kit/cross', 'kit/tulip_bed', 'buildings/', 'vehicles/', 'ship', 'nature/picket_fence', 'nature/haybale', 'nature/scarecrow', 'nature/bush', 'nature/rocks', 'nature/tree'))]
    _cands = [p_ for p_ in _cands if (float(p_[2]) if len(p_) > 2 else 0.5) > (-8.0 if (_glb_len(str(p_[0])) or 0) > 2.2 else -3.0) and ((str(p_[0]) == str(HEROI) and str(HEROI) in ('kit/logs', 'kit/campfire', 'kit/fire')) or not str(p_[0]) in ('kit/campfire', 'kit/fire', 'kit/logs', 'kit/volcano', 'kit/tower', 'kit/tower_catch', 'kit/booster_air', 'kit/prison', 'kit/white_house', 'kit/mountain_bunker', 'kit/miners', 'kit/falcon_air', 'kit/falcon9_land', 'kit/b2_air', 'kit/balloon_air', 'kit/helicopter_air', 'kit/iceberg'))]   # heroi pequeno (toras, fogueira) pode ter close; close de detalhe so em objeto pequeno e perto (objeto gigante ao fundo = tela vazia)
    _fam2 = lambda x_: re.sub(r'_(red|yellow|purple|striped)$', '', str(x_))
    _obj = next((p_ for p_ in _cands if HEROI and _fam2(p_[0]) == _fam2(HEROI)), None); _eh = _obj is not None
    _obj = _obj or next(iter(_cands), None)
    _placa = bool(b.get('text')) and "board:" in call
    if (b.get('detalhe') is not False and not (b.get('interior') and b.get('detalhe') is not True) and not wide and not b.get('impact') and not b.get('veiculo') and not (shot == 'track' or mv) and (k > 0 or _eh) and k < len(beats) - 1
            and not b.get('_shots') and (_obj or _placa) and len(b['say'].split()) >= (8 if _eh else 11) and (STATE.get('detalhes', 0) < int(B.get('max_detalhes', 3)) or (_eh and not STATE.get('det_heroi')))):
        if _eh: STATE['det_heroi'] = STATE.get('det_heroi', 0) + 1; b['_det_heroi'] = True
        Fq = lambda q: f"Math.round({a} + ({bb} + 1 - ({a})) * {q})"
        if _obj:
            ox, oz, os_ = (float(_obj[1]) if len(_obj) > 1 else 0.0), (float(_obj[2]) if len(_obj) > 2 else 0.5), (float(_obj[3]) if len(_obj) > 3 else 1.0)
            oy_ = float(_obj[4].get('alto', 0.75)) if len(_obj) > 4 and isinstance(_obj[4], dict) else (1.62 if 'tulip' in str(_obj[0]) else 1.2 if str(_obj[0]) in ('kit/cake_table', 'kit/throne') else 0.75)   # altura do centro do objeto ("alto" no 5o campo do prop)
            k0 = (ox, oy_ * os_, oz, (5.6 if oy_ > 1.5 else 5.0) if oy_ > 1 else 4.2, 14 if ox < 0 else -14, 6 if oy_ > 1 else 10, 44); k1 = (ox, oy_ * os_, oz, (4.7 if oy_ > 1.5 else 4.2) if oy_ > 1 else 3.4, 8 if ox < 0 else -8, 5 if oy_ > 1 else 9, 44)
            _Lo = (_glb_len(str(_obj[0])) or 0) * os_   # 23/11: objeto grande (carro, carroca, canhao...) inteiro no close: a distancia cresce com o tamanho dele (quadro vertical: cabe ~0,46 x distancia de largura)
            if _Lo > 1.6: k0 = (ox, max(0.75, oy_) * os_, oz, round(_Lo * 2.4 + 1.2, 2), k0[4], 7, 44); k1 = (ox, max(0.75, oy_) * os_, oz, round(_Lo * 2.15 + 1.0, 2), k1[4], 6, 44)
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
    if 'emus' in _sp: _b['emus'] = {'n': 6, 'mode': 'run' if re.search(r'corr|fug|dispar|espalh', _nz0(_b['say'])) else 'stand'}; _sp.remove('emus')
    if _sp: _b['animals'] = [[sp_, (1.9, -2.3, 2.9)[n_], (0.8, 1.1, 1.5)[n_]] for n_, sp_ in enumerate(_sp[:3])]
for _b in beats:   # DECOLAGEM A RISCA: "decolou/lancado/subiu ao ceu" com foguete/balao em cena -> troca pela versao JA NO AR (com chamas/subindo)
    if re.search(r'decol|levantou voo|lancad|lancou|subiu ao ceu|subiu para o ceu|foi para o espaco|rumo ao espaco', _nz0(_b['say'])):
        for _p in _b.get('props', []):
            _air = {'kit/rocket': 'kit/falcon_air', 'kit/balloon': 'kit/balloon_air', 'kit/tower': 'kit/booster_air'}.get(str(_p[0]))
            if _air and os.path.exists(f'web/assets/library/{_air}.glb'): _p[0] = _air
shots = [build_beat(k, b) for k, b in enumerate(beats)]
A_js = ', '.join(['0'] + [f"WS({starts[k]}, -3)" for k in range(1, len(beats))] + ['TOTAL_F()'])
assets = sorted(set(B.get('assets', []) + re.findall(r'asset: ["\']([^"\']+)["\']', ' '.join(shots)) + [p[0] for b in beats for p in b.get('props', [])] + [x_ for b in beats if b.get('veiculo') for x_ in (['kit/carro_redondo', 'kit/carro_antigo', 'kit/carro_50'] if b['veiculo'].get('asset', 'vehicles/car') in ('vehicles/car', 'kit/carro_redondo') else [b['veiculo'].get('asset')])]))

spec = f"""// {B.get('title', ID)} -- GERADO por mkvideo.py a partir de videos/{ID}/beats.json (edite o beats.json, nao este arquivo)
{_REG_JS}const X = {SETX}, DK = 6;{''.join(f' const X_{n} = {SETS_X[n]};' for n in USED_SETS[1:])}
const WS = (i, off = 0) => TIMING.words[Math.min(i, TIMING.words.length - 1)][0] + off;
const _MA = (a, b) => {{ const r = Object.assign({{}}, a, b); if (a.over && b.over) r.over = Object.assign({{}}, a.over, b.over); for (const k of ['gests', 'poses', 'moves', 'inters', 'yFns']) if (a[k] && b[k]) r[k] = a[k].concat(b[k]); return r; }};   // frame em que a palavra de indice i comeca
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
    if b.get('_galope'): c2.append(f"steps(F({a}), F({e}), 0.19, 0.55)")   # cascos do cavalo galopando
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
_pre += ['', f"OBJETO HEROI: {HEROI}" if HEROI else "OBJETO HEROI: nenhum achado (ponha 'heroi': 'kit/...' no topo do roteiro)" + (f' - aparece em {_nh} cena(s), close nele em {_nd}' + ('  << AVISO: sem close no objeto heroi' if not _nd else '') if HEROI else ''), f'GRANDES MOMENTOS (plano aberto com multidao, efeito e som): {_nm}' + ('  << AVISO: menos de 2' if _nm < 2 else '') + ' -> ' + ', '.join(f'b{i}' for i, b in enumerate(beats) if b.get('impact')), 'Interacoes entre personagens: ' + (', '.join(f"b{i} {b['_inter']}" for i, b in enumerate(beats) if b.get('_inter')) or 'nenhuma')]
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
    _ok |= set(b.get('_enc_words', []))
    if b.get('_veic_anim'): _ok |= {nrm(w) for w in b['say'].split() if re.match(r'(voa|voo|decol|pul|salt|desc|pous|acel|dirig)', nrm(w))}   # veiculo animado na palavra (poeira + som de arrancada)
    if b.get('montado'): _ok |= {nrm(w) for w in b['say'].split() if re.match(r'(corr|cavalg|galop|atir|dispar)', nrm(w))}   # galope com som de cascos + tiro com clarao
    _falta = [] if (b.get('impact') or b.get('sfx') or b.get('fx')) else sorted({w.strip('.,!?"') for w in b['say'].split() if _ACAO.match(nrm(w)) and nrm(w) not in _ok and len(nrm(w)) > 3 and not (b.get('_chega') and re.match(r'cheg|entr|invad', nrm(w))) and not (b.get('_acao') and re.match(r'conver|discut|brig|danc|comemor', nrm(w)))})[:4]
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
        elif not (b.get('animals') or b.get('emus') or (b.get('montado') and _ANIM_OK[a_] in ('horse',))): R.append((f'{a_} citado e nao esta em cena', '"animals": [["' + _ANIM_OK[a_] + '", 1.6, 0.6]]' if _ANIM_OK[a_] != 'emus' else '"emus": true'))
    m_ = re.findall(r'\b(nadou|nadaram|nadando|cavalg\w+|montou|montaram|escalou|escalaram|mergulh\w+|voou|voaram|ajoelh\w+|deitou|dormiu|dormiam|sentou|sentaram|subiu|subiram|pulou no|cavou|cavaram)\b', t)
    if b.get('_veic_anim'): m_ = [x_ for x_ in m_ if not re.match(r'voou|voaram|subiu|subiram', x_)]
    if b.get('montado'): m_ = [x_ for x_ in m_ if not re.match(r'cavalg|montou|montaram', x_)]
    if m_ and not b.get('impact') and not b.get('caminhoes'): R.append((f'acao sem animacao propria: {", ".join(sorted(set(m_)))}', 'mostrar o RESULTADO (objeto em cena, reacao, efeito + som) ou reescrever a frase com acao que a ferramenta faz (andar, chegar, discutir, empurrar, entregar, comemorar, atirar, fugir)'))
    # SEGUIR O ROTEIRO A RISCA (ordem do Gibson: 100% do que a narracao diz acontece na tela) -- cada familia de palavra EXIGE a acao correspondente
    if re.search(r'queim|incendi|\bfogo\b|em chamas|\bchamas\b', t) and not re.search(r'abriram fogo|abriu fogo|fogo amigo|cessar fogo|arma de fogo|lanca ?chamas|extintor', t) and not b.get('_fogo'): R.append(('a narracao fala de FOGO e nao ha fogo em cena', 'tirar "interior"/"fogo": false desta cena (as labaredas entram sozinhas em cena externa) e por tocha na mao de quem ateia: "who": ["GAU:0:angry:torch", ...]'))
    if re.search(r'\bbatalha|\blutaram|\blutou|\batacaram|\batacou|\bataque\b|\bcombate|\binvadiram|\binvadiu|\binvadido|bombarde|\bguerrearam|tiroteio', t) and not (b.get('impact') or b.get('batalha') or b.get('esperando') or b.get('desembarque') or (b.get('crowd') and re.search(r'aconteceu|houve|foi uma|ficou conhecid|chamad', t))): R.append(('a narracao fala de BATALHA/ATAQUE e a cena nao encena a luta', '"batalha": true nesta cena (tropa dos dois lados no "crowd", tiros/golpes e gente fugindo); cada batalha citada no roteiro = uma cena com "batalha": true'))
    if re.search(r'explodi|explos|\bbomba', t) and not (b.get('impact') or any(str(e_).startswith('burst') for e_ in b.get('fx', [])) or (re.search(r'\bbomba', t) and not re.search(r'explodi|explos', t) and any('bomb' in str(p_[0]) for p_ in b.get('props', [])))): R.append(('a narracao fala de EXPLOSAO e nao ha explosao', '"fx": ["burst@30"], "sfx": ["cannon@30"] (acerte o numero para o quadro da palavra)'))
    if re.search(r'\bfugiu|\bfugiram|\bcorreu|\bcorreram|debandada|\bfuga\b|bateu em retirada|recuaram', t) and not re.search(r'correu (o|pelo) mundo|noticia correu|boato correu|video correu|correu a noticia|tempo correu', t) and not (b.get('impact') or b.get('shot') == 'track' or b.get('move') or b.get('_chega') or b.get('montado')): R.append(('a narracao fala de FUGA/CORRERIA e ninguem corre', '"shot": "track" (os personagens atravessam a tela andando/correndo) ou "batalha": true (a tropa foge no plano aberto)'))
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
    # ===== VERIFICADOR DE ACAO (ordem do Gibson): todo verbo de acao da frase precisa de animacao na cena; senao o video NAO renderiza =====
    _stg = set(b.get('_enc_words', [])) | {nrm(w_) for kk_, w_, kd_ in PLANO if kk_ == k}
    _fam = (('voando', r'voar|voou|ares|explod|bomba'), ('desembarque', r'cheg|desembarc|navio|atrac|aport'), ('lados', r'avanc|atac|lut|enfrent|batalh|combat|tiro|canh|explod'),
            ('impact', r'atir|tiro|dispar|explod|canh|bomb|atac|lut|batalh|corr|fug|caiu|cairam|morre|matou|invad|grit'), ('interacao', r'apert|cumpriment|paz|abrac|empurr|entreg|pag|dava|deu'),
            ('para_casa', r'volt|foram|foi|retorn'), ('esperando', r'esper|aguard|escond'), ('acao', r'conver|discut|brig|ofend|danc|comemor|brind|riu|riram|gargalh|negoci'), ('veiculo', r'dirig|carro|pilot|corr|fug'),
            ('caminhoes', r'.'), ('animals', r'corr|fug|comeu|comia|comendo|andou|entrou'), ('chega', r'cheg|invad|entr'), ('crowd', r'march|desfil'), ('_veic_anim', r'voa|voo|voou|voar|decol|pul|salt|desc|pous|acel|dirig|and|corr'), ('montado', r'corr|cavalg|galop|fug|atir|dispar'))
    _faltam = []
    for w_ in b['say'].split():
        n_ = nrm(w_)
        if len(n_) < 4 or '-' in w_ or not _ACAO.match(n_) or n_ in _stg or re.match(r'corrente|comprid|comprim|vendo$|marchando$', n_): continue
        if any(b.get(f_) and re.match(r_, n_) for f_, r_ in _fam): continue
        _faltam.append(w_.strip('.,!?":;'))
    b['_faltam'] = list(dict.fromkeys(_faltam))
    if _faltam and not b.get('verificador') is False: R.append((f'ACAO SEM ANIMACAO na narracao: {", ".join(dict.fromkeys(_faltam))}', 'a cena precisa MOSTRAR a acao: reescreva com um verbo que a ferramenta encena (veja OPERACAO.md "MODO DE ACAO") ou marque a cena ("batalha", "interacao", "acao", "animals", "props")'))
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
if sum(1 for b in beats if b.get('impact')) < int(B.get('min_momentos', 2)): _glob.append(('menos de 2 grandes momentos', '"batalha": true (ou "impact": true) em duas cenas de acao'))
if HEROI and not any(b.get('_det_heroi') for b in beats): _glob.append((f'objeto heroi ({HEROI}) sem close de camera', 'por o objeto em "props" de uma cena media de 8+ palavras'))
_cl = __import__('collections').Counter(_lug(b_) for b_ in beats)
if len(beats) >= 6 and B.get('variar_cenario') is not False and (len(_cl) < 3 or _cl.most_common(1)[0][1] > len(beats) // 2):
    _glob.append((f'pouca variedade de cenario ({dict(_cl)}): o video fica parecendo todos os outros', 'pelo menos 3 lugares e nenhum em mais da metade das cenas: troque "set"/"interior" de algumas cenas (lugares: ' + ', '.join(SETS_X) + ' | interior: madeira, pedra, loja)'))
# PESQUISA VISUAL OBRIGATORIA (ordem do Gibson 23/11): todo roteiro traz "visual" com ONDE/QUANDO/QUEM/ROUPAS DA EPOCA/CENARIO/OBJETOS e as FONTES VISUAIS (fotos, quadros, videos)
_VIS = B.get('visual') or {}
_vfal = [k_ for k_ in ('local', 'quando', 'participantes', 'roupas', 'cenario', 'objetos', 'fontes_visuais') if not _VIS.get(k_)]
if B.get('serie') != 'Teste' and _vfal: _glob.append((f'roteiro sem pesquisa visual completa (falta: {", ".join(_vfal)})', 'pesquisar fotos/quadros/videos do fato e preencher "visual" no topo do beats.json (veja GUIA_DO_ROTEIRISTA.md "Pesquisa visual") e ajustar figurino, cenario e objetos a ela'))
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
# ---------- FOLHA 3 (ordem do Gibson 19/11): CATALOGO DE ACOES do roteiro, frase por frase, com o instante de cada acao e a animacao que a ferramenta executa ----------
_ENC_DESC = {'mistura': 'mexe a panela (borbulhando)', 'cai': 'o material voa da mao e cai no alvo pela GRAVIDADE (parabola, 0,53 s) + respingo', 'calor': 'vapor/calor saindo', 'vira': 'o material vira o produto, que surge girando em destaque',
    'constroi': 'martela e o objeto cresce', 'examina': 'examina com lupa/microscopio/balanca', 'quimico': 'frasco e tubos de ensaio + fumacinha', 'escreve': 'escreve/assina', 'golpe': 'soco + estouro', 'pega': 'levanta/segura',
    'corta': 'machado e toras + poeira', 'voto': 'poe o voto na urna', 'quebra': 'quebra + estouro + tremor', 'desaba': 'desaba: nuvem de poeira + tremor', 'pensa': 'mao no queixo + brilho de ideia',
    'protesto': 'punho para cima (protesto)', 'fala': 'aponta explicando', 'olha': 'aponta/olha', 'sai': 'sai andando pela lateral', 'tomba': 'cai sentado no chao + poeira', 'paga': 'estende a mao com moedas + brilho', 'chega': 'entra andando pela lateral', 'danca': 'danca de bracos para cima', 'duvida': 'ombros para cima (nao acredita)', 'ajoelha': 'de joelhos, maos de suplica', 'morre': 'cai no chao (ou tumulo se morreu anos depois)', 'dorme': 'dormindo', 'senta': 'senta',
    'raspa': 'maquina na cabeca + cabelo voando', 'prende': 'empurra/prende', 'escala': 'escala (bracos para cima)', 'espeta': 'espeta + estouro', 'bola': 'chuta a bola: parabola pela GRAVIDADE (0,67 s)', 'negocio': 'moeda girando (compra/venda)',
    'tira': 'tira foto (celular + flash)', 'rende': 'maos para cima (rendicao)', 'voa': 'decola: poeira no chao, olha para cima', 'cava': 'cava: poeira', 'vence': 'bracos para cima + brilho', 'perde': 'mao na testa',
    'toca': 'onda de som (sirene/sino)', 'queima': 'fogo + fumaca', 'grita': 'grita de bracos para cima', 'atira': 'arma na mao, aponta, clarao e som de tiro', 'corre': 'sai correndo pela lateral + poeira', 'pula': f'pula 2 vezes: sobe {GPULO_H} m e volta pela GRAVIDADE em {GPULO_T:.2f} s cada pulo', 'acena': 'acena com a mao', 'empurra': 'empurra/puxa', 'brilha': 'o objeto brilha na palavra (ondas de luz + estrelas)',
    'x_bebe': 'leva o copo a boca', 'x_come': 'leva a comida a boca', 'x_chora': 'mao no rosto + lagrimas', 'x_canta': 'canta de bracos abertos + onda de som', 'x_le': 'le o papel', 'x_fone': 'celular na mao + toque',
    'x_lava': 'lava/esfrega na bacia + respingo', 'x_beija': 'beijo/abraco + brilho', 'x_planta': 'cava/planta + terra', 'x_pesca': 'puxa a linha + respingo', 'x_costura': 'costura', 'x_pinta': 'pinta/desenha + brilho',
    'x_bate': 'bate + estouro', 'x_procura': 'procura com a lupa', 'x_vigia': 'vigia de bracos cruzados', 'x_saluda': 'bate continencia', 'x_reza': 'reza + brilho', 'x_aplaude': 'aplaude de bracos para cima',
    'x_abraca': 'abraco', 'x_acorda': 'estava dormindo e acorda na palavra', 'x_espera': 'espera de bracos cruzados', 'x_treme': 'treme', 'x_tosse': 'tosse/espirra + nuvenzinha', 'x_nada': 'braco para cima + respingo',
    'x_ri': 'ri de bracos para cima + brilho', 'x_abre': 'empurra a porta', 'x_solta': 'solta/liberta + brilho', 'x_entrega': 'estende a mao entregando', 'x_discute': 'discussao cara a cara (dedo apontado)', 'x_aperta': 'aperto de mao + brilho', 'x_desce': 'desce/pousa + poeira no chao', 'x_defende': 'bracos cruzados se defendendo + onda', 'x_dirige': 'dirige/acelera + poeira'}
_KIND_DESC = {'burst': 'estouro/clarao + som', 'dust': 'poeira + som', 'puff': 'fumaca + som', 'stars': 'estrelinhas + som', 'ring': 'onda + som', 'splash': 'respingo + som', 'creak': 'rangido', 'expr': 'o ROSTO muda na palavra'}
def _tempo_palavras():
    try: return [w_['s'] for w_ in json.load(open(f'stories/{ID}/work/words.json'))]
    except Exception: return None
_TW = _tempo_palavras()
def _tseg(wi_): return (_TW[min(wi_, len(_TW) - 1)] if _TW else wi_ / 2.7)
_f3 = [f'# FOLHA 3 - ACOES - {B.get("title", ID)}', '', 'Catalogo de TODAS as acoes do roteiro, frase por frase, com o instante (segundos) e a animacao que a ferramenta executa. Gerada pelo MODO DE ACAO (mkvideo.py); conferir no prechecar.', '']
_ntot = _nok = _nfal = 0
for k, b in enumerate(beats):
    _ws3 = b['say'].split(); _rows = []
    for kk_, w_, kd_ in PLANO:
        if kk_ != k: continue
        if w_.startswith('encena: '):
            t_ = w_.split(': ')[1].split(' ')[0]; rxs_ = [r__ for r__, g__, tt__ in ENC if tt__ == t_]
            _mj = re.search(r' @(\d+)$', w_); j_ = int(_mj.group(1)) if _mj else next((j__ for j__, ww__ in enumerate(_ws3) if any(re.match(r__, nrm(ww__)) for r__ in rxs_)), 0); j_ = min(j_, max(0, len(_ws3) - 1)); _rows.append((j_, _ws3[j_].strip('.,!?":;') if _ws3 else '-', 'ACAO: ' + t_, _ENC_DESC.get(t_, t_)))
        elif w_.startswith('(rosto) '):
            ex_ = w_.split(' ', 1)[1]; j_ = next((j__ for j__, ww__ in enumerate(_ws3) if any(re.match(r__, nrm(ww__)) and e__ == ex_ for r__, e__ in [])), None)
            _rows.append((None, '-', 'EMOCAO: ' + ex_, 'o rosto vira "' + ex_ + '" na palavra'))
        elif kd_ in ('acao', 'shot'): _rows.append((None, '-', 'CENA', w_))
        else:
            j_ = next((j__ for j__, ww__ in enumerate(_ws3) if nrm(ww__) == nrm(w_)), None); _rows.append((j_, w_, 'EFEITO: ' + kd_, _KIND_DESC.get(kd_, kd_)))
    if b.get('impact'): _rows.append((None, '-', 'BATALHA', 'tropa em combate: tiros piscando pela tropa, soldados caindo' + (', os dois exercitos um contra o outro' if b.get('lados') else '')))
    if b.get('_inter'): _rows.append((None, '-', 'INTERACAO', b['_inter']))
    if b.get('_acao') and b['_acao'] not in ('encena',): _rows.append((None, '-', 'ATUACAO', b['_acao']))
    if b.get('_chega'): _rows.append((None, '-', 'CHEGADA', 'alguem entra andando'))
    if b.get('mapa'): _rows.append((None, '-', 'MAPA', str(b['mapa'])))
    if b.get('text'): _rows.append((None, '-', 'PLACA', str(b['text'])))
    _fal = b.get('_faltam') or []
    _ntot += len(_rows) + len(_fal); _nok += len(_rows); _nfal += len(_fal)
    _f3 += [f'## Cena b{k} - {_tseg(starts[k]):.1f}s a {_tseg(starts[k] + max(0, len(_ws3) - 1)):.1f}s - {len(_ws3)} palavras - plano {b.get("shot")}', f'> "{b["say"]}"', '',
            '| # | palavra (instante) | acao catalogada | animacao executada | ok? |', '|---|---|---|---|---|']
    for n_, (j_, w_, tp_, an_) in enumerate(sorted(_rows, key=lambda r_: (r_[0] is None, r_[0] or 0)), 1):
        _f3.append(f'| {n_} | {w_}' + (f' ({_tseg(starts[k] + j_):.1f}s)' if j_ is not None else '') + f' | {tp_} | {an_} | OK |')
    for w_ in _fal: _f3.append(f'| ! | {w_} | ACAO SEM ANIMACAO | (nenhuma) - corrigir o roteiro ou marcar a cena | FALTA |')
    if not _rows and not _fal: _f3.append('| - | - | (frase de comentario) | personagens falando/gesticulando | OK |')
    _f3.append('')
_f3[3:3] = [f'**Resumo:** {len(beats)} frases, {_ntot} acoes catalogadas, {_nok} com animacao, {_nfal} faltando' + (' -> NAO RENDERIZAR ate zerar' if _nfal else ' -> pronto para renderizar'), '']
open(f'stories/{ID}/folha3_acao.md', 'w', encoding='utf-8').write('\n'.join(_f3) + '\n')
import hashlib as _hl
_F3_LIST = [l_ for l_ in _f3 if l_.startswith('| ') and not l_.startswith('| #')]
_F3_HASH = _hl.sha1('\n'.join(_F3_LIST).encode()).hexdigest()[:12]
open(f'stories/{ID}/folha1_roteiro.md', 'w', encoding='utf-8').write('\n'.join(_f1) + '\n'); open(f'stories/{ID}/folha2_producao.md', 'w', encoding='utf-8').write('\n'.join(_f2) + '\n')
_HPROD = _hl.sha1((open(f'stories/{ID}/spec.js', encoding='utf-8').read() + _F3_HASH).encode()).hexdigest()[:12]   # assinatura da PRODUCAO inteira (visual + acoes): storyboard e aprovacao valem so' para ela
json.dump({'riscos': _tot_r + len(_glob), 'acoes': _nok, 'faltando': _nfal, 'hash_folha3': _F3_HASH, 'hash_producao': _HPROD, 'linhas_folha3': len(_F3_LIST)}, open(f'stories/{ID}/folhas.json', 'w'))
with open(f'stories/{ID}/spec.js', 'a', encoding='utf-8') as _sf: _sf.write(f'\n// FOLHA3 {_F3_HASH} {len(_F3_LIST)} acoes={_nok} faltando={_nfal}\n')   # o video que vai ao render carrega a assinatura da folha 3 que o gerou
print(f'TRES FOLHAS: stories/{ID}/folha1_roteiro.md (historia e som), stories/{ID}/folha2_producao.md (producao) e stories/{ID}/folha3_acao.md ({_nok} acoes, {_nfal} faltando) -> {_tot_r + len(_glob)} RISCO(S) em aberto' + (': ' + '; '.join([f'b{k} {r}' for k, (r, c) in _allr] + [r for r, c in _glob])[:600] if _tot_r + len(_glob) else ''))

open(f'stories/{ID}/riscos.txt', 'w').write(str(_tot_r + len(_glob) + _sem) + '\n')   # lido por novo_video.sh e conferir.sh


# ---------- v10: HERO MANIFEST (Modos 1, 2 e 3) ----------
MODO_ATIVO = MODO_CLI if MODO_CLI is not None else int(B.get('modo', 1))
_hero_list = []
for _hk, _hb in enumerate(beats):
    if _hb.get('hero_shot'):
        _t0_h = _tseg(starts[_hk])
        _t1_h = _tseg(starts[_hk + 1]) if _hk + 1 < len(starts) else _tseg(len(_TW) - 1) + 0.5
        _hero_list.append({
            'beat': f'b{_hk}', 'index': _hk, 'start_word': starts[_hk],
            'end_word': starts[_hk + 1] - 1 if _hk + 1 < len(starts) else len(_TW) - 1,
            't_start': round(_t0_h, 3), 't_end': round(_t1_h, 3),
            'say': _hb['say'], 'set': _hb.get('set', SET),
            'prompt': _hb.get('hero_prompt') or f"Ricks Clips 2D stick-figure cartoon in vibrant 3D environment: {_hb['say']}",
            'blender_preset': _hb.get('blender_preset', 'explosion' if _hb.get('batalha') else 'action_closeup')
        })
json.dump({'id': ID, 'modo': MODO_ATIVO, 'title': B.get('title', ID), 'hero_shots': _hero_list},
          open(f'stories/{ID}/hero_manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"v10 MODO {MODO_ATIVO} ativo | {len(_hero_list)} hero shot(s) mapeado(s) -> stories/{ID}/hero_manifest.json")
