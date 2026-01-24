---
name: dev:review
description: Review qualité complète - PHPStan + Elegant Objects + code review (Phase 6)
model: claude-sonnet-4-5-20250929
allowed-tools: [Task, Bash, Read, Grep, Glob, Edit]
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

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour récupérer les fichiers modifiés
- Si phase 5 (code) non complétée, rediriger vers `/dev:code`

## 2. Lancer les reviews en parallèle

### Review 1 : Code Review (feature-dev)

Lancer l'agent `code-reviewer` avec le focus sur :
- Simplicité / DRY / Élégance
- Bugs / Correction fonctionnelle
- Conventions du projet

### Review 2 : PHPStan

Lancer l'agent `phpstan-error-resolver` (local)

### Review 3 : Elegant Objects

Lancer l'agent `elegant-objects-reviewer` (local)

## 3. Consolider les résultats

## 4. Demander l'action utilisateur

```
Que souhaites-tu faire ?

1. 🔧 Fix now - Corriger toutes les issues maintenant
2. 📋 Fix later - Noter pour plus tard et continuer
3. ✅ Proceed - Continuer sans corrections (non recommandé)
```

⚠️ **Attendre la décision avant de continuer.**

## 5. Si "Fix now" choisi

- Appliquer les corrections PHPStan en priorité (bloquent la CI)
- Appliquer les corrections Elegant Objects
- Relancer une review pour vérifier

## 6. Mettre à jour le workflow state

# Prochaine étape

```
✅ Review complétée

Prochaine étape : /dev:summary pour le résumé final
```

# Règles

- **PHPStan erreurs = BLOQUANT** (font échouer la CI)
- Confiance minimum 80% pour les issues code review
- Respecter le choix utilisateur (ne pas forcer les corrections)
