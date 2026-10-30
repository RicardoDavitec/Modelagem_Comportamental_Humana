---
name: deploy-mobile
description: "Publica release do mobile Bot_Pan na Google Play Store (AAB vitaguard). Use para play store, release android, upload aab, eas submit ou nova versao do app."
argument-hint: "Informe versionCode alvo, track (interno/producao) e se ha keystore configurada."
---

# Skill: deploy-mobile

Publica nova versao do **VitaGuard** (`br.gov.sp.franca.vitaguard`) na Google Play Store.

## Escopo

| Artefato | Uso |
|----------|-----|
| `.aab` (App Bundle) | **Play Store** (obrigatorio) |
| `.apk` | Teste local via USB — skill `build-mobile`, nao Play |

## Pre-requisitos bloqueantes

1. **`versionCode` incrementado** em `apps/mobile/app.config.js` (maior que o ultimo publicado)
2. **Upload key** em `apps/mobile/android/keystore.properties` + arquivo `.keystore` local
3. Acesso ao **Google Play Console**

Sem keystore de release, o AAB sera assinado com debug e o Play pode rejeitar.

## Fluxo local (padrao deste ambiente)

### 1. Bump de versao

Editar `apps/mobile/app.config.js`:

- `expo.version` — ex.: `1.04`
- `expo.android.versionCode` — ex.: `11` (sempre +1)
- `expo.ios.buildNumber` — incrementar se houver release iOS

### 2. Gerar AAB no WSL

```bash
cd /home/wsl/projetos/Bot_Pan
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
./scripts/build-mobile-aab.sh vitaguard
```

Confirmar saida em `releases/mobile/aab/bot_pan_vitaguard_v*_vc*_*.aab`.

### 3. Upload Play Console (manual)

Entregar ao usuario:

1. Caminho absoluto do `.aab`
2. Link: https://play.google.com/console
3. Passos: track (teste interno ou producao) > criar versao > upload AAB > notas > enviar

### 4. Validacao

- `versionCode` no console = esperado
- App no dispositivo mostra `versionName` correta
- Fluxos criticos testados

## Fluxo EAS (alternativa)

```bash
cd apps/mobile
npx eas-cli login
npx eas-cli build --platform android --profile production --non-interactive
npx eas-cli submit --platform android --latest
```

Perfil `production` em `eas.json`: `APP_VARIANT=vitaguard`, `buildType: app-bundle`.

## Regras

- Play Store usa variante **`vitaguard`**, nao `paralelo` (QA).
- Nao commitar `.aab`, `.keystore` nem `keystore.properties`.
- Falha de assinatura: ver `TENTATIVA_2026-05-11_PLAYSTORE_SHA1_ASSINATURA_INVALIDA.md`.
- Falha de build: skill `registrar-tentativa`.

## Referencias

- `docs/06-guias-rapidos/mobile/PLAY_STORE_RELEASE.md`
- `scripts/build-mobile-aab.sh`
- `apps/mobile/eas.json`

## Ordem fixa de saida

1. **Resultado objetivo** — versao, versionCode, caminho do AAB, bloqueios (keystore/login)
2. **Proximo passo manual** — upload Play Console ou `eas submit`
3. **Estado do plano/checklist**
4. **Extras** — somente se alinhados ao release
