# OPERAÇÃO DA FÁBRICA (leia isto primeiro, sempre)

Série atual: **Guerras Inusitadas** (EP numerado; `"serie": "Guerras Inusitadas", "ep": N` no topo do roteiro). Histórias reais e curiosas de guerras/conflitos absurdos, personagens originais, 150–175 palavras narradas (~60 s).
EPs já feitos: 01 Karánsebes, 02 Emus, 03 Toledo, 04 Balde, 05 Gansos, 06 Porco, 07 Bolos, 08 Zanzibar (38 minutos), 09 Futebol (1969), 10 Chaleira (1784). Não repita tema. Dança e Tulipas ficaram FORA da série (pasta `fora_do_tema/`): só entra guerra/conflito.
Ideias ainda livres: Orelha de Jenkins (1739), Banquinho Dourado (1900), 335 anos de Scilly, Guerra do Bacalhau, Guerra do Uísque, Guerra das Laranjas (1801), Guerra dos Pastéis não (já é Bolos).
Cuidado visto na prática: se a narração diz "noite", a cena e as seguintes ficam de noite até outra cena ter `"hora": "dia"`. Todo figurino precisa das cores `jacket`, `pants`, `boots`; chapéu `cap`/`beret`/`bonnet` usa a cor `cap`.

## Os 7 passos (não pule nenhum)

1. **Ler** `CAPACIDADES.md` (o que a ferramenta tem) e `MODO_RICKS.md` (como o roteiro é escrito).
2. **Escrever** `videos/<id>/beats.json` (formato no `GUIA_DO_ROTEIRISTA.md`; copie um roteiro pronto, ex. `videos/porco1859/beats.json`, e troque). Ao escrever cada frase, pergunte: "a ferramenta consegue MOSTRAR isto?". Se não, mude a frase.
3. **Portão de entrada:** `./novo_video.sh <id>`. Ele gera as duas folhas e responde `LIBERADO` (entrou na fila) ou `BLOQUEADO: N riscos`.
4. Se bloqueado: abra `stories/<id>/folha2_producao.md`, cada risco traz a **CORREÇÃO** pronta. Corrija o `beats.json` e repita o passo 3. Risco visto e aceito: `"riscos_ok": true` na cena. Falta modelo 3D (veja a tabela **PARA O BLENDER** da folha 2): escreva o objeto no arquivo da SUA sessão `blender/objetos_<sessao>.py` usando `blender/formas.py` (formas redondas e chanfradas: `cil`, `bola`, `torno`, `tubo`, `arco`, `caixa`; exemplo pronto em `blender/objetos_principal.py`), rode `blender -b --python blender/objetos_<sessao>.py` (objeto antigo com cara de caixote: `blender -b --python blender/arredondar.py -- nome`), acrescente uma linha `["regex da palavra", "kit/nome", escala, false]` no arquivo da SUA sessão em `obj_dict.d/` (`principal.json`, `sessao_a.json` ou `sessao_b.json` — nunca no `mkvideo.py`, para o merge entre sessões não apagar o objeto de ninguém; regex sempre com `\\b` de palavra inteira) e rode `python3 capacidades.py`. Faça commit + push do `.glb`, do `blender/` e do seu `obj_dict.d/` logo depois de modelar. Palavra com dois sentidos ("rádio" elemento × aparelho): NÃO ponha no `obj_dict.d/`; use no beats.json do vídeo `"objetos_do_video": {"\\bradio\\b": "kit/curie_box"}` (vale só nele). Animais com modelo: cavalo, urso, porco, galinha, galo, pato, gaivota, vaca, cachorro, gato, ovelha, cabra, burro, veado, raposa, lobo, coelho, leão, elefante, emu → `"animals": [["dog", 1.6, 0.6]]`. Algo no CÉU (balão voando): modele uma versão já no alto (ex.: `kit/balloon_air`). `torno(..., tampa=False)` faz anel/friso aberto.
5. **Esperar:** `bash status.sh`. Deixe SEMPRE uma espera em segundo plano (`until [ -f stories/<id>/DONE ] || [ -f stories/<id>/SKIP ]; do sleep 20; done`), senão a máquina dorme e a fila para.
6. **Verificação final:** `./conferir.sh <id>` e depois ABRIR `out/<id>/review_sheet.jpg` e olhar. Defeito crítico → corrigir o roteiro e `./refazer.sh <id> bN` (cenas) ou `./refazer_tudo.sh <id>` (inteiro). Não pergunte ao Gibson: corrija e relate.
7. **Entregar:** mandar pelo chat o mp4 ORIGINAL de `entregas/<id>/` (1080×1920) + relatório curto (o que passou, o que não passou, o que foi refeito). Commit + push.

