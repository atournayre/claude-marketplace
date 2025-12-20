---
name: git-pr
description: >
  Automatise la création de Pull Requests GitHub avec workflow complet :
  QA, commits, assignation milestone/projet, code review automatique.
allowed-tools: [Bash, Read, Write, TodoWrite, AskUserQuestion]
model: claude-sonnet-4-5-20250929
---

# Git PR Skill

## Usage
```
/git:pr [branche-base] [milestone] [projet] [--delete] [--no-review]
```

## Configuration

```bash
SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/skills/git-pr/scripts"
PR_TEMPLATE_PATH=".github/pull_request_template.md"
```

## Workflow

1. Vérifier scopes GitHub (`scripts/check_scopes.sh`)
2. Vérifier template PR (`scripts/verify_pr_template.sh`)
3. Lancer QA intelligente (`scripts/smart_qa.sh`)
4. Analyser changements git (`scripts/analyze_changes.sh`)
5. Confirmer branche de base (ou `AskUserQuestion`)
6. Générer description PR intelligente
7. Push et créer PR (`scripts/create_pr.sh`)
8. Assigner milestone (`scripts/assign_milestone.py`)
9. Assigner projet GitHub (`scripts/assign_project.py`)
10. Code review automatique (si plugin review installé)
11. Nettoyage branche (`scripts/cleanup_branch.sh`)

## Code Review

Si plugin `review` installé, lance 4 agents en parallèle :
- `code-reviewer` - Conformité CLAUDE.md
- `silent-failure-hunter` - Erreurs silencieuses
- `test-analyzer` - Couverture tests
- `git-history-reviewer` - Contexte historique

Agrège résultats (score >= 80) dans commentaire PR.

## Options

| Flag | Description |
|------|-------------|
| `--delete` | Supprimer branche après création PR |
| `--no-review` | Désactiver code review automatique |

## References

- [Template review](references/review-template.md) - Format commentaire et agents
- [Todos template](references/todos-template.md) - TodoWrite et génération description

## Error Handling

- Template absent → ARRÊT
- QA échouée → ARRÊT
- Milestone/projet non trouvé → WARNING (non bloquant)
