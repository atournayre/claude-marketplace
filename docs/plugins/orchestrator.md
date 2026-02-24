---
title: "orchestrator"
description: "Orchestrateur de workflows de développement : feature complète, mode automatique, implémentation parallèle, équipes d'agents"
version: "1.1.0"
---

# orchestrator <Badge type="info" text="v1.1.0" />

Orchestrateur de workflows de développement : feature complète, mode automatique, implémentation parallèle, équipes d'agents.

## Installation

```bash
/plugin install orchestrator@atournayre
```

## Skills Disponibles

Le plugin orchestrator fournit 9 skills :

### `/orchestrator:feature`

Workflow complet de développement de feature. Mode interactif (description texte) avec 8 phases et checkpoints utilisateur. Mode automatique (numéro issue GitHub) avec 10 phases sans interaction.

### `/orchestrator:team`

Orchestre une équipe d'agents spécialisés pour les tâches complexes. Auto-détecte le type (feature/refactor/api/fix), compose l'équipe, coordonne les phases analyse → challenge → implémentation → QA.

### `/orchestrator:parallel`

Implémentation parallèle de N issues GitHub via worktrees isolés. Chaque issue est traitée par un agent indépendant. Max 3 agents simultanés.

### `/orchestrator:ralph`

Setup du loop autonome de développement Ralph. Crée la structure `.claude/ralph/`, génère le PRD interactivement.

### `/orchestrator:status`

Affiche l'état actuel du workflow de développement (phases complétées, en cours, à faire).

### `/orchestrator:validate`

Vérifie la checklist (PHP, API ou sécurité) avant exécution.

### `/orchestrator:transform`

Transforme un prompt quelconque en prompt exécutable structuré avec TaskCreate/TaskUpdate/TaskList.

### `/orchestrator:check-prerequisites`

Vérifie tous les prérequis système avant de lancer un workflow automatique.

### `/orchestrator:fetch-issue`

Récupère et valide le contenu d'une issue GitHub pour le workflow automatique.

## Changelog

- Voir CHANGELOG.md
