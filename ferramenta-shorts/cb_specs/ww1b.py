# EP01 WW1 IN A NUTSHELL — v4 "estilo King": mapa chapado de cima, bolas GRANDES (45-55% da largura), ano gigante embaixo, glitch de viagem no tempo, gelatina nas bolas.
import json, random
random.seed(5)
AH = ['Austria', 'Hungary', 'Czechia', 'Slovakia', 'Slovenia', 'Croatia', 'Bosnia and Herz.']
RUS = ['Russia', 'Poland', 'Ukraine', 'Belarus', 'Lithuania', 'Latvia', 'Estonia', 'Finland', 'Moldova', 'Georgia', 'Armenia', 'Azerbaijan']
RED, BLUE, GOLD, GRAY = '#ff2a4a', '#2563ff', '#ffc400', '#c3c3c8'
S = dict(sea='#f6f6f8', land=GRAY, flat=True)
def K(t, lon, lat, h, roll=0): return dict(t=t, lon=lon, lat=lat, h=h, tilt=0, roll=roll, fw=0)
S['cam'] = [K(0, 15, 48.5, 60), K(2.2, 15, 48.5, 60), K(3.3, 18, 46.2, 33), K(5.2, 18, 46.2, 33), K(6.4, 14, 49.5, 62), K(10.8, 14, 49.5, 62), K(11.6, 7, 50.3, 40), K(18.8, 6, 50, 40),
  K(19.8, 5.5, 50, 36), K(29.4, 5.5, 50, 36), K(30.4, 8, 50, 58), K(38, 8, 50, 58), K(38.9, 6, 50, 38), K(49.6, 6, 50, 38), K(50.6, 16, 47.5, 44), K(57.6, 16, 47.5, 44), K(58.8, 5.5, 50, 36), K(64, 5.5, 50, 36), K(66, 15, 48.5, 60)]
B = []
def ball(i, flag, acc, lon, lat, size, tin, **k): B.append(dict(id=i, flag=flag, acc=acc, lon=lon, lat=lat, size=size, faces=[dict(t=tin, e='idle')], **{'in': tin}, **k))
def face(i, t, e, at=None): next(b for b in B if b['id'] == i)['faces'].append(dict(t=t, e=e, **({'at': at} if at else {})))
def path(i, *pts): next(b for b in B if b['id'] == i)['path'] = [dict(t=t, lon=lo, lat=la) for t, lo, la in pts]
ball('arch', 'AT', 'crown', 18.4, 43.9, 2.4, 2.3, vis=[[2.3, 4.2]], fall=3.3)
ball('srb', 'SR', None, 20.6, 44.2, 4.4, .5, vis=[[.5, 19]]); ball('aut', 'AT', 'crown', 14.8, 47.8, 7.2, .2, vis=[[.2, 11.5]], weapon=True)
ball('rus', 'RU', 'ushanka', 31, 55.5, 6.4, 6.3, vis=[[6.3, 12], [30.6, 36.5]], weapon=True); ball('ger', 'DE', 'pickel', 12, 51, 7.0, 8.2, weapon=True)
ball('fra', 'FR', 'kepi', 0, 48.4, 6.8, 9.2, weapon=True); ball('uk', 'UK', 'brodie', -3.5, 53.2, 3.6, 10.2, weapon=True, vis=[[10.2, 38.6]])
ball('bel', 'BE', None, 4.5, 50.7, 2.6, 11.6, vis=[[11.6, 19.5], [41, 49.5]])
ball('usa', 'US', 'shades+helmetus', -13, 47.5, 6.6, 31, weapon=True); ball('aut2', 'AT', 'crown', 15.5, 47.6, 6.8, 50.4, vis=[[50.4, 53.4]])
for i, (fl, lo, la) in dict(hu=('HU', 19.5, 47), cz=('CZ', 15.6, 49.8), pl=('PL', 19, 52), yu=('SR', 17.6, 44.4), at3=('AT', 14.2, 47.6)).items(): ball(i, fl, None, 15.5, 47.6, 3.6, 53.2, vis=[[53.2, 66]])
path('hu', (53.2, 15.5, 47.6), (54.2, 20, 47.2)); path('cz', (53.2, 15.5, 47.6), (54.2, 15.3, 49.9)); path('pl', (53.2, 15.5, 47.6), (54.2, 19.5, 52.2)); path('yu', (53.2, 15.5, 47.6), (54.2, 17.5, 44.3)); path('at3', (53.2, 15.5, 47.6), (54.2, 13.8, 47.7))
ball('tur', 'TR', 'fez', 31, 38.5, 3.2, 99, vis=[[99, 100]])
# ---- caminhos
path('rus', (6.3, 44, 57), (7.4, 31, 55.5), (11, 31, 55.5)); path('ger', (8.2, 17, 52), (9.4, 12, 51), (11.4, 12, 51), (13.6, 12, 51), (14.6, 7.4, 50.6), (17, 8.5, 50.6), (19.3, 12, 50.6), (43, 12, 50.6), (46.5, 13.8, 51), (49.5, 13.8, 51), (57.8, 13.8, 51), (58.8, 11.5, 50.3))
path('fra', (9.2, -6, 47), (10.2, 0, 48.4), (14.6, 0, 48.4), (16.2, -1.5, 47.6), (19.3, -1.2, 49.3), (58.8, -1.2, 49.3), (60, 1.5, 49.8))
path('usa', (31, -13, 47.5), (32.6, -3.5, 49.8), (49.5, -3.5, 49.8), (58.8, -3.6, 50.2)); path('uk', (10.2, -8, 53.2), (11.4, -3.5, 53.2), (19.5, -4.6, 54.2), (30, -4.6, 54.2))
# ---- cores (onda de invasao)
C = [dict(t=4.0, c=AH, col=RED, **{'from': [16, 47]}, dur=1.2), dict(t=7.0, c=RUS, col=BLUE, **{'from': [31, 55]}, dur=1.6), dict(t=8.9, c=['Germany'], col=RED, **{'from': [11, 51]}, dur=1.0), dict(t=9.8, c=['France'], col=BLUE, **{'from': [2.4, 47]}, dur=1.0),
  dict(t=10.6, c=['United Kingdom', 'Ireland'], col=BLUE, dur=.8), dict(t=11.2, c=['Serbia', 'Montenegro'], col=BLUE, dur=.8), dict(t=13.6, c=['Belgium', 'Luxembourg'], col=RED, **{'from': [6.5, 50]}, dur=1.3), dict(t=14.4, c=['Turkey', 'Bulgaria'], col=RED, dur=.8),
  dict(t=16, c=['Italy', 'Romania', 'Greece'], col=BLUE, dur=.9), dict(t=33, c=RUS, col=GOLD, **{'from': [32, 56]}, dur=2.0), dict(t=41, c=['Belgium', 'Luxembourg'], col=BLUE, **{'from': [3, 50]}, dur=1.0), dict(t=44, c=['Bulgaria', 'Turkey'], col='#ff9f1c', dur=.9),
  dict(t=53.3, c=['Austria'], col='#b967ff', **{'from': [15.5, 47.6]}, dur=.7), dict(t=53.4, c=['Hungary'], col='#00d1a0', **{'from': [15.5, 47.6]}, dur=.7), dict(t=53.5, c=['Czechia', 'Slovakia'], col='#ff5ec4', **{'from': [15.5, 47.6]}, dur=.7),
  dict(t=53.6, c=['Slovenia', 'Croatia', 'Bosnia and Herz.', 'Serbia', 'Montenegro'], col='#4cd137', **{'from': [15.5, 47.6]}, dur=.7), dict(t=54.4, c=['Poland'], col='#ffffff', dur=.7), dict(t=55.6, c=['Germany'], col='#7d7d92', dur=.9), dict(t=56.4, c=['Finland', 'Estonia', 'Latvia', 'Lithuania'], col='#00d1ff', dur=.8),
  dict(t=65.2, c=[], all=True, col=GRAY, dur=.5)]
