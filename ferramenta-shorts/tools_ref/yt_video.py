import json, re, sys, urllib.request, os, time
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
H = {'User-Agent': UA, 'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'SOCS=CAI; CONSENT=YES+1'}
def get(url, binary=False):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40).read()
    return r if binary else r.decode('utf-8', 'replace')
def jget(html, name):
    i = html.find(name + ' = '); 
    if i < 0: return None
    i = html.find('{', i); dec = json.JSONDecoder()
    try: return dec.raw_decode(html[i:])[0]
    except Exception as e: return None
for vid in sys.argv[1:]:
    d = f'v/{vid}'; os.makedirs(d, exist_ok=True); out = {'id': vid}
    try:
        html = get(f'https://www.youtube.com/watch?v={vid}'); pr = jget(html, 'ytInitialPlayerResponse') or {}
        json.dump(pr, open(f'{d}/player.json', 'w'))
        vd = pr.get('videoDetails', {}); mf = pr.get('microformat', {}).get('playerMicroformatRenderer', {})
        out.update(title=vd.get('title'), length=vd.get('lengthSeconds'), views=vd.get('viewCount'), desc=(vd.get('shortDescription') or '')[:600], keywords=vd.get('keywords'), publish=mf.get('publishDate'), category=mf.get('category'), status=pr.get('playabilityStatus', {}).get('status'))
        sb = pr.get('storyboards', {}).get('playerStoryboardSpecRenderer', {}).get('spec'); out['sb'] = bool(sb)
        if sb: open(f'{d}/sb_spec.txt', 'w').write(sb)
        tr = pr.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', []); out['caps'] = [(t.get('languageCode'), t.get('kind')) for t in tr]
        if tr: json.dump(tr, open(f'{d}/caps_tracks.json', 'w'))
    except Exception as e: out['err'] = str(e)[:200]
    for name in ('oar1', 'oar2', 'oar3', 'oardefault', 'maxresdefault', 'hq720', 'maxres1', 'maxres2', 'maxres3'):
        try:
            b = get(f'https://i.ytimg.com/vi/{vid}/{name}.jpg', True)
            if len(b) > 3000: open(f'{d}/{name}.jpg', 'wb').write(b); out.setdefault('imgs', []).append(name)
        except Exception as e: pass
    json.dump(out, open(f'{d}/meta.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps({k: out.get(k) for k in ('id', 'title', 'length', 'views', 'publish', 'status', 'sb', 'caps', 'imgs', 'err')}, ensure_ascii=False)); time.sleep(0.5)
