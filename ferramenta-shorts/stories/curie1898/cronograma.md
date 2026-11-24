# CRONOGRAMA - Curiosidade e Ciência EP 19 - O Caderno que Ainda Brilha

Gerado em 24/11 23:35 | 13 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_campo | two | PES, JOR | - | curie_box, marco_eiffel | - | Existem cadernos tão perigosos que só podem ser lidos com roupa de pro
b1 | chave | loc_campo | crowd | POV | 6 | marco_eiffel | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Era mil oitocentos e noventa e oito, em Paris, na França.
b2 | simples | interior madeira | two | MAR, PIE | - | - | - | Marie Curie trabalhava com o marido Pierre num galpão velho e gelado.
b3 | simples | interior madeira | group | MAR, PIE | - | - | - | O galpão tinha o teto furado, chovia dentro, e ela mexia a mistura com
b4 | simples | interior madeira | two | MAR, PIE | - | curie_box | - | Mexendo em toneladas de minério, eles descobriram dois elementos novos
b5 | simples | interior madeira | close | MAR | - | curie_box | - | O rádio brilhava no escuro, e Marie adorava olhar os frascos à noite.
b6 | simples | interior madeira | two | MAR, PIE | - | - | - | Ela carregava frascos no bolso. Ninguém sabia do perigo.
b7 | chave | loc_campo | orbit | MAR | 18 | marco_eiffel | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Ela ganhou dois prêmios Nobel, a primeira pessoa da história a consegu
b8 | simples | loc_campo | two | MAR | - | - | - | Acontece que a radiação foi destruindo a saúde dela. Em mil novecentos
b9 | simples | interior pedra | two | PES, JOR | - | crate, curie_box | - | Mas os cadernos dela continuam radioativos, guardados em caixas de chu
b10 | simples | interior pedra | close | PRO | - | curie_box | - | Para ler, é preciso assinar um termo e usar roupa de proteção.
b11 | simples | interior pedra | two | MAR | - | curie_box | - | Ou seja: os cadernos vão continuar radioativos por séculos.
b12 | simples | interior pedra | close | PES | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (11/13 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh curie1898
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh curie1898
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local curie1898 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

