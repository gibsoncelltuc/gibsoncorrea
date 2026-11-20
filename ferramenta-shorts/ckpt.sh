#!/usr/bin/env bash
# ckpt.sh <id> [msg] -- salva o progresso no git (trechos mp4 ja' codificados + estado pequeno do video) e empurra para o remoto,
# assim um reinicio da sessao/container nao perde o trabalho: ao voltar, o repositorio ja' traz os trechos e o render continua dali.
# Seguro para chamar sempre: sem git/remoto, ou com CKPT_GIT=0, nao faz nada. Nunca falha o render.
cd "$(dirname "$0")"; ID="$1"; MSG="${2:-ckpt}"
[ "${CKPT_GIT:-1}" = "0" ] && exit 0; git rev-parse --git-dir >/dev/null 2>&1 || exit 0; git remote | grep -q . || exit 0
exec 9>logs/ckpt.lock; flock -w 300 9 || exit 0
R=$(git rev-parse --show-toplevel); BR=$(git rev-parse --abbrev-ref HEAD)
cd "$R"; P=$(realpath --relative-to="$R" "$OLDPWD")
git add -A -- "$P/ckpt/$ID" "$P/stories/$ID" "$P/videos/$ID" 2>/dev/null
git diff --cached --quiet && exit 0
git commit -q -m "ckpt($ID): $MSG" -- "$P/ckpt/$ID" "$P/stories/$ID" "$P/videos/$ID" >/dev/null 2>&1 || exit 0
for i in 1 2 3 4; do git push -q -u origin "$BR" >/dev/null 2>&1 && exit 0; sleep $((i*3)); done
echo "ckpt: push falhou (commit local mantido)"; exit 0
