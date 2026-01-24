---
name: dev:discover
description: Comprendre le besoin avant développement (Phase 0)
argument-hint: <description-feature>
model: claude-sonnet-4-5-20250929
allowed-tools: [TaskCreate, TaskUpdate, TaskList, Read, AskUserQuestion, Glob, Grep]
version: 1.0.0
license: MIT
---

# Configuration de sortie

**IMPORTANT** : Cette skill génère un résumé de compréhension structuré et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

**Output-style requis** : `bullet-points`

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Phase 0 du workflow de développement : comprendre le besoin utilisateur avant de coder.

# Feature demandée

$ARGUMENTS

# Instructions

## 1. Analyser la demande

- Si la demande est claire et complète, passer à l'étape 2
- Si la demande est ambiguë ou incomplète, poser des questions pour clarifier :
  - Quel problème cette feature résout-elle ?
  - Qui sont les utilisateurs cibles ?
  - Quelles sont les contraintes connues ?

## 2. Explorer le contexte

- Chercher si des fichiers similaires existent déjà dans le projet
- Lire `CLAUDE.md` et `.ai/` pour comprendre les conventions
- Identifier les patterns architecturaux utilisés

## 3. Résumer la compréhension

Présenter un résumé structuré :

```
📋 Résumé de la demande

**Feature :** {titre court}

**Problème résolu :**
{description du problème}

**Utilisateurs cibles :**
{qui utilisera cette feature}

**Contraintes identifiées :**
- {contrainte 1}
- {contrainte 2}

**Contexte technique :**
- {pattern existant pertinent}
- {fichiers existants liés}
```

## 4. Confirmer avec l'utilisateur

Demander confirmation avant de passer à la phase suivante :

```
✅ Est-ce que cette compréhension est correcte ?

Prochaine étape : /dev:explore pour analyser le codebase
```

# Mise à jour du workflow state

Créer ou mettre à jour `.claude/data/.dev-workflow-state.json` (créer le répertoire si nécessaire)

# Règles

- Ne PAS commencer à coder
- Ne PAS proposer d'architecture
- Se concentrer sur la COMPRÉHENSION du besoin
- Poser des questions si quelque chose n'est pas clair
