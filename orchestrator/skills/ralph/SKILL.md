---
name: orchestrator:ralph
description: Setup du loop autonome de développement Ralph. Crée la structure .claude/ralph/, génère le PRD interactivement ou pour une feature spécifique, et affiche la commande à exécuter. NE lance jamais ralph.sh automatiquement.
argument-hint: "[project-path] [-i/--interactive] [-f/--feature <name>]"
model: sonnet
allowed-tools: [Read, Write, Edit, Bash, Glob, AskUserQuestion]
version: 1.0.0
license: MIT
---

# orchestrator:ralph

Setup du loop autonome de développement Ralph. **Ce skill ONLY configure Ralph — l'utilisateur lance les commandes lui-même.**

## Règle critique

- NEVER lancer ralph.sh ou des commandes d'exécution automatiquement
- NEVER exécuter le loop — seulement créer les fichiers et afficher les instructions
- ALWAYS laisser l'utilisateur copier et exécuter les commandes lui-même
- ALWAYS terminer en affichant la commande exacte à exécuter

## Paramètres

| Flag | Description |
|------|-------------|
| `<project-path>` | Chemin vers le projet (défaut: répertoire courant) |
| `-i, --interactive` | Mode interactif: brainstorm PRD avec assistance IA |
| `-f, --feature <name>` | Nom du dossier feature (ex: `01-add-auth`) |

## Instructions à Exécuter

### 1. Parser les arguments

Extraire depuis `$ARGUMENTS` :
- `project_path` : chemin projet (défaut: `.`)
- `interactive_mode` : true si `-i` ou `--interactive`
- `feature_name` : valeur après `-f` ou `--feature`

### 2. Créer la structure Ralph

```bash
mkdir -p {project_path}/.claude/ralph
```

Créer les fichiers Ralph nécessaires :
- `ralph.sh` : script principal du loop
- Structure de feature si `feature_name` fourni

### 3. Mode interactif (si -i)

Brainstormer le PRD avec l'utilisateur via AskUserQuestion :
- Objectif de la feature
- User stories principales
- Critères d'acceptation
- Contraintes techniques

### 4. Transformer le PRD en user stories

Créer `{feature_dir}/prd.json` avec les user stories formatées.

### 5. Afficher la commande à exécuter

```
Setup Ralph terminé

Structure créée :
  {project_path}/.claude/ralph/

Pour lancer Ralph :
  bun run .claude/ralph/ralph.sh -f {feature_name}
```

## Résultat attendu

- Structure `.claude/ralph/` créée dans le projet
- Dossier feature avec PRD.md, prd.json, progress.txt
- User stories correctement formatées dans prd.json
- Commande claire fournie à l'utilisateur (il l'exécute lui-même)
