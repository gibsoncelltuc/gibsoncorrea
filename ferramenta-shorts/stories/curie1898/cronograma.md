# CRONOGRAMA - Curiosidade e Ciência EP 19 - O Caderno que Ainda Brilha

Gerado em 24/11 03:14 | 13 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | PES, JOR | - | curie_box, marco_eiffel | - | Existem cadernos tão perigosos que só podem ser lidos com roupa de pro
b1 | transicao | loc_campo | reveal | POV, POV | 6 | marco_eiffel | - | Era mil oitocentos e noventa e oito, em Paris, na França.
b2 | simples | interior madeira | two | MAR, PIE | - | - | - | Marie Curie, uma polonesa genial, trabalhava com o marido Pierre num g
b3 | simples | interior madeira | group | MAR, PIE | - | curie_box | - | Mexendo em toneladas de minério, eles descobriram dois elementos novos
b4 | simples | interior madeira | close | MAR | - | curie_box | - | O rádio brilhava no escuro, com uma luz esverdeada. Marie adorava olha
b5 | simples | interior madeira | two | MAR, PIE | - | - | - | Ela carregava os frascos no bolso, e guardava na gaveta da mesa. Ningu
b6 | chave | loc_campo | crowd | MAR, PIE, JOR | 18 | marco_eiffel | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Marie ganhou dois prêmios Nobel, em física e em química. Foi a primeir
b7 | simples | loc_campo | two | MAR | - | marco_eiffel | - | Acontece que a radiação foi destruindo a saúde dela, aos poucos. Em mi
b8 | simples | interior pedra | two | PES, JOR | - | crate, curie_box | - | Mas os cadernos dela continuam radioativos até hoje, guardados em caix
b9 | simples | interior pedra | low | PES | - | curie_box | - | Quem quer ler precisa assinar um termo de responsabilidade e usar roup
b10 | chave | loc_montanha | orbit | POV, POV, PES | 16 | curie_box, marco_eiffel, picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E o rádio leva cerca de mil e seiscentos anos só para perder metade da
b11 | simples | loc_montanha | close | MAR | - | curie_box, marco_eiffel | - | Ou seja: os cadernos de Marie Curie vão continuar radioativos por muit
b12 | simples | loc_campo | close | PES | - | marco_eiffel | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/13 itens) | PENDENTE | python3 pesquisar.py curie1898
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 2) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh curie1898
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh curie1898
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local curie1898 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 2. Pesquisa de campo

