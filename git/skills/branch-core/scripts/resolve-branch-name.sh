#!/usr/bin/env bash
# resolve-branch-name.sh
# Script partagé pour résoudre un nom de branche depuis un numéro d'issue ou du texte.
#
# Usage: bash resolve-branch-name.sh <issue-or-text>
#
# Output (KEY=VALUE sur stdout) :
#   BRANCH_NAME     - Nom complet de la branche (ex: feature/42-login-fix)
#   PREFIX          - Préfixe détecté (ex: feature/)
#   PREFIX_SOURCE   - Source de détection (label/description/title/default/text)
#   ISSUE_NUMBER    - Numéro d'issue si applicable (vide sinon)
#   WORKTREE_DIRNAME - Nom du répertoire worktree (ex: feature-42-login-fix)
#
# Exit codes:
#   0 - Succès
#   1 - Erreur (issue introuvable, etc.)

set -euo pipefail

ISSUE_OR_TEXT="${1:-}"

if [ -z "$ISSUE_OR_TEXT" ]; then
  echo "❌ ERREUR : Aucun argument fourni" >&2
  echo "Usage: resolve-branch-name.sh <issue-number-or-text>" >&2
  exit 1
fi

# --- Fonctions utilitaires ---

clean_text() {
  local text="$1"
  local max_length="${2:-50}"
  echo "$text" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9 -]//g' \
    | sed 's/  */ /g' \
    | sed 's/ /-/g' \
    | sed 's/--*/-/g' \
    | sed 's/^-//' \
    | sed 's/-$//' \
    | cut -c1-"$max_length"
}

detect_prefix_from_labels() {
  local labels_json="$1"
  local label_names
  label_names=$(echo "$labels_json" | tr '[:upper:]' '[:lower:]')

  if echo "$label_names" | grep -qE '"(hotfix|critical|urgent)"'; then
    echo "hotfix/"
  elif echo "$label_names" | grep -qE '"(bug|fix|bugfix)"'; then
    echo "fix/"
  elif echo "$label_names" | grep -qE '"(feature|enhancement|new-feature)"'; then
    echo "feature/"
  elif echo "$label_names" | grep -qE '"(chore|maintenance|refactor)"'; then
    echo "chore/"
  elif echo "$label_names" | grep -qE '"(documentation|docs)"'; then
    echo "docs/"
  elif echo "$label_names" | grep -qE '"(test|tests)"'; then
    echo "test/"
  else
    echo ""
  fi
}

detect_prefix_from_text() {
  local text="$1"
  local lower_text
  lower_text=$(echo "$text" | tr '[:upper:]' '[:lower:]')

  if echo "$lower_text" | grep -qiE '(hotfix|critical|urgent|production)'; then
    echo "hotfix/"
  elif echo "$lower_text" | grep -qiE '(fix|bug|error|crash)'; then
    echo "fix/"
  elif echo "$lower_text" | grep -qiE '(feature|add|implement|new)'; then
    echo "feature/"
  elif echo "$lower_text" | grep -qiE '(refactor|cleanup|improve)'; then
    echo "chore/"
  else
    echo ""
  fi
}

detect_prefix_from_start() {
  local text="$1"
  local lower_text
  lower_text=$(echo "$text" | tr '[:upper:]' '[:lower:]')

  case "$lower_text" in
    hotfix*) echo "hotfix/" ;;
    fix*|bug*) echo "fix/" ;;
    chore*|refactor*) echo "chore/" ;;
    docs*|doc\ *) echo "docs/" ;;
    test*) echo "test/" ;;
    *) echo "" ;;
  esac
}

strip_prefix_from_text() {
  local text="$1"
  echo "$text" | sed -E 's/^(hotfix|fix|bug|chore|refactor|docs|doc|test)[[:space:]]*//'
}

# --- Logique principale ---

# Détecter si c'est un numéro d'issue ou du texte
if [[ "$ISSUE_OR_TEXT" =~ ^[0-9]+$ ]]; then
  # --- Mode issue GitHub ---
  ISSUE_NUMBER="$ISSUE_OR_TEXT"

  ISSUE_JSON=$(gh issue view "$ISSUE_NUMBER" --json title,labels,body 2>&1) || {
    echo "❌ ERREUR : L'issue #$ISSUE_NUMBER n'existe pas ou n'est pas accessible" >&2
    echo "$ISSUE_JSON" >&2
    exit 1
  }

  TITLE=$(echo "$ISSUE_JSON" | jq -r '.title // ""')
  BODY=$(echo "$ISSUE_JSON" | jq -r '.body // ""')
  LABELS_JSON=$(echo "$ISSUE_JSON" | jq -c '[.labels[].name]')

  # Détection du préfixe par priorité
  PREFIX=""
  PREFIX_SOURCE=""

  # 1. Labels
  PREFIX=$(detect_prefix_from_labels "$LABELS_JSON")
  if [ -n "$PREFIX" ]; then
    PREFIX_SOURCE="label"
  fi

  # 2. Description
  if [ -z "$PREFIX" ] && [ -n "$BODY" ]; then
    PREFIX=$(detect_prefix_from_text "$BODY")
    if [ -n "$PREFIX" ]; then
      PREFIX_SOURCE="description"
    fi
  fi

  # 3. Titre
  if [ -z "$PREFIX" ] && [ -n "$TITLE" ]; then
    PREFIX=$(detect_prefix_from_text "$TITLE")
    if [ -n "$PREFIX" ]; then
      PREFIX_SOURCE="title"
    fi
  fi

  # 4. Défaut
  if [ -z "$PREFIX" ]; then
    PREFIX="feature/"
    PREFIX_SOURCE="default"
  fi

  CLEAN_TITLE=$(clean_text "$TITLE")
  BRANCH_NAME="${PREFIX}${ISSUE_NUMBER}-${CLEAN_TITLE}"

else
  # --- Mode texte descriptif ---
  ISSUE_NUMBER=""

  # Détection du préfixe par le début du texte
  PREFIX=$(detect_prefix_from_start "$ISSUE_OR_TEXT")
  if [ -n "$PREFIX" ]; then
    PREFIX_SOURCE="text"
    STRIPPED_TEXT=$(strip_prefix_from_text "$ISSUE_OR_TEXT")
  else
    PREFIX="feature/"
    PREFIX_SOURCE="default"
    STRIPPED_TEXT="$ISSUE_OR_TEXT"
  fi

  CLEAN_TEXT=$(clean_text "$STRIPPED_TEXT")
  BRANCH_NAME="${PREFIX}${CLEAN_TEXT}"
fi

# Calculer le nom du répertoire worktree (remplacer / par -)
WORKTREE_DIRNAME=$(echo "$BRANCH_NAME" | tr '/' '-')

# --- Output ---
echo "BRANCH_NAME=$BRANCH_NAME"
echo "PREFIX=$PREFIX"
echo "PREFIX_SOURCE=$PREFIX_SOURCE"
echo "ISSUE_NUMBER=$ISSUE_NUMBER"
echo "WORKTREE_DIRNAME=$WORKTREE_DIRNAME"
