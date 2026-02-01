---
title: Code review automatisé multi-agents
description: Review complète avec 4 agents parallèles pour détecter bugs, violations et problèmes de qualité
category: development
plugins:
  - name: review
    skills: []
  - name: qa
    skills: [/qa:elegant-objects, /qa:phpstan-resolver]
complexity: 3
duration: 5
keywords: [review, quality, agents, parallel, phpstan, elegant-objects, tests]
related:
  - /usecases/development/full-feature-workflow
  - /usecases/git-workflow/create-pr-with-qa
  - /usecases/development/phpstan-error-resolution
---

# Code review automatisé multi-agents <Badge type="info" text="★★★ Avancé" /> <Badge type="tip" text="~5 min" />

## Contexte

Faire une review de code complète manuellement prend du temps et on peut rater des bugs subtils, violations de principes ou problèmes de tests. Une review automatisée avec agents spécialisés permet d'avoir un feedback rapide et complet.

## Objectif

Lancer une review complète avec 4 agents parallèles :

- ✅ **code-reviewer** - Bugs, sécurité, best practices
- ✅ **silent-failure-hunter** - Erreurs silencieuses, catch vides
- ✅ **test-analyzer** - Couverture et qualité des tests
- ✅ **git-history-reviewer** - Analyse historique (blame, PRs précédentes)

**Output :** Score sur 100 avec seuil de 80 pour validation.

## Prérequis

**Plugins :**
- [review](/plugins/review) - Agents de review
- [qa](/plugins/qa) - PHPStan et Elegant Objects

**Outils :**
- Git configuré
- PHPStan niveau 9
- Tests PHPUnit
- Coverage tool (phpunit --coverage)

**Configuration :**
Aucune configuration particulière nécessaire.

## Workflow Étape par Étape

### Phase 1 : Lancer la review complète

**Commande :**
```bash
/dev:review
```

**Que se passe-t-il ?**

Claude lance 4 agents en parallèle qui analysent le code récemment modifié :

**Agent 1 - code-reviewer :**
- Analyse bugs potentiels
- Vérifie sécurité (SQL injection, XSS, etc.)
- Détecte violations CLAUDE.md
- Check best practices PHP/Symfony

**Agent 2 - silent-failure-hunter :**
- Détecte `catch` vides
- Identifie erreurs ignorées silencieusement
- Trouve fallbacks sans logging
- Check gestion d'erreurs inadéquate

**Agent 3 - test-analyzer :**
- Analyse couverture de code
- Vérifie qualité des tests
- Détecte tests manquants critiques
- Check assertions faibles

**Agent 4 - git-history-reviewer :**
- Analyse `git blame` pour contexte
- Check PRs précédentes similaires
- Détecte patterns de bugs récurrents
- Identifie zones à risque

**Output attendu :**
```
🔍 Code Review - Analyse en cours...

✅ code-reviewer : 24/25 (96%)
✅ silent-failure-hunter : 25/25 (100%)
⚠️  test-analyzer : 18/25 (72%)
✅ git-history-reviewer : 22/25 (88%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SCORE GLOBAL : 89/100 ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Critiques (0)
  Aucune erreur critique

⚠️  Avertissements (3)
  1. UserController:42 - Méthode trop complexe (cyclomatic 12)
  2. OrderService:108 - Test manquant pour cas d'erreur
  3. EmailService:24 - Fallback sans logging

💡 Suggestions (5)
  1. Ajouter type hints partout
  2. Utiliser constantes pour magic numbers
  3. Extraire méthodes longues
  4. Améliorer messages d'erreur
  5. Ajouter tests edge cases

Détails : docs/specs/code-review-2026-02-01.md
```

## Exemple Complet

### Scénario : Review d'une PR "Add order validation"

**Code modifié :**
- `src/Service/OrderValidationService.php` (nouveau)
- `src/Controller/OrderController.php` (modifié)
- `tests/Service/OrderValidationServiceTest.php` (nouveau)

**Commande :**
```bash
/dev:review
```

**Résultats détaillés :**

### Agent 1 - code-reviewer (22/25 - 88%)

**✅ Positif :**
- Architecture propre (Hexagonal)
- Injection de dépendances correcte
- Type hints stricts
- Pas de SQL injection

**⚠️ Problèmes détectés :**

```php
// OrderController.php:45
public function validateOrder(int $orderId): Response
{
    $order = $this->repository->find($orderId); // ❌ Peut retourner null
    $this->validationService->validate($order); // Crash si null
}

// Suggestion : Ajouter null check
if (!$order) {
    throw new OrderNotFoundException($orderId);
}
```

```php
// OrderValidationService.php:28
if ($order->total() > 1000) { // ❌ Magic number
    throw new OrderTooExpensiveException();
}

// Suggestion : Utiliser constante
private const MAX_ORDER_TOTAL = 1000;

if ($order->total() > self::MAX_ORDER_TOTAL) {
```

### Agent 2 - silent-failure-hunter (23/25 - 92%)

**✅ Positif :**
- Pas de catch vides
- Erreurs bien propagées
- Logging présent

**⚠️ Problèmes détectés :**

```php
// OrderValidationService.php:42
try {
    $this->externalApi->check($order);
} catch (ApiException $e) {
    // ❌ Exception ignorée silencieusement, pas de logging
    return false; // Fallback silencieux
}

// Suggestion : Logger l'erreur
} catch (ApiException $e) {
    $this->logger->error('External API check failed', [
        'order_id' => $order->id(),
        'error' => $e->getMessage()
    ]);
    return false;
}
```

### Agent 3 - test-analyzer (16/25 - 64%)

