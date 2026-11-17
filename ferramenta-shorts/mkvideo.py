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
    body = ', '.join(f'{k}: {json.dumps(v)}' for k, v in o.items())
    mou = f", ...(v % 2 ? {{ moustache: {json.dumps(mo)} }} : {{}})" if mo else ''
    outfits_js.append(f"{name}: (v = 0, e = {{}}) => ({{ _id: {json.dumps(name.lower())}, {body}, skin: {json.dumps(SKINS)}[v % 4]{mou}, ...(v % 7 === 4 ? {{ glasses: true }} : {{}}), ...(v % 7 === 5 || v % 7 === 6 ? {{ beard: ['#3a2a1f', '#6b4a2a', '#8a8a86'][v % 3] }} : {{}}), ...e }})")

# ---------- posicoes automaticas ----------
def slots(n):
    base = {1: [0.0], 2: [-1.15, 1.15], 3: [-2.1, 0.0, 2.1], 4: [-3.0, -1.0, 1.0, 3.0], 5: [-3.6, -1.8, 0, 1.8, 3.6], 6: [-3.8, -2.3, -0.8, 0.8, 2.3, 3.8]}
    if n in base: return base[n]
    return [(i - (n - 1) / 2) * 1.6 for i in range(n)]
ZS = [2.4, 2.0, 2.8, 2.2, 3.0, 2.6]
ZSW = [-0.4, 0.2, -0.8, 0.0, -0.2, 0.4]

TEMPL = {  # h = altura do alvo; d0/d1 = distancia da camera no inicio/fim; el = elevacao; fov
    'wide':  dict(h=2.8, d0=30, d1=24, el=14, fov=46),
    'two':   dict(h=2.3, d0=7.0, d1=5.8),
    'close': dict(h=2.4, d0=4.8, d1=4.0),
    'group': dict(h=2.5, d0=9.0, d1=7.4),
    'prop':  dict(h=1.4, d0=8.0, d1=6.0, el=8),
    'crowd': dict(h=2.8, d0=29.0, d1=22.0, el=16),
    'track': dict(h=2.2, d0=8.0, d1=8.0, el=3, fov=44),
    'low':   dict(h=1.6, d0=7.0, d1=5.6, el=2),
    'reveal': dict(h=2.6, d0=15.0, d1=36.0, el=12, fov=46),   # recua e revela o exercito inteiro
    'orbit':  dict(h=2.6, d0=27.0, d1=22.0, el=14, fov=46, az0=-38, az1=32),   # panoramica aberta em arco
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
    (re.compile(r'^(tiro|tiros|disparou|dispararam|atirava|atirou|atiraram|explodiu|explosao|canhoes|canhao|fogo|bomba|bombas)$'), 'burst', 0.09),
    (re.compile(r'^(gritou|gritaram|socorro|ataque|atacar|atacaram|alarme)$'), 'ring', 0.06),
    (re.compile(r'^(panico|correu|correram|fugiu|fugiram|correria|debandada|fuga)$'), 'dust', 0.07),
    (re.compile(r'^(festa|beberam|brindou|brindaram|comemoraram|venceu|ganhou|vitoria)$'), 'stars', 0.0),
    (re.compile(r'^(empurra|empurrouse|briga|brigaram|discussao|confusao|caos|desastre)$'), 'puff', 0.05),
    (re.compile(r'^(chegou|chegaram|apareceu|surgiu|invadiu|desabou|caiu|cairam)$'), 'dust', 0.04),
]
IMPACT = re.compile(r'tiro|atir|dispar|metralhador|canho|explod|explos|batalha|atacou|atacaram|ataque|fugi|fugir|correndo|correram|debandada|espalha|panico|invadi|carga|bombard')
SHOOT = re.compile(r'tiro|atir|dispar|metralhador|canho|balas|bombard')
def direct(beats):
    """DIRETOR AUTOMATICO: planos abertos, multidao e ritmo de camera. 'shot_lock': true no beat desliga; 'director': false no arquivo desliga tudo."""
    if B.get('director') is False: return
    run = 0; wide_n = 0; wrun = 0; impact_n = 0
    outs = list(B.get('outfits', {}))
    for k, b in enumerate(beats):
        if b.get('shot_lock'):
            run = 0 if b.get('shot', 'two') in WIDE else run + 1; continue
        say = nrm(b['say']); words = [nrm(w) for w in b['say'].split()]
        mass = bool(MASS.search(say)); arrive = bool(ARRIVE.search(say))
        shot = b.get('shot', 'two'); first = (k == 0); last = (k == len(beats) - 1)
        if first: shot = 'reveal'
        elif mass and arrive: shot = 'reveal'
        elif mass: shot = 'orbit' if wide_n % 2 else 'crowd'
        elif last: shot = 'reveal'
        elif run >= 2 and not CLOSE_OK.search(say): shot = 'orbit' if wide_n % 2 else 'wide'
        elif shot in ('track', 'two', 'group') and k % 5 == 3 and not CLOSE_OK.search(say): shot = 'wide'
        if shot in WIDE and not b.get('impact') and (wrun >= 2 or (wrun >= 1 and k == len(beats) - 2)) and not (first or last):   # nunca mais de 2 planos abertos seguidos: alterna com plano medio + multidao ao fundo
            shot = 'group' if mass else 'two'
        if not (first or last) and IMPACT.search(say) and impact_n < int(B.get('max_impact', 2)) and b.get('impact') is not False:
            impact_n += 1; b['impact'] = True; shot = 'crowd' if impact_n % 2 else 'orbit'   # MOMENTO-CHAVE: plano aberto de alto impacto (fora da cota de planos abertos)
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
            if mass and not b.get('crowd') and b.get('who') and not b.get('emus'):
                persons_out = [w.split(':')[0] for w in b['who']]
                b['crowd'] = {'n': 5, 'outfits': list(dict.fromkeys(persons_out)), 'march': False, 'expr': 'shock' if re.search('panico|tiro|gritou', say) else 'neutral'}

