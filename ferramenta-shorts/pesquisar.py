#!/usr/bin/env python3
"""pesquisar.py <id>  -- PESQUISA DE CAMPO AUTOMATICA (folha 4), ordem do Gibson 24/11.
Le o plano de pesquisa que o mkvideo.py monta a partir do roteiro (referencias/<id>/plano_pesquisa.json: lugar, epoca, pessoas, roupas,
objetos, veiculos, mecanismos), busca cada item na internet (Wikimedia Commons: fotos, quadros e desenhos de dominio publico), baixa as
imagens ("prints") para referencias/<id>/prints/, monta o quadro de referencias referencias/<id>/moodboard.jpg e grava
referencias/<id>/pesquisa.json (o que foi achado para cada item). Depois rode `python3 mkvideo.py <id>` de novo: a folha 4 sai preenchida.
Item sem imagem: escreva a consulta em ingles em "visual": {"buscas": {"<item>": "<consulta>"}} no roteiro, ou anexe a referencia a mao em
"visual": {"referencias": {"<item>": "<url ou descricao do que foi visto>"}}."""
import json, os, re, sys, subprocess, urllib.parse, hashlib
ID = sys.argv[1]; ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
D = f'referencias/{ID}'; P = f'{D}/plano_pesquisa.json'
if not os.path.exists(P): subprocess.run([sys.executable, 'mkvideo.py', ID], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
plano = json.load(open(P, encoding='utf-8')); os.makedirs(f'{D}/prints', exist_ok=True)
UA = 'Mozilla/5.0 (X11; Linux x86_64) ferramenta-shorts/1.0 (pesquisa de referencia visual)'
import time
def get(url, out=None):   # educado com o servidor: 1 pedido a cada ~1,5 s e espera maior se ele reclamar de excesso
    for t_ in ((0,) if out else (0, 8, 25)):
        time.sleep(1.5 + t_)
        r = subprocess.run(['curl', '-s', '-L', '-m', '25', '-A', UA] + (['-o', out] if out else []) + [url], capture_output=True)
        if out:
            if os.path.exists(out) and os.path.getsize(out) > 1500 and open(out, 'rb').read(4)[:3] in (b'\xff\xd8\xff', b'\x89PN'): return True   # so' vale se for imagem de verdade (JPEG/PNG)
            if os.path.exists(out): os.remove(out)
            continue
        if b'too many requests' not in r.stdout[:200].lower() and r.stdout: return r.stdout
    return b'' if not out else False
def commons(q, n=3):   # busca de imagens do Wikimedia Commons (pagina de busca; a API fica bloqueada por excesso de pedidos nesta rede)
    u = 'https://commons.wikimedia.org/w/index.php?' + urllib.parse.urlencode({'search': q, 'title': 'Special:MediaSearch', 'type': 'image'})
    try: h = (get(u) or b'').decode('utf-8', 'ignore')
    except Exception: h = ''
    res = []; vistos = set()
    for m in re.finditer(r'"title":"(File:[^"]+)"', h):
        try: tit = json.loads('"' + m.group(1) + '"')
        except Exception: tit = m.group(1).encode('utf-8', 'ignore').decode('unicode_escape', 'ignore') if '\\u' in m.group(1) else m.group(1)   # titulo com escape estranho nao derruba a pesquisa
        blk = h[m.end():m.end() + 4000]
        if tit in vistos or not re.search(r'\.(jpe?g|png)$', tit, re.I): continue
        t = re.search(r'"thumburl":"([^"]+)"', blk) or re.search(r'"url":"(https:[^"]+upload[^"]+)"', blk)
        if not t: continue
        vistos.add(tit); nm_ = tit.replace('File:', '').replace(' ', '_'); hx = hashlib.md5(nm_.encode('utf-8')).hexdigest()
        thumb = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{hx[0]}/{hx[:2]}/{urllib.parse.quote(nm_)}/500px-{urllib.parse.quote(nm_)}"   # servidor liberado nesta rede (thumb.wikimedia.org e' bloqueado)
        idx = re.search(r'"index":(\d+)', blk); sn = re.search(r'"snippet":"([^"]{0,300})', blk)
        res.append({'titulo': tit.replace('File:', ''), 'thumb': thumb, 'pagina': 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(tit.replace(' ', '_')), 'descricao': re.sub(r'\\u003C[^>]*?\\u003E|<[^>]+>', '', sn.group(1))[:200] if sn else '', 'ordem': int(idx.group(1)) if idx else 99})
    return sorted(res, key=lambda x: x['ordem'])[:n]
# PRINT ERRADO SE DESCARTA (24/11): quem confere o quadro escreve em referencias/<id>/prints_ruins.txt o nome do arquivo (ou um pedaco do titulo) de cada
# print que nao tem nada a ver; ao rodar de novo, a pesquisa pula esses e pega o proximo resultado.
RUINS = [l.strip().lower() for l in open(f'{D}/prints_ruins.txt', encoding='utf-8')] if os.path.exists(f'{D}/prints_ruins.txt') else []
RUINS = [r for r in RUINS if r and not r.startswith('#')]
ruim = lambda titulo, arq='': any(r in titulo.lower() or (arq and r in os.path.basename(arq).lower()) for r in RUINS)
# CONSULTA EM INGLES AUTOMATICA (24/11: Goodyear e Abelhas travaram porque a busca em portugues nao acha nada no Commons):
# traduz palavra por palavra as palavras comuns; nomes proprios ficam como estao; o resto (artigos, preposicoes) sai.
PT_EN = dict(x.split(':') for x in ('abelha:bee abelhas:bees colmeia:beehive colmeias:beehives mel:honey flor:flower flores:flowers jardim:garden casa:house casas:houses '
  'verao:summer inverno:winter lago:lake rio:river mar:sea praia:beach porto:harbor cais:pier navio:ship navios:ships barco:boat barcos:boats trem:train estacao:station '
  'cientista:scientist cientistas:scientists colegas:colleagues laboratorio:laboratory microscopio:microscope vidro:glass madeira:wooden ferro:iron pedra:stone '
  'fogao:stove panela:pot panelas:pots cozinha:kitchen prisao:prison guarda:guard guardas:guards soldado:soldier soldados:soldiers tropa:troops exercito:army '
  'rei:king rainha:queen castelo:castle forte:fort igreja:church cidade:town vila:village rua:street mercado:market barraca:stall fazenda:farm campo:field '
  'montanha:mountain montanhas:mountains alpes:alps floresta:forest selva:jungle deserto:desert gelo:ice neve:snow ilha:island ponte:bridge fabrica:factory fabricas:factories '
  'roupa:clothing roupas:clothing vestido:dress chapeu:hat farda:uniform uniforme:uniform pescador:fisherman pescadores:fishermen lagosta:lobster melancia:watermelon '
  'borracha:rubber pneu:tire pneus:tires bola:ball bolas:balls carro:car caminhao:truck aviao:airplane avioes:airplanes balao:balloon foguete:rocket canhao:cannon '
  'espada:sword fuzil:rifle pistola:pistol bandeira:flag mapa:map carta:letter jornal:newspaper jornais:newspapers livro:book caderno:notebook cadernos:notebooks '
  'caixa:box caixas:boxes chumbo:lead garrafa:bottle uisque:whisky vinho:wine cerveja:beer pao:bread queijo:cheese bolo:cake porco:pig cavalo:horse vaca:cow '
  'galinha:chicken ganso:goose gansos:geese cachorro:dog gato:cat urso:bear emu:emu tulipa:tulip tulipas:tulips bulbo:bulb bulbos:bulbs comerciante:merchant '
  'comerciantes:merchants inventor:inventor presidente:president governador:governor marinheiro:sailor marinheiros:sailors policia:police tribunal:courtroom juiz:judge '
  'escola:school professor:teacher medico:doctor hospital:hospital doente:patient remedio:medicine mofo:mold placa:plate danca:dance dancam:dance mapa:map sol:sun '
  'noite:night antigo:antique antiga:antique quente:hot crua:raw cru:raw seculo:century epoca:period').split())
def ingles(q):
    import unicodedata
    ws = []
    for w in re.findall(r"[\w']+", q):
        k = unicodedata.normalize('NFD', w.lower()).encode('ascii', 'ignore').decode()
        if k in PT_EN: ws.append(PT_EN[k])
        elif w[:1].isupper() and len(w) > 2 and k not in ('era', 'uma', 'um', 'os', 'as', 'que', 'em', 'de', 'do', 'da'): ws.append(w)
        elif re.match(r'^1[5-9]\d\d$', w): ws.append(w)
    return ' '.join(dict.fromkeys(ws))
out = {'id': ID, 'itens': []}
for it in plano['itens']:
    achados = []
    qs = list(it['consultas'])
    for q in it['consultas']:   # consultas de reserva, cada vez mais simples: so' os nomes proprios; as 3 primeiras palavras fortes; as 2 primeiras
        prop = ' '.join(re.findall(r'\b[A-Z][\w]+', q)); fortes = [w for w in re.findall(r'[\w]{4,}', q) if w.lower() not in ('para', 'como', 'sobre', 'entre', 'estilo', 'grupo', 'branco', 'soltando', 'embaixo')]
        qs += [x for x in ((prop,) if it['tipo'] in ('tema', 'mecanismo', 'epoca') else (prop, ' '.join(fortes[:3]), ' '.join(fortes[:2]))) if x and len(x) > 3 and len(x.split()) >= (2 if it['tipo'] in ('tema', 'mecanismo') else 1)]   # tema e mecanismo: so' nomes proprios (busca solta traz imagem que nao tem nada a ver)
    qs += [ingles(q) for q in it['consultas'] if len(ingles(q).split()) >= 1]   # reserva em ingles (o Commons e' quase todo em ingles)
    for q in list(dict.fromkeys([q for q in qs if q.strip()]))[:8]:
        for r_ in commons(q, 3 - len(achados) + 6):
            if len(achados) >= 3: break
            fn = f"{D}/prints/{re.sub(r'[^a-z0-9]+', '_', it['item'].lower())[:40]}_{hashlib.md5(r_['thumb'].encode()).hexdigest()[:6]}.jpg"
            if ruim(r_['titulo'], fn):
                if os.path.exists(fn): os.remove(fn)
                continue
            if os.path.exists(fn) or get(r_['thumb'], fn): achados.append({**r_, 'print': fn, 'consulta': q})
        if len(achados) >= 2: break
    out['itens'].append({**it, 'achados': achados}); print(f"{'ok ' if achados else 'SEM'} {it['tipo']:10s} {it['item'][:50]:50s} {len(achados)} referencia(s)")
json.dump(out, open(f'{D}/pesquisa.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
try:   # QUADRO DE REFERENCIAS (moodboard): todos os prints lado a lado, com o nome do item
    from PIL import Image, ImageDraw
    cel = [(i_['item'], a_['print']) for i_ in out['itens'] for a_ in i_['achados'][:2]]
    if cel:
        cols = 4; W, H = 320, 270; rows = -(-len(cel) // cols); M = Image.new('RGB', (cols * W, rows * H), '#101418'); dr = ImageDraw.Draw(M)
        for n_, (nm, fn) in enumerate(cel):
            try: im = Image.open(fn).convert('RGB'); im.thumbnail((W - 8, H - 34)); M.paste(im, ((n_ % cols) * W + (W - im.width) // 2, (n_ // cols) * H + 4))
            except Exception: pass
            dr.text(((n_ % cols) * W + 6, (n_ // cols) * H + H - 26), nm[:44], fill='#ffffff')
        M.save(f'{D}/moodboard.jpg', quality=88); print(f'quadro de referencias: {D}/moodboard.jpg ({len(cel)} prints)')
except Exception as e: print('moodboard nao gerado:', e)
sem = [i_['item'] for i_ in out['itens'] if not i_['achados']]
print(f"PESQUISA: {len(out['itens']) - len(sem)}/{len(out['itens'])} itens com referencia" + (f" | SEM referencia: {', '.join(sem)}" if sem else ''))
