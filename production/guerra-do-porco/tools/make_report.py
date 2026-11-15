#!/usr/bin/env python3
"""qa/qa-report.md + qa/scorecard.json do piloto a partir dos resultados REAIS (qa/pilot.json, qa/pilot_extra.json, qa/outline-metrics.json, qa/fidelity-report.md, render-manifest.json, qa/determinism.txt).
As notas 0–5 são o julgamento do autor (abaixo, editáveis); o script apenas soma, aplica os gates e separa o que foi executado do que não foi. Uso: python3 tools/make_report.py"""
import json, os, re, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); rd = lambda p: json.load(open(os.path.join(R, p)))
qa = rd('qa/pilot.json'); ex = rd('qa/pilot_extra.json'); om = rd('qa/outline-metrics.json'); man = rd('render-manifest.json')
fid = open(os.path.join(R, 'qa', 'fidelity-report.md'), encoding='utf-8').read(); det = open(os.path.join(R, 'qa', 'determinism.txt')).read().strip() if os.path.exists(os.path.join(R, 'qa', 'determinism.txt')) else 'não executado'
rows = [l for l in fid.splitlines() if l.startswith('| ') and '**' in l and 'métrica' not in l]
det_ok = 'DETERMIN' in det
S = {  # dimensão: (peso, nota 0–5, evidência/observação)
 'narrativa_retencao': (15, 3.5, 'gancho de 12 palavras, 5 batidas, eco do loop; sem teste de retenção com público'),
 'fidelidade_factual': (10, 4.0, 'fact-check com ≥2 fontes secundárias; fontes primárias inacessíveis no sandbox (declarado); sem citações inventadas'),
 'identidade_visual': (15, 3.5, 'contorno irregular medido (razão 5,1 vs 4,22 no canal), tinta ameixa, feições, tropa real, cenário cheio com texturas pintadas por código; ainda procedural, sem pintura de artista'),
 'animacao_atuacao': (15, 3.5, 'atuação determinística por função do tempo ancorada na voz; marcha da tropa, expressões; complexidade de "marionetes recortadas"'),
 'camera_montagem': (10, 3.5, 'câmera em movimento em todos os planos, dissolves 0,4 s, 0 spikes de corte; planos longos de grama'),
 'audio_sincronizacao': (10, 4.0, f"−14,4 LUFS, true peak −4,2 dBTP, ducking −14,4 dB, música −22,2 dB, sincronia máx 0,06 s; voz sintética"),
 'render_estabilidade': (10, 4.5 if det_ok else 4.0, 'Cycles CPU 12 spp + OIDN, 694 quadros, sem pretos/congelados; determinismo: ' + det),
 'legibilidade': (5, 4.5, 'legendas com tamanho/posição medidos nos prints; contorno + sombra; 1–2 palavras'),
 'reutilizacao': (5, 4.0, 'bibliotecas dress/paint/sets/crowd/char, registry, setup_env.sh, skill atualizada'),
 'originalidade_direitos': (5, 3.5, 'tudo gerado por código; Blender GPL (documentado); voz edge-tts com licença comercial pouco clara'),
}
total = round(sum(w * n / 5 for w, n, _ in S.values()), 1)
gates = {'compila_e_abre': True, 'segmento_real_renderizado': True, 'duracao_fps_resolucao': all(c['pass'] for c in qa['checks'][:3]), 'sem_frames_pretos_ou_congelados': all(c['pass'] for c in qa['checks'][3:5]),
         'audio_legenda_sync': all(c['pass'] for c in qa['checks'] if 'sincronia' in c['name']), 'fatos_centrais_com_fonte': 'PARCIAL (fontes secundárias; primárias inacessíveis)', 'licencas_documentadas': 'PARCIAL (voz edge-tts: termos comerciais pouco claros)',
         'sem_clonagem_de_voz': True, 'qa_visual_humano': 'NÃO (revisão feita pelo autor em fotos de teste/contact sheet; revisão humana assistindo com som pendente)', 'relatorio_distingue_executado': True}