**✅ Positif :**
- Tests unitaires présents
- Factory Foundry utilisée
- Assertions correctes

**❌ Problèmes critiques :**

```
Missing tests (5 critiques) :
1. OrderValidationService::validate() - Cas d'erreur API non testé
2. OrderController::validateOrder() - Cas order not found non testé
3. OrderValidationService - Cas order > 1000€ non testé
4. OrderController - Cas de concurrence (2 validations simultanées) non testé
5. Integration test manquant (end-to-end validation flow)

Coverage : 78% (seuil : 80%)
  - OrderValidationService.php : 65% ❌
  - OrderController.php : 85% ✅
```

**Suggestions :**

```php
// Ajouter dans OrderValidationServiceTest.php

public function testValidateWithApiFailure(): void
{
    $order = OrderFactory::new()->create();

    $this->apiMock->method('check')->willThrowException(
        new ApiException('API down')
    );

    $this->expectException(OrderValidationException::class);

    $this->service->validate($order);
}

public function testValidateTooExpensiveOrder(): void
{
    $order = OrderFactory::new(['total' => 1500])->create();

    $this->expectException(OrderTooExpensiveException::class);

    $this->service->validate($order);
}
```

### Agent 4 - git-history-reviewer (24/25 - 96%)

**✅ Positif :**
- Pas de patterns de bugs récurrents
- Zone peu modifiée récemment (stable)

**💡 Insights :**

```
Git Blame Analysis :
- OrderController.php:42-50 : Nouveau code (ce commit)
- OrderValidationService.php : 100% nouveau fichier

Historical Issues :
- PR #65 (2 mois ago) : Bug similaire - null check manquant
  → Même pattern détecté dans ce code !

- PR #42 (3 mois ago) : Magic numbers refactorés en constantes
  → Recommandation : appliquer même pattern ici

Related PRs :
- PR #78 : Add payment validation (merged 1 week ago)
  → Code similaire, vérifier cohérence

Risk Assessment :
🟢 Low risk : Nouveau code, bonne couverture de tests
⚠️  Watch : Null checks (pattern récurrent dans ce repo)
```

### Score Final & Recommandations

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SCORE GLOBAL : 79/100 ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Seuil requis : 80
Statut : ⚠️ NEEDS WORK

Actions requises avant merge :
1. ✅ Ajouter null check (OrderController:45)
2. ✅ Extraire magic number en constante
3. ✅ Logger erreur API silencieuse
4. ✅ Ajouter 5 tests manquants critiques
5. ✅ Atteindre coverage 80%

Après corrections :
- Re-lancer /dev:review
- Target score : > 85
```

## Variantes

### Review rapide (2 agents)

```bash
/dev:review --quick
```

Lance seulement code-reviewer + test-analyzer (~2 min).

### Review focus sécurité

```bash
/dev:review --security
```

Active checks sécurité avancés (OWASP top 10).

### Review avec auto-fix

```bash
/dev:review --auto-fix
```

Applique automatiquement les corrections non-critiques (imports, formatting, etc.).

## Troubleshooting

### Score < 80

**Symptôme :** `Score : 72/100 - Needs work`

**Solution :**
1. Lire le rapport détaillé dans `docs/specs/code-review-*.md`
2. Corriger les problèmes critiques
3. Relancer `/dev:review`
4. Itérer jusqu'à score > 80

### Agent timeout

**Symptôme :** `test-analyzer timed out after 5 minutes`

**Solution :**
1. Réduire le scope : `/dev:review --path=src/Service`
2. Ou augmenter timeout dans config
3. Ou lancer agent manuellement

### Faux positifs

**Symptôme :** Agent signale problème qui n'en est pas un

**Solution :**
1. Ajouter commentaire `// @review-ignore` dans le code
2. Ou configurer exclusions dans `.clauderc`

## Liens Connexes

**Use cases :**
- [Workflow feature complet](/usecases/development/full-feature-workflow)
- [Créer PR avec QA](/usecases/git-workflow/create-pr-with-qa)
- [PHPStan error resolution](/usecases/development/phpstan-error-resolution)

**Plugins :**
- [Review](/plugins/review)
- [QA](/plugins/qa)

## Tips & Best Practices

### ✅ Bonnes pratiques

- **Review avant commit** : lancer `/dev:review` avant de commiter
- **Itérer** : ne pas accepter score < 85
- **Apprendre** : lire les rapports pour progresser
- **Automatiser** : ajouter en pre-commit hook

### 🔍 Optimisations

**Pre-commit hook :**
```bash
#!/bin/bash
# .git/hooks/pre-commit

/dev:review --quick

if [ $? -ne 0 ]; then
    echo "❌ Review failed - Fix issues before commit"
    exit 1
fi
```

**CI/CD :**
```yaml
# .github/workflows/review.yml
name: Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run review
        run: /dev:review
      - name: Check score
        run: |
          if [ $SCORE -lt 80 ]; then
            exit 1
          fi
```

### 🎯 Métriques de qualité

Un code de qualité c'est :
- ✅ Score review > 85/100
- ✅ 0 erreurs critiques
- ✅ Coverage > 80%
- ✅ 0 silent failures
- ✅ PHPStan niveau 9 vert

## Checklist Validation

Avant review :

- [ ] Code compilé sans erreur
- [ ] Tests écrits
- [ ] Commit récent

Pendant review :

- [ ] 4 agents lancés
- [ ] Tous terminent sans timeout
- [ ] Rapport généré

Après review :

- [ ] Score ≥ 80
- [ ] Erreurs critiques corrigées
- [ ] Tests manquants ajoutés
- [ ] Documentation à jour
