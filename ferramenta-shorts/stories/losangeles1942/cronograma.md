# CRONOGRAMA - Guerras Inusitadas EP 20 - A Batalha de Los Angeles

Gerado em 25/11 09:50 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | SOL, CID | 12 | apartment, house_two, searchlight, lamppost | - | Uma cidade inteira passou a noite atirando no céu, e não havia inimigo
b1 | chave | street | wide | CID, CID | 8 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Era fevereiro de mil novecentos e quarenta e dois, logo depois de Pear
b2 | simples | harbor | orbit | CID | - | submarino_ww2 | - | Na véspera, um submarino japonês tinha atirado na Califórnia, e todo m
b3 | simples | harbor | low | SOL, CID | - | apartment, house_two, searchlight, lamppost | - | Na madrugada, as sirenes tocaram, as luzes da cidade se apagaram, e ho
b4 | simples | street | wide | SOL | 3 | cannon, canhao_moderno | - | Alguém viu um objeto no céu, e os soldados começaram a atirar com canh
b5 | simples | harbor | group | SOL, GEN | 12 | - | - | Os soldados juravam que havia inimigos no céu. Acontece que não havia 
b6 | chave | loc_cidade | crowd | CID, CID | 48 | apartment, house_two, cannon, canhao_moderno, searchlight, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foram mais de mil tiros de canhão, e os estilhaços caíram na cidade, q
b7 | simples | interior madeira | two | GEN, PRE | - | - | - | No dia seguinte, os militares discutiram o que tinha acontecido, e nin
b8 | simples | loc_cidade | two | CID, CID | 12 | - | - | Algumas pessoas morreram, por acidente e por susto, mas nenhum inimigo
b9 | simples | street | two | CID | - | searchlight | - | O único alvo derrotado naquela noite foi o sono de Los Angeles.
b10 | simples | street | close | CID | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/15 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh losangeles1942
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh losangeles1942
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local losangeles1942 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

