# V5 — leia primeiro (para a sessão nova no notebook) — 2026-11-16
Usuário (Gibson) fala português; respostas curtas, honestas, tudo em português. Também leia `LEIA-PRIMEIRO_V4_OTIMIZACAO.md` (otimização + retomada), `RELATORIO_E_PLANO.md`, `SKILL.md`.

## Estado
- **Karansebes v2**: PRONTO e APROVADO pelo usuário ("ficou bom"). Voz neural `pt-BR-AntonioNeural` (escolhida pelo usuário). 62 s, 1080x1920.
- **Emus (id `emus1932`)**: em produção na sessão da nuvem (`bash status.sh`; log `logs/make_emus1932.log`). Roteiro novo em `videos/emus1932/beats.json`, formato novo com diretor, bando de emus (`"emus": {"n","mode":"stand|run|scatter","x","z","cols","dir"}`). Ponto fraco: emus escuros em alguns planos (de costas/contraluz) — se o usuário reclamar, refazer só esses planos (ajustar cor em `blender/make_emu.py` ou luz).
- **Emu 3D novo**: `blender/make_emu.py` (`blender -b --python blender/make_emu.py` → `web/assets/emu.glb`). Animação por nomes de nós em `web/core.js` (body, neckp, head, legL/R, shinL/R).
- Fila: `queue.txt`. Próximos a refazer (pedido do usuário, ainda sem lista de ajustes dele): Balões, Balde, Onoda; planos de correção em `RELATORIO_E_PLANO.md`. Perguntar quais mudanças.

## Como rodar (qualquer máquina com Linux/WSL/Git Bash, Python 3.10+, Node 20+, ffmpeg, Chromium via Playwright)
`bash setup.sh` → editar `queue.txt` → `bash run_queue.sh` (retomável) · `bash status.sh` · `bash boot.sh` (hook de sessão).
Desempenho medido na nuvem (4 núcleos, sem GPU): ~50-65 min por vídeo de ~1900 quadros. Em PC de 2 núcleos será bem mais lento — preferir a nuvem.
**Nuvem**: ambiente `gibsoncorrea-shorts` (hosts liberados: speech.platform.bing.com, huggingface.co + CDNs hf). Branch de trabalho: `claude/bold-sagan-dskrsj` (repo gibsoncelltuc/gibsoncorrea, pasta `ferramenta-shorts/`). Trechos do render são salvos no git (`ckpt/<id>/`).
Windows: ver `LEIA-PRIMEIRO_HANDOFF_2026-11-16.md` (shim python3, caminhos).

## Voz
- Padrão: `edge-tts` (Microsoft) — precisa de acesso a speech.platform.bing.com; sem ele cai em espeak (voz de teste robótica, cria `stories/<id>/VOICE_PLACEHOLDER`).
- Alternativa open source: VoiceStudio/OmniVoice (Apache-2.0 no modelo; app AGPL-3.0). Instalado em venv `/tmp/ovenv` (`pip install omnivoice`), CPU ~5x mais lento que tempo real; clonagem exige 5-15 s de áudio do usuário + texto exato. Ainda NÃO ligado ao `produce_voice.sh`.

## Regras do usuário
Verificar quadros (folha de contato) antes de entregar; nunca afrouxar o gate de estilo; enviar arquivos prontos de imediato; sem chaves/pagamentos feitos por mim; só licença comercial.
## Ideia do usuário (biblioteca de personagens prontos/sprites)
Boa para consistência entre vídeos, mas NÃO acelera o render hoje (medido: cartas de ator já não pesam após a resolução adaptativa). Oferecer como trabalho futuro (catálogo: padeiro, piloto, soldado, general...).
