# MODO DE AÇÃO DEFINITIVO
**Ordem do Gibson — 21/11/2026**  
Documento mestre. Vale acima de qualquer outra instrução de roteiro.

---

## 1. Objetivo único (não negociável)

Cada verbo de ação da narração **tem que aparecer visualmente na tela no instante da palavra**.

- Se a Folha 3 disser OK e a tela não mostrar a ação → o vídeo está errado.
- Se a ação aparecer fraca, atrasada ou escondida → o vídeo está errado.
- Zero ressalva. Zero “quase bom”.

A ferramenta já detecta as ações. O problema real é garantir que a detecção se transforme em animação clara e no tempo certo.

---

## 2. Contrato de escrita do roteiro

### 2.1 Uma frase = uma cena = uma ação principal

- Cada frase do `say` deve conter **no mínimo um verbo de ação visual**.
- Frases que só comentam são proibidas:
  - Ruim: “Foi um momento incrível.”
  - Ruim: “A situação piorou rapidamente.”
  - Ruim: “Ninguém esperava aquilo.”
- Se precisar de comentário, junte com ação:
  - Bom: “Foi um momento incrível e os soldados gritaram de vitória.”
  - Bom: “A situação piorou e os homens correram em pânico.”

### 2.2 Estrutura obrigatória de toda frase de ação

Toda frase de ação deve responder claramente:

| Pergunta     | O que escrever                          | Exemplo                          |
|--------------|-----------------------------------------|----------------------------------|
| Quem?        | Nome, cargo ou grupo                    | O fazendeiro / Os soldados       |
| O quê?       | Verbo de ação concreto                  | atirou / correram / desembarcou  |
| Com o quê?   | Objeto ou alvo                          | espingarda / praia / balão       |
| Onde?        | Lugar (quando relevante)                | na praia / no campo / no céu     |

**Exemplos bons:**
- “O fazendeiro pegou a espingarda e atirou no porco.”
- “A tropa desembarcou na praia correndo e gritando.”
- “O grande balão subiu no céu enquanto a multidão apontava.”
- “Os dois generais apertaram as mãos e fizeram as pazes.”
- “A gosma caiu no fogão quente e virou borracha firme.”

**Exemplos ruins (não passam):**
- “A batalha foi intensa.”
- “Eles resolveram o problema.”
- “O preço caiu.”
- “A notícia correu o mundo.”
- “O pânico tomou conta do acampamento.”

### 2.3 Verbos preferenciais (têm animação forte)

Use estes verbos sempre que possível. Eles já têm gesto + efeito + som bem resolvidos:

**Corpo**
correu, fugiu, pulou, caiu, ajoelhou, sentou, dormiu, gritou, chorou, riu, pensou, apontou, acenou, empurrar, socou, tomba, morreu, raspar

**Guerra e impacto**
atirou, disparou, explodiu, bombardeou, invadiu, desembarcou, marchou, rendeu-se, atacaram, batalha

**Processo e invenção**
misturou, mexeu, jogou, derramou, esquentou, ferveu, virou, endureceu, construiu, montou, examinou, escreveu, assinou, cavou

**Social**
conversaram, discutiram, brigaram, apertaram as mãos, abraçaram, entregou, pagou, vendeu, pediu, implorou, comemorou, dancou

**Movimento de objeto / veículo**
subiu, decolou, chegou, partiu, entrou no carro, dirigiu, lançou

---

## 3. Como forçar a ação a aparecer (quando o automático falha)

No `beats.json` da cena, use estes campos:

```json
{
  "say": "Os soldados correram em direção à praia.",
  "shot": "track",
  "batalha": true,
  "interacao": "empurrar",
  "acao": "correr",
  "who": ["SOL:0:angry", "SOL:1:determined"],
  "chega": true
}
```

### Campos mais importantes

