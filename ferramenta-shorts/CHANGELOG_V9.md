# Ferramenta Shorts v9 — Motor Multi-Ação + Engenharia Reversa @RicksClips3000

## O que foi corrigido e atualizado na v9

1. **Fim da sobrescrita de ações (`_MA` mergeActor em `mkvideo.py`):**
   - Substituído `Object.assign` destrutivo por `_MA()`, que mescla `gests`, `poses`, `moves`, `inters`, `yFns` e `over` sem apagar ações anteriores na mesma frase.
   - `interacao: "apertar"` não trava mais `reach` até o fim da cena quando há ações seguintes (ex.: "apertaram as mãos, riram e comemoraram").
2. **Suporte real a 3–4+ ações encadeadas na mesma frase (`mkvideo.py` + `web/runtime.js`):**
   - Antecipação calibrada de 8 frames (`WS(wi) - 8`) para o pico visual bater exatamente na palavra falada.
   - Janela mínima garantida por gesto (`Math.max(WS(wi) + 14, ...)`) para evitar ações esmagadas em <6 frames.
   - Teto de palavras-chave elevado (`kfx < 7`) e deduplicação inteligente (permite repetir a mesma família de ação se separada por >= 4 palavras).
   - Múltiplas mudanças de expressão facial por frase (`_wxs`) e até 3 gestos de atuação por frase em `web/acting.js`.
3. **Roteamento inteligente de sujeito vs. alvo (`mkvideo.py`):**
   - Em cenas de conflito com 2 personagens (soco, golpe, empurrão), o personagem alvo (`acts[1]`) recebe o recuo (`stagger`) e a queda (`fall`), em vez de `acts[0]` socar a si mesmo e cair.
   - Ações coletivas (`riram`, `comemoraram`, `gritaram`, `renderam-se`) animam ambos os personagens.
   - Cenas com `interacao: "empurrar"` + corrida não são mais sequestradas pelo modo `shot: "track"`, permitindo empurrão físico sincronizado na palavra.
4. **Física corporal expressiva e Action Punch-In (`web/runtime.js`):**
   - Gestos de ação agora movem o corpo inteiro (inclinação de tronco, avanço/recuo, salto em comemoração, recuo de disparo de rifle).
   - `opts.aim` funciona para qualquer soldado armado com mira antecipada (16 frames) e sem apagar o rifle em gestos compatíveis.
   - Micro zoom-in dinâmico (`S.punches`) sincronizado com picos de impacto (tiro, soco, empurrão, explosão) e proteção contra corte de detalhe (`_d`) durante tiros.
5. **Aproximação visual ao estilo `@RicksClips3000` (`web/toonbase.js`):**
   - Contorno caligráfico da cabeça ajustado para razão fino/grosso ~3.0× (`k = 0.68`) e tinta profunda `#16121A`.
   - Gestos bi-manuais de maior amplitude com overshoot (`punch`, `push`, `throw`, `hammer`, `reach`, `stir`).
   - Efeito cartunesco de fúria (linhas de tensão vermelhas na têmpora) em expressões `angry`/`shout`.
6. **Compatibilidade Python 3.10–3.12 e auditoria anti-falso-positivo (`verificar_execucao.py`):**
   - Corrigida f-string incompatível com Python 3.11 em `mkvideo.py`.
   - `verificar_execucao.py` agora acusa conflitos de sobrescrita de `gests`.
