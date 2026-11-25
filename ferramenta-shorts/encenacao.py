# ENCENACAO ESCRITA (25/11, Gibson: "a ferramenta tem que entender o contexto de cada frase... solucao definitiva").
# A ferramenta (codigo) nao entende frase: le palavra por palavra. Quem ENTENDE e' a IA que escreve o roteiro.
# Por isso cada frase do beats.json leva a LEITURA da IA, escrita, e a ferramenta so' EXECUTA:
#
#   "encena": {
#     "sentido": "afirmativa" | "negativa" | "hipotese" | "figurada" | "fato",
#     "passos": [
#        {"quem": 0, "faz": "anda_ate", "alvo": "kit/bathtub", "na": "entrou"},
#        {"quem": 0, "faz": "entra_em", "alvo": "kit/bathtub", "na": "entrou"},
#        {"alvo": "kit/bathtub", "faz": "transborda", "na": "transbordou"}
#     ]
#   }
#
# sentido: afirmativa = aconteceu de verdade (tiro, explosao, briga aparecem); negativa ("nenhum tiro", "nunca veio"),
#          hipotese ("quase", "ameacou", "se tivesse"), figurada ("guerra de precos", "bateu recorde") = NADA de tiro/explosao/batalha;
#          fato = frase sem acao fisica (data, numero, explicacao) -> a cena mostra o objeto/lugar/personagens citados.
# passos: o que a TELA mostra, em ordem, preso na palavra "na" da narracao. Vocabulario em VOCAB (abaixo).
# Passo com verbo fora do VOCAB = FALTA (trava o render): a correcao e' CONSTRUIR a animacao na ferramenta, nunca pular.
import re, unicodedata

VOCAB = {   # faz -> (descricao tecnica para a folha 3, como a ferramenta executa)
    'anda_ate': ('caminha ate o objeto/lugar (entra andando pela lateral e para ao lado do alvo)', 'move'),
    'entra_em': ('entra DENTRO do objeto e senta (o objeto fica em volta da cintura, a fisica nao empurra para fora)', 'senta_dentro'),
    'transborda': ('o liquido de dentro do objeto transborda e escorre: respingos azuis em volta da borda + som de agua', 'splash'),
    'senta': ('senta no chao/banco', 'acao'), 'dorme': ('deita e dorme', 'acao'), 'ajoelha': ('ajoelha', 'acao'),
    'tomba': ('cai no chao', 'acao'), 'morre': ('cai e fica imovel', 'acao'), 'pula': ('pula', 'acao'), 'corre': ('corre', 'acao'),
    'golpe': ('da um golpe/soco no alvo', 'acao'), 'empurra': ('empurra o alvo', 'acao'), 'atira': ('atira com a arma (clarao na boca do cano + som)', 'acao'),
    'grita': ('grita com os bracos para cima', 'acao'), 'vence': ('comemora a vitoria', 'acao'), 'fala': ('fala apontando', 'acao'), 'olha': ('olha/aponta para o alvo', 'acao'),
    'pensa': ('mao no queixo, pensando', 'acao'), 'perde': ('mao na testa (derrota)', 'acao'), 'rende': ('maos para cima (rendicao)', 'acao'),
    'pega': ('pega/levanta o objeto', 'acao'), 'mistura': ('mexe a mistura', 'acao'), 'cai': ('deixa cair/joga o objeto', 'acao'),
    'constroi': ('martela/constroi', 'acao'), 'escreve': ('escreve no papel', 'acao'), 'entrega': ('entrega o objeto ao alvo', 'acao'),
    'chega': ('chega na cena', 'acao'), 'desaba': ('o objeto desaba', 'acao'),
    'mostra': ('a camera mostra o objeto/lugar citado (sem acao de personagem)', 'nada'),
}
SENTIDOS = ('afirmativa', 'negativa', 'hipotese', 'figurada', 'fato')
CONTEINER = r'bathtub|banheira|tina|barril|barrel|barco|boat|caixa|crate|carro|car|cama|bed|poco|well|panela|caldeir'

def _n(t): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', str(t).lower()).encode('ascii', 'ignore').decode())

