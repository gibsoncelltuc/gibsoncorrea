# EP01 WORLD WAR 1 IN A NUTSHELL (66 s) -> web/countryball/ww1.json  (python3 cb_specs/ww1.py)
import json
AH = ['Austria', 'Hungary', 'Czechia', 'Slovakia', 'Slovenia', 'Croatia', 'Bosnia and Herz.']
RUS = ['Russia', 'Poland', 'Ukraine', 'Belarus', 'Lithuania', 'Latvia', 'Estonia', 'Finland', 'Moldova', 'Georgia', 'Armenia', 'Azerbaijan']
RED, BLUE, GOLD, GRAY = '#ff2e4d', '#2e8bff', '#ffc400', '#c9ced6'
S = {'title': 'WW1 in a Nutshell', 'sea': '#e3f1ff', 'land': GRAY}
S['cam'] = [dict(t=0, lon=16, lat=48, h=80, tilt=.0, roll=0), dict(t=3, lon=17, lat=46.5, h=62, tilt=.1, roll=0), dict(t=7, lon=17, lat=46, h=44, tilt=.12, roll=0), dict(t=8.5, lon=14, lat=49, h=85, tilt=.05, roll=.0),
  dict(t=13, lon=14, lat=49, h=85, tilt=.05, roll=0), dict(t=14, lon=7, lat=49.5, h=46, tilt=.15, roll=-.05), dict(t=20, lon=5.5, lat=50.4, h=44, tilt=.2, roll=.04), dict(t=27, lon=5.5, lat=50.8, h=44, tilt=.2, roll=-.03),
  dict(t=34, lon=6, lat=49, h=44, tilt=.15, roll=0), dict(t=37, lon=14, lat=50, h=80, tilt=.05, roll=0), dict(t=42, lon=14, lat=50, h=80, tilt=.05, roll=0), dict(t=44, lon=8, lat=49.5, h=52, tilt=.15, roll=.03),
  dict(t=50.5, lon=14, lat=47, h=70, tilt=.05, roll=0), dict(t=56, lon=15, lat=48, h=84, tilt=.0, roll=0), dict(t=60, lon=11, lat=51, h=38, tilt=.2, roll=0), dict(t=65, lon=16, lat=48, h=80, tilt=0, roll=0), dict(t=66, lon=16, lat=48, h=80, tilt=0, roll=0)]
C = [dict(t=7.5, c=AH, col=RED), dict(t=9, c=RUS, col=BLUE), dict(t=10, c=['Germany'], col=RED), dict(t=11, c=['France'], col=BLUE), dict(t=12, c=['United Kingdom', 'Ireland'], col=BLUE), dict(t=12.6, c=['Serbia', 'Montenegro'], col=BLUE),
  dict(t=15, c=['Belgium', 'Luxembourg'], col=RED), dict(t=16, c=['Turkey', 'Bulgaria'], col=RED), dict(t=18, c=['Italy', 'Romania', 'Greece'], col=BLUE),
  dict(t=38, c=RUS, col=GOLD), dict(t=44, c=['Belgium', 'Luxembourg'], col=BLUE), dict(t=47, c=['Bulgaria', 'Turkey'], col='#ff9f1c'),
  dict(t=51, c=['Austria'], col='#b967ff'), dict(t=51.1, c=['Hungary'], col='#00d1a0'), dict(t=51.2, c=['Czechia', 'Slovakia'], col='#ff5ec4'), dict(t=51.3, c=['Slovenia', 'Croatia', 'Bosnia and Herz.', 'Serbia', 'Montenegro'], col='#4cd137'),
  dict(t=56, c=['Poland'], col='#ffffff'), dict(t=56.1, c=['Germany'], col='#7d7d92'), dict(t=56.2, c=['Finland', 'Estonia', 'Latvia', 'Lithuania'], col='#00d1ff'), dict(t=65, c=[], all=True, col=GRAY)]
