# PHPStan Error Resolver Skill

Résout automatiquement les erreurs PHPStan en boucle jusqu'à zéro erreur ou stagnation.

## Fonctionnalités

- Détection automatique des erreurs PHPStan
- Groupement des erreurs par fichier
- Résolution par batch (5 erreurs max par fichier par itération)
- Boucle de résolution avec vérification après chaque correction
- Détection de stagnation (erreurs qui ne diminuent plus)
- Rapport détaillé avec taux de succès

## Usage

Via la commande délégante :
```bash
/qa:phpstan
```

Ou directement via le skill :
```bash
# Utiliser l'outil Task avec le skill phpstan-resolver
```

## Workflow

1. Analyse PHPStan initiale
2. Groupement erreurs par fichier
3. Pour chaque fichier avec erreurs :
   - Batch de 5 erreurs max
   - Délégation à agent `@phpstan-error-resolver`
   - Correction via Edit tool
4. Re-exécution PHPStan pour vérification
5. Répétition jusqu'à :
   - Zéro erreur (succès total)
   - Stagnation (erreurs ne diminuent plus)
   - Max itérations (10)

## Configuration

- `ERROR_BATCH_SIZE`: 5 erreurs par fichier par itération
- `MAX_ITERATIONS`: 10 itérations maximum
- `PHPSTAN_CONFIG`: phpstan.neon ou phpstan.neon.dist

## Dépendances

- PHPStan installé (`./vendor/bin/phpstan`)
- Configuration PHPStan valide
- Agent `@phpstan-error-resolver` disponible
- `jq` pour parsing JSON

## Rapport généré

```yaml
details:
  total_errors_initial: [nombre]
  total_errors_final: [nombre]
  errors_fixed: [nombre]
  success_rate: "[%]"
  iterations: [nombre]
```

## Notes

- Utilise format JSON de PHPStan pour parsing précis
- Évite boucles infinies avec max itérations
- Détecte stagnation automatiquement
- Rapport détaillé même en cas d'échec partiel
