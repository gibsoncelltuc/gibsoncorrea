# Notas de direção de arte
- Look: 2D cartoon em mundo 3D toon. Materiais `MeshToonMaterial` com rampa de 4 passos (168/206/236/255): sombras nunca pretas.
- Luz: sol quente (`#ffc27a`, intensidade 2.7) contra hemisfério azul/roxo; fill frio `#7185c0`. Ambientes por tempo: `dawn`, `morning`, `autumn`, `dusk`, `winter`, `room` (interpolados por `envAt`).
- Verde nunca lidera: folhagem em ocre/âmbar; QA mede fração de pixels dominados por verde (máx 1.6%).
- Câmera: baixa, fov 50–64, **sempre em movimento** (smootherstep + arco + sway), um lugar = um plano contínuo (sem cortes dentro do mesmo lugar). Roll no close do zombador.
- Pós: textura de papel (`public/paper.png`, multiply 20%), vinheta radial, split-tone quente/frio (soft-light), grain no papel. DoF/bloom 3D **não** aplicados (SwiftShader) — ver limitações.
- Cenário vivo: ~1.100+ tufos instanciados (InstancedMesh), nuvens, brilhos de água animados, neve instanciada (260 flocos), fumaça da padaria, bolhas do naufrágio, respingos/ondas.
- Fonte das legendas: Montserrat 800 (OFL), 76 px, contorno 15 px `#120e1a`, y≈70% do quadro, pop 108%→100% em 0.09 s, 1–2 palavras, sem ponto final.
