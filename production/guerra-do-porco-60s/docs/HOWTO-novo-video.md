# Como fazer um novo vídeo com esta linha de produção

Tudo é **código**: nenhuma imagem/vídeo/voz gerados por IA generativa; texturas, modelos, música e SFX são sintetizados por scripts (reproduzíveis, com semente fixa).
Estilo-alvo: Shorts 9:16 de ~20–65 s em 3D "recortes de papel" (contorno de tinta irregular, rostos de olhar pesado, multidões de **personagens reais**, cenário cheio com texturas pintadas por código).

## 0. Criar o projeto (1 comando)
```bash
tools/new_video.sh meu-video "Título do vídeo"      # cria production/meu-video/ + smoke test (renderiza 1 quadro 3D de exemplo)
```
O que é **reutilizado** (copiado): `blender/lib/` (char, crowd, pig, props, dress, paint, nature, farm, ships, deck, mats, texlib, renderlib, grade, anim), `blender/*.py` (render_shot, post, grade, stills, check_framing, sheets, motion_test), `tools/` (voz, mix, QA, fichas, relatórios), `montage/` (Remotion), `schemas/`, `docs/`.
O que é **específico da história** (esqueleto de exemplo): `blender/lib/shots.py` (uma classe por cena), `blender/lib/sets.py` (vestimenta do cenário), `script/story.json`, `storyboard/shots.json`, `research/claims.json`, `audio/events.json`, `assets/licenses/LICENSES.md`.

## 1. Pesquisa e fatos (gate: nenhuma afirmação central sem fonte)
1. Leia ≥ 2 fontes **independentes** por afirmação (guarde o texto em `research/sources/*.txt`).
2. Preencha `research/claims.json`: `fontes{}` e `afirmacoes[]` com `fala`, `afirmacao`, `fontes[{fonte, trecho LITERAL, url}]` (≥ 2 distintas), `confianca`, `nota` (numerais de fonte única, dramatizações).
3. `python3 tools/make_factcheck.py` (gera `research/fact-check.md`) e `python3 tools/validate_schemas.py` — este confere que **cada trecho citado aparece literalmente** no texto salvo da fonte.

## 2. Roteiro e voz (licença aberta; sem clonagem)
1. `script/story.json`: linhas `{id, shot, beat, text, pause_before, intent}`; gancho de 9–14 palavras, uma ideia por frase, payoff que ecoa o primeiro quadro (loop).
2. `python3 tools/build_voice.py` — Piper (modelo `pt_BR-cadu-medium`, dataset CC0) por frase + alinhamento de palavras por programação dinâmica sobre o envelope de energia → `script/word-timings.json`. `CROSSCHECK=1` confere com o faster-whisper.
3. `python3 tools/voice_asr_check.py` — ASR independente sobre a faixa de voz (WER/CER).

## 3. Plano de edição (EDL) e câmera
- `storyboard/shots.json` é a **lista de edição**: `{id, scene, start, end, lines, beat, camera, action, audio}`. `scene` escolhe a classe em `blender/lib/shots.py`; **inserts** (close, detalhe) reutilizam a mesma cena com outra câmera e os cortes seguem as palavras (`anim.word_start(linha, 'palavra')`).
- Alvo de ritmo: um plano a cada ~2 s (prints do canal: 2–2,7 s), câmera sempre em movimento, dissolve de 0,4 s.
- Coreografia = **função pura do tempo absoluto `t`** (`update(t)`): determinística, permite inserts com continuidade perfeita e re-render quadro a quadro idêntico.

## 4. Personagens, multidão e cenário (regras do usuário)
- Personagens: `char.Char(nome, look)` — olhos de pálpebra pesada, 9 bocas, suor, chapéus, contorno **irregular** (fino do lado da luz, ~2–3× mais grosso no oposto, em pedaços). Fichas: `python3 blender/sheets.py` → `design/character-sheet.png`.
- **Multidão/tropa/festa = personagens reais do mesmo rig e estilo** (`lib/crowd.py`: cada pessoa única; nunca instâncias genéricas nem bonecos aleatórios).
- **Cenário cheio** antes de qualquer render: objetos de `lib/dress.py` (barris, caixotes, feno, carroça, cercas, celeiro…) + texturas pintadas por código (`lib/paint.py`, `texlib.py`) + céu/nuvens/pássaros/fumaça. Confira com `python3 blender/stills.py 270 480 12 S1:1.0,2.5` e `blender/check_framing.py <edição>`.
- **Gate de render:** faça TODAS as correções (cenário, rosto, contorno, enquadramento) nos stills **antes** de subir a renderização longa.

## 5. Áudio
`audio/events.json` (SFX ancorados em palavras; timbres: `python3 tools/sfxlib.py --list`) + `audio/music.json` → `python3 tools/build_audio.py` → `python3 tools/mix.py` (ducking de −13,5 dB por envelope, −14 LUFS, TP ≤ −1,5 dBTP).

## 6. Render (CPU) em duas passadas, sempre baixa resolução primeiro
```bash
blender/render_all.sh 540 960 12 50000 2 0     # passada 1: quadros pares (15 fps efetivos), retomável
blender/render_all.sh 540 960 12 50000 2 1     # passada 2: quadros ímpares (30 fps completos)
```
Custo medido no piloto (4 vCPU, Cycles 12 spp + OIDN): ~11–14 s/quadro a 540×960 → ~2,5 h para 730 quadros. 1080×1920 ≈ 4×. Determinístico (re-render do mesmo quadro → pixels idênticos).

## 7. Montagem e grade
`tools/montage.sh renders/<video>.mp4` — Remotion (planos + dissolves + legendas em PNG com alfa) + FFmpeg (unsharp, grade, bloom, vinheta, grão, preto levantado). Cartões de legenda: 1–3 palavras, ≥ 0,30 s, vírgula/ponto fecham o cartão, sintagma não é partido.

## 8. QA e scorecard (rubrica V2: ≥ 85/100 e nenhum gate crítico reprovado)
```bash
REF_DIR=<pasta com quadros de referência> tools/run_qa.sh renders/<video>.mp4     # 17+4 checagens, fidelidade vs referência, contorno, manifesto, folha de contato
python3 tools/frame_samples.py renders/<video>.mp4 && python3 tools/legibility_check.py && python3 tools/voice_asr_check.py
python3 blender/motion_test.py && python3 tools/camera_report.py                      # movimento/contato/continuidade e curva de câmera
python3 tools/make_design_sheets.py renders/<video>.mp4 && python3 tools/validate_schemas.py && python3 tools/check_assets.py
tools/determinism_check.sh <edição> <quadro>                                          # re-render em processo separado → diferença de pixels
python3 tools/make_report.py                                                          # qa/qa-report.md + qa/scorecard.json (notas 0–5 do autor, editáveis; gates calculados)
```
Nunca declare "aprovado" sem: vídeo realmente renderizado, QA executado, gates verificados e a **revisão humana** (assistir com som, sem som e em tela pequena) registrada — o relatório distingue o que foi executado do que não foi.

## 9. Reuso e versionamento
`python3 tools/make_registry.py` regrava `registry/registry.json` (id, versão, hash do arquivo, licença, dependências, cena de teste). Mudou um módulo → suba a versão e rode `tools/validate_schemas.py` (acusa hash desatualizado).
