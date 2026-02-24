---
name: infra:bump
description: Automatise les mises à jour de version des plugins avec détection automatique du type (PATCH ou MINOR). Met à jour plugin.json, CHANGELOG, README du plugin, README global, CHANGELOG global, marketplace.json, template PR et documentation VitePress.
model: haiku
allowed-tools: [Read, Edit, Bash, Glob, Grep, TaskCreate, TaskUpdate, TaskList, AskUserQuestion]
version: 1.0.0
license: MIT
---

# infra:bump

Mise à jour automatique de version d'un ou plusieurs plugins.

## Règle critique : Task Management obligatoire

Chaque étape DOIT être trackée via TaskCreate/TaskUpdate.
Créer la tâche AVANT de commencer, marquer `completed` UNIQUEMENT quand 100% terminée.

## Instructions à Exécuter

### Étape 1 : Créer les tâches du workflow

```
TaskCreate #1: "Détecter les plugins modifiés"
TaskCreate #2: "Sélectionner les plugins à bumper"
TaskCreate #3: "Mettre à jour fichiers du plugin"
TaskCreate #4: "Mettre à jour fichiers du marketplace"
TaskCreate #5: "Mettre à jour dépendances et documentation"
TaskCreate #6: "Vérifier et afficher résumé"
```

### Étape 2 : Détecter les plugins modifiés

```bash
git diff --name-only HEAD
git diff --staged --name-only
```

Extraire les noms de plugins (premier répertoire). Ignorer `.claude/` et fichiers à la racine.

### Étape 3 : Sélection interactive

Via AskUserQuestion (multiSelect) : quels plugins bumper ?

### Étape 4 : Mettre à jour fichiers du plugin

Pour chaque plugin sélectionné :

**4.1 Détecter le type de version :**
- Nouveaux agents ou skills → MINOR (X.Y+1.0)
- Modifications/corrections → PATCH (X.Y.Z+1)

**4.2 Calculer la nouvelle version** depuis `{plugin}/.claude-plugin/plugin.json`

**4.3 Analyser les changements** : git diff, catégoriser (Added/Changed/Fixed/Removed)

**4.4 Mettre à jour plugin.json** avec nouvelle version

**4.5 Mettre à jour CHANGELOG du plugin** : nouvelle entrée datée en haut

**4.6 Mettre à jour README du plugin** (obligatoire si MINOR)

### Étape 5 : Mettre à jour fichiers du marketplace

- README.md global : mettre à jour la ligne du plugin dans le tableau
- CHANGELOG.md global : ajouter entrée du jour
- marketplace.json : ajouter le plugin si nouveau
- template PR : synchroniser la liste des plugins
- `docs/guide/env-claude.md` si nouvelles variables `.env.claude`

### Étape 6 : Dépendances et documentation

```bash
cd docs && npm run build
```

Obligatoire. Vérifier qu'aucune erreur n'apparaît.

### Étape 7 : Résumé final

```
Plugin {plugin} : v{OLD} -> v{NEW} ({TYPE})

Fichiers modifiés :
  {plugin}/.claude-plugin/plugin.json
  {plugin}/CHANGELOG.md
  README.md
  CHANGELOG.md
  docs/plugins/{plugin}.md

Prochaine étape : /git:commit
```

## Règles de versioning

- **MINOR** (X.Y.0) : Nouveaux agents, skills, ou nouveau plugin
- **PATCH** (X.Y.Z+1) : Modifications, corrections, documentation
