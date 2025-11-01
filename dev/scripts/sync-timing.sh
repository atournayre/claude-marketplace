#!/bin/bash
set -e

# Script de synchronisation de la section Timing
# Source de vérité : _templates/timing-section.md

TEMPLATE="_templates/timing-section.md"
COMMANDS_DIR="commands"

if [ ! -f "$TEMPLATE" ]; then
    echo "❌ Erreur: Template non trouvé: $TEMPLATE"
    exit 1
fi

echo "📖 Lecture du template depuis $TEMPLATE"
TIMING_CONTENT=$(cat "$TEMPLATE")

echo "🔍 Recherche des commandes avec section Timing..."
COMMAND_FILES=$(grep -rl "^## Timing" "$COMMANDS_DIR" --include="*.md" | sort)
TOTAL=$(echo "$COMMAND_FILES" | wc -l)

echo "📝 $TOTAL commandes trouvées"
echo ""

COUNT=0
for file in $COMMAND_FILES; do
    echo "⚙️  Migration: $file"

    # Utiliser Python pour le remplacement précis
    python3 << EOF
import re

with open('$file', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern qui capture tout entre "## Timing" et la prochaine section ##
pattern = r'(## Timing\s*\n\n)(.*?)(\n\n## [A-Z])'
timing_content = '''$TIMING_CONTENT'''

result = re.sub(pattern, r'\1' + timing_content + r'\3', content, flags=re.DOTALL)

if result != content:
    with open('$file', 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"   ✓ Mis à jour")
else:
    print(f"   ⚠ Aucun changement")
EOF

    COUNT=$((COUNT + 1))
done

echo ""
echo "✅ $COUNT/$TOTAL commandes synchronisées"
echo ""
echo "Vérification:"
MIGRATED=$(grep -r "JAMAIS inventer/halluciner" "$COMMANDS_DIR" --include="*.md" | cut -d: -f1 | sort -u | wc -l)
echo "   Commandes avec nouvelle version: $MIGRATED/$TOTAL"

if [ "$MIGRATED" -eq "$TOTAL" ]; then
    echo "   ✅ Toutes les commandes sont synchronisées"
else
    echo "   ⚠️  Certaines commandes n'ont pas été mises à jour"
fi
