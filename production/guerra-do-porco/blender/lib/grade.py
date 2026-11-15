"""Grade de cor compartilhada (post.py e grade.py): nitidez, contraste/saturação/gama, split-tone (sombras azul/roxo, realces quentes), bloom leve (screen), vinheta e grão.
Calibrada contra as métricas dos vídeos de referência (ver qa/fidelity-report.md). Parâmetros ajustáveis por variáveis de ambiente G_*."""
import os
def params():
    e = os.environ.get
    return dict(gamma=float(e('G_GAMMA', .94)), con=float(e('G_CON', 1.06)), sat=float(e('G_SAT', 1.03)), bloom=float(e('G_BLOOM', .18)), vig=float(e('G_VIG', .32)), sharp=float(e('G_SHARP', .45)))
def filters(last, W):
    """devolve (lista de filtros para -filter_complex, rótulo de saída) aplicando a grade ao rótulo `last` (ex.: 'o3' ou '0:v')"""
    G = params(); f = []
    f.append(f"[{last}]format=yuv420p,unsharp=5:5:{G['sharp']}:5:5:0,eq=contrast={G['con']}:saturation={G['sat']}:gamma={G['gamma']},colorbalance=rs=0.015:gs=-0.008:bs=0.045:rh=0.03:gh=0.012:bh=-0.02,split[g0][g1]")
    f.append('[g1]curves=all=\'0/0 0.7/0 0.9/0.4 1/1\',gblur=sigma=%d[bl]' % max(6, W // 45)); f.append(f"[g0][bl]blend=all_mode=screen:all_opacity={G['bloom']}[g2]")
    f.append(f"[g2]vignette=angle={G['vig']},noise=alls=4:allf=t[gf]"); return f, 'gf'
