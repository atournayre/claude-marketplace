---
description: Affiche le workflow et l'étape courante
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob
---

# Objectif

Afficher l'état actuel du workflow de développement pour que l'utilisateur sache où il en est.

# Instructions

1. Chercher un fichier `.claude/data/.dev-workflow-state.json` dans le répertoire courant
2. Si le fichier existe, lire l'état du workflow
3. Afficher le plan avec les statuts de chaque phase

# Format de sortie

```
🔄 Workflow de développement

  {status} 0. Discover   - Comprendre le besoin
  {status} 1. Explore    - Explorer codebase
  {status} 2. Clarify    - Questions clarification
  {status} 3. Design     - Proposer architectures
  {status} 4. Plan       - Générer specs
  {status} 5. Code       - Implémenter
  {status} 6. Review     - QA complète
  {status} 7. Summary    - Résumé final

📋 Feature: "{feature_description}"
📁 Plan: {plan_path}
```

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
