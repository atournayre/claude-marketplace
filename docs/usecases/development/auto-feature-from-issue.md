---
title: Feature automatisée depuis issue GitHub
description: Workflow 100% automatisé en 10 phases depuis une issue GitHub jusqu'à la PR sans interaction
category: development
plugins:
  - name: dev
    skills: [/dev:auto-feature, /dev:auto-fetch-issue, /dev:auto-discover, /dev:auto-explore, /dev:auto-clarify, /dev:auto-design, /dev:auto-plan, /dev:auto-code, /dev:auto-review]
  - name: github
    skills: []
  - name: git
    skills: []
  - name: qa
    skills: []
  - name: review
    skills: []
complexity: 5
duration: 60
keywords: [workflow, automatisation, github, issue, orchestrateur, ci-cd]
related:
  - /usecases/development/full-feature-workflow
  - /usecases/git-workflow/create-pr-with-qa
  - /usecases/advanced/multi-plugin-orchestration
---

# Feature automatisée depuis issue GitHub <Badge type="info" text="★★★★★ Complexe" /> <Badge type="tip" text="~60 min" />

## Contexte

Développer une feature depuis une issue GitHub nécessite normalement beaucoup d'interactions : lire l'issue, comprendre le besoin, explorer le code, designer, implémenter, tester et créer la PR. Ce workflow automatise toutes ces étapes sans interaction humaine.

## Objectif

Générer une PR complète automatiquement depuis une issue GitHub en 10 phases :

**Phase -1 :** Vérifier prérequis
**Phase 0 :** Récupérer issue GitHub
**Phase 1 :** Découverte automatique du besoin
**Phase 2 :** Exploration automatique du codebase
**Phase 3 :** Clarification avec heuristiques
**Phase 4 :** Design automatique d'architecture
**Phase 5 :** Génération de plan
**Phase 6 :** Implémentation TDD
**Phase 7 :** Review avec auto-fix
**Phase 8 :** Création PR
**Phase 9 :** Résumé et next steps

## Prérequis

**Plugins :**
- [dev](/plugins/dev) - Workflow automatisé
- [github](/plugins/github) - Interaction avec GitHub
- [git](/plugins/git) - Gestion des commits et PR
- [qa](/plugins/qa) - PHPStan et qualité
- [review](/plugins/review) - Code review automatique

**Outils :**
- GitHub CLI (`gh`) authentifié
- Git configuré
- PHPStan niveau 9
- Tests PHPUnit
- Accès en lecture/écriture au repository

**Configuration :**
```bash
# Vérifier que gh est authentifié
gh auth status

# Vérifier que PHPStan est configuré
cat phpstan.neon
```

**Permissions GitHub :**
- Lecture des issues
- Création de branches
- Push de commits
- Création de Pull Requests

## Workflow Étape par Étape

### Lancer le workflow complet

**Commande :**
```bash
/dev:auto-feature 42
```

Où `42` est le numéro de l'issue GitHub.

---

### Phase -1 : Vérifier prérequis

**Objectif :** Vérifier que tout est configuré avant de commencer.

**Vérifications automatiques :**
1. ✅ GitHub CLI authentifié
2. ✅ Repository GitHub accessible
3. ✅ Issue existe et est lisible
4. ✅ PHPStan configuré
5. ✅ Tests configurés
6. ✅ Git configuré (user.name, user.email)
7. ✅ Branch actuelle est main/master

**Output attendu :**
```
✅ Phase -1/9 : Prérequis validés

Checks :
✅ gh auth : OK
✅ Issue #42 : Accessible
✅ PHPStan : Configuré (level 9)
✅ Tests : PHPUnit détecté
✅ Git : Configuré (user@example.com)
✅ Branch : main (clean)
```

**En cas d'erreur :** Le workflow s'arrête avec un message explicite.

---

### Phase 0 : Récupérer l'issue GitHub

**Objectif :** Récupérer le contenu complet de l'issue.

**Actions automatiques :**
```bash
gh issue view 42 --json title,body,labels,assignees
```