## Regra número 1: seguir o roteiro À RISCA

Tudo que a narração cita tem que aparecer na tela, na mesma cena: se diz "fazenda", tem fazenda (celeiro, cerca, feno); se diz "notas de dólar", o personagem segura as notas; se diz "navios", tem navio. A ferramenta já põe sozinha lugares (`LUGARES` no `mkvideo.py`: fazenda, casa, igreja, mercado, floresta, acampamento, castelo, cidade, praça) e objetos (`OBJ_DICT`). Cada cena da folha 2 tem a linha **CONFERIR NA FOLHA DE CONTATO** com as palavras da narração: confira uma por uma no storyboard/folha de contato. Faltou → ponha em `props`, na mão (`who`), ou modele. Não entregue vídeo em que a narração fala de algo que não se vê.

### O que a ferramenta EXIGE por palavra (a folha 2 bloqueia se faltar)

| A narração diz | Tem que aparecer | Como |
|---|---|---|
| queimaram, tacaram fogo, incêndio, em chamas | labaredas em cena e alguém com tocha | automático em cena externa; `"who": ["X:0:angry:torch"]` |
| batalha, atacaram, invadiram, lutaram, bombardearam | tropa dos dois lados lutando em plano aberto | `"batalha": true` + `"crowd"` (uma cena por batalha citada: 3 batalhas = 3 cenas) |
| explodiu, explosão, bomba | explosão com som | `"fx": ["burst@N"], "sfx": ["cannon@N"]` |
| fugiu, correu, debandada, retirada | gente correndo | `"shot": "track"` ou `"batalha": true` |
| colina, montanha, morro | cenário de montanha | automático (`"set": "mountain"`) |
| cavaram, trincheira, enterraram | pá na mão e poeira | automático (pá) + `"fx": ["dust@N"]` |
| se abraçaram | os dois andam um até o outro e ficam colados | automático (`"interacao": "abracar"`) |
| beberam, brindaram | caneca na mão e comemoração | automático |
| muito frio, inverno, neve, gelado | neve caindo, chão branco, personagens tremendo | automático (`"clima": "neve"`) |
| muito quente, calor, deserto, seca | luz de sol forte e personagens suando | automático (`"clima": "calor"`) |
| conversaram / discutiram / brigaram | diálogo em turnos / discussão com cara fechada / empurrão | automático pelo texto ou `"acao"`/`"interacao"` |
| tiro, atirou, disparou (com soldado de fuzil em cena) | clarão e fumaça saindo do CANO da arma de quem atira, com som | automático; nunca estrela de explosão solta no meio da cena |
| correu, fugiu, perseguiu (cena de `"shot": "track"`) | personagens CORRENDO (passo rápido, corpo inclinado) | automático |
| correram atirando / atiraram correndo (soldado de fuzil numa cena `"shot": "track"`) | soldado correndo de perfil, aponta o fuzil no tiro e o clarão acompanha a ponta do cano | automático |
| cartório, prefeitura, tribunal, banco, consulado | o prédio ao fundo | automático |
| navio chegou / desembarcaram / aportou / zarpou / partiu | navio e barco ANDANDO na água (chegando ao cais ou indo embora) | automático em cena de cais (`"set": "harbor"`) |
| dirigiu, foi de carro/caminhão/carroça, pilotou, pedalou | o veículo atravessa a tela com o 1º personagem do `who` ao volante | automático (`"veiculo"`) |
| vento, ventania, vendaval | vento forte e folhas voando | automático (`"clima": "vento"`) |
| bandeira | mastro com bandeira ondulada (vermelha e branca) ou bandeira na mão listrada | automático |
| navio, porto, marinha | cais com navios | automático (`"set": "harbor"`) |
| rei, rainha, imperador, sultão | alguém de coroa | figurino com `"profissao": "rei"` |
| general, almirante, coronel, capitão | alguém de farda de oficial | `"profissao": "general"` |
| camponês, fazendeiro, agricultor | alguém de chapéu de palha | `"profissao": "agricultor"` |
| fazenda, casa, igreja, mercado, floresta, acampamento, castelo, cidade | o lugar ao fundo | automático (`LUGARES`) |
| qualquer objeto ou animal | o modelo 3D em cena | automático se existir; senão modelar |

