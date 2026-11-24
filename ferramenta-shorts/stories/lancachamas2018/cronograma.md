# CRONOGRAMA - Poder e Fama EP 12 - O Não é um Lança-Chamas

Gerado em 24/11 22:43 | 11 cenas | metricas: acoes_encenadas 100%, acoes_chave_com_efeito 100%, explicacoes_cobertas 100%, cenario_e_epoca_ok 100%

## 1. Plano de cenas (o que cada frase vai mostrar)

Cena | Classe | Cenario | Camera | Quem | Multidao | Objetos | Efeito planejado | Frase
---|---|---|---|---|---|---|---|---
b0 | simples | loc_cidade | two | MUS, POV | - | flamethrower, marco_hollywood | - | Um bilionário vendeu um lança-chamas e jurou que não era um lança-cham
b1 | simples | interior pedra | two | MUS, CMP | - | - | - | Foi em dois mil e dezoito, nos Estados Unidos. A Boring Company, a emp
b2 | simples | interior loja | two | MUS, CMP | - | flamethrower | - | O nome dele era Não é um lança-chamas, e custava quinhentos dólares.
b3 | chave | loc_deserto | wide | MUS | 18 | fire, flamethrower, marco_hollywood | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Acontece que o aparelho soltava fogo de verdade, e essa era a piada.
b4 | simples | interior pedra | two | MUS, CMP | - | flamethrower | - | Musk explicou que o nome era para driblar a alfândega, que barrava lan
b5 | simples | interior loja | two | CMP, POV | - | extinguisher | - | Cada compra vinha com um extintor de incêndio de brinde.
b6 | chave | loc_cidade | crowd | POV, POV | 16 | marco_hollywood | corpo: tropa/personagens encenam a batalha; emissao: claroes de tiro, fumaca e poeira; luz: clarao; camera: 4 cameras em | Foram vinte mil unidades à venda, e elas esgotaram em poucos dias.
b7 | simples | interior pedra | two | MUS, CMP | - | picket_fence | - | Isso rendeu cerca de dez milhões de dólares para a empresa.
b8 | chave | loc_deserto | two | MUS | - | fire, flamethrower | corpo: labaredas 3D; emissao: fumaca; luz: clarao do fogo; camera: plano da cena; som: fogo | O próprio Musk postou vídeos soltando fogo com o aparelho.
b9 | simples | loc_cidade | two | MUS, POV | - | extinguisher, flamethrower | - | Um produto que se chamava de tudo, menos do que parecia.
b10 | simples | loc_cidade | close | MUS | - | - | - | Agora não deixe de comentar: qual deve ser o tema do próximo vídeo?

## 2. Etapas (em ordem; nenhuma comeca com a anterior pendente)

N | Etapa | O que confere | Estado | Proximo passo
---|---|---|---|---
1 | Roteiro e 4 folhas | folha 1 (roteiro), 2 (producao), 3 (acao) e 4 (pesquisa) geradas; triagem de cada frase | FEITO | 
2 | Pesquisa de campo | cada item do raio-X com referencia; quadro de prints olhado (0/10 itens) | PENDENTE | python3 pesquisar.py lancachamas2018
3 | Modelagem do que falta | todo objeto das cenas existe na biblioteca 3D, da epoca e no tamanho real | REFAZER (a etapa anterior mudou) | 
4 | Travas do roteiro | folha 2 com 0 risco e folha 3 com 0 acao faltando (riscos agora: 1) | BLOQUEADO (etapa anterior pendente) | corrigir o roteiro conforme a folha 2
5 | Voz | narracao neural gerada e tempos por palavra | BLOQUEADO (etapa anterior pendente) | 
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

