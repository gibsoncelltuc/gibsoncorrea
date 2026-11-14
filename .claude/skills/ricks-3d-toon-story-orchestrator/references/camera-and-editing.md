# Direção de câmera e montagem

## Linguagem de câmera

A câmera deve dar a sensação de passeio pelo cenário, não de apresentação estática. Usar trajetórias curtas, suaves e com intenção: revelar espaço, aproximar a informação, conectar personagens ou mostrar causa e efeito.

### Movimentos recomendados

| Movimento | Uso | Duração inicial |
|---|---|---:|
| Establishing glide | Mostrar lugar e escala sem parar a narração | 1.5–3 s |
| Lateral tracking | Acompanhar personagem/objeto em movimento | 1–3 s |
| Slow push-in | Aumentar importância/curiosidade | 0.8–2.5 s |
| Pull-back reveal | Revelar dimensão, contexto ou consequência | 0.8–2 s |
| Parallax drift | Dar profundidade a diálogo/exposição | 2–4 s |
| Over-the-shoulder | Conectar personagem e mecanismo/objeto | 1.5–3 s |
| Reaction close-up | Ler ceticismo, surpresa ou medo | 0.7–1.8 s |
| Top-down explain | Explicar processo, percurso, mapa ou mecanismo | 1.5–4 s |
| Mini-orbit | Mostrar volume de objeto importante | 1–2.5 s |
| Whip/punch-in | Acento cômico ou revelação pontual | 4–10 frames |

Estas são faixas de direção propostas, não medições do canal de referência.

## Lentes e distância

- Padrão: perspectiva moderada, equivalente aproximado a 28–40 mm em full frame.
- Close de personagem: 45–65 mm equivalente para reduzir distorção facial.
- Plano amplo: 24–30 mm equivalente com cuidado para não deformar personagens nas bordas.
- DOF sutil; manter rosto, objeto de ação e legenda em foco legível. Evitar blur excessivo.

## Ritmo de montagem

- Fazer a imagem mudar quando uma nova informação chega.
- Em fala rápida, planos podem durar 1.5–4 s, mas a câmera pode continuar se movendo dentro do plano.
- Close-ups de reação podem ser curtos; o payoff pode segurar mais tempo para o cérebro processar.
- Evitar jump cut gratuito a cada frase. Alternar escala, posição, direção do olhar e composição.
- Cortes em ação devem respeitar continuidade de direção e posição dos objetos.
- Transições invisíveis por movimento de câmera são preferíveis a transições decorativas.

## Shot design

Cada shot deve conter:

```json
{
  "id": "S03",
  "start": 12.0,
  "end": 16.5,
  "purpose": "introduzir o personagem cético",
  "set": "workshop_day",
  "camera": {"type": "push_in", "start": [0, 1.8, 8], "end": [0.2, 1.8, 6.8], "ease": "cubicOut"},
  "action": "skeptic_laughs",
  "expression": "smug",
  "environment_motion": ["dust_motes", "lamp_flicker"],
  "caption_words": ["That", "will", "never", "work."],
  "sfx": ["short_chuckle"],
  "music_cue": "continue_under_voice"
}
```

## Composição vertical

- Manter protagonista longe das bordas extremas.
- Reservar a faixa inferior para legendas e UI da plataforma.
- Não colocar detalhe importante atrás de legenda, ícones do YouTube ou cortes automáticos.
- No início, apresentar imediatamente um objeto/personagem legível; evitar plano amplo sem foco.

## Composição horizontal

- Abrir mais espaço lateral para ação e geografia.
- Usar movimentos de travelling e parallax de maneira mais longa.
- Manter a mesma escala relativa do rosto/objeto importante.

## Continuidade

- Guardar posição, orientação, olhar, mão que segura objeto, direção de movimento e posição da key light em cada corte.
- Não inverter a tela sem motivação.
- Se houver match cut, alinhar shape, posição, direção ou movimento.
- Usar cutaway para mostrar detalhe factual sem quebrar a lógica espacial.
