---
title: "researcher"
description: "Recherche et analyse via Gemini (Google Search) et agents web spécialisés"
version: "1.1.0"
---

# researcher <Badge type="info" text="v1.1.0" />

Recherche et analyse via Gemini (Google Search) et agents web spécialisés.

## Installation

```bash
/plugin install researcher@atournayre
```

## Skills Disponibles

Le plugin researcher fournit 2 skills :

### `/researcher:search`

Recherche temps réel via Google Search intégré à Gemini. Idéal pour les docs récentes, versions actuelles de frameworks, actualités tech.

### `/researcher:analyze`

Analyse une codebase ou documentation avec Gemini (1M tokens). À utiliser quand le contexte dépasse les capacités de Claude ou pour analyser une codebase entière.

## Agents

- **gemini-researcher** : Recherche infos fraîches via Google Search intégré à Gemini
- **explore-docs** : Recherche dans la documentation de bibliothèques via Context7 MCP
- **websearch** : Recherche web rapide

## Changelog

- Voir CHANGELOG.md
