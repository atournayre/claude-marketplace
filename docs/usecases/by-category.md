---
title: Use Cases par Catégorie
description: Tous les use cases organisés par catégorie
---

# Use Cases par Catégorie

## Advanced

### [Orchestration multi-plugin](/usecases/advanced/multi-plugin-orchestration) <Badge type="info" text="★★★★★" /> <Badge type="tip" text="~60 min" />

Pipeline complet automatisé depuis une issue GitHub jusqu'à la PR mergée

**Plugins :** [dev](/plugins/dev), [git](/plugins/git), [github](/plugins/github), [framework](/plugins/framework), [review](/plugins/review)

**Mots-clés :** orchestration, pipeline, automation, ci-cd, workflow

---


## Development

### [Code review automatisé multi-agents](/usecases/development/code-review-automation) <Badge type="info" text="★★★" /> <Badge type="tip" text="~5 min" />

Review complète avec 4 agents parallèles pour détecter bugs, violations et problèmes de qualité

**Plugins :** [review](/plugins/review), [qa](/plugins/qa)

**Mots-clés :** review, quality, agents, parallel, phpstan, elegant-objects, tests

---

### [Résoudre erreurs PHPStan niveau 9](/usecases/development/phpstan-error-resolution) <Badge type="info" text="★★★" /> <Badge type="tip" text="~15 min" />

Agent spécialisé avec auto-fix loop pour corriger automatiquement les erreurs PHPStan strictes

**Plugins :** [qa](/plugins/qa)

**Mots-clés :** phpstan, static-analysis, auto-fix, types, generics

---

### [Workflow complet de développement de feature](/usecases/development/full-feature-workflow) <Badge type="info" text="★★★★" /> <Badge type="tip" text="~45 min" />

Orchestrateur 8 phases guidé pour développer une feature complète du besoin à la PR

**Plugins :** [dev](/plugins/dev), [git](/plugins/git), [qa](/plugins/qa), [review](/plugins/review)

**Mots-clés :** workflow, feature, orchestrateur, tdd, architecture, planning

---

### [Feature automatisée depuis issue GitHub](/usecases/development/auto-feature-from-issue) <Badge type="info" text="★★★★★" /> <Badge type="tip" text="~60 min" />

Workflow 100% automatisé en 10 phases depuis une issue GitHub jusqu'à la PR sans interaction

**Plugins :** [dev](/plugins/dev), [github](/plugins/github), [git](/plugins/git), [qa](/plugins/qa), [review](/plugins/review)

**Mots-clés :** workflow, automatisation, github, issue, orchestrateur, ci-cd

---


## Framework

### [Créer un workflow CQRS](/usecases/framework/create-cqrs-workflow) <Badge type="info" text="★★★" /> <Badge type="tip" text="~8 min" />

Générer Message + Handler + Tests pour architecture CQRS

**Plugins :** [framework](/plugins/framework)

**Mots-clés :** cqrs, message, handler, command, query

---

### [Générer une stack entité complète](/usecases/framework/generate-entity-stack) <Badge type="info" text="★★★" /> <Badge type="tip" text="~10 min" />

Génération orchestrée de Entity + Repository + Factory + Story + Tests en une commande

**Plugins :** [framework](/plugins/framework), [qa](/plugins/qa)

**Mots-clés :** entity, doctrine, foundry, tests, tdd, orchestrateur

---

### [Setup module DDD Bounded Context](/usecases/framework/setup-ddd-module) <Badge type="info" text="★★★★" /> <Badge type="tip" text="~30 min" />

Architecture complète avec prompts pour créer un module DDD isolé

**Plugins :** [framework](/plugins/framework), [prompt](/plugins/prompt)

**Mots-clés :** ddd, bounded-context, architecture, hexagonal

---


## Git & Workflow

### [Créer une Pull Request avec QA automatique](/usecases/git-workflow/create-pr-with-qa) <Badge type="info" text="★★" /> <Badge type="tip" text="~15 min" />

Workflow standard pour créer une PR avec PHPStan, tests et review automatique

**Plugins :** [git](/plugins/git), [qa](/plugins/qa), [review](/plugins/review)

**Mots-clés :** pr, pull-request, qa, phpstan, tests, review

---

### [Automatiser les release notes](/usecases/git-workflow/release-automation) <Badge type="info" text="★★" /> <Badge type="tip" text="~5 min" />

Génération automatique de notes de release HTML orientées utilisateurs finaux

**Plugins :** [git](/plugins/git), [doc](/plugins/doc)

**Mots-clés :** release, notes, changelog, git, automation

---

### [Corriger les commentaires de review PR](/usecases/git-workflow/fix-pr-comments) <Badge type="info" text="★★★" /> <Badge type="tip" text="~10 min" />

Skill avancée pour corriger tous les commentaires d'une PR en batch avec MultiEdit

**Plugins :** [git](/plugins/git), [github](/plugins/github)

**Mots-clés :** pr, review, comments, multi-edit, batch

---

### [Résoudre les conflits merge](/usecases/git-workflow/resolve-merge-conflicts) <Badge type="info" text="★★★" /> <Badge type="tip" text="~10 min" />

Workflow interactif pour résoudre les conflits git avec validation étape par étape

**Plugins :** [git](/plugins/git)

**Mots-clés :** git, merge, conflicts, resolution

---


## Testing

### [Test UI E2E avec scénario](/usecases/testing/e2e-ui-testing) <Badge type="info" text="★★" /> <Badge type="tip" text="~10 min" />

Tests end-to-end avec Chrome automation, GIF recording et debug mode

**Plugins :** [chrome-ui-test](/plugins/chrome-ui-test)

**Mots-clés :** e2e, ui, chrome, automation, testing, gif

---

### [Test responsive multi-device](/usecases/testing/responsive-testing) <Badge type="info" text="★★" /> <Badge type="tip" text="~8 min" />

Tester l'affichage sur 3 viewports (mobile, tablet, desktop) avec screenshots comparatifs

**Plugins :** [chrome-ui-test](/plugins/chrome-ui-test)

**Mots-clés :** responsive, viewport, mobile, tablet, desktop, screenshots

---


