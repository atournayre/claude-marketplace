#!/bin/bash
# Collecte les statistiques git en une fois
# Usage: analyze_changes.sh
# Output: JSON avec stats des changements

set -euo pipefail

# Vérifier outils requis
command -v jq >/dev/null 2>&1 || { echo "jq requis" >&2; exit 1; }

# Collecter stats en un seul appel
NUMSTAT=$(git diff --cached --numstat)

# Guard si aucun changement stagé
if [ -z "$NUMSTAT" ]; then
    cat <<EOF
{
  "files_changed": 0,
  "additions": 0,
  "deletions": 0,
  "modified_files": [],
  "has_php_files": false
}
EOF
    exit 0
fi

FILES_CHANGED=$(echo "$NUMSTAT" | wc -l)
ADDITIONS=$(echo "$NUMSTAT" | awk '{sum+=$1} END {print sum+0}')
DELETIONS=$(echo "$NUMSTAT" | awk '{sum+=$2} END {print sum+0}')

# Lister fichiers modifiés
MODIFIED_FILES=$(git diff --cached --name-only | jq -R . | jq -s .)

# Détecter fichiers PHP
HAS_PHP_FILES=false
if git diff --cached --name-only | grep -q '\.php$'; then
    HAS_PHP_FILES=true
fi

# Générer JSON
cat <<EOF
{
  "files_changed": $FILES_CHANGED,
  "additions": $ADDITIONS,
  "deletions": $DELETIONS,
  "modified_files": $MODIFIED_FILES,
  "has_php_files": $HAS_PHP_FILES
}
EOF
