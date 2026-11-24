#!/usr/bin/env python3
# LISTA UNICA DE REVISAO (ordem do Gibson 24/11: "bateu o olho, faz a lista dos 10 pontos de uma vez; no maximo 1 refacao").
# Junta numa lista numerada TUDO o que as checagens automaticas acharam (folhas, coerencia, olhos/visibilidade, ficha x tela)
# e abre uma linha por frase para o revisor marcar o que viu. O revisor completa a lista INTEIRA antes de devolver;
# quem refaz corrige TODOS os itens de uma vez e responde item por item. Cada devolucao soma em stories/<id>/refacoes.txt.
# uso: python3 lista_revisao.py <id>   -> stories/<id>/lista_revisao.md
import json, os, re, sys, subprocess
i = sys.argv[1]; D = f'stories/{i}'; itens = []
fj = json.load(open(f'{D}/folhas.json')) if os.path.exists(f'{D}/folhas.json') else {}
f2 = open(f'{D}/folha2_producao.md', encoding='utf-8').read() if os.path.exists(f'{D}/folha2_producao.md') else ''
for m in re.finditer(r'^## Cena (b\d+).*?- RISCOS: (.*?)$', f2, re.S | re.M):
    if m.group(2).strip() not in ('nenhum', ''): itens.append(f'{m.group(1)}: risco da folha 2: {m.group(2).strip()[:200]}')
c = subprocess.run([sys.executable, 'checagem_coerencia.py', i], capture_output=True, text=True).stdout
itens += [l.strip(' -') for l in c.splitlines()[1:] if l.strip().startswith('-')]
if os.path.exists(f'{D}/visibilidade.json'):
    itens += json.load(open(f'{D}/visibilidade.json')).get('falhas', [])
n_ref = int(open(f'{D}/refacoes.txt').read().split()[0]) if os.path.exists(f'{D}/refacoes.txt') else 0
ph = json.load(open(f'{D}/work/phrases.json'))['phrases'] if os.path.exists(f'{D}/work/phrases.json') else []
L = [f'# LISTA UNICA DE REVISAO - {i}  (refacoes ate agora: {n_ref}; limite: 1)', '',
     'Regra: olhar o storyboard/frase_a_frase INTEIRO e completar esta lista toda ANTES de devolver. Quem refaz corrige todos os itens de uma vez.', '',
     '## Achados automaticos (ferramenta)'] + ([f'{n + 1}. {t}' for n, t in enumerate(itens)] or ['- nenhum']) + ['', '## Achados do olho (uma linha por frase: OK ou DEFEITO + o que fazer)']
L += [f'- f{k} "{p["text"][:60]}": ' for k, p in enumerate(ph)] or ['- (sem voz ainda: usar as cenas da folha 2)']
L += ['', '## Itens gerais conferidos (marque): gancho nos 5 s | virada no meio | final + COMENTE | 54-66 s | cenario/epoca | fardas | objeto heroi | legenda livre | ninguem cortado']
open(f'{D}/lista_revisao.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(f'LISTA DE REVISAO: {len(itens)} achado(s) automatico(s), {len(ph)} frase(s) para marcar -> {D}/lista_revisao.md (refacoes: {n_ref})')
