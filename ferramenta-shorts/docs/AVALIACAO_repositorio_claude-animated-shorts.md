# Avaliação: repositório "claude-animated-shorts" (mromidev) × nossa ferramenta

## O que é
Um skill do Claude (MIT) para shorts verticais de 55–70 s com **personagens 2D "bean" desenhados em canvas, dentro de um mundo 3D pintado**, com contorno de tinta preto, desfoque de lente, câmera deslizando, narração e áudio sintetizado. Traz:
- `STYLE_BIBLE.md` + **7 relatórios MEDIDOS** de 20 shorts do canal de referência: movimento/câmera, profundidade, texturas, personagens, luz, contornos e cor (com números, receitas e "top 5 mudanças").
- Código de referência (TypeScript/Remotion/react-three-fiber): personagens, mundo, ink, lens blur, grade, cards iluminados, câmera.
- Ferramentas de áudio (SFX/música sintetizados, mixagem com ducking, -15 LUFS) e de QA (frame a frame: preto/branco/congelado/pop, loudness, folhas de contato, comparações lado a lado).

## Veredito
**Soma muito — é a mesma família do nosso estilo.** Nosso motor de personagens (`Pen`, cabeças "bean", rosto com 14 expressões, contorno ameixa, cards 2D no mundo 3D) já vem dessa linhagem. O repositório entrega o que nos faltava: **números reais do canal** em vez de achismo.

**Não serve como "plug-and-play":** o stack é outro (Remotion + react-three-fiber + postprocessing, render na GPU do PC do autor). O nosso é three.js headless no navegador + ffmpeg, render em CPU na nuvem. Então adotamos **os números e os algoritmos**, não o código como está.

**Regras dele que NÃO valem para nós:** "sem legendas" e "só inglês" (o nosso pedido é legenda + português). **Regra dele que vale:** nunca copiar roteiro/personagens/planos do canal e nunca citar o nome do canal na narração (histórias e personagens são sempre originais). Os quadros de referência do repositório (frames/sheets) são material de estudo privado do autor: **não copiei nem redistribuo**.

## O que ele me ensinou que eu estava fazendo ERRADO (medido nos 20 shorts)
| Tema | Antes (meu) | Medido no canal | Ação |
|---|---|---|---|
| Câmera | cortes a cada ~2 s | quase **sem corte seco** (0–1 por vídeo): glides suaves de 18–40 quadros, ease-in/out; empurra a câmera para dentro (~0,15–0,35%/quadro) em TODO plano parado; rolagem (dutch) 4–5°; sem tremor de mão; impacto = 6–7 quadros alternando de sinal | **aplicado** (glide contínuo, push-in constante, sem tremor) |
| Piscadas | a cada ~4 s | a cada **0,5–2,3 s**, 4 quadros (meia/fechada/fechada/meia) e **uma em toda troca de expressão** | **aplicado** |
| Expressão | trocas raras | muda em cada batida da fala, **2 quadros antes da palavra** | **aplicado** (diretor de atuação ligado à narração) |
| Corpo | — | adultos 3,5 cabeças, pernas/braços = traço fino, mãos = pontos | já tínhamos (build "lanky") |
| Textura | ruído + relevo | **campos de cor chapados + linhas finas pintadas**, claro e saturado (nada de lama) | **vou reduzir o ruído/relevo** (em andamento) |
| Luz | sombra cinza | sombra **violeta/azul** (dia: azul só na sombra; pôr do sol: contraluz, sombra violeta) | parcialmente aplicado (grade); falta sombreamento "two-tone" no material |
| Cards (personagens) | sem luz da cena | cartão **iluminado pela cena**, brilho de rosto ~0,93, gradiente suave do lado do sol | **a fazer** |
| Desfoque | fixo | DOF em ~1/3 do tempo, planos médios/fechados com raio 10–16 px, **foco nos olhos**; planos abertos nítidos | **a fazer** (tabela por tipo de plano) |
| Contorno | some com a distância | ~3 px, **quase constante** com a distância, vincos por normais | **aplicado** (fade removido) |

## O que vamos adicionar à ferramenta (checklist)
1. [feito] Câmera: glide contínuo, push-in, sem tremor, rolagens, kicks. 
2. [feito] Atuação: expressões por batida da fala (PT e EN), olhar para o parceiro e **para a lente (quarta parede)**, gestos de braço (apontar, mãos na cintura, levantar, encolher, pensar, facepalm, saudar…), piscadas irregulares.
3. [feito] Âncoras de tempo por PALAVRA (idioma/voz novos reencaixam o vídeo sozinho).
4. [em andamento] Textura chapada + linhas finas; cor/grade calibrada com os alvos do canal.
5. [a fazer] DOF por tipo de plano; cards iluminados pela cena; sombra "two-tone".
6. [a fazer] QA do repositório: `short_qa.py` (preto/branco/congelado/pop + loudness + folhas) e `sbs_sheet.py` (lado a lado com referência) — juntar ao nosso `qa_frames`.
7. [a fazer] Áudio: aproveitar `sfx_gen/instruments/mix` (ducking da trilha sob a voz, -15 LUFS) para SFX mais realistas.

Cópia local (texto/código, sem os quadros do canal): `reference/claude-animated-shorts/` dentro do kit.
