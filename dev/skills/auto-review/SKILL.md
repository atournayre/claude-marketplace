---
name: dev:auto:review
description: Review avec auto-fix automatique - Mode AUTO (Phase 7)
model: sonnet
allowed-tools:
  - Task
  - Bash
  - Read
  - Grep
  - Glob
version: 1.0.0
license: MIT
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `reviewer:review`. Voir le plugin `reviewer`. Sera supprimée en v3.0.

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Phase 7 du workflow automatisé : review de qualité **avec correction automatique**.

Boucle auto-fix max 3 tentatives. Si ça échoue → ROLLBACK + CLEANUP + EXIT 1.

# Instructions

## 1. Lire le contexte

Déterminer le chemin du workflow state :

```bash
# Récupérer issue_number depuis le contexte
workflow_state_file=".claude/data/workflows/issue-${issue_number}-dev-workflow-state.json"
```

- Lire le workflow state pour les fichiers modifiés (Phase 6)
- Si phase 6 non complétée, exit avec erreur

## 2. Détecter les langages du projet

```bash
# Déterminer les langages présents (peut être multi-langage)
LANGUAGES=()
QA_TOOLS=()

# Vérifier PHP
if [ -f "composer.json" ] && [ -f "vendor/bin/phpstan" ]; then
    LANGUAGES+=("php")
    QA_TOOLS+=("phpstan")
fi

# Vérifier JavaScript
if [ -f "package.json" ]; then
    LANGUAGES+=("javascript")
    # Utiliser eslint ou prettier selon disponibilité
    if command -v eslint &> /dev/null; then
        QA_TOOLS+=("eslint")
    fi
fi

# Vérifier Go
if [ -f "go.mod" ]; then
    LANGUAGES+=("go")
    QA_TOOLS+=("golangci-lint")
fi

if [ ${#LANGUAGES[@]} -eq 0 ]; then
    echo "⚠️ Aucun langage détecté. Skipping review automatique."
    exit 0
fi
```

## 3. Boucle de correction automatique (max 3 tentatives par langage)

```bash
# Lancer la review pour CHAQUE langage
for i in "${!LANGUAGES[@]}"; do
    language="${LANGUAGES[$i]}"
    tool="${QA_TOOLS[$i]}"

    echo ""
    echo "🔍 Reviewing $language (outil: $tool)..."

    attempt=1
    max_attempts=3
    qa_exit_code=0

    while [ $attempt -le $max_attempts ]; do
        echo "  Tentative $attempt/$max_attempts..."

        # 1. Lancer l'outil de qualité
        case "$language" in
            "php")
                qa_output=$(vendor/bin/phpstan analyse --level=9 2>&1)
                qa_exit_code=$?
                qa_errors=$(echo "$qa_output" | grep -c "error:" || true)
                qa_name="PHPStan niveau 9"
                ;;
            "javascript")
                qa_output=$(eslint . 2>&1)
                qa_exit_code=$?
                qa_errors=$(echo "$qa_output" | grep -c "error" || true)
                qa_name="ESLint"
                ;;
            "go")
                qa_output=$(golangci-lint run 2>&1)
                qa_exit_code=$?
                qa_name="golangci-lint"
                ;;
        esac

        # 2. Vérifier succès
        if [ $qa_exit_code -eq 0 ]; then
            echo "  ✅ $qa_name : PASS"
            break  # Success for this language!
        fi

        echo "  ⚠️ $qa_name : erreurs détectées"

        # 3. Auto-fix si applicable
        if [ "$language" = "php" ] && [ $attempt -lt $max_attempts ]; then
            echo "  🔧 Auto-fix en cours..."
            /qa:phpstan
        fi

        attempt=$((attempt + 1))
    done

    # 4. Vérifier succès final pour ce langage
    if [ $qa_exit_code -ne 0 ]; then
        echo "❌ ÉCHEC : $qa_name impossible après $max_attempts tentatives"
        echo ""
        echo "Erreurs :"
        echo "$qa_output"
        echo ""
        exit 1
    fi
done

# 5. Elegant Objects review (si PHP)
if [[ " ${LANGUAGES[@]} " =~ " php " ]]; then
    echo ""
    echo "🔍 Elegant Objects review..."
    elegant_output=$(/qa:elegant-objects 2>&1)
fi

echo ""
echo "✅ Review automatique complète (tous les langages)"
```

## 4. Consolider les résultats

Afficher un résumé :

```
🔍 Résultats de la review automatique

**Langage détecté :** {PROJECT_LANGUAGE}

**Outil de qualité :** {QA_TOOL}
✅ PASS (0 erreur après $attempt tentative(s))

**Elegant Objects (si PHP) :**
- Score : {score}/100
- Violations : {nombre}
- Status : {warning|pass}

**Tentatives :**
- Tentative 1 : 5 erreurs → 2 erreurs
- Tentative 2 : 2 erreurs → 0 erreurs ✅
```

## 5. Mettre à jour le workflow state

```json
{
  "currentPhase": 7,
  "phases": {
    "7": {
      "status": "completed",
      "completedAt": "{ISO timestamp}",
      "durationMs": {durée},
      "autoFixes": [
        {
          "attempt": 1,
          "tool": "phpstan",
          "errorsBefore": 5,
          "errorsAfter": 2,
          "duration": "15s"
        },
        {
          "attempt": 2,
          "tool": "phpstan",
          "errorsBefore": 2,
          "errorsAfter": 0,
          "duration": "8s"
        }
      ],
      "finalStatus": {
        "phpstan": "passed",
        "elegantObjects": {
          "score": 85,
          "violations": 3,
          "status": "warning"
        }
      }
    }
  }
}
```

# Critères d'abandon (FAIL)

- **PHPStan niveau 9** : 3 tentatives max → **FAIL si toujours des erreurs**
- **Elegant Objects violations** : LOG WARNING mais continuer (non-bloquant pour CI)
- **Tests unitaires** : Si Phase 5 inclut des tests et ils échouent → **FAIL**

# Gestion des erreurs bloquantes

Si PHPStan échoue après 3 tentatives :

```markdown
1. **Loguer l'erreur** dans `.dev-workflow-state.json` :
   ```json
   {
     "status": "failed",
     "failedAt": "{ISO timestamp}",
     "failurePhase": 7,
     "failureReason": "PHPStan niveau 9 impossible après 3 tentatives",
     "errors": ["{error1}", "{error2}"]
   }
   ```

2. **Déclencher ROLLBACK** (à implémenter dans feature.md)
3. **Cleanup worktree** automatique
4. **Exit code 1**

Message d'erreur :
```
❌ ÉCHEC du workflow automatique

Raison : PHPStan niveau 9 impossible après 3 tentatives
Phase : 6 (Review)

Erreurs détectées :
{erreurs}

Le worktree a été nettoyé et la branche supprimée.

Utilise /dev:feature pour un workflow interactif avec review manuel.
```
```

# Règles

- ✅ **Boucle auto-fix max 3 tentatives**
- ✅ **PHPStan niveau 9 DOIT passer**
- ⚠️ **Elegant Objects** : warning seulement (non-bloquant)
- ❌ **Zéro demande "Fix now/later/proceed"**
- ✅ **Documenter chaque tentative**
- ✅ **FAIL et ROLLBACK si impossible**
