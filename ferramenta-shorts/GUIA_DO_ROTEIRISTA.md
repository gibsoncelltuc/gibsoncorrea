# GUIA DO ROTEIRISTA — como escrever um vídeo para a ferramenta (para qualquer modelo de IA)
Você só precisa criar `videos/<id>/beats.json` e rodar a fila. NÃO edite o motor (`web/`, `mkvideo.py`) para fazer um vídeo.

## Passo a passo
1. Escreva o roteiro seguindo `MODO_RICKS.md` §1 (gancho sem data, 150–200 palavras, 1–2 falas entre aspas, virada "Acontece que...", final curto e irônico).
2. Crie `videos/<id>/beats.json` (modelo abaixo; copie `videos/emus1932/beats.json` ou `videos/teste_cenarios/beats.json`).
3. `python3 roteiro_check.py <id>` e corrija os avisos.
4. Prévia rápida (2 min): `python3 mkvideo.py <id> && ./produce_voice.sh <id> pt-BR-AntonioNeural +10% && ./build3.sh <id> && ./fit.sh <id> && node storyboard.mjs <id> sb_<id>.jpg 270 && python3 sbsheet.py sb_<id>.json sb_<id>.jpg` → abra `sb_<id>.jpg` e confira cada plano. (Nunca rode isso com a fila rodando.)
5. Ponha o id em `queue.txt` e rode `bash run_queue.sh` (~15–20 min por vídeo; `bash status.sh` mostra o andamento; retoma sozinho se a sessão reiniciar).
6. Abra `out/<id>/review_sheet.jpg` antes de entregar. Se o gate reprovar 2 vezes o vídeo é pulado: leia `logs/gate_<id>.txt`, ajuste a cena (personagem escondido atrás de objeto = mude a posição do objeto) e apague `stories/<id>/SKIP` e `stories/<id>/fails`.

## beats.json
```json
{"title": "Titulo", "voice": "pt-BR-AntonioNeural", "rate": "+10%", "set": "street", "light": "day", "mood": "playful",
 "outfits": {"CID": {"jacket": "#3b6fb5", "pants": "#2d3550", "boots": "#2a2218", "hat": "hair", "hair": "#4a3020"}},
 "beats": [{"say": "Frase narrada.", "shot": "two", "who": ["CID:0:smile", "CID:1:nervous"]}]}
```
Cada beat = uma frase (ou duas curtas). Campos do beat:
| Campo | Valores |
|---|---|
| `say` | texto narrado. Fala de personagem entre aspas "..." → o 2º personagem da cena mexe a boca |
| `shot` | `two` (2 personagens, padrão), `close`, `group` (3–5), `low`, `track` (andando), `prop` (objeto), `wide`/`crowd`/`orbit`/`reveal` (abertos). O diretor automático ajusta; `"shot_lock": true` fixa o seu |
| `who` | lista "FIGURINO:variante:expressão". Variantes 0–3 = padrão; 4 = óculos; 5 e 6 = barba |
| `set` | cenário SÓ desta cena (o do topo vale para as outras): arctic, countryside, hall, harbor, jungle, medieval, mountain, outback, palace, stadium, street |
| `light` | arctic, dawn, day, deck, desert, dusk, golden, grave, night, noon, overcast, storm, study, tense. Sem `light`, palavras como "noite"/"amanhecer" escolhem sozinhas |
| `mood` | música: playful |
| `text`, `tat`, `tstyle` | texto grande na cena, palavra em que aparece, estilo (red, gold...) |
| `props` | objetos: [["asset", x, z, escala], ...] (lista de assets abaixo) |
| `animals` | [["bear"|"horse"|"emu"..., x, z, "stand"]] ; bando de emus: `"emus": {"n": 10, "mode": "stand|run|scatter"}` |
| `crowd` | {"n": 12, "outfit": "AUS", "march": true} (o diretor já põe tropa quando a frase fala de exército) |
| `veiculo` | veículo andando: {"asset": "vehicles/car", "de": -7, "para": 7, "z": 1.2, "motorista": "CID:0:smile"} |
| `fx`, `sfx` | efeitos "burst@4", "dust@10", "puff", "stars", "ring"; sons "gun@8", "cannon@4" (nome@quadro). Sons: Wf, birds, cannon, creak, ding, drone, gulls, gun, harp, heartbeat, march, paper, playful, sea, snuffle, squeal, steps, sting, thump, tick, whoosh |
| `impact` | `false` impede que a cena vire plano aberto de impacto |
Figurino (`outfits`): `jacket`, `pants`, `boots`, `hat` (shako, shako_tall, cap, hair, tophat, bonnet), `cap`/`hair` (cor), `belt`, `buttons`, `sash`, `rifle: true`, `build: "stout"`, `moustache_on` (cor), `beard` (cor), `glasses: true`.
Expressões: dazed, grin, laugh, lick, nervous, neutral, pained, relief, relief_open, shock, smile, smile_closed, stern, whistle.

