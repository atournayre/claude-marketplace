#!/bin/bash
#
# Bump all modified plugins to PATCH version
#

set -euo pipefail

PLUGINS=("claude" "customize" "dev" "doc" "gemini" "git" "github" "marketing" "prompt" "qa" "review" "symfony")
CURRENT_DATE=$(date +%Y-%m-%d)

for plugin in "${PLUGINS[@]}"; do
    plugin_json="$plugin/.claude-plugin/plugin.json"

    if [ ! -f "$plugin_json" ]; then
        echo "⊘ $plugin: fichier plugin.json non trouvé"
        continue
    fi

    # Extraire version actuelle
    current_version=$(grep -o '"version": "[^"]*"' "$plugin_json" | head -1 | sed 's/"version": "//;s/"//g')

    # Bumper en PATCH
    IFS='.' read -ra parts <<< "$current_version"
    major=${parts[0]}
    minor=${parts[1]}
    patch=${parts[2]:-0}
    new_patch=$((patch + 1))
    new_version="$major.$minor.$new_patch"

    # Mettre à jour plugin.json
    sed -i "s/\"version\": \"$current_version\"/\"version\": \"$new_version\"/" "$plugin_json"

    # Mettre à jour CHANGELOG.md si existe
    changelog="$plugin/CHANGELOG.md"
    if [ -f "$changelog" ]; then
        # Créer une nouvelle section au début
        (
            echo "## [$new_version] - $CURRENT_DATE"
            echo ""
            echo "### Changed"
            echo "- Migrer noms de modèles Claude vers format court (sonnet, haiku, opus)"
            echo ""
            cat "$changelog"
        ) > "$changelog.tmp"
        mv "$changelog.tmp" "$changelog"
    fi

    echo "✓ $plugin: v$current_version → v$new_version"
done

echo ""
echo "Bump terminé !"
