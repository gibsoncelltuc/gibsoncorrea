#!/usr/bin/env python3
# CENAS SUSPEITAS (24/11, pedido do Gibson): compara o que cada FRASE diz com o que a CENA tem e marca o que nao bate,
# para o olho ir direto nelas (storyboard e frase a frase). Nao bloqueia: vai para stories/<id>/suspeitas.md e para a lista_revisao.
# uso: python3 suspeitas.py <id>
import json, re, sys, unicodedata, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sentido
ID = sys.argv[1]; B = json.load(open(f'videos/{ID}/beats.json')); BT = B['beats']
n = lambda t: unicodedata.normalize('NFKD', str(t).lower()).encode('ascii', 'ignore').decode()
MUITA = r'\b(multidao|milhares|centenas|todo mundo|pais inteiro|cidade inteira|povo|exercito|tropas?|soldados|batalhao|plateia|torcida|torcedores|moradores|funcionarios|manifestantes|dancarinos|pessoas)\b'
ANIM = r'\b(cavalos?|ursos?|porcos?|galinhas?|emus?|gansos?|vacas?|bois?|cachorros?|caes|gatos?|ovelhas?|cabras?|burros?|veados?|raposas?|lobos?|coelhos?|leao|leoes|elefantes?|patos?|galos?|gaivotas?|passaros|passarinhos|tentilhoes|abelhas?)\b'
NOITE = r'\b(noite|madrugada|meia-noite|escuro|de noite)\b'
EXTERNO = r'\b(no mar|na praia|no campo|na rua|nas ruas|na floresta|na mata|no monte|na montanha|no deserto|no ceu|no cais|no porto|na ilha)\b'
out = []
for k, b in enumerate(BT):
    if b.get('explica') or b.get('mapa') and len((b.get('say') or '').split()) < 8: continue
    s = n(b.get('say', '')); who = b.get('who') or []; cr = (b.get('crowd') or {}).get('n') or 0; fx = ' '.join(b.get('fx') or [])
    sc = sentido.cena(b.get('say', ''))
    _mm = re.search(MUITA, s); _negm = bool(_mm and re.match(r'\s+(nunca|nao|jamais)\b', s[_mm.end():])) or bool(_mm and re.match(r'(milhares|centenas)$', _mm.group(1)) and not re.match(r'\s+de\s+(pessoas|soldados|homens|mulheres|moradores|torcedores|manifestantes|fas|trabalhadores|operarios|criancas)', s[_mm.end():])) or bool(_mm and re.search(r'\b(nao|nunca|nem|sem|ninguem)\b(\s+\w+){0,3}\s*$', s[:_mm.start()]))
    if _mm and not _negm and not cr and len(who) < 3 and not b.get('batalha') and not b.get('emus'):
        out.append((k, 'a frase fala de MUITA GENTE e a cena tem ' + str(len(who)) + ' pessoa(s) e nenhuma multidao'))
    _bich = any(re.search(r'bee|abelha|finch|bird|passar|emu|gans|goose|chicken|galinh|horse|cavalo|pig|porco|dog|cow|fish|peixe|lagosta|lobster', str(p_[0])) for p_ in (b.get('props') or []) if isinstance(p_, list))
    if re.search(ANIM, s) and not (b.get('animals') or b.get('emus') or b.get('montado') or _bich) and not re.search(r'cavalaria', s):
        out.append((k, 'a frase cita ANIMAL e a cena nao tem animal'))
    if sc.get('sem_violencia') and (b.get('batalha') is True or 'burst' in fx or b.get('impact')):
        out.append((k, 'frase SEM violencia de verdade (' + '; '.join(sentido.explicar(b.get('say', ''))) + ') e a cena tem batalha/explosao'))
    if re.search(sentido.DISPARO.replace(r'acert\w*|ating\w*|', ''), s) and not sc.get('sem_violencia') and b.get('tiros') is False and 'burst' not in fx and not b.get('acoes'):
        out.append((k, 'a frase tem TIRO/EXPLOSAO de verdade e a cena esta sem tiro nem explosao'))
    if re.search(NOITE, s) and (b.get('hora') in ('dia', 'tarde', 'amanhecer') or b.get('light') in ('day', 'noon')):
        out.append((k, 'a frase e\' de NOITE e a cena esta de dia'))
    if re.search(EXTERNO, s) and b.get('interior'):
        out.append((k, 'a frase acontece AO AR LIVRE (' + re.search(EXTERNO, s).group(1) + ') e a cena esta dentro de uma sala'))
    if sc.get('nao_interior') and b.get('interior') == 'madeira':
        out.append((k, '"casa" na frase e\' valor, nao lugar, e a cena esta dentro de casa'))
# --corrigir: conserta sozinho o que e' seguro (antes do mkvideo): animal citado sem animal -> usa o bicho que o proprio video ja tem;
# muita gente sem multidao -> multidao de 12 com os figurinos da cena. O resto fica so' marcado para o olho.
if '--corrigir' in sys.argv and out:
    _bichos = [p_ for b_ in BT for p_ in (b_.get('props') or []) if isinstance(p_, list) and re.search(r'bee|finch|bird|emu|goose|chicken|lobster|fish', str(p_[0]))]
    feito = []
    for k, m in out:
        b = BT[k]
        if m.startswith('a frase cita ANIMAL') and _bichos and not b.get('_susp_ok'):
            b.setdefault('props', []).append([_bichos[0][0], 0.9, 1.0, _bichos[0][3] if len(_bichos[0]) > 3 and not isinstance(_bichos[0][3], dict) else 1.2, {'fixo': True}]); b['_susp_ok'] = True; feito.append(f'b{k}: {_bichos[0][0]} posto na cena')
        elif m.startswith('a frase fala de MUITA GENTE') and not b.get('interior') and not b.get('_susp_ok'):
            ofs = sorted({str(w).split(':')[0] for w in (b.get('who') or [])}) or ['POV']; b['crowd'] = {'n': 12, 'outfits': ofs, 'march': False}; b['_susp_ok'] = True; feito.append(f'b{k}: multidao de 12 ({", ".join(ofs)})')
    if feito:
        json.dump(B, open(f'videos/{ID}/beats.json', 'w'), ensure_ascii=False, indent=1); print('CORRIGIDO SOZINHO: ' + '; '.join(feito))
        out = [(k, m) for k, m in out if not BT[k].get('_susp_ok')]
txt = f'# CENAS SUSPEITAS - {ID} (frase x cena; olhar estas primeiro no storyboard e no frase a frase)\n'
txt += ''.join(f'- b{k}: {m} -> "{BT[k]["say"][:70]}"\n' for k, m in out) or '- nenhuma\n'
open(f'stories/{ID}/suspeitas.md', 'w').write(txt)
print(f'SUSPEITAS: {len(out)} cena(s) (stories/{ID}/suspeitas.md)')
for k, m in out: print(f'  b{k}: {m}')
