#!/usr/bin/env python3
"""PORTÃO DE ENTREGA (2 etapas). NENHUM vídeo — nem piloto de 5 s — é mostrado/enviado sem `GATE OK` para o MESMO arquivo (hash).
  Etapa A — quadro a quadro (tools/frame_gate.py): todo PNG precisa estar CONCLUÍDO (aprovado); reprovados são refeitos SÓ eles (tools/repair_frames.py).
  Etapa B — vídeo montado: qa.py (17) + qa_extra.py (4) + qa_more.py (15) + legibility_check.py (10) + fidelidade vs referência (7 métricas) = 53 checagens.
Uso: python3 tools/gate.py <video.mp4> <WxH@fps> [pasta_referencia] [--skip-frames]      |      python3 tools/gate.py --verify <video.mp4>   (confere o selo antes de enviar)"""
import hashlib, json, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R); TOK = 'qa/GATE_PASSED.json'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
if sys.argv[1] == '--verify':
    ok = os.path.exists(TOK) and json.load(open(TOK)).get('sha') == sha(sys.argv[2]); print('GATE OK (selo confere)' if ok else 'GATE AUSENTE/DESATUALIZADO — não enviar'); sys.exit(0 if ok else 2)
v, spec = sys.argv[1], sys.argv[2]; ref = next((a for a in sys.argv[3:] if not a.startswith('--')), os.environ.get('REF_DIR', '')); bad = []; n_checks = 0
if os.path.exists(TOK): os.remove(TOK)
def run(cmd): return subprocess.run([sys.executable, *cmd], capture_output=True, text=True).stdout
if '--skip-frames' not in sys.argv and os.path.isdir('blender/out/frames'):
    o = run(['tools/frame_gate.py']); m = re.search(r'quadros concluídos: (\d+)/(\d+)', o); print('A) quadro a quadro:', m.group(0) if m else '(sem quadros)'); bad += [l for l in o.splitlines() if l.startswith('FAIL')]; n_checks += int(m.group(2)) if m else 0
for name, cmd in (('qa.py (17)', ['tools/qa.py', v, 'gate', spec]), ('qa_extra.py (4)', ['tools/qa_extra.py', v, 'gate_extra']), ('qa_more.py (15)', ['tools/qa_more.py', v]), ('legibility_check.py (10)', ['tools/legibility_check.py', v])):
    o = run(cmd); p = sum(l.startswith('PASS') for l in o.splitlines()); f = [l for l in o.splitlines() if l.startswith('FAIL')]; print(f'B) {name}: {p}/{p + len(f)}'); bad += f
if ref and os.path.isdir(ref):
    o = run(['tools/fidelity_report.py', v, ref]); k = 0
    for l in o.splitlines():
        m = re.match(r'\|\s*(\w+)\s*\|.*\|\s*([\d.]+)\s*\|$', l)
        if m: k += 1; bad += [] if .75 <= float(m.group(2)) <= 1.3 else [f'FAIL fidelidade {m.group(1)} = {m.group(2)}× a referência (faixa 0,75–1,30)']
    print(f'B) fidelidade vs referência: {k - sum(1 for b in bad if "fidelidade" in b)}/{k}')
else: bad.append('FAIL sem pasta de referência: fidelidade NÃO medida (defina REF_DIR)')
for b in bad[:40]: print(b[:230])
if bad: print(f'GATE REPROVADO: {len(bad)} falhas — corrigir (tools/repair_frames.py para quadros; refazer montagem) e rodar de novo'); sys.exit(1)
json.dump(dict(video=v, sha=sha(v), data=__import__('datetime').datetime.now().isoformat(timespec='seconds')), open(TOK, 'w')); print('GATE OK'); sys.exit(0)
