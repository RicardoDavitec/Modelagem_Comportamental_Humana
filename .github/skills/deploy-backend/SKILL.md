---
name: deploy-backend
description: >-
  Deploy do backend no servidor SSH: git pull no clone remoto e compose la.
  Esta estacao nao tem permissao para subir containers. Use em deploy backend,
  publicar API.
argument-hint: "Ambiente e tag/sha."
---

# Skill: deploy-backend

Git root em foco. Esta estação **não tem permissão** para `docker compose up`.

1. Confirmar que o código já está no Git (`sincronize` / push). Sem pull da fonte no servidor, não rebuildar.
2. SSH no servidor (`172.21.31.167`, porta conforme Infra — em geral `22022`).
3. No clone remoto deste produto: `git fetch` + `git pull` (branch vigente). **Não** rsync da estação no lugar do pull.
4. **No SSH**, subir a stack: `docker compose up -d --build` (ou script do `AGENTS.md`). Health em `3690`. Não gravar dump/tar de backup no VM067.
5. Health na porta **deste** produto. Não ocupar a porta do irmão (SAMU 3700 vs Bot_Pan 3690).
6. Falha: `registrar-tentativa` se existir.

Saida: resultado, plano vigente, proximo passo.