B = []
def ball(i, flag, acc, lon, lat, size, tin, **k): B.append(dict(id=i, flag=flag, acc=acc, lon=lon, lat=lat, size=round(size * .95, 2), **{'in': tin}, **k))
ball('arch', 'AT', 'crown', 18.4, 43.9, 3.4, 3.2, fall=4.3, out=7.5, faces=[dict(t=3.2, e='happy'), dict(t=4.3, e='scared')])
ball('srb', 'SR', None, 20.2, 44.2, 4.6, 0.6, faces=[dict(t=.6, e='idle'), dict(t=3.5, e='smug'), dict(t=4.5, e='scared'), dict(t=8, e='shout'), dict(t=22, e='idle'), dict(t=42, e='happy')], pulse=[dict(t=4.4, a=.3)], path=[dict(t=0, lon=20.2, lat=44.2), dict(t=3.3, lon=20.2, lat=44.2), dict(t=3.5, lon=19.4, lat=44.5), dict(t=3.7, lon=20.2, lat=44.2)])
ball('aut', 'AT', 'crown', 15.5, 47.8, 6.4, 0.9, faces=[dict(t=.9, e='idle'), dict(t=4.6, e='angry'), dict(t=7, e='shout'), dict(t=30, e='scared'), dict(t=47, e='cry'), dict(t=51, e='scared')], pulse=[dict(t=4.6, a=.4), dict(t=7.2, a=.5)])
ball('rus', 'RU', 'ushanka', 32, 55.5, 9.5, 8.6, faces=[dict(t=8.6, e='angry'), dict(t=36, e='cry'), dict(t=38.5, e='scared')], pulse=[dict(t=8.8, a=.4)], path=[dict(t=8.6, lon=44, lat=57), dict(t=9.4, lon=32, lat=55.5), dict(t=36, lon=32, lat=55.5), dict(t=39, lon=46, lat=58)])
ball('ger', 'DE', 'pickel', 11, 51.2, 8.4, 9.7, faces=[dict(t=9.7, e='angry'), dict(t=14, e='shout'), dict(t=20, e='angry'), dict(t=27, e='smug'), dict(t=30, e='scared'), dict(t=44, e='scared'), dict(t=50, e='cry'), dict(t=56, e='cry'), dict(t=60, e='angry')],
     pulse=[dict(t=10, a=.4), dict(t=14.2, a=.4), dict(t=44.5, a=.3)], path=[dict(t=9.7, lon=11, lat=51.2), dict(t=13.5, lon=11, lat=51.2), dict(t=15.5, lon=7.2, lat=50.3), dict(t=17.5, lon=12.5, lat=50.8), dict(t=43, lon=12.5, lat=50.8), dict(t=47, lon=12.5, lat=51.5), dict(t=50, lon=12, lat=51.2)])
ball('fra', 'FR', 'kepi', 2.4, 47, 8.4, 10.8, faces=[dict(t=10.8, e='scared'), dict(t=15, e='scared'), dict(t=20, e='angry'), dict(t=30, e='cry'), dict(t=41, e='happy'), dict(t=47, e='shout'), dict(t=55, e='smug'), dict(t=60, e='angry')],
     pulse=[dict(t=11, a=.4), dict(t=15.2, a=.4)], path=[dict(t=10.8, lon=2.4, lat=47), dict(t=15, lon=2.4, lat=47), dict(t=17.5, lon=-1.2, lat=49.3), dict(t=43, lon=-1.2, lat=49.3), dict(t=47, lon=3.2, lat=49.8), dict(t=55, lon=3.2, lat=49.8)])
