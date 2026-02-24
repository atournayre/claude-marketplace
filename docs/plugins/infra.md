---
title: "infra"
description: "Infrastructure Claude Code : gestion mémoire, création de skills et agents, alias, versioning des plugins"
version: "1.1.0"
---

# infra <Badge type="info" text="v1.1.0" />

Infrastructure Claude Code : gestion mémoire (CLAUDE.md/.claude/rules), création de skills et agents, alias, versioning des plugins, initialisation marketplace.

## Installation

```bash
/plugin install infra@atournayre
```

## Skills Disponibles

Le plugin infra fournit 7 skills :

### `/infra:memory`

Crée et optimise les fichiers de mémoire Claude Code (CLAUDE.md ou .claude/rules/).

### `/infra:skill-creator`

Guide expert pour créer des skills Claude Code efficaces.

### `/infra:make-subagent`

Guide expert pour créer et configurer des sous-agents Claude Code spécialisés.

### `/infra:alias-add`

Crée un alias de slash command qui délègue à une autre slash command existante.

### `/infra:bump`

Automatise les mises à jour de version des plugins avec détection automatique du type (PATCH ou MINOR).

### `/infra:init`

Initialise le marketplace et vérifie toutes les dépendances nécessaires aux plugins.

### `/infra:fix-grammar`

Corrige les fautes de grammaire et d'orthographe dans un ou plusieurs fichiers.

## Agents

- **action** : Exécuteur conditionnel d'actions — vérifie indépendamment chaque item avant d'agir
- **meta-agent** : Génère un nouveau fichier de configuration d'agent Claude Code complet

## Changelog

- Voir CHANGELOG.md
