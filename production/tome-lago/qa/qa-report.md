# QA — O Homem que Jogava Cadeiras no Lago
**Resultado automático:** 17/17 checagens (`qa/final.json`, `qa/preview.json`). **Scorecard:** 71.5/100 → **NÃO aprovado** pela rubrica V2 (mínimo 85).

## Executado
- Build/compilação (`tsc --noEmit`), preview real 360×640 @10 fps, render final 1080×1920 @30 fps (2085 frames, 7 chunks) e concatenação sem perda (2085 frames conferidos).
- Duração/FPS/proporção, frames pretos (0), congelamento (0), paleta (verde máx 1,7 %; sombras azul/roxo 63 %), SRT (93 cartões), sincronia voz×timestamps (máx 0,10 s), loudness −14,3 LUFS, true peak −4,4 dBFS, ducking −12,7 dB, música −20,2 dB sob a voz.
- **Determinismo:** frame 1234 em duas execuções separadas (com o frame 77 renderizado entre elas) → hash idêntico.
- Revisão visual **feita por mim** em folhas de contato e frames 1080p.

## Não executado / limitações (declaradas)
- **Revisão humana (assistir com som, sem som, em celular):** pendente — gate crítico da V2.
- DoF/bloom 3D reais não aplicados (SwiftShader); grade feita por overlays CSS.
- Benchmark Claude Animated Shorts **não auditado** (GitHub 403).
- **Voz `edge-tts`:** termos comerciais não claros → substituir por voz licenciada antes de monetizar.
- Falhas visuais conhecidas: fim do S1 sem personagem em quadro; ponte submersa de móveis escura e pouco legível; estilo mais simples que o canal-referência (esse gap motivou o piloto novo).
- Conflito de metas de áudio: V2 sugere −15 LUFS/−1,0 dBTP; usado o perfil v3.1 (−14/−1,5).
