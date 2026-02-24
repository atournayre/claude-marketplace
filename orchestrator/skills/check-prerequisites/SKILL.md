---
name: orchestrator:check-prerequisites
description: Vérifie tous les prérequis système avant de lancer un workflow automatique (gh CLI, jq, git). Exit code 1 si un prérequis manque.
model: haiku
allowed-tools: [Bash]
version: 1.0.0
license: MIT
---

# orchestrator:check-prerequisites

Vérification des prérequis système avant le workflow automatique. Mode fail-fast.

## Instructions à Exécuter

### 1. Vérifier les outils système

```bash
# gh CLI
if ! command -v gh &> /dev/null; then
    echo "PREREQUIS MANQUANT : gh CLI"
    echo "Installe : https://github.com/cli/cli"
    exit 1
fi

# gh authentifié
if ! gh auth status &> /dev/null; then
    echo "PREREQUIS MANQUANT : gh CLI non authentifié"
    echo "Authentifie : gh auth login"
    exit 1
fi

# jq
if ! command -v jq &> /dev/null; then
    echo "PREREQUIS MANQUANT : jq"
    echo "Installe : apt-get install jq (Linux) ou brew install jq (macOS)"
    exit 1
fi

# git
if ! command -v git &> /dev/null; then
    echo "PREREQUIS MANQUANT : git"
    exit 1
fi
```

### 2. Afficher le succès

```
Tous les prérequis sont présents

Outils vérifiés :
  gh CLI authentifiée
  jq disponible
  git disponible
```

## Règles

- Exit 1 si prérequis manquant
- Messages d'erreur clairs avec instructions d'installation
- Pas d'interaction : fail fast
- Rapide : vérifications simples et directes
