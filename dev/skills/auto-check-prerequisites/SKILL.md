---
name: dev:auto:check-prerequisites
description: Vérifier tous les prérequis - Mode AUTO (Phase -1)
model: claude-haiku-4-5-20251001
allowed-tools: [Bash]
version: 1.0.0
license: MIT
---

# Objectif

Vérifier que TOUS les prérequis système sont présents avant de lancer le workflow automatisé.

Exit code 1 si quelque chose manque.

# Vérifications

- gh CLI installé et authentifié
- jq disponible
- git disponible

# Exit avec erreur si manquant

Message d'erreur détaillé avec instructions d'installation.