## Objetos 3D prontos (campo `props`)
- `vehicles/…`: car, taxi, car_blue, jeep, truck, tank, motorcycle, bicycle, airplane, helicopter, sailboat, motorboat, locomotive, wagon
- `buildings/…`: house_small, house_two, house_blue, apartment, skyscraper, church, barn, windmill, lighthouse, castle_tower, shop, bridge
- `nature/…`: tree_oak, tree_pine, tree_birch, tree_palm, bush, flowerbed, bench, fountain, lamppost, haybale, rocks, picket_fence, scarecrow
- `tools/…`: hammer, axe, shovel, pitchfork, rake, saw, bucket, wheelbarrow, ladder, anvil, lantern, broom, scythe, telescope
- `war/…`: musket, pistol, sword, shield, helmet_army, helmet_knight, drum, bugle, sandbags, bow, quiver, flagpole, cannonballs, bunker
- `mk/…` (94 objetos de interior/medieval): Anvil, Anvil_Log, Axe_Bronze, Bag, Banner_1, Banner_1_Cloth, Banner_2, Banner_2_Cloth, Barrel, Barrel_Apples, Barrel_Holder, Bed_Twin1, Bed_Twin2, Bench, BookGroup_Medium_1, BookGroup_Medium_2, BookGroup_Medium_3, BookGroup_Small_1, BookGroup_Small_2, BookGroup_Small_3, BookStand, Book_5, Book_7, Book_Simplified_Single, Book_Stack_1, Book_Stack_2, Bookcase_2, Bottle_1, Bucket_Metal, Bucket_Wooden_1, Cabinet, Cage_Small, CandleStick, CandleStick_Stand, CandleStick_Triple, Candle_1, Candle_2, Carrot, Cauldron, Chain_Coil, Chair_1, Chalice, Chandelier, Chest_Wood, Coin, Coin_Pile, Coin_Pile_2, Crate_Metal, Crate_Wooden, Dummy, FarmCrate_Apple, FarmCrate_Carrot, FarmCrate_Empty, Key_Gold, Key_Metal, Lantern_Wall, Mug, Nightstand_Shelf, Peg_Rack, Pickaxe_Bronze, Pot_1, Pot_1_Lid, Potion_1, Potion_2, Potion_4, Pouch_Large, Rope_1, Rope_2, Rope_3, Scroll_1, Scroll_2, Shelf_Arch, Shelf_Simple, Shelf_Small_Bottles, Shield_Wooden, SmallBottle, SmallBottles_1, Stall_Cart_Empty, Stall_Empty, Stool, Sword_Bronze, Table_Fork, Table_Knife, Table_Large, Table_Plate, Table_Spoon, Torch_Metal, Vase_2, Vase_4, Vase_Rubble_Medium, WeaponStand, Whetstone, Workbench, Workbench_Drawers
- raiz: barrel, boat, cabin, cannon, crate, fence, mgun, potato, ship, tent
- animais 3D (`animals`): bear, horse, emu ; modelos extras em `web/assets/animals/`: bear, cat, cow, deer, dog, donkey, elephant, fox, goat, horse, lion, pig, rabbit, sheep, wolf
Objeto novo: modele no Blender por script (`blender -b --python blender/<nome>.py`, exemplo `blender/make_emu.py`) e exporte .glb para `web/assets/`. Nós com nome `body`, `head`, `legL`, `legR`, `wheel*`, `propeller` são animados pelo motor.