Não corra os takes: se a frase tem duas ações, divida em duas cenas. Vídeo de 65–70 s com tudo acontecendo é melhor que 55 s com narração sem imagem.

## Todo vídeo tem (a folha 2 confere)

- Objeto herói abrindo e fechando o vídeo, com close de câmera.
- 2 grandes momentos em plano aberto com multidão, efeito e som; no mínimo 2 planos abertos.
- Mapa rápido quando cita lugar.
- Em toda cena média os personagens interagem (interações diferentes de cena para cena) e têm expressão própria (use expressões variadas no `who`: angry, shout, sad, cry, smug, surprised, scared, suspicious, além de smile, grin, laugh, shock, stern, nervous, pained).
- Efeito + som em toda palavra de ação.

## Enquadramento (o controle automático já barra; confira mesmo assim na folha de contato)

- **Placa** (texto em placa de madeira): tem que aparecer INTEIRA sempre que estiver no quadro. O inspetor de enquadramento agora mede a placa e abre a câmera sozinho; se a folha de contato ainda mostrar placa cortada, encurte o texto (`"text"`) ou troque para `"titulo": true`.
- **Personagem grande e cortado** (cabeça ou braço para fora, alguém passando colado na lente): o inspetor reprova qualquer pessoa com mais de 60% da altura do quadro e mais de 1/4 para fora, e no close de objeto quem fica entre a lente e o objeto não é desenhado. Se ainda aparecer: tire gente do `who`, use `"shot": "group"` ou `"chega": false`.
- Depois de mexer no roteiro por causa disso: `./refazer.sh <id> bN` (ou `./refazer_tudo.sh <id>` se os quadros já foram apagados).

## Se a máquina reiniciar ou a sessão dormir

- O trabalho NÃO se perde: cada etapa tem selo em `stories/<id>/stages/`, o render é salvo em trechos de 150 quadros (`ckpt/<id>/`) e o gancho de início (`boot.sh`) relança a fila sozinho, que continua do trecho onde parou.
- Há um despertador por sessão (tarefa agendada, de hora em hora) que manda conferir a fila e pegar o próximo item do `PLANO_PRODUCAO.md`. Nunca termine um turno sem vídeo na fila e sem espera em segundo plano.
- Não use ferramenta que peça aprovação do Gibson (ex.: mensagem entre sessões): a sessão trava até ele aprovar. Aviso de entrega = `entregas/<id>/RELATORIO.md` + commit + push.

## Identidade dos personagens (ordem do Gibson)

