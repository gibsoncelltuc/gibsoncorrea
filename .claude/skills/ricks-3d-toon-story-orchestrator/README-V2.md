# Ricks 3D Toon Story Orchestrator — V2

**Versão 2.0 — 14/11/2026**

Skill de orquestração para uma linha de produção audiovisual reutilizável, com animação procedural por código, personagens e ambientes próprios, direção de câmera, roteiro, áudio, legendas, render e QA.

## O que mudou da V1 para V2

- Auditoria crítica e integração opcional do `mromidev/claude-animated-shorts`.
- Scorecard com pesos, gates críticos e evidências de aprovação.
- Motor long-form separado para 3, 5 e 10 minutos sem duplicar a engine visual.
- Biblioteca persistente de personagens, rigs, expressões, movimentos, cenários, props, materiais, câmeras e áudio.
- Contratos de continuidade, cache, render segmentado e retomada de render.
- Perfil pt-BR para pronúncia, direção vocal, TTS e legendas.
- Requisitos de segurança, licença e provenance de assets.
- Critérios de conclusão que impedem declarar render pronto sem render real.

## Instalação

- Claude Code: copiar a pasta `ricks-3d-toon-story-orchestrator/` para `~/.claude/skills/` ou `.claude/skills/` no projeto.
- Claude.ai: compactar a pasta da skill e fazer upload em Settings → Capabilities/Features → Skills (a interface pode variar).
- O benchmark externo é opcional e deve ser clonado/auditado separadamente conforme `references/benchmark-claude-animated-shorts.md`.

## Prompt inicial recomendado

Ver `PROMPT-EXECUCAO-V2.md`.

## Limite honesto

A V2 melhora substancialmente as especificações e controles, mas não é prova de que o sistema já produziu um episódio equivalente ou superior ao canal de referência. Isso só pode ser validado após instalar dependências, produzir um episódio-piloto, renderizar e avaliar o resultado com o scorecard.
