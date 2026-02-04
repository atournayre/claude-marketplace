---
title: "gemini"
description: "Délégation Gemini CLI  - contexte ultra-long (1M tokens), Deep Think, Google Search temps réel"
version: "1.4.1"
---

# gemini <Badge type="info" text="v1.4.1" />


Intégration Gemini CLI pour Claude Code. Permet de déléguer des tâches spécialisées à Gemini tout en gardant Claude comme orchestrateur principal.

## Prérequis

- Gemini CLI installé et authentifié (`gemini --version`)
- Accès API Gemini configuré

## Skills Disponibles

Le plugin gemini fournit 3 skills (format natif Claude Code) :

| Commande | Description | Arguments |
|----------|-------------|-----------|
| `/gemini:analyze` | Analyse de contextes ultra-longs (codebases, docs) | `<path> <question>` |
| `/gemini:think` | Problèmes complexes nécessitant réflexion approfondie | `<problem-description>` |
| `/gemini:search` | Recherche temps réel via Google Search intégré | `<query>` |

## Agents

| Agent | Modèle Claude | Modèle Gemini | Cas d'usage |
|-------|---------------|---------------|-------------|
| `gemini-analyzer` | `haiku` | `gemini-3-pro-preview` | Analyse codebase/docs (1M tokens) |
| `gemini-thinker` | `haiku` | `gemini-3-pro-preview` | Deep Think (math, logique, architecture) |
| `gemini-researcher` | `haiku` | `gemini-2.5-flash` | Recherche web temps réel |

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

- `gemini-3-pro-preview` : Contexte long, Deep Think
- `gemini-2.5-flash` : Recherche rapide

Voir MODELS.md pour la liste complète des modèles disponibles.
