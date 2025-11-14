#!/usr/bin/env bash
# Lance tous les tests du projet claude-plugin

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "🧪 Lancement tests Claude Plugin Marketplace"
echo "=============================================="
echo ""

TOTAL_TESTS=0
FAILED_PLUGINS=()

# Trouver et lancer tous les scripts de tests (sauf celui-ci)
while IFS= read -r test_script; do
    # Ignorer le script racine
    if [ "$test_script" = "./run_tests.sh" ]; then
        continue
    fi

    plugin_name=$(echo "$test_script" | sed 's|./||' | sed 's|/tests/run_tests.sh||')
    echo "📦 Plugin: $plugin_name"
    echo "---"

    if bash "$test_script"; then
        echo "✅ $plugin_name OK"
    else
        echo "❌ $plugin_name FAILED"
        FAILED_PLUGINS+=("$plugin_name")
    fi
    echo ""
done < <(find . -name "run_tests.sh" -type f ! -path "./.git/*" ! -path "./.idea/*")

# Résumé
echo "=============================================="
if [ ${#FAILED_PLUGINS[@]} -eq 0 ]; then
    echo "✅ Tous les tests passés"
    exit 0
else
    echo "❌ Échecs détectés dans:"
    for plugin in "${FAILED_PLUGINS[@]}"; do
        echo "  - $plugin"
    done
    exit 1
fi
