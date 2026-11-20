#!/usr/bin/env bash
# instala o que falta (ffmpeg, node/playwright, edge-tts, Pillow, numpy, fonte Inter)
cd "$(dirname "$0")"; pip install -q edge-tts pillow numpy; [ -d node_modules/playwright ] || npm i playwright >/dev/null 2>&1; npx playwright install chromium
mkdir -p ~/.fonts && cp fonts/*.otf ~/.fonts/ 2>/dev/null && fc-cache -f >/dev/null 2>&1; which ffmpeg node python3 edge-tts
