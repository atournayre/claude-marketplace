---
model: claude-haiku-4-5-20251001
allowed-tools: Bash
argument-hint: <source-branch> [issue-number-or-text]
description: Création de branche Git avec workflow structuré
---

# Création de branche Git

## Purpose
Créer une nouvelle branche Git de manière structurée avec support des issues GitHub.

## Variables
SOURCE_BRANCH: $1
ISSUE_OR_TEXT: $2

## Instructions
- Utilise les outils Bash pour les opérations Git
- Valide que la branche source existe
- Génère un nom de branche basé sur l'issue si fournie
- Applique les conventions de nommage du projet

## Relevant Files
- @.git/config
- @.gitignore
- @docs/README.md

## Workflow

**🚨 ÉTAPE CRITIQUE : CHECKOUT VERS SOURCE D'ABORD 🚨**

1. **Vérifier SOURCE_BRANCH obligatoire**
   - Si `SOURCE_BRANCH` n'est pas fourni → ARRÊTER et demander à l'utilisateur

2. **Valider SOURCE_BRANCH existe localement**
   - `git branch --list "$SOURCE_BRANCH"`
   - Si n'existe pas → ARRÊTER avec erreur

3. **🔴 CHECKOUT VERS SOURCE_BRANCH AVANT TOUT 🔴**
   - `git checkout $SOURCE_BRANCH`
   - Vérifier qu'on est bien dessus : `git branch --show-current`
   - **CRITIQUE** : Cette étape garantit qu'on crée depuis un point propre

4. **🔴 PULL POUR METTRE À JOUR SOURCE_BRANCH 🔴**
   - `git pull origin $SOURCE_BRANCH`
   - Garantit qu'on part du dernier commit de origin
   - **CRITIQUE** : Évite de créer depuis un point obsolète

5. **Générer nom de la nouvelle branche**
   - Si `ISSUE_OR_TEXT` est fourni :
     - Détecte si c'est un numéro (entier) ou du texte
     - Si c'est un numéro :
       - Récupère les informations de l'issue via GitHub CLI (`gh issue view ${ISSUE_OR_TEXT}`)
       - Génère un nom de branche : `issue/${ISSUE_OR_TEXT}-{titre-simplifie}`
       - Le titre est nettoyé (espaces -> tirets, caractères spéciaux supprimés, minuscules)
     - Si c'est du texte :
       - Génère un nom de branche : `feature/${ISSUE_OR_TEXT-simplifie}`
       - Le texte est nettoyé (espaces -> tirets, caractères spéciaux supprimés, minuscules)
   - Si pas de `ISSUE_OR_TEXT`, demande le nom de branche à l'utilisateur

6. **Vérifier que la nouvelle branche n'existe pas déjà**
   - `git branch --list "$NEW_BRANCH"`
   - Si existe déjà → ARRÊTER avec erreur

7. **Créer et checkout la nouvelle branche**
   - `git checkout -b $NEW_BRANCH`
   - La branche est créée depuis SOURCE_BRANCH (car on est dessus)

8. **NE PAS configurer de tracking automatiquement**
   - ❌ **INTERDIT** : `git branch --set-upstream-to=origin/$SOURCE_BRANCH $NEW_BRANCH`
   - ✅ Le tracking sera configuré automatiquement lors du premier push avec `-u`
   - ✅ Lors du push : `git push -u origin $NEW_BRANCH`
   - **RAISON** : Configurer le tracking vers SOURCE_BRANCH pousse les commits sur la branche parente au lieu de créer une nouvelle branche distante

## Expertise
Conventions de nommage des branches :
- `feature/nom-descriptif` : Nouvelles fonctionnalités
- `fix/nom-bug` : Corrections de bugs
- `issue/123-nom-descriptif` : Basé sur une issue GitHub
- Utilise des tirets, pas d'espaces ni caractères spéciaux

## Template
```bash
# Exemple d'usage avec numéro d'issue :
/git:branch main 42

# Résultat attendu :
# - Récupère l'issue #42
# - Titre: "Add user authentication system"
# - Crée la branche: issue/42-add-user-authentication-system
# - Checkout vers cette branche

# Exemple d'usage avec texte :
/git:branch main "Add login form"

# Résultat attendu :
# - Crée la branche: feature/add-login-form
# - Checkout vers cette branche
```

## Examples
```bash
# Créer une branche depuis main avec issue GitHub
/git:branch main 123

# Créer une branche depuis main avec texte descriptif
/git:branch main "user authentication"

# Créer une branche depuis develop sans argument supplémentaire
/git:branch develop

# Créer une branche depuis une branche existante avec issue
/git:branch feature/api-base 456

# Créer une branche fix depuis main avec texte
/git:branch main "fix login bug"
```

## Report
- Nom de la branche créée
- Branche source utilisée
- Issue associée (si applicable)
- Statut du checkout
- Note : Le tracking remote sera configuré lors du premier push avec `git push -u origin $NEW_BRANCH`

## Validation
- ✅ `SOURCE_BRANCH` doit exister localement
- ✅ `SOURCE_BRANCH` est obligatoire
- ✅ **CHECKOUT vers SOURCE_BRANCH AVANT création** (CRITIQUE)
- ✅ **PULL pour mettre à jour SOURCE_BRANCH** (CRITIQUE)
- ✅ La nouvelle branche ne doit pas déjà exister
- ✅ Si `ISSUE_OR_TEXT` est un numéro, l'issue doit exister sur GitHub
- ✅ Le nom généré respecte les conventions de nommage
- ✅ Détection automatique entre numéro d'issue et texte descriptif

## Pourquoi checkout + pull vers SOURCE_BRANCH d'abord ?

**Problème 1 évité** :
- Si on est sur `feature/A` et on crée `feature/B` depuis `main`
- Sans checkout vers `main` d'abord, la branche est créée depuis `feature/A`
- Les commits de `feature/A` se retrouvent sur `feature/B`
- Résultat : impossible de créer une PR propre

**Problème 2 évité** :
- Si `main` locale est en retard sur `origin/main`
- Sans pull, on crée depuis un point obsolète
- Résultat : commits manquants, conflits, PR avec historique incorrect

**Solution** :
1. TOUJOURS faire `git checkout $SOURCE_BRANCH`
2. TOUJOURS faire `git pull origin $SOURCE_BRANCH`
3. PUIS créer avec `git checkout -b $NEW_BRANCH`
