---
title: Configuration .env.claude
description: Guide de configuration du fichier .env.claude pour personnaliser le comportement des plugins
---

# Configuration `.env.claude`

Le fichier `.env.claude` permet de configurer le comportement des plugins du marketplace pour chaque projet. Il est lu automatiquement par les skills qui en ont besoin.

## Emplacement

Le fichier doit se trouver **a la racine du projet utilisateur** (pas dans le plugin).

```
mon-projet/
├── .env.claude       # <-- ici
├── src/
├── composer.json
└── ...
```

## Format

Le format est `KEY=VALUE`, une variable par ligne. Pas de quotes, pas d'export.

```bash
MAIN_BRANCH=main
REPO=atournayre/mon-projet
PROJECT=Mon Projet
WORKTREE_DIR=../worktrees
```

## Variables disponibles

### `MAIN_BRANCH`

Branche principale du projet. Utilisee comme branche source par defaut quand aucune n'est specifiee.

| Propriete | Valeur |
|-----------|--------|
| **Defaut** | `main` |
| **Exemples** | `main`, `master`, `develop` |
| **Plugins** | git, dev |

**Skills qui l'utilisent :**

| Skill | Usage |
|-------|-------|
| `/git:branch` | Branche source par defaut si non fournie en argument |
| `/git:worktree` | Branche source par defaut si non fournie en argument |
| `/git:pr` | Branche de base pour la Pull Request |
| `/git:cd-pr` | Branche de base pour la Pull Request CD |
| `/dev:auto-feature` | Branche de base pour le workflow automatise |

**Exemple :**
```bash
# .env.claude
MAIN_BRANCH=develop
```

```bash
# Avant : branche source obligatoire
/git:branch main 42

# Apres : branche source optionnelle (utilise MAIN_BRANCH)
/git:branch 42
```

---

### `REPO`

Identifiant du depot GitHub au format `owner/repo`.

| Propriete | Valeur |
|-----------|--------|
| **Defaut** | Detecte automatiquement via `git remote` |
| **Format** | `owner/repo` |
| **Plugins** | git, dev |

**Skills qui l'utilisent :**

| Skill | Usage |
|-------|-------|
| `/git:pr` | Depot cible pour la creation de PR |
| `/git:cd-pr` | Depot cible pour la creation de PR CD |

**Exemple :**
```bash
REPO=atournayre/mon-projet
```

---

### `PROJECT`

Nom du projet GitHub (GitHub Projects v2). Utilise pour l'assignation automatique des PR a un projet.

| Propriete | Valeur |
|-----------|--------|
| **Defaut** | Vide (pas d'assignation) |
| **Plugins** | git, dev |

**Skills qui l'utilisent :**

| Skill | Usage |
|-------|-------|
| `/git:pr` | Assigne la PR au projet GitHub |
| `/git:cd-pr` | Assigne la PR au projet GitHub |
| `/dev:auto-feature` | Assigne la PR au projet GitHub |

**Exemple :**
```bash
PROJECT=Mon Projet Sprint 3
```

---

### `WORKTREE_DIR`

Repertoire de base pour la creation des worktrees Git. Peut etre un chemin relatif ou absolu.

| Propriete | Valeur |
|-----------|--------|
| **Defaut** | Demande a l'utilisateur si absent |
| **Exemples** | `../worktrees`, `.worktrees`, `/home/user/worktrees` |
| **Plugins** | git |

**Skills qui l'utilisent :**

| Skill | Usage |
|-------|-------|
| `/git:worktree` | Repertoire parent pour les worktrees |

**Convention de nommage des repertoires :**

La branche `feature/ma-fonctionnalite` cree un worktree dans `$WORKTREE_DIR/feature-ma-fonctionnalite` (les `/` sont remplaces par des `-`).

**Exemple :**
```bash
WORKTREE_DIR=../worktrees
```

```bash
/git:worktree 42
# Cree: ../worktrees/feature-42-login-fix/
```

## Exemple complet

```bash
# .env.claude - Configuration projet
MAIN_BRANCH=main
REPO=atournayre/mon-application
PROJECT=Sprint 4
WORKTREE_DIR=../worktrees
```

## Comportement

- **Fichier optionnel** : si `.env.claude` n'existe pas, les skills utilisent des valeurs par defaut ou demandent a l'utilisateur
- **Variables optionnelles** : chaque variable est independante, seules celles qui te sont utiles doivent etre definies
- **Pas de quotes** : ecrire `MAIN_BRANCH=main` et non `MAIN_BRANCH="main"`
- **Pas d'export** : ecrire `MAIN_BRANCH=main` et non `export MAIN_BRANCH=main`
- **Priorite** : les arguments passes en ligne de commande ont toujours priorite sur `.env.claude`

## Gitignore

Le fichier `.env.claude` peut contenir des configurations specifiques a l'environnement de chaque developpeur (par exemple `WORKTREE_DIR`). Selon le cas :

- **Commiter** : si les variables sont communes a l'equipe (`MAIN_BRANCH`, `REPO`, `PROJECT`)
- **Gitignorer** : si les variables sont specifiques a chaque developpeur (`WORKTREE_DIR`)

Pour un compromis, utiliser un template :

```bash
# Commiter .env.claude.dist comme reference
cp .env.claude.dist .env.claude

# Ajouter .env.claude au .gitignore
echo ".env.claude" >> .gitignore
```

## Ajouter une variable

Si tu developpes un plugin ou une skill qui a besoin d'une configuration projet, utilise `.env.claude` avec cette convention :

1. **Nommer en SCREAMING_SNAKE_CASE** : `MA_VARIABLE`
2. **Documenter** : ajouter la variable a cette page
3. **Fallback** : toujours prevoir un comportement par defaut si la variable est absente
4. **Lecture** : utiliser `Read` pour lire `.env.claude` et extraire la valeur
