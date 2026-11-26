import json, re, sys, urllib.request, os
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
H = {'User-Agent': UA, 'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'SOCS=CAI; CONSENT=YES+1'}
def get(url, data=None, headers=None):
    hh = dict(H); hh.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hh)
    return urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')
def initial(html, name='ytInitialData'):
    m = re.search(name + r'\s*=\s*(\{.*?\});\s*(?:var |</script>)', html, re.S)
    return json.loads(m.group(1)) if m else None
def walk(o, key, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: out.append(v)
            walk(v, key, out)
    elif isinstance(o, list):
        for v in o: walk(v, key, out)
    return out
tab = sys.argv[1] if len(sys.argv) > 1 else 'shorts'
html = get(f'https://www.youtube.com/@ricksclips3000/{tab}')
open(f'channel_{tab}.html', 'w').write(html)
d = initial(html); print('html', len(html), 'data', bool(d))
if not d: sys.exit(1)
json.dump(d, open(f'channel_{tab}.json', 'w'))
key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html); ver = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', html)
print('key', bool(key), 'ver', ver and ver.group(1))
meta = walk(d, 'channelMetadataRenderer', [])
if meta: print({k: meta[0].get(k) for k in ('title', 'externalId', 'description')})
chips = walk(d, 'chipCloudChipRenderer', []) + walk(d, 'chipViewModel', [])
print('chips', [(c.get('text') if isinstance(c.get('text'), str) else (c.get('text') or {}).get('simpleText') or c.get('text')) for c in chips][:6])
json.dump({'key': key and key.group(1), 'ver': ver and ver.group(1)}, open('innertube.json', 'w'))