ball('uk', 'UK', 'brodie', -2.5, 53, 7.5, 11.9, faces=[dict(t=11.9, e='smug'), dict(t=15, e='angry'), dict(t=27, e='shout'), dict(t=41, e='happy')], pulse=[dict(t=12, a=.4)], path=[dict(t=11.9, lon=-2.5, lat=53), dict(t=17.5, lon=-2.5, lat=53), dict(t=19.5, lon=-4.5, lat=54.2), dict(t=26, lon=-4.5, lat=54.2)])
ball('bel', 'BE', None, 4.6, 50.7, 4.6, 13.8, path=[dict(t=13.8, lon=4.6, lat=50.7), dict(t=15.4, lon=4.6, lat=50.7), dict(t=16.6, lon=5.6, lat=53.4)], faces=[dict(t=13.8, e='scared'), dict(t=15, e='cry'), dict(t=44, e='happy')], pulse=[dict(t=14, a=.4)])
ball('tur', 'TR', 'fez', 33, 39, 6.2, 16, faces=[dict(t=16, e='smug'), dict(t=47, e='cry')], pulse=[dict(t=16.2, a=.4)])
ball('usa', 'US', 'shades+helmetus', -15, 47, 9.5, 34.2, faces=[dict(t=34.2, e='smug'), dict(t=40, e='shout')], pulse=[dict(t=36.5, a=.45)], path=[dict(t=34.2, lon=-14, lat=47), dict(t=36.5, lon=-2, lat=49.5), dict(t=42, lon=-1, lat=49.6)], out=66)
ball('ita', 'IT', None, 12.5, 42.3, 5.6, 18, faces=[dict(t=18, e='shout'), dict(t=42, e='happy')], pulse=[dict(t=18.2, a=.4)])
FOE = {'ger': 'fra', 'fra': 'ger', 'uk': 'ger', 'usa': 'ger', 'aut': 'srb', 'srb': 'aut', 'rus': 'aut', 'bel': 'ger'}
for b in B:
    if b['id'] in ('ger', 'fra', 'uk', 'usa', 'rus', 'aut'): b['weapon'] = True
    if b['id'] in FOE: b['faces'] = [dict(f, at=FOE[b['id']]) if f['e'] in ('angry', 'shout', 'smug', 'scared', 'wow') else f for f in b['faces']]
S['balls'] = B; S['colors'] = C
for c_ in C:
    if c_.get('c') == ['Belgium', 'Luxembourg'] and c_['t'] == 15: c_['from'] = [6.5, 50]; c_['dur'] = 1.3
    if c_.get('c') == AH: c_['from'] = [16, 47]; c_['dur'] = 1.2
    if c_.get('c') == RUS and c_['t'] == 9: c_['from'] = [30, 55]; c_['dur'] = 1.6
    if c_.get('c') == ['Germany']: c_['from'] = [10, 51]; c_['dur'] = 1.0
    if c_.get('c') == ['France']: c_['from'] = [2.4, 47]; c_['dur'] = 1.0
    if c_.get('c') == RUS and c_['t'] == 38: c_['from'] = [32, 56]; c_['dur'] = 2.0
def lnk(t, a, b, col, d=1.6): return dict(t=t, k='link', a=a, b=b, col=col, d=d, w=1.1)
def volley(t0, t1, step=.55):
    L, i, t = [], 0, t0
    while t < t1: L.append(dict(t=round(t, 2), k='shot', a='ger' if i % 2 == 0 else 'fra', b='fra' if i % 2 == 0 else 'ger', d=.5)); L.append(dict(t=round(t + .45, 2), k='boom', lon=4.2 + (i * .9) % 2.4, lat=49.4 + (i * .9) % 2.0, d=.35, s=4.0)); i += 1; t += step
    return L
S['fx'] = [dict(t=3.5, k='shot', a='srb', b='arch', d=.6), dict(t=4.15, k='boom', lon=18.4, lat=43.9, d=.6, s=7), dict(t=4.4, k='skull', lon=18.4, lat=43.9, d=1.4, s=4),
  lnk(7.3, 'aut', 'srb', RED), lnk(9.2, 'rus', 'srb', BLUE), lnk(10.3, 'ger', 'aut', RED), lnk(11.3, 'fra', 'rus', BLUE), lnk(12.3, 'uk', 'fra', BLUE),
  dict(t=15, k='boom', lon=4.6, lat=50.7, d=.7, s=8), dict(t=15.4, k='boom', lon=3.2, lat=49.9, d=.5, s=6), dict(t=15.8, k='boom', lon=5.7, lat=49.6, d=.5, s=6)] + volley(20.5, 26.5) + [
  dict(t=27.5, k='puff', lon=3.8, lat=49.3, d=1.8, s=9, col='#9dff3a'), dict(t=28.4, k='puff', lon=5.3, lat=50.3, d=1.8, s=8, col='#9dff3a'), dict(t=29.4, k='puff', lon=4.2, lat=48.8, d=1.8, s=9, col='#9dff3a'),
  dict(t=31, k='boom', lon=3.5, lat=50, d=.5, s=7), dict(t=31.6, k='boom', lon=5.4, lat=49.2, d=.5, s=7), dict(t=32.5, k='shot', a='uk', b='ger', d=.5), dict(t=33, k='boom', lon=5.2, lat=50.3, d=.5, s=8),
  dict(t=38.1, k='star', lon=32, lat=57, d=.8, s=5, col='#ffd23f'), dict(t=44.5, k='boom', lon=6, lat=50, d=.5, s=8), dict(t=45.3, k='boom', lon=7.2, lat=50.8, d=.5, s=8), dict(t=46.3, k='shot', a='usa', b='ger', d=.5), dict(t=46.9, k='boom', lon=8, lat=51, d=.6, s=9),
  dict(t=48.5, k='boom', lon=9, lat=51, d=.5, s=7), dict(t=50.8, k='boom', lon=16, lat=47.5, d=.8, s=11), dict(t=51.2, k='star', lon=15, lat=47.5, d=.9, s=6), dict(t=56.1, k='star', lon=10, lat=51, d=.9, s=6)]
