# QA — A Guerra do Porco (piloto)
**Vídeo:** `renders/pilot_540.mp4` — 540x960 @ 30 fps, 20.933 s, h264 yuv420p + aac 48000 Hz, 28.33 MB · **Render:** Blender 5.3.0 Cycles CPU (12 spp + OIDN), 7234 s de render em CPU de 4 núcleos · **Montagem:** Remotion (planos, dissolves, legendas em React) + FFmpeg (grade, encode).
**Resultado automático:** 17/17 (qa.py) + 4/4 (qa_extra.py). **Scorecard:** 75.5/100 → **NÃO aprovado** pela rubrica V2 (mínimo 85 e gates críticos).

## Executado (com evidência)
- ✅ resolução/fps — 540x960@30
- ✅ duração ≈ manifesto — 20.93s vs 20.93s
- ✅ proporção 9:16 — 
- ✅ faixa de áudio presente — aac
- ✅ sem frames pretos — 0 trechos
- ✅ sem congelamento >0.8s — 0 trechos []
- ✅ sombras nunca pretas (L<0.05 < 6% dos pixels, exceto contorno) — máx 0.003
- ✅ verde nunca lidera (média < 12% e máx ≤ máx da referência 0,168 — regra v3.1 original: máx < 12 %, que os próprios prints não cumprem) — máx 0.071 média 0.027 (ref: máx 0,168 média 0,052)
- ✅ paleta quente + fria presente — quente 0.29 frio 0.37
- ✅ sombras predominantemente azul/roxo (≥ 90 % da referência medida 0,396 — regra v3.1 original > 0,55, que os prints também não cumprem) — 0.37 (ref 0,396)
- ✅ SRT: tempos crescentes e dentro da duração — 37 cartões
- ✅ legendas mantêm a pontuação do roteiro (observado no canal; config keepPunctuation) — 10 cartões com pontuação final
- ✅ sincronia voz×timestamps (desvio máx < 0.20s) — máx 0.060s
- ✅ loudness -14 LUFS (±0.7) — -14.4 LUFS
- ✅ true peak ≤ -1.5 dBTP — -4.2 dBFS
- ✅ ducking ≈ 13 dB (11–15) — -14.4 dB
- ✅ música ≈ 20 dB sob a voz (17–23) — -22.2 dB
- ✅ câmera sempre em movimento (média ≥ 1.2 em todos os planos) — {'S1': [27.07, 15.74], 'S2': [21.97, 9.92], 'S3': [16.84, 11.54], 'S4': [20.04, 11.74], 'S5': [12.35, 5.81], 'S6': [17.33, 3.08]}
- ✅ sem cortes secos (SPIKE isolado: salto > 20 e ≥ 3× a mediana local) fora de tiros — movimento rápido sustentado é permitido (prints: 16–22 % dos quadros com salto > 14) — 0 spikes [] | saltos: {'mean': 6.84, 'p90': 13.87, 'max': 29.68, 'frac_gt14': 0.099}
- ✅ gancho com 9–14 palavras — 12 palavras
- ✅ último quadro ecoa o primeiro (mais parecido que um quadro do meio) — loop 44.3 vs meio 64.2
- **Fidelidade vs referência** (7 métricas; razão meu/canal, ideal ≈ 1): laplacian_var 1.02; edge_density 0.88; colorfulness 0.87; sat_mean 0.98; val_mean 0.96; contrast_local 0.89; vignette 1.13 — detalhe em `qa/fidelity-report.md`.
- **Contorno de tinta** (razão espessura grossa/fina p90/p10): referência 4.22 · piloto 5.1 (`qa/outline-metrics.json`); versão antiga ≈ 2,0.
- **Determinismo:** DETERMINISTICO: quadro S3 f281 re-renderizado em processo separado → pixels idênticos (diferença máx 0); o hash do arquivo PNG difere só por metadados.
- Quadros: 694 (S1 117, S2 130, S3 125, S4 143, S5 72, S6 107), nenhum faltando; passada 1 (pares) + passada 2 (ímpares).
- Revisão visual **feita por mim** em fotos de teste de todos os planos, em folhas de contato e em quadros 540×960 (achou e corrigiu: legendas sobrepostas, vela do convés, sombra dos abetos, preto da tinta); evidências em `qa/pre-render-stills.png`, `qa/pre-render-review.md`, `renders/contact_540.png`.

## Recalibrações declaradas (o que mudou e por quê)
- **Verde nunca lidera** e **sombras azul/roxo**: as regras originais (máx < 12 % de pixels "verdes"; > 55 % de sombras azul/roxo) **não são cumpridas pelos próprios prints** (medido: verde máx 16,8 %, sombras azul/roxo 39,6 %). Os limiares passaram a ser relativos à referência.
- **Cortes secos**: o limiar de "salto médio > 14" reprovava movimento rápido sustentado; os prints têm 16–22 % dos quadros acima disso. Agora detecta **spike isolado** (> 20 e ≥ 3× a mediana local).
- **Preto da tinta**: medido RGB≈33,22,35 nos prints (o piloto saía ≈14,4,11); levantado na grade para ameixa escura.

## Não executado / limitações (declaradas)
- revisão humana assistindo com som, sem som e em celular
- versão 1080p (o pedido era piloto de baixa resolução)
- render em GPU
- fontes primárias da Guerra do Porco
- licença comercial da voz
- Texturas e modelos são **procedurais** (código), não pintados por um artista; sem cavalos/arquibancadas do canal (não fazem parte da história).
- Voz `edge-tts`: termos comerciais pouco claros → regravar com voz licenciada antes de monetizar.
- Conflito de metas de áudio: V2 sugere −15 LUFS/−1,0 dBTP; usado o perfil v3.1 (−14/−1,5).
