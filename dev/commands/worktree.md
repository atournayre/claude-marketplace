---
description: Gestion des git worktrees pour développement parallèle
argument-hint: <action> [args]
model: claude-sonnet-4-5-20250929
allowed-tools: Bash, Read, Write, Edit, Grep, TodoWrite, AskUserQuestion
---

# Objectif

Gérer les git worktrees pour permettre le développement de plusieurs features en parallèle sans conflits.

# Actions disponibles

## create

Créer un nouveau worktree pour une feature.

**Usage :**
```
/dev:worktree create <feature-name> [base-branch]
```

**Arguments :**
- `feature-name` : Nom de la feature (ex: "oauth-auth", "refactor-payment")
- `base-branch` : Branche de base (défaut: main ou master)

**Exemple :**
```
/dev:worktree create oauth-auth
/dev:worktree create hotfix-payment main
```

**Comportement :**
1. Détecter la branche principale (main/master)
2. Normaliser le nom de la feature (kebab-case)
3. Créer la branche `feature/<feature-name>` ou `hotfix/<feature-name>`
4. Créer le worktree dans `../<repo-name>-<feature-name>`
5. Mettre à jour `.claude/data/.dev-worktrees.json` avec les métadonnées
6. Afficher les instructions pour basculer vers le worktree

**Format `.claude/data/.dev-worktrees.json` :**
```json
{
  "worktrees": [
    {
      "name": "oauth-auth",
      "branch": "feature/oauth-auth",
      "path": "../claude-marketplace-oauth-auth",
      "createdAt": "2025-12-20T10:30:00Z",
      "status": "active"
    }
  ]
}
```

## list

Lister tous les worktrees actifs.

**Usage :**
```
/dev:worktree list
```

**Affichage :**
```
📂 Worktrees actifs

  ✓ oauth-auth
    Branche: feature/oauth-auth
    Path: ../claude-marketplace-oauth-auth
    Créé: 2025-12-20 10:30

  ✓ hotfix-payment
    Branche: hotfix/payment
    Path: ../claude-marketplace-hotfix-payment
    Créé: 2025-12-20 14:15

💡 Pour basculer : cd <path>
💡 Pour supprimer : /dev:worktree remove <name>
```

## remove

Supprimer un worktree (après merge ou abandon).

**Usage :**
```
/dev:worktree remove <feature-name>
```

**Comportement :**
1. Vérifier qu'il n'y a pas de modifications non commitées
2. Demander confirmation si des commits non poussés existent
3. Supprimer le worktree avec `git worktree remove`
4. Optionnellement supprimer la branche (demander confirmation)
5. Mettre à jour `.claude/data/.dev-worktrees.json`

## status

Afficher le statut détaillé d'un ou tous les worktrees.

**Usage :**
```
/dev:worktree status [feature-name]
```

**Affichage :**
```
📊 Statut : oauth-auth

Path: ../claude-marketplace-oauth-auth
Branche: feature/oauth-auth
Créé: 2025-12-20 10:30

Git status:
  • 3 fichiers modifiés
  • 2 commits en avance sur origin
  • Pas de modifications non commitées

Workflow /dev:feature:
  Phase actuelle: 5. Code
  Progression: 62%
```

## switch

Basculer vers un worktree existant (utilitaire de navigation).

**Usage :**
```
/dev:worktree switch <feature-name>
```

**Comportement :**
Afficher les commandes pour changer de répertoire :
```
Pour basculer vers le worktree 'oauth-auth' :

  cd ../claude-marketplace-oauth-auth

Puis relancer Claude Code dans ce répertoire.
```

# Règles de nommage

- **Features** : `feature/<name>` → worktree dans `../<repo>-<name>`
- **Hotfixes** : `hotfix/<name>` → worktree dans `../<repo>-<name>`
- **Nom normalisé** : kebab-case uniquement (convertir espaces et caractères spéciaux)

# Sécurité

- ❌ Ne jamais supprimer un worktree avec des modifications non commitées sans confirmation
- ❌ Ne jamais créer de worktree si le nom de branche existe déjà
- ⚠️ Avertir si des commits ne sont pas poussés avant suppression
- ✅ Toujours vérifier que le répertoire parent existe

# Intégration avec /dev:feature

La commande `/dev:feature` peut automatiquement proposer de créer un worktree en Phase 0 (Discover) :

```
🔄 Workflow de développement : Ajouter OAuth

📂 Créer un worktree pour cette feature ?

Avantages :
  • Garder votre branche main propre
  • Travailler sur plusieurs features en parallèle
  • Préserver le contexte de développement

Créer le worktree ? (o/n)
```

Si oui, exécuter :
```
/dev:worktree create oauth-auth
```

# Commande sans arguments

Si l'utilisateur tape `/dev:worktree` sans arguments :

```
📖 Gestion des git worktrees

Usage : /dev:worktree <action> [args]

Actions :
  create <name> [base]  - Créer un worktree
  list                  - Lister les worktrees
  remove <name>         - Supprimer un worktree
  status [name]         - Afficher le statut
  switch <name>         - Basculer vers un worktree

Exemples :
  /dev:worktree create oauth-auth
  /dev:worktree list
  /dev:worktree status oauth-auth
  /dev:worktree remove oauth-auth

Documentation complète :
  git worktree --help
```

# Notes d'implémentation

## Détection de la branche principale

```bash
# Chercher main, puis master, puis branche actuelle
MAIN_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
if [ -z "$MAIN_BRANCH" ]; then
  if git show-ref --verify --quiet refs/heads/main; then
    MAIN_BRANCH="main"
  elif git show-ref --verify --quiet refs/heads/master; then
    MAIN_BRANCH="master"
  else
    MAIN_BRANCH=$(git branch --show-current)
  fi
fi
```

## Création du worktree

```bash
# Normaliser le nom
FEATURE_NAME=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' _' '-')
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
WORKTREE_PATH="../${REPO_NAME}-${FEATURE_NAME}"
BRANCH_NAME="feature/${FEATURE_NAME}"

# Créer la branche et le worktree
git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH" "$BASE_BRANCH"
```

## Vérification avant suppression

```bash
# Vérifier modifications non commitées
cd "$WORKTREE_PATH"
if ! git diff-index --quiet HEAD --; then
  echo "⚠️ Des modifications non commitées existent !"
  read -p "Continuer quand même ? (o/n) " -n 1 -r
fi

# Vérifier commits non poussés
UNPUSHED=$(git log @{u}.. --oneline 2>/dev/null | wc -l)
if [ "$UNPUSHED" -gt 0 ]; then
  echo "⚠️ $UNPUSHED commit(s) non poussé(s) !"
fi
```
