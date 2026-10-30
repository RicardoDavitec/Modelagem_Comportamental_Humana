---
name: build-backend
description: >-
  Build, validacao e troubleshooting do backend NestJS/Prisma do repositorio
  em foco. Use em build backend, nest, prisma, health da API.
argument-hint: "Ambiente e objetivo."
---

# Skill: build-backend

Git root em foco. Nao misturar com web/mobile.

## Fluxo

1. Env do backend (`.env` / `.env.example` deste repo).
2. Se `schema.prisma` mudou: `npm run db:generate` se o script existir.
3. `npm run build:backend` (ou o script equivalente no `package.json` da raiz).
4. Health: ler porta no `AGENTS.md` deste repo (SAMU 3700; Bot_Pan conforme o produto — **nao** assumir a porta do irmao).
   `curl -fsS http://localhost:<porta>/health`
5. Falha: se existir skill `registrar-tentativa`, usa-la; senao registrar em `docs/03-compilacao/` **ou** `docs/03_implementacao/compilacao/` (o que existir).

Saida: resultado, estado do plano vigente, proximo passo.
