---
name: orchestrator:transform
description: Transforme un prompt quelconque (texte libre ou fichier) en prompt exécutable structuré avec TaskCreate/TaskUpdate/TaskList. Génère un fichier .claude/prompts/executable-{name}-{timestamp}.md
argument-hint: <prompt-file-or-text> [--name=<output-name>]
model: sonnet
allowed-tools: [Read, Write, Bash, AskUserQuestion, Glob, TaskCreate, TaskUpdate, TaskList]
version: 1.0.0
license: MIT
---

# orchestrator:transform

Transformation d'un prompt en prompt exécutable compatible avec le Task Management System.

## Instructions à Exécuter

### 1. Récupérer le prompt source

- Si argument est un fichier : `Read` le contenu
- Si argument est du texte : utiliser directement
- Si aucun argument : `AskUserQuestion` pour demander le prompt

### 2. Analyser le prompt

Identifier :
- L'objectif principal
- Les sous-tâches implicites ou explicites
- Les dépendances entre tâches
- Les livrables attendus
- Les critères de validation

### 3. Structurer en tâches exécutables

Pour chaque tâche :
- `#N` : Numéro (commence à 0)
- `content` : Description impérative (ex: "Créer le fichier X")
- `activeForm` : Forme continue (ex: "Création du fichier X")
- Critères de validation
- Dépendances si applicable

### 4. Générer le format exécutable

Le prompt transformé doit inclure :

```markdown
# [Titre]

## Objectif
[Description]

## Initialisation des Tâches

TaskCreate #0: [Nom]
  content: "[Description impérative]"
  activeForm: "[Forme continue]"

TaskCreate #1: [Nom]
  ...

## Instructions d'Exécution

### Phase 1 : [Nom]

**Tâche #0 : [Nom]**
1. TaskUpdate #0 → in_progress
2. [Instructions]
3. [Critères de validation]
4. TaskUpdate #0 → completed

## Critères de Validation Globaux

- [ ] Critère 1
- [ ] Toutes les tâches completed (TaskList)
```

### 5. Créer le répertoire de sortie

```bash
mkdir -p .claude/prompts
```

### 6. Écrire le prompt transformé

Nom : `.claude/prompts/executable-{name}-{timestamp}.md`

`{name}` depuis :
1. `--name=XXX` si fourni
2. Titre/objectif du prompt (kebab-case)
3. Sinon "prompt"

`{timestamp}` : format `YYYYMMDD-HHMMSS`

### 7. Afficher le résultat

```
.claude/prompts/executable-{name}-{timestamp}.md

Tâches extraites : X
Phases : Y
```

## Règles de transformation

- Granularité : chaque tâche réalisable en 5-30 minutes
- Atomicité : une tâche = une action claire
- Vérifiabilité : critère de validation par tâche
- Numérotation commence à #0
- Minimum 3 tâches, au moins 2 phases
