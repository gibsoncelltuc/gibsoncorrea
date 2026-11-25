# CRONOGRAMA - Guerras Inusitadas EP 20 - A Batalha de Los Angeles

Gerado em 25/11 18:39 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | street | two | SOL, CID | 12 | apartment, house_two, searchlight, lamppost | - | Uma cidade atirou no céu a noite toda contra um inimigo invisível.
b1 | simples | street | close | CID | - | searchlight | - | E até hoje ninguém sabe no que eles atiravam.
b2 | chave | street | wide | CID, CID | 8 | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1942, Los Angeles vivia com medo do Japão.
b3 | simples | harbor | wide | CID | - | submarino_ww2 | - | Na véspera, um submarino japonês atirou na Califórnia.
b4 | simples | harbor | low | SOL, CID | - | searchlight | - | De madrugada, sirenes tocaram e holofotes varreram o céu.
b5 | simples | street | wide | SOL | - | cannon, canhao_moderno | - | Alguém viu algo, e os canhões antiaéreos começaram a atirar.
b6 | chave | loc_cidade | orbit | CID, CID | - | apartment, house_two, canhao_moderno, searchlight, lamppost | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foram mais de mil tiros, e estilhaços caíram na cidade.
b7 | simples | loc_cidade | two | SOL, GEN | - | - | - | Acontece que não havia nada lá em cima.
b8 | simples | loc_cidade | group | CID, CID | 12 | - | - | Algumas pessoas morreram por acidente e susto.
b9 | simples | street | two | SOL, CID | 12 | searchlight | - | O medo venceu o sono. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (14/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | FEITO | 
10 | Render | todos os quadros renderizados nesta versao das folhas | PENDENTE | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh losangeles1942
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | REFAZER (a etapa anterior mudou) | bash auditar_acoes.sh local losangeles1942 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 10. Render