KICKS = []
direct(beats)
if B.get('director') is not False and not any(b.get('impact') for b in beats) and len(beats) > 4:
    _b = beats[int(len(beats) * 0.6)]
    if not _b.get('shot_lock'): _b['impact'] = True; _b['shot'] = 'orbit'; _b.setdefault('crowd', {'n': 12, 'outfits': [w.split(':')[0] for w in _b.get('who', [])] or list(B.get('outfits', {'X': 0}))[:1], 'march': False})

def build_beat(k, b):
    shot = b.get('shot', 'two'); T = dict(TEMPL.get(shot, TEMPL['two']))
    light = b.get('light')
    if not light:   # MODO RICKS: a luz acompanha a historia (noite azul, amanhecer, dia claro) quando o roteiro nao fixa
        _sy = nrm(b['say'])
        light = ('night' if re.search(r'noite|escuro|madrugada|meianoite', _sy) else 'dawn' if re.search(r'amanhecer|manhaseguinte|nascerdosol|aurora', _sy) else 'dusk' if re.search(r'pordosol|entardecer|anoitecer', _sy) else LIGHT)
    who = b.get('who', []); animals = b.get('animals', []); props = b.get('props', [])
    mv = b.get('move', 8 if shot == 'track' else 0)
    a, bb = f'A[{k}]', f'A[{k + 1}] - 1'
    # elenco de pessoas
    persons = []
    for w in who:
        p = w.split(':'); out = p[0]; v = int(p[1]) if len(p) > 1 and p[1] != '' else 0; ex = p[2] if len(p) > 2 else 'neutral'
        persons.append((out, v, ex))
    n = len(persons); sl = slots(max(n, 1))
    acts = []
    for i, (out, v, ex) in enumerate(persons):
        dx, z = sl[i], (ZSW[i % len(ZSW)] if shot in WIDE else ZS[i % len(ZS)])
        if shot == 'track' or mv:
            d = mv if mv else 8
            acts.append(f"{{ outfit: {json.dumps(out)}, v: {v}, at: [X + {num(dx - d / 2)}, {num(z)}], move: [[X + {num(dx + d / 2)}, {num(z)}], {a}, {bb}, 'lin'], pose: 'march', speed: 0.034, expr: {json.dumps(ex)} }}")
        else:
            acts.append(f"pp(X, {json.dumps(out)}, {v}, {num(dx)}, {num(z)}, {json.dumps(ex)})")
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
    em = b.get('emus')
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
            x0 = (col - (cols - 1) / 2) * (1.9 if wide else 1.7) + (row % 2) * 0.9 + jx; z0 = (1.2 if wide else -3.0) - row * 2.1 + jz
            out = outs_c[i % len(outs_c)]; ex = c.get('expr', 'neutral' if not c.get('march') else 'stern'); look = (-0.25, 0.25, 0.0, 0.15)[i % 4]
            crowd_pos.append((x0, z0))
            if c.get('march'):
                acts.append(f"{{ outfit: {json.dumps(out)}, v: {i % 4}, at: [X + {num(x0 - 9)}, {num(z0)}], move: [[X + {num(x0 + 3)}, {num(z0)}], {a}, {bb}, 'lin'], pose: 'march', speed: 0.034, expr: {json.dumps(ex)}, seed: {i % 4}, look: {look} }}")
            else:
                acts.append(f"pp(X, {json.dumps(out)}, {i % 4}, {num(x0)}, {num(z0)}, {json.dumps(ex)}, {{ look: {look}, seed: {i % 4} }})")
    # veiculo andando: "veiculo": {"asset":"vehicles/car","de":-9,"para":9,"z":0.6,"s":1.0,"motorista":"FARM:0:smile"}
    pr = []
    vc = b.get('veiculo')
    if vc:
        x0v, x1v, zv = vc.get('de', -9), vc.get('para', 9), vc.get('z', 0.6); ryv = 1.5708 if x1v >= x0v else -1.5708
        pr.append(f"{{ asset: {json.dumps(vc.get('asset', 'vehicles/car'))}, at: [X + {num(x0v)}, {num(zv)}], move: [[X + {num(x1v)}, {num(zv)}], {a}, {bb}, 'lin'], s: {num(vc.get('s', 1.0))}, bob: 0.03 }}")
        if vc.get('motorista'):
            mo_ = vc['motorista'].split(':'); 
            acts.append(f"{{ outfit: {json.dumps(mo_[0])}, v: {int(mo_[1]) if len(mo_) > 1 and mo_[1] else 0}, at: [X + {num(x0v)}, {num(zv - 0.35)}], move: [[X + {num(x1v)}, {num(zv - 0.35)}], {a}, {bb}, 'lin'], pose: 'stand', expr: {json.dumps(mo_[2] if len(mo_) > 2 else 'smile')}, s: 0.8 }}")

    for p in props:
        asset, dx, z, s = p[0], p[1] if len(p) > 1 else 0, p[2] if len(p) > 2 else 0.5, p[3] if len(p) > 3 else 1.0
        ex = p[4] if len(p) > 4 and isinstance(p[4], dict) else {}
        extra = ''.join(f', {kk}: {json.dumps(vv)}' for kk, vv in ex.items())
        pr.append(f"{{ asset: {json.dumps(asset)}, at: [X + {num(dx)}, {num(z)}], s: {num(s)}{extra} }}")
    # textos / efeitos
    fx = []
    if b.get('text'):
        st = TXT[b.get('tstyle', TXT_CYCLE[k % 4])]
        off = int(b.get('tat', 0))
        up = {'close': 0.55, 'two': 0.46}.get(shot, 0.42)   # em plano fechado o texto sobe para nao cobrir o chapeu
        fx.append(f"txt(X, WS({starts[k] + off}, -2), {bb}, {json.dumps(b['text'], ensure_ascii=False)}, '{st[0]}', '{st[1]}', {num(T['h'] + 2.2)}, {{ s: {b.get('tscale', 1.5)}, up: {up} }})")
    for e in b.get('fx', []):
        kind, _, at = e.partition('@'); at = int(at) if at else 4
        if kind == 'burst': fx.append(f"{{ k: 'burst', a: {a} + {at}, at: [X + {num(sl[0] if n else 0)}, DK + 1.8, 3.2], s: 1.2 }}")
        elif kind in ('dust', 'puff', 'stars', 'splash', 'ring', 'creak'): fx.append(f"{{ k: {json.dumps(kind)}, a: {a} + {at}, b: {a} + {at + 26}, at: [X, DK + 0.5, 1.2], s: 1.1 }}")
    if b.get('impact') and SHOOT.search(nrm(b['say'])) and crowd_pos:   # fuzilaria cartunesca: clarões piscando pela tropa + som de tiro
        for i in range(12):
            px, pz = crowd_pos[(i * 5 + 2) % len(crowd_pos)]; t0 = 8 + i * 6
            fx.append(f"{{ k: 'flash', a: {a} + {t0}, b: {a} + {t0 + 8}, at: [X + {num(px + 0.75)}, DK - 1.05, {num(pz + 0.4)}], s: 2.0 }}")   # a carta do efeito ancora pela base: y baixo poe o clarao na altura do fuzil
        b.setdefault('sfx', []); b['sfx'] += [f'gun@{8 + i * 6}' for i in range(12)]
    # animacao nas palavras-chave: golpe de camera + efeito no instante da palavra
    kfx = 0
    if b.get('kw') is not False:
        for j, w in enumerate(b['say'].split()):
            nw = nrm(w)
            for rx, kind, kick in KW:
                if rx.match(nw) and kfx < 3:
                    kfx += 1; wi = starts[k] + j; px, pz = (crowd_pos[(j * 5) % len(crowd_pos)] if crowd_pos else (sl[0] if n else 0.0, 1.5))
                    if kind == 'burst': fx.append(f"{{ k: 'burst', a: WS({wi}), b: WS({wi}) + 22, at: [X + {num(px)}, DK + 1.8, {num(pz + 1.5)}], s: {1.7 if wide else 1.2} }}")
                    else: fx.append(f"{{ k: {json.dumps(kind)}, a: WS({wi}), b: WS({wi}) + 28, at: [X + {num(px)}, DK + 0.5, {num(pz + 1.0)}], s: {1.9 if wide else 1.1} }}")
                    if kick: KICKS.append(f"{{ f: WS({wi}), a: {kick} }}")
                    break
    opts = []
    if wide:
        T.setdefault('cx', 0.0); T.setdefault('cz', -1.5)
    for kk in ('h', 'd0', 'd1', 'el', 'fov', 'az0', 'az1', 'cx', 'cz'):
        v = b.get(kk, T.get(kk))
        if v is not None: opts.append(f'{kk}: {num(v)}')
    if 'wind' in b: opts.append(f"wx: {{ wind: {b['wind']} }}")
    if wide: opts.append("hero: { hero: 'none', wide: true }"); opts.append('vary: false')
    elif b.get('veiculo'): opts.append("hero: { hero: 'none' }")   # motorista fica atras do carro de proposito
    elif persons: opts.append("hero: { hero: 'any', frame: 'medium', minH: 0.07 }")
    if b.get('trans'): opts.append(f"trans: {json.dumps(b['trans'])}")
    if b.get('vary') is False and not wide: opts.append('vary: false')
    opts.append(f"actors: [{', '.join(acts)}]")
    if pr: opts.append(f"props: [{', '.join(pr)}]")
    if fx: opts.append(f"fx: [{', '.join(fx)}]")
    call = f"S('b{k}', {a}, {bb}, X, {json.dumps(light)}, {{ {', '.join(opts)} }})"
    if wide and not (shot == 'track' or mv):
        call = f"{{ ...{call}, nocut: true }}"
    if shot == 'track' or mv:   # camera acompanha o grupo com velocidade constante (sem autocut)
        d = mv if mv else 8
        cam = (f"cam: [{{ f: {a}, at: [X + {num(-d / 2)}, DK + {num(T['h'])}, 1.5], d: {num(T['d0'])}, az: 6, el: {num(T.get('el', 3))}, fov: {num(T.get('fov', 44))} }}, "
               f"{{ f: {bb}, at: [X + {num(d / 2)}, DK + {num(T['h'])}, 1.5], d: {num(T['d1'])}, az: -8, el: {num(T.get('el', 3) + 1)}, fov: {num(T.get('fov', 44))}, ease: 'lin' }}]")
        call = f"{{ ...{call}, {cam}, nocut: true }}"
    if b.get('veiculo') and not b.get('cam_livre'):   # a camera acompanha o veiculo de lado, mostrando ele inteiro
        vc = b['veiculo']; x0v, x1v, zv = vc.get('de', -9), vc.get('para', 9), vc.get('z', 0.6); dd = vc.get('dist', 14)
        cam = (f"cam: [{{ f: {a}, at: [X + {num(x0v)}, DK + 1.5, {num(zv)}], d: {num(dd)}, az: {12 if x1v >= x0v else -12}, el: 7, fov: 40 }}, "
               f"{{ f: {bb}, at: [X + {num(x1v)}, DK + 1.5, {num(zv)}], d: {num(dd * 0.9)}, az: {-10 if x1v >= x0v else 10}, el: 8, fov: 40, ease: 'lin' }}]")
        call = f"{{ ...{call}, {cam}, nocut: true }}"
    if b.get('set') and b['set'] != SET and b['set'] in SETS_X: call = re.sub(r'\bX\b', 'X_' + b['set'], call)   # esta cena acontece em outro cenario
    return call

