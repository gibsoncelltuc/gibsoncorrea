#!/usr/bin/env bash
# Instala/verifica tudo que o pipeline Ricks 3D Toon precisa (mesmo script gravado no ambiente "gibsoncorrea"). Uso: sudo bash tools/setup_env.sh
# Pipeline Ricks 3D Toon: Blender 5.x (modulo bpy), FFmpeg, TTS e bibliotecas. Idempotente; nunca aborta a sessao.
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq || true
apt-get install -y -qq --no-install-recommends ffmpeg xvfb libgl1 libgl1-mesa-dri libglx-mesa0 libegl1 \
  libegl-mesa0 libgbm1 libopengl0 libxi6 libxxf86vm1 libxfixes3 libxrender1 libsm6 libxkbcommon0 libdrm2 mesa-utils || true
pip install -q --root-user-action=ignore bpy edge-tts fonttools brotli numpy pillow scipy scikit-image opencv-python-headless imageio || true
cat > /usr/local/bin/blender <<'EOW'
#!/usr/bin/env python3
# Comando `blender` (modo background) sobre o modulo bpy: --version, -b, arquivo.blend, -E, -o, -s, -e, -f, -a, -P, --python-expr, --
import sys, runpy
a = sys.argv[1:]
import bpy
if '--version' in a or '-v' in a:
    print('Blender', bpy.app.version_string); sys.exit(0)
sys.argv = ['blender'] + a
sc = lambda: bpy.context.scene
i = 0
while i < len(a):
    x = a[i]
    if x == '--': break
    if x.endswith('.blend'): bpy.ops.wm.open_mainfile(filepath=x)
    elif x in ('-E', '--engine'): i += 1; sc().render.engine = a[i]
    elif x in ('-o', '--render-output'): i += 1; sc().render.filepath = a[i]
    elif x in ('-s', '--frame-start'): i += 1; sc().frame_start = int(a[i])
    elif x in ('-e', '--frame-end'): i += 1; sc().frame_end = int(a[i])
    elif x in ('-f', '--render-frame'):
        i += 1; s0, e0 = sc().frame_start, sc().frame_end; sc().frame_start = sc().frame_end = int(a[i])
        bpy.ops.render.render(animation=True); sc().frame_start, sc().frame_end = s0, e0
    elif x in ('-a', '--render-anim'): bpy.ops.render.render(animation=True)
    elif x in ('-P', '--python'): i += 1; runpy.run_path(a[i], run_name='__main__')
    elif x == '--python-expr': i += 1; exec(a[i], {'bpy': bpy})
    i += 1
EOW
chmod +x /usr/local/bin/blender
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
if [ -f "$ROOT/production/tome-lago/package-lock.json" ]; then (cd "$ROOT/production/tome-lago" && npm install --no-audit --no-fund --silent) || true; fi
# Remotion/Three.js do piloto reaproveitam o node_modules do projeto tome-lago
if [ -d "$ROOT/production/guerra-do-porco" ]; then ln -sfn ../tome-lago/node_modules "$ROOT/production/guerra-do-porco/node_modules"; fi
blender --version | head -n 1
ffmpeg -version | head -n 1
python3 -c "import scipy, skimage, cv2; print('scipy', scipy.__version__, 'skimage', skimage.__version__, 'opencv', cv2.__version__)"
(cd "$ROOT/production/guerra-do-porco" && npx --no-install remotion versions 2>/dev/null | head -n 2)
true
