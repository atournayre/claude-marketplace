---
name: reviewer:elegant-objects
description: Vérifier la conformité du code PHP aux principes Elegant Objects de Yegor Bugayenko
argument-hint: [fichier.php]
model: sonnet
allowed-tools: [Bash, Read, Grep, Glob]
version: 1.0.0
license: MIT
---

# Elegant Objects Reviewer

Vérifier la conformité du code PHP aux principes Elegant Objects de Yegor Bugayenko. Analyse un fichier spécifique ou tous les fichiers modifiés dans la branche.

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

```
/reviewer:elegant-objects [fichier.php]
```

Sans argument : analyse les fichiers PHP modifiés dans la branche.

## Workflow

### 1. Déterminer les fichiers à analyser

- Avec argument : analyser le fichier spécifié
- Sans argument : `git diff --name-only` pour obtenir les fichiers PHP modifiés

### 2. Vérifier les règles Elegant Objects

#### Classes
- Classes `final` (sauf abstraites et interfaces)
- Max 4 attributs
- Pas de getters/setters publics
- Pas de méthodes statiques
- Noms sans suffixe -er (Manager, Handler, Helper...)
- Constructeur unique et simple (uniquement des affectations)

#### Méthodes
- Pas de retour `null`
- Pas d'argument `null`
- Corps sans lignes vides ni commentaires inline
- CQRS : séparation commandes/queries

#### Tests
- Une assertion par test (dernière instruction)
- Noms en français décrivant le comportement
- Pas de setUp/tearDown

### 3. Calculer le score de conformité

- Violation critique: -10 points
- Violation majeure: -5 points
- Recommandation: -2 points
- Base: 100

### 4. Générer le rapport

```
## Score de conformité Elegant Objects
Score global : X/100

## Violations critiques (bloquantes)
### [Règle violée]
- Fichier: /chemin/absolu/fichier.php:ligne
- Problème: Description précise
- Suggestion: Code corrigé ou approche recommandée

## Violations majeures (à corriger)
[Même format]

## Recommandations (améliorations)
[Même format]

## Statistiques
- Fichiers analysés : X
- Classes analysées : Y
- Méthodes analysées : Z
- Tests analysés : W
- Total violations : N

## Prochaines étapes
Liste priorisée des corrections à effectuer
```

## Règles

- Ignorer vendor/, var/, cache/
- Controllers Symfony tolérés
- Prioriser par criticité
