# Auditoria básica de dependências externas

Executadas **apenas no sandbox**, sem credenciais, a partir de índices oficiais. Nada foi baixado de fonte desconhecida; modelos têm licença citada na ficha.

## Python (PyPI)
| pacote | versão | licença declarada |
|---|---|---|
| bpy | 5.3.0 | GPL-3.0 |
| numpy | 2.5.3 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 |
| Pillow | 12.3.0 | MIT-CMU |
| scipy | 1.18.1 | BSD License |
| scikit-image | 0.26.0 | BSD License |
| opencv-python-headless | 5.0.0.93 | Apache 2.0 |
| imageio | 2.38.1 | BSD-2-Clause |
| fonttools | 4.68.0 | MIT |
| brotli | 1.2.1 | MIT |
| piper-tts | 1.8.0 | GPL-3.0-or-later |
| faster-whisper | 1.2.1 | MIT |
| ctranslate2 | 4.9.0 | MIT |
| onnxruntime | 1.29.0 | MIT License |
| jsonschema | 4.26.0 | MIT |
| matplotlib | 3.11.2 | Python Software Foundation License |
| edge-tts | 7.3.1 | GNU Lesser General Public License v3 (LGPLv3) |

## Node (npm; versões travadas em `package-lock.json`)
| pacote | versão | licença | script de instalação? | integridade (sha512) |
|---|---|---|---|---|
| remotion | 4.0.543 | SEE LICENSE IN LICENSE.md | não | `sha512-p3PS2+ZsaFBp1Ki…` |
| @remotion/cli | 4.0.543 | SEE LICENSE IN LICENSE.md | não | `sha512-pDc+pUIAuhoaQN8…` |
| @remotion/three | 4.0.543 | MIT | não | `sha512-GKJakNFB34PLG7f…` |
| react | 19.3.1 | MIT | não | `sha512-QNhWdt7nrgVWWQG…` |
| react-dom | 19.3.1 | MIT | não | `sha512-Y0bARz53lhEC1NM…` |
| three | 0.187.0 | MIT | não | `sha512-Qiu7R+Cmh8CstZs…` |
| @react-three/fiber | 9.8.2 | MIT | não | `sha512-6s0ejw0bT1myQ/a…` |
| @fontsource/montserrat | 5.3.0 | OFL-1.1 | não | `sha512-iQPDtZOnmM5ih4J…` |
| typescript | 7.0.2 | Apache-2.0 | não | `sha512-8FYau96o3NKOhbj…` |

## Ferramentas e modelos
- **FFmpeg**: ffmpeg version 6.1.1-3ubuntu5 Copyright (c) 2000-2023 the FFmpeg developers (apt, Ubuntu; build GPL/LGPL — ferramenta externa, não afeta a licença do vídeo).
- **Blender 5.3 / `bpy`** (GPL-3.0-or-later; Cycles e OpenImageDenoise: Apache-2.0): renders são do autor; scripts que importam `bpy` seguem GPL se redistribuídos.
- **Voz Piper `pt_BR-cadu-medium`** (Hugging Face `rhasspy/piper-voices`): dataset **CC0** (OHF-Voice/voice-datasets), modelo ajustado de base também CC0 (ficha MODEL_CARD lida). Código `piper-tts`: GPL-3.0 (ferramenta; a saída de áudio não herda a licença).
- **Whisper `base` via faster-whisper** (modelo MIT, OpenAI; código MIT): usado só para verificação cruzada opcional dos tempos de palavra.
- **Montserrat** (SIL OFL 1.1) via `@fontsource/montserrat`.
- `edge-tts`: **legado**, NÃO usado no vídeo final (termos comerciais não claros); script mantido em `tools/build_voice_edge_tts_LEGADO.py`.

## Verificações feitas
1. Nomes dos pacotes conferidos contra o projeto oficial (sem typosquatting); versões fixadas.
2. Licenças lidas dos metadados instalados (tabela acima), não de memória.
3. npm: `package-lock.json` com integridade sha512; nenhum pacote com script de instalação inesperado (coluna acima).
4. Rede do sandbox em modo restrito: cada host adicional (Hugging Face para a voz CC0; NPS/HistoryLink/Wikipedia para fontes) foi liberado explicitamente pelo usuário.
5. Nenhum código baixado foi executado fora do sandbox; nenhum segredo/credencial usado.