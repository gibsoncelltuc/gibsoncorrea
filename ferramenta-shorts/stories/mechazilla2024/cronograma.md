# CRONOGRAMA - Poder e Fama EP 16 - A Torre que Pegou um Foguete no Ar

Gerado em 25/11 06:36 | 12 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_patio | two | MUS, ENG | - | tower, tower_catch, tower_mini | - | Elon Musk mandou construir uma torre com braços gigantes, para pegar u
b1 | transicao | loc_campo | reveal | POV, POV | 6 | tower | - | Foi em outubro de dois mil e vinte e quatro, na base de foguetes da Sp
b2 | simples | loc_deserto | wide | ENG | - | booster_air | - | Normalmente, a parte de baixo do foguete é descartada, ou pousa sobre 
b3 | explicativa | loc_deserto | two | sem personagem | - | tower | corpo: kit/tower_catch (parado); emissao: rotulos/graficos; luz: estudio; camera: 2 enquadramentos sem corte seco; som:  | A ideia de Musk: tirar as pernas do foguete, e fazer a própria torre a
b4 | chave | loc_patio | crowd | ENA | - | tower, tower_catch | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os engenheiros chamaram a torre de Mechazilla, e os braços de pauzinho
b5 | simples | loc_patio | wide | ENG | - | booster_air | - | No dia do teste, o propulsor gigante decolou com trinta e três motores
b6 | simples | loc_patio | wide | ENG | - | booster_air | - | Minutos depois, ele voltou descendo de ré, direto na direção da torre.
b7 | chave | loc_patio | wide | ENA | - | tower, tower_catch | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que, no último segundo, os braços se fecharam, e seguraram o 
b8 | simples | loc_campo | wide | ENG | - | tower, tower_catch | - | Os engenheiros comemoraram: era a primeira vez na história.
b9 | explicativa | loc_deserto | two | sem personagem | - | tower_catch | corpo: kit/booster_air (sobe); emissao: fogo; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada en | Assim, o propulsor que antes ia para o lixo pode voar de novo, várias 
b10 | simples | loc_deserto | close | MUS | - | tower_catch, tower_mini | - | Parece filme de robô gigante, mas é engenharia.
b11 | simples | loc_deserto | two | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | PENDENTE | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh mechazilla2024
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh mechazilla2024
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local mechazilla2024 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 6. Estilo e enquadramento

