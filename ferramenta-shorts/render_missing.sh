#!/usr/bin/env bash
# usage: render_missing.sh <story_pt_id> <N>   -> renders only the frames that are missing in out/<id>/frames, balanced over 3 shards (blocks of 30 frames, round-robin)
cd "$(dirname "$0")"; P=$1; N=$2; mkdir -p out/$P/frames logs
python3 - "$P" "$N" <<'PY'
import os, sys
P, N = sys.argv[1], int(sys.argv[2]); d = f"out/{P}/frames"
have = {int(f[1:5]) for f in os.listdir(d) if f.startswith('f') and f.endswith('.jpg')}
miss = [f for f in range(N) if f not in have]; B = 30; sh = [[], [], []]
for i in range(0, len(miss), B):
    blk = miss[i:i + B]; sh[(i // B) % 3].append(blk)
for k in range(3):
    rng = []
    for blk in sh[k]:
        a = blk[0]
        for x, y in zip(blk, blk[1:] + [None]):
            if y != x + 1: rng.append(f"{a}-{x}" if a != x else f"{a}"); a = y
    open(f"logs/{P}_ranges_{k}.txt", "w").write(",".join(rng))
print(len(miss), "frames missing;", [sum(len(b) for b in s) for s in sh], "per shard")
PY
for k in 0 1 2; do R=$(cat logs/${P}_ranges_$k.txt); [ -n "$R" ] && WEB=$(cd ../webs/$P && pwd) RESUME=1 node render.mjs out/$P/frames "$R" > logs/${P}_$k.log 2>&1 & done; wait
