# CRONOGRAMA - Guerras Inusitadas EP 25 - As Guerras do Bacalhau

Gerado em 24/11 23:26 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | chave | harbor | two | sem personagem | - | barco_guarda, fishing_net, navio_leander, navio_vapor | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Islândia derrotou a marinha inglesa com um cortador de rede.
b1 | simples | harbor | wide | ICE, BRI | - | cod, navio_leander | - | Entre mil novecentos e cinquenta e oito e setenta e seis, os dois país
b2 | simples | harbor | two | ICE, PES | - | crate, cod | - | A Islândia vivia da pesca, mas barcos ingleses pescavam bacalhau perti
b3 | transicao | harbor | wide | ICE | - | navio_leander | - | Então ela ampliou os limites do mar: doze milhas, cinquenta, e por fim
b4 | chave | harbor | group | sem personagem | - | navio_leander | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A marinha mandou fragatas para proteger os barcos de pesca.
b5 | chave | harbor | group | sem personagem | - | barco_guarda, fishing_net, navio_vapor | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que a Islândia só tinha barquinhos da guarda costeira, mas el
b6 | transicao | harbor | wide | sem personagem | - | barco_guarda, fishing_net, navio_leander, navio_vapor, navios de guerra ao fundo, no tamanho real | - | Eles cortavam os cabos das redes, e os navios batiam um no outro, de p
b7 | chave | harbor | two | ICE, BRI | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Islândia ameaçou fechar a base da Otan e rompeu relações com a Ingla
b8 | simples | harbor | group | BRI, ICE | - | scroll | - | Em mil novecentos e setenta e seis, a Inglaterra cedeu, e a zona de du
b9 | simples | harbor | close | PES | - | crate, cod | - | Uma guerra inteira, por causa de um bacalhau.
b10 | simples | harbor | two | ICE | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/17 itens) | PENDENTE | python3 pesquisar.py bacalhau1958
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | BLOQUEADO (etapa anterior pendente) | modelar em blender/ (formas.py): kit/barco_guarda, kit/navio_leander
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh bacalhau1958
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh bacalhau1958
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local bacalhau1958 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 14. Entrega

