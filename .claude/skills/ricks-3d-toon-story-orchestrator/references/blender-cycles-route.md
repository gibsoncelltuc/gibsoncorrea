# Rota D — Blender (Cycles CPU) + FFmpeg: cenário 3D pintado no nível do canal

**Quando usar:** quando a referência visual exige cenários 3D ricos (luz com GI, sombras, profundidade de campo, texturas pintadas, multidão, objetos modelados). A rota B (Three.js/SwiftShader) rende rápido, mas **não** alcança esse acabamento: medido contra as gravações do canal, o piloto em Three.js teve 2,3× menos bordas, 1,7× menos detalhe fino e 1,5× menos contraste local (`scripts/fidelity_metrics.py`). A rota D foi validada neste ambiente (4 vCPU, sem GPU).

## Instalação (validada)
```bash
pip install bpy                      # Blender 5.x como módulo Python (cp313 ok); ~350 MB
apt-get install -y --no-install-recommends libgl1-mesa-dri libglx-mesa0 libegl1 libegl-mesa0 libgbm1 libopengl0 libxi6 libxxf86vm1 libxfixes3 libxrender1 libsm6 libxkbcommon0 libdrm2 mesa-utils libgl1
```
- **Cycles CPU funciona** (≈ 4 s/quadro em cena simples a 540×960, 24 spp + OIDN). **EEVEE em GL por software é ~40 s/quadro** — evitar.
- FFmpeg com `subtitles/ass`, `xfade`, `minterpolate`, `gblur`, `vignette`, `blend` basta para a pós. Converter a fonte WOFF → TTF com `fontTools` para o libass.

## Arquitetura (projeto `production/<slug>/blender/`)
- `lib/texlib.py` — texturas pintadas por código (numpy/PIL): tábuas, grama, solo, toras, telhas, vela, casco, bandeiras, notas, letreiros, tecidos; pinceladas semitransparentes dão o aspecto "pintado à mão".
- `lib/mats.py` — materiais Cycles: Principled + imagem/ruído, AO de contato, **neblina atmosférica por distância** (Camera Data → Mix com Emission), raios de luz falsos (planos camera-only), emissivos.
- `lib/nature.py`, `ships.py`, `deck.py`, `props.py` — modelagem procedural em numpy → malhas fundidas (milhares de lâminas de grama, flores, folhas em UMA malha; instâncias por *linked duplicates*).
- `lib/char.py`, `pig.py`, `crowd.py` — **personagem cut-out 3D**: discos/estádios planos com contorno atrás, pálpebra pesada, tecidos; cápsulas para membros; sombras reais; multidão enxuta.
- `lib/anim.py`, `lib/shots.py` — atuação/câmera como **funções puras de t**, ancoradas nos timestamps reais da voz; `check_framing.py` projeta cada personagem na câmera e acusa quem sai do quadro 9:16.
- `render_shot.py` / `render_all.sh` — um processo por plano; **pass 1 = quadros pares (15 fps), pass 2 = ímpares**; retomável.
- `post.py` — dissolve por alfa (overlay+fade), grade split-tone, bloom, vinheta, grão, legendas ASS, áudio.

## Armadilhas do Blender 5.x encontradas (poupam horas)
1. `scene.cycles.film_exposure` é **multiplicador** (padrão 1.0). Pôr 0 zera a luz (renders pretos). Use `scene.view_settings.exposure` (EV).
2. Meshes **compartilhados** guardam o material na malha: dois objetos com a mesma malha ficam com o mesmo material. Use slot `link='OBJECT'`.
3. Sky Texture: tipos `SINGLE_SCATTERING/MULTIPLE_SCATTERING/PREETHAM/HOSEK_WILKIE`; propriedade `aerosol_density` (não `dust_density`). Para o céu saturado do canal, **degradê próprio** (TexCoord.Object → Z → ColorRamp) é melhor que o físico.
4. Cápsulas 3D de contorno e preenchimento: o contorno de raio maior "fura" na frente — deslocar o contorno para trás por `(r_contorno − r_preenchimento) + ε`.
5. Look-dev: `Standard` dá o azul saturado do canal; `AgX` fica apagado. Calibrar brilho médio ≈ 0,56 (referência) com EV e a grade do FFmpeg.
6. Clarão de tiro branco some contra nuvens: usar camadas laranja → amarelo → branco e fumaça cinza.

## Orçamento de render (540×960, 12 spp + OIDN, 4 vCPU)
≈ 6–10 s/quadro (cenas com grama densa + DOF). Piloto de 21 s: ≈ 360 quadros/passada (≈ 45 min). Usar a passada 1 (15 fps) para ver o resultado cedo e completar para 30 fps depois.

## Método de fidelidade (obrigatório quando houver referência)
1. Extrair os quadros das gravações e das renders com FFmpeg; montar lado a lado (referência × meu).
2. Rodar `scripts/fidelity_metrics.py ref=... meu=...`: Laplacian (detalhe), densidade de bordas, contraste local, saturação, brilho, colorfulness, vinheta.
3. Só aprovar quando as métricas ficarem na faixa da referência **e** a comparação visual passar; registrar no `qa/fidelity-report.md`.
