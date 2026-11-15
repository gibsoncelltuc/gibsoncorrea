# A Guerra do Porco — piloto de 21 s (9:16, 540×960 @ 30 fps)
Short animado 100 % por código seguindo a skill **Ricks 3D Toon Story Orchestrator V2** (+ perfil v3.1 + referência visual do canal Ricks Clips). Mundo e atores em **3D no Blender 5.3 (Cycles CPU)**, pós e áudio no **FFmpeg**. Sem gerador de vídeo/imagem por IA.

```
research/      fact-check (Guerra do Porco, 1859) e fontes
script/        story.json, roteiro, voiceover, word-timings.json (tempos reais da voz)
storyboard/    shots.json (6 planos)
design/        bíblia de personagens e notas de direção de arte
blender/       pipeline 3D: lib/ (modelagem, texturas, rig, animação, planos), render_shot.py, render_all.sh, post.py
tools/         voz (edge-tts), áudio sintetizado, mix -14 LUFS, QA, fidelidade vs referência, manifest, contact sheet, setup_env.sh
audio/ stems/  mix final e stems (voz, música, SFX, ambiência) em FLAC
renders/       vídeo final, legendas (.srt/.ass), folhas de contato
qa/            relatórios de QA e fidelidade, scorecard
registry/      registry de assets/personagens/props reutilizáveis
assets/licenses/ procedência e licenças
publish/       título, descrição, hashtags
src/           código histórico (versão Remotion/Three.js rejeitada pelo usuário; mantido só como registro)
```

## Reproduzir
```bash
sudo bash tools/setup_env.sh            # Blender (bpy) + FFmpeg + dependências (também gravado no ambiente "gibsoncorrea")
python3 tools/build_voice.py && python3 tools/build_audio.py && python3 tools/mix.py && python3 tools/make_meta.py
blender/render_all.sh 540 960 12 50000 2 0 && blender/render_all.sh 540 960 12 50000 2 1     # passada 1 (15 fps) + passada 2 (30 fps)
tools/montage.sh renders/pilot_540.mp4                   # Remotion (montagem + legendas) + FFmpeg (grade); alternativa só-FFmpeg: python3 blender/post.py blender/out/frames renders/pilot_540.mp4
python3 tools/qa.py renders/pilot_540.mp4 pilot 540x960@30 && python3 tools/qa_extra.py renders/pilot_540.mp4 pilot_extra
python3 tools/fidelity_report.py renders/pilot_540.mp4 <pasta_com_frames_de_referencia> && python3 tools/make_manifest.py && python3 tools/contact_sheet.py renders/pilot_540.mp4 renders/contact_540.png
```
Subir de resolução: `render_all.sh 1080 1920 24 90000 …` (tempo ≈ 4×); a pós se adapta ao tamanho dos quadros.
Detalhes do pipeline Blender: `blender/README.md`. Licenças: `assets/licenses/LICENSES.md` (⚠ voz `edge-tts`: regravar com voz licenciada antes de monetizar).
