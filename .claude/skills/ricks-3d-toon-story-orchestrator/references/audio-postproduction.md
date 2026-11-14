# Narração, legendas, sound design e mixagem

## Narração

- Uma voz narradora clara, enérgica e conversacional; velocidade alta, mas sem atropelar consoantes, números ou nomes.
- Preferir interpretação com intenção e microvariação, sem imitar a voz do canal ou de uma pessoa real.
- Marcar ênfase em verbos, objeto-chave, número e última frase.
- Usar pausas de 80–250 ms para separar ideia e permitir leitura visual; ajustar pelo take real.
- Trabalhar com gravação original ou serviço TTS licenciado e com permissão. Registrar a origem/licença da voz.

## Alinhamento palavra-a-palavra

- Gerar timestamps a partir do áudio final usando alinhador/forced alignment disponível ou transcrição manual assistida; conferir manualmente números, nomes e palavras curtas.
- Formato de entrada recomendado:

```json
{
  "words": [
    {"text": "He", "start": 0.12, "end": 0.28},
    {"text": "built", "start": 0.29, "end": 0.58},
    {"text": "a", "start": 0.59, "end": 0.66},
    {"text": "strange", "start": 0.67, "end": 1.02}
  ]
}
```

- Agrupar 1–2 palavras por cartão conforme velocidade e largura. Não usar divisão uniforme pelo texto: o tempo real das palavras varia.

## Legenda visual

- Branco ou quase branco, negrito, contorno escuro e sombra curta.
- Uma a duas palavras por tela; agrupar locuções curtas se melhorar a leitura.
- Destacar números e palavra central com acento de cor somente quando necessário.
- Manter altura e posição constantes. Evitar cobrir expressão facial e objeto demonstrativo.
- Fazer QA em celular/preview reduzido.

## Sound design

Criar uma lista de eventos com `time`, `asset`, `gain`, `pan`, `fadeIn`, `fadeOut`, `category` e `license`.

Categorias úteis:
- ambiente: vento, cidade, água, interior, multidão, madeira, máquina;
- personagem: passos, tecido, gesto, respiração/reações sutis;
- objeto: metal, papel, pedra, vidro, engrenagem, queda, impacto;
- transição: whoosh curto, riser discreto, hit leve;
- payoff: silêncio momentâneo, impacto, queda de ambiência ou acento musical.

Evitar encher cada movimento com whoosh. O efeito precisa confirmar a ação ou reforçar a história.

## Música

- Uma faixa principal por vídeo, ou pequenas variações temáticas por ato.
- Música instrumental licenciada/original; não usar faixa comercial sem direito.
- Reduzir a trilha sob a voz por automação ou sidechain; recuperar lentamente em pausas.
- O payoff pode receber acento ou breve retirada de música para dar contraste.

## Mixagem

Valores de partida sugeridos, não requisito oficial do YouTube:
- master estéreo com loudness integrado em torno de -14 a -16 LUFS;
- true peak não acima de -1 dBTP;
- voz clara e central; SFX sem mascarar consoantes;
- música normalmente 8–14 dB abaixo da voz durante fala, ajustada por espectro e arranjo;
- headroom suficiente nos stems; nada deve clipar.

Usar FFmpeg loudnorm/limiter como etapa final, mas não tentar consertar com limiter uma mixagem desequilibrada. Arquivar voz, música e SFX separados.

## Exportação

- Vídeo: H.264, perfil alto, pixel format yuv420p, fps constante, bitrate adequado à resolução e ao movimento.
- Áudio: AAC estéreo, 48 kHz; preservar master lossless no projeto.
- Entregar `.srt` separado e master sem legenda quando possível.
