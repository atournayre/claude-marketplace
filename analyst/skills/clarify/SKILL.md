---
name: analyst:clarify
description: Lever les ambiguïtés avant design - Phase 2 (mode interactif ou heuristiques automatiques)
model: sonnet
allowed-tools: [AskUserQuestion, Read, Grep, Glob, Task]
version: 1.0.0
license: MIT
---

# Lever les ambiguïtés (Phase 2)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Phase 2 du workflow de développement : identifier et résoudre toutes les ambiguïtés avant de designer l'architecture.

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour la feature et les findings de l'exploration
- Si le fichier n'existe pas ou phase 1 non complétée, rediriger vers `/analyst:explore`
  (en mode automatique : exit avec erreur code 1)

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

## 3. Résoudre les ambiguïtés

### Mode interactif

Utiliser `AskUserQuestion` pour présenter les questions de manière organisée.

**CRITIQUE : Ne PAS passer à la phase suivante avant d'avoir toutes les réponses.**

### Mode automatique (zéro AskUserQuestion)

Appliquer cette table de décision :

| Catégorie | Heuristique par défaut |
|-----------|------------------------|
| **Edge cases** | Valeur null/vide → Exception métier explicite (`InvalideXXX` ou `{NomEntité}Invalide`) |
| **Gestion erreurs** | Exceptions métier typées (héritant d'une base commune) + logging PSR-3 niveau ERROR |
| **Intégration** | Réutiliser patterns existants détectés en Phase 1 (patterns de repository, services, DTOs) |
| **Rétrocompatibilité** | Préserver API publique (pas de breaking changes), créer nouvelle méthode si needed |
| **Performance** | Pas de cache prématuré sauf si liste > 1000 items (sinon trop de complexité) |
| **Sécurité** | TOUJOURS valider inputs (whitelist si possible), échapper outputs selon context |

## 4. Documenter les décisions

Mettre à jour le workflow state avec les réponses ou les décisions appliquées :

```json
{
  "currentPhase": 2,
  "phases": {
    "2": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": "{durée}",
      "autoDecisions": {
        "edgeCases": "Exception métier InvalideXXX pour valeurs null/vides",
        "errorHandling": "Exceptions typées héritant de DomainException + logging PSR-3 ERROR",
        "integration": "Réutilisation patterns existants Phase 1",
        "compatibility": "Préservation API publique, nouvelle méthode si breaking",
        "performance": "Pas de cache prématuré sauf liste > 1000 items",
        "security": "Validation inputs (whitelist), échappement outputs"
      }
    }
  }
}
```

# Règles

- Ne PAS proposer d'architecture à ce stade
- Ne PAS faire de suppositions en mode interactif - poser des questions
- En mode automatique : zéro AskUserQuestion, heuristiques appliquées directement
- Documenter TOUTES les décisions prises
- Utiliser les patterns existants détectés en Phase 1

# Prochaine étape

```
Clarifications complètes

Prochaine étape : /architect:design pour proposer des architectures
```
