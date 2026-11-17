#!/usr/bin/env python3
"""Monta um Short a partir de um arquivo de configuração JSON.

Uso: python3 montar_short.py config.json

O JSON descreve: música, trechos de vídeo (clipe, início, duração, zoom, janela da música),
transições e legendas. Gera vídeo vertical 1080x1920 com:
  - transições entre trechos (e whoosh discreto em cada uma),
  - push-in suave de câmera,
  - zoom de reenquadramento opcional por trecho (ex.: esconder o topo do quadro),
  - legendas em inglês (fonte arredondada), no terço inferior, deixando o canto inferior esquerdo livre para o Libras,
  - volume padrão do YouTube (-14 LUFS) e fade final.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "assets", "FredokaOne-Regular.ttf")


def caption_png(text, path, size=80):
    font = ImageFont.truetype(FONT, size)
    maxw = 960
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    words = text.split()
    if probe.textlength(text, font=font) <= maxw:
        lines = [text]
    else:  # quebra em 2 linhas equilibradas (evita palavra solta)
        best = None
        for k in range(1, len(words)):
            a, b = " ".join(words[:k]), " ".join(words[k:])
            m = max(probe.textlength(a, font=font), probe.textlength(b, font=font))
            if best is None or m < best[0]:
                best = (m, [a, b])
        lines = best[1]
    lh = int(size * 1.18)
    pad = 36
    img = Image.new("RGBA", (W, lh * len(lines) + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=font)
        x, y = (W - tw) / 2, pad + i * lh
        d.text((x + 0, y + 7), ln, font=font, fill=(20, 40, 90, 120), stroke_width=14, stroke_fill=(20, 40, 90, 120))  # sombra
        d.text((x, y), ln, font=font, fill=(255, 255, 255, 255), stroke_width=12, stroke_fill=(32, 92, 190, 255))
    img.save(path)
    return img.height


def main(cfg_path):
    cfg = json.load(open(cfg_path))
    base = os.path.dirname(os.path.abspath(cfg_path))
    rp = lambda p: p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))
    segs = cfg["segments"]
    TR = cfg.get("transition", 0.35)
    fx = cfg.get("effects", ["smoothleft", "zoomin", "circleopen", "fadewhite"])
    music = rp(cfg["music"])
    total = sum(s["dur"] for s in segs)
    tmp = tempfile.mkdtemp()
    args, fc = [], []
    # ---- vídeo
    for i, s in enumerate(segs):
        args += ["-i", rp(s["clip"])]
        z = s.get("zoom", 1.0)
        ss = s.get("start", 0.0)
        pad = f",tpad=stop_mode=clone:stop_duration={TR}" if i < len(segs) - 1 else ""
        f = f"[{i}:v]fps=24,scale={W}:{H},setsar=1,trim=start={ss}:duration={s['dur']},setpts=PTS-STARTPTS"
        if z > 1.0:  # reenquadra ancorado embaixo (corta o topo do quadro)
            f += f",crop=w={W}/{z}:h={H}/{z}:x=({W}-{W}/{z})/2:y={H}-{H}/{z},scale={W}:{H}:flags=lanczos"
        f += pad
        f += f",scale=w='trunc({W}*(1+0.05*min(t,{s['dur']})/{s['dur']})/2)*2':h=-2:eval=frame,crop={W}:{H}"
        f += ",eq=saturation=1.07:contrast=1.03,format=yuv420p"
        fc.append(f + f"[v{i}]")
    prev, t = "v0", 0.0
    for k in range(len(segs) - 1):
        t += segs[k]["dur"]
        fc.append(f"[{prev}][v{k+1}]xfade=transition={fx[k % len(fx)]}:duration={TR}:offset={t:.3f}[x{k}]")
        prev = f"x{k}"
    # ---- legendas (PNG por linha)
    cap_idx = len(segs) + 1  # entrada 0..n-1 clipes, n = música
    args += ["-i", music]
    music_idx = len(segs)
    caps = cfg.get("captions", [])
    cap_y = cfg.get("caption_y", 1180)
    for j, c in enumerate(caps):
        png = os.path.join(tmp, f"cap{j}.png")
        caption_png(c["text"], png, c.get("size", 80))
        args += ["-loop", "1", "-t", f"{c['end']-c['start']+0.1:.2f}", "-i", png]
        d = c["end"] - c["start"]
        fc.append(f"[{cap_idx+j}:v]format=rgba,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st={max(d-0.12,0):.2f}:d=0.12:alpha=1,"
                  f"setpts=PTS+{c['start']}/TB[c{j}]")
        out = f"o{j}"
        fc.append(f"[{prev}][c{j}]overlay=x=0:y={c.get('y', cap_y)}:eof_action=pass:enable='between(t,{c['start']},{c['end']})'[{out}]")
        prev = out
    fc.append(f"[{prev}]fade=t=out:st={total-0.6:.2f}:d=0.6[vout]")
    # ---- áudio: janelas da música coladas + whooshes
    parts = []
    for i, s in enumerate(segs):
        m0 = s["music_start"]; fi = s.get("fade_in", 0.03); fo = s.get("fade_out", 0.05)
        fc.append(f"[{music_idx}:a]atrim=start={m0}:duration={s['dur']},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d={fi},afade=t=out:st={s['dur']-fo}:d={fo},aformat=sample_rates=48000:channel_layouts=stereo[ma{i}]")
        parts.append(f"[ma{i}]")
    fc.append("".join(parts) + f"concat=n={len(segs)}:v=0:a=1[mus]")
    sfx, t = [], 0.0
    for k in range(len(segs) - 1):
        t += segs[k]["dur"]
        ms = int(max(t - 0.06, 0) * 1000)
        if fx[k % len(fx)] == "fadewhite":
            fc.append(f"aevalsrc='(sin(2*PI*2093*t)+0.8*sin(2*PI*2637*t)+0.6*sin(2*PI*3136*t))*exp(-5*t)*0.10':d=0.7:s=48000,adelay={ms}|{ms}[s{k}]")
        else:
            fc.append(f"anoisesrc=d=0.45:c=pink:a=0.5:r=48000,bandpass=f=1700:w=1.6,afade=t=in:d=0.15,afade=t=out:st=0.18:d=0.27,volume=0.16,aformat=channel_layouts=stereo,adelay={ms}|{ms}[s{k}]")
        sfx.append(f"[s{k}]")
    n = 1 + len(sfx)
    fc.append(f"[mus]{''.join(sfx)}amix=inputs={n}:normalize=0:duration=first,loudnorm=I=-14:TP=-2:LRA=7,afade=t=out:st={total-1.4:.2f}:d=1.4[aout]")
    out = rp(cfg["out"])
    cmd = ["ffmpeg", "-v", "error", "-y"] + args + ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
           "-t", f"{total}", "-c:v", "libx264", "-preset", "slow", "-crf", str(cfg.get("crf", 21)), "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "csv=p=0", out], capture_output=True, text=True)
    print(r.stdout.strip())


if __name__ == "__main__":
    main(sys.argv[1])
