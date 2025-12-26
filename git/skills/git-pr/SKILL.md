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
7. Push et créer PR avec titre Conventional Commits (`scripts/create_pr.sh`)
   - Copie automatique des labels depuis l'issue liée
   - Labels CD si projet en CD (`scripts/apply_cd_labels.sh`)
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

## Labels CD (Continuous Delivery)

Détection automatique si le repo contient des labels `version:*`.

**Ordre de détection du type de version :**
1. `BREAKING CHANGE` ou `!:` dans commits → `version:major`
2. Labels de l'issue liée (insensible casse, ignore emojis) :
   - Patterns minor : `enhancement`, `feature`, `feat`, `nouvelle`, `new`
   - Patterns patch : `bug`, `fix`, `bugfix`, `correction`, `patch`
3. Nom de branche : `feat/*`, `feature/*` → minor / `fix/*`, `hotfix/*` → patch
4. Premier commit de la branche : `feat:` → minor / `fix:` → patch
5. Si indéterminé → message `CD_NEED_USER_INPUT`

**Si `CD_NEED_USER_INPUT` apparaît :** Utiliser `AskUserQuestion` pour demander :
> "Cette PR est une nouvelle fonctionnalité (minor) ou une correction (patch) ?"
Puis appliquer le label manuellement : `gh pr edit <PR> --add-label "version:minor|patch"`

**Feature flag :**
- Détecté si fichiers `.twig` modifiés contiennent `Feature:Flag` ou `Feature/Flag`
- Applique le label `🚩 Feature flag`

**Création labels :** Si labels absents, ils sont créés automatiquement avec couleurs appropriées.

## Error Handling

- Template absent → ARRÊT
- QA échouée → ARRÊT
- Milestone/projet non trouvé → WARNING (non bloquant)
