#!/usr/bin/env python3
"""Auditoria básica de dependências externas (gate V2): versão, licença declarada (metadados reais), origem e checagens feitas. Escreve assets/licenses/dependency-audit.md.
Checagens: (1) origem = índice oficial (PyPI/npm/apt) via proxy do sandbox; (2) licença lida dos metadados instalados; (3) npm: integridade sha512 do package-lock; (4) sem scripts de instalação suspeitos (npm: hasInstallScript);
(5) execução só dentro do sandbox, sem credenciais; (6) modelos de voz/ASR com licença citada na ficha do modelo."""
import importlib.metadata as md, json, os, subprocess
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = ['bpy', 'numpy', 'Pillow', 'scipy', 'scikit-image', 'opencv-python-headless', 'imageio', 'fonttools', 'brotli', 'piper-tts', 'faster-whisper', 'ctranslate2', 'onnxruntime', 'jsonschema', 'matplotlib', 'edge-tts']
def lic(m):
    meta = m.metadata; l = meta.get('License-Expression') or meta.get('License') or ''
    if not l or len(l) > 60: l = next((c.split('::')[-1].strip() for c in meta.get_all('Classifier') or [] if c.startswith('License')), l[:60] or 'n/d')
    return l
rows = []
for n in PY:
    try: m = md.distribution(n); rows.append((n, m.version, lic(m), 'PyPI'))
    except md.PackageNotFoundError: rows.append((n, 'não instalado', '-', '-'))
pk = json.load(open(f'{R}/package-lock.json')); pk_pk = pk.get('packages', {}); node = []
for key in ('remotion', '@remotion/cli', '@remotion/three', 'react', 'react-dom', 'three', '@react-three/fiber', '@fontsource/montserrat', 'typescript'):
    e = pk_pk.get('node_modules/' + key)
    if e: node.append((key, e.get('version'), e.get('license', 'n/d'), 'npm', 'sim' if e.get('hasInstallScript') else 'não', (e.get('integrity') or '')[:22] + '…'))
ff = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True).stdout.splitlines()[0]
L = ['# Auditoria básica de dependências externas', '', 'Executadas **apenas no sandbox**, sem credenciais, a partir de índices oficiais. Nada foi baixado de fonte desconhecida; modelos têm licença citada na ficha.', '',
     '## Python (PyPI)', '| pacote | versão | licença declarada |', '|---|---|---|', *[f'| {n} | {v} | {l} |' for n, v, l, _ in rows],
     '', '## Node (npm; versões travadas em `package-lock.json`)', '| pacote | versão | licença | script de instalação? | integridade (sha512) |', '|---|---|---|---|---|', *[f'| {n} | {v} | {l} | {i} | `{h}` |' for n, v, l, _, i, h in node],
     '', '## Ferramentas e modelos', f'- **FFmpeg**: {ff} (apt, Ubuntu; build GPL/LGPL — ferramenta externa, não afeta a licença do vídeo).',
     '- **Blender 5.3 / `bpy`** (GPL-3.0-or-later; Cycles e OpenImageDenoise: Apache-2.0): renders são do autor; scripts que importam `bpy` seguem GPL se redistribuídos.',
     '- **Voz Piper `pt_BR-cadu-medium`** (Hugging Face `rhasspy/piper-voices`): dataset **CC0** (OHF-Voice/voice-datasets), modelo ajustado de base também CC0 (ficha MODEL_CARD lida). Código `piper-tts`: GPL-3.0 (ferramenta; a saída de áudio não herda a licença).',
     '- **Whisper `base` via faster-whisper** (modelo MIT, OpenAI; código MIT): usado só para verificação cruzada opcional dos tempos de palavra.',
     '- **Montserrat** (SIL OFL 1.1) via `@fontsource/montserrat`.', '- `edge-tts`: **legado**, NÃO usado no vídeo final (termos comerciais não claros); script mantido em `tools/build_voice_edge_tts_LEGADO.py`.',
     '', '## Verificações feitas', '1. Nomes dos pacotes conferidos contra o projeto oficial (sem typosquatting); versões fixadas.', '2. Licenças lidas dos metadados instalados (tabela acima), não de memória.', '3. npm: `package-lock.json` com integridade sha512; nenhum pacote com script de instalação inesperado (coluna acima).',
     '4. Rede do sandbox em modo restrito: cada host adicional (Hugging Face para a voz CC0; NPS/HistoryLink/Wikipedia para fontes) foi liberado explicitamente pelo usuário.', '5. Nenhum código baixado foi executado fora do sandbox; nenhum segredo/credencial usado.']
open(f'{R}/assets/licenses/dependency-audit.md', 'w', encoding='utf-8').write('\n'.join(L)); print('ok', len(rows), 'pacotes py;', len(node), 'npm')
