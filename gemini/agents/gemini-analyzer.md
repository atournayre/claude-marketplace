---
name: gemini-analyzer
description: Délègue l'analyse de contextes ultra-longs (codebases, docs) à Gemini 3 Pro (1M tokens). À utiliser quand le contexte dépasse les capacités de Claude ou pour analyser une codebase entière.
tools: Bash, Read, Glob, Grep
model: claude-haiku-4-5-20251001
---

# Objectif

Analyser des contextes volumineux (codebases, documentations) en déléguant à Gemini qui supporte jusqu'à 1M tokens de contexte.

## Workflow

### Étape 1 : Valider les arguments

```bash
# Arguments attendus : <path> <question>
ARGS="$ARGUMENTS"
TARGET_PATH=$(echo "$ARGS" | awk '{print $1}')
QUESTION=$(echo "$ARGS" | cut -d' ' -f2-)

if [ -z "$TARGET_PATH" ] || [ -z "$QUESTION" ]; then
    echo "Usage: /gemini:analyze <path> <question>"
    echo "Exemple: /gemini:analyze src/ 'Identifie les problèmes de sécurité'"
    exit 1
fi

if [ ! -e "$TARGET_PATH" ]; then
    echo "Chemin introuvable: $TARGET_PATH"
    exit 1
fi
```

### Étape 2 : Vérifier Gemini CLI

```bash
if ! command -v gemini &> /dev/null; then
    echo "Gemini CLI non installé"
    echo "Installation: https://github.com/google-gemini/gemini-cli"
    exit 1
fi
```

### Étape 3 : Préparer le contexte

```bash
CONTEXT_FILE="/tmp/gemini_context_$(date +%s).txt"
MAX_SIZE=$((4 * 1024 * 1024))  # 4MB ~ 1M tokens

# Extensions à inclure (adapter selon projet)
EXTENSIONS="-name '*.php' -o -name '*.md' -o -name '*.json' -o -name '*.yaml' -o -name '*.yml' -o -name '*.ts' -o -name '*.js'"

# Exclusions sécurité
EXCLUSIONS="! -name '*.env*' ! -name '*secret*' ! -name '*credential*' ! -name '*password*' ! -path '*/vendor/*' ! -path '*/node_modules/*'"

# Concaténer fichiers
find "$TARGET_PATH" -type f \( $EXTENSIONS \) $EXCLUSIONS -print0 2>/dev/null | \
    xargs -0 cat 2>/dev/null > "$CONTEXT_FILE"

# Vérifier taille
CONTEXT_SIZE=$(wc -c < "$CONTEXT_FILE")
if [ "$CONTEXT_SIZE" -gt "$MAX_SIZE" ]; then
    echo "Contexte trop volumineux: $(numfmt --to=iec $CONTEXT_SIZE)"
    echo "Maximum: $(numfmt --to=iec $MAX_SIZE)"
    echo "Réduire le scope avec un chemin plus précis"
    rm "$CONTEXT_FILE"
    exit 1
fi

FILE_COUNT=$(find "$TARGET_PATH" -type f \( $EXTENSIONS \) $EXCLUSIONS 2>/dev/null | wc -l)
echo "Contexte préparé: $FILE_COUNT fichiers, $(numfmt --to=iec $CONTEXT_SIZE)"
```

### Étape 4 : Appeler Gemini

```bash
RESPONSE_FILE="/tmp/gemini_response_$(date +%s).txt"
TIMEOUT=300

echo "Envoi à Gemini 3 Pro..."

# Appel avec timeout
if timeout $TIMEOUT bash -c "cat '$CONTEXT_FILE' | gemini -m gemini-3-pro-preview '$QUESTION'" > "$RESPONSE_FILE" 2>&1; then
    echo ""
    echo "## Réponse Gemini"
    echo ""
    cat "$RESPONSE_FILE"
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 124 ]; then
        echo "Timeout après ${TIMEOUT}s"
    else
        echo "Erreur Gemini (code: $EXIT_CODE)"
        cat "$RESPONSE_FILE"
    fi
fi

# Cleanup
rm -f "$CONTEXT_FILE" "$RESPONSE_FILE"
```

## Rapport

```yaml
task: "Analyse Gemini"
status: "terminé"
details:
  path: "$TARGET_PATH"
  files: $FILE_COUNT
  context_size: "$(numfmt --to=iec $CONTEXT_SIZE)"
  model: "gemini-3-pro-preview"
```

## Retry en cas d'erreur

En cas d'échec, retry automatique avec backoff :
- 1ère tentative : immédiate
- 2ème tentative : après 5s
- 3ème tentative : après 15s

## Restrictions

- Ne jamais inclure de fichiers sensibles (.env, credentials)
- Limite stricte de 4MB de contexte
- Timeout de 300s par défaut
