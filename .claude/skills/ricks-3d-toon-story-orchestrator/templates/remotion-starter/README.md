# Remotion + Three.js starter

Este starter é um ponto de partida didático: um ambiente 3D simples, personagem 2D cut-out construído por malhas/planos, câmera deslocando-se por frame e uma legenda de demonstração. Substituir o personagem, o set, a timeline e a legenda por assets e dados originais do episódio.

## Requisitos

- Node.js LTS compatível com a versão atual do Remotion.
- Chromium/WebGL suportado no ambiente de render.
- FFmpeg para montagem/mixagem final (não necessário para abrir a prévia).

## Instalar e executar

```bash
npm install
npm run studio
```

Para renderizar:

```bash
npm run render
```

## Notas

- O exemplo foi entregue como código-fonte de referência; não foi executado/renderizado nesta sessão, pois não foram instaladas as dependências Node nem configurado um ambiente Chromium/WebGL neste runtime.
- As animações devem continuar sendo derivadas de `useCurrentFrame()`. Não substituir por `useFrame()` com relógio independente ou timers.
- O exemplo usa formas geométricas simples; para produção, separar o rig em módulos, implementar expressões faciais, props, interações de mão/objeto, legendas sincronizadas por word timings e audio stems.
- Conferir a documentação da versão que `npm install` efetivamente resolver antes de ampliar o projeto.
