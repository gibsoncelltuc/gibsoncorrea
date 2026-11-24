#!/usr/bin/env bash
# CONFERENCIA FRASE A FRASE (24/11, Gibson): 1 quadro do mp4 no meio de cada frase com a frase escrita embaixo; OLHAR se a imagem mostra a frase. uso: frase_a_frase.sh <branch> <id> <mp4> <saida.jpg>  -> 1 quadro no meio de cada frase (timing da sessao), rotulado com a frase
BR=$1; ID=$2; M=$3; OUT=$4; D=$(mktemp -d); cd /home/user/gibsoncorrea
git show origin/$BR:ferramenta-shorts/stories/$ID/work/phrases.json > $D/ph.json 2>/dev/null || cp ferramenta-shorts/stories/$ID/work/phrases.json $D/ph.json
python3 - "$D" "$M" "$OUT" <<'PY'
import json,sys,subprocess
from PIL import Image,ImageDraw
d,m,out=sys.argv[1:]; P=json.load(open(d+'/ph.json'))['phrases']; ims=[]
for i,p in enumerate(P):
    t=(p['s']+p['e'])/2; f=f'{d}/q{i}.jpg'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',m,'-frames:v','1','-vf','scale=240:427',f])
    im=Image.open(f); c=Image.new('RGB',(240,500),'white'); c.paste(im,(0,0)); dr=ImageDraw.Draw(c)
    txt=p['text']; lines=[txt[j:j+40] for j in range(0,len(txt),40)][:4]
    for k,l in enumerate(lines): dr.text((3,430+k*17),l,fill='black')
    ims.append(c)
n=len(ims); cols=6; rows=(n+cols-1)//cols; W=Image.new('RGB',(240*cols,500*rows),'black')
for i,im in enumerate(ims): W.paste(im,((i%cols)*240,(i//cols)*500))
W.save(out,quality=82); print(n,'frases')
PY
rm -rf $D
