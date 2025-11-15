---
name: doc-loader
description: >
  Charge la documentation d'un framework depuis son site web dans des fichiers markdown
  locaux. Supporte Symfony, API Platform, Meilisearch, atournayre-framework et Claude Code.
  Gère le cache, rate limiting et délègue aux agents scraper spécialisés.
allowed-tools: [Task, WebFetch, Write, Edit, Bash, Read, Glob]
model: claude-sonnet-4-5-20250929
---

# Documentation Loader Skill

## Variables

```bash
ARGUMENTS="$ARGUMENTS"  # <framework> [version]
FRAMEWORK=""
VERSION=""
DOCS_PATH=""
README_PATH=""
CACHE_HOURS=24
AGENT_NAME=""
```

## Frameworks Supportés

| Framework           | Agent                          | Path                                    |
|---------------------|--------------------------------|-----------------------------------------|
| symfony             | symfony-docs-scraper           | docs/symfony/[version]/                 |
| api-platform        | api-platform-docs-scraper      | docs/api-platform/[version]/            |
| meilisearch         | meilisearch-docs-scraper       | docs/meilisearch/[version]/             |
| atournayre-framework| atournayre-framework-docs-scraper | docs/atournayre-framework/[version]/ |
| claude              | claude-docs-scraper            | docs/claude/                            |

## Workflow

### Étape 0: Timing
```bash
START_TIME=$(date +%s)
date
```

### Étape 1: Parsing Arguments

```bash
# Parser arguments
ARGS=($ARGUMENTS)
FRAMEWORK="${ARGS[0]}"
VERSION="${ARGS[1]}"  # Optionnel

# Validation framework
case "$FRAMEWORK" in
    symfony|api-platform|meilisearch|atournayre-framework|claude)
        echo "✅ Framework: $FRAMEWORK"
        ;;
    *)
        echo "❌ Framework non supporté: $FRAMEWORK"
        echo "Frameworks disponibles:"
        echo "  - symfony"
        echo "  - api-platform"
        echo "  - meilisearch"
        echo "  - atournayre-framework"
        echo "  - claude"
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

echo "📁 Paths:"
echo "   - Docs: $DOCS_PATH"
echo "   - README: $README_PATH"
echo "   - Agent: @$AGENT_NAME"
```

### Étape 2: Vérification README

```bash
# Vérifier existence README
if [ ! -f "$README_PATH" ]; then
    echo "❌ README introuvable: $README_PATH"
    echo "Ce fichier doit contenir la liste des URLs à charger"
    exit 1
fi

# Compter URLs
TOTAL_URLS=$(grep -c "^http" "$README_PATH" || echo "0")
if [ "$TOTAL_URLS" -eq 0 ]; then
    echo "❌ Aucune URL trouvée dans $README_PATH"
    exit 1
fi

echo "📋 URLs à traiter: $TOTAL_URLS"
```

### Étape 3: Gestion Cache

```bash
SKIPPED=0
DELETED=0
PROCESSED=0

# Créer répertoire si nécessaire
mkdir -p "$DOCS_PATH"

# Vérifier fichiers existants
find "$DOCS_PATH" -name "*.md" -type f | while read existing_file; do
    # Calculer âge en heures
    FILE_AGE_SECONDS=$(( $(date +%s) - $(stat -c %Y "$existing_file") ))
    FILE_AGE_HOURS=$(( FILE_AGE_SECONDS / 3600 ))

    if [ "$FILE_AGE_HOURS" -lt "$CACHE_HOURS" ]; then
        echo "⏭️ Ignoré (récent): $existing_file ($FILE_AGE_HOURS h)"
        SKIPPED=$((SKIPPED + 1))
    else
        echo "🗑️ Supprimé (ancien): $existing_file ($FILE_AGE_HOURS h)"
        rm "$existing_file"
        DELETED=$((DELETED + 1))
    fi
done

echo "📊 Cache:"
echo "   - Fichiers ignorés (récents): $SKIPPED"
echo "   - Fichiers supprimés (anciens): $DELETED"
```

