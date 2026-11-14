# Perfil Cloud Render v3.1 (texto fornecido pelo usuário)

> Origem: skill descritiva “RICKS-CLIPS-STYLE ORCHESTRATOR (v3.1 — CLOUD RENDER)” colada pelo usuário. Transcrita sem alterar a intenção. Onde conflita com a V2, ver “Precedência” em `SKILL.md`.

**Descrição:** orquestrador autônomo de produção de vídeo no estilo Rick's Clips, executado inteiramente no computador em nuvem do Claude. Faz probe de ambiente, escolhe a rota técnica compatível com CPU/sandbox, renderiza em chunks com retomada, mixa áudio com ducking e −14 LUFS, queima legendas e entrega MP4 baixável. Sem IA generativa de vídeo. Sem perguntas após o briefing.

## 0. Briefing (única interação)
1. Formato e duração: Short (55–75 s) ou longo (3 / 5 / 10 min)?
2. História: já tem uma história real com reviravolta, ou quer 3 pitches (primeira linha, o zombador, a reviravolta, título que esconde o final)? Sobre qual tema?
3. Voz: edge-tts (grátis, rede, mais confiável no sandbox) ou ElevenLabs (se fornecer API key)? Kokoro só se estiver instalado.
4. Qualidade vs. tempo: “Preview rápido” (360×640, 10 fps) ou “Final” (1080×1920, 30 fps)?
Após as respostas, não fazer mais perguntas; executar o pipeline.

## 1. Filosofia visual (núcleo não negociável)
- 2D cartoon em cenário 3D toon iluminado (2.5D). Personagens de cabeça redonda branca, membros de macarrão, mãos de luva, contorno `#2a2230`.
- Cenário com MeshToonMaterial em rampa de 4 passos (168, 206, 236, 255) — sombras nunca pretas. Textura de papel em overlay com leve displace.
- Luz quente (`#ffc27a`, 2,7) contra sombras roxas/azuis. Verde nunca lidera; se aparecer, 55 % para ouro.
- Câmera baixa, ampla (fov 54–64), sempre em movimento (push-in lento ou dolly), sem cortes dentro do mesmo lugar.

## 2. Probe de ambiente (obrigatório antes de tudo; gravar `env_report.json`)
`uname -a; nproc; free -h; df -h`; Python (`PIL`, `numpy`, `cairo`, `skia`); Node/Playwright/Chromium; FFmpeg; Blender; GPU; rede (TTS/APIs).
Regras: Python+Pillow+numpy+FFmpeg → Rota A (Pillow, parallax de camadas); Node+Playwright+Chromium+FFmpeg → Rota B (Three.js CPU/SwiftShader); Blender headless → Rota C (só se A e B falharem); nada disso → parar e reportar.
(Nesta instalação a **Rota B via Remotion + Three.js + SwiftShader** foi validada e é a usada, em conformidade com a V2.)

## 3. Rotas de render
- **A (Pillow):** 4–6 camadas de profundidade com parallax; personagens por frame com ImageDraw; luz por gradientes; papel por ruído numpy; determinismo com `default_rng(seed)`; ≈1–3 fps a 1080×1920.
- **B (Three.js + Chromium headless/SwiftShader):** frames em disco + FFmpeg; sem WebCodecs; `--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`; `renderFrame(f)` determinístico.
- **C (Blender headless):** EEVEE/Workbench + Grease Pencil; mais lento.

## 4. Roteiro (beats)
Short: 0–3 s gancho (9–14 palavras, ato sem sentido com razão escondida) · 3–12 s setup (números exatos) · 12–20 s zombador (frase sarcástica 4–12 palavras, close inclinado) · 20–27 s herói (calmo, enigmático, nunca explica) · 27–40 s escalada (fica mais estranho 3×) · 40–52 s “you see” (analogia cotidiana, 3–5 linhas, 1×) · 52–64 s pagamento (mostrado, não explicado; sem moral; loop no último frame).
Longos: gancho idêntico; setup expandido; escalada 5–7 beats; “you see” mais longo; pagamento imediato + final com gancho.

## 5. Animação, áudio, legendas, pós
- Proporções: cabeça r=55, torso 92–108, pernas 132–170, braços 92 com mãos de bola; pose-to-pose com overshoot; piscadas/respiração; expressões neutro/zombaria/choque/preocupação/riso; um lugar = uma câmera; push-in ease-out; viagens com smootherstep + arco + motion blur; cenário vivo (~2.000 tufos/pedrinhas no primeiro plano).
- Voz: edge-tts (voz masculina, 1,05–1,1) ou ElevenLabs eleven_v4; ducking sidechain; música 20 dB abaixo, ducking 13 dB; loudnorm two-pass **−14 LUFS, true peak −1,5 dB**; alimiter; SFX alinhados ao frame.
- Legendas: 1–2 palavras; Montserrat 800, 76 px, branca, contorno 15 px `#120e1a`, y≈1345; pop 108 %→100 % em 0,09 s; aparece 0,1 s antes; **“sem pontos finais”** (ver conflito em `visual-reference-ricks-clips.md`); .ass + timings do TTS.
- Pós (ordem): DoF → bloom (0,42/0,82) → tone mapping neutral (exposure 1,32) → split-tone (sombras +RGB(0,03, −0,012, 0,085); realces +RGB(0,045, 0,018, −0,035); verdes 55 % → ouro) → saturação 1,08, vinheta 0,22, grain 2 %.

## 6. Recursos do sandbox
Preview antes do final (360×640 @ 10 fps ≈ 2 min); chunks de 300 frames com retomada; limpar frames/ após o encode; MP4 < 200 MB (CRF 20–23); informar estimativa de tempo; nunca carregar todos os frames em RAM.

## 7. QA automático com correção
Paleta quente-fria sem verde dominante; sombras roxas/azuis nunca pretas; contorno `#2a2230`; zero cortes no mesmo lugar; gancho 9–14 palavras; legendas sincronizadas (Montserrat 800); −14 LUFS, música −20 dB, ducking 13 dB.

## 8. Diagnóstico
Pillow/numpy ausentes → `pip install --user`; Chromium/Playwright ausentes → `npx playwright install chromium`; render estourou tempo → reduzir resolução/fps; legenda fora de sincronia → refazer alinhamento; clipping → loudnorm two-pass + alimiter; download grande → CRF 23 ou 720×1280.