shots = [build_beat(k, b) for k, b in enumerate(beats)]
A_js = ', '.join(['0'] + [f"WS({starts[k]}, -3)" for k in range(1, len(beats))] + ['TOTAL_F()'])
assets = sorted(set(B.get('assets', []) + [p[0] for b in beats for p in b.get('props', [])] + [b['veiculo'].get('asset', 'vehicles/car') for b in beats if b.get('veiculo')]))

spec = f"""// {B.get('title', ID)} -- GERADO por mkvideo.py a partir de videos/{ID}/beats.json (edite o beats.json, nao este arquivo)
const X = {SETX}, DK = 6;{''.join(f' const X_{n} = {SETS_X[n]};' for n in USED_SETS[1:])}
const WS = (i, off = 0) => TIMING.words[Math.min(i, TIMING.words.length - 1)][0] + off;   // frame em que a palavra de indice i comeca
const A = [{A_js}];
const SPEC = {{
  id: {json.dumps(ID)}, {('exp: '+str(B['exp'])+', ') if 'exp' in B else ''}{('cinf: '+str(B['cinf'])+', ') if 'cinf' in B else ''}total: TOTAL_F(), sets: {json.dumps(USED_SETS)}, setx: {{ {SET}: X{''.join(f', {n}: X_{n}' for n in USED_SETS[1:])} }},
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
open(f'stories/{ID}/cues.py', 'w', encoding='utf-8').write('\n'.join(c1) + '\n#--SFX--\n' + '\n'.join(c2) + '\n')
print(f'{ID}: {len(beats)} cenas, {n} palavras narradas -> stories/{ID}/spec.js, cues.py')
