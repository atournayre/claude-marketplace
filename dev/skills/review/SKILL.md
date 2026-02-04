---
name: dev:review
description: Review qualité complète - PHPStan + Elegant Objects + code review (Phase 6)
model: sonnet
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, Bash, Read, Grep, Glob, Edit]
version: 1.0.0
license: MIT
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: |
            # Hook 1: Tests avant review
            echo "🧪 Exécution des tests avant review..."

            if [ -f "Makefile" ] && grep -q "^test:" Makefile; then
              make test || {
                echo "❌ Tests échoués - corrige-les avant la review"
                exit 1
              }
            elif [ -f "vendor/bin/phpunit" ]; then
              vendor/bin/phpunit || {
                echo "❌ Tests échoués - corrige-les avant la review"
                exit 1
              }
            else
              echo "⚠️  Tests non détectés, review sans validation tests"
            fi
          once: true
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: |
            # Hook 2: Auto-commit après fixes
            if ! git diff --quiet; then
              echo ""
              echo "📝 Corrections appliquées. Prêt pour :"
              echo "   git add ."
              echo "   /git:commit"
              echo ""
              echo "Message suggéré :"
              echo "   🚨 fix: corrections suite à review"
            fi
          once: false
---

# Objectif

Phase 6 du workflow de développement : review qualité complète du code implémenté.

# Prérequis

⚠️ **Plugin feature-dev requis** pour l'agent `code-reviewer`.

Si non installé :
```
/plugin install feature-dev@claude-code-plugins
```

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### 1. Vérifier le contexte

- Lis `.claude/data/.dev-workflow-state.json` avec Read
- Extrais les fichiers modifiés et l'état de la phase 5 (code)
- Si phase 5 non complétée, affiche :
  ```
  ❌ La phase d'implémentation (code) n'est pas terminée

  Lance d'abord : /dev:code
  ```
  - Arrête le workflow

### 2. Créer les tâches de review

- Utilise TaskCreate pour chaque tâche de review :

```
TaskCreate #1: Code Review - Simplicité/bugs/conventions (feature-dev)
TaskCreate #2: PHPStan - Résoudre erreurs niveau 9
TaskCreate #3: Elegant Objects - Conformité principes
TaskCreate #4: Consolider - Agréger résultats et décider
TaskCreate #5: Examine - Adversarial review (challenge decisions, edge cases)
```

**Important :**
- Utiliser `activeForm` (ex: "Reviewing code quality", "Résolvant erreurs PHPStan")
- Les 3 premières tâches peuvent se lancer en parallèle
- La tâche #4 dépend des 3 premières (utiliser `addBlockedBy`)

## 3. Lancer les reviews en parallèle

**⚠️ Avant de lancer les agents :** Marquer les 3 tâches en `in_progress` :
- `TaskUpdate` → tâche #1 en `in_progress`
- `TaskUpdate` → tâche #2 en `in_progress`
- `TaskUpdate` → tâche #3 en `in_progress`

### Review 1 : Code Review (feature-dev)

Lancer l'agent `code-reviewer` avec le focus sur :
- Simplicité / DRY / Élégance
- Bugs / Correction fonctionnelle
- Conventions du projet

**Quand terminé :** `TaskUpdate` → tâche #1 en `completed`

### Review 2 : PHPStan

Lancer l'agent `phpstan-error-resolver` (local)

**Quand terminé :** `TaskUpdate` → tâche #2 en `completed`

### Review 3 : Elegant Objects

Lancer l'agent `elegant-objects-reviewer` (local)

**Quand terminé :** `TaskUpdate` → tâche #3 en `completed`

## 4. Consolider les résultats

**🔄 Progression :** `TaskUpdate` → tâche #4 en `in_progress`

Agréger les résultats des 3 reviews.

**Quand terminé :** `TaskUpdate` → tâche #4 en `completed`

## 4.5. Examine (Adversarial Review) ⭐ NOUVEAU

**🔄 Progression :** `TaskUpdate` → tâche #5 en `in_progress`

Challenge l'implémentation avec perspective adversariale :

**Questions à poser :**
- **Edge cases** : Qu'arrive-t-il si input null/vide/invalide ?
- **Limites** : Quelle est la taille maximale acceptable ? Le timeout ?
- **Sécurité** : Injection possible ? Exposition de données sensibles ?
- **Performance** : N+1 queries ? Boucles infinies possibles ?
- **Concurrence** : Race conditions ? Deadlocks ?
- **Rollback** : Comment annuler si ça échoue en prod ?
- **Décisions d'architecture** : Pourquoi ce pattern ? Alternative meilleure ?

**Focus prioritaire :**
1. Chercher ce qui **pourrait casser** en production
2. Identifier **hypothèses non validées** dans le code
3. Tester mentalement **scénarios extrêmes**
4. Challenger **décisions d'implémentation** (pourquoi X au lieu de Y ?)

**Output :**
```
🔍 Examine Results:

Edge cases trouvés:
- [cas] : [risque] → [suggestion]

Limites détectées:
- [limite] : [impact] → [mitigation]

Décisions challengées:
- [décision] : [alternative] → [trade-off]
```

**Quand terminé :** `TaskUpdate` → tâche #5 en `completed`

## 5. Demander l'action utilisateur

```
Que souhaites-tu faire ?

1. 🔧 Fix now - Corriger toutes les issues maintenant
2. 📋 Fix later - Noter pour plus tard et continuer
3. ✅ Proceed - Continuer sans corrections (non recommandé)
```

⚠️ **Attendre la décision avant de continuer.**

## 6. Si "Fix now" choisi

- Appliquer les corrections PHPStan en priorité (bloquent la CI)
- Appliquer les corrections Elegant Objects
- Relancer une review pour vérifier

## 7. Finaliser

Mettre à jour le workflow state

# Prochaine étape

```
✅ Review complétée

Prochaine étape : /dev:summary pour le résumé final
```

# Règles

- **Task Management** :
  - Créer 5 tâches au démarrage (3 reviews + 1 consolidation + 1 examine)
  - Marquer les 3 reviews en `in_progress` avant lancement parallèle
  - La tâche de consolidation est bloquée par les 3 reviews (`addBlockedBy`)
  - La tâche examine est bloquée par la consolidation (`addBlockedBy`)
  - Utiliser `TaskList` pour afficher la progression
- **PHPStan erreurs = BLOQUANT** (font échouer la CI)
- Confiance minimum 80% pour les issues code review
- Respecter le choix utilisateur (ne pas forcer les corrections)
