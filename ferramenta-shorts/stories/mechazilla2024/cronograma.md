# CRONOGRAMA - Poder e Fama EP 16 - A Torre que Pegou um Foguete no Ar

Gerado em 25/11 17:17 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_patio | two | MUS, ENG | - | tower, tower_catch, tower_mini | - | Foguete pousa no chão? Este foi agarrado no ar por uma torre.
b1 | simples | loc_deserto | two | MUS | - | tower_catch, tower_mini | - | Parece filme de robô gigante. Mas é engenharia de verdade.
b2 | chave | loc_campo | wide | POV, POV | 6 | tower | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foi em outubro de 2024, na base da SpaceX, no Texas.
b3 | simples | loc_deserto | wide | ENG | - | booster_air | - | A parte de baixo do foguete costumava ir para o lixo.
b4 | explicativa | loc_deserto | two | sem personagem | - | tower | corpo: kit/tower_catch (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som:  | A ideia: tirar as pernas e fazer a torre agarrar o propulsor.
b5 | simples | loc_patio | two | ENA | - | tower, tower_catch | - | Os engenheiros chamaram a torre de Mechazilla.
b6 | transicao | loc_patio | wide | ENG | - | booster_air | - | O propulsor decolou com trinta e três motores acesos.
b7 | simples | loc_patio | wide | ENG | - | booster_air | - | Minutos depois, voltou descendo de ré, direto na torre.
b8 | chave | loc_patio | wide | ENA | - | tower, tower_catch | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, no último segundo, os braços se fecharam e seguraram.
b9 | simples | loc_campo | two | ENG, ENG | - | tower, tower_catch | - | Os engenheiros comemoraram: era a primeira vez na história.
b10 | simples | loc_patio | two | MUS, ENG | - | tower_catch, tower_mini | - | Uma torre que pega foguete no ar. E não é filme.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh mechazilla2024
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh mechazilla2024
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local mechazilla2024 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

