# CRONOGRAMA - Guerras Inusitadas EP 21 - A Invasão da Ilha Vazia

Gerado em 25/11 18:26 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | wide | USA, CAN | 32 | ship | - | Trinta e quatro mil soldados desembarcaram numa ilha sem nenhum inimig
b1 | simples | harbor | crowd | OFF, USA | 32 | dog_sit | - | E mesmo assim, houve mortos nessa invasão.
b2 | simples | arctic | group | USA, CAN, USA | - | navio_vapor, airplane | - | Em 1943, a ilha de Kiska, no Alasca, estava com os japoneses.
b3 | simples | harbor | reveal | USA, CAN | - | aviao_ww2, tanque_ww2, navio em movimento, navios de guerra ao fundo, no tamanho real | - | Americanos e canadenses chegaram com navios, aviões e tanques.
b4 | chave | harbor | crowd | USA | 48 | aviao_ww2, canhao_moderno | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Bombardearam a ilha durante semanas inteiras.
b5 | simples | interior pedra | two | USA, CAN | - | - | - | Acontece que os japoneses já tinham ido embora.
b6 | transicao | harbor | wide | sem personagem | - | ship | - | Saíram escondidos na neblina, semanas antes.
b7 | chave | harbor | orbit | USA, CAN, USA | 48 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | No nevoeiro, os Aliados atiraram uns nos outros.
b8 | simples | harbor | orbit | USA, CAN | 48 | navio_encouracado, navios de guerra ao fundo, no tamanho real | - | Mais de vinte soldados morreram, e um navio bateu numa mina.
b9 | simples | harbor | prop | USA, CAN | - | dog_sit | - | Na ilha inteira, só acharam alguns cachorros abandonados.
b10 | transicao | harbor | wide | USA, CAN | 32 | ship | - | Uma invasão contra cachorros. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/16 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | REFAZER (a etapa anterior mudou) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | REFAZER (a etapa anterior mudou) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh kiska1943
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh kiska1943
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local kiska1943 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

