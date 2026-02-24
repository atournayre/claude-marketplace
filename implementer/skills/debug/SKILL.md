---
name: implementer:debug
description: Analyser et résoudre une erreur (message simple ou stack trace)
argument-hint: <message-erreur-ou-fichier-log>
model: sonnet
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Task]
version: 1.0.0
license: MIT
---

# Debug — Analyse et Résolution d'Erreurs

Analyser une erreur (message ou stack trace) et proposer/appliquer la résolution.

## Variables

- ERROR_INPUT: $ARGUMENTS
- ERROR_TYPE: Type détecté (simple message vs stack trace)
- CONTEXT_FILES: Fichiers pertinents
- RESOLUTION_PLAN: Plan structuré si résolution demandée

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

## Détection Automatique

Le système détecte automatiquement :
- **Stack trace** : Parsing + formatage + analyse approfondie
- **Message simple** : Analyse directe + diagnostic

Patterns stack trace :
- `Fatal error:`, `Uncaught`, `Exception`, `Error:`
- Présence de `at <file>:<line>`
- Multiple lignes avec indentation/numéros

## Workflow

### 1. Identification du type

**Si stack trace détectée** :
- Parser la trace (type, message, fichier:ligne, call stack)
- Formater hiérarchiquement
- Lire le code source à la ligne incriminée

**Si message simple** :
- Catégoriser (syntaxe, runtime, logique, config)
- Extraire les informations contextuelles

### 2. Analyse du contexte

- Examiner les fichiers mentionnés
- Analyser les logs récents corrélés
- Vérifier l'environnement (deps, config)
- Identifier les changements récents (git)

### 3. Diagnostic

- Cause racine vs symptômes
- Impact et criticité
- Solutions possibles + trade-offs
- Priorisation

### 4. Solutions

**Stack trace** : 3 niveaux
1. **Quick Fix** : Rapide, agit sur le symptôme
2. **Recommandée** : Équilibrée, traite la cause
3. **Long-terme** : Robuste, prévention

**Message simple** : Plan de résolution
- Étapes séquencées
- Tests de validation
- Rollbacks prévus
- Risques estimés

### 5. Exécution (si demandée)

Si l'utilisateur demande la résolution :
- Appliquer les corrections pas à pas
- Valider chaque modification
- Vérifier la résolution complète
- Documenter les changements

## Exemples

```bash
# Stack trace PHP
/implementer:debug "Fatal error: Call to undefined method User::getName()"

# Fichier log
/implementer:debug /var/log/app.log

# Message d'erreur npm
/implementer:debug "npm ERR! missing script: build"
```

## Résultat

```markdown
## Diagnostic : [Type d'erreur]

### Cause racine
[Description de la cause réelle, pas du symptôme]

### Solutions

#### Quick Fix _(rapide, symptôme)_
[Solution immédiate]

#### Recommandée _(équilibrée, cause)_
[Solution traitant la cause racine]

#### Long terme _(robuste, prévention)_
[Solution pérenne]

### Correction appliquée
[Si exécution demandée : étapes appliquées + validation]
```

## Règles

- Détecter le type avant de traiter
- Lire le code source pour le contexte
- Proposer des solutions testables avec exemples
- Corrections incrémentales si exécution
- Validation systématique après chaque changement
- Ne JAMAIS créer de commits Git
