---
name: deploy-web
description: "Use para deploy, publicação e troubleshooting do web do Bot_Pan."
argument-hint: "Informe ambiente, destino e objetivo do deploy web."
---

# Skill: deploy-web

Executa deploy do web do Bot_Pan com foco em previsibilidade, env pública e integração com backend.

## Quando usar
- Publicar o painel web
- Validar build e variáveis públicas
- Checar integração com API
- Registrar falhas de deploy do frontend web

## Fluxo recomendado
1. Validar env do web.
2. Executar build.
3. Conferir integração com backend.
4. Validar publicação no destino.
5. Registrar tentativa técnica se houver erro.
6. Ajustar docs de operação quando necessário.

## Regras
- Não misturar com backend ou mobile.
- Se o problema for de erro ou falha, usar `registrar-tentativa`.
- Manter o processo simples e repetível.

## Saida padrao esperada
- Resultado objetivo da acao
- Estado atual do plano/checklist
- Proximo item do plano
- Ideias extras apenas se nao desviarem do fluxo principal

## Ordem fixa de saida
1. Resultado objetivo
2. Estado do plano/checklist
3. Proximo passo
4. Extras opcionais alinhados ao plano
