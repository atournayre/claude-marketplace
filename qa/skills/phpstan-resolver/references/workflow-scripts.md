# Scripts de workflow PHPStan Resolver

## Vérification environnement

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

## Exécution initiale PHPStan

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

## Groupement erreurs par fichier

```bash
# Parser JSON et grouper par fichier
jq -r '.files | to_entries[] | "\(.key)|\(.value.messages | length)"' /tmp/phpstan_initial.json > /tmp/phpstan_files.txt

# Afficher groupement
echo "📁 Erreurs par fichier:"
cat /tmp/phpstan_files.txt | while IFS='|' read file count; do
    echo "  - $file: $count erreurs"
done
```

## Boucle de résolution

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

            # Vérification anti-suppression après chaque correction
            SUPPRESSIONS=$(git diff -- "$file" | grep -cE '^\+.*@phpstan-ignore' || echo 0)
            if [ "$SUPPRESSIONS" -gt 0 ]; then
                echo "  REJET : $SUPPRESSIONS suppression(s) dans $file"
                git checkout -- "$file"
            fi
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

## Analyse résultat final

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

## Task Management (TaskCreate/TaskUpdate)

Les tâches doivent être créées à l'initialisation du workflow avec `TaskCreate` :

```
TaskCreate #1: Vérifier environnement PHPStan
TaskCreate #2: Exécuter analyse initiale (--error-format=json)
TaskCreate #3: Grouper erreurs par fichier
TaskCreate #4: Boucle de résolution (max 10 itérations)
TaskCreate #5: Générer rapport final
```

**Pattern d'exécution :**
- `TaskUpdate` → tâche en `in_progress` → exécution → `TaskUpdate` → tâche en `completed`
- La tâche #4 (boucle) reste `in_progress` pendant toutes les itérations
