#!/bin/bash

# Script d'assignation d'une Pull Request à un projet GitHub
# Usage: ./assign_github_project.sh <PR_NUMBER> [OWNER] [REPO]
#
# Arguments:
#   PR_NUMBER : Numéro de la Pull Request
#   OWNER     : Propriétaire du repository (optionnel, utilise le remote origin par défaut)
#   REPO      : Nom du repository (optionnel, utilise le remote origin par défaut)
#
# Retourne:
#   0 si succès
#   1 si échec ou annulation
#
# Exemple:
#   ./assign_github_project.sh 123
#   ./assign_github_project.sh 123 myorg myrepo

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validation des arguments
if [ $# -lt 1 ]; then
    echo -e "${RED}Erreur: Numéro de PR requis${NC}"
    echo "Usage: $0 <PR_NUMBER> [OWNER] [REPO]"
    exit 1
fi

PR_NUMBER=$1
OWNER=${2:-$(gh repo view --json owner --jq '.owner.login' 2>/dev/null || echo "")}
REPO=${3:-$(gh repo view --json name --jq '.name' 2>/dev/null || echo "")}

# Vérification des paramètres
if [ -z "$OWNER" ] || [ -z "$REPO" ]; then
    echo -e "${RED}Erreur: Impossible de déterminer le repository${NC}"
    echo "Veuillez spécifier OWNER et REPO ou exécuter depuis un repository git"
    exit 1
fi

echo -e "${BLUE}📋 Récupération des projets GitHub pour ${OWNER}/${REPO}...${NC}"

# Récupérer la liste des projets
PROJECTS=$(gh api graphql -f query="
query {
  repository(owner: \"$OWNER\", name: \"$REPO\") {
    projectsV2(first: 20, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        id
        title
        closed
        updatedAt
      }
    }
  }
}" --jq '.data.repository.projectsV2.nodes[] | select(.closed == false) | {id: .id, title: .title}' 2>/dev/null)

if [ -z "$PROJECTS" ]; then
    echo -e "${YELLOW}⚠️  Aucun projet GitHub ouvert trouvé${NC}"
    echo "La PR ne sera pas assignée à un projet"
    exit 0
fi

# Créer un tableau des projets
declare -a PROJECT_IDS
declare -a PROJECT_TITLES
INDEX=1

echo -e "\n${GREEN}Projets GitHub disponibles :${NC}"
while IFS= read -r line; do
    if [ -n "$line" ]; then
        PROJECT_ID=$(echo "$line" | jq -r '.id')
        PROJECT_TITLE=$(echo "$line" | jq -r '.title')
        PROJECT_IDS+=("$PROJECT_ID")
        PROJECT_TITLES+=("$PROJECT_TITLE")
        echo "[$INDEX] 📋 $PROJECT_TITLE"
        ((INDEX++))
    fi
done <<< "$(echo "$PROJECTS" | jq -c '.')"

# Ajouter l'option d'ignorer
echo "[$INDEX] ❌ Ignorer (pas de projet)"
echo ""

# Demander la sélection
echo -e "${YELLOW}⚠️  OBLIGATOIRE - Choisir le projet [1-$INDEX]:${NC}"
read -r CHOICE

# Validation du choix
if ! [[ "$CHOICE" =~ ^[0-9]+$ ]] || [ "$CHOICE" -lt 1 ] || [ "$CHOICE" -gt "$INDEX" ]; then
    echo -e "${RED}Choix invalide${NC}"
    exit 1
fi

# Si l'utilisateur choisit d'ignorer
if [ "$CHOICE" -eq "$INDEX" ]; then
    echo -e "${BLUE}ℹ️  Assignation au projet ignorée${NC}"
    exit 0
fi

# Récupérer l'ID du projet sélectionné
SELECTED_INDEX=$((CHOICE - 1))
SELECTED_PROJECT_ID="${PROJECT_IDS[$SELECTED_INDEX]}"
SELECTED_PROJECT_TITLE="${PROJECT_TITLES[$SELECTED_INDEX]}"

echo -e "${BLUE}🔄 Assignation de la PR #$PR_NUMBER au projet '$SELECTED_PROJECT_TITLE'...${NC}"

# Récupérer l'ID GraphQL de la PR
PR_NODE_ID=$(gh pr view "$PR_NUMBER" --json id --jq '.id' 2>/dev/null)

if [ -z "$PR_NODE_ID" ]; then
    echo -e "${RED}Erreur: Impossible de récupérer l'ID de la PR #$PR_NUMBER${NC}"
    exit 1
fi

# Assigner la PR au projet
RESULT=$(gh api graphql -f query="
mutation {
  addProjectV2ItemById(input: {
    projectId: \"$SELECTED_PROJECT_ID\"
    contentId: \"$PR_NODE_ID\"
  }) {
    item {
      id
    }
  }
}" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PR #$PR_NUMBER ajoutée au projet '$SELECTED_PROJECT_TITLE'${NC}"

    # Afficher l'URL du projet si possible
    PROJECT_URL="https://github.com/$OWNER/$REPO/projects"
    echo -e "${BLUE}📍 Voir le projet: $PROJECT_URL${NC}"

    exit 0
else
    echo -e "${RED}❌ Erreur lors de l'assignation au projet${NC}"
    echo "Vérifiez les permissions et réessayez"
    exit 1
fi