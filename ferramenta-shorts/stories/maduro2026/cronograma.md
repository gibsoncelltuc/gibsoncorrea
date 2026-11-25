# CRONOGRAMA - Poder e Fama EP 22 - A Operação da Madrugada

Gerado em 25/11 02:02 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | wide | SOL, MAD | 32 | apartment, house_two, lamppost | - | Um presidente foi capturado de madrugada, dentro da própria capital, e
b1 | chave | loc_cidade | wide | POV, POV | 6 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foi em janeiro de dois mil e vinte e seis, em Caracas, na Venezuela, n
b2 | simples | loc_pista | wide | MAD | - | - | - | Era o presidente venezuelano Nicolás Maduro, acusado pela justiça amer
b3 | chave | loc_pista | wide | SOL | 48 | helicopter_air | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Às duas da manhã, helicópteros levaram soldados da Força Delta direto 
b4 | explicativa | loc_estudio | two | sem personagem | - | helicopter_air | corpo: kit/helicopter_air (paira); emissao: velocidade; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som  | Ao mesmo tempo, ataques aéreos desligaram as defesas antiaéreas do paí
b5 | chave | loc_pista | orbit | SOL, MAD | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, em menos de três horas, Maduro foi capturado e levado pa
b6 | simples | interior loja | two | TRU, GEN | - | - | - | Trump acompanhou tudo de longe, na Flórida, ao lado do diretor da CIA 
b7 | transicao | loc_pista | wide | AGE, MAD | - | scroll, airplane | - | Maduro foi levado de avião para Nova York, onde responde a um processo
b8 | simples | loc_patio | crowd | POV, POV, POV | 18 | - | - | Nenhum militar americano morreu. A notícia parou o mundo, e dividiu op
b9 | simples | loc_patio | close | TRU | - | - | - | A operação ganhou um nome que resume tudo: Resolução Absoluta.
b10 | simples | loc_cidade | close | MAD | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (15/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | FEITO | 
10 | Render | todos os quadros renderizados nesta versao das folhas | FEITO | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | FEITO | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | PENDENTE | ./conferir.sh maduro2026
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local maduro2026 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 12. Conferencia

