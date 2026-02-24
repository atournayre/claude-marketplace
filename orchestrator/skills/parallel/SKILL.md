---
name: orchestrator:parallel
description: Implémentation parallèle de N issues GitHub via worktrees isolés. Chaque issue est traitée par un agent indépendant. Max 3 agents simultanés.
argument-hint: <issue1> <issue2> [issue3...]
model: sonnet
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, SendMessage, Bash, Read, Write, Edit, Grep, Glob, Skill]
version: 1.0.0
license: MIT
---

# orchestrator:parallel

Implémentation parallèle de N issues via worktrees isolés.

## Instructions à Exécuter

### 1. Parser les numéros d'issues

```bash
ISSUES=($ARGUMENTS)
```

Valider que chaque argument est un numéro valide.

### 2. Health check RAM

```bash
AVAILABLE_RAM=$(free -m | grep Mem | awk '{print $7}')
```

- RAM < 2 GB : abort avec message
- Max 3 agents parallèles (même si plus d'issues)
- Si plus de 3 issues : traiter par lots de 3

### 3. Créer les worktrees

Pour chaque issue :

```bash
ISSUE_TITLE=$(gh issue view $ISSUE_NUMBER --json title -q '.title')
SLUG=$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
git worktree add ".worktrees/issue-${ISSUE_NUMBER}-${SLUG}" -b "feature/issue-${ISSUE_NUMBER}"
```

### 4. Créer l'équipe et les tâches

```
TeamCreate("parallel-impl")
```

Pour chaque issue, créer une tâche :
```
TaskCreate : "Issue #N - {titre}"
```

### 5. Spawner les agents (max 3 en parallèle)

Pour chaque issue :

```
Task(
  subagent_type="general-purpose",
  team_name="parallel-impl",
  name="impl-{issue_number}",
  max_turns=30,
  prompt="
    Tu travailles dans le worktree .worktrees/issue-{issue_number}-{slug}.
    Exécute /orchestrator:feature {issue_number} --auto
    Quand terminé, signale-le au team lead.
  "
)
```

### 6. Surveiller la progression

- Attendre les messages des agents
- Suivre la progression via TaskList
- Gérer les erreurs (retry ou skip)

### 7. Créer les PRs

Pour chaque issue complétée :

```bash
cd ".worktrees/issue-${ISSUE_NUMBER}-${SLUG}"
git push -u origin "feature/issue-${ISSUE_NUMBER}"
gh pr create --title "feat: ${ISSUE_TITLE}" --body "Closes #${ISSUE_NUMBER}"
```

### 8. Cleanup

```bash
git worktree prune
TeamDelete()
```

## Rapport final

```
Implémentation parallèle terminée

  Issues traitées : X/Y
  PRs créées :
  - PR #N1 : Issue #101 - {titre} -> {url}

  Echecs : (aucun | liste avec raisons)
```

## Règles

- Max 3 agents parallèles
- Worktree isolé par issue
- Cleanup obligatoire des worktrees
- TeamDelete après fin de tous les agents
- Ne jamais créer de commits Git directement (seulement via les agents)
