---
title: Résoudre les conflits merge
description: Workflow interactif pour résoudre les conflits git avec validation étape par étape
category: git-workflow
plugins:
  - name: git
    skills: [/git:conflit]
complexity: 3
duration: 10
keywords: [git, merge, conflicts, resolution]
related:
  - /usecases/git-workflow/create-pr-with-qa
  - /usecases/git-workflow/fix-pr-comments
---

# Résoudre les conflits merge <Badge type="info" text="★★★ Avancé" /> <Badge type="tip" text="~10 min" />

## Contexte

Les conflits git surviennent lors du merge de branches divergentes. Les résoudre manuellement peut être complexe et source d'erreurs.

## Objectif

Résoudre les conflits git de manière guidée avec :

- ✅ Analyse automatique des conflits
- ✅ Suggestions de résolution
- ✅ Validation étape par étape
- ✅ Tests après résolution
- ✅ Commit automatique

## Prérequis

**Plugins :**
- [git](/plugins/git) - Gestion des conflits

**Outils :**
- Git configuré
- Tests PHPUnit

## Workflow

**Commande :**
```bash
/git:conflit
```

**Que se passe-t-il ?**

1. Détection des fichiers en conflit
2. Analyse de chaque conflit
3. Suggestion de résolution (garder incoming, current, ou merge manuel)
4. Validation utilisateur
5. Application de la résolution
6. Tests
7. Commit

**Output attendu :**
```
🔍 Analyse des conflits...

Conflits détectés : 3 fichiers

src/Service/OrderService.php:
  Conflit ligne 42-56
  Current (main): méthode validate() v1
  Incoming (feature): méthode validate() v2

  Suggestion : Garder incoming (version plus récente)
  Appliquer ? [y/n]

✅ Conflit résolu
✅ Tests passent
✅ Commit créé
```

## Troubleshooting

### Conflit complexe

**Solution :** Résoudre manuellement puis relancer `/git:conflit` pour valider.

### Tests en échec

**Solution :** Corriger le code puis relancer la résolution.

## Liens Connexes

**Use cases :**
- [Créer PR avec QA](/usecases/git-workflow/create-pr-with-qa)
- [Corriger review PR](/usecases/git-workflow/fix-pr-comments)

**Plugins :**
- [Git](/plugins/git)
