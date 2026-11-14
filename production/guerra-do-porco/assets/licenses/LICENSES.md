# Licenças e procedência — "A Guerra do Porco" (piloto)
| Item | Origem | Licença / observação |
|---|---|---|
| Personagens, rigs (Rig v2, Pig), cenário (ilha, horta, cabana, ovelhas, acampamento, fragatas, convés), props, câmera, animação | código original do projeto (`src/`) | Propriedade do projeto. Sem assets de terceiros. Navios/uniformes/rostos são **ficção genérica**, não reproduções. |
| Texturas (grama, solo, madeira, toras, telhas, vela, casco, água, bandeiras, notas, placa, nuvem, raios, tecidos) | geradas proceduralmente em Canvas 2D (`src/world/tex.ts`, seed fixo) | Original do projeto. Bandeiras desenhadas por código (design de domínio público do séc. XIX). |
| Música (`stems/music.flac`) | sintetizada por `tools/build_audio.py` (numpy, seed fixo) | Original do projeto, sem amostras. |
| SFX/ambiência (`stems/sfx.flac`, `stems/ambience.flac`) | sintetizados por `tools/build_audio.py` | Original do projeto. |
| Narração | `edge-tts` (`pt-BR-AntonioNeural`), voz sintética; não clona pessoa real | ⚠ Termos comerciais do endpoint não são claros para monetização/redistribuição. **Regravar com voz licenciada antes de publicar monetizado.** Timestamps/pipeline permanecem válidos. |
| Fonte das legendas | Montserrat 800 via `@fontsource/montserrat` | SIL OFL 1.1 |
| Textura de papel | `public/paper.png`, gerada por script | Original do projeto. |
| three, @react-three/fiber, react | npm | MIT |
| Remotion | npm (`remotion`, `@remotion/*` v4) | Licença Remotion: gratuita p/ indivíduos e empresas pequenas; **empresas maiores precisam de licença** — verifique se se aplica. |
| Referência de estilo (prints/gravações do canal Ricks Clips) | enviados pelo usuário, usados só para **observação de linguagem visual** | Nenhum frame, personagem, roteiro, voz ou asset do canal foi copiado ou incorporado; elenco e cenários são originais. |
