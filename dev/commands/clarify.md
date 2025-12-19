---
description: Poser questions pour lever ambiguités (Phase 2)
model: claude-sonnet-4-5-20250929
allowed-tools: AskUserQuestion, Read
---

# Objectif

Phase 2 du workflow de développement : identifier et résoudre toutes les ambiguités avant de designer l'architecture.

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour la feature et les findings de l'exploration
- Si le fichier n'existe pas ou phase 1 non complétée, rediriger vers `/dev:explore`

## 2. Analyser les zones d'ombre

Identifier les aspects sous-spécifiés dans les catégories suivantes :

### Edge cases
- Que se passe-t-il si X est vide/null ?
- Comment gérer les cas limites ?

### Gestion d'erreurs
- Quelles erreurs peuvent survenir ?
- Comment les communiquer à l'utilisateur ?

### Points d'intégration
- Comment cette feature interagit avec l'existant ?
- Y a-t-il des dépendances circulaires à éviter ?

### Rétrocompatibilité
- Cette feature impacte-t-elle des fonctionnalités existantes ?
- Y a-t-il des migrations de données nécessaires ?

### Performance
- Y a-t-il des contraintes de performance ?
- Faut-il penser au caching ?

### Sécurité
- Quelles autorisations sont nécessaires ?
- Y a-t-il des données sensibles à protéger ?

## 3. Présenter les questions

Utiliser `AskUserQuestion` pour présenter les questions de manière organisée :

```
❓ Questions de clarification

Avant de designer l'architecture, j'ai besoin de clarifier :

**Edge cases :**
1. {question}
2. {question}

**Gestion d'erreurs :**
3. {question}

**Intégration :**
4. {question}

**Rétrocompatibilité :**
5. {question}

**Performance :**
6. {question}
```

## 4. Attendre les réponses

⚠️ **CRITIQUE : Ne PAS passer à la phase suivante avant d'avoir toutes les réponses.**

## 5. Documenter les décisions

Mettre à jour le workflow state avec les réponses :

```json
{
  "currentPhase": 2,
  "phases": {
    "2": {
      "status": "completed",
      "completedAt": "{timestamp}",
      "decisions": {
        "edgeCases": "{réponses}",
        "errorHandling": "{réponses}",
        "integration": "{réponses}",
        "compatibility": "{réponses}",
        "performance": "{réponses}"
      }
    }
  }
}
```

# Prochaine étape

```
✅ Clarifications complètes

Prochaine étape : /dev:design pour proposer des architectures
```

# Règles

- Ne PAS proposer d'architecture à ce stade
- Ne PAS faire de suppositions - poser des questions
- Documenter TOUTES les décisions prises
