#!/usr/bin/env python3
"""PORTÃO DE ENTREGA: nenhum vídeo é mostrado/enviado sem passar aqui. Roda qa.py + qa_extra.py + fidelidade vs referência (se houver) e imprime os quadros-chave para olhar.
Código de saída ≠ 0 se qualquer checagem falhar. Uso: python3 tools/gate.py <video.mp4> <WxH@fps> [pasta_referencia]"""
import subprocess, sys, re
v, spec = sys.argv[1], sys.argv[2]; ref = sys.argv[3] if len(sys.argv) > 3 else ''
bad = []
for cmd in (['tools/qa.py', v, 'gate', spec], ['tools/qa_extra.py', v, 'gate_extra']):
    o = subprocess.run([sys.executable, *cmd], capture_output=True, text=True).stdout; bad += [l for l in o.splitlines() if l.startswith('FAIL')]
if ref:
    o = subprocess.run([sys.executable, 'tools/fidelity_report.py', v, ref], capture_output=True, text=True).stdout
    for l in o.splitlines():
        m = re.match(r'\|\s*(\w+)\s*\|.*\|\s*([\d.]+)\s*\|$', l)
        if m and not (0.75 <= float(m.group(2)) <= 1.3): bad.append(f'FAIL fidelidade {m.group(1)} fora de 0,75–1,30× a referência ({m.group(2)})')
print('\n'.join(bad) or 'PORTÃO OK'); sys.exit(1 if bad else 0)
