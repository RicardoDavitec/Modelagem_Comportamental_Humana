---
name: imprimir
description: >-
  Imprime arquivo (md, pdf, txt, docx, imagem) do WSL na impressora do
  Windows, inclusive compartilhada na rede (ex.: Xerox B210). Converte
  markdown para PDF antes de imprimir. Use em imprimir, print, mandar para
  a impressora, imprimir checklist. Nao use para exportar PDF sem imprimir.
argument-hint: "caminho do arquivo; opcional: nome da impressora"
---

# Skill: imprimir

Objetivo: imprimir um arquivo a partir do WSL na impressora do Windows
(local ou compartilhada na rede), com conversao automatica de Markdown
para PDF.

## Fluxo padrao (baixo custo de tokens)

1. Executar o script de apoio com o caminho informado pelo usuario:
   - `tools/imprimir/imprimir <arquivo>`
   - `tools/imprimir/imprimir -p "Xerox B210" <arquivo>` (impressora especifica)
2. Reportar apenas o resultado final: impressora usada e status do envio.
   Nao colar logs longos.

## Como funciona

- Markdown (`.md`) vira PDF temporario via `pandoc` (+ `weasyprint`);
  sem pandoc, imprime como texto puro.
- **PDF** imprime via **SumatraPDF** (`-print-to`), direto na impressora,
  sem depender de associacao de arquivos do Windows.
- Demais tipos (txt, docx, imagens): o PowerShell do Windows
  (`tools/imprimir/imprimir.ps1`) define a impressora alvo como padrao
  temporaria, dispara o verbo `Print` e restaura a padrao anterior.
- Autodeteccao: primeira impressora cujo nome contem "Xerox"
  (ajustavel com `IMPRESSORA_MATCH`); nesta estacao o `~/.bashrc` define
  `IMPRESSORA="Val"` (Canon, 172.21.200.22) como padrao.

## Pre-requisitos (verificar so em caso de erro)

- Impressora **adicionada no Windows** (Configuracoes > Impressoras;
  compartilhamento de rede: `\\NOME-DO-PC\Xerox B210`, com o PC que
  compartilha ligado).
- Listar impressoras disponiveis: `tools/imprimir/imprimir --list`.
- `pandoc` + `weasyprint` no WSL (MD -> PDF) e **SumatraPDF** no Windows
  (PDF): ja instalados nesta estacao
  (`winget install SumatraPDF.SumatraPDF`).

## Variaveis suportadas

- `IMPRESSORA`: nome exato da impressora (equivale a `-p`).
- `IMPRESSORA_MATCH`: regex de autodeteccao (padrao `Xerox`).

## Criterio de conclusao

- Script retorna `OK: enviado para a fila de '<impressora>'`.

## Referencias

- Script CLI: [../../../tools/imprimir/imprimir](../../../tools/imprimir/imprimir)
- PowerShell: [../../../tools/imprimir/imprimir.ps1](../../../tools/imprimir/imprimir.ps1)
