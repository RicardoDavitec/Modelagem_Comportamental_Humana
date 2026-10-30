# Subagentes deste repositório

`.cursor/agents` aponta para `.github/agents`. Arquivos daqui vencem `~/.cursor/agents/` com o mesmo `name`.

| Arquivo | Papel |
|---------|--------|
| `orquestrador-hexagonal.agent.md` | Fluxo hexagonal, com delegação |
| `revisor-arquitetura-hexagonal.agent.md` | Revisão de portas e adaptadores |
| `analista-incidentes-integracao.agent.md` | Twilio, Selenium, planilhas, envio |
| `operador-entrega-controlada.agent.md` | Ajuste mínimo e entrega verificável |
| `redator-ricardizar.md` | Voz autoral (skill `ricardizar`) |
| `redator-ricardo-david.md` | Voz autoral (skill `estilo-ricardo-david`) |
| `pmf-repo.md` | AGENTS.md do git root em foco |
| `pmf-backend.md` / `pmf-web.md` / `pmf-mobile.md` | Módulo `apps/<nome>` no monorepo PMF |

Agentes `glpi-*` do bot_pan não foram importados.

Os `.agent.md` locais foram mantidos: trazem `tools` e delegação. As cópias homônimas do bot_pan não substituem esses arquivos.
