---
name: revisar-docs
description: "Use para revisar e auditar a documentacao do Bot_Pan, incluindo estrutura de docs, links internos, consistencia de nomes e paginas sem indice."
argument-hint: "Informe o escopo da auditoria (ex: docs/, docs/03-compilacao, docs/08-setup)."
---

# Skill: revisar-docs

Executa auditoria da documentacao do Bot_Pan com relatorio objetivo e priorizacao por severidade.

## Contexto do Bot_Pan
- A documentacao deve cobrir arquitetura, cronograma, decisao, checklist e guias por camadas
- A estrutura precisa ficar pronta para crescimento sem perder rastreabilidade
- A auditoria deve apontar inconsistencias de forma clara e acionavel

## Modo eficiente
- Escopo padrao: `docs/` ou subpasta indicada
- Rodar verificacoes em lote e responder com contagens e caminhos
- Fazer 1 pergunta de acao: corrigir automaticamente problemas leves/importantes ou nao

## Fluxo minimo obrigatorio
1. Verificar arquivos indevidos na raiz de `docs/`.
2. Verificar pastas sem `README.md` ou arquivo de indice equivalente.
3. Verificar historicos sem data, nomes fora do padrao e links internos quebrados.
4. Classificar severidade em critico, importante e leve.
5. Gerar relatorio de auditoria em `docs/05-gestao-projeto/geral/`.
6. Oferecer correcoes para itens leves/importantes.
7. Se corrigir, sugerir commit no formato obrigatorio: `<emoji> <tipo>(<escopo>): <mensagem-curta-pt-br-sem-acentos>_DD_MM_YY-hh_mm`.

## Regras essenciais
- Nao usar este skill para criar docs novas de progresso ou log de tentativa.
- Nao ignorar links quebrados.
- Nao fazer alteracoes amplas sem confirmar o escopo.

## Saida padrao esperada
- Resultado objetivo da auditoria
- Estado atual do plano/checklist de documentos
- Proximo item de correcao ou validacao
- Ideias extras apenas se nao desviarem do fluxo principal

## Ordem fixa de saida
1. Resultado objetivo
2. Estado do plano/checklist
3. Proximo passo
4. Extras opcionais alinhados ao plano
