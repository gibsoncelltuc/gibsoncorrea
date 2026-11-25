# CRONOGRAMA - Curiosidade e Ciência EP 19 - O Caderno que Ainda Brilha

Gerado em 25/11 16:45 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior pedra | two | PRO | - | curie_box | - | Existem cadernos tão perigosos que só se lê com roupa especial.
b1 | simples | interior pedra | close | PES | - | curie_box | - | E vão continuar perigosos por mais de mil anos.
b2 | chave | street | wide | POV | 6 | marco_eiffel | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em 1898, em Paris, Marie Curie trabalhava num galpão gelado.
b3 | simples | interior galpao | two | MAR, PIE | - | pechblenda | - | O teto pingava, e ela mexia minério com uma barra de ferro.
b4 | chave | interior galpao | wide | MAR, PIE | - | curie_box, pechblenda | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Assim ela e Pierre acharam dois elementos novos: polônio e rádio.
b5 | explicativa | interior galpao | two | sem personagem | - | curie_box | corpo: kit/curie_box (gira); emissao: brilho; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada en | O rádio brilhava no escuro, e ela adorava olhar os frascos.
b6 | simples | interior galpao | group | MAR, PIE | - | - | - | Ela carregava frascos no bolso. Ninguém sabia do perigo.
b7 | simples | street | low | MAR | - | - | - | Acontece que a radiação destruiu a saúde dela. Ela morreu em 1934.
b8 | simples | interior pedra | two | PRO | - | crate, curie_box | - | Hoje, os cadernos dela ficam em caixas de chumbo em Paris.
b9 | simples | interior pedra | wide | PRO | - | curie_box | - | Para ler, é preciso assinar um termo e vestir proteção.

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (12/14 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 0) | FEITO | 
5 | Voz | narracao neural gerada e tempos por palavra | FEITO | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | FEITO | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | FEITO | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | FEITO | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | PENDENTE | ./aprovar_storyboard.sh curie1898
10 | Render | todos os quadros renderizados nesta versao das folhas | REFAZER (a etapa anterior mudou) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | REFAZER (a etapa anterior mudou) | ./conferir.sh curie1898
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local curie1898 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | REFAZER (a etapa anterior mudou) | 

**Etapa atual:** 9. Revisao escrita e aprovacao

