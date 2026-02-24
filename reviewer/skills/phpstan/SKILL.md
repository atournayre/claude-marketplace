---
name: reviewer:phpstan
description: Résoudre automatiquement les erreurs PHPStan niveau 9 — boucle jusqu'à zéro erreur
model: opus
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, Bash, Read, Edit, Grep, Glob]
version: 1.0.0
license: MIT
---

# PHPStan Error Resolver

Résoudre automatiquement les erreurs PHPStan en analysant et corrigeant les problèmes de types. Boucle jusqu'à zéro erreur ou stagnation.

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

## Configuration

```bash
PHPSTAN_BIN="./vendor/bin/phpstan"
PHPSTAN_CONFIG="phpstan.neon"  # ou phpstan.neon.dist
ERROR_BATCH_SIZE=5
MAX_ITERATIONS=10
```

## Initialisation

Créer les tâches du workflow :

```
TaskCreate #1: Vérifier environnement PHPStan
TaskCreate #2: Exécuter analyse initiale (--error-format=json)
TaskCreate #3: Grouper erreurs par fichier
TaskCreate #4: Boucle de résolution (max 10 itérations)
TaskCreate #5: Générer rapport final
```

- Utiliser `activeForm` (ex: "Vérifiant environnement PHPStan", "Résolvant erreurs")
- La tâche #4 peut prendre du temps (boucle jusqu'à 10 itérations)
- Chaque tâche doit être marquée `in_progress` puis `completed`

## Étapes

### 1. Vérifier l'environnement PHPStan

- PHPStan non trouvé → ARRÊT
- Config absente → ARRÊT

### 2. Exécuter l'analyse initiale

```bash
vendor/bin/phpstan analyse --error-format=json --level=9
```

### 3. Grouper les erreurs par fichier

Classifier par priorité :
- **Critique** : Erreurs de type mismatch, undefined variables, méthodes inexistantes
- **Haute** : Array shapes incorrects, generics manquants, nullable non gérés
- **Moyenne** : Collections Doctrine mal typées, return types incomplets
- **Basse** : Dead code, unreachable statements, unused parameters

### 4. Boucle de résolution (max 10 itérations)

Pour chaque lot de 5 erreurs :

1. Analyser le contexte de chaque erreur (lire le fichier source complet)
2. Appliquer les corrections appropriées :
   - **Type mismatch** : Ajouter assertions de type ou type narrowing
   - **Array shapes** : Documenter avec `@param array{key: type}` ou `@return array<string, mixed>`
   - **Generics** : Ajouter `@template` et `@extends` pour collections et repositories
   - **Nullable** : Utiliser union types `?Type` ou `Type|null`
   - **Undefined** : Initialiser variables ou ajouter checks existence
   - **Exceptions** : Documenter avec `@throws` toutes les exceptions levées
3. Vérification anti-suppression après chaque correction :
   - `grep -rn '@phpstan-ignore' dans les fichiers modifiés`
   - Si détectée : revert le fichier (`git checkout -- <fichier>`), passer à l'erreur suivante
4. Re-exécuter PHPStan
5. Répéter jusqu'à 0 erreur ou stagnation

**Stagnation = ARRÊT avec rapport**

### 5. Rapport final

```yaml
details:
  total_errors_initial: X
  total_errors_final: Y
  errors_fixed: Z
  success_rate: "X%"
  iterations: N
```

## Règles

- **INTERDIT** d'ajouter `@phpstan-ignore`, `@phpstan-ignore-line`, `@phpstan-ignore-next-line`
- Si la seule solution est une suppression : marquer l'erreur comme "non résolue" et passer à la suivante
- Ne JAMAIS créer de commits Git
