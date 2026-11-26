"""MAPA DE VERDADE (ordem do Gibson 19/11: cada lugar com o seu mapa, nao o mesmo desenho com outro nome).
geo(nome) -> {'polys': [[x,y,...]], 'hl': [i...], 'pin': [x,y]} em pixels do quadro do mapa (508x520, origem 46,182),
com o contorno real dos paises (world-atlas / Natural Earth 1:50m), o pais/lugar em destaque e o alfinete no ponto certo."""
import json, os, math, unicodedata
_D = os.path.dirname(os.path.abspath(__file__))
_nz = lambda s: unicodedata.normalize('NFKD', s.upper()).encode('ascii', 'ignore').decode().strip()
# nome em portugues -> nome no atlas (pais)
PAIS = {'ESTADOS UNIDOS': 'United States of America', 'EUA': 'United States of America', 'EL SALVADOR': 'El Salvador', 'FRANCA': 'France', 'AUSTRIA': 'Austria', 'HOLANDA': 'Netherlands', 'PAISES BAIXOS': 'Netherlands',
 'BELGICA': 'Belgium', 'ITALIA': 'Italy', 'AUSTRALIA': 'Australia', 'VENEZUELA': 'Venezuela', 'SUICA': 'Switzerland', 'MEXICO': 'Mexico', 'IRA': 'Iran', 'IRAO': 'Iran', 'EGITO': 'Egypt', 'DINAMARCA': 'Denmark',
 'BULGARIA': 'Bulgaria', 'BRASIL': 'Brazil', 'ALEMANHA': 'Germany', 'INGLATERRA': 'United Kingdom', 'REINO UNIDO': 'United Kingdom', 'ESCOCIA': 'United Kingdom', 'REPUBLICA TCHECA': 'Czechia', 'PANAMA': 'Panama',
 'ISLANDIA': 'Iceland', 'GROENLANDIA': 'Greenland', 'GANA': 'Ghana', 'CUBA': 'Cuba', 'CANADA': 'Canada', 'JAPAO': 'Japan', 'CHINA': 'China', 'RUSSIA': 'Russia', 'POLONIA': 'Poland', 'ESPANHA': 'Spain', 'PORTUGAL': 'Portugal',
 'GRECIA': 'Greece', 'TURQUIA': 'Turkey', 'INDIA': 'India', 'IRAQUE': 'Iraq', 'ISRAEL': 'Israel', 'ARABIA SAUDITA': 'Saudi Arabia', 'ARGENTINA': 'Argentina', 'CHILE': 'Chile', 'PERU': 'Peru', 'COLOMBIA': 'Colombia',
 'BOLIVIA': 'Bolivia', 'PARAGUAI': 'Paraguay', 'URUGUAI': 'Uruguay', 'HONDURAS': 'Honduras', 'GUATEMALA': 'Guatemala', 'NICARAGUA': 'Nicaragua', 'COSTA RICA': 'Costa Rica', 'HAITI': 'Haiti', 'JAMAICA': 'Jamaica',
 'UCRANIA': 'Ukraine', 'HUNGRIA': 'Hungary', 'ROMENIA': 'Romania', 'SERVIA': 'Serbia', 'CROACIA': 'Croatia', 'SUECIA': 'Sweden', 'NORUEGA': 'Norway', 'FINLANDIA': 'Finland', 'IRLANDA': 'Ireland', 'MARROCOS': 'Morocco',
 'ARGELIA': 'Algeria', 'TUNISIA': 'Tunisia', 'LIBIA': 'Libya', 'SUDAO': 'Sudan', 'ETIOPIA': 'Ethiopia', 'QUENIA': 'Kenya', 'TANZANIA': 'Tanzania', 'NIGERIA': 'Nigeria', 'AFRICA DO SUL': 'South Africa', 'MALI': 'Mali',
 'CONGO': 'Dem. Rep. Congo', 'ANGOLA': 'Angola', 'MOCAMBIQUE': 'Mozambique', 'COREIA DO NORTE': 'North Korea', 'COREIA DO SUL': 'South Korea', 'COREIA': 'South Korea', 'VIETNA': 'Vietnam', 'TAILANDIA': 'Thailand',
 'CAMBOJA': 'Cambodia', 'INDONESIA': 'Indonesia', 'FILIPINAS': 'Philippines', 'PAQUISTAO': 'Pakistan', 'AFEGANISTAO': 'Afghanistan', 'NOVA ZELANDIA': 'New Zealand', 'MONGOLIA': 'Mongolia', 'SIRIA': 'Syria', 'JORDANIA': 'Jordan',
 'LIBANO': 'Lebanon', 'EMIRADOS ARABES': 'United Arab Emirates', 'QATAR': 'Qatar', 'KUWAIT': 'Kuwait', 'IEMEN': 'Yemen', 'SOMALIA': 'Somalia', 'MADAGASCAR': 'Madagascar', 'PORTO RICO': 'Puerto Rico', 'EQUADOR': 'Ecuador'}
