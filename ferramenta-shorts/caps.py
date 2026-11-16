#!/usr/bin/env python3
"""Make caps.ass from work/words.json + work/phrases.json (timing.py output). Chunks of <=3 words, never crossing a phrase.
Style (measured on Ricks Clips): Inter Black 88 px, white, black outline 6, centred at y=1338 of 1920 (~70%), 1-2 words. Burn with: ffmpeg -vf subtitles=caps.ass:fontsdir=/usr/share/fonts/opentype/inter"""
import json
W = json.load(open('work/words.json')); ph = json.load(open('work/phrases.json'))['phrases']
chunks = []; i = 0
for p in ph:
    n = len(p['text'].split()); ws = W[i:i + n]; i += n; k = 0
    while k < len(ws):
        m = 2 if (len(ws) - k >= 2 and len(ws[k]['w']) + len(ws[k + 1]['w']) <= 15) else 1
        g = ws[k:k + m]; chunks.append((g[0]['s'], g[-1]['e'], ' '.join(x['w'] for x in g))); k += m
ts = lambda t: f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Inter Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,6,3,5,50,50,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
ev = []
for j, (s, e, t) in enumerate(chunks):
    nxt = chunks[j + 1][0] if j + 1 < len(chunks) else 1e9; e2 = min(max(e + 0.25, s + 0.5), nxt - 0.02)
    ev.append(f"Dialogue: 0,{ts(s)},{ts(e2)},Cap,,0,0,0,,{{\\an5\\pos(540,1338)\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)\\fad(30,30)}}{t}")
open('caps.ass', 'w').write(hdr + '\n'.join(ev) + '\n'); print(len(chunks), 'caption chunks -> caps.ass')
