#!/usr/bin/env bash
# uso: ./frase_a_frase.sh <id> <mp4>  -> 1 quadro no MEIO de cada frase, montado em /tmp/ff_<id>.jpg (conferir se a imagem mostra o que a frase diz)
ID="$1"; MP4="$2"; D=/tmp/ff_$ID; rm -rf $D; mkdir -p $D
python3 - "$ID" "$MP4" "$D" <<'P'
import json,subprocess,sys
i,mp4,d=sys.argv[1:4]
ph=json.load(open(f'stories/{i}/work/phrases.json'))['phrases']
for k,p in enumerate(ph):
    a=p['s']; b=p['e']; t=(a+b)/2
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{t:.2f}','-i',mp4,'-frames:v','1','-vf','scale=270:-1',f'{d}/f{k:02d}.jpg'])
    print(k,f'{t:.1f}s',p.get('text',p.get('say',''))[:90])
P
ffmpeg -y -loglevel error -pattern_type glob -i "$D/f*.jpg" -vf "tile=6x5" -frames:v 1 /tmp/ff_$ID.jpg
