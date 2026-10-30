---
name: empacotar-apk
description: >-
  Alias de build-mobile (APK no WSL, adb no PowerShell). Use em empacotar APK.
argument-hint: "Variante se o repo tiver."
---

# Skill: empacotar-apk

Seguir integralmente `build-mobile`.

- Gerar no WSL com o script/npm **deste** clone.
- Entregar `adb install -r` com caminho Windows.
- Nao instalar via adb no WSL.
- Keystore: pasta `apps/mobile/signing/` (ou a que o `app.json` apontar) **deste** repo. Nao reusar `Chave_Vitaguard` em package SAMU nem o contrario.