| Campo          | Quando usar                                      | Efeito                                      |
|----------------|--------------------------------------------------|---------------------------------------------|
| `shot`         | Sempre que a ação precisar de espaço             | `track` (correndo), `crowd`, `reveal`, `group` |
| `batalha`      | Combate, tiros, explosão, tropa                  | Tropa dos dois lados + tiros + gente caindo |
| `interacao`    | Briga, abraço, entrega, empurrão, súplica        | Gestos físicos entre dois personagens       |
| `acao`         | Forçar família de animação                       | `correr`, `discutir`, `comemorar` etc.      |
| `chega`        | Alguém chega ou aparece                          | Personagem entra andando pela lateral       |
| `encena`       | Desligar a encenação automática (raro)           | `false`                                     |

---

## 4. Regras de ouro (matam 90% dos problemas)

1. **Negação não gera ação**  
   “Ninguém atirou” → proibido aparecer tiro.  
   “Sem dar um único tiro” → não gera animação de tiro.

2. **Expressão idiomática não gera ação literal**  
   “A notícia correu o mundo” → não põe gente correndo.  
   “O pânico tomou conta” → não põe gente bebendo.  
   “O preço caiu” → não põe objeto caindo.

3. **Ação no final da frase precisa começar antes**  
   Se o verbo importante está no final da frase, o objeto ou a pose deve começar a aparecer alguns frames antes da palavra.

4. **Máximo 4 personagens principais por cena fechada**  
   Mais que isso a ação some ou fica confusa.

5. **Plano aberto obrigatório em momentos de impacto**  
   Batalha, multidão, desembarque, explosão, comemoração grande → use `shot: "crowd"` ou `"reveal"` + `"batalha": true`.

6. **Objeto herói com close**  
   Todo vídeo precisa de um objeto herói com close no começo e no fim.

7. **Uma ação por frase**  
   Se a frase tiver duas ações fortes, divida em duas cenas.

---

## 5. Verificação obrigatória (ordem fixa)

Nunca pule etapas.

1. Rode `python3 mkvideo.py <id>`
2. Abra `stories/<id>/folha3_acao.md`  
   → Zero linha com “FALTA”
3. Gere storyboard + grade de ações
4. **Olhe a `grade_acoes.jpg` quadro por quadro**  
   A ação escrita embaixo do quadro tem que estar acontecendo na imagem no instante certo.
5. Escreva `stories/<id>/revisao_storyboard.md` com uma linha por frase:
   ```
   b0: OK - soldados correndo pela praia com poeira nos pés
   b1: CORRIGIDO - tiro sem clarão → adicionei "atirou" + who com rifle
   b2: OK - generais apertando as mãos com brilho
   ```
6. Só depois rode `./aprovar_storyboard.sh <id>`

**Regra de ouro da revisão:**  
Se você precisar “imaginar” a ação para entender o quadro → a ação não está clara o suficiente. Corrija.

---

## 6. O que a Folha 3 ainda não garante sozinha

A Folha 3 confirma que a ação foi **detectada**.  
Ela não garante:

- Intensidade da animação (soco fraco vs soco forte)
- Timing perfeito (ação que começa tarde demais)
- Oclusão (objeto ou personagem na frente da câmera)
- Escala errada do objeto
- Personagem cortado ou pose estranha

Por isso a **grade de ações + revisão escrita frase por frase** continua obrigatória.  
A Folha 3 é o mínimo. A revisão visual é o gate real.

---

## 7. Checklist rápido antes de aprovar qualquer vídeo

- [ ] Toda frase tem pelo menos um verbo de ação visual
- [ ] Folha 3 com zero “FALTA”
- [ ] Grade de ações mostra a ação acontecendo em cada quadro
- [ ] Nenhuma ação importante está escondida, atrasada ou fraca
- [ ] Planos abertos nos momentos de impacto
- [ ] Objeto herói aparece com close
- [ ] Revisão escrita (`revisao_storyboard.md`) feita frase por frase
- [ ] Zero ressalva

---

## 8. Frase-resumo (cole na parede)

**Escreva a frase como se estivesse descrevendo exatamente o que a câmera precisa mostrar.  
Se a frase for ambígua, a animação será ambígua.**

---

**Fim do documento.**  
Use este arquivo como regra mestre em todas as sessões (principal, A e B).  
Sempre que houver dúvida entre “catalogou” e “apareceu na tela”, este documento manda.