S['flash'] = [dict(t=4.15, d=.3, a=.9), dict(t=15, d=.25, a=.6), dict(t=36.4, d=.3, a=.5), dict(t=46.9, d=.3, a=.7), dict(t=50.8, d=.35, a=.9), dict(t=65, d=.7, a=1)]
S['shake'] = [dict(t=4.15, d=.5, a=2), dict(t=15, d=.6, a=2.2), dict(t=31.6, d=.5, a=1.5), dict(t=46.9, d=.6, a=2), dict(t=50.8, d=.7, a=2.5)]
S['texts'] = [dict(t=.2, d=2.6, text='1914', style='year'), dict(t=3.3, d=3.4, text='ONE SHOT', style='big', top=330), dict(t=7.2, d=5.2, text='EVERYONE JOINS', style='big', top=330), dict(t=13.8, d=5.5, text='SCHLIEFFEN PLAN', style='big', top=330),
  dict(t=20, d=3.2, text='3 YEARS', style='num', top=230), dict(t=23.3, d=3.6, text='10 METERS', style='num', top=230), dict(t=27, d=6.5, text='GAS • TANKS • PLANES', style='big', top=330), dict(t=34.2, d=2.8, text='1917', style='year'),
  dict(t=37, d=3.5, text='RUSSIA QUITS', style='big', top=330), dict(t=44, d=5, text='1918: THE FINAL PUSH', style='big', top=330), dict(t=50.7, d=4.3, text='EMPIRES COLLAPSE', style='big', top=330), dict(t=55.2, d=2.8, text='11.11', style='year'),
  dict(t=58, d=3.6, text='NEW COUNTRIES', style='big', top=330, size=100), dict(t=61.5, d=3.4, text='TO BE CONTINUED...', style='big', top=330, color='#ffd23f')]
S['texts'] += [dict(t=a, d=b - a, text=x, style='cap') for a, b, x in [(0.3, 2.9, 'Europe, 1914. Everyone is tense.'), (3.2, 6.8, 'One bullet in Sarajevo...'), (7.2, 12.8, 'Austria attacks Serbia. Then everyone helps a friend.'), (13.4, 19, 'Germany cuts through Belgium to reach Paris.'),
  (19.6, 26.8, 'The front freezes for three years.'), (27, 33.8, 'Poison gas, tanks, and bad moods.'), (34.2, 36.8, 'America joins the party.'), (37, 41, 'Russia has a revolution and leaves.'), (41.4, 49.8, 'Fresh troops push Germany back.'),
  (50.6, 55, 'Austria-Hungary breaks into pieces.'), (55.3, 59.8, 'Nov 11, 1918: the guns go quiet.'), (60, 65, 'Germany gets the bill. It will remember.')]]
S['sfx'] = [dict(t=.2, k='whoosh'), dict(t=3.5, k='shot'), dict(t=4.15, k='boom'), dict(t=7.3, k='siren'), dict(t=8.6, k='pop'), dict(t=9.7, k='pop'), dict(t=10.8, k='pop'), dict(t=11.9, k='pop'), dict(t=13.8, k='pop'), dict(t=14.0, k='horn'), dict(t=15, k='boom'), dict(t=15.4, k='boom'), dict(t=16, k='pop'), dict(t=18, k='pop'),
  dict(t=34.2, k='ding'), dict(t=36.5, k='horn'), dict(t=38.1, k='bonk'), dict(t=44.5, k='boom'), dict(t=45.3, k='boom'), dict(t=46.3, k='shot'), dict(t=46.9, k='boom'), dict(t=48.5, k='boom'), dict(t=50.8, k='boom'), dict(t=51.2, k='ding'), dict(t=56.1, k='ding'), dict(t=55.2, k='horn'), dict(t=65, k='whoosh')]
