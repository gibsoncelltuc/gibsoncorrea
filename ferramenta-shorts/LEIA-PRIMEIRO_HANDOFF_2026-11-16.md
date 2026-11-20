# HANDOFF 2026-11-16 — leia primeiro (para a próxima conta/sessão)

Usuário fala português, quer tudo em português, respostas curtas e honestas. Conta anterior chegou a 99% do limite semanal.
Contexto do projeto: `RELATORIO_E_PLANO.md` (mesma pasta) + `SKILL.md` + `docs/`. Este arquivo cobre o que aconteceu DEPOIS.

## 1. O que foi feito nesta sessão (PC do usuário, Windows 11, 2 núcleos, sem GPU, 12 GB RAM, pasta D:\PopcornPop_ferramenta\ferramenta-shorts)
- Ferramenta instalada (Python 3.12, Node 24, ffmpeg, Playwright+Chromium, edge-tts).
- **Correções de compatibilidade Windows** (já aplicadas neste zip): `import url`/`pathToFileURL` em `qa_camera.mjs`, `qa_takes.mjs`, `storyboard.mjs`; `autostyle.py` chama `bash ./x.sh` e `sys.executable`; `/tmp` → `tmp/` em `qa_style.sh`; `fontsdir=fonts` em `assemble.sh`; pasta `shim/python3` (wrapper para o Python 3.12; usar `export PATH="$PWD/shim:$PATH"` antes de rodar). No Linux/nuvem nada disso atrapalha.
- **Karansebes v1** foi renderizado e entregue (PT-BR, 62 s, 1080x1920, -15 LUFS). Usuário: "ficou bom", mas pediu melhorias (ver §2).
- **Diretor automático** implementado em `mkvideo.py` (backup: `mkvideo.py.bak`; roteiro original: `videos/karansebes/beats.v1.json`):
  - planos abertos `reveal` (recua e revela o exército), `orbit` (panorâmica em arco), `wide`, `crowd`; nunca >2 abertos seguidos; abertura e final sempre `reveal`; abertos não sofrem sub-corte (`nocut`) nem `vary`.
  - multidão automática (10–26 soldados em fileiras; marchando para dentro quando a fala diz chegou/chegaram etc.). `shot_lock:true` no beat desliga o diretor naquele beat; `"director": false` no arquivo desliga tudo.
  - animação em palavras-chave (tabela `KW` em `mkvideo.py`): golpe de câmera (`kicks`) + efeito (burst/ring/dust/stars/puff) no instante da palavra.
  - `qa_takes.mjs`: limite "TINY" menor (0.028) para takes com `hero:{wide:true}` (senão o `fit.sh` aproxima a câmera e destrói o plano aberto).
  - Prévia (storyboard) aprovada visualmente: `sb.jpg`. Efeitos/golpes de câmera **ainda não vistos em movimento**.
- **Karansebes v2 NÃO foi renderizado**: o render foi interrompido por lentidão (ver §3). `out/karansebes_v1/` guarda o v1.

## 2. Feedback do usuário sobre o v1 (requisitos para todos os vídeos)
1. Faltou personagem: "chegou a infantaria" mostrava 2 personagens. Quer batalhões/multidão de verdade.
2. Câmera: nenhum ângulo aberto em todo o vídeo; movimentos fracos/básicos. Quer ângulos abertos, mostrar chegada de batalhão, interação entre câmeras.
3. Palavras-chave da narração devem disparar movimento/animação que as destaque.
4. Ainda pendentes do relatório antigo: ações de corpo (pegar/carregar/correr — não existe no motor), animais melhores, voz com licença comercial (edge-tts é não oficial), os 7 roteiros PT que não vieram no zip (Onoda, Uísque, Zanzibar, Pastéis, Jenkins, Futebol, Wojtek), Guerra do Porco (`videos/porco1859/beats.json` por criar).

## 3. PROBLEMA PRIORITÁRIO: tempo de render
Meta do usuário: **vídeo de ~1.500–2.500 quadros a 30 fps, 1080x1920, qualidade alta, passando por TODAS as verificações (QA), em ≤ 40 min (no máx. 1 h)**, de preferência **na nuvem** (4 núcleos / 15 GB; a sessão de nuvem **reinicia a cada ~1 h**, então o processo tem que ser retomável sem perder nada).

