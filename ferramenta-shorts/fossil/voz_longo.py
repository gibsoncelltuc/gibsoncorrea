# voz de cada bloco de um video longo: python3 voz_longo.py <roteiro.json> <dir>  -> <dir>/voz/bNN.mp3
import asyncio, json, os, sys, edge_tts
S = json.load(open(sys.argv[1])); D = sys.argv[2]; os.makedirs(f'{D}/voz', exist_ok=True)
async def main():
    for i, b in enumerate(S['blocos']):
        p = f'{D}/voz/b{i:02d}.mp3'
        if os.path.exists(p) and os.path.getsize(p) > 1000: continue
        for k in range(4):
            try: await edge_tts.Communicate(b['texto'], S['voz'], rate=S.get('rate', '+0%'), proxy=os.environ.get('HTTPS_PROXY')).save(p); break
            except Exception as e: print('retry', i, e); await asyncio.sleep(3)
    print('voz ok', len(S['blocos']))
asyncio.run(main())
