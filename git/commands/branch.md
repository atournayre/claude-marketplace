---
model: claude-haiku-4-5-20251001
allowed-tools: Bash
argument-hint: <source-branch> [issue-number-or-text]
description: Création de branche Git avec workflow structuré
output-style: ultra-concise
hooks:
  PreToolUse:
    - matcher: "Bash(git checkout:*)"
      hooks:
        - type: command
          command: |
            # Hook 1: Bloquer si modifications non commitées
            if ! git diff --quiet || ! git diff --cached --quiet; then
              echo "❌ ERREUR : Modifications non commitées détectées"
              echo ""
              echo "Fichiers modifiés :"
              git status --short
              echo ""
              echo "Vous devez commit ou stash avant de créer une branche"
              exit 1
            fi
          once: true
    - matcher: "Bash(git branch:*)"
      hooks:
        - type: command
          command: |
            # Hook 2: Validation branche source existe (détection du premier argument)
            SOURCE_BRANCH=$(echo "$ARGUMENTS" | awk '{print $1}')
            if [ -n "$SOURCE_BRANCH" ] && ! git rev-parse --verify "$SOURCE_BRANCH" >/dev/null 2>&1; then
              echo "❌ ERREUR : La branche source '$SOURCE_BRANCH' n'existe pas"
              echo ""
              echo "Branches disponibles :"
              git branch -a
              exit 1
            fi
          once: true
  PostToolUse:
    - matcher: "Bash(git checkout -b:*)"
      hooks:
        - type: command
          command: |
            # Hook 3: Feedback création
            BRANCH=$(git branch --show-current)
            echo "✅ Branche créée : $BRANCH"
            echo "📝 Le tracking sera configuré automatiquement au premier commit"
          once: false
---

# Configuration de sortie

**IMPORTANT** : Cette commande effectue une opération Git rapide et nécessite un format de sortie spécifique.

Lis le frontmatter de cette commande. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

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
       - Récupère les informations de l'issue via GitHub CLI (`gh issue view ${ISSUE_OR_TEXT} --json title,labels,body`)
       - **Détermine le préfixe de branche (dans cet ordre de priorité)** :
         1. **Labels de l'issue** (priorité haute) :
            - Labels `bug`, `fix`, `bugfix` → préfixe `fix/`
            - Labels `hotfix`, `critical`, `urgent` → préfixe `hotfix/`
            - Labels `feature`, `enhancement`, `new-feature` → préfixe `feature/`
            - Labels `chore`, `maintenance`, `refactor` → préfixe `chore/`
            - Labels `documentation`, `docs` → préfixe `docs/`
            - Labels `test`, `tests` → préfixe `test/`
         2. **Description de l'issue** (si pas de labels pertinents) :
            - Cherche des mots-clés dans la description (case-insensitive)
            - Mots-clés `fix`, `bug`, `error`, `crash` → `fix/`
            - Mots-clés `hotfix`, `critical`, `urgent`, `production` → `hotfix/`
            - Mots-clés `feature`, `add`, `implement`, `new` → `feature/`
            - Mots-clés `refactor`, `cleanup`, `improve` → `chore/`
         3. **Titre de l'issue** (dernier recours) :
            - Même logique de recherche de mots-clés que pour la description
         4. **Défaut** : Si aucun préfixe détecté → `feature/`
       - Génère le nom complet : `{prefixe}{ISSUE_OR_TEXT}-{titre-simplifie}`
       - Le titre est nettoyé (espaces -> tirets, caractères spéciaux supprimés, minuscules)
     - Si c'est du texte :
       - Analyse le texte pour détecter le type d'action :
         - Commence par `fix`, `bug` → `fix/`
         - Commence par `hotfix` → `hotfix/`
         - Commence par `chore`, `refactor` → `chore/`
         - Commence par `docs`, `doc` → `docs/`
         - Commence par `test` → `test/`
         - Sinon → `feature/`
       - Génère un nom de branche : `{prefixe}{texte-simplifie}`
       - Le texte est nettoyé (préfixe détecté retiré, espaces -> tirets, caractères spéciaux supprimés, minuscules)
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
Conventions de nommage des branches (préfixe détecté automatiquement) :
- `feature/{numéro}-{description}` : Nouvelles fonctionnalités
- `fix/{numéro}-{description}` : Corrections de bugs
- `hotfix/{numéro}-{description}` : Corrections urgentes en production
- `chore/{numéro}-{description}` : Maintenance, refactoring
- `docs/{numéro}-{description}` : Documentation
- `test/{numéro}-{description}` : Tests
- Utilise des tirets, pas d'espaces ni caractères spéciaux

Détection automatique du préfixe (par priorité) :
1. Labels de l'issue GitHub
2. Mots-clés dans la description de l'issue
3. Mots-clés dans le titre de l'issue
4. Défaut : `feature/` si aucun indicateur trouvé

## Template
```bash
# Exemple 1 : Issue avec label "bug"
/git:branch main 42
# Résultat :
# - Récupère l'issue #42 (labels: ["bug"])
# - Titre: "Login form crashes on submit"
# - Détecte le préfixe "fix/" via le label
# - Crée la branche: fix/42-login-form-crashes-on-submit

# Exemple 2 : Issue avec label "feature"
/git:branch main 58
# Résultat :
# - Récupère l'issue #58 (labels: ["enhancement"])
# - Titre: "Add dark mode support"
# - Détecte le préfixe "feature/" via le label
# - Crée la branche: feature/58-add-dark-mode-support

# Exemple 3 : Issue sans label, description contient "fix"
/git:branch main 99
# Résultat :
# - Récupère l'issue #99 (labels: [])
# - Description contient "This will fix the error..."
# - Détecte le préfixe "fix/" via la description
# - Crée la branche: fix/99-{titre-simplifie}

# Exemple 4 : Issue sans label, sans description, titre contient "bug"
/git:branch main 123
# Résultat :
# - Récupère l'issue #123 (labels: [], description vide)
# - Titre: "Bug in user profile"
# - Détecte le préfixe "fix/" via le titre
# - Crée la branche: fix/123-bug-in-user-profile

# Exemple 5 : Texte descriptif avec préfixe explicite
/git:branch main "fix login validation"
# Résultat :
# - Détecte "fix" au début du texte
# - Crée la branche: fix/login-validation

# Exemple 6 : Texte descriptif sans préfixe
/git:branch main "Add OAuth support"
# Résultat :
# - Pas de préfixe détecté → défaut "feature/"
# - Crée la branche: feature/add-oauth-support
```

## Examples
```bash
# Créer une branche depuis main avec issue GitHub (détection auto du préfixe)
/git:branch main 123
# → Le préfixe sera détecté via labels/description/titre de l'issue

# Créer une branche depuis main avec texte descriptif
/git:branch main "user authentication"
# → Créera: feature/user-authentication (défaut)

# Créer une branche fix depuis main avec texte explicite
/git:branch main "fix login bug"
# → Créera: fix/login-bug (détecté via "fix" au début)

# Créer une branche hotfix depuis main
/git:branch main "hotfix critical payment issue"
# → Créera: hotfix/critical-payment-issue (détecté via "hotfix")

# Créer une branche depuis develop sans argument supplémentaire
/git:branch develop
# → Demandera le nom de branche à l'utilisateur

# Créer une branche depuis une branche existante avec issue
/git:branch feature/api-base 456
# → Préfixe détecté automatiquement depuis l'issue #456
```

## Report
- Nom de la branche créée
- Préfixe détecté et sa source (label/description/titre/défaut)
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
