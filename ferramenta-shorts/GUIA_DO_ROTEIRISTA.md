# GUIA DO ROTEIRISTA — como escrever um vídeo para a ferramenta (para qualquer modelo de IA)
Você só precisa criar `videos/<id>/beats.json` e rodar a fila. NÃO edite o motor (`web/`, `mkvideo.py`) para fazer um vídeo.

## Passo a passo
1. Escreva o roteiro seguindo `MODO_RICKS.md` §1 (gancho sem data, 150–200 palavras, 1–2 falas entre aspas, virada "Acontece que...", final curto e irônico).
2. Crie `videos/<id>/beats.json` (modelo abaixo; copie `videos/emus1932/beats.json` ou `videos/teste_cenarios/beats.json`).
3. `python3 roteiro_check.py <id>` e corrija os avisos.
4. Prévia rápida (2 min): `python3 mkvideo.py <id> && ./produce_voice.sh <id> pt-BR-AntonioNeural +10% && ./build3.sh <id> && ./fit.sh <id> && node storyboard.mjs <id> sb_<id>.jpg 270 && python3 sbsheet.py sb_<id>.json sb_<id>.jpg` → abra `sb_<id>.jpg` e confira cada plano. (Nunca rode isso com a fila rodando.)
5. Ponha o id em `queue.txt` e rode `bash run_queue.sh` (~15–20 min por vídeo; `bash status.sh` mostra o andamento; retoma sozinho se a sessão reiniciar).
6. Abra `out/<id>/review_sheet.jpg` antes de entregar. Se o gate reprovar 2 vezes o vídeo é pulado: leia `logs/gate_<id>.txt`, ajuste a cena (personagem escondido atrás de objeto = mude a posição do objeto) e apague `stories/<id>/SKIP` e `stories/<id>/fails`.

## Pesquisa visual (OBRIGATORIA desde 23/11 - sem ela o video nao renderiza)
Antes de escrever, alem da fonte da HISTORIA, pesquise a FONTE VISUAL (fotos, quadros, gravuras, videos, museus) e preencha no topo do beats.json:
```json
"visual": {
  "local": "SpaceX, McGregor (Texas): campo de testes a ceu aberto, chao de terra/concreto",
  "quando": "15/out/2026, a noite",
  "participantes": ["Elon Musk (camiseta escura)", "engenheiros da Tesla", "convidados"],
  "roupas": {"MUS": "camiseta cinza-escura, calca jeans", "ENG": "camisa azul da equipe"},
  "cenario": "rampa curva gigante (estilo Hot Wheels), torres de refletor, plateia; galpao iluminado",
  "objetos": ["Roadster branco (cunha)", "propulsores com fumaca branca"],
  "fontes_visuais": ["https://...foto1", "https://...video"]
}
```
Depois AJUSTE o roteiro a ela: figurino de cada personagem (cor, chapeu, uniforme da epoca), "set"/"interior"/"hora" de cada cena, objetos em "props" (modele no Blender o que faltar: o cenario real, o veiculo real, o utensilio da epoca). Fato que a pesquisa contradiz sai da narracao.
No fim de todo video a ferramenta poe sozinha a chamada: "Agora nao deixe de comentar: qual deve ser o tema do proximo video?" ("cta_texto" troca a frase; "cta": false desliga).

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

## As duas folhas (obrigatório em todo vídeo)

1. Escreva `videos/<id>/beats.json` e rode `python3 mkvideo.py <id>`.
2. **Folha 1** `stories/<id>/folha1_roteiro.md`: a história cena a cena (narração, duração, som ambiente, efeitos sonoros, efeito nas palavras-chave, texto/mapa na tela, função da cena: gancho, virada, grande momento, fecho).
3. **Folha 2** `stories/<id>/folha2_producao.md`: as coordenadas de produção cena a cena (cenário, luz, clima, câmera, personagens, animação e interação, objetos/modelos) e os **RISCOS** com a **CORREÇÃO** pronta para copiar no roteiro. No fim: resumo dos riscos e como reparar depois do render.
4. A última linha do mkvideo diz quantos riscos estão em aberto. Corrija o roteiro e rode de novo até dar **0**. Risco que você viu e aceita: `"riscos_ok": true` na cena.

Riscos que a ferramenta acusa: chegada/travessia pela água em plano fechado; água citada em cenário sem água; animal sem modelo ou fora de cena (existem: porco, galinha/ganso, emu); ação sem animação (nadar, cavalgar, escalar, sentar...); cena longa (>26 palavras) ou curta (<6); mais de 4 personagens em plano fechado; multidão em interior; veículo citado e ausente; 3 cenas seguidas iguais; objeto sem modelo; personagens parados; vídeo sem mapa, sem objeto herói, com menos de 2 grandes momentos ou com palavra de ação sem efeito.