Cada personagem tem cara e roupa próprias, como no canal de referência. Use `"profissao"` no figurino (padeiro, agricultor, nobre, politico, empresario, rei, general, soldado, marinheiro, cientista, medico, comerciante, pescador, padre, camponesa, jornalista) e mude as cores para diferenciar; a ferramenta distribui barba, bigode e óculos por personagem (para fixar: `"beard"`, `"moustache"`, `"glasses"`). Dois personagens principais da mesma cena nunca com o mesmo figurino + variante. Use expressões diferentes ao longo do vídeo (o `who` de cada cena pode mudar a expressão). Quem não é soldado não usa uniforme: terno (`"tie"`) para político/empresário, avental para padeiro, chapéu de palha para agricultor.

## Objeto real que não existe (carro, avião, prédio, aparelho de outro nicho)

Siga `referencias/LEIA.md`: pesquisar na internet → ficha do objeto em `referencias/<nome>/FICHA.md` → modelar com `formas.py` → conferir com `foto.py` contra a referência → cadastrar. Profissões novas (médico de jaleco, piloto, astronauta...): use `"profissao"` ou monte o figurino com as cores e o chapéu certos e registre a profissão nova em `PROFISSOES` no `mkvideo.py`.

## Formato dos objetos (ordem do Gibson: nada de estilo Minecraft)

Quadrado só o que é quadrado de verdade: placa, casa, caixote, mesa, livro. Todo o resto (bichos, frutas, bolo, garrafa, vaso, bola, chaleira, barco, roda, fogo, flor, coroa...) é modelado com as formas redondas do `blender/formas.py`. A folha 2 acusa como RISCO todo objeto do kit montado com caixas ("CAIXOTE") usado no vídeo: refaça o objeto (mesmo nome de arquivo) antes de renderizar. Confira na folha de contato se cada objeto se lê de primeira; se parecer bloco, refaça.

## Proibido

- Renderizar com risco em aberto, ou entregar sem olhar a folha de contato.
- Editar `web/`, `mkvideo.py`, `stories/_h.js` só para "fazer passar" um vídeo. Só se mexe na ferramenta para corrigir defeito dela, testando antes num storyboard fora da pasta da fila.
- Rodar `build3.sh`, `fit.sh`, `shot.mjs`, `storyboard.mjs` na pasta da fila enquanto ela roda.
- Afrouxar gate/QA, apagar `SKIP` sem corrigir a causa, usar agentes/subagentes.
- Entregar prévia comprimida no lugar do original.

## Quando algo dá errado

| Sintoma | O que fazer |
|---|---|
| `BLOQUEADO` no `novo_video.sh` | corrigir o roteiro pela folha 2 e rodar de novo |
| `stories/<id>/SKIP` apareceu | ler `logs/gate_<id>.txt`; quase sempre é enquadramento: tire gente do `who`, troque `shot` para `group`; apague `SKIP` e `fails` e relance a fila |
| render terminou em 2 min sem mudar nada | reaproveitou quadro velho: `./refazer_tudo.sh <id>` |
| log diz `voz de TESTE` / a fila para com `PARADO: voz de TESTE` | o edge-tts falhou (certificado do proxy). Teste: `cd stories/<id> && SSL_CERT_FILE=/root/.ccr/ca-bundle.crt edge-tts --proxy "$HTTPS_PROXY" --voice pt-BR-AntonioNeural --text oi --write-media /tmp/t.mp3`. Se só funcionar assim, acrescente a CA ao certifi: `cat /root/.ccr/ca-bundle.crt >> $(python3 -c 'import certifi;print(certifi.where())')`. Depois relance a fila. NUNCA entregue vídeo com voz de teste |
| dois `run_queue.sh` ao mesmo tempo (SKIP falso, ENOENT em `ckpt/`) | sempre `pgrep -f run_queue.sh` antes de lançar; se houver dois, `pkill -f run_queue; pkill -f make_video; pkill -f render_pool` e lance um só |
| render com `erro de pagina` / `No space left on device` / quadros `DESISTIDO` | disco cheio: `df -h .`; apague `out/<id>/frames` dos vídeos já entregues e `/root/.cache/pip` (NÃO apague `/root/.cache/huggingface`). Se o log do vídeo tiver quadro DESISTIDO, rode `./refazer_tudo.sh <id>` depois de liberar espaço |
| fila parada (`bash status.sh` sem processo) | `nohup bash run_queue.sh > logs/queue_run.log 2>&1 &` |
| máquina reiniciou | a fila volta sozinha; recrie a espera em segundo plano |
| personagem cortado / cena vazia / objeto fora do quadro | ver "Reparos" no fim da folha 2 |
| várias sessões no mesmo repositório | cada sessão trabalha no SEU branch e em ids diferentes; antes de começar: `git fetch origin claude/bold-sagan-dskrsj && git merge --no-edit FETCH_HEAD` para pegar a ferramenta mais nova |

