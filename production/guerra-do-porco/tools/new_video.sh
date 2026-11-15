#!/usr/bin/env bash
# Cria um NOVO vídeo (production/<slug>/) a partir do toolchain reutilizável deste projeto: bibliotecas 3D (personagens cut-out com contorno irregular, multidão, objetos de cena, texturas
# pintadas por código, luz/câmera), pipeline de render/montagem/QA, schemas e docs — com esqueletos mínimos do que é específico da história (roteiro, pesquisa, planos, cenário).
# Depois de criar, roda um SMOKE TEST: renderiza 1 quadro 3D do plano de exemplo. Uso:  tools/new_video.sh <slug> "<Título>" [--no-smoke]      (DEST_ROOT=<pasta> cria fora de production/)
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)"; SLUG="${1:?uso: new_video.sh <slug> \"Título\" [--no-smoke]}"; TITLE="${2:-$SLUG}"; DEST_ROOT="${DEST_ROOT:-$(dirname "$SRC")}"; DST="$DEST_ROOT/$SLUG"
[[ "$SLUG" =~ ^[a-z0-9-]+$ ]] || { echo "slug inválido (use a-z, 0-9 e hífen)"; exit 2; }
[ -e "$DST" ] && { echo "já existe: $DST"; exit 1; }
mkdir -p "$DST"/{research/sources,script,storyboard,design,audio,stems,renders,qa,registry,assets/licenses,publish,docs,montage,tools,schemas,blender/out}
# ---- reutilizável: copiado ----
tar -C "$SRC/blender" --exclude=__pycache__ --exclude=out --exclude='tex/*.png' --exclude='lookdev_*.py' --exclude=lib/shots.py --exclude=lib/sets.py --exclude=sheets.py --exclude=motion_test.py -cf - . | tar -C "$DST/blender" -xf -
cp "$SRC/blender/sheets.py" "$SRC/blender/motion_test.py" "$DST/blender/" 2>/dev/null || true
for f in "$SRC"/tools/*.py "$SRC"/tools/*.sh; do b="$(basename "$f")"; case "$b" in new_video.sh|build_audio.py|make_storyboard.py|make_registry.py|make_report.py|build_voice_edge_tts_LEGADO.py|fix_tokens.py) ;; *) cp "$f" "$DST/tools/";; esac; done
cp "$SRC"/schemas/*.json "$DST/schemas/"; cp "$SRC/docs/HOWTO-novo-video.md" "$DST/docs/" 2>/dev/null || true
cp "$SRC/montage/index.ts" "$SRC/montage/Root.tsx" "$SRC/montage/Montage.tsx" "$DST/montage/"; cp "$SRC/package.json" "$SRC/package-lock.json" "$SRC/remotion.config.ts" "$SRC/tsconfig.json" "$DST/" 
NM="$(readlink -f "$SRC/node_modules" 2>/dev/null || true)"; [ -n "$NM" ] && [ -d "$NM" ] && ln -sfn "$NM" "$DST/node_modules"
# ---- esqueletos específicos da história ----
T="$SRC/tools/templates"; cp "$T/build_audio_events.py.tpl" "$DST/tools/build_audio.py"; chmod +x "$DST"/tools/*.sh
sed "s/@TITLE@/$TITLE/g" "$T/shots_demo.py.tpl" > "$DST/blender/lib/shots.py"; sed "s/@TITLE@/$TITLE/g" "$T/sets_demo.py.tpl" > "$DST/blender/lib/sets.py"; sed "s/@TITLE@/$TITLE/g" "$T/LICENSES.md.tpl" > "$DST/assets/licenses/LICENSES.md"
python3 - "$DST" "$SLUG" "$TITLE" "$T" <<'PY'
import json, os, sys
dst, slug, title, T = sys.argv[1:5]
# anim.py: troca o bloco de tempo/EDL da história pelo bloco genérico (lê storyboard/shots.json)
p = f"{dst}/blender/lib/anim.py"; s = open(p, encoding='utf-8').read(); a = s.index('# ---------------- timing ----------------'); b = s.index('# ---------------- atuação')
open(p, 'w', encoding='utf-8').write(s[:a] + open(f"{T}/anim_timeline.py.tpl", encoding='utf-8').read() + s[b:])
W = {"voice": "(preencher: tools/build_voice.py)", "license_voice": "(preencher)", "total": 4.0, "lines": [{"id": "L1", "shot": "S1", "beat": "gancho", "text": "Exemplo de fala.", "pause_before": 0.1, "start": 0.4, "end": 2.0, "dur": 1.6}],
     "words": [{"line": "L1", "text": "Exemplo", "start": 0.4, "end": 1.0}, {"line": "L1", "text": "de", "start": 1.0, "end": 1.2}, {"line": "L1", "text": "fala.", "start": 1.2, "end": 2.0}]}
json.dump(W, open(f"{dst}/script/word-timings.json", "w"), ensure_ascii=False, indent=1)
json.dump({"title": title, "language": "pt-BR", "fiction": False, "note": "esqueleto — escreva as linhas; cada linha: id, shot, beat, text, pause_before, intent", "lines": [{"id": "L1", "shot": "S1", "beat": "gancho", "text": "Exemplo de fala.", "pause_before": 0.1, "intent": "curiosidade"}]},
          open(f"{dst}/script/story.json", "w"), ensure_ascii=False, indent=1)
json.dump({"edl": "storyboard/shots.json (edite à mão)", "shot_count": 1, "mean_shot_s": 4.0, "shots": [{"id": "S1", "scene": "S1", "start": 0.0, "end": 4.0, "dur": 4.0, "lines": ["L1"], "beat": "GANCHO", "purpose": "plano de exemplo", "camera": "push-in leve", "action": "personagem em idle", "audio": "vento"}]},
          open(f"{dst}/storyboard/shots.json", "w"), ensure_ascii=False, indent=1)
json.dump({"projeto": title, "data_da_checagem": "", "regra": "cada afirmação central do roteiro tem ≥ 2 fontes independentes lidas, com trecho literal e confiança", "fontes": {}, "afirmacoes": [], "limitacoes": []}, open(f"{dst}/research/claims.json", "w"), ensure_ascii=False, indent=1)
json.dump({"title": title, "slug": slug, "language": "pt-BR", "format": "short", "width": 1080, "height": 1920, "fps": 30, "durationSeconds": 4.0, "visualEngine": "blender 5.3 Cycles CPU (bpy) + remotion + ffmpeg", "visualGeneration": "procedural-code-only",
           "captions": {"wordsPerCard": "1-2", "keepPunctuation": True, "font": "Montserrat 800"}, "audio": {"sampleRate": 44100, "channels": 2, "targetIntegratedLufs": -14, "maxTruePeakDbtp": -1.5}, "voice": "(preencher)", "tts": None},
          open(f"{dst}/production.json", "w"), ensure_ascii=False, indent=1)
open(f"{dst}/README.md", "w", encoding="utf-8").write(f"# {title}\n\nCriado por `tools/new_video.sh`. Siga `docs/HOWTO-novo-video.md` (roteiro → pesquisa → voz → planos → render → montagem → QA → scorecard).\n")
PY
cat > "$DST/.gitignore" <<'GI'
blender/out/
blender/tex/*.png
__pycache__/
montage/public/
montage/data.json
renders/_montage_raw.mp4
renders/_captions/
research/sources/
GI
echo "criado: $DST"
if [ "${3:-}" != "--no-smoke" ]; then
  echo "== smoke test: 1 quadro 3D do plano de exemplo (135x240, 4 amostras) =="
  ( cd "$DST" && OUT="$DST/out/smoke" GRASS=1500 python3 blender/stills.py 135 240 4 S1:1.0 2>&1 | tail -2 && test -s "$DST/out/smoke/st_S1_1.0.png" && echo "SMOKE OK: out/smoke/st_S1_1.0.png" )
fi
echo "próximo: leia $DST/docs/HOWTO-novo-video.md"
