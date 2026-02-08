---
name: dev:parallel-implement
description: Implémentation parallèle de N issues via worktrees isolés
argument-hint: <issue1> <issue2> [issue3...]
model: sonnet
allowed-tools: [Task, TaskCreate, TaskUpdate, TaskList, TeamCreate, TeamDelete, SendMessage, Bash, Read, Write, Edit, Grep, Glob, Skill]
version: 1.0.0
license: MIT
---

# Objectif

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

Implémenter N issues en parallèle via worktrees isolés. Chaque issue est traitée par un agent indépendant dans son propre worktree.

# Issues demandées

$ARGUMENTS

# Workflow

## 1. Parser les numéros d'issues

Extraire les numéros d'issues depuis les arguments :

```bash
# Exemple: /dev:parallel-implement 101 102 103
ISSUES=($ARGUMENTS)
```

Valider que chaque argument est un numéro valide.

## 2. Health check RAM

```bash
AVAILABLE_RAM=$(free -m | grep Mem | awk '{print $7}')
```

- Si RAM < 2 GB : abort avec message
- **Max 3 agents parallèles** (même si plus d'issues)
- Si plus de 3 issues : traiter par lots de 3

## 3. Créer les worktrees

Pour chaque issue :

```bash
# Récupérer le titre de l'issue pour le slug
ISSUE_TITLE=$(gh issue view $ISSUE_NUMBER --json title -q '.title')
SLUG=$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

git worktree add ".worktrees/issue-${ISSUE_NUMBER}-${SLUG}" -b "feature/issue-${ISSUE_NUMBER}"
```

## 4. Créer l'équipe

```
TeamCreate("parallel-impl")
```

Créer une tâche par issue :

```
TaskCreate : "Issue #101 - {titre}"
TaskCreate : "Issue #102 - {titre}"
```

## 5. Spawner les agents

Pour chaque issue (max 3 en parallèle) :

```
Task(
  subagent_type="general-purpose",
  team_name="parallel-impl",
  name="impl-{issue_number}",
  max_turns=30,
  prompt="
    Tu travailles dans le worktree .worktrees/issue-{issue_number}-{slug}.
    Change ton répertoire de travail vers ce worktree.

    Exécute /dev:implement pour l'issue #{issue_number}.
    Description de l'issue : {issue_description}

    Quand terminé, signale-le au team lead.
  "
)
```

## 6. Surveiller la progression

Le team lead :
- Attend les messages des agents
- Suit la progression via `TaskList`
- Gère les erreurs (retry ou skip)

## 7. Créer les PRs

Pour chaque issue complétée :

```bash
cd ".worktrees/issue-${ISSUE_NUMBER}-${SLUG}"
git push -u origin "feature/issue-${ISSUE_NUMBER}"
gh pr create --title "feat: ${ISSUE_TITLE}" --body "Closes #${ISSUE_NUMBER}"
```

## 8. Cleanup

```bash
# Supprimer les worktrees
for issue in "${ISSUES[@]}"; do
    git worktree remove ".worktrees/issue-${issue}-*" 2>/dev/null || true
done

git worktree prune
```

```
TeamDelete()
```

# Rapport final

```
✅ Implémentation parallèle terminée

  Issues traitées : X/Y
  PRs créées :
  - PR #N1 : Issue #101 - {titre} -> {url}
  - PR #N2 : Issue #102 - {titre} -> {url}

  Échecs : (aucun | liste avec raisons)
```

# Règles

- **Max 3 agents parallèles** (limiter consommation RAM)
- **Worktree isolé** par issue (pas de conflits)
- **Chaque agent** utilise `/dev:implement`
- **Cleanup obligatoire** des worktrees en fin de workflow
- **TeamDelete** après fin de tous les agents
- **Restriction** : ne JAMAIS créer de commits Git directement, seulement via les agents