# lugar que nao e pais: (lat, lon, largura do mapa em graus, pais em destaque ou None)
LUGAR = {'PERNAMBUCO': (-8.3, -37.8, 16, 'Brazil'), 'RECIFE': (-8.05, -34.9, 12, 'Brazil'), 'FLORIDA': (28.0, -81.6, 16, 'United States of America'), 'CABO CANAVERAL': (28.4, -80.6, 9, 'United States of America'),
 'TEXAS': (31.0, -99.5, 20, 'United States of America'), 'NOVA YORK': (40.7, -74.0, 12, 'United States of America'), 'CALIFORNIA': (36.8, -119.4, 18, 'United States of America'), 'LOS ANGELES': (34.05, -118.25, 12, 'United States of America'),
 'SAO FRANCISCO': (37.77, -122.42, 12, 'United States of America'), 'MAINE': (45.3, -69.2, 12, 'United States of America'), 'WASHINGTON': (38.9, -77.0, 12, 'United States of America'), 'TOLEDO': (41.65, -83.54, 10, 'United States of America'),
 'KARANSEBES': (45.42, 22.22, 12, 'Romania'), 'ESTRASBURGO': (48.57, 7.75, 9, 'France'), 'SICILIA': (37.6, 14.0, 9, 'Italy'), 'ROMA': (41.9, 12.5, 12, 'Italy'), 'PARIS': (48.86, 2.35, 10, 'France'), 'LONDRES': (51.5, -0.13, 10, 'United Kingdom'),
 'ZANZIBAR': (-6.16, 39.2, 10, 'Tanzania'), 'ILHA DE YAP': (9.53, 138.13, 30, None), 'ILHA DE SAN JUAN': (48.53, -123.02, 8, None), 'ILHAS SCILLY': (49.93, -6.3, 8, 'United Kingdom'), 'GALAPAGOS': (-0.7, -90.5, 14, 'Ecuador'),
 'AMERICA CENTRAL': (13.5, -86.0, 28, None), 'CAIRO': (30.04, 31.24, 14, 'Egypt'), 'ALEXANDRIA': (31.2, 29.9, 14, 'Egypt'), 'AMAZONIA': (-4.0, -62.0, 30, 'Brazil'), 'MARAJO': (-1.0, -49.6, 12, 'Brazil'), 'PARA': (-3.8, -52.5, 18, 'Brazil'),
 'RIO DE JANEIRO': (-22.9, -43.2, 14, 'Brazil'), 'SAO PAULO': (-23.55, -46.63, 14, 'Brazil'), 'BAHIA': (-12.5, -41.7, 16, 'Brazil'), 'MINAS GERAIS': (-18.5, -44.5, 16, 'Brazil'), 'OURO PRETO': (-20.38, -43.5, 12, 'Brazil'),
 'TOQUIO': (35.68, 139.69, 14, 'Japan'), 'MOSCOU': (55.75, 37.62, 16, 'Russia'), 'BERLIM': (52.52, 13.4, 12, 'Germany'), 'VARSOVIA': (52.23, 21.0, 12, 'Poland'), 'WATERLOO': (50.71, 4.4, 8, 'Belgium'), 'PETRA': (30.33, 35.44, 12, 'Jordan'),
 'ANGKOR': (13.41, 103.87, 14, 'Cambodia'), 'TIMBUKTU': (16.77, -3.0, 20, 'Mali'), 'CRETA': (35.24, 24.8, 10, 'Greece'), 'ESPARTA': (37.08, 22.43, 10, 'Greece'), 'ATENAS': (37.98, 23.73, 10, 'Greece'), 'TENOCHTITLAN': (19.43, -99.13, 14, 'Mexico'),
 'CUSCO': (-13.53, -71.97, 16, 'Peru'), 'ANDES': (-13.5, -72.0, 30, 'Peru'), 'HAVAI': (20.8, -156.3, 14, None), 'TAITI': (-17.65, -149.4, 14, None), 'MOHENJO-DARO': (27.33, 68.14, 16, 'Pakistan'), 'EUROPA': (50.0, 12.0, 50, None),
 'OCEANO PACIFICO': (5.0, -150.0, 120, None), 'OCEANO ATLANTICO': (25.0, -40.0, 90, None), 'OCEANOS': (0.0, -30.0, 240, None), 'MUNDO': (15.0, 0.0, 300, None), 'AFRICA': (2.0, 20.0, 80, None), 'ASIA': (35.0, 95.0, 100, None)}