**Output attendu :**
```
✅ Phase 0/9 : Issue récupérée

Issue #42 : Add email notification on order validation
Labels : enhancement, backend
Assignee : @atournayre

Description :
Users should receive an email when their order status changes to "validated".
The email should include order details and a tracking link.

Acceptance criteria :
- Email sent asynchronously (Messenger)
- Template with order details
- Tests with email assertions
```

**Données extraites :**
- Titre : "Add email notification on order validation"
- Type : enhancement (feature)
- Critères d'acceptation : 3 critères identifiés
- Assignee : @atournayre

---

### Phase 1 : Découverte automatique

**Objectif :** Analyser le besoin sans poser de questions.

**Heuristiques automatiques :**
1. Détecter le type de feature (API, UI, Background Job)
2. Identifier les entités concernées (Order, User, Email)
3. Détecter les patterns (Event, Command, Query)
4. Identifier les dépendances (Mailer, Messenger)

**Output attendu :**
```
✅ Phase 1/9 : Découverte terminée

Type de feature : Background Job (EventSubscriber)
Entités : Order, User
Patterns : Event-Driven Architecture
Dépendances : Symfony Mailer, Messenger

Document : docs/specs/issue-42-discovery.md
```

**Contenu `issue-42-discovery.md` :**
```markdown
# Discovery : Email notification on order validation

## Problème
Users don't know when their order is validated.

## Solution
Send email asynchronously when OrderValidatedEvent is dispatched.

## Critères de succès
- Email sent via Messenger
- Template with order details
- Tests covering email sending

## Contraintes techniques
- Asynchronous (non-blocking)
- Use existing EmailService if available
```

---

### Phase 2 : Exploration automatique

**Objectif :** Explorer le codebase pour comprendre l'existant.

**Agents lancés automatiquement :**
1. **code-explorer** : Cherche les EventSubscribers existants
2. **pattern-detector** : Identifie le pattern email existant
3. **dependency-mapper** : Trouve EmailService, Mailer, templates

**Output attendu :**
```
✅ Phase 2/9 : Exploration terminée

Patterns détectés :
- EventSubscriber : OrderCreatedSubscriber exists
- EmailService : App\Service\EmailService exists
- Templates : templates/emails/base.html.twig exists
- Messenger : config/packages/messenger.yaml configured

Recommandation : Réutiliser EmailService et créer nouveau template

Document : docs/specs/issue-42-exploration.md
```

---

### Phase 3 : Clarification automatique

**Objectif :** Prendre des décisions techniques sans interaction.

**Heuristiques de décision :**
1. **Réutiliser ou créer ?** → Réutiliser EmailService existant
2. **EventSubscriber ou Command ?** → EventSubscriber (pattern existant)
3. **Template Twig ou HTML pur ?** → Twig (pattern existant)
4. **Tests unitaires ou fonctionnels ?** → Les deux

**Output attendu :**
```
✅ Phase 3/9 : Clarifications automatiques

Décisions :
✅ Réutiliser EmailService existant
✅ Créer OrderValidatedSubscriber (pattern cohérent)
✅ Template Twig (templates/emails/order_validated.html.twig)
✅ Tests unitaires + fonctionnels

Document : docs/specs/issue-42-clarifications.md
```

---

### Phase 4 : Design automatique

**Objectif :** Choisir automatiquement la meilleure architecture.

**Scoring automatique des approches :**

**Approche 1 : EventSubscriber + EmailService** (Score : 95)
- ✅ Cohérent avec codebase
- ✅ Réutilise existant
- ✅ Simple à tester

**Approche 2 : Command + Handler** (Score : 70)
- ⚠️  Pattern pas utilisé pour emails
- ⚠️  Plus complexe

**Approche 3 : Listener Doctrine** (Score : 40)
- ❌ Couplage fort
- ❌ Difficile à tester

**Choix automatique :** Approche 1 (score le plus élevé)

**Output attendu :**
```
✅ Phase 4/9 : Architecture choisie

Approche sélectionnée : EventSubscriber + EmailService (score 95)

Architecture :
1. App\EventSubscriber\OrderValidatedSubscriber
2. Template templates/emails/order_validated.html.twig
3. Tests avec EmailAssertions

Document : docs/specs/issue-42-design.md
```

---