## Regras automáticas do diretor (não precisa pedir)
Personagens grandes na maior parte do vídeo; até 2 planos abertos comuns + até 2 planos de impacto nos momentos-chave (tiro/ataque/fuga) com tropa e clarões; exército chegando = 18 marchando; legenda de 1–2 palavras a 70% da altura; câmera sempre em leve movimento; luz pela história.

## Interior e fachada (cenas dentro de casa)
- `"interior": "madeira"` | `"pedra"` | `"loja"` no beat: a cena passa dentro de uma sala (parede perto, janela, porta, quadros, piso com juntas; a loja tem balcão e prateleiras). A luz vira `study` sozinha e os móveis padrão entram (estante, mesa, cadeira, baú). Para trocar os móveis: `"moveis": [["mk/Table_Large", -6.6, -1.6, 2.2], ...]` (asset, dx, z, escala).
- Ao ar livre, em plano médio, o diretor põe sozinho uma construção atrás dos personagens (campo, deserto, rua, medieval, porto). Para tirar: `"fachada": false`.
- Use interior sempre que a narração falar de sala, escritório, palácio, loja, quartel, tribunal, casa. No canal, a maioria das cenas de conversa é com parede perto.

## Personagens: chapéus, cabelos e objetos na mão
- Chapéus (`"hat"` no figurino): `shako`, `shako_tall`, `cap`, `tophat`, `bonnet`, `helmet` (capacete), `bowler` (coco), `straw` (palha), `slouch` (australiano/aba larga), `fez`, `turban`, `crown` (coroa), `beret` (boina), `wizard`. Cor com `"cap": "#rrggbb"`.
- Chapéu diferente por pessoa: `"hats": ["straw", "cap", "bowler"]` (a variante escolhe). Sem `hat` nem `hats`, cada variante ganha cor e corte de cabelo próprios (curto, longo, coque).
- Objeto na mão: 4º campo do `who` → `"HUS:0:laugh:mug"`. Opções: `bottle`, `mug`, `paper`, `book`, `lantern`, `pitchfork`, `staff`, `flag`, `torch`, `bag`, `coin`, `spyglass`. Use o objeto da história (quem bebe segura caneca, jornalista segura papel).

## Texto na cena
- `"text"` agora vira **placa de madeira fincada atrás dos personagens** (como no canal). Em plano aberto, na última cena ou com texto longo (>14 letras) vira título flutuante. Para forçar título: `"titulo": true`.

## Conferir contra o canal
- `python3 comparar.py <id>` gera `out/comparativo_<id>.jpg` (canal em cima, nosso embaixo) e a tabela de medidas (luz, contraste, saturação, escuros, nitidez, ruído).

## O que a ferramenta faz sozinha a partir do texto (não precisa pedir)
- **Hora do dia**: "noite", "madrugada" → noite azul; "amanhecer" → amanhecer; "pôr do sol", "fim de tarde" → sol baixo; "à tarde" → luz dourada; "dias depois", "no dia seguinte" → volta o dia. Vale até o texto mudar. Para forçar: `"hora": "dia|tarde|pordosol|noite|amanhecer"`.
- **Clima**: "chuva", "tempestade", "neve/inverno", "neblina", "calor/sol escaldante", "ventania" → chuva, neve (a cena vai para o cenário nevado), névoa, luz de deserto, vento com folhas. Para forçar: `"clima": "chuva|tempestade|neve|neblina|calor|vento|limpo"`.
- **Pássaros no céu** em cena externa de dia (tirar: `"passaros": false`).
- **Objeto na mão** do primeiro personagem quando o texto fala de bebida, carta/jornal, livro, lanterna, tocha, bandeira, dinheiro, saco, luneta. Ele usa o objeto (bebe, lê, olha pela luneta). Tirar: `"maos": false`.
- **Rosto próprio** para cada personagem (olhos, sobrancelha, bochecha, sardas, pinta), igual em todas as cenas.
- **Caminhada**: quem atravessa a tela (`"shot": "track"` ou `"move"`) anda de perfil com passada completa; soldado (figurino com `rifle`) marcha, civil caminha solto.
- **Tropa e batalha**: palavras de exército/tropa chegando criam a multidão uniformizada; tiro/batalha/pânico criam o plano aberto de impacto com clarões e som.

