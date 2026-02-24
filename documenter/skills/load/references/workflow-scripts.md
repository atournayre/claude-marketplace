# Scripts de workflow Documentation Loader

## Parsing arguments

```bash
# Parser arguments
ARGS=($ARGUMENTS)
FRAMEWORK="${ARGS[0]}"
VERSION="${ARGS[1]}"  # Optionnel

# Validation framework
case "$FRAMEWORK" in
    symfony|api-platform|meilisearch|atournayre-framework|claude)
        echo "Framework: $FRAMEWORK"
        ;;
    *)
        echo "Framework non supporté: $FRAMEWORK" >&2
        echo "Frameworks disponibles:" >&2
        echo "  - symfony" >&2
        echo "  - api-platform" >&2
        echo "  - meilisearch" >&2
        echo "  - atournayre-framework" >&2
        echo "  - claude" >&2
        exit 1
        ;;
esac

# Déterminer agent
case "$FRAMEWORK" in
    symfony)
        AGENT_NAME="symfony-docs-scraper"
        ;;
    api-platform)
        AGENT_NAME="api-platform-docs-scraper"
        ;;
    meilisearch)
        AGENT_NAME="meilisearch-docs-scraper"
        ;;
    atournayre-framework)
        AGENT_NAME="atournayre-framework-docs-scraper"
        ;;
    claude)
        AGENT_NAME="claude-docs-scraper"
        ;;
esac

# Construire paths
if [ -n "$VERSION" ]; then
    DOCS_PATH="docs/${FRAMEWORK}/${VERSION}/"
    README_PATH="~/.claude/docs/${FRAMEWORK}/${VERSION}/README.md"
else
    DOCS_PATH="docs/${FRAMEWORK}/"
    README_PATH="~/.claude/docs/${FRAMEWORK}/README.md"
fi

echo "Paths:"
echo "   - Docs: $DOCS_PATH"
echo "   - README: $README_PATH"
echo "   - Agent: @$AGENT_NAME"
```

## Vérification README

```bash
# Vérifier existence README
if [ ! -f "$README_PATH" ]; then
    echo "README introuvable: $README_PATH" >&2
    echo "Ce fichier doit contenir la liste des URLs à charger" >&2
    exit 1
fi

# Compter URLs
TOTAL_URLS=$(grep -c "^http" "$README_PATH" || echo "0")
if [ "$TOTAL_URLS" -eq 0 ]; then
    echo "Aucune URL trouvée dans $README_PATH" >&2
    exit 1
fi

echo "URLs à traiter: $TOTAL_URLS"
```

## Gestion cache

```bash
set -euo pipefail

SKIPPED=0
DELETED=0
PROCESSED=0
CACHE_HOURS=24

# Créer répertoire si nécessaire
mkdir -p "$DOCS_PATH"

# Vérifier fichiers existants
while IFS= read -r existing_file; do
    # Calculer âge en heures
    FILE_AGE_SECONDS=$(( $(date +%s) - $(stat -c %Y "$existing_file") ))
    FILE_AGE_HOURS=$(( FILE_AGE_SECONDS / 3600 ))

    if [ "$FILE_AGE_HOURS" -lt "$CACHE_HOURS" ]; then
        echo "Ignoré (récent): $existing_file ($FILE_AGE_HOURS h)"
        SKIPPED=$((SKIPPED + 1))
    else
        echo "Supprimé (ancien): $existing_file ($FILE_AGE_HOURS h)"
        rm "$existing_file"
        DELETED=$((DELETED + 1))
    fi
done < <(find "$DOCS_PATH" -name "*.md" -type f)

echo "Cache:"
echo "   - Fichiers ignorés (récents): $SKIPPED"
echo "   - Fichiers supprimés (anciens): $DELETED"
```

## Chargement documentation

```bash
set -euo pipefail

CREATED=0
ERRORS=0

# Lire URLs depuis README
while IFS= read -r url; do
    # Générer nom fichier depuis URL
    FILENAME=$(echo "$url" | sed 's|https\?://||' | tr '/: ' '___' | sed 's|_$||').md
    FILEPATH="${DOCS_PATH}${FILENAME}"

    # Vérifier si déjà traité (skipped dans cache)
    if [ -f "$FILEPATH" ]; then
        echo "Déjà existant: $FILEPATH"
        continue
    fi

    echo "Traitement: $url"

    # Déléguer à agent via Task tool
    # L'agent lit l'URL, convertit en markdown, sauvegarde dans FILEPATH
    echo "Utiliser agent @$AGENT_NAME avec URL: $url"

    # Vérifier succès
    if [ -f "$FILEPATH" ]; then
        FILE_SIZE=$(du -k "$FILEPATH" | cut -f1)
        echo "Créé: $FILEPATH (${FILE_SIZE}KB)"
        CREATED=$((CREATED + 1))
    else
        echo "Échec: $url" >&2
        ERRORS=$((ERRORS + 1))
    fi

    # Délai anti-rate-limit
    sleep 2
done < <(grep "^http" "$README_PATH")

PROCESSED=$((CREATED + ERRORS))
```

## Statistiques finales

```bash
set -euo pipefail

# Compter fichiers totaux
TOTAL_FILES=$(find "$DOCS_PATH" -name "*.md" -type f | wc -l)

# Taille totale
TOTAL_SIZE_KB=$(du -sk "$DOCS_PATH" | cut -f1)
TOTAL_SIZE_MB=$(awk "BEGIN {printf \"%.2f\", $TOTAL_SIZE_KB / 1024}")

# Couverture
if [ "$TOTAL_URLS" -gt 0 ]; then
    COVERAGE=$(awk "BEGIN {printf \"%.1f\", ($TOTAL_FILES / $TOTAL_URLS) * 100}")
else
    COVERAGE="0"
fi

echo ""
echo "Statistiques finales:"
echo "   - URLs totales: $TOTAL_URLS"
echo "   - Fichiers documentation: $TOTAL_FILES"
echo "   - Taille totale: ${TOTAL_SIZE_MB}MB"
echo "   - Couverture: ${COVERAGE}%"
```

## Gestion Rate Limiting

**IMPORTANT** : En cas d'erreurs 429/401 :

1. Délai de 2-3s entre requêtes (déjà implémenté)
2. Réduire parallélisme si nécessaire
3. Retry avec backoff exponentiel (5s, 10s, 20s)
4. Noter URLs en échec dans rapport final
