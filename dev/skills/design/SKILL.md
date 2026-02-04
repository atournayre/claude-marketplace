---
name: dev:design
description: Designer 2-3 approches architecturales (Phase 3)
model: sonnet
allowed-tools: [Task, Read, Glob, Grep, AskUserQuestion]
version: 1.0.0
license: MIT
---

# Configuration de sortie

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


**IMPORTANT** : Cette skill génère une comparaison d'architectures et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

**Output-style requis** : `table-based`

# Objectif

Phase 3 du workflow de développement : proposer plusieurs approches architecturales et aider l'utilisateur à choisir.

# Prérequis

⚠️ **Plugin feature-dev requis** pour les agents `code-architect`.

Si non installé :
```
/plugin install feature-dev@claude-code-plugins
```

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour la feature, les findings et les décisions
- Si phases précédentes non complétées, rediriger vers la phase manquante

## 2. Lancer les agents code-architect

Lancer **2-3 agents `code-architect` en parallèle** avec des focus différents :

### Agent 1 : Minimal changes
### Agent 2 : Clean architecture
### Agent 3 : Pragmatic balance

## 3. Consolider et comparer

Présenter les approches de manière structurée

## 4. Demander le choix de l'utilisateur

⚠️ **CRITIQUE : Attendre le choix avant de passer à la phase suivante.**

## 5. Documenter l'architecture choisie

Mettre à jour le workflow state

# Prochaine étape

```
✅ Architecture choisie

Prochaine étape : /dev:plan pour générer le plan d'implémentation
```
