# Benchmarks externos

Esta pasta é reservada para clones de referência. O benchmark recomendado está descrito em `../references/benchmark-claude-animated-shorts.md`.

Não copie automaticamente o repositório para dentro do projeto de produção. Primeiro clone em sandbox isolado, confira licença, commit, scripts, dependências e ativos. Não execute o código de terceiros antes de auditar.

Comando manual:

```bash
git clone --depth 1 https://github.com/mromidev/claude-animated-shorts.git external/claude-animated-shorts
cd external/claude-animated-shorts
git rev-parse HEAD
```

Guarde o hash retornado em `benchmark-lock.json`. Nunca registrar `main` como se fosse versão imutável.
