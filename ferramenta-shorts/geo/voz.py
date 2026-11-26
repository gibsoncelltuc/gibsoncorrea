# voz em ingles por trecho (gancho + itens) com o tempo de cada palavra: geo/out/<id>/voz/sNN.mp3 + palavras.json
import asyncio, json, os, sys, edge_tts
VOZ, RATE = 'en-US-AndrewNeural', '+10%'
async def um(txt, mp3, voz=None):
    c = edge_tts.Communicate(txt, voz or VOZ, rate=RATE, boundary='WordBoundary', proxy=os.environ.get('HTTPS_PROXY'))
    pal = []
    with open(mp3, 'wb') as f:
        async for ch in c.stream():
            if ch['type'] == 'audio': f.write(ch['data'])
            elif ch['type'] == 'WordBoundary': pal.append([ch['offset'] / 1e7, (ch['offset'] + ch['duration']) / 1e7, ch['text']])
    return pal
async def main(rid):
    R = json.load(open(f'roteiros/{rid}.json' if os.path.exists(f'roteiros/{rid}.json') else f'guerras/{rid}.json')); d = f'out/{rid}/voz'; os.makedirs(d, exist_ok=True)
    txts = [R['hook']] + [i['say'] for i in R['items']]; tudo = []
    for k, t in enumerate(txts):
        for tent in range(4):
            try: tudo.append(await um(t, f'{d}/s{k:02d}.mp3', R.get('voz'))); break
            except Exception as e: print('retry', k, e); await asyncio.sleep(3)
    json.dump(tudo, open(f'{d}/palavras.json', 'w'), ensure_ascii=False)
    print(rid, 'ok', len(tudo))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for rid in sys.argv[1:]: asyncio.run(main(rid))
