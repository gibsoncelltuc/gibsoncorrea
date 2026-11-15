#!/usr/bin/env bash
# Take de teste: exporta do Blender (só ativos 3D) e renderiza no Three.js. Uso: three/take.sh <id1> <id2> ... (ids de edição) ; env: FPS=15 W=540 H=960 GRASS=20000
set -e; cd "$(dirname "$0")/.."; FPS=${FPS:-15}; W=${W:-540}; H=${H:-960}; G=${GRASS:-20000}
for e in "$@"; do
  env=golden; case $e in E34_grave) env=dusk;; E23_deck|E24_baynes) env=bright;; esac
  nice -n 5 python3 blender/export_gltf.py $e $FPS out/gltf/$e $G 2>&1 | grep -E "^OK|rror|Traceback"
  NODE_PATH=$(npm root -g) node three/render.cjs out/gltf/$e out/three/$e $W $H $env 0 999999 2.8 3.4 | tail -1
done
