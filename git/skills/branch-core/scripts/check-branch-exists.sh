#!/usr/bin/env bash
# check-branch-exists.sh
# Vérifie qu'une branche n'existe pas déjà (pour empêcher les doublons).
#
# Usage: bash check-branch-exists.sh <branch-name>
#
# Exit codes:
#   0 - La branche n'existe PAS (ok pour créer)
#   1 - La branche existe déjà (erreur)

set -euo pipefail

BRANCH_NAME="${1:-}"

if [ -z "$BRANCH_NAME" ]; then
  echo "❌ ERREUR : Aucun nom de branche fourni" >&2
  echo "Usage: check-branch-exists.sh <branch-name>" >&2
  exit 1
fi

if git branch --list "$BRANCH_NAME" | grep -q .; then
  echo "❌ ERREUR : La branche '$BRANCH_NAME' existe déjà" >&2
  echo "" >&2
  echo "Choisis un autre nom de branche" >&2
  exit 1
fi
