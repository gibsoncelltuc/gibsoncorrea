#!/usr/bin/env python3
"""research/fact-check.md a partir de research/claims.json (fonte única da verdade; validate_schemas.py confere que cada trecho é literal nas fontes salvas)."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); d = json.load(open(f'{R}/research/claims.json', encoding='utf-8'))
n_src = lambda c: len({f['fonte'] for f in c['fontes']})
L = [f"# Checagem de fatos — {d['projeto']}", f"**Data:** {d['data_da_checagem']} · **Regra:** {d['regra']}", '',
     f"**Resumo:** {len(d['afirmacoes'])} afirmações centrais · mínimo de fontes por afirmação: {min(n_src(c) for c in d['afirmacoes'])} · citações literais verificadas contra o texto salvo das fontes (`tools/validate_schemas.py`) · "
     f"confiança: " + ', '.join(f"{k} {sum(1 for c in d['afirmacoes'] if c['confianca'] == k)}" for k in ('alta', 'média-alta', 'média', 'baixa')), '',
     '| # | Fala do roteiro | Afirmação checada | Fontes (trechos literais abaixo) | Confiança | Observação |', '|---|---|---|---|---|---|']
for c in d['afirmacoes']: L.append(f"| {c['id']} | {c['fala']} | {c['afirmacao']} | {', '.join(f['fonte'] for f in c['fontes'])} | {c['confianca']} | {c.get('nota', '')} |")
L += ['', '## Trechos literais (inglês, como nas fontes)']
for c in d['afirmacoes']:
    L.append(f"- **{c['id']}** — {c['afirmacao']}")
    for f in c['fontes']: L.append(f"  - {f['fonte']}: “{f['trecho']}” — <{f['url']}>")
L += ['', '## Fontes'] + [f"- **{k}** — [{v['title']}]({v['url']}) — {v['tipo']}; acesso em {v['acesso']}; {'lida' if v['lido'] else 'NÃO lida'}." for k, v in d['fontes'].items()]
L += ['', '## Limitações'] + [f'- {x}' for x in d['limitacoes']]
L += ['', '## Regras editoriais', '- Ficção marcada: personagens, rostos, uniformes e navios são **genéricos e dramatizados**; nenhuma fala é atribuída a pessoa real (só narração).',
      '- Números usados sem cifras exatas quando as fontes divergem ("centenas"); o numeral "cinco navios" tem fonte única (ver C09).']
open(f'{R}/research/fact-check.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('ok', len(d['afirmacoes']), 'afirmações')
