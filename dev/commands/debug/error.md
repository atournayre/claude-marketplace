---
model: claude-sonnet-4-5-20250929
allowed-tools: Bash,Read,Write,Edit,Grep,Glob,TodoWrite,Task
description: Analyser et résoudre une erreur (message simple ou stack trace)
argument-hint: <message-erreur-ou-fichier-log>
---

# Debug Error - Analyse et Résolution

Analyser une erreur (message ou stack trace) et proposer/appliquer résolution.

{{_templates/timing.md}}

## Variables

- ERROR_INPUT: Message erreur ou chemin fichier log
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

## Format Rapport

### Stack Trace
```markdown
# Stack Trace Analysis - [TIMESTAMP]

## Résumé
- Type : [ERROR_TYPE]
- Localisation : [FILE:LINE]
- Cause racine : [ROOT_CAUSE]
- Sévérité : [LEVEL]

## Stack Trace Formatée
[Trace complète formatée]

## Analyse
### Point origine
- Fichier/Ligne/Méthode
- Code context

### Contexte
- Call stack simplifié
- État probable
- Dépendances

### Cause Racine
[Explication]

## Solutions
### 1. Quick Fix ⚡
[Description + étapes]

### 2. Recommandée ✅
[Description + étapes]

### 3. Long-terme 🎯
[Description + étapes]

## Prochaines Étapes
[Actions recommandées]
```

### Message Simple
```markdown
## Analyse Erreur

### Type
[Classification + sévérité]

### Localisation
[Fichiers/lignes]

### Contexte
[Environnement + conditions]

## Diagnostic
- Cause racine
- Impact
- Recommandations

## Résolution
[Si exécutée]
- Actions effectuées
- Validations
- Suivi
```

## Exemples

```bash
# Stack trace PHP
/debug:error "Fatal error: Call to undefined method User::getName()"

# Fichier log
/debug:error /var/log/app.log

# Message NPM
/debug:error "npm ERR! missing script: build"

# Stack trace JS
/debug:error "TypeError: Cannot read property 'id' of undefined at main.js:156"
```

## Best Practices

- Détecter type avant traiter
- Parser intelligemment selon langage
- Lire code source pour contexte
- Solutions testables avec exemples
- Corrections incrémentales si exécution
- Validation systématique après chaque change