approved = total >= 85 and all(v is True for v in gates.values())
sc = {'rubric_version': '2.0', 'video': f"A Guerra do Porco — piloto ({man['resolucao']} @ {man['fps']:g} fps, {man['duracao_s']} s)", 'score_total': total, 'pass_threshold': 85, 'critical_gates_passed': approved,
      'dimensions': {k: {'weight': w, 'score_0_to_5': n, 'evidence': e} for k, (w, n, e) in S.items()}, 'critical_gates': gates,
      'not_tested': ['revisão humana assistindo com som, sem som e em celular', 'versão 1080p (o pedido era piloto de baixa resolução)', 'render em GPU', 'fontes primárias da Guerra do Porco', 'licença comercial da voz'],
      'reviewed_by': 'autor (modelo); revisão humana pendente', 'review_date': datetime.date.today().isoformat(), 'aprovado': approved,
      'motivo': 'nota < 85 e gates críticos pendentes (revisão humana; licença da voz)' if not approved else 'ok'}
json.dump(sc, open(os.path.join(R, 'qa', 'scorecard.json'), 'w'), indent=1, ensure_ascii=False)
ck = lambda d: '\n'.join(f"- {'✅' if c['pass'] else '❌'} {c['name']} — {c['detail']}" for c in d['checks'])
md = f"""# QA — A Guerra do Porco (piloto)
**Vídeo:** `renders/pilot_540.mp4` — {man['resolucao']} @ {man['fps']:g} fps, {man['duracao_s']} s, {man['codec_video']} + {man['codec_audio']}, {man['tamanho_mb']} MB · **Render:** Blender {man['renderer']['blender']} Cycles CPU ({man['renderer']['amostras']} spp + OIDN), {man['tempo_total_render_s']:.0f} s de render em CPU de 4 núcleos · **Montagem:** Remotion (planos, dissolves, legendas em React) + FFmpeg (grade, encode).
**Resultado automático:** {qa['score_checks']} (qa.py) + {ex['score_checks']} (qa_extra.py). **Scorecard:** {total}/100 → **{'APROVADO' if approved else 'NÃO aprovado'}** pela rubrica V2 (mínimo 85 e gates críticos).

## Executado (com evidência)
{ck(qa)}
{ck(ex)}
- **Fidelidade vs referência** (7 métricas; razão meu/canal, ideal ≈ 1): {'; '.join(re.sub(r'\*|\|', '', r).split()[0] + ' ' + r.strip('| ').split('|')[-1].strip() for r in rows)} — detalhe em `qa/fidelity-report.md`.
- **Contorno de tinta** (razão espessura grossa/fina p90/p10): referência {om['referencia']['razao_p90_p10_mediana']} · piloto {om['piloto']['razao_p90_p10_mediana']} (`qa/outline-metrics.json`); versão antiga ≈ 2,0.
- **Determinismo:** {det}.
- Quadros: 694 (S1 117, S2 130, S3 125, S4 143, S5 72, S6 107), nenhum faltando; passada 1 (pares) + passada 2 (ímpares).
- Revisão visual **feita por mim** em fotos de teste de todos os planos, em folhas de contato e em quadros 540×960 (achou e corrigiu: legendas sobrepostas, vela do convés, sombra dos abetos, preto da tinta); evidências em `qa/pre-render-stills.png`, `qa/pre-render-review.md`, `renders/contact_540.png`.

## Recalibrações declaradas (o que mudou e por quê)
- **Verde nunca lidera** e **sombras azul/roxo**: as regras originais (máx < 12 % de pixels "verdes"; > 55 % de sombras azul/roxo) **não são cumpridas pelos próprios prints** (medido: verde máx 16,8 %, sombras azul/roxo 39,6 %). Os limiares passaram a ser relativos à referência.
- **Cortes secos**: o limiar de "salto médio > 14" reprovava movimento rápido sustentado; os prints têm 16–22 % dos quadros acima disso. Agora detecta **spike isolado** (> 20 e ≥ 3× a mediana local).
- **Preto da tinta**: medido RGB≈33,22,35 nos prints (o piloto saía ≈14,4,11); levantado na grade para ameixa escura.

## Não executado / limitações (declaradas)
{chr(10).join('- ' + x for x in sc['not_tested'])}
- Texturas e modelos são **procedurais** (código), não pintados por um artista; sem cavalos/arquibancadas do canal (não fazem parte da história).
- Voz `edge-tts`: termos comerciais pouco claros → regravar com voz licenciada antes de monetizar.
- Conflito de metas de áudio: V2 sugere −15 LUFS/−1,0 dBTP; usado o perfil v3.1 (−14/−1,5).
"""
open(os.path.join(R, 'qa', 'qa-report.md'), 'w', encoding='utf-8').write(md); print('ok', total, 'aprovado' if approved else 'não aprovado')
