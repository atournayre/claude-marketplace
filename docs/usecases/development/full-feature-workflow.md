---
title: Workflow complet de développement de feature
description: Orchestrateur 8 phases guidé pour développer une feature complète du besoin à la PR
category: development
plugins:
  - name: dev
    skills: [/dev:feature, /dev:discover, /dev:explore, /dev:clarify, /dev:design, /dev:plan, /dev:code, /dev:review, /dev:summary]
  - name: git
    skills: [/git:pr]
  - name: qa
    skills: []
  - name: review
    skills: []
complexity: 4
duration: 45
keywords: [workflow, feature, orchestrateur, tdd, architecture, planning]
related:
  - /usecases/development/auto-feature-from-issue
  - /usecases/git-workflow/create-pr-with-qa
  - /usecases/development/code-review-automation
---

# Workflow complet de développement de feature <Badge type="info" text="★★★★ Expert" /> <Badge type="tip" text="~45 min" />

## Contexte

Développer une feature nécessite plusieurs étapes : comprendre le besoin, explorer le codebase, designer l'architecture, planifier, implémenter, reviewer et créer la PR. Faire tout ça de manière structurée évite les allers-retours et garantit la qualité.

## Objectif

Développer une feature complète en suivant un workflow guidé en 8 phases :

1. **Discover** - Comprendre le besoin utilisateur
2. **Explore** - Explorer le codebase existant
3. **Clarify** - Lever les ambiguïtés
4. **Design** - Designer 2-3 approches architecturales
5. **Plan** - Générer plan d'implémentation détaillé
6. **Code** - Implémenter selon le plan
7. **Review** - QA complète (PHPStan + Elegant Objects + Code Review)
8. **Summary** - Résumé de ce qui a été construit

## Prérequis

**Plugins :**
- [dev](/plugins/dev) - Workflow de développement
- [git](/plugins/git) - Gestion des commits et PR
- [qa](/plugins/qa) - PHPStan et qualité du code
- [review](/plugins/review) - Code review automatique

**Outils :**
- Git configuré
- PHPStan niveau 9
- Tests PHPUnit
- GitHub CLI (`gh`)

**Configuration :**
Aucune configuration particulière nécessaire.

## Workflow Étape par Étape

### Phase 0 : Lancer le workflow

**Commande :**
```bash
/dev:feature
```

**Que se passe-t-il ?**

Claude lance un orchestrateur interactif qui va te guider à travers les 8 phases. À chaque phase, il te demande validation avant de passer à la suivante.

---

### Phase 1 : Discover - Comprendre le besoin

**Objectif :** Analyser le besoin utilisateur et clarifier les exigences.

**Actions automatiques :**
1. Claude pose des questions pour comprendre :
   - Quel est le problème à résoudre ?
   - Qui sont les utilisateurs cibles ?
   - Quels sont les critères de succès ?
   - Y a-t-il des contraintes techniques ?

2. Génère un document de découverte dans `docs/specs/[feature-name]-discovery.md`

**Output attendu :**
```
✅ Discovery document créé
📄 docs/specs/user-authentication-discovery.md

Résumé :
- Problème : Les utilisateurs ne peuvent pas se connecter
- Solution : Système d'auth JWT
- Critères de succès : Login + token refresh
- Contraintes : Compatible avec API Platform
```

**Action utilisateur :** Valider ou modifier le document de découverte.

---

### Phase 2 : Explore - Explorer le codebase

**Objectif :** Comprendre l'architecture existante et identifier les patterns.

**Actions automatiques :**
1. Lance 3 agents parallèles :
   - **code-explorer** : Analyse l'architecture actuelle
   - **pattern-detector** : Identifie les patterns utilisés
   - **dependency-mapper** : Mappe les dépendances

2. Génère `docs/specs/[feature-name]-exploration.md`

