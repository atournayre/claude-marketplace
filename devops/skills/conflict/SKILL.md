---
name: devops:conflict
description: Analyse les conflits git et propose à l'utilisateur une résolution pas à pas avec validation de chaque étape.
model: sonnet
allowed-tools: [Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git merge:*), Bash(git rebase:*), Bash(git checkout:*), Bash(git add:*), Read, Edit]
argument-hint: <branche-destination>
version: 1.0.0
license: MIT
---

# Résolution Interactive de Conflits Git

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Résoudre les conflits git de manière interactive : $ARGUMENTS

## Purpose

Analyser les conflits git et guider l'utilisateur dans une résolution pas à pas, fichier par fichier, avec validation à chaque étape.

## Variables
- DESTINATION_BRANCH: $1 (branche de destination pour le merge/rebase)
- CURRENT_BRANCH: !`git branch --show-current`
- CONFLICTED_FILES: Liste des fichiers en conflit
- RESOLUTION_MODE: merge ou rebase (détecté automatiquement)

## État Actuel du Repository

- Branche actuelle : !`git branch --show-current`
- Status Git : !`git status --porcelain`
- Conflits détectés : !`git diff --name-only --diff-filter=U`
- Commits divergents : !`git log --oneline HEAD...$DESTINATION_BRANCH --max-count=5`

## Workflow

### 1. Validation initiale

**Vérifier DESTINATION_BRANCH obligatoire :**
- Si `DESTINATION_BRANCH` n'est pas fourni -> ARRÊTER et demander à l'utilisateur

**Vérifier que DESTINATION_BRANCH existe :**
- `git branch --list "$DESTINATION_BRANCH"` (locale)
- `git branch -r --list "origin/$DESTINATION_BRANCH"` (remote)
- Si n'existe pas -> ARRÊTER avec erreur

**Vérifier l'état du repository :**
- `git status` pour détecter :
  - Merge en cours (fichiers "both modified")
  - Rebase en cours (`.git/rebase-merge/` ou `.git/rebase-apply/`)
  - Conflits existants

### 2. Initier l'opération si nécessaire

**Si aucun merge/rebase en cours :**
- Demander à l'utilisateur : "Voulez-vous merger ou rebaser $CURRENT_BRANCH sur $DESTINATION_BRANCH ?"
- Options :
  1. Merge : `git merge $DESTINATION_BRANCH`
  2. Rebase : `git rebase $DESTINATION_BRANCH`
  3. Annuler
- Exécuter l'opération choisie

**Si l'opération échoue avec conflits :**
- Continuer avec l'analyse des conflits

### 3. Analyse des conflits

**Lister tous les fichiers en conflit :**
```bash
git diff --name-only --diff-filter=U
```

**Pour chaque fichier, collecter :**
- Chemin complet du fichier
- Nombre de sections en conflit
- Lignes concernées
- Contexte (fonction/classe/module)

### 4. Résolution interactive par fichier

**Pour chaque fichier en conflit :**

**Étape A : Afficher le contexte**
- Nom du fichier et chemin
- Nombre de conflits dans ce fichier
- `git diff $FICHIER` pour voir les marqueurs de conflit

**Étape B : Analyser les versions**
- Lire le fichier avec Read pour voir les marqueurs :
  - `<<<<<<< HEAD` : version actuelle
  - `=======` : séparateur
  - `>>>>>>> $DESTINATION_BRANCH` : version à merger
- Afficher les différences de manière claire

**Étape C : Proposer 3 stratégies**

1. **Garder la version actuelle (ours)**
   - `git checkout --ours $FICHIER`
   - Quand : notre version est correcte, l'autre est obsolète

2. **Garder la version entrante (theirs)**
   - `git checkout --theirs $FICHIER`
   - Quand : leur version est correcte, la nôtre est obsolète

3. **Résolution manuelle**
   - Utiliser Edit pour fusionner manuellement
   - Supprimer les marqueurs `<<<<<<<`, `=======`, `>>>>>>>`
   - Combiner les changements pertinents des deux versions

**Étape D : Demander confirmation**
- Afficher un résumé de la stratégie choisie
- Demander : "Voulez-vous appliquer cette résolution ? (oui/non/voir le diff)"
- Si "voir le diff" : montrer le résultat avec `git diff --cached $FICHIER`

**Étape E : Appliquer la résolution**
- Exécuter la stratégie choisie
- Marquer le fichier comme résolu : `git add $FICHIER`
- Confirmer : "Conflit résolu dans $FICHIER"

### 5. Vérification finale

**Après avoir résolu tous les fichiers :**
```bash
git status
```
- Vérifier qu'il n'y a plus de fichiers "both modified"
- Vérifier que tous les fichiers conflictuels sont stagés

**Demander confirmation finale :**
- "Tous les conflits sont résolus. Voulez-vous finaliser ?"
- Options :
  1. Oui, finaliser
  2. Non, réviser les changements
  3. Annuler tout (abort)

### 6. Finalisation

**Si merge :**
```bash
git commit --no-edit
# ou si l'utilisateur veut personnaliser :
git commit -m "Merge branch '$DESTINATION_BRANCH' into $CURRENT_BRANCH"
```

**Si rebase :**
```bash
git rebase --continue
```

**Si annulation demandée :**
```bash
git merge --abort   # ou
git rebase --abort
```

## Examples

```bash
# Situation : on est sur feature/auth, on veut merger main
/devops:conflict main

# Situation : rebase en cours, 3 fichiers en conflit
/devops:conflict develop
```

## Rapport / Réponse

```markdown
# Rapport de Résolution de Conflits

## Configuration
- Branche actuelle : $CURRENT_BRANCH
- Branche destination : $DESTINATION_BRANCH
- Type d'opération : merge/rebase

## Conflits Détectés
- Nombre total de fichiers : X
- Fichiers résolus : Y
- Fichiers restants : Z

## Résolutions Appliquées

### Fichier : src/auth.php
- Stratégie : Résolution manuelle
- Raison : Fusion de deux implémentations valides

### Fichier : config/app.php
- Stratégie : Garder version actuelle (ours)
- Raison : Configuration locale spécifique

## Statut Final
Tous les conflits résolus
Merge/rebase finalisé avec succès
```

## Validation

- DESTINATION_BRANCH doit exister (locale ou remote)
- Tous les fichiers en conflit doivent être traités
- Aucun marqueur de conflit ne doit rester dans les fichiers
- Tous les fichiers résolus doivent être stagés
- L'utilisateur doit valider avant chaque résolution
- L'utilisateur doit confirmer avant la finalisation

## Notes Importantes

- La commande est 100% interactive : chaque action nécessite validation
- L'utilisateur garde le contrôle total du processus
- Possibilité d'annuler à tout moment avec merge/rebase --abort
- Les résolutions manuelles utilisent Edit pour garantir la qualité
