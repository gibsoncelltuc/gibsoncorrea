# A / trumpgame1989 - defeito de FERRAMENTA (pesquisar.py)
O print do objeto kit/boardgame vem de buscar "boardgame" sozinho e traz paisagens do Brasil (cachoeiras, cidade); "visual.buscas" por chave 'boardgame'/'kit/boardgame'/'tabuleiro' nao muda o resultado (itens 'sem referencia': "O Jogo de Tabuleiro do Trump", "familias jogando"). Ja marquei os prints em prints_ruins.txt. Pedido: a busca do objeto deve usar o termo do roteiro ("Trump The Game 1989 board game") e respeitar visual.buscas na chave do OBJETO (kit/x).

# Sugestao de modelo (A, 25/11): kit/phone e' um totem de tela em suporte, nao um celular de mao. Aparece em bitcoin2021 (app fora do ar), xplaca2023 e bateria2017 (resposta escrita no celular). Pedido: modelar celular de mao (retangulo fino, tela acesa) e trocar o asset.

# Defeito (A, 25/11): prechecar.sh acoes quebra com "ValueError: cannot write empty image" quando a folha 3 nao tem NENHUMA linha de acao com tempo (leitura toda 'mostra', como em xplaca2023). Pedido: a grade de acoes deve ser pulada (ou gerar imagem vazia) quando acoes_frames.txt estiver vazio. Contorno: coloquei 3 passos com verbo real (pega/grita/fala + forcar).