**Output attendu :**
```
✅ Exploration terminée
📄 docs/specs/user-authentication-exploration.md

Patterns détectés :
- Architecture Hexagonale (Ports & Adapters)
- Repository Pattern (Doctrine)
- CQRS (Message + Handler)
- Foundry pour fixtures
```

**Action utilisateur :** Valider les patterns identifiés.

---

### Phase 3 : Clarify - Lever les ambiguïtés

**Objectif :** Clarifier les points techniques flous.

**Actions automatiques :**
1. Claude pose des questions ciblées :
   - Quelle librairie JWT utiliser ? (LexikJWTAuthenticationBundle vs custom)
   - Où stocker les tokens ? (Database, Redis, in-memory)
   - Refresh token ? (oui/non)

2. Génère `docs/specs/[feature-name]-clarifications.md`

**Output attendu :**
```
✅ Clarifications documentées
📄 docs/specs/user-authentication-clarifications.md

Décisions :
- Librairie : LexikJWTAuthenticationBundle
- Stockage : Database (User entity)
- Refresh : Oui (15 jours)
```

**Action utilisateur :** Répondre aux questions et valider.

---

### Phase 4 : Design - Designer l'architecture

**Objectif :** Proposer 2-3 approches architecturales.

**Actions automatiques :**
1. Claude génère 2-3 approches avec :
   - Architecture détaillée
   - Avantages / Inconvénients
   - Trade-offs

2. Génère `docs/specs/[feature-name]-design.md`

**Output attendu :**
```
✅ 3 approches générées
📄 docs/specs/user-authentication-design.md

Approche 1 : LexikJWT + Doctrine
Avantages : Simple, bien documenté
Inconvénients : Moins flexible

Approche 2 : Custom JWT + Redis
Avantages : Performance, contrôle total
Inconvénients : Maintenance, complexité

Approche 3 : OAuth2 + JWT
Avantages : Standard, SSO ready
Inconvénients : Setup complexe
```

**Action utilisateur :** Choisir l'approche préférée.

---

### Phase 5 : Plan - Générer le plan d'implémentation

**Objectif :** Créer un plan détaillé d'implémentation.

**Actions automatiques :**
1. Basé sur l'approche choisie, génère :
   - Liste des fichiers à créer/modifier
   - Ordre d'implémentation
   - Tests à écrire
   - Tâches détaillées

2. Génère `docs/specs/[feature-name]-plan.md`

**Output attendu :**
```
✅ Plan d'implémentation généré
📄 docs/specs/user-authentication-plan.md

Fichiers à créer :
1. src/Security/JWTAuthenticator.php
2. src/Controller/AuthController.php
3. tests/Security/JWTAuthenticatorTest.php
4. tests/Controller/AuthControllerTest.php

Ordre d'implémentation :
1. Installer LexikJWTAuthenticationBundle
2. Configurer config/packages/lexik_jwt_authentication.yaml
3. Créer JWTAuthenticator
4. Créer AuthController (login + refresh)
5. Écrire tests
```

**Action utilisateur :** Valider le plan.

---

### Phase 6 : Code - Implémenter

**Objectif :** Implémenter la feature selon le plan.

**Actions automatiques :**
1. Claude suit le plan étape par étape
2. Crée/modifie les fichiers dans l'ordre
3. Écrit les tests en parallèle (TDD)
4. Lance les tests après chaque étape

**Output attendu :**
```
✅ Implémentation terminée
✅ Tous les tests passent (12 tests, 45 assertions)

Fichiers créés :
- src/Security/JWTAuthenticator.php
- src/Controller/AuthController.php
- tests/Security/JWTAuthenticatorTest.php
- tests/Controller/AuthControllerTest.php

Fichiers modifiés :
- config/packages/security.yaml
- config/routes.yaml
```

**Action utilisateur :** Tester manuellement si nécessaire.

---

### Phase 7 : Review - QA complète

**Objectif :** Valider la qualité du code avant PR.

