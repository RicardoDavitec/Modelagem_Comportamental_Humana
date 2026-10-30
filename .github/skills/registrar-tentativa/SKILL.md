---
name: registrar-tentativa
description: "Use para registrar tentativa tecnica, falha, erro ou acerto parcial de build, deploy, configuracao ou integracao no Bot_Pan. Aceite pedidos curtos como 'registrar tentativa' e direcione para o log tecnico certo em docs/03-compilacao/."
argument-hint: "Informe ferramenta, comando, erro exato, contexto, pasta alvo e resultado (ex: build backend, deploy frontend, ssh, proxy, DNS)."
---

# Skill: registrar-tentativa

Registra tentativas tecnicas do Bot_Pan com foco em rastreabilidade, comparacao de falhas e reaproveitamento de solucoes.

## Contexto do Bot_Pan
- O projeto novo deve herdar o aprendizado util de BotPanLea e simp_bot_pan
- Cada falha relevante deve virar referencia futura em docs de compilacao ou operacao
- A tentativa deve ser documentada com causa, efeito, solucao e proximo passo

## Modo eficiente
- Se a solicitacao for vaga, fazer no maximo 2 perguntas curtas: comando executado e mensagem de erro
- Se o pedido vier apenas como 'registrar tentativa', inferir o contexto recente e escolher o log tecnico mais provavel
- Manter checklist e todo list atualizados sempre que a tentativa alterar o estado do plano
- Usar o plano documentado como direcao principal; nao desviar para novos caminhos antes de registrar o proximo passo
- Nao repetir a politica completa na resposta
- Reportar saida curta com arquivo, indice e status

## Ciclo de tentativa obrigatorio
- Tratar o trabalho como uma sequencia de tentativas ate resolver ou isolar o bloqueio real
- Registrar cada tentativa frustrada com causa, efeito e pista obtida
- Registrar a solucao encontrada separadamente, deixando claro o que mudou para funcionar
- Se uma tentativa falhar e a proxima depender do novo dado, atualizar o registro antes de seguir

## Saida padrao esperada
- O que foi tentado
- O que falhou
- O que mudou
- Proximo item do plano ou checklist
- So depois disso, alternativas de continuidade se ainda forem uteis

## Ordem fixa de saida
1. Tentativa executada
2. Falha ou resultado observado
3. Mudanca aplicada
4. Proximo item do plano/checklist
5. Alternativas adicionais apenas se estiverem alinhadas ao plano

## Como interpretar o pedido
- Se o usuario disser apenas 'registrar tentativa', buscar o contexto recente e decidir se a saida deve ir para build, deploy, configuracao ou integracao
- Se o foco for erro de compilacao, priorizar docs/03-compilacao/problemas-e-solucoes/
- Se houver efeito funcional ou impacto em docs, registrar tambem a necessidade de atualizar o checklist

## Fluxo minimo obrigatorio
1. Identificar a tentativa e seu escopo.
2. Criar ou atualizar um arquivo de log de tentativa em `docs/03-compilacao/`.
3. Atualizar correlacao de tentativas se existir no projeto.
4. Se houve efeito funcional, sinalizar a necessidade de atualizar o checklist.
5. Versionar as mudancas em `docs/`.
6. Sugerir commit no formato obrigatorio: `<emoji> <tipo>(<escopo>): <mensagem-curta-pt-br-sem-acentos>_DD_MM_YY-hh_mm` e perguntar sobre push.

## Exemplos de leitura do pedido
- 'registrar tentativa' -> usar o contexto recente para localizar a falha e gravar em `docs/03-compilacao/problemas-e-solucoes/`
- 'registrar tentativa de build backend' -> criar/atualizar o relato do build do backend com causa, efeito e solucao
- 'registrar tentativa de deploy frontend' -> documentar o deploy e o erro/resultado em `docs/03-compilacao/`
- 'registrar tentativa ssh' -> registrar o problema de acesso e os comandos/testes executados
- 'registrar tentativas frustradas' -> listar as falhas em ordem e a solucao final encontrada

## Regras essenciais
- Nao usar este skill para resumo geral de progresso.
- Nao tratar como documentacao comum quando o foco for erro de build ou deploy.
- Registrar a causa raiz quando conhecida e separar sintoma de solucao.
