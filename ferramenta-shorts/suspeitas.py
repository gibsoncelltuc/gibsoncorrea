#!/usr/bin/env python3
# CENAS SUSPEITAS (24/11, pedido do Gibson): compara o que cada FRASE diz com o que a CENA tem e marca o que nao bate,
# para o olho ir direto nelas (storyboard e frase a frase). Nao bloqueia: vai para stories/<id>/suspeitas.md e para a lista_revisao.
# uso: python3 suspeitas.py <id>
import json, re, sys, unicodedata, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sentido
ID = sys.argv[1]; B = json.load(open(f'videos/{ID}/beats.json')); BT = B['beats']
n = lambda t: unicodedata.normalize('NFKD', str(t).lower()).encode('ascii', 'ignore').decode()
MUITA = r'\b(multidao|milhares(?! de (vezes|anos|dias|horas|quilos|toneladas|metros|quilometros|km|dolares|reais|libras|francos|litros))|centenas(?! de (vezes|anos|dias|horas|quilos|toneladas|metros|quilometros|km|dolares|reais|libras|francos|litros))|todo mundo|pais inteiro|cidade inteira|povo|exercito|tropas?|soldados|batalhao|plateia|torcida|torcedores|moradores|funcionarios|manifestantes|dancarinos|pessoas|congresso|assembleia|parlamento|senado|deputados|vereadores|eleitores|plateia|convidados)\b'
ANIM = r'\b(cavalos?|ursos?|porcos?|galinhas?|emus?|gansos?|vacas?|bois?|cachorros?|caes|gatos?|ovelhas?|cabras?|burros?|veados?|raposas?|lobos?|coelhos?|leao|leoes|elefantes?|patos?|galos?|gaivotas?|passaros|passarinhos|tentilhoes|abelhas?)\b'
NOITE = r'\b(noite|madrugada|meia-noite|escuro|de noite)\b'
EXTERNO = r'\b(no mar|na praia|no campo|na rua|nas ruas|na floresta|na mata|no monte|na montanha|no deserto|no ceu|no cais|no porto|na ilha)\b'
out = []
_am = re.search(r'(\d{3,4})$', ID); _ANO = int(B.get('ano') or (_am.group(1) if _am else 2000)) if str(B.get('ano') or (_am.group(1) if _am else 2000)).isdigit() else 2000   # celular so' depois de 2007, TV de 1950 em diante
for k, b in enumerate(BT):
    if b.get('explica') or b.get('susp_ok') or b.get('mapa') and len((b.get('say') or '').split()) < 8: continue   # susp_ok: cena revisada no olho (ex.: 'o Congresso ofereceu um acordo' = decisao, nao multidao)
    s = n(b.get('say', '')); who = b.get('who') or []; cr = (b.get('crowd') or {}).get('n') or 0; fx = ' '.join(b.get('fx') or [])
    sc = sentido.cena(b.get('say', ''))
    _mm = re.search(MUITA, s); _negm = bool(_mm and re.match(r'\s+(nunca|nao|jamais)\b', s[_mm.end():])) or bool(_mm and re.match(r'(milhares(?! de (vezes|anos|dias|horas|quilos|toneladas|metros|quilometros|km|dolares|reais|libras|francos|litros))|centenas)$', _mm.group(1)) and not re.match(r'\s+de\s+(pessoas|soldados|homens|mulheres|moradores|torcedores|manifestantes|fas|trabalhadores|operarios|criancas)', s[_mm.end():])) or bool(_mm and re.search(r'\b(nao|nunca|nem|sem|ninguem)\b(\s+\w+){0,3}\s*$', s[:_mm.start()]))
    if _mm and not _negm and not cr and len(who) < 3 and not b.get('batalha') and not b.get('emus'):
        out.append((k, 'a frase fala de MUITA GENTE e a cena tem ' + str(len(who)) + ' pessoa(s) e nenhuma multidao'))
    TELA = r'\b(aplicativo|app|site|internet|e-?mail|tweet\w*|postou|postava|perfil|redes sociais|celular|online|computador|videogame|transmissao|ao vivo na tv|televisao)\b'
    _tem_tela = any(re.search(r'phone|tv|telao|computer|pc|laptop|monitor|screen|pong|chess_pc|tablet', str(p_[0])) for p_ in (b.get('props') or []) if isinstance(p_, list))
    if re.search(TELA, s) and not _tem_tela and b.get('tela') is not False and not b.get('explica') and not b.get('mapa') and not b.get('_cta'):
        out.append((k, 'a frase fala de CELULAR/INTERNET/TELA e a cena nao tem celular nem tela'))
    _cr_ok = r'candidat|hussard|infantaria|acampamento|cavalaria|regimento|marinha|plenario|todos|teceloes|homens|mil |voluntari|milicia|competidor|atleta|estadio|jogo|venceu|copa|nobel|premio|cerimonia|operarios|engenheiros|funcionarios|cientistas|comemor|festa|aplaud|assist|public|plateia|torcid|lotar|lotou|lotaram|multidao|milhares|centenas|todo mundo|mundo inteiro|cidade|povo|pais|rua|marcha|protest|fila|compr|vend|esgot|celebr|desfile|convidad|leilao|mercado|feira|jornais|imprensa|noticia|viral|rodou o mundo|eleic|urna|vot|assunto|soldad|tropa|exercito|guerra|batalha|invad|atac|frota|navios|marinheiros|tripula|dancar|danc'
    if cr > 0 and not re.search(MUITA, s) and not re.search(_cr_ok, s) and not b.get('batalha') and not b.get('emus') and not b.get('_cta') and not b.get('mapa'):
        out.append((k, 'MULTIDAO SEM MOTIVO: a frase nao fala de gente, publico ou festa e a cena tem ' + str(cr) + ' figurantes'))
    _bich = any(re.search(r'bee|abelha|finch|bird|passar|emu|gans|goose|chicken|galinh|horse|cavalo|pig|porco|dog|cow|fish|peixe|lagosta|lobster', str(p_[0])) for p_ in (b.get('props') or []) if isinstance(p_, list))
    _comida = re.sub(r'\b(carne|consome|ensopado|pernil|bife|sopa|prato|filet|file|costela|assado|churrasco|linguica) de (\w+)', ' ', re.sub(r'\bservi\w* (o |a |um |uma )?(?!consome|ensopado|carne|pernil|sopa|bife)\w+', ' ', s))   # 'carne de elefante' e' comida, nao bicho em cena
    if re.search(ANIM, _comida) and not (b.get('animals') or b.get('emus') or b.get('montado') or _bich) and not re.search(r'cavalaria', s):
        out.append((k, 'a frase cita ANIMAL e a cena nao tem animal'))
    if b.get('batalha') is True and not re.search(r'tomar|tomaram|queim|cerc|revolt|guerra|batalha|lut|atac|invad|tiro|atir|dispar|bomb|explo|soldad|tropa|exercito|combat|canh|fogo|arma|metralh|espada|duelo|briga|captur|ofensiv', s):
        out.append((k, 'cena com BATALHA e a frase nao fala de luta nenhuma'))
    if sc.get('sem_violencia') and (b.get('batalha') is True or 'burst' in fx):
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
        elif m.startswith('MULTIDAO SEM MOTIVO'):
            b['crowd'] = {'n': 0}; b['_susp_ok'] = True; feito.append(f'b{k}: multidao sem motivo tirada')
        elif m.startswith('cena com BATALHA e a frase nao fala'):
            b['batalha'] = False; b['tiros'] = False; feito.append(f'b{k}: batalha desligada (frase sem luta)')
        elif m.startswith('a frase fala de CELULAR') and not b.get('_susp_tela') and _ANO >= 1950:
            b.setdefault('props', []).append(['kit/tv' if (_ANO < 2007 or re.search(r'televis|transmiss|ao vivo', n(b.get('say', '')))) else 'kit/phone', 0.0, -0.8, 0.9, {'fixo': True}]); b['_susp_tela'] = True; b['_susp_ok'] = True; feito.append(f'b{k}: celular/tela posto na cena')
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
