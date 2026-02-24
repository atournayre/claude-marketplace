---
title: "documenter"
description: "Documentation : RTFM, génération docs, chargement frameworks, scraping agents"
version: "1.1.0"
---

# documenter <Badge type="info" text="v1.1.0" />

Documentation : RTFM, génération docs, chargement frameworks, scraping agents.

## Installation

```bash
/plugin install documenter@atournayre
```

## Skills Disponibles

Le plugin documenter fournit 6 skills :

### `/documenter:rtfm`

Lit la documentation technique (Read The Fucking Manual) depuis une URL ou un fichier local.

### `/documenter:load`

Charge la documentation d'un framework depuis son site web dans des fichiers markdown locaux.

### `/documenter:update`

Crée la documentation pour la fonctionnalité en cours, met à jour le README global, et lie les documents entre eux.

### `/documenter:summary`

Résumé de ce qui a été construit — Phase 7 du workflow de développement.

### `/documenter:claude-load`

Charge la documentation Claude Code depuis docs.claude.com dans des fichiers markdown locaux.

### `/documenter:claude-question`

Interroge la documentation Claude Code locale pour répondre à une question.

## Agents

- **api-platform-docs-scraper** : Extrait et sauvegarde la documentation API Platform dans `docs/api-platform/`
- **atournayre-framework-docs-scraper** : Extrait et sauvegarde la documentation atournayre-framework depuis readthedocs.io
- **claude-docs-scraper** : Extrait et sauvegarde la documentation Claude Code dans `docs/claude/`
- **meilisearch-docs-scraper** : Extrait et sauvegarde la documentation Meilisearch dans `docs/meilisearch/`
- **symfony-docs-scraper** : Extrait et sauvegarde la documentation Symfony dans `docs/symfony/`

## Changelog

- Voir CHANGELOG.md
