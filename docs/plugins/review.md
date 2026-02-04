---
title: "review"
description: "Agents spécialisés pour la code review automatique des PRs. Inclut 4 agents  - code-reviewer, silent-failure-hunter, test-analyzer, git-history-reviewer."
version: "1.0.1"
---

# review <Badge type="info" text="v1.0.1" />


Agents spécialisés pour la code review automatique des Pull Requests.

## Agents inclus

| Agent | Description |
|-------|-------------|
| **code-reviewer** | Review complète : conformité CLAUDE.md, détection bugs, qualité code. Scoring 0-100 (seuil 80). |
| **silent-failure-hunter** | Détecte catch vides, erreurs silencieuses, fallbacks non justifiés, gestion d'erreurs inadéquate. |
| **test-analyzer** | Analyse couverture PHPUnit : tests manquants, edge cases, qualité comportementale vs implémentation. |
| **git-history-reviewer** | Contexte historique : git blame, PRs précédentes, TODOs/FIXMEs existants. |

## Intégration avec /git:pr

Ce plugin est utilisé par le skill `/git:pr` du plugin `git` pour la review automatique.

Si ce plugin n'est pas installé, `/git:pr` affichera un message d'incitation à l'installer.

## Utilisation standalone

Les agents peuvent être invoqués directement :

```
"Review mon code pour conformité CLAUDE.md"
→ Déclenche code-reviewer

"Vérifie la gestion d'erreurs dans mes changements"
→ Déclenche silent-failure-hunter

"Analyse la couverture de tests de ma PR"
→ Déclenche test-analyzer

"Montre-moi le contexte historique des fichiers modifiés"
→ Déclenche git-history-reviewer
```

## Architecture

```
review/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── code-reviewer.md
│   ├── silent-failure-hunter.md
│   ├── test-analyzer.md
│   └── git-history-reviewer.md
└── README.md
```

## Spécificités PHP/Symfony

Les agents sont adaptés pour :
- **PHPStan niveau 9** - Vérification des @throws, types stricts
- **Conditions Yoda** - `null === $value`
- **Conventions françaises** - Variables, messages, documentation
- **Exceptions métier** - Classes *Invalide du projet
- **PHPUnit 10** - Analyse des tests comportementaux
- **Docker obligatoire** - Rappels des commandes make

## Scoring

Tous les agents utilisent un scoring de confiance 0-100 :
- **0-25** : Faux positif probable
- **26-50** : Nitpick mineur
- **51-75** : Valide mais faible impact
- **76-90** : Important
- **91-100** : Critique

**Seuil de rapport : >= 80**
