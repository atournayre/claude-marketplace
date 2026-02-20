---
name: implementer:code
description: Implémenter selon le plan — avec ou sans approbation préalable
argument-hint: [path-to-plan]
model: sonnet
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
---

# Implémenter selon le plan

Phase d'implémentation du workflow de développement : implémenter la feature selon le plan généré.

## Variables

PATH_TO_PLAN: $ARGUMENTS

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### 1. Vérifier le contexte et charger le plan

- Extraire PATH_TO_PLAN depuis $ARGUMENTS
- Si PATH_TO_PLAN n'est pas fourni :
  - Lire `.claude/data/.dev-workflow-state.json` avec Read
  - Extraire `planPath` du JSON
- Si toujours pas de plan, afficher une erreur et arrêter

### 2. Lire le plan

- Lire le fichier plan complet
- Extraire les étapes d'implémentation
- Identifier les fichiers à créer/modifier

### 3. Demander approbation avant implémentation (mode manuel)

Si lancé sans argument `--auto` :

> Attendre confirmation de l'utilisateur avant de continuer.

Si lancé avec `--auto` ou si le contexte workflow le demande :

> Démarrage immédiat sans checkpoint d'approbation.

### 4. Implémenter étape par étape

Pour chaque étape du plan :

1. Créer une todo pour l'étape (`TaskCreate`)
2. Lire les fichiers concernés (si modification)
3. Implémenter le code
4. Respecter :
   - Les conventions du projet (CLAUDE.md)
   - Les patterns identifiés dans l'exploration
   - Les décisions prises en phase d'analyse
5. Marquer la todo comme complétée (`TaskUpdate`)

**Ordre d'implémentation recommandé :**
1. Interfaces et contrats
2. Value Objects et exceptions métier
3. Entités et collections
4. Services et handlers
5. Configuration (services.yaml, etc.)

### 5. Créer les tests

- Créer les tests unitaires spécifiés dans le plan
- Suivre l'approche TDD si possible
- S'assurer que les tests passent

### 6. Vérifications qualité

```bash
make phpstan    # PHPStan niveau 9
make fix        # Formatage PSR-12
```

Corriger TOUTES les erreurs PHPStan avant de continuer.

### 7. Rapport final

```
Implémentation terminée

  Checklist : X/Y fichiers complétés

  Fichiers créés :
  - src/Service/NewService.php
  - tests/Service/NewServiceTest.php

  Fichiers modifiés :
  - config/services.yaml
  - src/Controller/MainController.php

  PHPStan : 0 erreur
  Tests : verts
```

## Règles

- PHPStan = 0 erreurs (bloquant CI)
- Respecter le plan (pas d'improvisation)
- Tests pour chaque composant
- Ne JAMAIS créer de commits Git
