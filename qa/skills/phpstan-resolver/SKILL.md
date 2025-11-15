---
name: phpstan-resolver
description: >
  Résout automatiquement les erreurs PHPStan détectées dans le projet en analysant
  et corrigeant les problèmes de types stricts, annotations generics, array shapes
  et collections Doctrine. Boucle jusqu'à zéro erreur ou stagnation.
allowed-tools: [Task, Bash, Read, Edit, Grep, Glob, TodoWrite]
model: claude-opus-4-1-20250805
---

# PHPStan Error Resolver Skill

## Variables

```bash
PHPSTAN_CONFIG="phpstan.neon"  # ou phpstan.neon.dist
PHPSTAN_BIN="./vendor/bin/phpstan"
ERROR_BATCH_SIZE=5
MAX_ITERATIONS=10
```

## Workflow

### Étape 0: Timing
```bash
START_TIME=$(date +%s)
date
```

### Étape 1: Vérification Environnement

```bash
# Vérifier PHPStan installé
if [ ! -f "$PHPSTAN_BIN" ]; then
    echo "❌ PHPStan non trouvé: $PHPSTAN_BIN"
    exit 1
fi

# Vérifier config PHPStan
if [ ! -f "$PHPSTAN_CONFIG" ] && [ ! -f "phpstan.neon.dist" ]; then
    echo "❌ Configuration PHPStan introuvable"
    exit 1
fi

# Utiliser phpstan.neon.dist si phpstan.neon absent
if [ ! -f "$PHPSTAN_CONFIG" ]; then
    PHPSTAN_CONFIG="phpstan.neon.dist"
fi

echo "✅ Environnement PHPStan valide"
echo "   Config: $PHPSTAN_CONFIG"
```

### Étape 2: Exécution Initiale PHPStan

```bash
echo "🔍 Analyse PHPStan initiale..."

# Exécuter PHPStan
$PHPSTAN_BIN analyze --no-progress --error-format=json > /tmp/phpstan_initial.json

# Parser résultat
TOTAL_ERRORS_INITIAL=$(jq '.totals.file_errors' /tmp/phpstan_initial.json)

if [ "$TOTAL_ERRORS_INITIAL" -eq 0 ]; then
    echo "✅ Aucune erreur PHPStan détectée"
    exit 0
fi

echo "📊 Erreurs détectées: $TOTAL_ERRORS_INITIAL"
```

### Étape 3: TodoWrite Initialisation

```yaml
todos:
  - content: "Analyser erreurs PHPStan"
    status: "completed"
    activeForm: "Analyse des erreurs PHPStan"
  - content: "Grouper erreurs par fichier"
    status: "pending"
    activeForm: "Groupement des erreurs par fichier"
  - content: "Résoudre erreurs (itération 1)"
    status: "pending"
    activeForm: "Résolution des erreurs (itération 1)"
  - content: "Vérifier résolution"
    status: "pending"
    activeForm: "Vérification de la résolution"
```

### Étape 4: Groupement Erreurs par Fichier

Marquer todo #2 `in_progress`.

```bash
# Parser JSON et grouper par fichier
jq -r '.files | to_entries[] | "\(.key)|\(.value.messages | length)"' /tmp/phpstan_initial.json > /tmp/phpstan_files.txt

# Afficher groupement
echo "📁 Erreurs par fichier:"
cat /tmp/phpstan_files.txt | while IFS='|' read file count; do
    echo "  - $file: $count erreurs"
done
```

Marquer todo #2 `completed`.

### Étape 5: Boucle de Résolution

Marquer todo #3 `in_progress`.

