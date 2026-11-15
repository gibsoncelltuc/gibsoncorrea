# ---------------- timing (bloco gerado por tools/new_video.sh: linha do tempo a partir de script/word-timings.json e storyboard/shots.json) ----------------
T = json.load(open(os.path.join(ROOT, 'script', 'word-timings.json')))
def _norm(s):
    import re; return re.sub(r'[^\w]', '', s.lower())
def word_start(line, prefix, nth=0): return [w for w in T['words'] if w['line'] == line and _norm(w['text']).startswith(_norm(prefix))][nth]['start']
def word_end(line, prefix, nth=0): return [w for w in T['words'] if w['line'] == line and _norm(w['text']).startswith(_norm(prefix))][nth]['end']
def line_start(i): return [l for l in T['lines'] if l['id'] == i][0]['start']
TOTAL = T['total']; FPS = 30
BANGS = []            # instantes (s) de tiro/impacto que tremem a câmera em cam_at(); ex.: [word_start('L1', 'palavra') + .1]
BANG1 = BANGS[0] if BANGS else 0.0; BANG2 = BANGS[1] if len(BANGS) > 1 else 0.0
DIS = 0.4             # dissolve entre planos (s)
# ---------------- EDL: lista de edição = storyboard/shots.json (edite lá). (id da edição, classe de cena em shots.py, início, fim)
_SB = json.load(open(os.path.join(ROOT, 'storyboard', 'shots.json')))['shots']
EDL = [(s['id'], s['scene'], s['start'], s['end']) for s in _SB]
EDIT = {e[0]: (e[2], e[3]) for e in EDL}; EDIT_CLASS = {e[0]: e[1] for e in EDL}
SHOTS = {}
for _e in EDL: SHOTS[_e[1]] = (SHOTS[_e[1]][0] if _e[1] in SHOTS else _e[2], _e[3])
