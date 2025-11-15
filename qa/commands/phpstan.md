---
model: claude-opus-4-1-20250805
description: Résoudre les erreurs PHPStan en utilisant l'agent phpstan-error-resolver
allowed-tools: Task, Bash (./vendor/bin/phpstan:*), Read
---

# Résoudre les erreurs PHPStan

Résout les erreurs PHPStan détectées dans le projet en utilisant l'agent spécialisé phpstan-error-resolver.

## Variables

**Lire configuration :**
- Lire `.claude/plugins.settings.json` et `~/.claude/plugins.settings.json`
- Extraire `atournayre-claude-plugin-marketplace.qa.phpstan.*`
- Fusionner configs (projet écrase global)
- Valeurs par défaut si absentes :
  - `level`: 9
  - `auto_fix`: true
  - `config_file`: "phpstan.neon"

PHPSTAN_CONFIG: Valeur de config `config_file` OU phpstan.neon (ou phpstan.neon.dist)
PHPSTAN_BIN: ./vendor/bin/phpstan
PHPSTAN_LEVEL: Valeur de config `level` OU 9
AUTO_FIX: Valeur de config `auto_fix` OU true
ERROR_BATCH_SIZE: 5

## Flux de Travail

1. Exécuter PHPStan pour récupérer la liste des erreurs

2. Si aucune erreur, terminer avec succès

3. Si des erreurs existent :
   - Grouper les erreurs par fichier
   - Compter le nombre total d'erreurs

4. Pour chaque groupe d'erreurs (max ERROR_BATCH_SIZE erreurs par fichier), utiliser l'outil Task en parallèle et suivre le `error_resolution_prompt` comme prompt exact pour chaque Task

<error_resolution_prompt>

Utiliser l'agent @phpstan-error-resolver en lui passant les informations suivantes :

Fichier: [chemin du fichier]
Erreurs:
[liste des erreurs avec ligne et message]

</error_resolution_prompt>

5. Après chaque résolution, ré-exécuter PHPStan pour vérifier que les erreurs sont corrigées

6. Répéter jusqu'à ce qu'il n'y ait plus d'erreurs ou que le nombre d'erreurs ne diminue plus

7. Une fois toutes les tâches terminées, répondre selon le Format de Rapport

## Format de Rapport

```yaml
task: "Résolution des erreurs PHPStan"
status: "terminé"
details:
  total_errors_initial: "[nombre d'erreurs au départ]"
  total_errors_final: "[nombre d'erreurs restantes]"
  files_processed: "[nombre de fichiers traités]"
  errors_fixed: "[nombre d'erreurs corrigées]"
  errors_remaining: "[nombre d'erreurs non résolues]"
  iterations: "[nombre d'itérations effectuées]"
files:
  fixed:
    - file: "[chemin du fichier]"
      errors_fixed: "[nombre d'erreurs corrigées]"
      errors_remaining: "[nombre d'erreurs restantes]"
  failed:
    - file: "[chemin du fichier]"
      errors: "[liste des erreurs non résolues]"
      reason: "[raison de l'échec]"
statistics:
  success_rate: "[pourcentage d'erreurs corrigées]"
  execution_time: "[temps d'exécution total]"
  phpstan_level: "[niveau PHPStan utilisé]"
notes:
  - "Toutes les erreurs PHPStan ont été analysées"
  - "Les corrections ont été appliquées automatiquement"
  - "[autres notes importantes]"
```
