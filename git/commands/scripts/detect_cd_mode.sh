#!/bin/bash
# Détecte si le repo est en mode Continuous Delivery
# Output: CD_DETECTED ou STANDARD
# Exit: 0 si CD détecté, 1 sinon
#
# IMPORTANT: Ne pas tronquer les résultats avec head/tail
# La commande doit traiter TOUS les labels du repo

set -euo pipefail

# Récupérer TOUS les labels et chercher ceux qui commencent par "version:"
# IMPORTANT: --limit 1000 car la limite par défaut est 30 labels seulement
if gh label list --limit 1000 --json name -q '.[].name' | grep -q "^version:"; then
    echo "CD_DETECTED"
    exit 0
else
    echo "STANDARD"
    exit 1
fi
