#!/bin/bash
#
# Affiche les notifications avec formatage coloré
#

QUEUE_FILE="${CLAUDE_FILE_QUEUE_FILE:-$HOME/.claude/notifications/queue.jsonl}"

# Couleurs
RESET='\033[0m'
BOLD='\033[1m'
DIM='\033[2m'
GRAY='\033[90m'
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
CYAN='\033[36m'

format_notification() {
    local line="$1"

    # Extraire les champs JSON
    local timestamp=$(echo "$line" | jq -r '.timestamp' | cut -d'T' -f2 | cut -d'.' -f1)
    local emoji=$(echo "$line" | jq -r '.emoji')
    local message=$(echo "$line" | jq -r '.message')
    local priority=$(echo "$line" | jq -r '.priority')

    # Couleur selon priorité
    local color="$GREEN"
    case "$priority" in
        critical) color="$RED$BOLD" ;;
        high)     color="$YELLOW" ;;
        normal)   color="$GREEN" ;;
        low)      color="$GRAY" ;;
    esac

    echo -e "${GRAY}[$timestamp]${RESET} ${color}${emoji} ${message}${RESET}"
}

# Header
echo -e "${BOLD}${CYAN}"
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║              Claude Code - Notifications History                  ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"
echo -e "${DIM}Queue file: $QUEUE_FILE${RESET}"
echo ""

if [[ ! -f "$QUEUE_FILE" ]]; then
    echo "❌ Aucune notification pour le moment"
    exit 0
fi

# Compter les notifications
TOTAL=$(wc -l < "$QUEUE_FILE")
echo -e "${BOLD}Total : $TOTAL notifications${RESET}"
echo ""

# Afficher les 20 dernières
echo -e "${BOLD}Dernières notifications :${RESET}"
echo ""

tail -20 "$QUEUE_FILE" | while IFS= read -r line; do
    format_notification "$line"
done

echo ""
echo -e "${DIM}─────────────────────────────────────────────────────────────────────${RESET}"
echo ""
echo "💡 Commandes utiles :"
echo "   watch-notifications.sh     # Surveiller en temps réel"
echo "   tail -f $QUEUE_FILE | jq   # Voir le JSON complet"
echo ""
