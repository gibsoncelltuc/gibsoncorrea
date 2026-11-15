# Licenças e procedência — "A Guerra do Porco" (piloto v3, Blender)
Nenhum asset de terceiros foi usado no vídeo: modelos, texturas, animação, música e SFX foram **gerados por código** neste repositório. Não foi usado gerador de vídeo/imagem por IA.

| Item | Origem | Licença / observação |
|---|---|---|
| Personagens (cut-outs 2D em 3D), porco, soldados, props, navios, convés, ilha, horta, cabana, árvores, nuvens, mar, montanhas, câmera, animação | código original do projeto: `blender/lib/*.py` (Python + `bpy`), poses como função pura do tempo (`lib/anim.py`) | Propriedade do projeto. Navios/uniformes/rostos são **ficção genérica**, não reproduções de pessoas ou obras. |
| Texturas pintadas (grama, solo, madeira, telhas, vela, casco, água, bandeiras, notas, placa, tecidos, nuvens) | geradas proceduralmente (numpy/Pillow, pinceladas, seed fixo): `blender/lib/texlib.py` + vertex colors + shaders (`lib/mats.py`) | Original do projeto. Bandeiras desenhadas por código a partir de design de domínio público (séc. XIX). |
| Música (`stems/music.flac`) | sintetizada por `tools/build_audio.py` (numpy, seed fixo) | Original do projeto, sem amostras. |
| SFX e ambiência (`stems/sfx.flac`, `stems/ambience.flac`) | sintetizados por `tools/build_audio.py` | Original do projeto. |
| Narração | `edge-tts` (`pt-BR-AntonioNeural`), voz sintética; não clona pessoa real | ⚠ Os termos comerciais do endpoint não são claros para monetização/redistribuição. **Regravar com voz licenciada antes de publicar monetizado.** Timestamps e pipeline continuam válidos. |
| Fonte das legendas | Montserrat ExtraBold (`blender/fonts/Montserrat-ExtraBold.ttf`), convertida de `@fontsource/montserrat` com fontTools (sem alterar glifos) | SIL OFL 1.1 |
| Blender 5.3 (módulo Python `bpy`, Cycles, OpenImageDenoise) | PyPI `bpy` / blender.org | GPL-3.0-or-later (Cycles e OIDN: Apache-2.0). O conteúdo criado (renders/vídeo) pertence ao autor. Os scripts que importam `bpy` devem ser tratados como GPL se forem redistribuídos — confirmar a política atual em blender.org/about/license antes de abrir o código. |
| FFmpeg 6.1 (build Ubuntu, com libx264) | apt | Ferramenta externa (LGPL/GPL); a licença do binário não se aplica ao vídeo gerado. |
| numpy (BSD-3), Pillow (HPND), fontTools (MIT), brotli (MIT), edge-tts (LGPL-3.0) | PyPI | Dependências de ferramentas de build. |
| Remotion, React, three, @react-three/fiber (apenas no código histórico `src/` e no projeto *Tomé e o Lago*) | npm | MIT; Remotion: gratuita p/ indivíduos e empresas pequenas — **empresas maiores precisam de licença**. |
| Referência de estilo (prints/gravações do canal Ricks Clips) | enviados pelo usuário, usados só para **observação de linguagem visual** e métricas objetivas | Nenhum frame, personagem, roteiro, voz ou asset do canal foi copiado ou incorporado; elenco, cenários e texto são originais. Frames de referência ficam só em `qa/_local/` (não versionado). |
