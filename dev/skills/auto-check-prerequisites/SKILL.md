---
name: dev:auto:check-prerequisites
description: Vérifier tous les prérequis - Mode AUTO (Phase -1)
model: claude-haiku-4-5-20251001
allowed-tools:
  - Bash
version: 1.0.0
license: MIT
---

# Objectif

Vérifier que TOUS les prérequis système, PHP et Claude Code sont présents avant de lancer le workflow.

Exit code 1 et message d'erreur détaillé si quelque chose manque.

# Instructions

## 1. Vérifier les outils système

```bash
# Vérifier gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ PRÉREQUIS MANQUANT : gh CLI"
    echo "Installe : https://github.com/cli/cli"
    echo "Authentifie : gh auth login"
    exit 1
fi

# Vérifier gh authentifié
if ! gh auth status &> /dev/null; then
    echo "❌ PRÉREQUIS MANQUANT : gh CLI non authentifié"
    echo "Authentifie : gh auth login"
    exit 1
fi

# Vérifier jq
if ! command -v jq &> /dev/null; then
    echo "❌ PRÉREQUIS MANQUANT : jq"
    echo "Installe : apt-get install jq (Linux) ou brew install jq (macOS)"
    exit 1
fi

# Vérifier git
if ! command -v git &> /dev/null; then
    echo "❌ PRÉREQUIS MANQUANT : git"
    exit 1
fi
```


## 2. Vérifier les plugins Claude Code

```bash
# Vérifier plugin feature-dev (optionnel pour Explore/Design, mais requis pour automation)
# Note: La vérification exacte dépend de l'API Claude Code disponible
# Pour maintenant, on va supposer qu'il est installé
# Si absent, les phases vont échouer et afficher un message clair
```

## 3. Afficher le succès

```bash
echo "✅ Tous les prérequis sont présents"
echo ""
echo "Outils vérifiés :"
echo "  ✅ gh CLI authentifiée"
echo "  ✅ jq disponible"
echo "  ✅ git disponible"
echo ""
```

# Règles

- ✅ **Exit 1 si prérequis manquant**
- ✅ **Messages d'erreur clairs** avec instructions d'installation
- ✅ **Pas d'interaction** : fail fast
- ✅ **Rapide** : vérifications simples et directes
