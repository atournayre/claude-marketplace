---
title: Orchestration multi-plugin
description: Pipeline complet automatisé depuis une issue GitHub jusqu'à la PR mergée
category: advanced
plugins:
  - name: dev
    skills: [/dev:auto-feature]
  - name: git
    skills: [/git:pr]
  - name: github
    skills: [/github:fix]
  - name: framework
    skills: []
  - name: review
    skills: []
complexity: 5
duration: 60
keywords: [orchestration, pipeline, automation, ci-cd, workflow]
related:
  - /usecases/development/auto-feature-from-issue
  - /usecases/development/full-feature-workflow
  - /usecases/git-workflow/create-pr-with-qa
---

# Orchestration multi-plugin <Badge type="info" text="★★★★★ Complexe" /> <Badge type="tip" text="~60 min" />

## Contexte

Développer une feature complète nécessite plusieurs plugins : récupérer l'issue, développer, tester, reviewer, créer la PR. Orchestrer tout ça manuellement prend du temps.

## Objectif

Pipeline complet automatisé :

**Phase 1 :** Récupérer issue GitHub (`github` plugin)
**Phase 2 :** Développer feature (`dev` plugin)
**Phase 3 :** Générer entités si nécessaire (`framework` plugin)
**Phase 4 :** Review multi-agents (`review` plugin)
**Phase 5 :** Créer PR (`git` plugin)
**Phase 6 :** Corriger commentaires (`git` + `github` plugin)

Le tout sans interaction humaine.

## Prérequis

**Plugins :**
- [dev](/plugins/dev)
- [git](/plugins/git)
- [github](/plugins/github)
- [framework](/plugins/framework)
- [review](/plugins/review)

**Outils :**
- Tous configurés (Git, GitHub CLI, PHPStan, Tests)

## Workflow

**Commande :**
```bash
/dev:auto-feature 42 && /dev:review && /git:pr
```

Ou créer un workflow personnalisé :

```bash
/command:make-command full-pipeline
```

**Pipeline généré :**
```yaml
name: full-pipeline
phases:
  - fetch-issue: /github:fix 42
  - develop: /dev:auto-feature 42
  - review: /dev:review
  - create-pr: /git:pr
  - wait-for-comments: sleep 3600 # 1h
  - fix-comments: /git:fix-pr-comments
```

## Exemple

**Input :** Issue #42 "Add product catalog"

**Output :**
- Feature développée automatiquement
- 15 fichiers créés
- Tests : 100% coverage
- Review score : 94/100
- PR créée et mergée

**Durée :** 45 minutes (sans interaction)

## Liens Connexes

**Use cases :**
- [Feature auto](/usecases/development/auto-feature-from-issue)
- [Workflow complet](/usecases/development/full-feature-workflow)

**Plugins :**
- Tous les plugins
