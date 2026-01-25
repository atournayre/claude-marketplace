---
name: framework:make:all
description: Génère tous les fichiers pour une entité complète (orchestrateur)
license: MIT
version: 1.0.0
---

# Framework Make All Skill

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


## Description
Orchestrateur générant une stack complète Elegant Objects + DDD pour une entité.

## Usage
```
Use skill framework:make:all
```

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{properties}** - Liste des propriétés avec types (optionnel)

## Skills orchestrées

1. `framework:make:contracts` (si absent)
2. `framework:make:entity`
3. `framework:make:out`
4. `framework:make:invalide`
5. `framework:make:urls`
6. `framework:make:collection`
7. `framework:make:factory`
8. `framework:make:story`

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
TaskCreate #3: Générer Entity (framework:make:entity)
TaskCreate #4: Générer Out (framework:make:out)
TaskCreate #5: Générer Invalide (framework:make:invalide)
TaskCreate #6: Générer Urls (framework:make:urls)
TaskCreate #7: Générer Collection (framework:make:collection)
TaskCreate #8: Générer Factory (framework:make:factory)
TaskCreate #9: Générer Story (framework:make:story)
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
