# Cartoon Shorts — SKILL v6 (estado da ferramenta, em português)

## Pipeline em uma linha
roteiro (PT ou EN) → voz → **âncoras de palavra** → spec (shots) → ajuste automático de enquadramento → verificações → áudio + legendas → render (3 fatias) → QA de quadros → MP4.

## Comandos (pasta `~/shorts/v3`)
| O quê | Comando |
|---|---|
| Voz + tempos (PT-BR) | `./produce_voice.sh <id> pt-BR-AntonioNeural +10%` |
| Versão PT a partir de um vídeo EN (retempo automático) | `./mkpt.sh <id>` (cria `<id>_pt`, traduz textos na tela via `stories/i18n_pt.json`) |
| Build | `./build3.sh <id>` |
| Ajustar enquadramento (ninguém cortado/escondido) | `./fit.sh <id>` |
| Gates (câmera + take a take + estilo) | `./gate_all.sh <id>` |
| Áudio + snapshot | `./snap.sh <id> <quadros>` |
| Produção PT em fila | `./pipeline_pt.sh` (idempotente; relançar após reinício) |
| Achar objeto da biblioteca | `python3 libfind.py copo` |
| Folhas de personagem/objetos/storyboard | `python3 sheets.py <id>` |

**Regra de ouro:** nunca rode `build3.sh`/`shot.mjs` enquanto a fila roda (a pasta `web/` é compartilhada). Para experimentar, copie para `~/shorts/v3x`.

## O que a ferramenta faz hoje
- **Câmera (medido em 20 shorts do canal):** glides suaves (ease-in/out) entre ângulos em vez de cortes, push-in constante (~0,45%/quadro), rolagem 2–4°, sem tremor de mão, impactos com kick de 6–7 quadros, transição "push-through" com borrão radial, cross-dissolve em mudança de lugar/luz.
- **Atuação (`web/acting.js`):** expressão por batida da fala (léxico PT e EN), 2 quadros antes da palavra; olhar para o parceiro e **direto para a lente** (quarta parede); gestos de braço (apontar, mãos na cintura, levantar, encolher, pensar, facepalm, saudar, mãos juntas…); piscadas irregulares (a cada 0,5–2,3 s) e uma em toda troca de expressão; leve "lean" para a câmera nas falas fortes.
- **Tempo por palavra:** `W('palavra', n)` / `WE(...)` em specs novos; specs antigos são reaproveitados em outro idioma pelo **retempo** (`mkretime.py`: alinha frase a frase e oração a oração).
- **Cor/luz:** grade medido contra o canal (zonas sombra/meio/luz, tint violeta nas sombras), ambiente lavanda → sombras violeta, céu com gradiente mais saturado, nuvens com barriga lavanda, bloom, luz de borda, raios de luz e poeira flutuando, ink de ~3 px quase constante.
- **Profundidade:** desfoque de lente em ~1/3 dos takes (10–14 px) e quase nítido no resto; personagens com sombreamento do lado do sol (card iluminado pela cena).
- **Mundo:** vento em grama/bandeiras/árvores/personagens, objetos caem e quicam, nuvens andando, cenários com camadas de objetos (dress), animais 3D (urso, cavalo, emu) feitos no Blender.
- **Biblioteca:** 75 objetos procedurais (Blender) + **94 objetos Quaternius CC0** (copo, mesa, cadeira, barril, baú, bigorna, garrafas, livros…) — `mk/<Nome>`.
- **QA:** `qa_camera` (saltos), `qa_takes` (herói cortado/pequeno/escondido, câmera dentro de geometria — inclui animais 3D), `qa_style` (faixas do canal), `qa_frames` (preto/branco/congelado/pop), freeze e loudness.

## Limites conhecidos (honestos)
- Cenário é gerado por código; o canal usa modelagem manual — chegamos perto em luz/cor/textura/densidade, não idênticos.
- Roupa dos personagens é desenho 2D: balança com o vento, mas não é tecido simulado.
- O ajuste automático afasta a câmera quando um take não cabe; em alguns takes os personagens ficam menores do que o ideal.
- Ritmo de câmera do canal medido em 2 gravações de tela de 8 s + relatórios do repositório; falta um vídeo longo de referência.

## Referências externas
`reference/claude-animated-shorts/` (MIT): relatórios medidos de 20 shorts do canal de referência (câmera, personagens, textura, luz, ink, cor), templates de áudio e QA. Quadros do canal NÃO incluídos (estudo privado).

---
## v6.1 — correções do motor encontradas na revisão do Emu War (PT)
Revendo os quadros do Emu War em português apareceram três defeitos reais (que também existiam nos vídeos em inglês). Todos corrigidos no motor e travados nos testes:

