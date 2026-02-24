---
title: "devops"
description: "Opérations DevOps Git : branches, commits, worktrees, PR, CI, releases"
version: "1.1.0"
---

# devops <Badge type="info" text="v1.1.0" />

Opérations DevOps Git : branches, commits, worktrees, PR, CI, releases.

## Installation

```bash
/plugin install devops@atournayre
```

## Skills Disponibles

Le plugin devops fournit 9 skills :

### `/devops:branch`

Création de branche Git avec workflow structuré.

### `/devops:commit`

Créer des commits bien formatés avec format conventional et emoji.

### `/devops:pr`

Crée une Pull Request GitHub standard avec workflow complet : QA, commits, assignation milestone/projet, code review automatique.

### `/devops:cd-pr`

Crée une Pull Request en mode Continuous Delivery avec workflow complet : QA, labels version (major/minor/patch), feature flags.

### `/devops:worktree`

Gestion des git worktrees pour développement parallèle (création, liste, suppression, statut, switch).

### `/devops:conflict`

Analyse les conflits git et propose une résolution pas à pas avec validation de chaque étape.

### `/devops:release-notes`

Génère des notes de release HTML orientées utilisateurs finaux.

### `/devops:release-report`

Génère un rapport HTML d'analyse d'impact entre deux branches.

### `/devops:ci-autofix`

Parse les logs CI et corrige automatiquement les erreurs.

## Changelog

- Voir CHANGELOG.md
