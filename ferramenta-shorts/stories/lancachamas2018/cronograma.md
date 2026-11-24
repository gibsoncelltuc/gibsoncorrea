# CRONOGRAMA - Poder e Fama EP 12 - O Não é um Lança-Chamas

Gerado em 24/11 17:33 | 10 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | MUS, CMP | - | marco_hollywood | - | No começo de dois mil e dezoito, nos Estados Unidos, a Boring Company,
b1 | simples | loc_patio | reveal | MUS, CMP | 8 | flamethrower | - | O nome dele era Não é um lança-chamas.
b2 | simples | loc_patio | two | MUS, CMP | - | flamethrower | - | O preço era de quinhentos dólares.
b3 | simples | loc_pista | two | CMP, MUS | - | flamethrower | - | O nome dizia que não era, mas o aparelho tinha cara de lança-chamas, e
b4 | simples | loc_pista | wide | MUS, CMP | 6 | extinguisher | - | Cada compra vinha com um extintor de incêndio de brinde.
b5 | simples | interior loja | group | MUS, CMP, POV | - | - | - | Foram vinte mil unidades à venda.
b6 | chave | loc_campo | crowd | CMP, MUS | 30 | marco_hollywood, picket_fence | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | E elas esgotaram em poucos dias, rendendo cerca de dez milhões de dóla
b7 | simples | loc_campo | group | CMP, MUS | 6 | globe, marco_hollywood | - | A notícia se espalhou pelo mundo inteiro.
b8 | simples | loc_pista | group | MUS, CMP | - | extinguisher, flamethrower | - | Um produto que se chamava de tudo, menos do que parecia.
b9 | simples | loc_cidade | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (3/4 itens) | FEITO | 
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | FEITO | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 4) | PENDENTE | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | REFAZER (a etapa anterior mudou) | 
6 | Estilo e enquadramento | autoajuste de luz/cor e ajuste de camera de cada tomada | BLOQUEADO (etapa anterior pendente) | 
7 | Gates | camera OK, todas as tomadas OK, estilo OK | BLOQUEADO (etapa anterior pendente) | 
8 | Storyboard e grade de acoes | video inteiro em quadros + 1 quadro no instante de cada acao | BLOQUEADO (etapa anterior pendente) | 
9 | Revisao escrita e aprovacao | uma linha por frase conferindo com a folha 3 e com o quadro da pesquisa | BLOQUEADO (etapa anterior pendente) | ./aprovar_storyboard.sh lancachamas2018
10 | Render | todos os quadros renderizados nesta versao das folhas | BLOQUEADO (etapa anterior pendente) | 
11 | Montagem e som | trechos + voz + musica + efeitos; volume normalizado | BLOQUEADO (etapa anterior pendente) | 
12 | Conferencia | conferir.sh sem falha e folha de contato olhada | BLOQUEADO (etapa anterior pendente) | ./conferir.sh lancachamas2018
13 | Auditoria das acoes | 1 quadro do mp4 em cada palavra de acao | BLOQUEADO (etapa anterior pendente) | bash auditar_acoes.sh local lancachamas2018 <mp4>
14 | Entrega | mp4 original 1080x1920 enviado; commit e push | BLOQUEADO (etapa anterior pendente) | 

**Etapa atual:** 4. Travas do roteiro

