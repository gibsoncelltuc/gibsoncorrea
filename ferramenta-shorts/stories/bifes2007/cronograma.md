# CRONOGRAMA - Poder e Fama EP 06 - Os Bifes com o Nome do Trump

Gerado em 25/11 17:25 | 9 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | TRU, VEN | - | steak | - | O bife do Trump sumiu das lojas em só dois meses.
b1 | simples | interior madeira | two | VEN | - | steak | - | E o resultado foi bem menor do que se imaginava.
b2 | simples | interior loja | two | TRU, VEN | - | steak | - | Em 2007, ele lançou a Trump Steaks.
b3 | chave | interior pedra | group | VEN, CLI, POV | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Os pacotes custavam até novecentos e noventa e nove dólares.
b4 | simples | interior loja | two | VEN, CLI | - | steak | - | Acontece que, em julho, a loja já não oferecia os bifes.
b5 | chave | loc_cidade | wide | TRU, JOR | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Uma reportagem estimou menos de cinquenta mil dólares no total.
b6 | simples | interior pedra | two | CLI, VEN | - | - | - | Em 2014, a marca foi cancelada.
b7 | simples | interior madeira | two | TRU, CLI | - | steak | - | Mesmo assim, o bife seguiu no cardápio dos hotéis dele.
b8 | simples | loc_cidade | two | TRU, VEN | - | steak | - | Nome famoso não salvou a carne. E foi assim que...

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/11 itens) | PENDENTE | python3 pesquisar.py bifes2007
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh bifes2007
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bifes2007
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local bifes2007 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