def aplicar(B, slots, ZS):
    """Traduz "encena" de cada beat para os campos que o motor ja executa. Chamado no comeco do mkvideo."""
    for b in B['beats']:
        e = b.get('encena')
        if not isinstance(e, dict): continue
        s = e.get('sentido')
        if s in ('negativa', 'hipotese', 'figurada'):   # nada de violencia na tela, o roteiro decidiu
            b['batalha'] = False; b['tiros'] = False; b['_sentido_lido'] = s
        acoes = [a for a in (b.get('acoes') or []) if not a.get('_de_encena')]
        who = b.get('who') or []
        for p in e.get('passos') or []:
            faz = p.get('faz'); na = p.get('na') or ''; q = int(p.get('quem', 0) or 0); alvo = p.get('alvo')
            if faz == 'anda_ate': b['_anda_quem'] = q
            elif faz == 'entra_em':
                if who:
                    x0 = slots(len(who))[min(q, len(who) - 1)]
                    pr = [x for x in (b.get('props') or []) if not (isinstance(x, list) and str(x[0]) == str(alvo))]
                    b['props'] = pr + [[alvo, x0, round(ZS[min(q, len(ZS) - 1)] + 0.35, 2), 1.15, {'fixo': True, 'nocol': True}]]
                acoes.append({'palavra': na, 'tipo': 'senta', 'quem': q, '_de_encena': True})
                for k_ in ('cx', 'cz', 'd0', 'd1', '_auto_vis'): b.pop(k_, None)
            elif faz == 'transborda': b.setdefault('_splash_na', []).append([na, alvo])
            elif faz in VOCAB and VOCAB[faz][1] == 'acao':
                a = {'palavra': na, 'tipo': faz, 'quem': q, '_de_encena': True}
                if 'alvo_quem' in p: a['alvo'] = p['alvo_quem']
                acoes.append(a)
        if acoes: b['acoes'] = acoes

def validar(B):
    """Riscos que TRAVAM o render: frase sem leitura escrita, sentido invalido, passo que a ferramenta nao sabe fazer, palavra fora da frase."""
    R = []
    if B.get('encenacao_obrigatoria') is False: return R
    for i, b in enumerate(B['beats']):
        if b.get('_cta'): continue
        e = b.get('encena')
        if not isinstance(e, dict): R.append((i, 'frase SEM LEITURA ESCRITA ("encena": sentido + passos): a IA tem que ler a frase e escrever o que a tela mostra')); continue
        if e.get('sentido') not in SENTIDOS: R.append((i, f'sentido "{e.get("sentido")}" invalido (use {", ".join(SENTIDOS)})'))
        ws = [_n(w) for w in b.get('say', '').split()]
        for p in e.get('passos') or []:
            if p.get('faz') not in VOCAB: R.append((i, f'FALTA ANIMACAO "{p.get("faz")}": construir na ferramenta (encenacao.py VOCAB + motor) antes de renderizar'))
            na = _n(p.get('na', ''))
            if na and not any(na == w or na in w for w in ws): R.append((i, f'passo "{p.get("faz")}" preso na palavra "{p.get("na")}", que nao esta na frase'))
            if p.get('faz') in ('entra_em', 'transborda') and not re.search(CONTEINER, str(p.get('alvo', ''))): R.append((i, f'"{p.get("faz")}" pede um recipiente (banheira, barril, barco...): alvo "{p.get("alvo")}"'))
        if e.get('sentido') in ('negativa', 'hipotese', 'figurada') and any(p.get('faz') in ('atira', 'golpe') for p in e.get('passos') or []):
            R.append((i, f'sentido {e.get("sentido")} com tiro/golpe na tela: contradicao'))
    return R

def ficha(b, tempo_da_palavra=None):
    """Texto tecnico da encenacao para a folha 3 (o que a tela vai mostrar, passo a passo)."""
    e = b.get('encena')
    if not isinstance(e, dict): return []
    L = [f'- LEITURA DA FRASE: sentido {e.get("sentido", "?").upper()}' + (' (nada de tiro, explosao ou batalha na tela)' if e.get('sentido') in ('negativa', 'hipotese', 'figurada') else '')]
    who = b.get('who') or []
    for k, p in enumerate(e.get('passos') or [], 1):
        q = p.get('quem'); nome = str(who[q]).split(':')[0] if q is not None and q < len(who) else 'objeto'
        t = tempo_da_palavra(p.get('na')) if tempo_da_palavra and p.get('na') else None
        L.append(f'  {k}) {nome} {VOCAB.get(p.get("faz"), ("FALTA ANIMACAO",))[0]}' + (f' | alvo: {p["alvo"]}' if p.get('alvo') else '') + (f' | na palavra "{p["na"]}"' if p.get('na') else '') + (f' ({t:.1f}s)' if t is not None else ''))
    return L
