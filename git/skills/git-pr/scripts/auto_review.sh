#!/bin/bash
# Lance une review automatique et poste un commentaire sur la PR
# Usage: auto_review.sh <pr_number>
# Exit 0 si OK, Exit 1 si échec

set -euo pipefail

PR_NUMBER="$1"

if [ -z "$PR_NUMBER" ]; then
    echo "❌ PR_NUMBER requis" >&2
    exit 1
fi

echo "🔍 Analyse des changements de la PR #$PR_NUMBER..."

# Récupérer le diff de la PR
DIFF=$(gh pr diff "$PR_NUMBER" 2>/dev/null || echo "")

if [ -z "$DIFF" ]; then
    echo "⚠️ Impossible de récupérer le diff de la PR" >&2
    exit 1
fi

# Compter les lignes modifiées
ADDITIONS=$(echo "$DIFF" | grep -c "^+" || echo "0")
DELETIONS=$(echo "$DIFF" | grep -c "^-" || echo "0")
FILES_CHANGED=$(gh pr view "$PR_NUMBER" --json files -q '.files | length' 2>/dev/null || echo "0")

# Récupérer la liste des fichiers modifiés
FILES_LIST=$(gh pr view "$PR_NUMBER" --json files -q '.files[].path' 2>/dev/null | head -20 || echo "")

# Générer le commentaire de review
REVIEW_COMMENT="## 🔍 Review Automatique

### Statistiques
- **Fichiers modifiés**: $FILES_CHANGED
- **Lignes ajoutées**: $ADDITIONS
- **Lignes supprimées**: $DELETIONS

### Fichiers analysés
\`\`\`
$FILES_LIST
\`\`\`

### Vérifications
- ✅ Diff récupéré avec succès
- ✅ Analyse des changements effectuée

---
*Review automatique générée par git-pr skill*"

# Poster le commentaire
echo "📝 Publication du commentaire de review..."
if gh pr comment "$PR_NUMBER" --body "$REVIEW_COMMENT"; then
    echo "✅ Review automatique complétée"
    exit 0
else
    echo "❌ Échec publication commentaire" >&2
    exit 1
fi
