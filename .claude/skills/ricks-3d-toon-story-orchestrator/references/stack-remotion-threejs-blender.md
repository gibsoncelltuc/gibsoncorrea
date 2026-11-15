# Remotion × Three.js × Blender — quem faz o quê (decisão de stack)

**Resumo:** não competem; são camadas diferentes.
| Ferramenta | O que é | Faz bem | Limites |
|---|---|---|---|
| **Remotion** | framework React que vira vídeo (Chromium headless + FFmpeg) | linha do tempo/sequências, dissolves, **legendas**, áudio, templates reutilizáveis, dados → vídeo | não modela nem ilumina 3D; render de 3D depende do Three.js |
| **Three.js** (+ `@react-three/fiber`, `@remotion/three`) | biblioteca de 3D em tempo real (WebGL) | protótipos/animatics rápidos, 3D leve, mesmo código do navegador | na nuvem roda em software (SwiftShader): sem luz global, sombras fracas, sem DoF real, lento por quadro |
| **Blender (Cycles)** | DCC 3D offline, scriptável por Python (`bpy`) | **qualidade do look do canal**: luz global, sombras suaves, DoF, volumétricos, materiais pintados, malhas de verdade | ~8–12 s/quadro em 540×960 numa CPU de 4 núcleos; exige modelagem procedural cuidadosa |
| **FFmpeg** | ferramenta de mídia | grade de cor, bloom/vinheta/grão, loudnorm, encode final | não edita por código de alto nível |

**O que o canal original usa:** não é público/verificável. Pelo resultado (sombras suaves, profundidade de campo, luz volumétrica, texturas pintadas) parece **render 3D offline** (Blender/Unity/Unreal), não WebGL em tempo real. Isso é inferência visual, não fato.

**Recomendação (Rota D+):** Blender renderiza os quadros → **Remotion** monta (sequências, dissolves, legendas em React, áudio) → **FFmpeg** aplica a grade calibrada e codifica. Three.js só entra dentro do Remotion para 3D leve/protótipo. A primeira tentativa do piloto (Remotion + Three.js puro) foi **reprovada pelo usuário** justamente pela diferença de qualidade de render para o canal.

**Como está no projeto (`production/guerra-do-porco/`):**
1. `blender/render_all.sh` — passada 1 (15 fps) e passada 2 (30 fps) de PNGs.
2. `tools/montage.sh` — `make_montage_data.py` → `montage/` (Remotion: composição `Montage` = planos + dissolves + áudio; composição `Captions` = legendas em PNG com alfa) → `blender/grade.py` (FFmpeg: grade + overlay das legendas + encode).
3. `blender/post.py` — rota alternativa só-FFmpeg (mesma grade em `blender/lib/grade.py`; legendas por ASS). Use quando o Remotion não estiver disponível.
Detalhe de execução: o bundler do Remotion não segue *symlinks* em `public/`; `make_montage_data.py` usa *hardlinks*.

## Regras de produção acrescentadas (pedidos do usuário)
- **Multidões, tropas, festas, plateias:** cada pessoa é um **personagem completo do mesmo rig e estilo** (rosto, contorno, atuação), com variação individual (altura, cabeça, olhos, boca, pelos faciais, bochechas, tom de roupa, fase da marcha, olhar), em quantidade realista e **renderizada de fato**. Proibido: bonecos genéricos/“manequins”, sprites, instâncias sem braços ou rosto simplificado, ou 5 figurantes para “centenas”. Implementação: `blender/lib/crowd.py` (80 `Char` na cena da tropa, ~12 s/quadro).
- **Contorno de tinta irregular (look “à mão”):** espessura **variável ao longo da linha** — fina do lado da luz (alto-esquerda), ~2–3× mais grossa no lado oposto, com lobos suaves e trechos de espessura diferente; cabeça com ~2 % (fino) a ~6 % (grosso) do diâmetro; membros = traço de tinta fino (~7 % do diâmetro da cabeça) com leve ondulação. Implementação: `ink_g/ink_poly/m_capsule_var` em `blender/lib/char.py` (gêmea de tinta gerada por polígono deslocado pela normal × g(φ), semente por personagem). Calibrado em quadros **nativos** (1290×2796) das gravações.
- **Feições:** olhos = ovais pretos sob barra de pálpebra; sobrancelhas e boca em traço afilado (lente); feições **acima do centro** da cabeça (olhos a +0,12 D, boca a −0,06 D).

## Regras do usuário (acrescentadas) — gate antes de qualquer render
- **Nenhum render longo (passadas completas) antes de TODAS as correções serem feitas e verificadas em fotos de teste lado a lado com os quadros de referência.** Apontar uma lacuna ("ainda falta cenário cheio…") sem corrigi-la antes do render é falha. Fluxo: (1) listar diferenças vs referência (frame a frame, com medidas); (2) corrigir tudo; (3) fotos de teste de TODOS os planos em vários instantes; (4) métricas objetivas (`fidelity_metrics.py`, `outline_metrics.py`); (5) só então renderizar.
- **Cenário cheio:** cada plano precisa de objetos de cena variados e legíveis (mín. ~10 peças distintas visíveis no fundo/meio-plano), com **textura pintada à mão**, **letras estampadas** em pelo menos 2 objetos (caixotes, barris, placas), detalhes de chão (caminho de terra, palha, folhas), arquitetura de fundo (celeiro/cabana/arquibancada/casco), vida (animais, fumaça, bandeiras) e **primeiro plano desfocado** (DOF f/2–2,4 em câmeras baixas). Implementação: `blender/lib/dress.py` (peças), `lib/sets.py` (posicionamento por plano), `lib/paint.py` (texturas e decalques).