O que a ferramenta **sabe** animar (escreva o roteiro com isto): andar, chegar andando, marchar, conversar, discutir, empurrar, cochichar, entregar, levar susto, comemorar, dançar, reverência, segurar e usar objeto, atirar, batalha com tropa, fugir, animais fugindo, soldados subindo em caminhão, veículo passando.

## v13 (24/11) — Cena de explicação, objeto como sujeito, locação limpa e época

**1. Cena de explicação (sem personagem).** Frase que explica ciência/mecanismo (propulsão, pressão, "funciona", "o segredo é", "de zero a cem"...) é classificada como EXPLICATIVA e **trava o render** se a cena não tiver `"explica"`. A cena fica só com o objeto num estúdio escuro, o mecanismo funcionando e rótulos de 1 a 3 palavras, tudo entrando na palavra da narração:

```json
{"say": "O segredo são propulsores de ar comprimido escondidos embaixo do carro, que empurram ele para cima.",
 "explica": {"objeto": "kit/roadster26", "raiox": "escondidos",
   "pecas": [["kit/tanque_ar", -0.9, 0.42, 0, 0.55, {"rz": 1.5708}]],
   "vfx": [{"k": "jato", "na": "empurram"}],
   "rotulos": [["PROPULSORES", "baixo", "propulsores"], ["AR COMPRIMIDO", "topo", "comprimido"]],
   "setas": [["cima", "EMPUXO", "", "cima"]]}}
```

- `objeto`: modelo 3D (padrão: o herói). `manobra`: `paira` | `parado` | `gira` | `sobe`. `raiox`: `true` ou a palavra em que o objeto fica translúcido; `pecas`: o que aparece dentro (`[asset, dx, dy, dz, escala, {"rz", "rx", "cor"}]`, em metros do modelo).
- `vfx`: `jato` (propulsor: sai de baixo, bate no chão e se espalha), `pneu`, `poeira`, `fogo`, `faisca`, `vapor`, `velocidade`, `onda`, `brilho`. `na` = palavra em que começa; `ate` = palavra ou fração (0 a 1) em que acaba; `pot` = força; `pts` = `baixo4` | `centro` | `topo` | `meio`.
- `rotulos`: `[TEXTO, ponto, palavra, lado]` — ponto: `topo`, `baixo`, `meio`, `frente`, `tras`, `roda`, `capo`. `setas`: `[direcao, TEXTO, cor, palavra, ponto]` — direção `cima` | `baixo` | `esq` | `dir`.
- Gráficos (parte de cima da tela, longe da legenda): `"medidor": {"de": 0, "para": 100, "un": "km/h", "titulo": "ZERO A CEM", "na": "zero", "dur": 0.9}`, `"contador"` (igual, só o número), `"passos": ["TANQUE", "VÁLVULA", "JATO"]`, `"comparar": [["CARRO COMUM", 3, "s"], ["ROADSTER", 1, "s"]]`.
- Só um número em cima de uma cena **com** personagens: `"hud": {"contador": {...}}` no beat. Frase que não é explicação de verdade: `"explica": false`.
- Peças prontas: `kit/tanque_ar`, `kit/bocal_propulsor`. Se o objeto explicado não existe, modele (`blender/formas.py`).

**2. O objeto é o sujeito.** "O carro decolou / voou / pulou / desceu / pousou / acelerou" com o veículo em `props`: a cena passa a ser dele — câmera aberta nele e seguindo, quem assiste fica de lado (no máximo 2), sem multidão na frente, e o efeito sai **do objeto** (jato embaixo, onda de ar no chão, poeira, fumaça de pneu, riscos de velocidade), com som próprio (`jato`, `motor_ev`, `pneu`, `pouso`, `espanto`). `"altura"` no 5º campo do prop muda a altura do voo (padrão 5,2 m). `"obj_acao": false` desliga.

**3. Locação limpa.** Os cenários antigos são temáticos (`outback` = fazenda com celeiro e moinho; `mountain` = front de guerra; `countryside` = vila rural...). Eles só entram se a narração ou a pesquisa visual falarem daquele tema; senão a ferramenta troca sozinha por uma locação limpa (só chão + horizonte): `loc_pista` (asfalto de pista de teste/evento), `loc_patio` (pátio industrial moderno), `loc_cidade` (cidade atual), `loc_deserto`, `loc_campo`, `loc_montanha`, `loc_estudio` (explicação). Use direto em `"set"`. Para fixar os lugares do vídeo: `"visual": {"locacoes": ["loc_pista", "interior galpao", "loc_cidade"]}`. Itens reais do lugar: `"locacao": {"loc_pista": {"itens": [["kit/telao_led", 0, -16, 1.2]], "horizonte": "cidade", "chao": "#3a3d45"}}`. `"set_tematico_ok": true` libera o cenário temático.

