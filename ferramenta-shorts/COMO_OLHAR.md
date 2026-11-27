# COMO OLHAR — o jeito de pensar, olhar e agir da sessão principal

Ordem do Gibson (24/11): as sessões de produção têm de pensar, agir e **olhar** igual à sessão principal. Este arquivo é o treino. Leia inteiro antes do primeiro storyboard e volte a ele em cada vídeo. As imagens citadas estão em `treino_olhar/` — **abra cada uma**.

## 1. A postura

- **O quadro é culpado até provar o contrário.** Você não olha o storyboard para confirmar que está bom; olha para achar o que está errado. Se terminou de olhar e não achou nada, olhou rápido demais: olhe de novo, fundo para a frente.
- **A pesquisa manda, não a sua memória nem o padrão da ferramenta.** Antes do storyboard, abra `referencias/<id>/moodboard.jpg` e `folha4_pesquisa.md`. Cada quadro é comparado com o que a pesquisa mostrou: lugar, época, roupa, objeto, navio, veículo.
- **A narração manda na cena.** Leia a frase e pergunte: "quem assiste sem som entende o que a frase diz?" Se não, a cena falhou, mesmo bonita.
- **Bonito não é certo.** O primeiro storyboard da Guerra do Porco era bonito e tinha prédio de tijolo de cidade numa ilha de fazendas em 1859.
- **Passou no gate não é aprovado.** Os gates conferem câmera, corte e luz. Não sabem se o navio é da época.
- **Nunca diga "ficou bom" sem ter aberto a imagem** (Read no arquivo). Nunca descreva um quadro que você não abriu.

## 2. O método (sempre nesta ordem)

1. Abra o quadro da pesquisa. Escreva em uma linha o que ele estabelece: lugar, época, roupas, objeto/veículo/navio.
2. Abra o storyboard **em faixas** (uma fileira por vez, cortada no tamanho certo — se cortar errado você julga quadro pela metade; aconteceu comigo). Abra também `grade_acoes.jpg`.
3. Para **cada quadro**, olhe em 4 passadas, sem pular:
   - **Fundo:** que prédios, árvores, horizonte, navio? São do lugar e da época da pesquisa?
   - **Meio:** objetos e veículos. Tamanho real? Da época? O herói aparece?
   - **Gente:** quem está ali? Alguém cortado, de costas, dentro do chão, tapando o objeto? Tem clone do personagem principal? A tropa é um batalhão ou um punhado?
   - **Frase:** a ação da narração está acontecendo nesse instante? Texto ou rótulo passa por cima da legenda (faixa a 70% da altura)?
4. Liste os defeitos. Para cada um decida: **é do roteiro** (corrija o `beats.json`) ou **é da ferramenta** (qualquer roteiro parecido sofreria o mesmo → `pendencias_motor/` + aviso à principal; não tente contornar no roteiro).
5. Corrija, gere o storyboard de novo e **olhe de novo do zero** — a correção de uma cena muda outras.
6. Só então escreva a revisão e aprove.

## 3. A pergunta que separa roteiro de ferramenta

"Se outro roteiro tivesse uma frase parecida, o defeito apareceria de novo?"
- **Sim** → é da ferramenta. Ex.: a palavra "canhões" fazia soldado voar pelos ares numa guerra sem tiro. Qualquer roteiro com "canhões" sofreria. Corrigido no motor, com teste.
- **Não** → é do roteiro. Ex.: a cena pede `"tiros": false` e o roteiro não pôs.

## 4. Catálogo de defeitos reais (o que eu deixei passar ou peguei, e como se vê)

