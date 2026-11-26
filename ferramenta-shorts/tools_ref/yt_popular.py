import json, re, sys, urllib.request
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
H = {'User-Agent': UA, 'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'SOCS=CAI; CONSENT=YES+1', 'Content-Type': 'application/json'}
def walk(o, key, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: out.append(v)
            walk(v, key, out)
    elif isinstance(o, list):
        for v in o: walk(v, key, out)
    return out
tab = sys.argv[1]; d = json.load(open(f'channel_{tab}.json')); it = json.load(open('innertube.json'))
chips = walk(d, 'chipCloudChipRenderer', []) + walk(d, 'chipViewModel', [])
tok = None
for c in chips:
    t = c.get('text'); t = t if isinstance(t, str) else (t or {}).get('simpleText')
    if t == 'Popular': tok = walk(c, 'token', [])[0]
print('token', bool(tok))
def parse(o, out):
    for s in walk(o, 'shortsLockupViewModel', []):
        vid = (walk(s, 'videoId', []) or [None])[0]; acc = s.get('accessibilityText', ''); title = (s.get('overlayMetadata', {}).get('primaryText', {}) or {}).get('content'); views = (s.get('overlayMetadata', {}).get('secondaryText', {}) or {}).get('content')
        out.append({'id': vid, 'title': title, 'views': views, 'acc': acc})
    for s in walk(o, 'videoRenderer', []) + walk(o, 'gridVideoRenderer', []):
        out.append({'id': s.get('videoId'), 'title': (walk(s.get('title', {}), 'text', []) or [s.get('title', {}).get('simpleText')])[0], 'views': (s.get('viewCountText') or {}).get('simpleText'), 'len': (s.get('lengthText') or {}).get('simpleText'), 'pub': (s.get('publishedTimeText') or {}).get('simpleText')})
    return out
latest = parse(d, []); print('latest', len(latest)); json.dump(latest, open(f'{tab}_latest.json', 'w'), ensure_ascii=False, indent=1)
pop = []
if tok:
    body = {'context': {'client': {'clientName': 'WEB', 'clientVersion': it['ver'], 'hl': 'en', 'gl': 'US'}}, 'continuation': tok}
    for page in range(3):
        req = urllib.request.Request('https://www.youtube.com/youtubei/v1/browse?prettyPrint=false&key=' + it['key'], data=json.dumps(body).encode(), headers=H)
        r = json.loads(urllib.request.urlopen(req, timeout=40).read()); json.dump(r, open(f'{tab}_pop_{page}.json', 'w'))
        n0 = len(pop); parse(r, pop); print('page', page, len(pop) - n0)
        conts = [t for t in walk(r, 'continuationCommand', []) if t.get('token')]
        nxt = [c['token'] for c in conts if c.get('request') == 'CONTINUATION_REQUEST_TYPE_BROWSE']
        if len(pop) >= 60 or not nxt: break
        body['continuation'] = nxt[-1]
json.dump(pop, open(f'{tab}_popular.json', 'w'), ensure_ascii=False, indent=1)
for i, p in enumerate(pop[:30]): print(i + 1, p['id'], '|', p.get('views'), '|', p.get('len', ''), '|', (p['title'] or '')[:70])