## Regras fixas de câmera (a ferramenta aplica sozinha)
- **Todo vídeo tem no mínimo 2 planos abertos de câmera contínua** (a câmera abre ou gira numa tomada só, mostrando o cenário, a tropa, a batalha). Se o roteiro não tiver, o diretor converte duas cenas. Mudar o mínimo: `"min_wide": 3` no topo do beats.json.
- **Batalha**: `"batalha": true` na cena força o plano aberto com a tropa atirando (clarões e som) e o inimigo/animais se espalhando. `"caminhoes": 2` põe caminhões com soldados em pé na carroceria.
- **Mapa didático**: na primeira vez que o texto cita um país ou cidade conhecidos, a ferramenta corta para um mapa de pergaminho com alfinete e o nome (~1,8 s). Forçar: `"mapa": "AUSTRÁLIA"`; desligar no vídeo: `"mapas": false`.
- **Variedade de planos**: use no roteiro `two` (dois personagens), `close` (rosto, na palavra-chave/emoção), `group`, `low` (câmera baixa), `track` (acompanha quem anda), `wide`/`crowd`/`reveal`/`orbit` (abertos). O diretor abre e fecha em plano médio e nunca põe dois abertos sem batalha em sequência.

## Refazer só algumas cenas (2–5 min em vez de 20)
- Vídeo já renderizado e você quer melhorar uma cena (câmera, personagens, objetos, batalha, placa)? Edite a cena no `beats.json` e rode `./refazer.sh <id> b4 b8` (os números das cenas, contando de b0). Só os trechos dessas cenas são renderizados de novo e o vídeo é remontado.
- Só vale se o **texto falado não mudou**. Se mudou a narração, o tempo de tudo muda e o vídeo inteiro precisa ser refeito pela fila.
- Não rode com a fila rodando.

## Plano de ação (obrigatório antes de renderizar)
- Toda vez que roda, o `mkvideo.py` lê o roteiro, separa as palavras-chave e os momentos de impacto e grava `stories/<id>/plano.md`: por cena, o plano de câmera, o que aparece (tropa, batalha, placa, mapa, objeto na mão) e cada palavra-chave com o **efeito visual + o som** que ela dispara.
- A última coluna lista **palavras de ação sem efeito**. Não renderize com essa coluna preenchida: ou a palavra entra na lista automática, ou você põe na cena um `"fx"`, `"sfx"`, objeto na mão (4º campo do `who`), `"batalha": true`, animal, veículo.
- Sons disponíveis em `"sfx": ["gun@40"]` (nome@quadro dentro da cena): `gun`, `cannon`, `sting`, `thump`, `ding`, `whoosh`, `squeal`, `tick`, `steps`.

## Detalhe de objeto e mistura de planos
- **Detalhe de objeto**: numa cena de 11+ palavras que tenha um objeto em `"props"` ou uma placa (`"text"`), a câmera desliza até o objeto no meio da cena e volta (até 3 por vídeo). Desligar na cena: `"detalhe": false`. Use para o objeto que carrega a história (o balde, o barril, a carta).
- **Mistura de planos**: ao rodar `mkvideo.py` sai a linha `mistura de planos: close X% | medio Y% | aberto Z% | detalhe W%` com AVISO quando foge do padrão do canal (close 10% | médio+corpo 67% | aberto 19% | detalhe 5–15%). Também fica no fim do `stories/<id>/plano.md`. Corrija o roteiro antes de renderizar se houver AVISO.

