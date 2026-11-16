#!/usr/bin/env bash
# usage: review_video.sh <video.mp4> <outprefix>   -> <outprefix>_sheet.jpg (1 frame / 1.5 s, with timestamps) + printed technical report
V="$1"; O="$2"; [ -f "$V" ] || { echo "no video"; exit 1; }
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames,duration -of default=nw=1 "$V" | tr '\n' ' '; echo
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels -of default=nw=1 "$V" | tr '\n' ' '; echo
echo -n "loudness: "; ffmpeg -hide_banner -nostats -i "$V" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|True peak|Peak:" | tr -s ' ' | tr '\n' ' '; echo
echo -n "freeze(>=0.7s): "; ffmpeg -hide_banner -nostats -i "$V" -vf "freezedetect=n=-60dB:d=0.7" -an -f null - 2>&1 | grep -c "freeze_start"
echo -n "black(>=0.2s): ";  ffmpeg -hide_banner -nostats -i "$V" -vf "blackdetect=d=0.2:pix_th=0.06" -an -f null - 2>&1 | grep -c "black_start"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V"); python3 - "$V" "$O" "$D" <<'PY'
import sys, subprocess, os, tempfile
from PIL import Image, ImageDraw
v, o, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
ts = [t * 1.5 for t in range(int(dur / 1.5))]; tmp = tempfile.mkdtemp(); ims = []
for k, t in enumerate(ts):
    p = os.path.join(tmp, "%03d.jpg" % k); subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "%.2f" % t, "-i", v, "-frames:v", "1", "-vf", "scale=216:384", p])
    im = Image.open(p).convert("RGB"); d = ImageDraw.Draw(im); d.rectangle((0, 0, 44, 14), fill=(0, 0, 0)); d.text((3, 2), "%.1fs" % t, fill=(255, 255, 255)); ims.append(im)
cols = 8; rows = (len(ims) + cols - 1) // cols; sh = Image.new("RGB", (216 * cols, 384 * rows), (20, 20, 20))
for k, im in enumerate(ims): sh.paste(im, ((k % cols) * 216, (k // cols) * 384))
sh.save(o + "_sheet.jpg", quality=86); print(o + "_sheet.jpg", sh.size)
PY
