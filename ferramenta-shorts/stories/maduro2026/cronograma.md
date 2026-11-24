# CRONOGRAMA - Poder e Fama EP 22 - A Operação da Madrugada

Gerado em 24/11 10:56 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior loja | two | TRU, GEN | - | helicopter_air | - | Numa madrugada de janeiro de dois mil e vinte e seis, Trump autorizou 
b1 | simples | loc_cidade | reveal | POV, POV | 6 | apartment, house_two, lamppost | - | O alvo estava em Caracas, a capital da Venezuela.
b2 | simples | loc_patio | two | MAD, POV | - | helicopter_air | - | Era o presidente venezuelano Nicolás Maduro, acusado pela justiça amer
b3 | simples | interior loja | two | TRU, AGE | - | - | - | Durante meses, a inteligência americana estudou cada passo dele, em se
b4 | chave | loc_patio | crowd | SOL, SOL, SOL | 48 | helicopter_air | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Às duas da manhã, helicópteros levaram os soldados da Força Delta dire
b5 | simples | loc_pista | low | SOL | - | helicopter_air | - | Ao mesmo tempo, ataques aéreos desligaram as defesas antiaéreas do paí
b6 | simples | loc_pista | two | SOL, MAD | - | - | - | Acontece que, em menos de três horas, Maduro foi capturado e levado pa
b7 | simples | interior loja | two | TRU, GEN | - | - | - | Trump acompanhou tudo de longe, na Flórida, ao lado do diretor da CIA 
b8 | simples | loc_cidade | two | AGE, MAD | - | scroll, airplane | - | Maduro foi levado de avião para Nova York, onde responde a um processo
b9 | chave | loc_cidade | orbit | POV, POV, POV | 18 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Nenhum militar americano morreu. A notícia parou o mundo, e dividiu op
b10 | simples | loc_pista | close | TRU | - | helicopter_air | - | A operação ganhou um nome que resume tudo: Resolução Absoluta.
b11 | simples | loc_cidade | close | TRU | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/6 itens) | PENDENTE | python3 pesquisar.py maduro2026
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 5) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh maduro2026
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh maduro2026
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local maduro2026 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