Medido/observado nesta sessão (PC local):
- 3 shards `chrome-headless-shell` (SwiftShader = WebGL por CPU) em PC de 2 núcleos: CPU 100%, ~1,4 GB RAM cada, RAM livre ~0,5 GB (swap), e um processo Python estranho (pid 8932) com 5000+ s de CPU desde de manhã. Ritmo medido: **~3 quadros/min** (44→48 em 90 s) → >10 h para 1872 quadros. Inviável.
- Antes do render, as etapas de verificação (`autostyle` 6 rodadas + `fit.sh` até 15 iterações de `qa_takes` + `gate_all`) levaram **~2 h** com multidões de 26 (11:38→13:36). A hipótese do usuário (QA pesa mais do que o render) é **procedente**.
- Benchmark limpo (s/quadro a 1080x1920 vs 720x1280, 1 shard, PC livre): `logs/bench.txt` (se existir) — ver §4.

Causas (do código):
1. WebGL por software a 1080x1920 por quadro, com pós-processamento em tela cheia (bloom, desfoque de lente/DoF, contorno de tinta por profundidade, grade de cor, sombras): tudo na CPU.
2. `getFrameDataURL` → `readPixels` + base64 JPEG ida e volta por quadro (aviso "GPU stall due to ReadPixels").
3. `render_missing.sh` fixa 3 shards, independente do nº de núcleos (superassinatura em 2 núcleos; RAM estoura).
4. QA em resolução cheia e repetido: `fit.sh` (até 10+5 iterações × todos os takes, `qa_takes 4`), `autostyle` (6 × build+render de 1 quadro por take), `gate_all` refaz build + qa_camera + qa_takes + qa_style.
5. Multidões grandes (26 atores) aumentam o custo por quadro.

## 4. Plano de otimização (a fazer, em ordem de ganho esperado; estimativas NÃO medidas)
A. **GPU na nuvem (maior ganho potencial, 10–30×)**: Chromium headless com GPU real (Linux + NVIDIA: `--use-gl=angle --use-angle=gl-egl` / `--ignore-gpu-blocklist`, remover `swiftshader`). O usuário já usou GPU L4 no Lightning (memória "Lightning factory") e Kaggle. Validar primeiro: `chrome://gpu` / `renderer` no WebGL deve dizer NVIDIA, não SwiftShader. Se funcionar, 2000 quadros em ~10 min.
B. **QA em baixa resolução (360x640)**: `qa_takes`, `qa_style`, `autostyle`, `storyboard` em ~1/9 dos pixels. Estilo: 2 rodadas no máximo. `fit.sh`: reaproveitar resultado (cache por hash do spec) e só reiterar takes que falharam; no máximo 4 iterações. Meta: QA total < 8 min.
C. **Render em 720x1280 + upscale para 1080x1920** (lanczos no ffmpeg) como modo "rascunho/rápido" (~2,25× menos pixels); final em 1080 nativo só se a GPU permitir. O estilo é suave/pintado, perda pequena — validar visualmente.
D. **Shards = nº de núcleos** (`nproc`), 1 aba por shard, limitar RAM; escrever JPEG direto do canvas (`canvas.toBlob`/CDP `Page.captureScreenshot` com `format:jpeg`) em vez de base64 por `evaluate`.
E. **Cache de fundo estático** (céu/terreno/cenário que não muda entre quadros do mesmo take) e cortar passos de pós-processo caros; instanciar multidão; limitar multidão a ~14 em render CPU.
F. (Opcional) renderizar a 15 fps e interpolar para 30 (`minterpolate`/`framerate`) — testar artefatos; só se C+D não bastarem.

Quadros por vídeo: 30 fps × 60 s = 1800; 2500 quadros ≈ 83 s. Meta realista com GPU: render < 15 min + QA < 8 min + montagem 3 min.