**4. Época.** A ferramenta troca sozinha o que ela mesma poria fora de época (barril, caixote, lampião, castiçal, canhão antigo) e **bloqueia** o render se sobrar objeto de outra época (lista em `referencias/<id>/FICHA.md`). Exceção consciente: `"epoca_ok": ["<asset>"]`. Kit moderno: `kit/cone_transito`, `kit/barreira_jersey`, `kit/palete`, `kit/telao_led`, `kit/grade_evento`, `kit/tripe_camera`, `kit/torre_luz`, `kit/canhao_moderno`.

**5. Dossiê.** Todo `mkvideo.py` grava `referencias/<id>/DOSSIE.json` e `FICHA.md` (ano, lugar, cenários, proibidos, fontes). Vídeo com cena de explicação exige `"visual": {"explicacoes": ["como funciona X — fonte"]}`.

**6. Padrões do canal travados:** a 1ª frase não pode abrir com data; duração entre 55 e 75 s (bloqueia fora de 50–80); `stories/<id>/orquestracao.json` traz a classe de cada frase (chave / explicativa / simples / transição), o briefing de efeito das ações-chave e 4 métricas que têm de dar 100%.

## v13b (24/11) — Folha 4 (pesquisa), heróis, tamanho real, queda e carro correndo

**Folha 4 — PESQUISA (`stories/<id>/folha4_pesquisa.md`).** O `mkvideo.py` faz o raio-X do roteiro e monta o plano de pesquisa (tema, lugar, época, pessoas, roupas, objetos, veículos, heróis e cada mecanismo explicado). `python3 pesquisar.py <id>` busca cada item na internet (Wikimedia Commons: fotos, quadros, desenhos), baixa os prints para `referencias/<id>/prints/` e monta o quadro `referencias/<id>/moodboard.jpg`. A fila (`make_video.sh`) roda isso sozinha no começo. **Olhe o quadro antes de aprovar o storyboard** e ajuste figurino, cenário e objetos a ele. Sem pesquisa, ou com mais de 1/3 dos itens sem referência, o render trava. Item que a busca não acha: consulta em inglês em `"visual": {"buscas": {"<item>": "<consulta>"}}`, ou a referência vista por outro meio em `"visual": {"referencias": {"<item>": "<url/descrição>"}}`.

**Heróis.** Todo roteiro tem o(s) seu(s) herói(s). Objeto: `"heroi": "kit/x"` (um) ou `"herois": ["kit/x", "kit/y"]` (vários); nome legível para a pesquisa em `"herois_nomes": {"kit/x": "Tesla Roadster 2026"}`. Personagens-herói são deduzidos (quem mais aparece; em vídeo de guerra/batalha, até 4 — os dois lados). Herói que não aparece em nenhuma cena trava o render. A folha 4 lista os heróis.

**Tamanho real.** Carro tem tamanho de carro, tanque de tanque, balão tripulado é gigante, balão de festa é pequeno. A tabela `_TAM_REAL` (em `mkvideo.py`) guarda o tamanho em metros de cada tipo de objeto grande e a ferramenta corrige a escala sozinha quando o roteiro põe menor (1 m real = 1,35 unidade; o boneco tem ~3). A correção aparece na folha 4. Objeto novo de tamanho conhecido: acrescente uma linha na tabela. `"s_livre": true` no 5º campo do prop libera (maquete, brinquedo).

**Queda e pulo.** Quem cai fica deitado EM CIMA do chão, inteiro no quadro (a câmera abre sozinha em frase com caiu/tombou/desmaiou/empurrou). Quem pula: a câmera abre e sobe. Frase que fala "os dois / ambos / juntos" nunca vira close em um só.

**Carro correndo no medidor.** Em cena de explicação, medidor em km/h (ou mph) com veículo = o veículo CORRENDO de lado, câmera junto, riscos de velocidade, fumaça de pneu na largada e propulsor na traseira (`"propulsor": false` tira o jato). Manual: `"manobra": "corre"`.

## v13c (24/11) — Cronograma, embarcações da época, batalhão, multidão

**Cronograma (`stories/<id>/cronograma.md`).** Sai junto com as 4 folhas e é atualizado pela fila a cada etapa. Parte 1: plano de cenas (cada frase: classe, cenário, câmera, quem, multidão, objetos, efeito planejado). Parte 2: as 14 etapas em ordem (folhas → pesquisa → modelagem → travas → voz → estilo/enquadramento → gates → storyboard → revisão e aprovação → render → montagem → conferência → auditoria → entrega), cada uma com o que confere e o estado. Nenhuma etapa começa com a anterior pendente; se uma etapa anterior muda, as seguintes aparecem como REFAZER. Atualizar à mão: `python3 cronograma.py <id>`.

