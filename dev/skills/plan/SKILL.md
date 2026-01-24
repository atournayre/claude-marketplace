---
name: dev:plan
description: Générer plan d'implémentation dans docs/specs/ (Phase 4)
model: claude-sonnet-4-5-20250929
allowed-tools: [Write, Read, Glob]
version: 1.0.0
license: MIT
---

# Objectif

Phase 4 du workflow de développement : générer un plan d'implémentation détaillé basé sur l'architecture choisie.

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour récupérer :
  - La feature description
  - Les décisions de clarification
  - L'architecture choisie
- Si phases précédentes non complétées, rediriger vers la phase manquante

## 2. Générer le plan

Créer le fichier `docs/specs/feature-{nom-kebab-case}.md` avec la structure complète du plan

## 3. Créer le répertoire si nécessaire

```bash
mkdir -p docs/specs
```

## 4. Afficher le résumé

## 5. Mettre à jour le workflow state

# Prochaine étape

```
✅ Plan généré : docs/specs/feature-{nom}.md

Prochaine étape : /dev:code docs/specs/feature-{nom}.md

⚠️ L'implémentation nécessite ton approbation explicite.
```

# Règles

- Le plan doit être **actionnable** (pas de descriptions vagues)
- Chaque étape doit avoir des **fichiers** et des **tâches** clairs
- Les tests doivent être **spécifiés** avant l'implémentation
- Respecter les **conventions du projet** (CLAUDE.md)