### Phase 5 : Génération du plan

**Objectif :** Générer un plan d'implémentation détaillé.

**Plan généré automatiquement :**

**Output attendu :**
```
✅ Phase 5/9 : Plan d'implémentation généré

Fichiers à créer :
1. src/EventSubscriber/OrderValidatedSubscriber.php
2. templates/emails/order_validated.html.twig
3. tests/EventSubscriber/OrderValidatedSubscriberTest.php
4. tests/Functional/OrderEmailTest.php

Ordre d'implémentation :
1. Créer template email
2. Créer OrderValidatedSubscriber
3. Écrire tests unitaires
4. Écrire tests fonctionnels
5. Lancer tests

Document : docs/specs/issue-42-plan.md
```

---

### Phase 6 : Implémentation TDD

**Objectif :** Implémenter automatiquement avec TDD.

**Workflow TDD automatique :**
1. Écrire test (rouge)
2. Implémenter minimal (vert)
3. Refactorer
4. Répéter

**Output attendu :**
```
✅ Phase 6/9 : Implémentation terminée

Fichiers créés :
✅ src/EventSubscriber/OrderValidatedSubscriber.php
✅ templates/emails/order_validated.html.twig
✅ tests/EventSubscriber/OrderValidatedSubscriberTest.php
✅ tests/Functional/OrderEmailTest.php

Tests :
✅ 8 tests écrits
✅ 8 tests passent
✅ Coverage : 100%
```

**Code généré :**

`src/EventSubscriber/OrderValidatedSubscriber.php` :
```php
<?php

namespace App\EventSubscriber;

use App\Event\OrderValidatedEvent;
use App\Service\EmailServiceInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

final class OrderValidatedSubscriber implements EventSubscriberInterface
{
    public function __construct(
        private readonly EmailServiceInterface $emailService
    ) {
    }

    public static function getSubscribedEvents(): array
    {
        return [
            OrderValidatedEvent::class => 'onOrderValidated',
        ];
    }

    public function onOrderValidated(OrderValidatedEvent $event): void
    {
        $order = $event->order();

        $this->emailService->send(
            to: $order->user()->email(),
            template: 'emails/order_validated',
            context: [
                'order' => $order,
                'trackingUrl' => '/orders/' . $order->id() . '/track'
            ]
        );
    }
}
```

`templates/emails/order_validated.html.twig` :
```twig
{% extends 'emails/base.html.twig' %}

{% block content %}
    <h1>Votre commande a été validée !</h1>

    <p>Bonjour {{ order.user.name }},</p>

    <p>Votre commande #{{ order.id }} a été validée et est en cours de préparation.</p>

    <h2>Détails de la commande</h2>
    <ul>
        {% for item in order.items %}
            <li>{{ item.product.name }} - {{ item.quantity }} x {{ item.price }}€</li>
        {% endfor %}
    </ul>

    <p><strong>Total : {{ order.total }}€</strong></p>

    <p>
        <a href="{{ trackingUrl }}">Suivre ma commande</a>
    </p>
{% endblock %}
```

---

### Phase 7 : Review avec auto-fix

**Objectif :** Review automatique et correction des erreurs.

**Agents de review :**
1. PHPStan niveau 9
2. Elegant Objects checker
3. Code reviewer
4. Test analyzer

**Auto-fix automatique :**
- Erreurs PHPStan → Correction automatique
- Violations Elegant Objects → Refactoring automatique
- Tests manquants → Génération automatique

**Output attendu :**
```
✅ Phase 7/9 : Review terminée - Score : 98/100

PHPStan : ✅ 0 errors (2 auto-fixés)
Elegant Objects : ✅ 100% conforme
Code Review : ✅ Aucun problème
Tests : ✅ 100% coverage

Auto-fixes appliqués :
- OrderValidatedSubscriber:12 : Type hint ajouté
- OrderEmailTest:24 : Assertion améliorée

Document : docs/specs/issue-42-review.md
```

---

### Phase 8 : Création de la PR

**Objectif :** Créer automatiquement la PR sur GitHub.

**Actions automatiques :**
1. Créer branche `feature/issue-42-email-notification`
2. Commit avec message conventionnel
3. Push vers origin
4. Créer PR avec gh CLI

