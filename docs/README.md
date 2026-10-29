# Estrutura de Documentacao

Este diretorio traz um esqueleto padrao para documentacao tecnica e operacional.

## Pastas

- `00_visao_geral`: objetivo, escopo e contexto.
- `01_requisitos`: requisitos funcionais e nao funcionais.
- `02_arquitetura`: diagramas, decisoes e padroes arquiteturais.
- `03_implementacao`: detalhes tecnicos de execucao e integracao.
- `04_operacao`: runbooks, rotinas e procedimentos operacionais.
- `05_progresso`: status macro, checkpoints e historico de sessao.
- `05_progresso/historico`: diario de sessao e historico detalhado.
- `06_literatura`: acervo da obra, esbocos e referencias do autor.

## Uso com skills

- A skill `documentar-sessao` pode registrar automaticamente resumos em `05_progresso/historico`.
- Ajuste caminho e formato no endpoint operacional de sessao.
