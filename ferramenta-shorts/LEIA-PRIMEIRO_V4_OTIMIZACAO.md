# V4 — render rápido + retomada à prova de reinício (2026-11-16)

## Resultado medido (nuvem, 4 núcleos, sem GPU) — Karansebes, 1931 quadros, 1080x1920, 30 fps
| etapa | antes | agora |
|---|---|---|
| render por quadro (1 navegador) | 6,7 s | 2,3 s |
| render do vídeo (4 navegadores, parede) | ~2,5 h (estimado) | **~44 min** (1,35 s/quadro) |
| QA (estilo + enquadramento + gate) | ~2 h no PC / ~20 min medidos aqui | **~4 min** |
| montagem final | re-codificação inteira | segundos (só junta trechos) |
| **total fim a fim** | >2 h | **~50 min** (uma vez já rodado, retomado após SIGKILL no meio) |

## O que era o gargalo (medido, não chute)
O custo **não era por pixel**: cada ator é um canvas 2D de **1200x2000** redesenhado e reenviado como textura (com mipmaps) a cada quadro; multidão de 26 = 26 uploads de ~10 MB. (O benchmark "720 = 1080" do handoff anterior estava errado: o canvas WebGL continuava 1080x1920.)
Otimizações (em `web/tail.js`, visualmente idênticas — comparado lado a lado):
1. **Cartas adaptativas** (`cardTier`): altura do canvas = altura do ator na tela (+20% de folga), em degraus. Determinístico (não depende do quadro anterior). `window.CARD_FULL=1` volta ao modo antigo.
2. **CoC (desfoque) no alfa do passe de tinta** + amostras do bokeh proporcionais ao raio (era 48 sempre, 2 leituras cada).
3. **MSAA 0** (a tinta por profundidade já suaviza; indistinguível no teste). `window.MSAA=4` volta.
4. **Canvas 2D por software** (`launch.mjs`): ~20% mais rápido que 2D "acelerado" via SwiftShader.
5. `fit.sh` → `fit_fast.mjs`: **um** navegador para todas as iterações (antes 1 novo por iteração, até 15). `gate_all.sh` não repete o inspetor se o fit já selou (`stories/<id>/takes_ok`).
6. QA do inspetor roda a 540x960 (só geometria).

Ainda possível (não feito): sombra 1024 (ganho pequeno), menos taps de bloom/borda (~7-10% cada, mexe no visual), **GPU real** (10-30x; não há GPU nesta nuvem), ou dividir os trechos entre várias sessões em paralelo (o formato em trechos já permite).

## Retomada (o que você pediu)
- `render_pool.mjs`: fila dinâmica de quadros; cada quadro grava `.part`→renomeia; ao iniciar **valida os JPEG** e descarta corrompidos; a cada 150 quadros faz QA do trecho (re-renderiza só os ruins) e **codifica o trecho** `ckpt/<id>/seg_NNN.mp4` (já com legenda). Trecho pronto nunca é refeito. Montagem final = concatenar trechos sem re-codificar.
- `make_video.sh`: selos por etapa em `stories/<id>/stages/` (voz, estilo, fit, gate). Apague um selo para refazer só aquela etapa.
- **Testado**: `kill -9` em tudo no meio do render → relançado → "3/13 trechos prontos, 115 quadros soltos" e continuou do ponto exato.
- **Trava de segurança** (`run_queue.sh`): perto de SESSION_MIN−SAFETY_MIN (60−6) desde o início do container, para de puxar quadros, termina os em curso, codifica trechos completos, faz `ckpt.sh` (commit+push no git) e pausa (código 75). Se a sessão reiniciar, o hook `SessionStart` (`.claude/settings.json` → `boot.sh`) **relança a fila sozinho**. Se não reiniciar em 3 min, a fila segue sozinha. `SESSION_GUARD=0` desliga. Ajuste `SESSION_MIN/SAFETY_MIN/GRACE_MIN` por variável de ambiente.
- `ckpt.sh`: empurra trechos+estado para o git (`CKPT_GIT=0` desliga). **Atenção:** trechos ≈ 7 MB cada (CRF 20) ≈ 90 MB por vídeo no histórico do git. Se o disco do container sobrevive ao reinício, isso é só seguro-extra.
- `status.sh`: mostra fila, etapas e trechos. Uso: `bash run_queue.sh` (ids em `queue.txt`).

## Pendências / avisos honestos
- **Voz**: `speech.platform.bing.com` está bloqueado no proxy da nuvem → o Karansebes desta rodada usa **voz de TESTE (espeak, robótica)**. Para a voz neural: liberar esse host no ambiente (Configurações → ambiente → rede) e apagar `stories/<id>/stages/voice`.
- Sem `GPU`: ~50 min/vídeo é o piso atual do CPU; para < 40 min precisa de GPU ou paralelizar entre sessões.
- O motor tem aleatoriedade (cartas/partículas): dois renders do mesmo quadro diferem levemente (já era assim).
- Efeitos/golpes de câmera do diretor v2: veja no vídeo gerado (`out/karansebes/review_sheet.jpg`).