| # | O que estava errado | Como perceber | Onde ver |
|---|---|---|---|
| 1 | Prédios de tijolo com caixa d'água numa ilha de fazendas de 1859 | Olhe o **fundo** antes dos personagens; compare com a pesquisa (fazenda, pinheiros, costa) | `01_ERRADO…` × `01_CERTO…` |
| 2 | Dez clones do fazendeiro na cena do mapa | Conte as pessoas: rostos e roupas iguais ao personagem principal = clone | `01_ERRADO…` (quadro do "1859") |
| 3 | Rua de paralelepípedo na cena da horta | O **chão** também é cenário: grama ou pedra? | `02_ERRADO…` × `02_CERTO…` |
| 4 | Navio a vapor com chaminé em 1859, e minúsculo | Navio tem época (veja `05_navios_por_epoca.png`) e tamanho: "navios de guerra" têm de dominar o fundo | `02_ERRADO…` × `03_CERTO…` |
| 5 | Dois exércitos misturados, vermelhos e azuis no mesmo bloco, e poucos | Cada farda no seu lado; plano aberto de tropa = batalhão (32/48) | `02_ERRADO…` × `03_CERTO…` |
| 6 | Soldado voando e clarão de tiro numa guerra sem um tiro | Leia a história: houve tiro? houve explosão? Se não, nada explode | — |
| 7 | Carro "voando" a 3 m, sem nada saindo de baixo | "Voou" = sai do chão, sobe alto, atravessa a cena, com o efeito saindo **do objeto** | `04_CERTO…` |
| 8 | Frase de ciência com dois bonecos parados conversando | Frase que explica mecanismo = cena de explicação sem personagem | `04_CERTO…` |
| 9 | Personagem na frente do carro na cena do carro | Quem é o sujeito da frase? Se é o objeto, gente fica de lado | `04_CERTO…` |
| 10 | Rótulo cortado na borda / em cima da legenda | Olhe as **bordas** do quadro e a faixa dos 70% | — |
| 11 | Boneco caído com metade do corpo dentro do chão, ou com a cabeça fora do quadro | Em toda queda, procure os pés E a cabeça | — |
| 12 | "Os dois pularam" com close num só | Conte quantos a frase cita e quantos estão no quadro | — |
| 13 | Carro do tamanho de brinquedo ao lado do boneco | Compare com a altura do personagem: carro bate no peito, não no joelho | — |
| 14 | Barril, caixote e lampião em vídeo de 2026 | Passe o olho nos objetos pequenos do chão: são da época? | — |
| 15 | Print da pesquisa que não tem nada a ver (uma torre, um tanque, uma nota de dólar moderna, um retrato de 1940) | A pesquisa também se confere, print por print: escreva o nome do arquivo ruim em `referencias/<id>/prints_ruins.txt`, refine a busca (`"visual": {"buscas": …}`) e rode `pesquisar.py` de novo | `06_quadro_de_pesquisa…` (a sessão B achou 7 prints errados que a principal tinha deixado passar) |

## 5. Erros de processo que eu cometi (não repita)

- Afirmei um fato do roteiro com duas fontes fracas e estava errado. **Confira na fonte antes de afirmar; se errou, diga que errou.**
- Rodei um comando de limpeza com variável vazia e apaguei pastas. **Nunca `rm -rf` com variável sem checar que não está vazia.**
- Julguei um storyboard cortado na altura errada. **Confira o corte antes de julgar.**
- Disse "pronto" antes de olhar o quadro renderizado; o defeito só apareceu no vídeo. **Olhe o mp4 (quadros extraídos), não só o storyboard.**

## 6. Como relatar

- Só defeito **já resolvido** vai para o Gibson (regra mestra). Para a principal, a sessão relata tudo.
- Diga o que viu, em qual quadro, e o que mudou. Sem "acho que ficou bom".
- Se não conseguiu conferir algo, diga que não conferiu. Não invente.

## 7. O que a aprovação exige agora

`stories/<id>/revisao_storyboard.md` precisa ter, além de uma linha por frase:
- `pesquisa: …` — o que o quadro de referências estabelece (lugar, época, roupas, objetos) e o que você comparou.
- `defeitos procurados: …` — respondendo, com o que viu: **cenario, epoca, tamanho, cortado, multidao, legenda, acao, objeto**.

Sem essas duas linhas `./aprovar_storyboard.sh` recusa.

## Conferencia FRASE A FRASE (24/11, obrigatoria antes de mandar o mp4)
`bash frase_a_frase.sh <seu-branch> <id> <caminho do mp4> /tmp/ff.jpg` e abra /tmp/ff.jpg: um quadro no meio de cada frase, com a frase escrita embaixo.
Para cada frase pergunte: a imagem mostra o que a narracao diz? (papa -> tem papa; muros -> tem muralha; sacada -> tem sacada; presos -> tem gente sendo presa).
Frase que nao aparece na tela = defeito: refaca a cena (./refazer.sh <id> bN) antes de mandar.
