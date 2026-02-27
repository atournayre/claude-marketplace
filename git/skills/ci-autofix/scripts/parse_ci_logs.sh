#!/bin/bash
# Parse les logs CI GitHub Actions pour une PR donnée
# Usage: parse_ci_logs.sh <pr_number>
# Output: JSON avec les erreurs catégorisées

set -euo pipefail

# Vérifier outils requis
command -v gh >/dev/null 2>&1 || { echo "gh CLI requis" >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "jq requis" >&2; exit 1; }

PR_NUMBER="${1:-}"

if [ -z "$PR_NUMBER" ]; then
    echo "❌ Usage: parse_ci_logs.sh <pr_number>" >&2
    exit 1
fi

# Récupérer la branche de la PR
BRANCH=$(gh pr view "$PR_NUMBER" --json headRefName -q '.headRefName' 2>&1) || {
    echo "❌ Impossible de récupérer la branche de la PR #$PR_NUMBER" >&2
    echo "$BRANCH" >&2
    exit 1
}

if [ -z "$BRANCH" ]; then
    echo "❌ Branche vide pour PR #$PR_NUMBER" >&2
    exit 1
fi

# Récupérer le dernier run en échec
RUN_ID=$(gh run list --branch "$BRANCH" --status failure --limit 1 --json databaseId -q '.[0].databaseId' 2>&1) || {
    echo "❌ Impossible de lister les runs CI" >&2
    echo "$RUN_ID" >&2
    exit 1
}

if [ -z "$RUN_ID" ] || [ "$RUN_ID" = "null" ]; then
    echo '{"status": "no_failures", "errors": []}'
    exit 0
fi

# Récupérer les logs du run en échec
LOG_FILE=$(mktemp /tmp/ci_logs_XXXXXX.txt)
trap 'rm -f "$LOG_FILE"' EXIT

gh run view "$RUN_ID" --log-failed > "$LOG_FILE" 2>&1 || {
    echo "❌ Impossible de récupérer les logs du run #$RUN_ID" >&2
    exit 1
}

if [ ! -s "$LOG_FILE" ]; then
    echo '{"status": "empty_logs", "run_id": '"$RUN_ID"', "errors": []}'
    exit 0
fi

# Catégoriser les erreurs
PHPSTAN_ERRORS=$(grep -c 'PHPStan\|phpstan\|------ ' "$LOG_FILE" 2>/dev/null || echo 0)
TEST_ERRORS=$(grep -c 'FAILURES\|ERRORS\|Failed asserting\|PHPUnit' "$LOG_FILE" 2>/dev/null || echo 0)
CS_ERRORS=$(grep -c 'php-cs-fixer\|coding standard\|CS error' "$LOG_FILE" 2>/dev/null || echo 0)
BUILD_ERRORS=$(grep -c 'composer.*error\|npm.*ERR\|build.*failed' "$LOG_FILE" 2>/dev/null || echo 0)

# Extraire les lignes d'erreur pertinentes (max 50)
ERROR_LINES=$(grep -E '(Error|FAIL|ERROR|Fatal|Exception)' "$LOG_FILE" | head -50 | jq -R . | jq -s .)

cat <<EOF
{
  "status": "failures_found",
  "run_id": $RUN_ID,
  "branch": $(echo "$BRANCH" | jq -R .),
  "categories": {
    "phpstan": $PHPSTAN_ERRORS,
    "tests": $TEST_ERRORS,
    "cs_fixer": $CS_ERRORS,
    "build": $BUILD_ERRORS
  },
  "error_lines": $ERROR_LINES
}
EOF