S['colors'] = C
# ---- lutas
def lunge(a, foe, t, d=1.0): next(b for b in B if b['id'] == a).setdefault('lunges', []).append(dict(t=round(t, 2), foe=foe, dur=d))
def duel(a, b, t0, t1, d=1.0):
    t = t0
    while t + d <= t1: lunge(a, b, t, d); lunge(b, a, t + d / 2, d); t += d
duel('aut', 'srb', 4.5, 9.6, 1.1); lunge('ger', 'bel', 12.2, 1.0); lunge('ger', 'bel', 13.3, 1.0); duel('ger', 'fra', 15.2, 18.6, 1.0)
duel('ger', 'fra', 20.0, 28.8, .95); lunge('uk', 'ger', 21.0, 1.3); lunge('uk', 'ger', 24.0, 1.3); lunge('uk', 'ger', 27.0, 1.3)
duel('usa', 'ger', 39.2, 45.4, 1.0); duel('fra', 'ger', 45.4, 49.2, .95); lunge('usa', 'ger', 46.4, 1.0)
for b in B:
    for l in b.get('lunges', []):
        d = l['dur']; th = l['t'] + .4 * d; foe = next(x for x in B if x['id'] == l['foe'])
        b['faces'] += [dict(t=round(l['t'] + .05, 2), e='angry', at=l['foe']), dict(t=round(l['t'] + .27 * d, 2), e='shout', at=l['foe']), dict(t=round(th + .35, 2), e=random.choice(['smug', 'angry', 'happy']), at=l['foe'])]
        foe['faces'] += [dict(t=round(th + .02, 2), e=random.choice(['wow', 'scared', 'dizzy', 'cry']), at=b['id']), dict(t=round(th + .55, 2), e='angry', at=b['id'])]
