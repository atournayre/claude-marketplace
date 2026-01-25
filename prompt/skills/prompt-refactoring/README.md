# Skill : prompt:refactoring

Génère un prompt pour refactoring et optimisation de code existant.

## Usage

```bash
/prompt:refactoring <TargetFile> [--optimization-type=<type>]
```

## Arguments

| Argument | Type | Requis | Description | Exemple |
|----------|------|--------|-------------|---------|
| `TargetFile` | string | Oui | Fichier à refactorer | `src/Service/MenuBuilder.php` |
| `--optimization-type` | flag | Oui* | Type d'optimisation | `--optimization-type=cache-decorator` |
| `--current-complexity` | flag | Non | Complexité actuelle | `--current-complexity=15` |
| `--improvement-target` | flag | Non | Objectif complexité | `--improvement-target=8` |

*Si omis, Claude demandera

## Types d'Optimisation Courants

- `cache-decorator` - Ajouter cache via Decorator
- `reduce-complexity` - Réduire complexité cyclomatique
- `extract-service` - Extraire service depuis classe
- `strategy-pattern` - Remplacer if/else par Strategy
- `performance` - Optimisation performance générale

## Exemples

```bash
# Ajouter cache decorator
/prompt:refactoring MenuBuilder --optimization-type=cache-decorator

# Réduire complexité
/prompt:refactoring src/Calculator.php --optimization-type=reduce-complexity --current-complexity=20 --improvement-target=10
```

## Variables Substituées

- `{TARGET_FILE}` - Fichier cible
- `{OPTIMIZATION_TYPE}` - Type optimisation
- `{CURRENT_COMPLEXITY}` - Complexité actuelle
- `{IMPROVEMENT_TARGET}` - Objectif

## Prompt Généré

Inclut :
- Analyse problème (métriques, symptoms)
- Pattern technique proposé
- Phases : Préparation, Refactoring, Validation, Déploiement
- Benchmarks avant/après
- Tests de non-régression

## Fichier Généré

`.claude/prompts/refactoring-{nom}-{timestamp}.md`