## Séries com episódio numerado
- No topo do `beats.json`: `"serie": "Guerras Inusitadas", "ep": 6`. O título e o nome do arquivo saem como `Guerras Inusitadas EP 06 - <título>`. Numere na ordem de publicação; a série atual vai até o EP 05 (Karánsebes, Emus, Toledo, Balde, Gansos).

## Corrigir sem perguntar (regra fixa)
- Conferiu a folha de contato e viu defeito? Corrija na hora e mande refazer só a cena: `echo "<id> b3 b7" >> refazer.txt` (a fila refaz antes do próximo vídeo) ou `./refazer.sh <id> b3 b7` com a fila parada. `bash status.sh` mostra as correções pendentes. Para o Gibson vai só o relatório do que passou, do que não passou e do que já foi refeito.

## Pré-produção (antes de animar)

`python3 mkvideo.py <id>` grava `stories/<id>/preproducao.md`: uma linha por cena com cenário, plano, número de personagens, ação dos personagens, objetos em cena, objeto na mão e o que **falta**. Leia antes de renderizar.

- **Objetos automáticos**: o que a narração cita e existe na biblioteca entra na cena sozinho (bolo/doce → mesa de bolos, trono, fogueira, tenda, baú, barraca de feira, barril, canhão, bandeira, tambor, tulipa, cova, torre, igreja, moinho...). Lista em `OBJ_DICT` no `mkvideo.py`. Desligar numa cena: `"objetos": false`.
- **Falta modelar**: palavra do roteiro sem modelo 3D aparece em "FALTA MODELAR". Modele no Blender (copie um bloco de `blender/make_objetos.py`, rode `blender -b --python blender/make_objetos.py`) e acrescente uma linha no `OBJ_DICT`.
- **Porto/navio**: cena pequena que fala de navio, porto, marinha vai sozinha para o cenário `harbor` (cais com navio); em plano aberto de cenário com mar entram navios ao fundo. Desligar: `"porto_cenario": false` no topo.
- **Ação dos personagens** (ninguém fica só piscando):
  - fala entre aspas ou cena sem ação marcada → `conversar` (gesticula de leve);
  - "discutiu, gritou, exigiu, ameaçou" → `discutir`; "riu, comemorou, venceu, festa" → `comemorar`; "dançou" → `dancar`;
  - expressão `shock`/`nervous` → `reagir` (susto, mãos no rosto);
  - "chegou, entrou, apareceu, veio, correu para" → o último personagem do `who` **entra andando** na cena (`"chega": true/false` força);
  - forçar: `"acao": "conversar|discutir|comemorar|dancar|nenhuma"`.
- Teste de storyboard sem atrapalhar a fila: copie `web/*.js` para uma pasta de rascunho com links para o resto e rode `build3.sh`/`fit.sh`/`storyboard.mjs` lá (nunca na pasta da fila).

## Objeto herói, interação e grandes momentos

- **Objeto herói**: o objeto-tema do vídeo. A ferramenta acha pelo título ou pelo mais citado; para fixar, ponha `"heroi": "kit/tulip_red"` no topo (`"heroi": null` desliga). Ele entra sozinho na primeira e na última cena e ganha close de câmera garantido.
- **Interação física** (`"interacao"` na cena, ou automática pelo texto): `empurrar`, `discutir`, `cochichar`, `entregar`, `susto`, `reverencia`, `pular`. Sem pista no texto, a ferramenta roda uma lista (aproxima-se, avança e o outro recua, insiste...) sem repetir dentro do vídeo e começando num ponto diferente em cada vídeo. `"interacao": false` desliga na cena.
- **Dois grandes momentos**: se o roteiro render só um plano de impacto, a virada ("Acontece que") vira o segundo, com multidão, efeito e som. `"min_momentos"` no topo muda o mínimo.
- O fim de `preproducao.md` resume: objeto herói (cenas e closes), grandes momentos e interações por cena. Qualquer "AVISO" ali se resolve antes de renderizar.