### Étape 4: Chargement Documentation

```bash
CREATED=0
ERRORS=0

# Lire URLs depuis README
grep "^http" "$README_PATH" | while read url; do
    # Générer nom fichier depuis URL
    FILENAME=$(echo "$url" | sed 's|https\?://||' | sed 's|[/:]|_|g' | sed 's|_$||').md
    FILEPATH="${DOCS_PATH}${FILENAME}"

    # Vérifier si déjà traité (skipped dans cache)
    if [ -f "$FILEPATH" ]; then
        echo "⏭️ Déjà existant: $FILEPATH"
        continue
    fi

    echo "📥 Traitement: $url"

    # Déléguer à agent via Task tool
    # L'agent lit l'URL, convertit en markdown, sauvegarde dans FILEPATH
    echo "Utiliser agent @$AGENT_NAME avec URL: $url"

    # Vérifier succès
    if [ -f "$FILEPATH" ]; then
        FILE_SIZE=$(du -k "$FILEPATH" | cut -f1)
        echo "✅ Créé: $FILEPATH (${FILE_SIZE}KB)"
        CREATED=$((CREATED + 1))
    else
        echo "❌ Échec: $url"
        ERRORS=$((ERRORS + 1))
    fi

    # Délai anti-rate-limit
    sleep 2
done

PROCESSED=$((CREATED + ERRORS))
```

### Étape 5: Statistiques Finales

```bash
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
echo "📊 Statistiques finales:"
echo "   - URLs totales: $TOTAL_URLS"
echo "   - Fichiers documentation: $TOTAL_FILES"
echo "   - Taille totale: ${TOTAL_SIZE_MB}MB"
echo "   - Couverture: ${COVERAGE}%"
```

### Étape 6: Rapport Final

```bash
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ $DURATION -lt 60 ]; then
    DURATION_STR="${DURATION}s"
elif [ $DURATION -lt 3600 ]; then
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    DURATION_STR="${MINUTES}m ${SECONDS}s"
else
    HOURS=$((DURATION / 3600))
    MINUTES=$(((DURATION % 3600) / 60))
    SECONDS=$((DURATION % 60))
    DURATION_STR="${HOURS}h ${MINUTES}m ${SECONDS}s"
fi

echo "⏱️ Durée: $DURATION_STR"
```

```yaml
task: "Chargement documentation ${FRAMEWORK}${VERSION:+ ${VERSION}}"
status: "terminé"
details:
  framework: "$FRAMEWORK"
  version: "${VERSION:-latest}"
  total_urls: $TOTAL_URLS
  processed: $PROCESSED
  skipped: $SKIPPED
  deleted: $DELETED
  created: $CREATED
  errors: $ERRORS
statistics:
  documentation_files: $TOTAL_FILES
  total_size: "${TOTAL_SIZE_MB}MB"
  coverage: "${COVERAGE}%"
notes:
  - "Documentation ${FRAMEWORK}${VERSION:+ ${VERSION}} disponible dans ${DOCS_PATH}"
  - "Fichiers individuels pour éviter conflits"
  - "Cache valide ${CACHE_HOURS}h"
```

## Gestion Rate Limiting

**IMPORTANT** : En cas d'erreurs 429/401 :

1. Délai de 2-3s entre requêtes (déjà implémenté)
2. Réduire parallélisme si nécessaire
3. Retry avec backoff exponentiel (5s, 10s, 20s)
4. Noter URLs en échec dans rapport final

## Error Handling

- Framework non supporté → ARRÊT (exit 1)
- README introuvable → ARRÊT (exit 1)
- Aucune URL dans README → ARRÊT (exit 1)
- Échec scraping URL → WARNING + continue (non bloquant)

## Notes

- Délai 2s entre URLs pour éviter rate limiting
- Cache 24h par défaut
- Délègue aux agents scraper spécialisés
- Support multi-version via argument optionnel
- Fichiers markdown avec nommage basé sur URL
