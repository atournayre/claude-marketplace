---
name: dev:summary
description: Résumé de ce qui a été construit (Phase 7)
model: haiku
allowed-tools: [Read, Glob]
version: 1.0.0
license: MIT
---

# Configuration de sortie

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


**IMPORTANT** : Cette skill génère un résumé concis et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

**Output-style requis** : `ultra-concise`

# Objectif

Phase 7 du workflow de développement : documenter ce qui a été accompli et suggérer les prochaines étapes.

# Instructions

## 1. Lire le contexte

- Lire `.claude/data/.dev-workflow-state.json` pour récupérer toutes les informations du workflow
- Lister tous les fichiers créés/modifiés

## 2. Générer le résumé

Présenter un résumé structuré avec :
- Description de la feature
- Composants créés
- Fichiers modifiés
- Décisions clés
- Résultats qualité
- Temps de développement par phase
- Prochaines étapes suggérées

## Format de durée

Formater les durées de manière lisible :
- `< 60s` → `{X}s` (ex: `45s`)
- `< 60min` → `{X}m {Y}s` (ex: `2m 30s`)
- `>= 60min` → `{X}h {Y}m` (ex: `1h 15m`)

## 3. Nettoyer le workflow state

Marquer le workflow comme terminé

## 4. Proposer les actions suivantes

```
📋 Et maintenant ?

- /git:commit - Commiter les changements
- /git:pr - Créer une Pull Request
- /dev:feature <nouvelle-feature> - Démarrer une nouvelle feature

Merci d'avoir utilisé le workflow de développement !
```

# Règles

- Être **concis** mais **complet**
- Mettre en avant les **décisions importantes**
- Toujours suggérer des **prochaines étapes**
- Ne pas oublier de **marquer les todos comme complétés**
