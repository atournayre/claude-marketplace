---
name: git-branch-core
description: >
  Skill interne fournissant les scripts communs pour la création de branches.
  Ne pas appeler directement - utilisé par git:branch et git:worktree.
allowed-tools: [Bash, Read, AskUserQuestion]
model: haiku
---

# Git Branch Core (Internal)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Ce skill fournit les scripts partagés pour la résolution de noms de branches. Il ne doit pas être appelé directement.

## Scripts disponibles

| Script | Description | Usage |
|--------|-------------|-------|
| `resolve-branch-name.sh` | Résout un nom de branche depuis un numéro d'issue ou du texte | `bash "$CORE_SCRIPTS/resolve-branch-name.sh" <issue-or-text>` |
| `validate-source-branch.sh` | Valide qu'une branche source existe localement | `bash "$CORE_SCRIPTS/validate-source-branch.sh" <source-branch>` |
| `check-branch-exists.sh` | Vérifie qu'une branche n'existe pas déjà | `bash "$CORE_SCRIPTS/check-branch-exists.sh" <branch-name>` |

## Usage par les skills enfants

```bash
CORE_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/branch-core/scripts"

# Valider la branche source
bash "$CORE_SCRIPTS/validate-source-branch.sh" "$SOURCE_BRANCH"

# Résoudre le nom de branche
eval "$(bash "$CORE_SCRIPTS/resolve-branch-name.sh" "$ISSUE_OR_TEXT")"
# Variables disponibles après eval :
#   $BRANCH_NAME      - Nom complet (ex: feature/42-login-fix)
#   $PREFIX           - Préfixe (ex: feature/)
#   $PREFIX_SOURCE    - Source (label/description/title/default/text)
#   $ISSUE_NUMBER     - Numéro d'issue (vide si texte)
#   $WORKTREE_DIRNAME - Nom répertoire worktree (ex: feature-42-login-fix)

# Vérifier que la branche n'existe pas
bash "$CORE_SCRIPTS/check-branch-exists.sh" "$BRANCH_NAME"
```

## Détection du préfixe

### Par numéro d'issue (priorité décroissante)

1. **Labels de l'issue** :
   - `bug`, `fix`, `bugfix` → `fix/`
   - `hotfix`, `critical`, `urgent` → `hotfix/`
   - `feature`, `enhancement`, `new-feature` → `feature/`
   - `chore`, `maintenance`, `refactor` → `chore/`
   - `documentation`, `docs` → `docs/`
   - `test`, `tests` → `test/`

2. **Description de l'issue** (mots-clés)

3. **Titre de l'issue** (mots-clés)

4. **Défaut** : `feature/`

### Par texte descriptif

- Analyse le premier mot du texte (`fix`, `hotfix`, `chore`, `docs`, `test`, etc.)
- Défaut : `feature/`

## Désambiguisation des arguments

Les skills enfants (`git:branch`, `git:worktree`) partagent la même logique de parsing des arguments.

SOURCE_BRANCH est **optionnel** et défaut à `MAIN_BRANCH` de `.env.claude`.

**Règle de désambiguisation (quand 1 seul argument) :**

| Argument | Type détecté | SOURCE_BRANCH | ISSUE_OR_TEXT |
|----------|-------------|---------------|---------------|
| `42` | Entier | MAIN_BRANCH (.env.claude) | `42` (issue) |
| `develop` | Branche locale existante | `develop` | Non fourni (demander) |
| `"fix login bug"` | Texte | MAIN_BRANCH (.env.claude) | `"fix login bug"` |

**Cascade de résolution de SOURCE_BRANCH :**
1. Argument explicite (premier de deux arguments, ou unique argument si branche existante)
2. `MAIN_BRANCH` de `.env.claude`
3. AskUserQuestion en dernier recours