## Arquivos

`novo_video.sh` portão de entrada · `conferir.sh` verificação final · `refazer.sh` / `refazer_tudo.sh` reparo · `status.sh` andamento · `run_queue.sh` fila · `mkvideo.py` diretor (gera spec, folhas, plano) · `capacidades.py` → `CAPACIDADES.md` · `GUIA_DO_ROTEIRISTA.md` formato do roteiro · `MODO_RICKS.md` estilo.


## BIBLIOTECA 3D PRIMEIRO (ordem do Gibson) — NÃO modele o que já existe
1. Antes de pensar em Blender, abra `CAPACIDADES.md`: seção **Animais** (todos prontos e animados — entram sozinhos quando a narração cita) e **Biblioteca 3D completa** (84+ objetos em `kit/`, prédios, veículos, natureza, ferramentas, guerra).
2. Só modele se a **folha 2** disser `FALTA` na tabela **PARA O BLENDER**. Se a folha não pedir, NÃO modele.
3. Animal nunca se modela (cachorro, gato, vaca, ovelha, cabra, porco, cavalo, burro, veado, raposa, lobo, coelho, leão, elefante, urso, galinha, galo, pato, ganso, gaivota, emu já existem). Close de cachorro: `kit/dog_sit`.
4. Modelo novo de verdade: siga o exemplo de `blender/objetos_cc*.py` (formas redondas), confira com `blender/foto.py`, registre a palavra em `obj_dict.d/<sua sessão>.json` e dê commit — ele passa a valer para as 3 sessões no próximo merge.

## Lições de 18/11 (a ferramenta já faz sozinha; confira na pré-checagem)
- **Pré-checagem antes do render** (pega 80% dos defeitos sem gastar render): adiante a voz (`./produce_voice.sh <id> <voz> <rate>` + `stories/<id>/stages/voice`) e gere a folha de storyboard numa cópia fora da fila (`sb.sh <id>`). Olhe: objeto herói visível, sem clones, cenário certo, nada tapando o quadro.
- **Multidão sem clones**: multidão criada pela ferramenta usa só o figurino `POV` (povo, 7 variantes de cor/chapéu). Na multidão escrita no roteiro ponha só `["POV"]` (e soldados/marinheiros em Guerras); nunca rei, cientista, médico, famoso ou protagonista.
- **Famosos** (`"pele"` no figurino) e **mulheres** (`hairStyle` `bun`/`long`) não ganham barba/óculos sorteados.
- **Hora/clima** (`"hora": "noite"`, neve por "gelado"…) valem só na cena onde aparecem.
- **Objeto gigante** (torre, foguete, vulcão) fica ao fundo (z −11 a −16); para o close de objeto herói faça uma **maquete** pequena num pedestal (ex.: `kit/tower_mini`). Coisa no céu: versão já no alto (`kit/balloon_air`, `kit/falcon_air`).
- **Cenário**: base de foguete/litoral = `harbor`; campo sem fazenda não tem mais celeiro gigante automático.
- **Boné** (`hat: cap`) agora fica acima dos olhos.
