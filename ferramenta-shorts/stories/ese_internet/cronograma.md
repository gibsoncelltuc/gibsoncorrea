# CRONOGRAMA - E Se EP 04 - E Se a Internet Acabasse por Um Dia?

Gerado em 25/11 17:11 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | POV, PRO | - | phone | - | E se a internet do mundo inteiro caísse amanhã por um dia?
b1 | simples | loc_cidade | reveal | POV, POV | 6 | - | - | Parece impossível. Mas pedaços disso já aconteceram.
b2 | simples | loc_pista | two | POV, POV | - | phone | - | Em 2021, WhatsApp, Instagram e Facebook caíram por seis horas.
b3 | chave | loc_pista | crowd | PIL, POV, POV | 30 | miners, airplane | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 2024, uma atualização com defeito travou oito milhões de computador
b4 | simples | interior loja | two | CAI, POV | - | coin | - | Sem internet, sem cartão: só dinheiro de papel.
b5 | simples | loc_pista | two | PRO, POV | - | - | - | Hospitais e bancos voltariam para a caneta, com filas enormes.
b6 | simples | loc_pista | close | PRO | - | phone | - | O mais estranho? Não saber o que fazer com as mãos.
b7 | simples | loc_cidade | two | POV, POV | - | ball | - | Gente conversando na rua, jogando bola, olhando para o céu.
b8 | chave | loc_patio | crowd | PRO, POV | 12 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Pesquisadores dizem que, longe das telas, muita gente dorme melhor.
b9 | simples | loc_cidade | two | POV, PRO | - | phone | - | Você aguentaria um dia? Responde enquanto ainda tem internet.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/11 itens) | PENDENTE | python3 pesquisar.py ese_internet
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh ese_internet
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh ese_internet
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local ese_internet <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

