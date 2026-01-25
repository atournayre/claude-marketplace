#!/usr/bin/env bash
set -euo pipefail

PROMPT_FILE="$1"

if [[ ! -f "$PROMPT_FILE" ]]; then
    echo "❌ Prompt introuvable : $PROMPT_FILE" >&2
    exit 1
fi

CONTENT=$(cat "$PROMPT_FILE")

# Vérifier variables non substituées
UNSUBSTITUTED=$(echo "$CONTENT" | grep -o '{[A-Z_]*}' || true)
if [[ -n "$UNSUBSTITUTED" ]]; then
    echo "❌ Variables non substituées détectées :" >&2
    echo "$UNSUBSTITUTED" | sort -u >&2
    exit 1
fi

# Vérifier sections requises
REQUIRED_SECTIONS=("## Objectif" "## Architecture" "## Plan d'Implémentation" "## Vérification")
for SECTION in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "^$SECTION" "$PROMPT_FILE"; then
        echo "❌ Section manquante : $SECTION" >&2
        exit 1
    fi
done

# Vérifier longueur (pas plus de 2000 lignes pour éviter des prompts trop longs)
LINE_COUNT=$(wc -l < "$PROMPT_FILE")
if [[ $LINE_COUNT -gt 2000 ]]; then
    echo "❌ Prompt trop long : $LINE_COUNT lignes (max 2000)" >&2
    exit 1
fi

echo "✅ Prompt valide ($LINE_COUNT lignes)"
