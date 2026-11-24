# CRONOGRAMA - Poder e Fama EP 18 - O Jogo de Tabuleiro do Trump

Gerado em 24/11 22:39 | 13 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | TRU, EXE | - | boardgame, marco_liberdade | - | Muito antes da política, Donald Trump lançou um jogo de tabuleiro com 
b1 | transicao | loc_cidade | reveal | POV, POV | 6 | marco_liberdade | - | Era mil novecentos e oitenta e nove, nos Estados Unidos. Trump era um 
b2 | simples | interior loja | two | EXE, TRU | - | boardgame | - | Uma grande fábrica de brinquedos fez o jogo: comprar e vender prédios,
b3 | simples | interior loja | close | TRU | - | boardgame | - | As notas do jogo eram de dez, cinquenta e cem milhões de dólares. Com 
b4 | simples | interior madeira | two | PAI, FIL | - | boardgame | - | Acontece que o manual tinha mais de doze páginas. As famílias abriam a
b5 | simples | interior madeira | group | FIL, PAI | - | boardgame | - | Muita gente comprou só de presente, ou de curiosidade, e nunca tirou a
b6 | chave | loc_cidade | crowd | EXE, POV, POV | 30 | marco_liberdade | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A fábrica esperava vender dois milhões de jogos. Vendeu oitocentos mil
b7 | simples | interior loja | two | EXE, TRU | - | - | - | O jogo saiu das lojas, e ficou esquecido por anos.
b8 | simples | loc_pista | two | TRU, EXE | - | boardgame, tv | - | Até que, em dois mil e quatro, Trump virou estrela de um programa de T
b9 | chave | loc_cidade | crowd | TRU, POV, POV | 18 | boardgame, marco_liberdade | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E o jogo voltou às lojas, com regras mais simples, e com a frase famos
b10 | simples | interior pedra | two | PAI, FIL | - | crate, boardgame | - | Hoje, as caixas originais de mil novecentos e oitenta e nove viraram i
b11 | simples | loc_pista | two | TRU | - | boardgame | - | Um jogo sobre ficar bilionário, que acabou virando só uma curiosidade 
b12 | simples | loc_cidade | close | TRU | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py trumpgame1989
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 3) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh trumpgame1989
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh trumpgame1989
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local trumpgame1989 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

