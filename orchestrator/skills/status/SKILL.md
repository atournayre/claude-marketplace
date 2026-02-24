---
name: orchestrator:status
description: Affiche l'état actuel du workflow de développement (phases complétées, en cours, à faire) avec timings depuis le fichier d'état.
model: haiku
allowed-tools: [Read, Glob]
version: 1.0.0
license: MIT
---

# orchestrator:status

Affiche l'état courant du workflow de développement.

## Instructions à Exécuter

1. Chercher `.claude/data/.dev-workflow-state.json` dans le répertoire courant
2. Si le fichier existe, lire l'état du workflow
3. Afficher le plan avec les statuts de chaque phase

## Format de sortie

```
Workflow de développement

  {status} 0. Discover   - Comprendre le besoin     {duration}
  {status} 1. Explore    - Explorer codebase        {duration}
  {status} 2. Clarify    - Questions clarification  {duration}
  {status} 3. Design     - Proposer architectures   {duration}
  {status} 4. Plan       - Générer specs            {duration}
  {status} 5. Code       - Implémenter              {duration}
  {status} 6. Review     - QA complète              {duration}
  {status} 7. Summary    - Résumé final             {duration}

Feature: "{feature_description}"
Plan: {plan_path}
Temps total: {total_duration}
```

## Légende des statuts

- Phase complétée : `[OK]`
- Phase en cours : `[>>]` + `<- En cours`
- Phase à faire : `[ ]`

## Affichage des durées

- `completed` avec `durationMs` → `({formatted_duration})`
- `in_progress` avec `startedAt` → `(en cours depuis {elapsed})`
- Pas de timing → rien afficher

## Format de durée

- `< 60s` → `{X}s`
- `< 60min` → `{X}m {Y}s`
- `>= 60min` → `{X}h {Y}m`

## Si aucun workflow actif

```
Aucun workflow actif

Pour démarrer un nouveau workflow :
  /orchestrator:feature <description>
```

## Commandes disponibles

```
Workflow complet :
  /orchestrator:feature <desc>  - Lance toutes les phases

Utilitaires :
  /orchestrator:status          - Afficher l'état courant
  /orchestrator:parallel <N1> <N2>  - Implémenter N issues en parallèle
```
