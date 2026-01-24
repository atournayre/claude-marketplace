---
name: dev:status
description: Affiche le workflow et l'étape courante
model: claude-haiku-4-5-20251001
allowed-tools: [Read, Glob]
version: 1.0.0
license: MIT
---

# Configuration de sortie

**IMPORTANT** : Cette skill affiche un statut court et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

**Output-style requis** : `ultra-concise`

# Objectif

Afficher l'état actuel du workflow de développement pour que l'utilisateur sache où il en est.

# Instructions

1. Chercher un fichier `.claude/data/.dev-workflow-state.json` dans le répertoire courant
2. Si le fichier existe, lire l'état du workflow
3. Afficher le plan avec les statuts de chaque phase

# Format de sortie

```
🔄 Workflow de développement

  {status} 0. Discover   - Comprendre le besoin     {duration}
  {status} 1. Explore    - Explorer codebase        {duration}
  {status} 2. Clarify    - Questions clarification  {duration}
  {status} 3. Design     - Proposer architectures   {duration}
  {status} 4. Plan       - Générer specs            {duration}
  {status} 5. Code       - Implémenter              {duration}
  {status} 6. Review     - QA complète              {duration}
  {status} 7. Summary    - Résumé final             {duration}

📋 Feature: "{feature_description}"
📁 Plan: {plan_path}
⏱️ Temps total: {total_duration}
```

# Affichage des durées

Pour chaque phase :
- Si `completed` avec `durationMs` → afficher `({formatted_duration})`
- Si `in_progress` avec `startedAt` → afficher `(en cours depuis {elapsed})`
- Si pas de timing → ne rien afficher

## Format de durée

Formater les durées de manière lisible :
- `< 60s` → `{X}s` (ex: `45s`)
- `< 60min` → `{X}m {Y}s` (ex: `2m 30s`)
- `>= 60min` → `{X}h {Y}m` (ex: `1h 15m`)

# Légende des statuts

- `✅` - Phase complétée
- `🔵` - Phase en cours (ajouter `← En cours` à la fin)
- `⬜` - Phase à faire

# Si aucun workflow actif

Afficher :

```
📭 Aucun workflow actif

Pour démarrer un nouveau workflow :
  /dev:feature <description>

Ou exécuter les phases individuellement :
  /dev:discover <description>
```

# Commandes disponibles

Lister les commandes du workflow :

```
📖 Commandes disponibles

Workflow complet :
  /dev:feature <desc>  - Lance toutes les phases automatiquement

Phases individuelles :
  /dev:discover <desc> - 0. Comprendre le besoin
  /dev:explore         - 1. Explorer le codebase
  /dev:clarify         - 2. Questions de clarification
  /dev:design          - 3. Proposer architectures
  /dev:plan            - 4. Générer le plan
  /dev:code [plan]     - 5. Implémenter
  /dev:review          - 6. QA complète
  /dev:summary         - 7. Résumé final

Utilitaires :
  /dev:debug <error>   - Analyser une erreur
  /dev:log <fichier>   - Ajouter LoggableInterface
```
