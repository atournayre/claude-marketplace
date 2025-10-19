---
model: claude-sonnet-4-5-20250929
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git merge:*), Bash(git rebase:*), Bash(git checkout:*), Bash(git add:*), Read, Edit
argument-hint: <branche-destination>
description: Analyse les conflits git et propose à l'utilisateur une résolution pas à pas avec validation de chaque étape.
---

# Résolution Interactive de Conflits Git

Résoudre les conflits git de manière interactive : $ARGUMENTS

## Purpose
Analyser les conflits git et guider l'utilisateur dans une résolution pas à pas, fichier par fichier, avec validation à chaque étape.

## Timing

### Début d'Exécution
**OBLIGATOIRE - PREMIÈRE ACTION** :
1. Exécuter `date` pour obtenir l'heure réelle
2. Afficher immédiatement : 🕐 **Démarrage** : [Résultat de la commande date]
3. Stocker le timestamp pour le calcul de durée

### Fin d'Exécution
**OBLIGATOIRE - DERNIÈRE ACTION** :
1. Exécuter `date` à nouveau pour obtenir l'heure de fin
2. Calculer la durée réelle entre début et fin
3. Afficher :
   - ✅ **Terminé** : [Résultat de la commande date]
   - ⏱️ **Durée** : [Durée calculée au format lisible]

### Formats
- Date : résultat brut de la commande `date` (incluant CEST/CET automatiquement)
- Durée :
  - Moins d'1 minute : `XXs` (ex: 45s)
  - Moins d'1 heure : `XXm XXs` (ex: 2m 30s)
  - Plus d'1 heure : `XXh XXm XXs` (ex: 1h 15m 30s)

### Instructions CRITIQUES
- TOUJOURS exécuter `date` via Bash - JAMAIS inventer/halluciner l'heure
- Le timestamp de début DOIT être obtenu en exécutant `date` immédiatement
- Le timestamp de fin DOIT être obtenu en exécutant `date` à la fin
- Calculer la durée en soustrayant les timestamps unix (utiliser `date +%s`)
- NE JAMAIS supposer ou deviner l'heure

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

## Ce Que Fait Cette Commande

1. Détecte s'il y a un merge/rebase en cours ou si on doit l'initier
2. Identifie tous les fichiers en conflit
3. Pour chaque fichier en conflit :
   - Affiche le contexte du conflit
   - Montre les différences entre les versions
   - Propose 3 stratégies de résolution
   - Demande validation avant d'appliquer
4. Vérifie que tous les conflits sont résolus
5. Finalise le merge/rebase

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

### 1. Validation initiale

**Vérifier DESTINATION_BRANCH obligatoire :**
- Si `DESTINATION_BRANCH` n'est pas fourni → ARRÊTER et demander à l'utilisateur

**Vérifier que DESTINATION_BRANCH existe :**
- `git branch --list "$DESTINATION_BRANCH"` (locale)
- `git branch -r --list "origin/$DESTINATION_BRANCH"` (remote)
- Si n'existe pas → ARRÊTER avec erreur

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
- Confirmer : "✅ Conflit résolu dans $FICHIER"

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

## Stratégies de Résolution Détaillées

### Stratégie 1 : Garder la version actuelle (ours)
- Utilisation : Quand notre implémentation est plus récente/correcte
- Commande : `git checkout --ours $FICHIER && git add $FICHIER`
- Attention : Perte des changements de l'autre branche

### Stratégie 2 : Garder la version entrante (theirs)
- Utilisation : Quand la version à merger est plus récente/correcte
- Commande : `git checkout --theirs $FICHIER && git add $FICHIER`
- Attention : Perte de nos changements

### Stratégie 3 : Résolution manuelle intelligente
- Utilisation : Quand les deux versions contiennent des changements valides
- Processus :
  1. Lire le fichier avec Read
  2. Identifier les sections en conflit
  3. Analyser la logique de chaque version
  4. Utiliser Edit pour fusionner :
     - Garder les imports/dépendances des deux côtés
     - Fusionner la logique métier intelligemment
     - Supprimer tous les marqueurs de conflit
  5. Vérifier la syntaxe du résultat
  6. `git add $FICHIER`

## Examples

### Exemple 1 : Merge avec conflits
```bash
# Situation : on est sur feature/auth, on veut merger main
/git:conflit main

# Claude détecte : pas de merge en cours
# Claude demande : "Voulez-vous merger main dans feature/auth ?"
# Utilisateur : "oui, merge"
# Claude exécute : git merge main
# Conflits détectés dans : src/auth.php, config/app.php
# Claude guide la résolution fichier par fichier
```

### Exemple 2 : Rebase en cours avec conflits
```bash
# Situation : rebase en cours, 3 fichiers en conflit
/git:conflit develop

# Claude détecte : rebase en cours sur develop
# Claude liste : file1.php, file2.js, file3.md
# Claude résout interactivement chaque fichier
# Claude finalise : git rebase --continue
```

### Exemple 3 : Résolution manuelle complexe
```bash
/git:conflit main

# Conflit dans src/payment.php :
# HEAD : ajout méthode processRefund()
# main : ajout méthode processChargeback()
# Stratégie : Résolution manuelle
# Claude fusionne les deux méthodes
# Validation : utilisateur confirme
```

## Report Format

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
- Lignes modifiées : 42-58

### Fichier : config/app.php
- Stratégie : Garder version actuelle (ours)
- Raison : Configuration locale spécifique

## Statut Final
✅ Tous les conflits résolus
✅ Merge/rebase finalisé avec succès

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]
⏱️ Durée : [durée formatée]
```

## Best Practices

### Avant de commencer
- ✅ S'assurer que le working directory est propre
- ✅ Avoir une sauvegarde (commit ou stash)
- ✅ Comprendre les changements des deux branches

### Pendant la résolution
- ✅ Résoudre un fichier à la fois
- ✅ Tester la syntaxe après chaque résolution manuelle
- ✅ Ne jamais garder les marqueurs de conflit (<<<<, ====, >>>>)
- ✅ Valider que la logique est cohérente
- ✅ En cas de doute, demander à l'utilisateur

### Après la résolution
- ✅ Vérifier que le code compile/s'exécute
- ✅ Lancer les tests si disponibles
- ✅ Réviser le diff final avant commit

## Messages d'Erreur et Solutions

### "error: you need to resolve your current index first"
- Cause : Conflits non résolus
- Solution : Continuer la résolution ou faire `git merge --abort`

### "no changes added to commit"
- Cause : Fichiers résolus mais non stagés
- Solution : `git add $FICHIER` après chaque résolution

### "conflict (content): Merge conflict in X"
- Cause : Changements incompatibles dans le même fichier
- Solution : Résoudre avec une des 3 stratégies

## Validation

- ✅ DESTINATION_BRANCH doit exister (locale ou remote)
- ✅ Tous les fichiers en conflit doivent être traités
- ✅ Aucun marqueur de conflit ne doit rester dans les fichiers
- ✅ Tous les fichiers résolus doivent être stagés
- ✅ L'utilisateur doit valider avant chaque résolution
- ✅ L'utilisateur doit confirmer avant la finalisation

## Notes Importantes

- La commande est 100% interactive : chaque action nécessite validation
- L'utilisateur garde le contrôle total du processus
- Possibilité d'annuler à tout moment avec merge/rebase --abort
- Les résolutions manuelles utilisent Edit pour garantir la qualité
- Un rapport détaillé est généré à la fin
