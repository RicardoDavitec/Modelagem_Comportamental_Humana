---
name: build-mobile
description: >-
  Gera APK release no WSL e entrega comando adb install para PowerShell no
  Windows. Use em build mobile, APK, instalar no celular.
argument-hint: "Variante se o repo tiver (paralelo/mainline) ou so gerar."
---

# Skill: build-mobile

APK no **WSL**; instalacao no **PowerShell Windows**. Nao `adb install` pelo WSL.

`tsc --noEmit`, `expo start` e `npm run android` **nao** substituem APK.

## Detectar variante e artefato

No git root:

- Se existir `npm run build:mobile:apk:paralelo` → padrao **paralelo** (coexiste com a loja). `mainline`/`vitaguard` so se pedido.
- Senao `npm run build:mobile:apk` ou `./scripts/build-mobile-apk.sh`.

```bash
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java-17-openjdk-amd64}"
# script ou npm do proprio repo
```

Artefato tipico:

```text
<git-root>/apps/mobile/android/app/build/outputs/apk/release/app-release.apk
```

Copia versionada (`releases/mobile/`) se o repo usar — gitignored, nao commitar.

## Apos o build (obrigatorio)

```bash
wslpath -w <caminho-apk>
```

Bloco para o usuario (PowerShell):

```powershell
adb devices
adb install -r "<caminho Windows do APK>"
```

Pacote: ler `app.json` / `applicationId` **deste** repo (`adb shell pm list packages | Select-String …`). Nao misturar keystore VitaGuard com package SAMU.

## Falha

`registrar-tentativa` se existir. Java 17 se Gradle reclamar. Nao commitar APK em `android/app/build/`.