face('srb', 2.5, 'smug', 'arch'); face('srb', 3.5, 'scared', 'aut'); face('aut', 3.5, 'angry', 'srb'); face('arch', 2.3, 'happy'); face('arch', 3.3, 'scared')
face('rus', 6.3, 'angry'); face('ger', 8.2, 'smug'); face('fra', 9.2, 'wow'); face('uk', 10.2, 'smug'); face('bel', 11.6, 'scared', 'ger'); face('bel', 13.4, 'cry')
face('usa', 31, 'smug'); face('fra', 31.2, 'happy'); face('uk', 31.2, 'happy'); face('rus', 30.8, 'cry'); face('rus', 33.2, 'scared'); face('ger', 31.4, 'smug')
face('aut2', 50.6, 'scared'); face('aut2', 52.6, 'cry'); face('ger', 56, 'cry'); face('fra', 58.9, 'smug', 'ger'); face('ger', 58.9, 'cry', 'fra'); face('usa', 59, 'happy')
for i in ('hu', 'cz', 'pl', 'yu', 'at3'): face(i, 53.2, 'happy')
for b in B: b['faces'] = sorted(b['faces'], key=lambda f: f['t'])
S['balls'] = B
# ---- efeitos
S['fx'] = [dict(t=2.6, k='shot', a='srb', b='arch', d=.55), dict(t=3.2, k='boom', lon=18.4, lat=43.9, d=.6, s=5), dict(t=3.4, k='skull', lon=18.4, lat=43.9, d=1.3, s=3),
  dict(t=4.5, k='link', a='aut', b='srb', col=RED, d=1.4, w=1.0), dict(t=6.9, k='link', a='rus', b='srb', col=BLUE, d=1.5, w=1.0), dict(t=8.8, k='link', a='ger', b='aut', col=RED, d=1.5, w=1.0), dict(t=9.8, k='link', a='fra', b='rus', col=BLUE, d=1.5, w=1.0), dict(t=10.7, k='link', a='uk', b='fra', col=BLUE, d=1.5, w=1.0),
  dict(t=23.6, k='puff', lon=4.2, lat=49.6, d=1.8, s=8, col='#9dff3a'), dict(t=24.8, k='puff', lon=5.6, lat=50.3, d=1.8, s=7, col='#9dff3a'), dict(t=26, k='puff', lon=3.6, lat=48.9, d=1.8, s=8, col='#9dff3a'),
  dict(t=33.3, k='star', lon=32, lat=56.5, d=.8, s=3.5, col='#ffd23f'), dict(t=52.9, k='boom', lon=15.5, lat=47.6, d=.7, s=9), dict(t=53.1, k='star', lon=15.5, lat=47.6, d=.9, s=5)]
S['punch'] = [dict(t=52.9, a=4)]; S['flash'] = [dict(t=3.2, d=.25, a=.8), dict(t=52.9, d=.35, a=.95)]; S['shake'] = [dict(t=3.2, d=.5, a=2), dict(t=52.9, d=.7, a=2.5)]
GL = [(4.0 - 4.0 + 18.9, .9), (29.3, 1.1), (37.9, 1.0), (57.7, 1.0), (64.6, 1.4)]; S['glitch'] = [dict(t=t, d=d) for t, d in GL]
S['texts'] = [dict(t=a, d=b - a, text=x, style='yearb') for a, b, x in [(.2, 19.4, '1914'), (19.5, 29.9, '1916'), (30, 38.5, '1917'), (38.6, 58, '1918'), (58.2, 64.8, '11.11')]]
S['texts'] += [dict(t=a, d=b - a, text=x, style='stamp', top=top, color=c) for a, b, x, top, c in [(2.3, 4.2, 'ONE SHOT', 170, '#fff'), (6.6, 10.5, 'EVERYONE JOINS', 170, '#fff'), (11.8, 18.6, 'SCHLIEFFEN PLAN', 170, '#fff'), (20.2, 23.2, '3 YEARS', 170, '#ff4a4a'), (23.4, 29, '10 METERS', 170, '#ff4a4a'),
  (30.6, 33, 'USA JOINS', 170, '#fff'), (33.2, 37.6, 'RUSSIA QUITS', 170, '#ffd23f'), (39, 49, 'THE FINAL PUSH', 170, '#fff'), (50.5, 57.4, 'EMPIRES COLLAPSE', 170, '#fff'), (59.1, 62.2, 'NEW COUNTRIES', 170, '#fff'), (62.4, 64.8, 'TO BE CONTINUED...', 170, '#ffd23f')]]
S['sfx'] = [dict(t=g['t'], k='whoosh') for g in S['glitch']] + [dict(t=x, k='ding') for x in (.2, 19.5, 30, 38.6, 58.2)] + [dict(t=2.6, k='shot'), dict(t=3.2, k='boom'), dict(t=4.5, k='siren'), dict(t=52.9, k='boom'), dict(t=33.3, k='bonk')] + [dict(t=b['in'], k='pop') for b in B if b['id'] not in ('arch',)]
S['sfx'] += [dict(t=f['t'], k='puff') for f in S['fx'] if f['k'] == 'puff']
for b in B:
    for l in b.get('lunges', []): S['sfx'].append(dict(t=round(l['t'] + .4 * l['dur'], 2), k='bonk'))
S['music'] = dict(bpm=132, dur=66)
json.dump(S, open('web/countryball/ww1b.json', 'w'), ensure_ascii=False); print('ok', len(B), 'bolas', len(S['sfx']), 'sfx')
