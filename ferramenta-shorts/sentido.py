# SENTIDO DA FRASE (24/11, pedido do Gibson: "um script que resolva a questao do sentido").
# A ferramenta lia PALAVRA por palavra: "o tiro nunca veio" virava explosao, "pediram metralhadoras" virava tiro,
# "misturou as etiquetas" virava panela, "o preco de uma casa" virava cena dentro de casa.
# Este modulo le a FRASE INTEIRA e devolve:
#   figurado(say) -> indices das palavras que NAO devem ser encenadas (negadas, figuradas, so' citadas, hipoteticas)
#   cena(say)     -> flags da cena: sem_violencia (nada de tiro/explosao/batalha), nao_interior, nao_cozinha
#   explicar(say) -> lista de frases curtas dizendo o que foi entendido (vai para a folha 2, para quem revisa)
# Regra geral: verbo de ACAO REAL so' vale se nao estiver negado, no futuro/condicional/desejo, numa comparacao
# ou numa expressao figurada. Substantivo de arma so' vira tiro com VERBO de disparo na mesma frase.
import re, unicodedata

def _n(t):
    return unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode()

def _w(t):
    return re.sub(r'[^a-z]', '', _n(t))

ARMA = r'^(metralhadoras?|balas?|canhoes|canhao|bombas?|fuzis|fuzil|armas?|municao|misseis|missil|artilharia|cartuchos?|tiros?|mosquetes?|granadas?|torpedos?|disparos?|polvora)$'
DISPARO = r'\b(atir\w*|dispar\w*|abri\w* fogo|bombarde\w*|explod\w*|explos\w*|acert\w*|ating\w*|fuzil(ou|aram)|metralh(ou|aram|ava)|lanc\w* (os |uns |dois |tres )?(misseis|missil|bombas?|torpedos?|granadas?)|bombas? ca\w*|ca\w* (as |uma |duas |catorze |doze )?bombas?|fogo cruzado|tiroteio|balear\w*|mat\w*|feri\w*|derrub\w* (o |os |um |uns )?(aviao|avioes|navio))'
VIOLENTO = r'^(atirou|atiraram|atirava|atiravam|atirar|disparou|dispararam|disparar|explodiu|explodiram|explodir|bombardeou|bombardearam|atacou|atacaram|atacar|matou|mataram|lutou|lutaram|brigou|brigaram|guerra|batalha|tiro|tiros|bomba|bombas|explosao|canhao|canhoes|metralhadora|metralhadoras|balas?|fogo|invadiu|invadiram|combate|combateram)$'
NEG_ANTES = r'^(nao|nunca|jamais|nem|sem|ninguem|nenhum|nenhuma)$'
HIPOTESE = r'^(quase|queria|queriam|ameacou|ameacaram|ameacava|planejou|planejaram|pensou|pensaram|tentou\s*evitar|evitou|evitaram|temia|temiam|poderia|poderiam|iria|iriam|preferiu|prefeririam|pediu|pediram|pedia|pediam|exigiu|exigiram|prometeu|prometeram|sonhava|imaginou)$'
VEIO = r'^(veio|vieram|chegou|chegaram|aconteceu|aconteceram|houve|saiu|foi|foram|apareceu|existiu|disparado|disparada|usado|usada|dado)$'
VALOR = r'^(preco|precos|valor|custo|custava|custou|custa|valia|vale|valiam|trocou|trocaram|troca|trocava|vendeu|venderam|vendia|comprou|compraram|comprava|pagou|pagaram|pagava|dava|equivalia|equivale)$'
BEM = r'^(casa|casas|carro|carros|fortuna|terra|terras|ouro|navio|navios|cavalo|cavalos|fazenda|mansao|palacio|predio|ilha)$'
PAPEL = r'^(etiquetas?|papel|papeis|cartas?|nomes?|fichas?|dados|numeros?|arquivos?|documentos?|fotos?|ideias?|cores|rotulos?|registros?|anotacoes)$'
MISTURA = r'^(misturou|misturaram|misturava|misturavam|trocou|trocaram|confundiu|confundiram|embaralhou|embaralharam|mexeu|mexeram)$'
EXPLODE_FIG = r'(explod\w* (de |em |as |a )(rir|riso|alegria|raiva|popularidade|vendas|audiencia|sucesso|fama)|explod\w* nas? (redes|internet|vendas|paradas)|bomba (de |na )?(noticia|internet|midia|imprensa)|a bomba (foi|era) a noticia)'
FIG = [   # (regex na frase normalizada, palavras afetadas) -> expressoes que NAO sao acao fisica
    (r'\b(bat\w*|quebr\w*) (o |um |todos os |varios )?recordes?\b', r'^(bateu|bateram|quebrou|quebraram|batia)$'),
    (r'\bca\w* na risada\b', r'^(caiu|cairam)$'),
    (r'\bmat\w* a (charada|saudade|fome|sede|curiosidade)\b', r'^(matou|mataram|matar)$'),
    (r'\b(guerra|batalha|briga|luta) (de precos|fria|de nervos|comercial|judicial|na justica|de egos|contra a (doenca|fome|pobreza))\b', r'^(guerra|batalha|briga|luta)$'),
    (r'\b(chuva|onda|enxurrada) de (criticas|comentarios|pedidos|cartas|reclamacoes|mensagens)\b', r'^(chuva|onda|enxurrada)$'),
    (r'\bfoi (um )?tiro (no pe|certeiro)\b', r'^(tiro)$'),
    (r'\batir\w* para (todo lado|todos os lados)\b', r'^(atirou|atiraram)$'),
    (r'\b(fogo|chamas) (da paixao|nos olhos)\b', r'^(fogo|chamas)$'),
]