**Actions automatiques :**
1. Lance 4 agents parallèles :
   - **PHPStan level 9** : Analyse statique stricte
   - **elegant-objects-reviewer** : Vérifie conformité Elegant Objects
   - **code-reviewer** : Review générale (bugs, sécurité, best practices)
   - **test-analyzer** : Analyse couverture et qualité des tests

2. Génère `docs/specs/[feature-name]-review.md`

**Output attendu :**
```
✅ Review terminée - Score : 92/100

PHPStan : ✅ 0 errors
Elegant Objects : ✅ 100% conforme
Code Review : ⚠️  2 warnings (non bloquants)
Tests : ✅ 100% coverage

Warnings :
- AuthController:42 : Méthode trop longue (15 lignes, max 10)
- JWTAuthenticator:28 : Commentaire TODO à résoudre
```

**Action utilisateur :** Corriger les warnings si nécessaire.

---

### Phase 8 : Summary - Résumé

**Objectif :** Générer un résumé de la feature.

**Actions automatiques :**
1. Génère `docs/specs/[feature-name]-summary.md` avec :
   - Ce qui a été construit
   - Fichiers créés/modifiés
   - Tests ajoutés
   - Documentation mise à jour
   - Prochaines étapes

**Output attendu :**
```
✅ Summary généré
📄 docs/specs/user-authentication-summary.md

Résumé :
- Feature : Système d'authentification JWT
- Fichiers créés : 4
- Fichiers modifiés : 2
- Tests : 12 (100% coverage)
- Score qualité : 92/100

Prochaines étapes :
1. Créer PR avec /git:pr
2. Tester manuellement avec Postman
3. Déployer en staging
```

**Action utilisateur :** Créer la PR.

---

### Phase finale : Créer la PR

**Commande :**
```bash
/git:pr
```

Voir [Créer PR avec QA](/usecases/git-workflow/create-pr-with-qa).

## Exemple Complet

### Scénario : Ajouter un système de notifications email

**Besoin :**
"Les utilisateurs doivent recevoir un email quand leur commande est validée."

**Workflow complet :**

```bash
/dev:feature
```

**Phase 1 - Discover :**
```
Q: Quel événement déclenche l'email ?
R: Validation de commande (statut "validated")

Q: Quel service email utiliser ?
R: Symfony Mailer + template Twig

Q: Synchrone ou asynchrone ?
R: Asynchrone (Messenger)
```

**Phase 2 - Explore :**
```
✅ Pattern détecté : Messenger + Handler
✅ Template existant : emails/base.html.twig
✅ Service existant : App\Service\EmailService
```

**Phase 3 - Clarify :**
```
Q: Utiliser EmailService existant ou créer un nouveau service ?
R: Réutiliser EmailService

Q: Créer un Message CQRS ou EventSubscriber ?
R: EventSubscriber sur OrderValidatedEvent
```

**Phase 4 - Design :**
```
Approche choisie : EventSubscriber + EmailService

Architecture :
1. App\EventSubscriber\OrderValidatedSubscriber
2. Template emails/order_validated.html.twig
3. Tests fonctionnels avec Foundry
```

**Phase 5 - Plan :**
```
1. Créer OrderValidatedSubscriber
2. Créer template email
3. Modifier EmailService pour supporter nouveau template
4. Écrire tests unitaires + fonctionnels
```

**Phase 6 - Code :**
```
✅ OrderValidatedSubscriber créé
✅ Template email créé
✅ EmailService modifié
✅ 8 tests écrits et passent
```

**Phase 7 - Review :**
```
✅ PHPStan : 0 errors
✅ Elegant Objects : 100%
✅ Code Review : Score 95/100
✅ Tests : 100% coverage
```

**Phase 8 - Summary :**
```
Feature terminée : Notifications email commande validée

Fichiers créés :
- src/EventSubscriber/OrderValidatedSubscriber.php
- templates/emails/order_validated.html.twig
- tests/EventSubscriber/OrderValidatedSubscriberTest.php

Tests : 8 (100% coverage)
```

