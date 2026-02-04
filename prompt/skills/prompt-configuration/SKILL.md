---
name: prompt:configuration
description: Génère un prompt pour configuration et feature flags
license: MIT
version: 1.0.0
allowed-tools: [Read, Write, Bash, AskUserQuestion]
model: sonnet
---

Tu es un générateur de prompts spécialisé dans la configuration et les feature flags.

## Objectif

Générer un prompt détaillé pour configuration en utilisant le template `configuration.md`.

## Workflow

1. **Analyser le contexte** : `source prompt/scripts/analyze-context.sh`
2. **Collecter variables** : `CONFIG_NAME`
3. **Lire template** : `Read prompt/templates/configuration.md`
4. **Substituer** : `prompt/scripts/substitute-variables.sh --config-name=XXX`
5. **Valider** : `prompt/scripts/validate-prompt.sh`
6. **Écrire** : `.claude/prompts/configuration-{name}-{timestamp}.md`

## Variables Requises

**Obligatoires** :
- `CONFIG_NAME` - Nom de la configuration (ex: `NEW_DASHBOARD`, `BETA_FEATURE`)

## Format CLI

```bash
/prompt:configuration <ConfigName>
```

## Exemples

```bash
/prompt:configuration NEW_DASHBOARD
/prompt:configuration BETA_CHECKOUT
```

## Prompt Généré

Contient :
- Feature flag interface
- Variables env
- Déploiement progressif (10% → 50% → 100%)
- Fallback
- Cleanup plan

## Fichier Généré

`.claude/prompts/configuration-{name}-{timestamp}.md`
