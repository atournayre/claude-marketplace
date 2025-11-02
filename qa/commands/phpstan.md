---
model: claude-opus-4-1-20250805
description: Résoudre les erreurs PHPStan en utilisant l'agent phpstan-error-resolver
allowed-tools: Task, Bash (./vendor/bin/phpstan:*), Read
---

# Résoudre les erreurs PHPStan

Résout les erreurs PHPStan détectées dans le projet en utilisant l'agent spécialisé phpstan-error-resolver.

## Timing

### Début d'Exécution
**OBLIGATOIRE - PREMIÈRE ACTION** :
1. Exécuter `date` pour obtenir l'heure réelle
2. Afficher immédiatement : 🕐 **Démarrage** : [Résultat de la commande date]
3. Stocker le timestamp pour le calcul de durée

### Fin d'Exécution
**OBLIGATOIRE - DERNIÈRE ACTION** :
1. Exécuter `date` à nouveau pour obtenir l'heure de fin
2. Calculer la durée réelle entre début et fin
3. Afficher :
   - ✅ **Terminé** : [Résultat de la commande date]
   - ⏱️ **Durée** : [Durée calculée au format lisible]

### Formats
- Date : résultat brut de la commande `date` (incluant CEST/CET automatiquement)
- Durée :
  - Moins d'1 minute : `XXs` (ex: 45s)
  - Moins d'1 heure : `XXm XXs` (ex: 2m 30s)
  - Plus d'1 heure : `XXh XXm XXs` (ex: 1h 15m 30s)

### Instructions CRITIQUES
- TOUJOURS exécuter `date` via Bash - JAMAIS inventer/halluciner l'heure
- Le timestamp de début DOIT être obtenu en exécutant `date` immédiatement
- Le timestamp de fin DOIT être obtenu en exécutant `date` à la fin
- Calculer la durée en soustrayant les timestamps unix (utiliser `date +%s`)
- NE JAMAIS supposer ou deviner l'heure

## Variables

PHPSTAN_CONFIG: phpstan.neon (ou phpstan.neon.dist)
PHPSTAN_BIN: ./vendor/bin/phpstan
ERROR_BATCH_SIZE: 5

## Flux de Travail

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

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

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
```