**Créer PR :**
```bash
/git:pr
```

## Variantes

### Workflow automatisé complet

Pour un workflow 100% automatisé sans interaction :
```bash
/dev:auto-feature
```

Voir [Feature auto depuis issue GitHub](/usecases/development/auto-feature-from-issue).

### Workflow partiel

Pour ne lancer que certaines phases :
```bash
/dev:discover
/dev:explore
/dev:design
# Choisir approche
/dev:plan
/dev:code
```

### Workflow avec issue GitHub

Pour partir d'une issue GitHub :
```bash
/dev:auto-fetch-issue 123
/dev:feature
```

## Troubleshooting

### Erreur en Phase 6 (Code)

**Symptôme :** Tests en échec après implémentation

**Solution :**
1. Analyser les erreurs de test
2. Corriger le code
3. Relancer `/dev:code` ou corriger manuellement
4. Passer à la phase suivante

### Score Review < 80

**Symptôme :** `Review terminée - Score : 72/100`

**Solution :**
1. Lire le rapport détaillé dans `docs/specs/[feature-name]-review.md`
2. Corriger les erreurs critiques
3. Relancer `/dev:review`
4. Si score > 80, passer à la suite

### Agent exploration timeout

**Symptôme :** `code-explorer timed out`

**Solution :**
1. Relancer `/dev:explore` avec scope réduit
2. Ou continuer manuellement en écrivant `docs/specs/[feature-name]-exploration.md`

## Liens Connexes

**Use cases :**
- [Feature auto depuis issue](/usecases/development/auto-feature-from-issue)
- [Code review automatisé](/usecases/development/code-review-automation)
- [Créer PR avec QA](/usecases/git-workflow/create-pr-with-qa)

**Plugins :**
- [Dev](/plugins/dev)
- [Git](/plugins/git)
- [QA](/plugins/qa)
- [Review](/plugins/review)

**Documentation :**
- [Task Management Claude Code](https://code.claude.com/docs)

## Tips & Best Practices

### ✅ Bonnes pratiques

- **Suivre les 8 phases** : ne pas sauter d'étape pour garantir la qualité
- **Petites features** : décomposer les grandes features en sous-features
- **TDD** : écrire les tests avant le code (Phase 6)
- **Review systématique** : toujours passer par la Phase 7 avant PR

### 🔍 Optimisations

- **Templates de specs** : créer des templates dans `docs/specs/templates/`
- **Hooks pre-commit** : ajouter PHPStan en pre-commit
- **CI/CD** : GitHub Actions qui re-vérifie tout

### 🎯 Métriques de qualité

Un workflow réussi c'est :
- ✅ 8 phases complétées
- ✅ Score review > 85/100
- ✅ 100% tests passent
- ✅ PHPStan niveau 9 vert
- ✅ Documentation à jour

### 📊 Temps moyen par phase

- Discover : ~5 min
- Explore : ~10 min
- Clarify : ~5 min
- Design : ~5 min
- Plan : ~5 min
- Code : ~20-30 min
- Review : ~5 min
- Summary : ~2 min

**Total : 45-60 min** pour une feature moyenne.

## Checklist Validation

Avant de lancer `/dev:feature` :

- [ ] Besoin utilisateur clair
- [ ] Accès au codebase
- [ ] PHPStan + tests configurés
- [ ] Temps disponible (~1h)

Pendant le workflow :

- [ ] Phase 1 : Document discovery validé
- [ ] Phase 2 : Patterns identifiés
- [ ] Phase 3 : Ambiguïtés levées
- [ ] Phase 4 : Approche choisie
- [ ] Phase 5 : Plan détaillé validé
- [ ] Phase 6 : Tests passent
- [ ] Phase 7 : Score > 80
- [ ] Phase 8 : Summary généré

Après le workflow :

- [ ] PR créée avec `/git:pr`
- [ ] CI/CD vert
- [ ] Tests manuels OK
- [ ] Documentation mise à jour