## 5. Retomada automática (nuvem reinicia a cada ~1 h) — implementar/ativar
- Já é retomável: `render_missing.sh` só renderiza quadros que faltam (arquivos `out/<id>/frames/fNNNN.jpg`); `make_video.sh` é idempotente (`stories/<id>/DONE`). Falta: persistir tudo (voz, `stories/<id>/work`, `out/<id>/frames`, `fit.js`) em volume/disco que sobreviva ao reinício, e um **supervisor**.
- Este zip traz `run_queue.sh`: laço que lê `queue.txt` (um id por linha) e roda `make_video.sh` de cada id em sequência; ao ser relançado após reinício continua de onde parou (pula DONE, retoma quadros). Na nuvem: chamar no boot (`@reboot`/script de inicialização/`nohup`) e gravar log em `logs/queue.log`. Escrever em arquivo temporário e renomear (`.part` → final) para não deixar JPEG/MP4 truncado.
- Etapa do `make_video.sh` deve gravar checkpoint (arquivo `stories/<id>/stage`) para pular fases já feitas (estilo, fit, snap) sem refazer.

## 6. Redes sociais (pedido do usuário; só plano, nada feito)
Mesmo vídeo vertical 1080x1920 (≤ 60–90 s) em **YouTube Shorts, TikTok e Instagram Reels**, mesmo nome de perfil nos três (TikTok já criado). Opinião honesta: reaproveitar o mesmo vídeo é padrão e funciona (alcance de cada plataforma é independente; "rede conectada na outra" não impulsiona sozinha, mas multiplica as chances do mesmo conteúdo); cuidar de: sem marca d'água de outra plataforma, legenda/safe-zones, título e descrição ajustados a cada plataforma, `#shorts` no YouTube, postar em horários similares, medir qual plataforma retém mais e dobrar nela. Criação de contas/uploads: **só com o usuário** (senhas/verificações são dele; a skill de upload do YouTube existe no projeto N8N, ver memória "Upload YouTube + limite diário").

## 7. Comandos úteis
```
cd D:\PopcornPop_ferramenta\ferramenta-shorts     # (Git Bash) export PATH="$PWD/shim:$PATH"   # só no Windows
bash make_video.sh karansebes          # roteiro→voz→estilo→fit→gate→render→QA→mp4  (apague stories/<id>/DONE para refazer; apague out/<id>/frames para re-renderizar tudo)
node storyboard.mjs <id> sb.jpg 270 && python3 sbsheet.py sb.json sb.jpg    # prévia de takes
bash run_queue.sh                      # fila retomável (queue.txt)
```
Nunca rodar `build3.sh`/`shot.mjs` durante um render (pasta `web/` compartilhada).


## 8. Benchmark medido (PC do usuário, 2 núcleos, 1 shard, 8 quadros do take b5, 700-707)
- done 8 frames, 24.91 s/frame
- done 8 frames, 23.86 s/frame
- Referência: sessão de nuvem 4 núcleos/15 GB renderizava um vídeo de ~1900 quadros em pouco mais de 1 h (≈ 2 s/quadro de parede com 3 shards).

**CONCLUSÃO DO BENCHMARK (importante):** 720x1280 levou 23,9 s/quadro e 1080x1920 levou 24,9 s/quadro — quase igual. Ou seja, **o custo NÃO é por pixel**; reduzir resolução (item C do §4) quase não ajuda. O gargalo é por quadro, fixo: provavelmente a montagem da cena em JavaScript (desenho 2D de cada personagem/sprite em canvas, geração de texturas, muitos objetos 3D) e o pipeline CPU do SwiftShader, mais o readPixels. Antes de otimizar, **perfilar um quadro** (Chrome DevTools/`performance.now()` por etapa dentro de `renderFrame`: cena, sprites/atores, pós-processo, readPixels, JPEG) para achar onde vão os ~24 s. Prioridade: (1) GPU real na nuvem (A), (2) perfilar e cortar o custo fixo por quadro (cache de sprites/texturas entre quadros, menos atores e passos de pós), (3) QA em baixa resolução só reduz o QA se o custo por quadro também cair — por isso o QA deve usar MENOS quadros (amostrar 1 quadro por take, não `step 4`), e não só menos pixels.