**Embarcações da época.** Navio em cena é sempre o da época do vídeo, modelado e pintado como nas referências (`blender/navios_epoca.py`): galera a remo (até 1400), caravela com cruz vermelha (1400–1620), fragata preta com faixa creme e portinholas (1620–1865), vapor de guerra preto e branco com chaminé amarela (1865–1905), encouraçado cinza (1905–1960), destroier (1960+). Vale para o navio do cenário de porto e para os que entram pela narração; todos no tamanho real (30 m). `"navio_livre": true` desliga a troca. Embarcação específica (ex.: um vapor de rodas, uma jangada): pesquise na folha 4 e modele.

**Batalhão de verdade.** Plano aberto com tropa (figurino com fuzil ou SOL/TRO): mínimo de 32 soldados; batalha, ou dois exércitos em cena, mínimo de 48, cada farda no SEU bloco, frente a frente, com corredor no meio. Vale mesmo que o roteiro peça menos. `"poucos": true` no `crowd` libera (patrulha, escolta).

**Multidão nunca clona personagem.** Multidão automática só usa tropa (fuzil), povo (`POV`, `POVO`, `SOL`, `TRO`) ou figurino com `"hats"`/`"multidao": true`. Dois personagens da história num plano aberto ficam sozinhos. O "grande momento" automático só nasce em cena com tropa ou povo.

**Guerra sem tiro.** `"tiros": false` na batalha = impasse: ninguém voa, não há clarão. "Canhões" na frase só gera explosão se a frase disser que dispararam.

**Cidade só com cidade.** Rua, prédios e o kit de cidade da região só entram se a narração ou a pesquisa falarem de cidade/rua/loja/praça. História de fazenda, ilha, mato ou acampamento não ganha prédio de tijolo.

## LEITURA ESCRITA DE CADA FRASE — "encena" (25/11, obrigatorio; o storyboard nao e' aprovado sem ela)
A ferramenta nao entende frase: ela le palavra por palavra. Quem ENTENDE e' a IA que escreve/revisa o roteiro. Por isso, para CADA frase, escreva no beat:
```json
"encena": {"sentido": "afirmativa",
  "passos": [{"quem": 0, "faz": "anda_ate", "alvo": "kit/bathtub", "na": "entrou"},
             {"quem": 0, "faz": "entra_em", "alvo": "kit/bathtub", "na": "entrou"},
             {"alvo": "kit/bathtub", "faz": "transborda", "na": "transbordou"}]}
```
- `sentido`: **afirmativa** (aconteceu: tiro, briga, explosao aparecem) | **negativa** ("nenhum soldado deu um tiro", "o tiro nunca veio") | **hipotese** ("quase", "ameacou", "se tivesse") | **figurada** ("guerra de precos", "bateu recorde") | **fato** (data, numero, explicacao). Negativa/hipotese/figurada = NADA de tiro, explosao ou batalha na tela, sempre.
- `passos`: o que a TELA mostra, em ordem, preso na palavra `na` da narracao (`quem` = indice no "who"). Verbos (`faz`) em `encenacao.py` VOCAB: anda_ate, entra_em, transborda, senta, dorme, ajoelha, tomba, morre, pula, corre, golpe, empurra, atira, grita, vence, fala, olha, pensa, perde, rende, pega, mistura, cai, constroi, escreve, entrega, chega, desaba, mostra.
- Precisa de uma acao que nao existe? NAO pule: o passo vira "FALTA ANIMACAO" e trava; a correcao e' construir a animacao na ferramenta (encenacao.py + motor) e depois renderizar.
- A folha 3 mostra a LEITURA DA FRASE passo a passo (quem, o que, qual objeto 3D, em qual palavra e segundo). Conferir ali antes de aprovar o storyboard.

### Como fazer a leitura (comandos)
1. A fila gera sozinha o RASCUNHO da maquina: `stories/<id>/leitura.md` (frase + o que a maquina entendeu). O rascunho ERRA (ex.: "deu errado" = entregar; "a cidade passou a noite atirando, e nao havia inimigo" = negativa). NAO aprove rascunho.
2. LEIA cada frase e escreva a leitura certa em linhas curtas:
   `python3 encenacao.py revisar <id> <<'X'` / `b0 A atira@atirando:0` / `b1 F mostra@Pearl` / `b2 A golpe@brigaram:0>1; tomba@caiu:1` / `X`
   S = A afirmativa | N negativa | H hipotese | G figurada | F fato; passo = faz@palavra[:quem][>alvo] (alvo = indice do outro personagem ou objeto kit/...).
3. `python3 mkvideo.py <id>`; `python3 encenacao.py conferir <id>` (mao dupla); se acusar passo nao executado: `python3 encenacao.py forcar <id>` + mkvideo de novo + conferir.
4. A LEITURA MANDA: acao de personagem que nao esta na leitura NAO acontece na tela (acabou o "lenhadores = cortar").
