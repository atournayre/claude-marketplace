#!/bin/bash
# Applique les labels CD (version:major/minor/patch, feature flag) à une PR
# Usage: apply_cd_labels.sh <pr_number> <base_branch> [issue_number]
# Détection CD : présence des labels version:* dans le repo
# Output: Labels appliqués ou skip si pas en CD
# Exit codes: 0=OK, 1=erreur, 2=besoin input utilisateur (VERSION_TYPE non déterminé)

set -euo pipefail

PR_NUMBER="${1:-}"
BASE_BRANCH="${2:-main}"
ISSUE_NUMBER="${3:-}"

if [ -z "$PR_NUMBER" ]; then
    echo "❌ Numéro de PR requis" >&2
    exit 1
fi

# Labels CD attendus
CD_LABELS=("version:major" "version:minor" "version:patch")
FEATURE_FLAG_LABEL="🚩 Feature flag"

# Patterns de détection (insensibles à la casse, ignorent emojis/préfixes)
# Ces patterns matchent si le label CONTIENT le mot clé
MINOR_PATTERNS="enhancement|feature|feat|nouvelle|new"
PATCH_PATTERNS="bug|fix|bugfix|correction|patch"

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

# Fonction pour nettoyer un label (retirer emojis, lowercase)
normalize_label() {
    echo "$1" | sed 's/[^a-zA-Z0-9 ]//g' | tr '[:upper:]' '[:lower:]' | xargs
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

# Déterminer le type de version
echo "🔍 Analyse du type de version..." >&2

BRANCH_NAME=$(git branch --show-current)
COMMITS=$(git log --oneline "origin/$BASE_BRANCH..HEAD" 2>/dev/null || echo "")

if [ -z "$COMMITS" ]; then
    echo "⚠️ Aucun commit à analyser" >&2
    exit 0
fi

VERSION_LABEL=""
DETECTION_SOURCE=""

# 1. Check pour breaking change (major) - TOUJOURS prioritaire
if echo "$COMMITS" | grep -qiE '!:|BREAKING CHANGE|breaking:'; then
    VERSION_LABEL="version:major"
    DETECTION_SOURCE="breaking change dans commits"
fi

# 2. Si pas major, chercher dans les labels de l'issue liée
if [ -z "$VERSION_LABEL" ] && [ -n "$ISSUE_NUMBER" ]; then
    ISSUE_LABELS=$(gh issue view "$ISSUE_NUMBER" --json labels -q '.labels[].name' 2>/dev/null || echo "")

    if [ -n "$ISSUE_LABELS" ]; then
        # Normaliser et chercher les patterns
        while IFS= read -r label; do
            NORMALIZED=$(normalize_label "$label")

            if echo "$NORMALIZED" | grep -qiE "$MINOR_PATTERNS"; then
                VERSION_LABEL="version:minor"
                DETECTION_SOURCE="label issue '$label'"
                break
            elif echo "$NORMALIZED" | grep -qiE "$PATCH_PATTERNS"; then
                VERSION_LABEL="version:patch"
                DETECTION_SOURCE="label issue '$label'"
                # Continue chercher, minor a priorité sur patch
            fi
        done <<< "$ISSUE_LABELS"
    fi
fi

# 3. Si toujours pas déterminé, regarder le nom de branche
if [ -z "$VERSION_LABEL" ]; then
    if echo "$BRANCH_NAME" | grep -qiE '^(feat|feature)/'; then
        VERSION_LABEL="version:minor"
        DETECTION_SOURCE="branche feat/*"
    elif echo "$BRANCH_NAME" | grep -qiE '^(fix|hotfix|bugfix)/'; then
        VERSION_LABEL="version:patch"
        DETECTION_SOURCE="branche fix/*"
    fi
fi

# 4. Si toujours pas déterminé, regarder le premier commit
if [ -z "$VERSION_LABEL" ]; then
    FIRST_COMMIT=$(git log --oneline --reverse "origin/$BASE_BRANCH..HEAD" 2>/dev/null | head -1 || echo "")

    if echo "$FIRST_COMMIT" | grep -qiE '(✨ )?feat(\(|:)'; then
        VERSION_LABEL="version:minor"
        DETECTION_SOURCE="premier commit feat"
    elif echo "$FIRST_COMMIT" | grep -qiE '(🐛 )?fix(\(|:)'; then
        VERSION_LABEL="version:patch"
        DETECTION_SOURCE="premier commit fix"
    fi
fi

# 5. Si toujours indéterminé → signaler besoin d'input utilisateur
if [ -z "$VERSION_LABEL" ]; then
    echo "⚠️ NEED_USER_INPUT: Impossible de déterminer le type de version" >&2
    echo "  - Branche: $BRANCH_NAME" >&2
    echo "  - Issue: ${ISSUE_NUMBER:-aucune}" >&2
    echo "  - Veuillez spécifier: minor (nouvelle fonctionnalité) ou patch (correction)" >&2
    # On continue sans label version, feature flag sera quand même appliqué si détecté
fi

if [ -n "$VERSION_LABEL" ]; then
    echo "  → $DETECTION_SOURCE → $VERSION_LABEL" >&2
fi

# Détecter feature flag dans les fichiers modifiés
echo "🔍 Détection feature flags..." >&2
FEATURE_FLAG_DETECTED=false

MODIFIED_FILES=$(git diff --name-only "origin/$BASE_BRANCH..HEAD" 2>/dev/null || echo "")

if [ -n "$MODIFIED_FILES" ]; then
    for file in $MODIFIED_FILES; do
        if [[ "$file" == *.twig ]] && [ -f "$file" ]; then
            if grep -qE "Feature:Flag|Feature/Flag|component\(['\"]Feature" "$file" 2>/dev/null; then
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
    if [ -z "$VERSION_LABEL" ]; then
        echo "⚠️ Aucun label version appliqué (détection impossible)"
        exit 2  # Code spécial: besoin input utilisateur
    fi
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

# Si version indéterminée mais feature flag appliqué
if [ -z "$VERSION_LABEL" ]; then
    exit 2
fi
