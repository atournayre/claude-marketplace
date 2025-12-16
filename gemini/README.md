# Plugin Gemini

Intégration Gemini CLI pour Claude Code. Permet de déléguer des tâches spécialisées à Gemini tout en gardant Claude comme orchestrateur principal.

## Prérequis

- Gemini CLI installé et authentifié (`gemini --version`)
- Accès API Gemini configuré

## Cas d'usage

| Commande | Agent | Description |
|----------|-------|-------------|
| `/gemini:analyze` | gemini-analyzer | Analyse de contextes ultra-longs (codebases, docs) - jusqu'à 1M tokens |
| `/gemini:think` | gemini-thinker | Problèmes complexes nécessitant réflexion approfondie (math, logique, architecture) |
| `/gemini:search` | gemini-researcher | Recherche temps réel via Google Search intégré |

## Utilisation

### Analyse de codebase

```bash
/gemini:analyze src/ "Identifie les problèmes de performance potentiels"
```

### Deep Think

```bash
/gemini:think "Comment implémenter un système de saga pour transactions distribuées?"
```

### Recherche temps réel

```bash
/gemini:search "Symfony 7 release date features"
```

## Sécurité

- Fichiers sensibles (.env, credentials) automatiquement exclus
- Limite contexte : 4MB max
- Timeout : 300s par défaut

## Modèles utilisés

- `gemini-2.5-pro` : Contexte long, Deep Think
- `gemini-2.5-flash` : Recherche rapide
