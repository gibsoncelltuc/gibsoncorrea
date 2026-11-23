# FERRAMENTA SHORTS v10 FINAL — 2 MODOS 100% LOCAIS (SEM API EXTERNA)

A ferramenta opera exclusivamente com **código local** e **Blender 3D local**, sem chamar nenhuma API externa ou IA generativa de vídeo.
No Claude Desktop, basta pedir **Modo 1** ou **Modo 2**:

| Modo | Nome | Comando | O que faz |
|---|---|---|---|
| **Modo 1** | **100% Código** | `python3 mkvideo.py <id> --modo 1` | Motor v10 completo (30 fps reais): boneco 2D redesenhado fiel ao estilo `@RicksClips3000`, timeline explícita `acoes`, rosto roxo + vapor de fúria, *speed lines*, *whip-pan* e punch-in de câmera. |
| **Modo 2** | **Híbrido Blender (100% local)** | `python3 mkvideo.py <id> --modo 2` + `python3 hero_shots.py <id> --modo 2 --base <base.mp4> --out <final.mp4>` | Renderiza os beats marcados com `"hero_shot": true` localmente no **Blender** (`blender/hero_render.py` → `stories/<id>/blender_clips/bN.mp4`) e costura automaticamente no vídeo base com áudio e legendas. |
