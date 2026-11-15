# A Guerra do Porco — pipeline Blender (Cycles CPU) + FFmpeg

Pré-requisitos: `pip install bpy` (Blender 5.x) + libs GL (ver `.claude/skills/.../references/blender-cycles-route.md`), FFmpeg, Python 3.13.

```bash
# 1) voz + timings reais (edge-tts) e áudio sintetizado
python3 tools/build_voice.py && python3 tools/build_audio.py && python3 tools/mix.py && python3 tools/make_meta.py
# 2) conferir enquadramento (projeta personagens na câmera 9:16)
for s in S1 S2 S3 S4 S5 S6; do python3 blender/check_framing.py $s; done
# 3) quadros-chave (look-dev) e animatic
python3 blender/stills.py 540 960 14 S1:0.0 S3:9.5 S5:16.8
# 4) render: passada 1 (quadros pares = 15 fps) e passada 2 (ímpares = 30 fps)
blender/render_all.sh 540 960 12 50000 2 0 && blender/render_all.sh 540 960 12 50000 2 1
# 5) pós (dissolves, grade, bloom, vinheta, grão, legendas, áudio) e QA
python3 blender/post.py blender/out/frames renders/pilot_540.mp4 --every 2     # passada 1
python3 blender/post.py blender/out/frames renders/pilot_540.mp4               # 30 fps completo
python3 tools/qa.py renders/pilot_540.mp4 pilot 540x960@30 && python3 tools/qa_extra.py renders/pilot_540.mp4 pilot_extra
```
Tudo é função pura do tempo (`lib/anim.py`), ancorado em `script/word-timings.json`. Texturas são geradas por `lib/texlib.py` (determinístico, seed fixo).
