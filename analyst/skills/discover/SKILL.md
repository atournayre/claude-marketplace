---
name: analyst:discover
description: Comprendre le besoin avant développement - Phase 0 (supporte le mode automatique)
argument-hint: <description-feature>
model: sonnet
allowed-tools: [TaskCreate, TaskUpdate, TaskList, Read, AskUserQuestion, Glob, Grep]
version: 1.0.0
license: MIT
---

# Comprendre le besoin (Phase 0)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Phase 0 du workflow de développement : comprendre le besoin utilisateur avant de coder.

# Feature demandée

$ARGUMENTS

# Instructions

## 1. Analyser la demande

- Si la demande est claire et complète, passer à l'étape 2
- Si la demande est ambiguë ou incomplète :
  - **Mode interactif** : poser des questions pour clarifier :
    - Quel problème cette feature résout-elle ?
    - Qui sont les utilisateurs cibles ?
    - Quelles sont les contraintes connues ?
  - **Mode automatique** (si issue GitHub fournie) : évaluer la clarté automatiquement
    - Si ambiguïté critique → FAIL immédiatement avec message explicite et exit 1
    - Si description claire → continuer sans interaction

## 2. Explorer le contexte

- Chercher si des fichiers similaires existent déjà dans le projet
- Lire `CLAUDE.md` et `.ai/` pour comprendre les conventions
- Identifier les patterns architecturaux utilisés
- Lire `.claude/rules/` si le répertoire existe pour extraire les contraintes

En mode automatique : limiter l'exploration à **5 fichiers maximum**

## 3. Résumer la compréhension

Présenter un résumé structuré :

```
Résumé de la demande

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

## 4. Confirmer ou valider

- **Mode interactif** : demander confirmation avant de passer à la phase suivante
  ```
  Est-ce que cette compréhension est correcte ?
  Prochaine étape : /analyst:explore pour analyser le codebase
  ```
- **Mode automatique** : valider automatiquement et continuer sans interaction

# Mise à jour du workflow state

Créer ou mettre à jour `.claude/data/.dev-workflow-state.json` (créer le répertoire si nécessaire)

# Règles

- Ne PAS commencer à coder
- Ne PAS proposer d'architecture
- Se concentrer sur la COMPRÉHENSION du besoin
- Poser des questions si quelque chose n'est pas clair (mode interactif)
- Fail fast si ambiguïté critique (mode automatique)
