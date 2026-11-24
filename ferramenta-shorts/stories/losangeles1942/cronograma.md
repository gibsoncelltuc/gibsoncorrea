# CRONOGRAMA - Guerras Inusitadas EP 20 - A Batalha de Los Angeles

Gerado em 24/11 02:57 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | SOL, CID | - | apartment, house_two, marco_hollywood, searchlight, lamppost | - | Uma cidade inteira passou a noite atirando no céu, e não havia inimigo
b1 | simples | street | reveal | CID, CID | 8 | marco_hollywood | - | Era fevereiro de mil novecentos e quarenta e dois, logo depois de Pear
b2 | chave | harbor | group | CID, SOL | 10 | marco_hollywood | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Na véspera, um submarino japonês tinha atirado na Califórnia, e todo m
b3 | simples | harbor | two | SOL, CID | - | apartment, house_two, marco_hollywood, searchlight, lamppost | - | Na madrugada, as sirenes tocaram, as luzes da cidade se apagaram, e ho
b4 | chave | mountain | orbit | SOL, SOL | 48 | cannon, canhao_moderno, marco_hollywood | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Alguém viu um objeto no céu, e os soldados começaram a atirar com canh
b5 | simples | harbor | group | SOL, GEN | 10 | marco_hollywood | - | Os soldados juravam que havia inimigos no céu. Acontece que não havia 
b6 | chave | street | crowd | CID, CID | 48 | apartment, house_two, cannon, marco_hollywood, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foram mais de mil tiros de canhão, e os estilhaços caíram na cidade, q
b7 | simples | interior madeira | two | GEN, PRE | - | - | - | No dia seguinte, os militares discutiram o que tinha acontecido, e nin
b8 | simples | interior pedra | two | PRE, GEN | - | - | - | Algumas pessoas morreram, por acidente e por susto, mas nenhum inimigo
b9 | simples | street | close | CID | - | marco_hollywood, searchlight | - | O único alvo derrotado naquela noite foi o sono de Los Angeles.
b10 | simples | street | two | CID | - | marco_hollywood | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/14 itens) | PENDENTE | python3 pesquisar.py losangeles1942
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh losangeles1942
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh losangeles1942
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local losangeles1942 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

