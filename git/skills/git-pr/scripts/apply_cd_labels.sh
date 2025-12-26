#!/bin/bash
# Applique les labels CD (version:major/minor/patch, feature flag) à une PR
# Usage: apply_cd_labels.sh <pr_number> <base_branch>
# Détection CD : présence des labels version:* dans le repo
# Output: Labels appliqués ou skip si pas en CD

set -euo pipefail

PR_NUMBER="${1:-}"
BASE_BRANCH="${2:-main}"

if [ -z "$PR_NUMBER" ]; then
    echo "❌ Numéro de PR requis" >&2
    exit 1
fi

# Labels CD attendus
CD_LABELS=("version:major" "version:minor" "version:patch")
FEATURE_FLAG_LABEL="🚩 Feature flag"
FEATURE_FLAG_COMPONENT="templates/components/Feature/Flag.html.twig"

# Fonction pour vérifier si un label existe dans le repo
label_exists() {
    local label="$1"
    gh label list --json name -q ".[].name" | grep -qx "$label" 2>/dev/null
}

# Fonction pour créer un label
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"

    echo "📝 Création du label '$name'..." >&2
    gh label create "$name" --color "$color" --description "$description" 2>/dev/null || true
}

# Vérifier si le projet est en CD (présence d'au moins un label version:*)
echo "🔍 Détection mode CD..." >&2
CD_DETECTED=false
for label in "${CD_LABELS[@]}"; do
    if label_exists "$label"; then
        CD_DETECTED=true
        break
    fi
done

if [ "$CD_DETECTED" = false ]; then
    echo "ℹ️ Projet non CD (labels version:* absents), skip labels CD"
    exit 0
fi

echo "✅ Mode CD détecté" >&2

# S'assurer que tous les labels CD existent, sinon les créer
LABELS_CREATED=()
for label in "${CD_LABELS[@]}"; do
    if ! label_exists "$label"; then
        case "$label" in
            "version:major")
                create_label "$label" "d73a4a" "Breaking change - version majeure"
                ;;
            "version:minor")
                create_label "$label" "0e8a16" "Nouvelle fonctionnalité - version mineure"
                ;;
            "version:patch")
                create_label "$label" "1d76db" "Correction/amélioration - version patch"
                ;;
        esac
        LABELS_CREATED+=("$label")
    fi
done

# Vérifier/créer le label feature flag
if ! label_exists "$FEATURE_FLAG_LABEL"; then
    create_label "$FEATURE_FLAG_LABEL" "fbca04" "Fonctionnalité derrière un feature flag"
    LABELS_CREATED+=("$FEATURE_FLAG_LABEL")
fi

if [ ${#LABELS_CREATED[@]} -gt 0 ]; then
    echo "✅ Labels créés: ${LABELS_CREATED[*]}" >&2
fi

# Déterminer le type de version basé sur la branche et les breaking changes
echo "🔍 Analyse du type de version..." >&2

BRANCH_NAME=$(git branch --show-current)
COMMITS=$(git log --oneline "origin/$BASE_BRANCH..HEAD" 2>/dev/null || echo "")

if [ -z "$COMMITS" ]; then
    echo "⚠️ Aucun commit à analyser" >&2
    exit 0
fi

# Déterminer le type de version
VERSION_LABEL=""

# 1. Check pour breaking change (major) - prioritaire sur tout
if echo "$COMMITS" | grep -qiE '!:|BREAKING CHANGE|breaking:'; then
    VERSION_LABEL="version:major"
    echo "  → Breaking change détecté dans commits → version:major" >&2
# 2. Basé sur le type de branche (pas les commits individuels)
elif echo "$BRANCH_NAME" | grep -qE '^feat/'; then
    VERSION_LABEL="version:minor"
    echo "  → Branche feat/* → version:minor" >&2
# 3. Tout le reste = patch (fix, hotfix, chore, refactor, etc.)
else
    VERSION_LABEL="version:patch"
    echo "  → Branche non-feat → version:patch" >&2
fi

# Détecter feature flag dans les fichiers modifiés
echo "🔍 Détection feature flags..." >&2
FEATURE_FLAG_DETECTED=false

# Vérifier si le composant Feature/Flag est utilisé dans les fichiers modifiés
MODIFIED_FILES=$(git diff --name-only "origin/$BASE_BRANCH..HEAD" 2>/dev/null || echo "")

if [ -n "$MODIFIED_FILES" ]; then
    # Chercher les références au composant dans les fichiers twig modifiés
    for file in $MODIFIED_FILES; do
        if [[ "$file" == *.twig ]] && [ -f "$file" ]; then
            if grep -q "Feature:Flag\|Feature/Flag\|component('Feature:Flag')\|component('Feature/Flag')" "$file" 2>/dev/null; then
                FEATURE_FLAG_DETECTED=true
                echo "  → Feature flag détecté dans $file" >&2
                break
            fi
        fi
    done
fi

# Appliquer les labels
LABELS_TO_APPLY=()

if [ -n "$VERSION_LABEL" ]; then
    LABELS_TO_APPLY+=("$VERSION_LABEL")
fi

if [ "$FEATURE_FLAG_DETECTED" = true ]; then
    LABELS_TO_APPLY+=("$FEATURE_FLAG_LABEL")
fi

if [ ${#LABELS_TO_APPLY[@]} -eq 0 ]; then
    echo "ℹ️ Aucun label CD à appliquer"
    exit 0
fi

# Construire la commande pour appliquer les labels
LABEL_ARGS=""
for label in "${LABELS_TO_APPLY[@]}"; do
    LABEL_ARGS="$LABEL_ARGS --add-label \"$label\""
done

eval "gh pr edit $PR_NUMBER $LABEL_ARGS"

echo "✅ Labels CD appliqués à PR #$PR_NUMBER:"
for label in "${LABELS_TO_APPLY[@]}"; do
    echo "  - $label"
done