**Output attendu :**
```
✅ Phase 8/9 : PR créée

Branche : feature/issue-42-email-notification
Commit : ✨ feat(email): add notification on order validation

Closes #42

PR #123 : https://github.com/user/repo/pull/123

Titre : feat(email): Add notification on order validation
Description :
## Summary
- Add OrderValidatedSubscriber
- Add email template
- Add comprehensive tests

Closes #42

## Test Plan
- [x] PHPStan level 9 passes
- [x] Unit tests pass (8 tests)
- [x] Functional tests pass
- [x] Email sent asynchronously
```

---

### Phase 9 : Résumé et next steps

**Objectif :** Générer un résumé complet.

**Output attendu :**
```
✅ Phase 9/9 : Workflow terminé !

📊 Résumé :
- Issue : #42 (Add email notification)
- Durée : 12 minutes
- Fichiers créés : 4
- Tests : 8 (100% coverage)
- Score review : 98/100
- PR : #123

📄 Documents générés :
- docs/specs/issue-42-discovery.md
- docs/specs/issue-42-exploration.md
- docs/specs/issue-42-clarifications.md
- docs/specs/issue-42-design.md
- docs/specs/issue-42-plan.md
- docs/specs/issue-42-review.md
- docs/specs/issue-42-summary.md

🚀 Next steps :
1. Reviewer la PR : https://github.com/user/repo/pull/123
2. Tester manuellement avec Postman
3. Merger après CI vert
4. Déployer en staging
```

## Exemple Complet

### Scénario : Issue #56 "Add product search API endpoint"

**Issue GitHub #56 :**
```
Title: Add product search API endpoint

Description:
Create a REST API endpoint to search products by name.

Requirements:
- GET /api/products/search?q={query}
- Return JSON array of products
- Limit to 20 results
- Case-insensitive search

Acceptance criteria:
- Endpoint returns 200 with products
- Empty query returns all products (limited to 20)
- Non-existent product returns empty array
```

**Commande :**
```bash
/dev:auto-feature 56
```

**Workflow automatique :**

1. **Phase -1 :** Prérequis ✅
2. **Phase 0 :** Issue récupérée ✅
3. **Phase 1 :** Découverte → Type: REST API, Entités: Product
4. **Phase 2 :** Exploration → API Platform détecté, ProductRepository existant
5. **Phase 3 :** Clarification → Utiliser API Platform custom operation
6. **Phase 4 :** Design → Custom StateProvider (score 90)
7. **Phase 5 :** Plan → Créer SearchProductsProvider + tests
8. **Phase 6 :** Implémentation TDD ✅
9. **Phase 7 :** Review → Score 96/100 ✅
10. **Phase 8 :** PR #124 créée ✅
11. **Phase 9 :** Résumé généré ✅

**Durée totale :** 8 minutes

**Résultat :**
- PR créée : https://github.com/user/repo/pull/124
- 6 tests (100% coverage)
- Score review : 96/100
- Ready to merge

## Variantes

### Workflow semi-automatique

Si tu veux valider chaque phase :
```bash
/dev:feature
```

Voir [Workflow feature complet](/usecases/development/full-feature-workflow).

### Workflow avec review manuelle avant PR

```bash
/dev:auto-feature 42 --pause-before-pr
```

Claude s'arrête après la Phase 7 pour review manuelle.

### Workflow en mode draft PR

```bash
/dev:auto-feature 42 --draft
```

Crée une Draft PR au lieu d'une PR normale.

## Troubleshooting

### Erreur Phase 0 : Issue not found

**Symptôme :** `Issue #42 not found`

**Solution :**
1. Vérifier que l'issue existe : `gh issue view 42`
2. Vérifier les permissions : `gh auth status`
3. Vérifier le repository : `gh repo view`

### Erreur Phase 4 : Cannot choose architecture

**Symptôme :** `All approaches scored < 50`

**Solution :**

Le codebase est trop inconsistant. Passer en mode manuel :
```bash
/dev:feature
```

### Erreur Phase 6 : Tests failed

**Symptôme :** `Implementation failed: 3 tests failing`

