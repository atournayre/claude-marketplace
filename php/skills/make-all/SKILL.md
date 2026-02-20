---
name: php:make-all
description: Génère tous les fichiers pour une entité complète (orchestrateur)
model: sonnet
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob]
version: 1.0.0
license: MIT
---

# PHP Make All Skill

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


## Description
Orchestrateur générant une stack complète Elegant Objects + DDD pour une entité.

## Usage
```
Use skill php:make-all
```

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{properties}** - Liste des propriétés avec types (optionnel)

## Skills orchestrées

1. `php:make-contracts` (si absent)
2. `php:make-entity`
3. `php:make-out`
4. `php:make-invalide`
5. `php:make-urls`
6. `php:make-collection`
7. `php:make-factory`
8. `php:make-story`

## Outputs

| Phase | Fichiers |
|-------|----------|
| Core | Entity, Repository, RepositoryInterface |
| Patterns | Out, Invalide |
| Avancé | Urls, UrlsMessage, UrlsMessageHandler, Collection |
| Tests | Factory, Story, AppStory |

## Workflow

### Initialisation

**Créer les tâches du workflow :**

Utiliser `TaskCreate` pour chaque phase :

```
TaskCreate #1: Demander EntityName et propriétés
TaskCreate #2: Vérifier/créer Contracts
TaskCreate #3: Générer Entity (php:make-entity)
TaskCreate #4: Générer Out (php:make-out)
TaskCreate #5: Générer Invalide (php:make-invalide)
TaskCreate #6: Générer Urls (php:make-urls)
TaskCreate #7: Générer Collection (php:make-collection)
TaskCreate #8: Générer Factory (php:make-factory)
TaskCreate #9: Générer Story (php:make-story)
TaskCreate #10: Afficher résumé + prochaines étapes
```

**Important :**
- Utiliser `activeForm` (ex: "Demandant EntityName", "Générant Entity")
- Respecter l'ordre d'exécution (dépendances entre skills)
- Chaque tâche doit être marquée `in_progress` puis `completed`

**Pattern d'exécution pour chaque étape :**
1. `TaskUpdate` → tâche en `in_progress`
2. Exécuter l'étape
3. `TaskUpdate` → tâche en `completed`

### Étapes

1. Demander EntityName et propriétés
2. Vérifier/créer Contracts
3. Exécuter séquentiellement les 8 skills
4. Afficher résumé + prochaines étapes

## Ordre d'exécution

```
contracts → entity → out/invalide → urls/collection → factory → story
```

## Task Management

**Progression du workflow :**
- 10 tâches créées à l'initialisation
- Chaque skill orchestré correspond à une tâche (tâches #3 à #9)
- Respecter l'ordre séquentiel (dépendances entre skills)
- Chaque tâche suit le pattern : `in_progress` → exécution → `completed`
- Utiliser `TaskList` pour voir la progression globale

## Notes
- Orchestrateur sans templates propres
- Ordre critique (respecte dépendances)
- Idéal pour démarrer rapidement
