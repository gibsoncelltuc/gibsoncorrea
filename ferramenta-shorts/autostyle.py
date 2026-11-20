#!/usr/bin/env python3
"""autostyle.py <id> -- AUTOAJUSTE DE ESTILO: roda o teste de estilo e corrige sozinho (ate 6 rodadas) editando videos/<id>/beats.json:
 luminancia alta -> exp menor | escuro/detalhe/contorno baixos -> exp maior, cinf menor (menos desfoque), 'night'->'dusk' | pouco colorido -> troca luz para 'golden'.
Sai com codigo 0 se STYLE OK."""
import json, subprocess, sys, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__))); ID = sys.argv[1]; F = f'videos/{ID}/beats.json'
for it in range(6):
    subprocess.run([sys.executable, 'mkvideo.py', ID], capture_output=True); subprocess.run(['bash', './build3.sh', ID], capture_output=True)
    out = subprocess.run(['bash', './qa_style.sh', ID], capture_output=True, text=True).stdout; print(f'rodada {it}:', ' '.join(re.findall(r'(\w+)\s+[\d.]+\s+target[^\n]*FAIL', out)) or 'ok', flush=True)
    if 'STYLE OK' in out: sys.exit(0)
    B = json.load(open(F)); fails = set(re.findall(r'(\w+)\s+[\d.]+\s+target[^\n]*FAIL', out))
    exp = B.get('exp', 1.0)
    if 'lum_mean' in fails and re.search(r'lum_mean\s+(0\.[6-9]\d*)', out): exp *= 0.9
    elif fails & {'detail', 'edges', 'lum_std', 'dark'}: exp *= 1.12; B['cinf'] = max(1.5, B.get('cinf', 6) - 1.5)
    if fails & {'detail', 'edges', 'sat', 'colorful'}:
        for b in B['beats']:
            if b.get('light', B.get('light')) == 'night': b['light'] = 'dusk'
        if B.get('light') == 'night': B['light'] = 'dusk'
    if 'colorful' in fails or 'sat' in fails: B['light'] = 'golden' if B.get('light') in ('day', 'noon', 'overcast') else B.get('light')
    B['exp'] = round(exp, 3); json.dump(B, open(F, 'w'), ensure_ascii=False, indent=1)
print('STYLE nao convergiu: revisar manualmente'); sys.exit(1)