def figurado(say):
    ws = say.split(); nw = [_w(x) for x in ws]; frase = _n(say); out = set()
    tem_disparo = bool(re.search(DISPARO, frase))
    for j, w in enumerate(nw):
        if re.match(ARMA, w) and not tem_disparo: out.add(j)                                   # "pediram metralhadoras", "levou dez mil balas"
        if re.match(NEG_ANTES, w): out.update(k for k in range(j + 1, min(len(nw), j + 6)) if re.match(VIOLENTO, nw[k]) or re.match(ARMA, nw[k]))
        if w in ('nunca', 'jamais', 'nao') and j + 1 < len(nw) and re.match(VEIO, nw[j + 1]): out.update(range(max(0, j - 4), j))   # "o tiro nunca veio"
        if re.match(HIPOTESE, w): out.update(k for k in range(j + 1, min(len(nw), j + 6)) if re.match(VIOLENTO, nw[k]) or re.match(ARMA, nw[k]))   # "quase entraram em guerra", "ameacou atacar"
        if re.match(VALOR, w): out.update(k for k in range(j + 1, min(len(nw), j + 6)) if re.match(BEM, nw[k]))   # "o preco de uma casa"
        if re.match(MISTURA, w) and any(re.match(PAPEL, nw[k]) for k in range(j + 1, min(len(nw), j + 4))): out.add(j)   # "misturou as etiquetas"
    if re.search(EXPLODE_FIG, frase): out.update(j for j, w in enumerate(nw) if re.match(r'^(explodiu|explodiram|explodir|bomba)$', w))
    for rx, rxw in FIG:
        if re.search(rx, frase): out.update(j for j, w in enumerate(nw) if re.match(rxw, w))
    return out

def cena(say):
    ws = say.split(); nw = [_w(x) for x in ws]; fig = figurado(say); frase = _n(say)
    viol = [j for j, w in enumerate(nw) if re.match(VIOLENTO, w) or re.match(ARMA, w)]
    f = {}
    if viol and all(j in fig for j in viol): f['sem_violencia'] = True                       # toda a violencia da frase e' negada/figurada/hipotetica
    if any(j in fig and re.match(BEM, nw[j]) and nw[j].startswith('casa') for j in range(len(nw))): f['nao_interior'] = True
    if any(j in fig and re.match(MISTURA, nw[j]) for j in range(len(nw))): f['nao_cozinha'] = True
    return f

def explicar(say):
    ws = say.split(); fig = sorted(figurado(say)); f = cena(say); out = []
    if fig: out.append('nao encenar: ' + ', '.join(ws[j].strip('.,!?":;') for j in fig))
    if f.get('sem_violencia'): out.append('frase sem violencia de verdade (negada, so citada ou hipotetica): sem tiro, explosao ou batalha')
    if f.get('nao_interior'): out.append('"casa" aqui e\' valor, nao lugar: a cena nao vai para dentro de casa')
    if f.get('nao_cozinha'): out.append('"misturar" aqui e\' de papeis/dados, nao de comida: sem panela')
    return out

if __name__ == '__main__':
    import sys
    for s in sys.argv[1:]: print(s, '->', explicar(s))
