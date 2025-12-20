#!/bin/bash
# Source de vérité unique pour le mapping type -> emoji
# Conforme aux conventions de git/commands/commit.md
#
# Usage:
#   source commit-emoji.sh
#   emoji=$(get_commit_emoji "feat")
#
# Ou directement:
#   ./commit-emoji.sh feat  # Retourne: ✨

get_commit_emoji() {
    local type="$1"
    case "$type" in
        feat)     echo "✨" ;;
        fix)      echo "🐛" ;;
        docs)     echo "📝" ;;
        style)    echo "💄" ;;
        refactor) echo "♻️" ;;
        perf)     echo "⚡️" ;;
        test)     echo "✅" ;;
        build)    echo "📦️" ;;
        ci)       echo "🚀" ;;
        chore)    echo "🔧" ;;
        revert)   echo "⏪️" ;;
        wip)      echo "🚧" ;;
        hotfix)   echo "🚑️" ;;
        security) echo "🔒️" ;;
        deps)     echo "➕" ;;
        breaking) echo "💥" ;;
        *)        echo "🔧" ;;  # Fallback sur chore
    esac
}

# Liste des types valides
get_valid_commit_types() {
    echo "feat fix docs style refactor perf test build ci chore revert wip hotfix security deps breaking"
}

# Si appelé directement (pas sourcé)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [ -n "$1" ]; then
        get_commit_emoji "$1"
    else
        echo "Usage: $0 <type>" >&2
        echo "Types valides: $(get_valid_commit_types)" >&2
        exit 1
    fi
fi