| Defeito | Causa | Correção | Trava (QA) |
|---|---|---|---|
| **Faixa escura/preta no horizonte** em ~40% dos quadros | o contorno ("tinta") comparava a profundidade de pixels vizinhos; no chão visto em ângulo rasante a profundidade muda rápido e o chão distante virava "borda" | `edgeAt` em `web/tail.js` agora mede a profundidade contra o **plano local** (em superfície plana, 1/profundidade é linear na tela; o pixel oposto prevê o vizinho). Silhuetas e quinas continuam com contorno | `qa_frames.py` marca "dark horizon band" |
| **Câmera abaixo do chão** (take mostrava a parte de baixo do terreno + faixa preta) | variações automáticas de elevação negativa com câmera longe jogavam `y` abaixo do piso (DECK = 6) | `camAt` (`runtime.js`) aplica **piso suave** (`SPEC.camFloor`, padrão 0,55 acima do chão, sem quinas; `false` desliga) | `qa_takes` reprova `below-ground` |
| **Rosto do herói desfocado** com o novo desfoque de lente | o foco ficava no ponto de mira, atrás do personagem mais próximo | o foco vai para o **personagem (ou animal 3D) mais próximo no meio do quadro**; só fundo/objetos de frente desfocam (`near` = 0,45) | revisão visual + estilo |

Fila de produção (`pipeline_pt.sh`) agora: exige gate verde (câmera + takes + estilo; 1 refit automático, senão pula a história e registra), renderiza em 3 fatias, roda o QA de quadros, **re-renderiza só os quadros marcados** (1 passada) e só então monta o vídeo.

---
## v6.2 — composição automática + storyboard antes de renderizar
Depois do Emu War, o processo ficou assim para cada vídeo (nada vai para o render sem passar por aqui):

1. **Storyboard de verdade** (`node storyboard.mjs <id> sb.jpg 360 && python3 sbsheet.py sb.json sb.jpg`): 1–2 quadros por take, já com o enquadramento ajustado, tempo e a frase da narração. Leva ~1,5 min por vídeo (renderiza em 360×640).
2. **Regras globais de composição** (`qa_takes.mjs`, valem até para takes sem herói definido):
   - personagem maior que 125% da altura do quadro → "too close";
   - personagens existem mas nenhum aparece → "empty";
   - personagens menores que 10% da altura (6% em multidão) na maior parte do take → "TINY" (aviso; o `fit.sh` aproxima a câmera);
   - câmera **dentro de um sólido** (casa, caminhão, tanque…) → reprova (detecção por caixa + raios de dupla face).
3. **`fit.sh` em duas fases**: afasta a câmera (×1,12) enquanto houver corte/oclusão/"too close"/"empty"; depois aproxima (×0,89, mínimo 0,55) os takes minúsculos, desfazendo se quebrar alguma regra.
4. **Ferramentas de câmera/ação**: movimento com velocidade constante (`move: [destino, a, b, 'lin']`), câmera que acompanha um personagem/veículo (`cam` com `ease: 'lin'` + `nocut: true`), ator sobre veículo com `y` em função do quadro, rastro de poeira (`dustTrail`), nuvem de poeira em silhueta única.
5. **Render balanceado** (`render_missing.sh`): divide só os quadros que faltam em 3 fatias iguais; depois do render o `qa_frames.py` marca e refaz só os quadros com defeito (faixa escura, preto, branco, pisca).

---
## v6.3 — lições da fila em português (para não repetir)
- **Dois "defeitos" que eram só meu erro de leitura:** ao dividir uma folha de contato com um corte no meio de uma linha, os takes cortados pareciam "câmera olhando o chão". Sempre cortar a folha em múltiplos da altura da linha (`splitrows.py`).
- **Teste de estilo por história:** o gate compara cada vídeo com as faixas do canal de referência (saturação ≥ 0,32, luminância 0,31–0,63, detalhe ≥ 0,229...). Cenas de neve, praça de pedra e palácio de areia reprovavam por serem naturalmente pálidas ou muito claras. Correção por história, sem mexer nas outras: neve azul-violeta + céu rosa (Uísque), paralelepípedo quente (Balde), exposição 0,72 + desfoque menor (Zanzibar). Ajustar a **cena**, nunca afrouxar o teste.
- **Rastreamento em vez de plano aberto:** takes de ação (caminhão, bando de emus, cavalaria, retirada) usam câmera que acompanha o alvo com velocidade constante (`ease:'lin'` + `move:[...,'lin']`, `nocut:true`). Resultado: personagem grande e legível o tempo todo.
- **Escala de animais 3D:** cavalo/urso/emu com `s` calculado para o mundo (cards têm 3,15 m); animal com `s` 1,4 ficava ~2× maior que o soldado e ocupava >100% do quadro. Cavalo `s` 0,7.
- **Câmera dentro de casa:** o take do rio ficou "dentro" de uma casa (parede azul). O detector de "câmera dentro de sólido" agora reprova isso antes do render.
- **Link simbólico em laço** (`web/sets/sets`) fazia o zip do kit anterior ficar com pastas aninhadas; removido.
