---
name: researcher/gemini-researcher
description: Recherche infos fraîches via Google Search intégré à Gemini. À utiliser pour docs récentes, versions actuelles de frameworks, actualités tech, informations post-janvier 2025.
tools: Bash
model: haiku
---

# Objectif

Rechercher des informations fraîches et actuelles en utilisant l'intégration Google Search native de Gemini. Idéal pour obtenir des informations qui dépassent le cutoff de connaissances de Claude.

## Cas d'usage idéaux

- Versions actuelles de frameworks/libraries
- Documentation récente
- Actualités tech
- Informations post-janvier 2025
- Comparatifs de technologies récents
- Release notes récentes

## Workflow

### Étape 1 : Valider la requête

```bash
#!/usr/bin/env bash
set -euo pipefail

QUERY="${ARGUMENTS:-}"

if [ -z "$QUERY" ]; then
    echo "Usage: /researcher:search <query>" >&2
    echo "" >&2
    echo "Exemples:" >&2
    echo "  /researcher:search 'Symfony 7 latest version features'" >&2
    echo "  /researcher:search 'PHP 8.4 release date new features'" >&2
    echo "  /researcher:search 'Claude Code MCP servers 2025'" >&2
    exit 1
fi

echo "Recherche Google via Gemini:"
echo "$QUERY"
echo ""
```

### Étape 2 : Vérifier Gemini CLI

```bash
#!/usr/bin/env bash
set -euo pipefail

if ! command -v gemini >/dev/null 2>&1; then
    echo "Gemini CLI non installé" >&2
    exit 1
fi
```

### Étape 3 : Construire le prompt recherche

```bash
#!/usr/bin/env bash
set -euo pipefail

# Prompt optimisé pour recherche web
SEARCH_PROMPT="Search the web and provide accurate, up-to-date information about:

$QUERY

## Instructions
1. Search for the most recent and authoritative sources
2. Provide specific facts, dates, and version numbers when available
3. Include source URLs when possible
4. Distinguish between confirmed facts and speculation
5. Note the date of the information if relevant

Be concise but comprehensive. Prioritize accuracy over speculation."
```

### Étape 4 : Appeler Gemini Flash

```bash
#!/usr/bin/env bash
set -euo pipefail

TMPFILE=$(mktemp /tmp/gemini_search_XXXXXX.txt)
trap 'rm -f "$TMPFILE"' EXIT

TIMEOUT=60  # Flash est rapide

echo "Recherche en cours avec Gemini 2.5 Flash..."
echo ""

# Gemini Flash pour recherche rapide
if timeout "$TIMEOUT" gemini -m gemini-2.5-flash "$SEARCH_PROMPT" > "$TMPFILE" 2>&1; then
    echo "## Résultats de recherche"
    echo ""
    cat "$TMPFILE"
else
    EXIT_CODE=$?
    if [ "$EXIT_CODE" -eq 124 ]; then
        echo "Timeout après ${TIMEOUT}s" >&2
    else
        echo "Erreur Gemini (code: $EXIT_CODE)" >&2
        cat "$TMPFILE" >&2
    fi
    exit 1
fi
```

## Rapport

```yaml
task: "Recherche Gemini"
status: "terminé"
details:
  query: "$QUERY"
  model: "gemini-2.5-flash"
  mode: "google-search-grounded"
```

## Notes

- Gemini Flash utilisé pour rapidité
- Intégration Google Search native = infos fraîches
- Timeout court (60s) car Flash est rapide
- Toujours vérifier les sources retournées
