---
name: dev:debug
description: Analyser et résoudre une erreur (message simple ou stack trace)
model: sonnet
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Task]
argument-hint: <message-erreur-ou-fichier-log>
version: 1.0.0
license: MIT
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `implementer:debug`. Voir le plugin `implementer`. Sera supprimée en v3.0.

# Debug - Analyse et Résolution d'Erreurs

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Analyser une erreur (message ou stack trace) et proposer/appliquer résolution.

## Variables

- ERROR_INPUT: $ARGUMENTS
- ERROR_TYPE: Type détecté (simple message vs stack trace)
- CONTEXT_FILES: Fichiers pertinents
- RESOLUTION_PLAN: Plan structuré si résolution demandée

## Détection Automatique

Le système détecte automatiquement :
- **Stack trace** : Parsing + formatage + analyse approfondie
- **Message simple** : Analyse directe + diagnostic

Patterns stack trace :
- `Fatal error:`, `Uncaught`, `Exception`, `Error:`
- Présence de `at <file>:<line>`
- Multiple lignes avec indentation/numéros

## Workflow

### 1. Identification Type

**Si stack trace détectée** :
- Parser trace (type, message, fichier:ligne, call stack)
- Formater hiérarchiquement
- Lire code source ligne incriminée
- Générer rapport `/tmp/stack-trace-analysis-[timestamp].md`

**Si message simple** :
- Catégoriser (syntaxe, runtime, logique, config)
- Extraire infos contextuelles

### 2. Analyse Contexte

- Examiner fichiers mentionnés
- Analyser logs récents corrélés
- Vérifier environnement (deps, config)
- Identifier changements récents (git)

### 3. Diagnostic

- Cause racine vs symptômes
- Impact et criticité
- Solutions possibles + trade-offs
- Priorisation

### 4. Solutions

**Stack trace** : 3 niveaux
1. **Quick Fix ⚡** : Rapide, symptôme
2. **Recommandée ✅** : Équilibrée, cause
3. **Long-terme 🎯** : Robuste, prévention

**Message simple** : Plan résolution
- Étapes séquencées
- Tests validation
- Rollbacks prévus
- Risques estimés

### 5. Exécution (optionnel)

Si utilisateur demande résolution :
- Appliquer corrections pas à pas
- Valider chaque modif
- Vérifier résolution complète
- Documenter changements

## Exemples

```bash
# Stack trace PHP
/dev:debug "Fatal error: Call to undefined method User::getName()"

# Fichier log
/dev:debug /var/log/app.log

# Message NPM
/dev:debug "npm ERR! missing script: build"
```

## Best Practices

- Détecter type avant traiter
- Parser intelligemment selon langage
- Lire code source pour contexte
- Solutions testables avec exemples
- Corrections incrémentales si exécution
- Validation systématique après chaque change
