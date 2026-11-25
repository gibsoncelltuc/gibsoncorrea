# CRONOGRAMA - Curiosidade e Ciência EP 11 - O Raio X de Röntgen

Gerado em 25/11 18:29 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | ROE, ANA | - | marco_wurzburg, xray_plate | - | A primeira foto de dentro do corpo assustou a esposa do cientista.
b1 | simples | interior madeira | two | ANA | - | xray_plate | - | Conta-se que ela viu ali a própria morte.
b2 | chave | street | wide | POV, POV | 6 | crookes_tube, marco_wurzburg | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1895, Wilhelm Röntgen testava um tubo de vidro.
b3 | simples | interior madeira | two | ROE | - | crookes_tube | - | Uma noite, cobriu o tubo e apagou a luz.
b4 | simples | interior madeira | close | ROE | - | xray_plate | - | Acontece que, do outro lado da sala, uma tela brilhou no escuro.
b5 | simples | interior madeira | two | ROE | - | xray_plate | - | Pôs a mão na frente e viu os próprios ossos.
b6 | simples | interior madeira | group | ROE, ANA | - | xray_plate | - | Depois, fotografou a mão da esposa, Anna, com a aliança.
b7 | simples | interior madeira | two | ROE, JOR | - | xray_plate | - | Sem saber o que era, chamou de raio X.
b8 | chave | street | orbit | ROE, MED, POV | 18 | marco_wurzburg | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ganhou o primeiro Nobel de Física.
b9 | simples | street | two | ROE, ANA | - | xray_plate | - | Um raio desconhecido, e foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/12 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh rontgen1895
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh rontgen1895
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local rontgen1895 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

