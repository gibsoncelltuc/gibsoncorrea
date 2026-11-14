#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/external/claude-animated-shorts"
REPO="https://github.com/mromidev/claude-animated-shorts.git"
if [[ -e "$DEST" ]]; then
  echo "Destino já existe: $DEST" >&2
  echo "Revise o conteúdo manualmente; o script não sobrescreve clones existentes." >&2
  exit 2
fi
mkdir -p "$ROOT/external"
git clone --depth 1 "$REPO" "$DEST"
COMMIT="$(git -C "$DEST" rev-parse HEAD)"
printf '%s\n' "$COMMIT" > "$ROOT/external/benchmark-resolved-commit.txt"
echo "Clone concluído. Commit: $COMMIT"
echo "IMPORTANTE: não execute scripts do benchmark antes de auditar README, SKILL, LICENSE, dependências e scripts."
