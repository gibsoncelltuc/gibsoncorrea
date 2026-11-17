#!/usr/bin/env python3
"""roteiro_check.py <id> -- confere o roteiro (videos/<id>/beats.json) contra as regras medidas do MODO RICKS. So' avisa; nao bloqueia."""
import json, re, sys
B = json.load(open(f'videos/{sys.argv[1]}/beats.json')); says = [b['say'] for b in B['beats']]; txt = ' '.join(says)
sent = [s.strip() for s in re.split(r'(?<=[.!?])\s+', txt) if s.strip()]; words = len(txt.split()); av = []
first = sent[0]; nf = len(first.split())
if re.match(r'^(Em|No ano|Há|Na década)\b.*\d|^Em mil', first): av.append('GANCHO: comeca por data/contexto. Abra com o paradoxo ou a acao absurda como fato.')
if nf > 16: av.append(f'GANCHO: {nf} palavras (alvo 10-16).')
if not 150 <= words <= 200: av.append(f'TAMANHO: {words} palavras (alvo 150-200 para 55-70 s na voz +10%).')
if not re.search(r'["“”]', txt): av.append('FALAS: nenhuma fala de personagem entre aspas (canal: 1-2 por video).')
mw = sum(len(s.split()) for s in sent) / len(sent)
if mw > 17: av.append(f'FRASES: media de {mw:.0f} palavras (alvo ~14).')
if len(sent[-1].split()) > 14: av.append(f'FINAL: ultima frase com {len(sent[-1].split())} palavras (alvo curta, ironica, <= 12).')
if not re.search(r'\b(acontece que|é que|o segredo|na verdade|só que|mas havia|o problema)\b', txt.lower()): av.append('VIRADA: nao achei frase de virada/explicacao ("Acontece que...", "Na verdade...").')
print(f'{sys.argv[1]}: {words} palavras, {len(sent)} frases, gancho de {nf} palavras'); print('\n'.join('  AVISO ' + a for a in av) if av else '  OK: dentro das regras')
