#!/usr/bin/env bash
# Lance tous les tests unitaires du skill git-pr

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TEST_DIR"

echo "🧪 Lancement tests git-pr..."
echo ""

python3 test_milestone_cache.py -v
echo ""

python3 test_project_cache.py -v
echo ""

echo "✅ Tous les tests passés"
