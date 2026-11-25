# CRONOGRAMA - E Se EP 08 - E Se Napoleão Tivesse Vencido em Waterloo?

Gerado em 25/11 17:30 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | countryside | two | NAP, WEL | - | crown | - | Napoleão ganha em Waterloo, e a Europa muda para sempre.
b1 | simples | interior madeira | close | PRO | - | crown | - | A resposta dos historiadores vai te surpreender.
b2 | transicao | countryside | reveal | FRA, FRA | 6 | - | - | Era 18 de junho de 1815, na Bélgica.
b3 | simples | interior pedra | two | NAP, FRA | - | - | - | Napoleão tinha saído do exílio e retomado o poder.
b4 | chave | countryside | crowd | FRA, ING, FRA | 40 | cannon | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ele enfrentou os ingleses de Wellington. Canhões dispararam o dia todo
b5 | chave | mountain | orbit | ING, ING, FRA | 18 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No fim da tarde, os prussianos chegaram, e Napoleão perdeu.
b6 | simples | harbor | two | NAP, WEL | - | crown | - | Foi mandado para Santa Helena, uma ilha perdida no Atlântico.
b7 | simples | interior madeira | close | PRO | - | crown | - | Acontece que, para muitos historiadores, a derrota viria igual.
b8 | simples | interior madeira | two | PRO, POV | 6 | scroll | - | Rússia e Áustria já marchavam contra ele.
b9 | simples | countryside | two | NAP, WEL | - | crown | - | Um dia famoso nem sempre muda o destino. Mas imagina que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/12 itens) | PENDENTE | python3 pesquisar.py ese_napoleao
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh ese_napoleao
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh ese_napoleao
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local ese_napoleao <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

