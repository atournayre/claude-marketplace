---
name: architect/deep-think
description: Délègue les problèmes complexes (math, logique, architecture) à Gemini Deep Think. À utiliser pour réflexion approfondie nécessitant exploration multi-hypothèses.
tools: Bash
model: haiku
---

# Objectif

Résoudre des problèmes complexes en déléguant à Gemini qui utilise un mode de réflexion approfondie (thinking step by step, exploration multi-hypothèses).

## Cas d'usage idéaux

- Problèmes mathématiques complexes
- Puzzles logiques
- Décisions architecturales avec trade-offs
- Algorithmes d'optimisation
- Raisonnement sur des systèmes distribués

## Workflow

### Étape 1 : Valider le problème

```bash
PROBLEM="$ARGUMENTS"

if [ -z "$PROBLEM" ]; then
    echo "Usage: /architect:deep-think <problem-description>"
    echo ""
    echo "Exemples:"
    echo "  /architect:deep-think 'Comment implémenter un système de saga pour transactions distribuées?'"
    echo "  /architect:deep-think 'Quel algorithme de cache optimal pour des lectures fréquentes et écritures rares?'"
    exit 1
fi

echo "Problème soumis à Gemini Deep Think:"
echo "$PROBLEM"
echo ""
```

### Étape 2 : Vérifier Gemini CLI

```bash
command -v gemini >/dev/null 2>&1 || { echo "Gemini CLI non installé" >&2; exit 1; }
```

### Étape 3 : Construire le prompt Deep Think

```bash
# Prompt structuré pour maximiser la réflexion
DEEP_THINK_PROMPT="You are an expert problem solver. Analyze this problem thoroughly.

## Problem
$PROBLEM

## Instructions
1. First, understand the problem completely
2. Identify key constraints and requirements
3. Consider multiple approaches
4. Evaluate trade-offs for each approach
5. Recommend the best solution with justification
6. Provide implementation guidance if applicable

Think step by step. Show your reasoning process."
```

### Étape 4 : Appeler Gemini avec retry

```bash
TMPDIR=$(mktemp -d)
RESPONSE_FILE="$TMPDIR/gemini_think.txt"
trap 'rm -rf "$TMPDIR"' EXIT
TIMEOUT=300

echo "Réflexion en cours avec Gemini Pro..."
echo ""

for attempt in 1 2 3; do
    if timeout $TIMEOUT gemini -m gemini-3-pro-preview "$DEEP_THINK_PROMPT" > "$RESPONSE_FILE" 2>&1; then
        echo "## Analyse Gemini Deep Think"
        echo ""
        cat "$RESPONSE_FILE"
        break
    else
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 124 ]; then
            echo "Timeout après ${TIMEOUT}s - problème peut-être trop complexe"
            break
        else
            echo "Erreur Gemini tentative $attempt (code: $EXIT_CODE)"
            if [ $attempt -lt 3 ]; then
                WAIT=$((attempt * 5))
                echo "Retry dans ${WAIT}s..."
                sleep $WAIT
            else
                cat "$RESPONSE_FILE"
            fi
        fi
    fi
done
```

## Rapport / Réponse

```yaml
task: "Deep Think Gemini"
status: "terminé"
details:
  problem: "$PROBLEM"
  model: "gemini-3-pro-preview"
  mode: "step-by-step reasoning"
```

## Notes

- Gemini Pro excelle en raisonnement multi-étapes
- Le prompt est structuré pour forcer l'exploration d'alternatives
- Timeout généreux (300s) pour problèmes complexes
- Retry automatique avec backoff exponentiel (5s, 15s)
