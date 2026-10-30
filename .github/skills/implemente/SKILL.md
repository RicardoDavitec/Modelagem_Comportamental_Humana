---
name: implemente
description: >-
  Executa planos no modelo documente-o-plano (fases S e tarefas P, inclusive
  prefixos PF/CO/SL/RF). Use quando o usuario pedir implemente, implementar o plano,
  execute o plano, seguir o skill Implemente, ou implementar a partir de Sn.Pm.
argument-hint: "Codigo inicial opcional (ex: PF0.P2). Vazio = primeiro P aberto do plano ativo."
---

# Skill: Implemente

Espelho do skill `implemente` do `samu-operacional`, adaptado aos caminhos do Bot_Pan.

Implementa o plano vigente em `docs/05_progresso/planos_ativos/` (índice `README.md`).
Planos no formato da skill `documente-o-plano` (checklist `- [ ]`/`[~]`/`[x]` + `<!-- glpi: ... -->`).

## Diretivas (verbatim)

execute todos o "P" de cada "S", fazendo commit a o final de cada "P"
Ao final de cada "S" rebuild local (build-backend, build-web, build-mobile), teste.
Ao final dos testes, documente correções, encerre a sessão, commit e push.
Up de APK aqui (build-mobile / adb PowerShell). Up Docker no servidor SSH após push daqui e pull de lá.
Onde  "P" são passos ou tarefas e "S" são sessões ou semanas.

## Equivalência de códigos

| Papel | Códigos |
|-------|---------|
| **S** (fase / sessão / semana) | `PF0`, `CO1`, `SL2`, `RF3`, … — item pai no organograma |
| **P** (passo / tarefa) | `PF0.P2`, `CO3.P5`, … |

Um extras `E1` no plano trata-se como **P** se tiver critério de aceite (commit ao final).

## Antes de começar

1. Ler `docs/05_progresso/planos_ativos/README.md` e o plano da linha pedida.
2. Ler RN/anexo ligados à fase (`docs/01_requisito/`, `planos_ativos/anexos/`).
3. Ponto de partida: argumento `Sn.Pm` **ou** o primeiro P `- [ ]` da fase S `[~]`/`[ ]`.
4. Não pular P. Não implementar a próxima S antes de fechar a S atual (rebuild local + teste + sessão + push).
5. Secrets / `.env` / keystore nunca no commit. `apps/mobile/android/` de prebuild local fora do commit.

## Loop de cada P

1. Marcar o P `[~]` com `real_start` (agora).
2. Implementar só o critério daquele P (anexo da S).
3. Teste mínimo do P (unitário / `curl` se for API). Falha → corrigir no mesmo P.
4. Atualizar o plano: P `[x]`, `real_end`, critério se mudou. S pai permanece `[~]` até todos os P.
5. Skill `commit` — **um commit por P**, mensagem cita o código (`PF0.P2`, …).
6. **Não** push no meio da S (salvo o usuário pedir). Push só no fechamento da S.

## Fechamento de cada S

Quando **todos** os P da S estiverem `[x]`:

### Nesta estação (WSL)

1. **Backend, web e banco (Prisma): testes no servidor, não aqui.** Aqui só `tsc`/build rápido para não commitar quebrado; sem Postgres local, sem suíte de integração. Entregar **commit + push** e um **script ou comando de build + up** (ex.: `scripts/deploy-<fase>.sh`: pull, build, `migrate deploy`, seed, `jest`, `up`, `/health`). O **usuário** faz pull e executa build/up/testes no servidor e devolve a saída. **Proibido nesta estação:** `docker compose up` / `build`.
2. **APK: build e instalação aqui** — skill `build-mobile` (WSL) + `adb install` no **PowerShell Windows**, se a S alterou o app.
3. Falha relatada do servidor → registrar em `docs/03-compilacao/` (skill `registrar-tentativa`) e corrigir **antes** de marcar a S `[x]`.
4. **Documente correções** — skill `documentar`: anexo da S, RN se a regra mudou, nota no plano.
5. Marcar S `[x]` com `real_end` (após o OK do servidor).
6. Skill `encerrar-sessao` (arquivo `SESSAO_*`).
7. Skill `commit` (docs da sessão + correções).
8. Skill `sincronize` (push `origin` GitHub + `gitness`). Gate: três SHA iguais.

### Up APK (esta estação)

Skill `build-mobile`: gera o APK no WSL e entrega `adb install` para o **PowerShell Windows**. Não instalar pelo WSL. Não subir APK no servidor (publicação pelo Centro de Distribuição do painel).

### Up Docker (servidor SSH)

Esta estação **não tem permissão** para subir containers nem SSH. Só **depois** do push; quem executa é o usuário (skill `deploy-backend`):

```text
ssh -p 22022 172.21.31.167 → cd <clone Bot_Pan> → git pull → docker compose up -d --build
```

Health na porta 3690 (não confundir com SAMU 3700). Sem pull da fonte já no Git, não rebuildar imagem. Não gravar backup no VM067. Não rsync da estação no lugar do `git pull`. Migration Prisma: `npx prisma migrate deploy` (ou `migrate reset` só se o plano declarar base de teste descartável) **dentro** do container no servidor.

## Ordem das S

Seguir o organograma. Próxima S só depois do fechamento acima.

## Relação com outras skills

| Skill | Quando |
|-------|--------|
| `documente-o-plano` | Criar/ajustar o plano; **não** substitui implementar |
| `oncoto-oncovo` | Descobrir S/P ativo se o argumento vier vazio |
| `commit` | Todo fim de P e o commit da sessão no fim da S |
| `build-backend` / `build-web` / `build-mobile` | Rebuild **local** no fim da S (APK + adb no Windows) |
| `documentar` | Correções pós-teste da S |
| `registrar-tentativa` | Falha de build/deploy |
| `encerrar-sessao` | Fim da S |
| `sincronize` | Push no **fim da S** (antes do docker no servidor) |
| `deploy-backend` | SSH + `git pull` + compose **no servidor**; nunca compose na estação |

GLPI (`glpi-retro-scan` / upsert): só se o usuário pedir.
