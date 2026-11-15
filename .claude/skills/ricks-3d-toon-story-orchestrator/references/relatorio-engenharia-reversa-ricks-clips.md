# Relatório de engenharia reversa (texto enviado pelo usuário, 15/11/2026) — incorporado com diagnóstico

Origem: relatório "Do Estilo à Skill: um guia técnico para replicar programaticamente o universo visual de Rick's Clips 3000" (pesquisa secundária com citações numeradas). O texto integral foi recebido na conversa; aqui ficam as ideias aproveitadas e o que foi REJEITADO por contradizer medições feitas nos quadros reais.

## Aproveitado (e onde já está implementado)
- **Pipeline TTS → timestamps de palavra → JSON de linha do tempo → orquestrador → render → FFmpeg**: já existe (`tools/build_voice.py` → `word-timings.json` → `storyboard/edl.json` → render → `tools/montage.sh`).
- **Estrutura de 5 blocos** (gancho 8–15 palavras, promessa, contexto, pagamento em micro-pagamentos de ~8–10 s, fechamento 10–20 palavras) e checagem de gancho 9–14 palavras (`qa.py`).
- **Música −18 a −26 dB abaixo da voz, SFX em palavras-chave, ducking** (`mix.py`: −13,5 dB de ducking, música −21 dB).
- **Legendas palavra a palavra com pop**, sem pontuação final nos prints? NÃO: nos prints do canal a pontuação aparece (medido).
- **Remotion como orquestrador** (useCurrentFrame, interpolate) e **FFmpeg para pós** (CRF 18–23).
- Ideia nova adotada: **modelagem 3D só como produtor de ativos** (cenário/objetos exportados em glTF) e **render rápido em Three.js/Remotion** — ver `stack-remotion-threejs-blender.md` (rota híbrida).

## Rejeitado / corrigido (contradiz as medições nos quadros reais)
- **Paleta `#b2daed #d5c8b8 #9fded5 #70592d #303032` e estética "analog horror / VHS"**: vem de uma página de paleta de terceiros; os quadros reais do canal são 3D cartoon saturado (céu azul, grama dourada, sombras roxas). Medido: saturação média 0,45, tinta ≈ RGB(33,22,35). Não usar VHS/glitch.
- **"Figuras de palito, cenário rudimentar"**: os prints mostram cenário cheio, texturas pintadas e multidões de personagens reais.
- **"~6 cortes/minuto"**: os prints têm um plano a cada ~2–2,7 s (≈ 25 cortes/min) — o piloto usa 1,75–1,85 s.
- **Fontes/tamanhos de legenda genéricos** (36–44 px, stroke 4–6): medido no canal: ascendente ≈ 5,4 % da altura, linha de base a 72,7 %, Montserrat 800 com contorno ameixa (`visual-reference-ricks-clips.md`).
- "Blender é complexo demais": para ESTE estilo o Blender é a melhor ferramenta de modelagem de cenário/objetos (texturas pintadas por código); o problema é só usá-lo como renderizador (lento em CPU).

## Lacunas do relatório (não resolve)
Não traz medições próprias (duração média de plano, paleta real, SFX/min são "hipóteses de fontes de terceiros"); não trata de licença de voz, checagem de fatos, QA automático, determinismo, custo de render nem personagens/multidão.
