---
name: pmf-repo
description: >-
  Carrega o AGENTS.md do git root em foco (Bot_Pan ou samu-operacional) e
  qualquer subagente em .cursor/agents/ desse repo. Use ao delegar trabalho
  no produto, iniciar sessao no monorepo, ou quando o usuario falar em agente
  do projeto. Override do repositorio vence o agente pessoal.
---

Voce e o agente do **repositorio em foco**, nao de um template generico.

1. Rode `python3 ~/.cursor/skills/_pmf/resolve.py --agent` (e `--agent <modulo>` se o trabalho for `apps/backend`, `apps/web` ou `apps/mobile`).
2. **Read** cada arquivo listado. `.cursor/agents/*.md` do repo vence instrucoes pessoais com o mesmo nome.
3. Siga o `AGENTS.md` da raiz. Se houver `apps/<modulo>/AGENTS.md`, aplique as regras daquele modulo **alem** da raiz, sem misturar dominio SAMU com Bot_Pan.
4. Skills: despachar com `python3 ~/.cursor/skills/_pmf/resolve.py <nome>` e seguir o SKILL.md retornado. Nao usar o skill do outro produto quando o arquivo nao existir neste root.
5. Pedido no plural / workspace: `--all` e tratar cada git root isolado.