```bash
ITERATION=1
ERRORS_CURRENT=$TOTAL_ERRORS_INITIAL
ERRORS_PREVIOUS=0

while [ $ITERATION -le $MAX_ITERATIONS ] && [ $ERRORS_CURRENT -gt 0 ] && [ $ERRORS_CURRENT -ne $ERRORS_PREVIOUS ]; do
    echo ""
    echo "🔄 Itération $ITERATION/$MAX_ITERATIONS"
    echo "   Erreurs: $ERRORS_CURRENT"

    # Traiter chaque fichier avec erreurs
    cat /tmp/phpstan_files.txt | while IFS='|' read file error_count; do
        if [ "$error_count" -gt 0 ]; then
            echo "  📝 Traitement: $file ($error_count erreurs)"

            # Extraire erreurs pour ce fichier
            jq -r --arg file "$file" '.files[$file].messages[] | "\(.line)|\(.message)"' /tmp/phpstan_initial.json > /tmp/phpstan_file_errors.txt

            # Limiter batch size
            head -n $ERROR_BATCH_SIZE /tmp/phpstan_file_errors.txt > /tmp/phpstan_batch.txt

            # Déléguer à agent phpstan-error-resolver
            echo "Utiliser agent @phpstan-error-resolver avec:"
            echo "Fichier: $file"
            echo "Erreurs:"
            cat /tmp/phpstan_batch.txt

            # L'agent lit le fichier, analyse erreurs, applique corrections via Edit
        fi
    done

    # Re-exécuter PHPStan
    echo "  🔍 Vérification post-correction..."
    $PHPSTAN_BIN analyze --no-progress --error-format=json > /tmp/phpstan_iteration_${ITERATION}.json

    ERRORS_PREVIOUS=$ERRORS_CURRENT
    ERRORS_CURRENT=$(jq '.totals.file_errors' /tmp/phpstan_iteration_${ITERATION}.json)

    echo "  📊 Résultat: $ERRORS_CURRENT erreurs restantes"

    # Mettre à jour fichiers avec erreurs
    jq -r '.files | to_entries[] | "\(.key)|\(.value.messages | length)"' /tmp/phpstan_iteration_${ITERATION}.json > /tmp/phpstan_files.txt

    ITERATION=$((ITERATION + 1))
done
```

Marquer todo #3 `completed`.

### Étape 6: Analyse Résultat Final

Marquer todo #4 `in_progress`.

```bash
ERRORS_FIXED=$((TOTAL_ERRORS_INITIAL - ERRORS_CURRENT))
SUCCESS_RATE=$(awk "BEGIN {printf \"%.1f\", ($ERRORS_FIXED / $TOTAL_ERRORS_INITIAL) * 100}")

echo ""
echo "📊 Résumé Final:"
echo "   - Erreurs initiales: $TOTAL_ERRORS_INITIAL"
echo "   - Erreurs restantes: $ERRORS_CURRENT"
echo "   - Erreurs corrigées: $ERRORS_FIXED"
echo "   - Taux de succès: ${SUCCESS_RATE}%"
echo "   - Itérations: $((ITERATION - 1))/$MAX_ITERATIONS"

# Identifier fichiers non résolus
if [ $ERRORS_CURRENT -gt 0 ]; then
    echo ""
    echo "⚠️ Fichiers avec erreurs restantes:"
    cat /tmp/phpstan_files.txt | while IFS='|' read file count; do
        if [ "$count" -gt 0 ]; then
            echo "  - $file: $count erreurs"
        fi
    done
fi
```

Marquer todo #4 `completed`.

### Étape 7: Rapport Final

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
task: "Résolution des erreurs PHPStan"
status: "terminé"
details:
  total_errors_initial: $TOTAL_ERRORS_INITIAL
  total_errors_final: $ERRORS_CURRENT
  errors_fixed: $ERRORS_FIXED
  success_rate: "${SUCCESS_RATE}%"
  iterations: $((ITERATION - 1))
files:
  fixed:
    - [Liste des fichiers corrigés]
  failed:
    - [Liste des fichiers non résolus]
statistics:
  success_rate: "${SUCCESS_RATE}%"
  execution_time: "$DURATION_STR"
  phpstan_level: "[Niveau détecté depuis config]"
notes:
  - "Toutes les erreurs PHPStan ont été analysées"
  - "Les corrections ont été appliquées automatiquement"
  - "Relancer si erreurs restantes avec contexte différent"
```

## Error Handling

- PHPStan non trouvé → ARRÊT (exit 1)
- Config PHPStan absente → ARRÊT (exit 1)
- Stagnation (erreurs ne diminuent plus) → ARRÊT avec rapport
- Max itérations atteint → ARRÊT avec rapport

## Notes

- Utilise l'agent `@phpstan-error-resolver` pour corrections
- Batch size de 5 erreurs par fichier par itération
- Maximum 10 itérations pour éviter boucles infinies
- Parser JSON via `jq`
- Marquer CHAQUE todo completed immédiatement après succès
