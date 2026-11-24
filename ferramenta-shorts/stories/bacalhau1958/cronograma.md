# CRONOGRAMA - Guerras Inusitadas EP 25 - As Guerras do Bacalhau

Gerado em 24/11 10:24 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | harbor | two | ICE, BRI | - | cod, ship | - | Entre mil novecentos e cinquenta e oito e mil novecentos e setenta e s
b1 | simples | harbor | group | ICE, PES | - | crate, cod | - | A Islândia é pequena, e vivia da pesca. Mas barcos ingleses pescavam b
b2 | transicao | harbor | wide | ICE | - | ship | - | Então a Islândia aumentou os limites do seu mar: doze milhas, cinquent
b3 | simples | harbor | group | BRI, BRI, PES | - | ship | - | A Inglaterra mandou a marinha para proteger os barcos de pesca.
b4 | simples | harbor | close | ICE | - | - | - | A Islândia só tinha uns barquinhos da guarda costeira, mas eles tinham
b5 | simples | harbor | wide | ICE | - | navios de guerra ao fundo, no tamanho real, ship | - | Eles cortavam os cabos das redes inglesas, e os navios batiam um no ou
b6 | chave | harbor | orbit | ICE, BRI | - | - | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | A Islândia ainda ameaçou fechar a base da Otan no país.
b7 | simples | harbor | two | BRI, ICE | - | - | - | Em mil novecentos e setenta e seis, os ingleses cederam, e a ideia de 
b8 | simples | harbor | close | PES | - | crate, cod | - | Foi uma guerra de navios batendo e de redes cortadas, e tudo por causa
b9 | simples | harbor | two | ICE | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/5 itens) | PENDENTE | python3 pesquisar.py bacalhau1958
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 7) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
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

**Etapa atual:** 2. Pesquisa de campo

