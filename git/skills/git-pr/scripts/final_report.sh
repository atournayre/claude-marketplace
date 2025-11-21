#!/bin/bash
# Génère le rapport final YAML de la PR
# Usage: final_report.sh <pr_number> <start_time>
# Output: Rapport YAML formaté

set -euo pipefail

PR_NUMBER="$1"
START_TIME="$2"

if [ -z "$PR_NUMBER" ] || [ -z "$START_TIME" ]; then
    echo "❌ Usage: final_report.sh <pr_number> <start_time>" >&2
    exit 1
fi

# Récupérer infos de la PR
PR_INFO=$(gh pr view "$PR_NUMBER" --json title,url,baseRefName,headRefName,additions,deletions,changedFiles 2>/dev/null || echo "{}")

PR_TITLE=$(echo "$PR_INFO" | jq -r '.title // "N/A"')
PR_URL=$(echo "$PR_INFO" | jq -r '.url // "N/A"')
BRANCH_BASE=$(echo "$PR_INFO" | jq -r '.baseRefName // "N/A"')
BRANCH_NAME=$(echo "$PR_INFO" | jq -r '.headRefName // "N/A"')
ADDITIONS=$(echo "$PR_INFO" | jq -r '.additions // 0')
DELETIONS=$(echo "$PR_INFO" | jq -r '.deletions // 0')
FILES_CHANGED=$(echo "$PR_INFO" | jq -r '.changedFiles // 0')

# Calculer durée
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Formater durée
if [ $DURATION -lt 60 ]; then
    DURATION_STR="${DURATION}s"
elif [ $DURATION -lt 3600 ]; then
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    DURATION_STR="${MINUTES}m ${SECONDS}s"
else
    HOURS=$((DURATION / 3600))
    MINUTES=$(((DURATION % 3600) / 60))
    SECONDS=$((DURATION % 60))
    DURATION_STR="${HOURS}h ${MINUTES}m ${SECONDS}s"
fi

# Formater timestamps
START_DATE=$(date -d "@$START_TIME" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -r "$START_TIME" '+%Y-%m-%d %H:%M:%S')
END_DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Générer rapport YAML
cat <<EOF
task: "Pull Request créée avec succès"
status: "completed"

details:
  pr_number: $PR_NUMBER
  pr_title: "$PR_TITLE"
  pr_url: "$PR_URL"
  branch_source: "$BRANCH_NAME"
  branch_base: "$BRANCH_BASE"

stats:
  files_changed: $FILES_CHANGED
  additions: $ADDITIONS
  deletions: $DELETIONS

timing:
  start: "$START_DATE"
  end: "$END_DATE"
  duration: "$DURATION_STR"
EOF
