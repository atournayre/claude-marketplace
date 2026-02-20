---
name: reviewer:review
description: Review qualité complète — PHPStan + Elegant Objects + code review + adversarial
model: sonnet
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, Bash, Read, Grep, Glob, Edit]
version: 1.0.0
license: MIT
---

# Review Qualité Complète

Review qualité complète du code implémenté : PHPStan, Elegant Objects, code review et analyse adversariale.

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### 1. Créer les tâches de review

Utiliser TaskCreate pour chaque tâche :

```
TaskCreate #1: Code Review — Simplicité/bugs/conventions
TaskCreate #2: PHPStan — Résoudre erreurs niveau 9
TaskCreate #3: Elegant Objects — Conformité principes
TaskCreate #4: Consolider — Agréger résultats et décider
TaskCreate #5: Examine — Adversarial review (edge cases, architecture)
```

- Utiliser `activeForm` pour chaque tâche (ex: "Reviewing code quality", "Résolvant erreurs PHPStan")
- Les 3 premières tâches peuvent se lancer en parallèle
- La tâche #4 dépend des 3 premières (`addBlockedBy`)
- La tâche #5 dépend de #4 (`addBlockedBy`)

### 2. Lancer les reviews en parallèle

Marquer les 3 premières tâches en `in_progress`.

#### Review 1 : Code Review

Lancer l'agent `reviewer/code-reviewer` avec le focus sur :
- Simplicité / DRY / Élégance
- Bugs / Correction fonctionnelle
- Conventions du projet (CLAUDE.md)

#### Review 2 : PHPStan

Lancer l'agent `reviewer/phpstan-error-resolver`.

#### Review 3 : Elegant Objects

Lancer l'agent `reviewer/elegant-objects-reviewer`.

### 3. Consolider les résultats

Agréger les résultats des 3 reviews.

Classifier les issues :
- **BLOQUANT** : PHPStan erreurs, bugs critiques, violations CLAUDE.md
- **IMPORTANT** : Violations Elegant Objects majeures, code quality élevé
- **MINEUR** : Recommandations, nitpicks

### 4. Analyse adversariale (Examine)

Challenge l'implémentation avec une perspective adversariale :

**Questions à poser :**
- **Edge cases** : Qu'arrive-t-il si input null/vide/invalide ?
- **Limites** : Quelle est la taille maximale acceptable ? Le timeout ?
- **Sécurité** : Injection possible ? Exposition de données sensibles ?
- **Performance** : N+1 queries ? Boucles infinies possibles ?
- **Concurrence** : Race conditions ? Deadlocks ?
- **Rollback** : Comment annuler si ça échoue en prod ?
- **Décisions d'architecture** : Pourquoi ce pattern ? Alternative meilleure ?

**Output :**
```
Examine Results:

Edge cases trouvés:
- [cas] : [risque] → [suggestion]

Limites détectées:
- [limite] : [impact] → [mitigation]

Décisions challengées:
- [décision] : [alternative] → [trade-off]
```

### 5. Demander l'action utilisateur

```
Que souhaites-tu faire ?

1. Fix now — Corriger toutes les issues maintenant
2. Fix later — Noter pour plus tard et continuer
3. Proceed — Continuer sans corrections (non recommandé)
```

Attendre la décision avant de continuer.

### 6. Si "Fix now" choisi

- Appliquer les corrections PHPStan en priorité (bloquent la CI)
- Appliquer les corrections Elegant Objects
- Relancer une review pour vérifier

## Règles

- **PHPStan erreurs = BLOQUANT** (font échouer la CI)
- Confiance minimum 80% pour les issues code review
- Respecter le choix utilisateur (ne pas forcer les corrections)
- Ne JAMAIS créer de commits Git
