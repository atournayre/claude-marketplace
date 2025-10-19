#!/bin/bash
# Collecte les statistiques git en une fois
# Usage: analyze_changes.sh
# Output: JSON avec stats des changements

set -euo pipefail

# Collecter stats
FILES_CHANGED=$(git diff --cached --numstat | wc -l)
ADDITIONS=$(git diff --cached --numstat | awk '{sum+=$1} END {print sum+0}')
DELETIONS=$(git diff --cached --numstat | awk '{sum+=$2} END {print sum+0}')

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