_G = None
def _load():
    global _G
    if _G is not None: return _G
    t = json.load(open(os.path.join(_D, 'countries-50m.json'))); sc, tr = t['transform']['scale'], t['transform']['translate']; arcs = []
    for a in t['arcs']:
        x = y = 0; pts = []
        for dx, dy in a: x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        arcs.append(pts)
    ring = lambda ids: [p for k, i in enumerate(ids) for p in ((arcs[i] if i >= 0 else arcs[~i][::-1])[1 if k else 0:])]
    _G = []
    for g in t['objects']['countries']['geometries']:
        polys = [[ring(r) for r in p][0] for p in (g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']])] if g.get('arcs') else []
        _G.append((g['properties']['name'], polys))
    return _G
def _bbox(polys):
    xs = [x for p in polys for x, _ in p]; ys = [y for p in polys for _, y in p]; return min(xs), min(ys), max(xs), max(ys)
def geo(nome, W=508, H=520):
    n = _nz(nome); G = _load()
    if n in LUGAR: lat, lon, span, hl = LUGAR[n]; pin = (lon, lat)
    elif n in PAIS:
        hl = PAIS[n]; ps = next((p for nm, p in G if nm == hl), None)
        if not ps: return None
        big = max(ps, key=lambda p: (_bbox([p])[2] - _bbox([p])[0]) * (_bbox([p])[3] - _bbox([p])[1]))   # territorio principal (Franca sem a Guiana, EUA sem o Alasca)
        x0, y0, x1, y1 = _bbox([big]); lon, lat = (x0 + x1) / 2, (y0 + y1) / 2; span = max(x1 - x0, (y1 - y0) * 1.2) * 1.7 + 3; pin = (lon, lat)
    else: return None
    kx = math.cos(math.radians(max(-70, min(70, lat)))); s = W / span; out, hli = [], []
    px = lambda lo, la: ((lo - lon) * kx * s + W / 2, (lat - la) * s + H / 2)
    for nm, ps in G:
        for p in ps:
            q = [px(lo, la) for lo, la in p]
            if max(x for x, _ in q) < -20 or min(x for x, _ in q) > W + 20 or max(y for _, y in q) < -20 or min(y for _, y in q) > H + 20: continue
            bw = max(x for x, _ in q) - min(x for x, _ in q); bh = max(y for _, y in q) - min(y for _, y in q)
            if bw < 4 and bh < 4: continue                      # ilhota menor que 4 px: some
            st = max(1, len(q) // 90); q = q[::st]
            if len(q) < 3: continue
            if nm == hl: hli.append(len(out))
            out.append([int(round(v)) for xy in q for v in xy])
    return {'polys': out, 'hl': hli, 'pin': [round(v, 1) for v in px(*pin)]}
if __name__ == '__main__':
    import sys; g = geo(sys.argv[1]); print(len(g['polys']) if g else None, g and g['hl'], g and g['pin'], len(json.dumps(g)) if g else 0)
