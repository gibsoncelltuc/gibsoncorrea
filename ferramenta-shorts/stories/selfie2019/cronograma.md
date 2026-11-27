# CRONOGRAMA - Poder e Fama EP 28 - A Selfie na ONU

Gerado em 27/11 19:49 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior pedra | reveal | BUK, DIP | - | phone, podium, un_flags, un_wall | - | Um presidente roubou a cena da ONU com uma selfie.
b1 | simples | interior madeira | two | POV, POV | - | un_flags | - | Foi em Nova York, na Assembleia Geral. Ali, discursos são longos e sér
b2 | simples | interior loja | two | BUK, DIP | - | un_flags | - | Nayib Bukele, de El Salvador, tinha só trinta e oito anos.
b3 | simples | interior loja | close | BUK | - | podium, un_flags, un_wall | - | Ele foi ao púlpito e pediu: só um segundo, por favor.
b4 | simples | interior loja | two | BUK | - | phone, un_flags | - | Tirou o celular do bolso e virou de costas para o plenário.
b5 | chave | interior pedra | two | BUK, DIP | - | un_flags | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Clique! Uma selfie com a ONU inteira atrás dele.
b6 | simples | interior madeira | two | BUK, DIP | - | un_flags | - | Ele brincou: mais gente verá a selfie do que o discurso.
b7 | chave | interior pedra | two | POV, POV, REP, BUK | - | globe, podium, un_flags, un_wall | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E ele estava certo: a foto rodou o planeta em poucas horas.
b8 | simples | interior pedra | reveal | BUK, DIP | - | phone, podium, un_flags, un_wall | - | Alguns viram desrespeito, outros viram genialidade, e foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | PENDENTE | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh selfie2019
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh selfie2019
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local selfie2019 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 5. Voz