**Solution :**

1. Lire les erreurs de test dans la console
2. Corriger manuellement
3. Relancer `/dev:auto-code` pour continuer

### Erreur Phase 7 : Review score < 80

**Symptôme :** `Review score: 68/100 - Cannot proceed`

**Solution :**

1. Lire `docs/specs/issue-42-review.md`
2. Corriger les erreurs critiques
3. Relancer `/dev:auto-review`

### Erreur Phase 8 : Cannot create PR

**Symptôme :** `gh pr create failed`

**Solution :**
1. Vérifier permissions : `gh auth refresh`
2. Vérifier branch : `git status`
3. Créer manuellement : `gh pr create`

## Liens Connexes

**Use cases :**
- [Workflow feature complet](/usecases/development/full-feature-workflow)
- [Créer PR avec QA](/usecases/git-workflow/create-pr-with-qa)
- [Multi-plugin orchestration](/usecases/advanced/multi-plugin-orchestration)

**Plugins :**
- [Dev](/plugins/dev)
- [GitHub](/plugins/github)
- [Git](/plugins/git)
- [QA](/plugins/qa)
- [Review](/plugins/review)

**Documentation :**
- [GitHub CLI](https://cli.github.com/)
- [Task Management](https://code.claude.com/docs)

## Tips & Best Practices

### ✅ Bonnes pratiques

- **Issues bien rédigées** : Plus l'issue est détaillée, meilleur est le résultat
- **Acceptance criteria** : Toujours inclure des critères d'acceptation
- **Labels** : Utiliser des labels (`enhancement`, `bug`, `backend`, `frontend`)
- **Templates** : Utiliser des templates d'issues GitHub

### 🔍 Optimisations

**Template d'issue optimal :**
```markdown
## Description
[Description claire du problème]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes
[Contraintes techniques, dépendances, etc.]
```

**Hooks GitHub Actions :**
```yaml
# .github/workflows/auto-feature.yml
name: Auto Feature
on:
  issues:
    types: [labeled]

jobs:
  auto-feature:
    if: contains(github.event.issue.labels.*.name, 'auto-feature')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run auto feature
        run: |
          /dev:auto-feature ${{ github.event.issue.number }}
```

### 🎯 Métriques de qualité

Un workflow automatisé réussi c'est :
- ✅ 10 phases complétées
- ✅ Score review > 90/100
- ✅ 100% tests passent
- ✅ PHPStan niveau 9 vert
- ✅ PR créée et mergeable
- ✅ Durée < 15 minutes

### ⏱️ Temps moyen par phase

- Phase -1 : ~30s (checks)
- Phase 0 : ~10s (fetch issue)
- Phase 1 : ~2 min (discovery)
- Phase 2 : ~3 min (exploration)
- Phase 3 : ~1 min (clarifications)
- Phase 4 : ~1 min (design)
- Phase 5 : ~1 min (plan)
- Phase 6 : ~5 min (code)
- Phase 7 : ~2 min (review)
- Phase 8 : ~30s (PR)
- Phase 9 : ~30s (summary)

**Total moyen : 10-15 min**

## Checklist Validation

Avant de lancer :

- [ ] Issue bien rédigée avec acceptance criteria
- [ ] Labels ajoutés (`enhancement`, `bug`, etc.)
- [ ] GitHub CLI authentifié
- [ ] Prérequis installés (PHPStan, tests)
- [ ] Branch main à jour

Pendant le workflow :

- [ ] Phase -1 : Prérequis validés
- [ ] Phase 0 : Issue récupérée
- [ ] Phase 1 : Discovery OK
- [ ] Phase 2 : Exploration OK
- [ ] Phase 3 : Clarifications OK
- [ ] Phase 4 : Architecture choisie
- [ ] Phase 5 : Plan généré
- [ ] Phase 6 : Tests passent
- [ ] Phase 7 : Score > 90
- [ ] Phase 8 : PR créée
- [ ] Phase 9 : Summary généré

Après le workflow :

- [ ] PR visible sur GitHub
- [ ] CI/CD lancé et vert
- [ ] Reviewers notifiés
- [ ] Issue liée à la PR
- [ ] Documentation à jour
