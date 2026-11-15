# Revisão antes do render (v5) — diferenças contra os prints e correções

Regra do usuário: **nenhum render longo antes de todas as correções.** Esta revisão registra o que foi comparado, medido e corrigido *antes* de iniciar o render v5. Evidências: `qa/pre-render-stills.png` (fotos de teste dos 6 planos), `qa/outline-comparison-head.png` (cabeça da referência × minha), `qa/outline-metrics.json`.

| # | Diferença encontrada nos quadros nativos (1290×2796) | Correção | Verificação |
|---|---|---|---|
| 1 | Contorno dos personagens **uniforme**; nos prints é fino de um lado e 2–3× mais grosso do outro, em trechos | `ink_g/ink_poly/m_capsule_var` (`lib/char.py`): espessura variável por polígono × g(φ), semente por personagem; cabeça, corpo, mãos, pés, chapéus, porco | razão espessura grossa/fina (p90/p10): referência 4,22 · versão antiga 2,0 · nova 4,12 |
| 2 | Membros muito grossos (≈15 % da cabeça) | traço de tinta ≈ 7 % do diâmetro da cabeça, com ondulação leve | comparação lado a lado (`outline-comparison-head.png`) |
| 3 | Feições pequenas e baixas; prints: olhos acima do centro (+0,12 D), boca a −0,06 D, olhos = ovais pretos sob barra de pálpebra | feições subidas (`FACE_DZ`), tamanhos medidos, sobrancelha/boca em traço afilado | comparação lado a lado |
| 4 | Legendas ~1,6× menores e mais altas que as do canal | Montserrat ExtraBold; ascendente 5,4 % da altura, linha de base 72,7 %, contorno 7 + sombra (medido: 29–30 px, 72,7–72,8 %) | medição pixel a pixel em quadros da referência |
| 5 | Tropa simplificada (sem braços/rosto igual) | 80 `Char` completos e variados + fuzil no ombro + porta-bandeira (`lib/crowd.py`) | foto de teste do plano 4 |
| 6 | Cenários vazios (grama + cerca) | biblioteca de objetos pintados (`lib/dress.py`, `lib/paint.py`, `lib/sets.py`): celeiro, ovelhas, barris/caixotes com letras, feno, carrinho, poço, carroça, espantalho, varal, cerca de estacas, fogueira, convés com amurada pintada, mastro/vela/cordame, caminho de terra, palha/folhas no chão, fumaça | fotos de teste de todos os planos |
| 7 | Primeiro plano nítido; prints têm primeiro plano bem desfocado | DOF f/2,1–2,4 nas câmeras baixas | fotos de teste |
| 8 | Sombra longa e escura dos abetos no plano 4 | sombra dos abetos desligada nesse plano | foto de teste |
| 9 | Métricas gerais | — | 7 métricas (detalhe, bordas, colorido, saturação, brilho, contraste local, vinheta) entre 0,86× e 1,20× da referência |

Limitações que **permanecem** (declaradas): texturas são procedurais (não pintadas por um artista), sem cavalos/arquibancadas do canal (não fazem parte desta história), 15 fps na primeira passada, voz sintética `edge-tts` com licença comercial pouco clara.
