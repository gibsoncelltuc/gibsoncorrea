# Biblioteca de animação — personagens, expressões e ambiente

## Regra geral

Usar animação 2D cut-out por partes, em planos 2D posicionados dentro do mundo 3D ou como billboards orientados à câmera. Criar rig simples e reutilizável. Preferir poses legíveis a movimentos complexos que não acrescentam informação.

## Partes mínimas de um rig

- cabeça;
- olhos esquerdo/direito e pupilas independentes;
- sobrancelhas independentes;
- boca (pelo menos 6 shapes);
- tronco;
- ombro, braço, antebraço e mão de cada lado;
- quadril, coxa, perna e pé de cada lado;
- cabelo/chapéu e acessórios separados;
- ponto de pivô por articulação.

Manter nomes estáveis nos assets: `head`, `eye_L`, `eye_R`, `pupil_L`, `pupil_R`, `brow_L`, `brow_R`, `mouth`, `torso`, `upper_arm_L`, `forearm_L`, `hand_L`, etc.

## Expressões faciais

| Estado | Olhos | Sobrancelhas | Boca | Ação corporal |
|---|---|---|---|---|
| Neutro | abertos, pupila centrada | relaxadas | linha curta | respiração leve |
| Curioso | olhos ligeiramente maiores | uma levantada | pequeno “o” | cabeça inclina 5–10° |
| Cético | pálpebra baixa | assimétricas | linha lateral | inclinação curta para trás |
| Confiante | foco estável | levemente inclinadas | sorriso discreto | peito aberto |
| Zombaria | olhos semicerrados | arqueadas | sorriso de canto | ombro relaxado |
| Surpresa | olhos grandes | elevadas | círculo aberto | recuo curto |
| Medo | pupilas menores/abertas | altas e juntas | tremor/aberta | corpo encolhe |
| Pânico | olhos amplos | altas | boca grande | recuo + braços levantados |
| Frustração | olhar fixo | juntas | boca pressionada | peso em um pé |
| Alívio | olhos relaxam/fecham | soltas | sorriso | ombros descem |
| Satisfação | olhos focados | relaxadas | sorriso pequeno | pose firme |
| Confusão | olhar deslocado | uma levantada | boca torta | cabeça inclina |

Implementar como estados com transições de 4–12 frames; não trocar instantaneamente, exceto em gag cômica deliberada.

## Biblioteca de ações

### Idle / vida constante

- Respiração: escala do torso ±1–2% em ciclo de 2,5–4 s.
- Head bob: deslocamento vertical pequeno em ciclo diferente da respiração.
- Blink: fechar por 2–4 frames, intervalo variável e não perfeitamente periódico.
- Gaze shift: pupilas mudam para objeto/personagem antes da cabeça; atraso de 2–4 frames.
- Weight shift: alternar centro de massa lentamente.
- Micro-gesture: dedos/mão/ombro em repouso, quando legível.

### Reações

- Surprise pop: antecipação de 2–3 frames, escala 1.05–1.10, retorno com overshoot leve.
- Flinch: cabeça e tronco recuam em 3–6 frames, settle em 6–10.
- Sigh: peito sobe, pausa curta, desce; ombros acompanham.
- Look-at: pupilas primeiro, cabeça depois, tronco por último.
- Double-take: olhar para um lado, pausa, voltar rapidamente.
- Shrug: ombros sobem, mãos abrem, cabeça inclina.
- Point: braço antecipa, mão aponta, foco ocular acompanha o objeto.
- Step-back: perna inicia, quadril desloca, cabeça mantém foco no evento.

### Locomoção

- Walk cycle 8–12 poses-chave por ciclo; pés não deslizam.
- Run cycle com inclinação do torso para frente e amplitude maior.
- Sneak: joelhos flexionados, amplitude curta, cabeça procura em dois eixos.
- Stop: foot plant, compressão curta, torso settle.
- Turn: olhar → cabeça → ombro → quadril, salvo reação instantânea.

### Interação com objeto

- Reach: mão se aproxima em arco; cotovelo lidera; dedos fecham no contato.
- Grab: registrar frame de contato; objeto passa a seguir o ponto de mão sem salto.
- Push/pull: inclinação de corpo e reação do objeto; sincronizar som no frame do contato.
- Drop: mão abre, objeto acelera por gravidade; squash/impacto moderado.
- Inspect: cabeça e olho alternam foco entre dois detalhes.
- Demonstrate: mão apresenta objeto na área limpa do quadro; câmera ou luz reforça o foco.

## Princípios de animação

- Antecipação: 2–6 frames em ações rápidas, mais em movimentos pesados.
- Ação principal: clara, com arco e leitura de silhueta.
- Follow-through: partes leves continuam depois do corpo (cabelo, chapéu, roupa, acessório).
- Settle: 4–12 frames dependendo do peso.
- Squash/stretch discreto; não deformar tanto que perca o design.
- Usar curvas ease-in/ease-out, cubic bezier ou spring com overshoot controlado.
- Evitar sincronizar todos os personagens ao mesmo ciclo. Cada um precisa de fase e personalidade próprias.

## Ambiente vivo

Ativar apenas 2–4 camadas secundárias por plano, escolhidas conforme o contexto:
- nuvens/névoa deslocando-se lentamente;
- água com deslocamento de textura/procedural waves;
- fogo/lâmpadas com flicker de baixa amplitude;
- bandeiras, folhas, cordas e tecidos com oscilação;
- poeira/partículas em volume com movimento lento;
- fumaça com drift e dissipação;
- insetos/pontos de luz;
- sombras de vegetação, reflexos e luz de janela;
- objetos mecânicos com ciclo curto quando a história exigir.

Tudo deve ser determinístico por frame. Sem ruído temporal não semeado.
