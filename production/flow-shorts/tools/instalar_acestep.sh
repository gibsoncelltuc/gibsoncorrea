#!/usr/bin/env bash
# Instala o ACE-Step 1.5 (acestep.cpp, MIT) em CPU. ~10 GB de disco, compila em ~2 min, baixa modelos em ~3 min.
set -euo pipefail
mkdir -p /home/user/musica && cd /home/user/musica
[ -d acestep.cpp ] || git clone --depth 1 --recurse-submodules --shallow-submodules https://github.com/ServeurpersoCom/acestep.cpp
cd acestep.cpp
pip install -q huggingface_hub --break-system-packages || true
./models.sh --lm 1.7B
rm -rf build && mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON && cmake --build . --config Release -j"$(nproc)"
