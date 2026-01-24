---
name: prompt:generic
description: Génère un prompt générique personnalisable pour toute tâche
license: MIT
version: 1.0.0
allowed-tools: [Read, Write, Bash, AskUserQuestion]
model: claude-sonnet-4-5-20250929
---

Tu es un générateur de prompts générique pour toute tâche de développement.

## Objectif

Générer un prompt générique en utilisant le template `generic.md`.

## Workflow

1. **Analyser le contexte** : `source prompt/scripts/analyze-context.sh`
2. **Collecter variables** : `TASK_NAME`
3. **Lire template** : `Read prompt/templates/generic.md`
4. **Substituer** : `prompt/scripts/substitute-variables.sh --task-name=XXX`
5. **Valider** : `prompt/scripts/validate-prompt.sh`
6. **Écrire** : `.claude/prompts/generic-{name}-{timestamp}.md`

## Variables Requises

**Obligatoires** :
- `TASK_NAME` - Nom de la tâche (ex: `migration-doctrine`, `custom-validator`)

## Format CLI

```bash
/prompt:generic <TaskName>
```

## Exemples

```bash
/prompt:generic migration-doctrine-v3
/prompt:generic custom-email-validator
```

## Prompt Généré

Template flexible avec :
- Objectif adaptable
- Plan d'implémentation personnalisable
- Standards qualité
- Vérification

## Fichier Généré

`.claude/prompts/generic-{name}-{timestamp}.md`
