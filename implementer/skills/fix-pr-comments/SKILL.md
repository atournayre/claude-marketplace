---
name: implementer:fix-pr-comments
description: Récupérer les commentaires de review PR et implémenter tous les changements demandés
argument-hint: [pr-number]
model: sonnet
allowed-tools: [Bash, Read, Edit, Grep, Glob]
version: 1.0.0
license: MIT
---

# Fix PR Comments

Traiter systématiquement TOUS les commentaires de review non résolus jusqu'à approbation de la PR.

## Contexte

- Branche actuelle: !`git branch --show-current`
- Statut du working tree: !`git status --short`
- Commits récents: !`git log --oneline -3`

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### 1. RÉCUPÉRER LES COMMENTAIRES

- Identifier la PR : `gh pr status --json number,headRefName`
- Récupérer les reviews : `gh pr review list --state CHANGES_REQUESTED`
- Récupérer les commentaires inline : `gh api repos/{owner}/{repo}/pulls/{number}/comments`
- Capturer BOTH les commentaires de review ET les commentaires inline
- STOP si pas de PR trouvée — demander le numéro de PR à l'utilisateur

### 2. ANALYSER ET PLANIFIER

- Extraire les références exactes fichier:ligne
- Grouper par fichier pour l'efficacité
- RESTER DANS LE SCOPE : ne JAMAIS corriger des problèmes non liés
- Créer une checklist : un item par commentaire

### 3. IMPLÉMENTER LES CORRECTIONS

- AVANT d'éditer : TOUJOURS `Read` le fichier cible en premier
- Grouper les changements avec Edit pour les modifications du même fichier
- Faire EXACTEMENT ce que le reviewer a demandé
- Cocher chaque commentaire résolu

### 4. RAPPORT

Après avoir traité tous les commentaires :

```
Commentaires traités : X/Y

Résolus :
- [fichier:ligne] : [description du changement]

Non résolus (si applicable) :
- [fichier:ligne] : [raison]
```

## Règles

- Chaque commentaire non résolu DOIT être adressé
- Lire les fichiers AVANT chaque modification — sans exception
- INTERDIT : changements de style au-delà des demandes du reviewer
- En cas d'échec : revenir à la phase ANALYSER, ne jamais sauter des commentaires
- Ne JAMAIS créer de commits Git

User: $ARGUMENTS