S['sfx'] += [dict(t=f['t'], k=('shot' if f['k'] == 'shot' else 'boom' if f['k'] == 'boom' else 'puff')) for f in S['fx'] if f['k'] in ('shot', 'boom', 'puff') and 19 < f['t'] < 34]
S['punch'] = [dict(t=f['t'], a=2.5) for f in S['fx'] if f['k'] == 'boom' and f.get('s', 0) >= 7]
for b in B:
    if b['id'] == 'ger': b['knock'] = [dict(t=15, dx=1, a=2.4), dict(t=44.6, dx=1, a=2.2)]
    if b['id'] == 'fra': b['knock'] = [dict(t=15.3, dx=-1, a=2.4)]

def lunges(b, a, t0, t1, d=1.1, off=0):
    t = t0
    while t + d <= t1: next(x for x in B if x['id'] == a).setdefault('lunges', []).append(dict(t=round(t, 2), foe=b, dur=d)); t += d
def duel(a, b, t0, t1, d=1.1): lunges(b, a, t0, t1, d); lunges(a, b, t0 + d / 2, t1, d)
duel('aut', 'srb', 7.4, 12.6, 1.2); lunges('bel', 'ger', 14.0, 15.0, 1.0)
duel('ger', 'fra', 19.4, 27.4, 1.1); duel('ger', 'fra', 31.0, 34.0, 1.1); duel('ger', 'usa', 44.4, 47.6, 1.0); duel('ger', 'fra', 47.6, 50.2, 1.0)
lunges('uk', 'ger', 27.6, 31.0, 1.2)
import random
random.seed(3); BY = {x['id']: x for x in B}
for b in B:
    for l in b.get('lunges', []):
        d = l['dur']; th = l['t'] + .4 * d; foe = BY[l['foe']]
        b['faces'] += [dict(t=round(l['t'] + .05, 2), e='angry', at=l['foe']), dict(t=round(l['t'] + .27 * d, 2), e='shout', at=l['foe']), dict(t=round(th + .35, 2), e=random.choice(['smug', 'angry', 'happy']), at=l['foe'])]
        foe['faces'] += [dict(t=round(th + .02, 2), e=random.choice(['wow', 'scared', 'dizzy', 'cry']), at=b['id']), dict(t=round(th + .55, 2), e='angry', at=b['id'])]
for b in B: b['faces'] = sorted(b['faces'], key=lambda f: f['t'])
for b in B:
    for l in b.get('lunges', []): S['sfx'].append(dict(t=round(l['t'] + .4 * l['dur'], 2), k='bonk'))
for c_ in S['cam']: c_.setdefault('fw', 0)
def focus(t, ids, w=.55):
    for c_ in S['cam']:
        if abs(c_['t'] - t) < .01: c_['fo'] = ids; c_['fw'] = w
for t_, ids in [(8.5, ['aut', 'srb']), (13, ['ger', 'bel']), (14, ['ger', 'fra']), (20, ['ger', 'fra']), (27, ['ger', 'fra', 'uk']), (34, ['ger', 'fra']), (44, ['ger', 'usa', 'fra']), (50.5, ['aut', 'ger'])]: focus(t_, ids)
VIS = {'aut': [[0.9, 13.5], [49.5, 62]], 'srb': [[0.6, 13.5], [49.5, 60]], 'tur': [[16, 22], [46, 50]], 'ita': [[18, 24]], 'rus': [[8.6, 14.5], [35.5, 41]], 'bel': [[13.8, 20]], 'uk': [[11.9, 36], [40, 45.5]], 'arch': [[3.2, 7.5]]}
for b in B:
    if b['id'] in VIS: b['vis'] = VIS[b['id']]
S['music'] = dict(bpm=132, dur=66)
json.dump(S, open('web/countryball/ww1.json', 'w'), ensure_ascii=False)
print('ok', len(S['fx']), 'fx', len(S['sfx']), 'sfx')
