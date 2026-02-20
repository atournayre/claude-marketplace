---
name: implementer:implement
description: Forcer l'implémentation complète d'une feature (pas juste planification)
argument-hint: <description-ou-issue>
model: opus
allowed-tools: [Task, Bash, Read, Write, Edit, Grep, Glob, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
---

# Implémentation Complète d'une Feature

Ce skill produit du CODE, pas un plan.

## Feature demandée

$ARGUMENTS

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

## Étape 1 : Inventaire (max 3 tours)

**Règle :** Maximum 5 fichiers lus avant de coder. Pas de phase explore longue.

1. Lire le `CLAUDE.md` du projet pour les contraintes architecturales
2. Lire `.claude/rules/` si le répertoire existe
3. Identifier TOUS les fichiers à créer/modifier avec chemin exact
4. Pour chaque fichier, noter :
   - Chemin exact
   - Action : `create` ou `modify`
   - Description courte de ce qui sera fait

**Sortie :**

```
Inventaire des fichiers

  Fichiers à créer :
  - src/Service/NewService.php (create) : Service principal
  - tests/Service/NewServiceTest.php (create) : Tests unitaires

  Fichiers à modifier :
  - config/services.yaml (modify) : Enregistrer le service
  - src/Controller/MainController.php (modify) : Utiliser le service

  Total : X fichiers
```

## Étape 2 : Checklist

Créer une tâche pour CHAQUE fichier identifié :

```
TaskCreate : "Créer src/Service/NewService.php"
TaskCreate : "Créer tests/Service/NewServiceTest.php"
TaskCreate : "Modifier config/services.yaml"
TaskCreate : "Modifier src/Controller/MainController.php"
```

- `activeForm` pour chaque tâche (ex: "Créant NewService.php")
- La checklist est OBLIGATOIRE avant le premier Edit/Write

## Étape 3 : Implémentation

Pour chaque fichier de la checklist :

1. `TaskUpdate` → tâche en `in_progress`
2. Implémenter le fichier (Write pour création, Edit pour modification)
3. `TaskUpdate` → tâche en `completed`

**Ordre d'implémentation :**
- D'abord les fichiers de base (entités, value objects, interfaces)
- Puis les services et repositories
- Puis les tests
- Enfin la configuration et le wiring

**Contraintes :**
- Respecter les contraintes du CLAUDE.md du projet
- Chaque fichier doit être complet et fonctionnel
- Les tests doivent couvrir les cas principaux

## Étape 4 : Vérification

1. Compter les fichiers créés/modifiés vs la checklist
2. Si des fichiers manquent, boucler sur l'étape 3 pour les compléter
3. Lancer les vérifications si disponibles (PHPStan, tests)

**Rapport final :**

```
Implémentation terminée

  Checklist : X/Y fichiers complétés

  Fichiers créés :
  - src/Service/NewService.php
  - tests/Service/NewServiceTest.php

  Fichiers modifiés :
  - config/services.yaml
  - src/Controller/MainController.php

  Manquants : (aucun | liste)
```

## Règles

- **Max 5 fichiers lus** avant de coder (pas de phase explore longue)
- **Checklist obligatoire** AVANT le premier Edit/Write
- **Chaque fichier** = une tâche dans le task manager
- **Rapport final** : fichiers créés/modifiés vs checklist + manquants
- **Pas de planification seule** : ce skill DOIT produire du code
- **Restriction** : ne JAMAIS créer de commits Git
