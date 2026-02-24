---
title: "reviewer"
description: "Skills de review de code : qualité, PHPStan, Elegant Objects, challenge adversarial"
version: "1.1.0"
---

# reviewer <Badge type="info" text="v1.1.0" />

Skills de review de code : qualité, PHPStan, Elegant Objects, challenge adversarial.

## Installation

```bash
/plugin install reviewer@atournayre
```

## Skills Disponibles

Le plugin reviewer fournit 4 skills :

### `/reviewer:review`

Review qualité complète — PHPStan + Elegant Objects + code review + adversarial.

### `/reviewer:phpstan`

Résout automatiquement les erreurs PHPStan niveau 9 — boucle jusqu'à zéro erreur.

### `/reviewer:elegant-objects`

Vérifie la conformité du code PHP aux principes Elegant Objects de Yegor Bugayenko.

### `/reviewer:challenge`

Évalue la dernière réponse Claude, donne une note sur 10 et propose des améliorations.

## Agents

- **code-reviewer** : Review de code complète — scoring 0-100 avec seuil 80
- **elegant-objects-reviewer** : Vérifie la conformité aux principes Elegant Objects
- **phpstan-error-resolver** : Analyse et corrige les erreurs PHPStan niveau 9
- **git-history-reviewer** : Analyse le contexte historique git pour détecter des problèmes potentiels
- **silent-failure-hunter** : Détecte les erreurs silencieuses et gestion d'erreurs inadéquate
- **qa** : Découverte dynamique et exécution de tous les outils QA du projet

## Changelog

- Voir CHANGELOG.md
