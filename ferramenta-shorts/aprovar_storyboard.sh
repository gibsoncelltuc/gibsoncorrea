#!/usr/bin/env bash
# APROVAR O STORYBOARD (obrigatorio antes do render, ordem do Gibson 19/11). So' rode DEPOIS de abrir e olhar stories/<id>/storyboard.jpg
# conferindo frase por frase com a folha 3 (cada acao acontecendo, ninguem cortado, cenario certo, objeto heroi visivel).
# EXIGE stories/<id>/revisao_storyboard.md (uma linha por frase, feita depois do storyboard atual).
# uso: ./aprovar_storyboard.sh <id>        (a aprovacao vale para ESTA versao das folhas; mudou o roteiro/ferramenta -> novo storyboard e nova aprovacao)
cd "$(dirname "$0")"; ID="${1:?id}"
[ -f stories/$ID/storyboard.jpg ] || { echo "sem storyboard: a fila gera sozinha (ou ./prechecar.sh $ID && cp stories/$ID/precheck.jpg stories/$ID/storyboard.jpg)"; exit 1; }
python3 verificar_folhas.py $ID || exit 1
H=$(python3 -c "import json;print(json.load(open('stories/$ID/folhas.json'))['hash_producao'])")
[ "$(cat stories/$ID/storyboard.hash 2>/dev/null)" = "$H" ] || { echo "o storyboard e' de uma versao ANTIGA das folhas: gere de novo (rm stories/$ID/storyboard.jpg e relance a fila)"; exit 1; }
python3 - "$ID" <<'PYR' || exit 1
# REVISAO ESCRITA OBRIGATORIA (ordem do Gibson 19/11: toda sessao revisa e corrige como a principal). stories/<id>/revisao_storyboard.md,
# feita DEPOIS do storyboard atual, com UMA linha por frase: "bN: OK - <o que aparece na tela nessa frase>" ou "bN: CORRIGIDO - <defeito> -> <correcao>".
# Cada linha precisa citar algo da propria frase (palavra da narracao) e ter 8+ palavras: aprovar "no olho" sem comparar frase por frase nao passa.
import json, os, re, sys, unicodedata
i = sys.argv[1]; R = f'stories/{i}/revisao_storyboard.md'; SB = f'stories/{i}/storyboard.jpg'
n = lambda t: unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode()
if not os.path.exists(R) or os.path.getmtime(R) < os.path.getmtime(SB):
    print(f'FALTA A REVISAO ESCRITA: abra {SB}, compare frase por frase com stories/{i}/folha3_acao.md e escreva {R} (uma linha por frase: "bN: OK - o que aparece" ou "bN: CORRIGIDO - defeito -> correcao"). Achou defeito? CORRIJA antes (regra mestra).'); sys.exit(1)
B = json.load(open(f'videos/{i}/beats.json'))['beats']; L = {}
for ln in open(R):
    m = re.match(r'\s*[-*]?\s*b(\d+)\s*[:\-]\s*(.+)', ln)
    if m: L[int(m.group(1))] = m.group(2)
falta = []
for k, b in enumerate(B):
    t = L.get(k)
    if not t: falta.append(f'b{k}: sem linha'); continue
    pal = {w for w in re.findall(r'[a-z]{5,}', n(b['say']))}
    if len(t.split()) < 8 or not (pal & set(re.findall(r'[a-z]{5,}', n(t)))): falta.append(f'b{k}: linha curta ou sem citar nada da frase')
    elif re.search(r'pendente|a corrigir|vou corrigir|defeito(?!.*->)', n(t)) and 'corrigido' not in n(t): falta.append(f'b{k}: defeito sem correcao (regra mestra: corrija antes de aprovar)')
if falta: print('REVISAO INCOMPLETA:', '; '.join(falta[:8])); sys.exit(1)
print(f'revisao escrita OK ({len(B)} frases conferidas)')
PYR
echo "$H" > stories/$ID/STORYBOARD_OK; rm -f stories/$ID/AGUARDA_STORYBOARD; echo "STORYBOARD APROVADO: $ID ($H). A fila renderiza na proxima volta."
