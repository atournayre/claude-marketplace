#!/bin/bash
# Vérifie l'existence du template PR
# Usage: verify_pr_template.sh <chemin_template>
# Exit: 0=ok, 1=absent

set -euo pipefail

TEMPLATE_PATH="${1:-.github/pull_request_template.md}"

if [ ! -f "$TEMPLATE_PATH" ]; then
    echo "❌ Template PR absent: $TEMPLATE_PATH" >&2
    exit 1
fi

echo "✅ Template PR trouvé: $TEMPLATE_PATH"
exit 0
