---
name: build-web
description: >-
  Build e validacao do app web do repositorio em foco. Use em build web, vite,
  painel.
argument-hint: "Ambiente e objetivo."
---

# Skill: build-web

Git root em foco. Nao misturar com backend/mobile.

## Fluxo

1. Env publica (prefixos `VITE_` deste repo).
2. `npm run build:web` se existir; senao o script de build do workspace web.
3. Validar login/tela principal em dev se o usuario pedir (`npm run dev:web` ou equivalente).
4. Proxy `/api` → backend: porta **deste** `AGENTS.md`.
5. Falha: `registrar-tentativa` se o skill existir neste repo.

Saida: resultado, estado do plano vigente, proximo passo.
