---
name: dev:plan
description: Générer plan d'implémentation dans docs/specs/ (Phase 4)
model: sonnet
allowed-tools: [Write, Read, Glob]
version: 1.0.0
license: MIT
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `architect:plan`. Voir le plugin `architect`. Sera supprimée en v3.0.

# Objectif

Phase 4 du workflow de développement : générer un plan d'implémentation détaillé basé sur l'architecture choisie.

# Instructions

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

## 1. Créer les tâches de planification

Utiliser `TaskCreate` pour chaque étape :

```
TaskCreate #1: Lire le contexte du workflow
TaskCreate #2: Créer le répertoire docs/specs
TaskCreate #3: Générer le plan d'implémentation
TaskCreate #4: Afficher le résumé
TaskCreate #5: Mettre à jour le workflow state
```

**Important :**
- Utiliser `activeForm` (ex: "Lisant le contexte", "Générant le plan")
- Chaque tâche doit être marquée `in_progress` puis `completed`

**Pattern d'exécution pour chaque étape :**
1. `TaskUpdate` → tâche en `in_progress`
2. Exécuter l'étape
3. `TaskUpdate` → tâche en `completed`

## 2. Lire le contexte

**🔄 Progression :** `TaskUpdate` → tâche #1 en `in_progress`

- Lire `.claude/data/.dev-workflow-state.json` pour récupérer :
  - La feature description
  - Les décisions de clarification
  - L'architecture choisie
- Si phases précédentes non complétées, rediriger vers la phase manquante

**🔄 Progression :** `TaskUpdate` → tâche #1 en `completed`

## 3. Créer le répertoire si nécessaire

**🔄 Progression :** `TaskUpdate` → tâche #2 en `in_progress`

```bash
mkdir -p docs/specs
```

**🔄 Progression :** `TaskUpdate` → tâche #2 en `completed`

## 4. Générer le plan

**🔄 Progression :** `TaskUpdate` → tâche #3 en `in_progress`

Créer le fichier `docs/specs/feature-{nom-kebab-case}.md` avec la structure complète du plan

**🔄 Progression :** `TaskUpdate` → tâche #3 en `completed`

## 5. Afficher le résumé

**🔄 Progression :** `TaskUpdate` → tâche #4 en `in_progress`

Présenter le plan généré.

**🔄 Progression :** `TaskUpdate` → tâche #4 en `completed`

## 6. Mettre à jour le workflow state

**🔄 Progression :** `TaskUpdate` → tâche #5 en `in_progress`

Mettre à jour `.claude/data/.dev-workflow-state.json`

**🔄 Progression :** `TaskUpdate` → tâche #5 en `completed`

# Task Management

**Progression du workflow :**
- 5 tâches créées à l'initialisation
- Chaque étape suit le pattern : `in_progress` → exécution → `completed`
- La tâche #3 (génération du plan) est la plus importante
- Utiliser `TaskList` pour voir la progression
- Les tâches permettent à l'utilisateur de suivre la création du plan d'implémentation

# Prochaine étape

```
✅ Plan généré : docs/specs/feature-{nom}.md

Prochaine étape : /dev:code docs/specs/feature-{nom}.md

⚠️ L'implémentation nécessite ton approbation explicite.
```

# Règles

- Le plan doit être **actionnable** (pas de descriptions vagues)
- Chaque étape doit avoir des **fichiers** et des **tâches** clairs
- Les tests doivent être **spécifiés** avant l'implémentation
- Respecter les **conventions du projet** (CLAUDE.md)
