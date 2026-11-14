# Benchmark: Claude Animated Shorts — status
**Não auditado e não integrado.** Tentativa de acesso a `github.com/mromidev/claude-animated-shorts` pelo ambiente de execução retornou HTTP 403 (política de rede do sandbox: o acesso ao GitHub está restrito a repositórios da sessão). Pela regra do módulo (`references/benchmark-claude-animated-shorts.md`), nada foi clonado, executado ou copiado, e **nenhum commit hash foi registrado** (nada a travar em `benchmark-lock.json`).
| Recurso | Upstream | Implementação própria | Decisão |
|---|---|---|---|
| Todos | não auditado | arquitetura própria (Remotion + R3F, rig 2D em mundo 3D toon, áudio sintetizado, QA próprio) | **adiado** — rever quando houver acesso à rede/repo |
Como continuar: clonar em `external/claude-animated-shorts/`, ler README/SKILL/LICENSE, auditar scripts/dependências, comparar determinismo e tempo de render, registrar hash e decisões nesta tabela.
