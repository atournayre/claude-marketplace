---
title: "analyst"
description: "Analyse de besoin, exploration de codebase et clarification avant développement"
version: "1.1.0"
---

# analyst <Badge type="info" text="v1.1.0" />

Analyse de besoin, exploration de codebase et clarification avant développement.

## Installation

```bash
/plugin install analyst@atournayre
```

## Skills Disponibles

Le plugin analyst fournit 4 skills :

### `/analyst:discover`

Comprendre le besoin avant développement — Phase 0 du workflow.

### `/analyst:explore`

Explorer le codebase avec agents parallèles — Phase 1 du workflow.

### `/analyst:clarify`

Lever les ambiguïtés avant design — Phase 2 (mode interactif ou heuristiques automatiques).

### `/analyst:impact`

Génère automatiquement deux rapports d'impact (métier et technique) pour une PR GitHub.

## Agents

- **analyst** : Analyse architecture + design DDD, propose l'architecture technique et le modèle de domaine
- **designer** : Conçoit le design DDD, les contrats, interfaces et flux de données
- **explore-codebase** : Exploration spécialisée du codebase pour identifier les patterns et fichiers pertinents
- **gemini-analyzer** : Délègue l'analyse de contextes ultra-longs (codebases, docs) à Gemini Pro (1M tokens)

## Changelog

- Voir CHANGELOG.md
