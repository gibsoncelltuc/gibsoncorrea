# CRONOGRAMA - Curiosidade e Ciência EP 19 - O Caderno que Ainda Brilha

Gerado em 25/11 17:19 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | interior pedra | two | PRO | - | curie_box | - | Os cadernos de Marie Curie só podem ser lidos com proteção.
b1 | simples | interior pedra | close | PES | - | curie_box | - | E vão continuar radioativos por mais de mil anos.
b2 | chave | street | wide | POV | 6 | marco_eiffel | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Em Paris, ela trabalhava num galpão gelado com o marido Pierre.
b3 | simples | interior galpao | two | MAR, PIE | - | pechblenda | - | Mexia toneladas de minério com uma barra de ferro.
b4 | chave | interior galpao | wide | MAR, PIE | - | curie_box, pechblenda | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Assim descobriram dois elementos novos: polônio e rádio.
b5 | explicativa | interior galpao | two | sem personagem | - | curie_box | corpo: kit/curie_box (gira); emissao: brilho; luz: estudio; camera: 2 enquadramentos sem corte seco; som: som em cada en | O rádio brilhava no escuro, e ela adorava olhar.
b6 | simples | interior galpao | group | MAR, PIE | - | - | - | Ela andava com frascos no bolso, sem saber do perigo.
b7 | simples | street | low | MAR | - | - | - | Acontece que a radiação destruiu a saúde dela.
b8 | simples | interior pedra | two | PRO | - | crate, curie_box | - | Hoje, os cadernos dormem em caixas de chumbo em Paris.
b9 | simples | interior pedra | wide | PRO | - | curie_box | - | Quem quiser ler, precisa de autorização. É por isso que...

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
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | PENDENTE | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh curie1898
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh curie1898
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local curie1898 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 8. Storyboard e grade de acoes

