#!/usr/bin/env bash
# validate-source-branch.sh
# Valide qu'une branche source existe localement.
#
# Usage: bash validate-source-branch.sh <source-branch>
#
# Exit codes:
#   0 - La branche existe
#   1 - La branche n'existe pas (affiche les branches disponibles)

set -euo pipefail

SOURCE_BRANCH="${1:-}"

if [ -z "$SOURCE_BRANCH" ]; then
  echo "❌ ERREUR : Aucune branche source fournie" >&2
  echo "Usage: validate-source-branch.sh <source-branch>" >&2
  exit 1
fi

if ! git branch --list "$SOURCE_BRANCH" | grep -q .; then
  echo "❌ ERREUR : La branche source '$SOURCE_BRANCH' n'existe pas localement" >&2
  echo "" >&2
  echo "Branches disponibles :" >&2
  git branch -a >&2
  exit 1
fi
