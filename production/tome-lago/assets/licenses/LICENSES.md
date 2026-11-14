# Licenças e procedência
| Item | Origem | Licença / observação |
|---|---|---|
| Personagens, rigs, cenários, props, câmera, animação | código original deste projeto (`src/`) | Propriedade do projeto. Nenhum asset de terceiros. |
| Música (`audio/music.wav`) | **sintetizada** por `tools/build_audio.py` (numpy, seed fixo): progressão Am–F–C–G, pad/pluck/baixo | Original do projeto, sem amostras de terceiros. |
| SFX e ambiência (`audio/sfx.wav`, `audio/ambience.wav`) | **sintetizados** por `tools/build_audio.py` (ruído filtrado, osciladores) | Original do projeto. |
| Textura de papel (`public/paper.png`) | gerada proceduralmente por script Python/numpy | Original do projeto. |
| Narração | TTS `edge-tts` (voz `pt-BR-AntonioNeural`, serviço neural da Microsoft). Voz sintética, **não** clona pessoa real. | ⚠ O pacote `edge-tts` usa o endpoint do Edge/Read Aloud; os termos de uso comerciais do serviço da Microsoft não são claramente licenciados para redistribuição comercial. Para publicação monetizada, regravar com voz licenciada (ex.: Azure Speech com contrato, ElevenLabs com chave) ou voz humana. Os timestamps/pipeline continuam válidos. |
| Fonte Montserrat 800 | pacote npm `@fontsource/montserrat` | SIL Open Font License 1.1 |
| three, @react-three/fiber, react | npm | MIT |
| Remotion | npm (`remotion`, `@remotion/*` v4) | Licença Remotion: uso gratuito para indivíduos e empresas pequenas; empresas maiores precisam de licença de empresa. **Verifique se se aplica a você.** |
| FFmpeg, Chromium (render), Python/numpy/Pillow | ferramentas locais | licenças próprias das ferramentas; sem redistribuição de binários. |
| Claude Animated Shorts (benchmark) | **não obtido** | Ver `external/benchmark-diff.md`. Nenhum código/asset incorporado. |
