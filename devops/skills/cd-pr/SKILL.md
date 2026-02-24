---
name: devops:cd-pr
description: >
  Crée une Pull Request en mode Continuous Delivery avec workflow complet :
  QA, labels version (major/minor/patch), feature flags, code review automatique.
allowed-tools: [Bash, Read, Write, TaskCreate, TaskUpdate, TaskList, AskUserQuestion]
model: sonnet
version: 1.0.0
license: MIT
---

# DevOps CD PR Skill (Continuous Delivery)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

## Usage
```
/devops:cd-pr [branche-base] [milestone] [projet] [--no-interaction] [--delete] [--no-review]
```

## Configuration

```bash
CORE_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/../git/skills/git-pr-core/scripts"
SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/../git/skills/git-cd-pr/scripts"
PR_TEMPLATE_PATH=".github/PULL_REQUEST_TEMPLATE/cd_pull_request_template.md"
ENV_FILE_PATH=".env.claude"
```

> Note : Les scripts partagés sont dans le plugin `git` (déprécié mais disponible).
> Références : `git/skills/git-pr-core/scripts/` et `git/skills/git-cd-pr/scripts/`

## Workflow

### Initialisation

**Créer les tâches du workflow :**

```
TaskCreate #1: Charger config .env.claude
TaskCreate #2: Confirmation initiale (si --no-interaction absent)
TaskCreate #3: Vérifier scopes GitHub
TaskCreate #4: Vérifier template PR CD
TaskCreate #5: Lancer QA intelligente
TaskCreate #6: Analyser changements git
TaskCreate #7: Confirmer branche de base
TaskCreate #8: Générer description PR
TaskCreate #9: Push et créer PR
TaskCreate #10: Copier labels depuis issue liée
TaskCreate #11: Appliquer labels CD (version + feature flag)
TaskCreate #12: Assigner milestone
TaskCreate #13: Assigner projet GitHub
TaskCreate #14: Code review automatique (si plugin installé)
TaskCreate #15: Nettoyage branche locale
```

**Important :**
- Utiliser `activeForm` (ex: "Chargeant config", "Appliquant labels CD")
- Ne créer la tâche #14 que si plugin review installé ET `--no-review` absent
- Chaque tâche doit être marquée `in_progress` puis `completed`

### Étapes

1. **Charger configuration depuis `.env.claude`** :
   - Parser les variables `MAIN_BRANCH` et `PROJECT`

2. **Confirmation initiale** :
   - Si `--no-interaction` : passer toutes les confirmations
   - Sinon : résumer paramètres (dont mode CD) et demander confirmation

3. Vérifier scopes GitHub (`$CORE_SCRIPTS/check_scopes.sh`)
4. Vérifier template PR CD (`$CORE_SCRIPTS/verify_pr_template.sh`)
5. Lancer QA intelligente (`$CORE_SCRIPTS/smart_qa.sh`)
6. Analyser changements git (`$CORE_SCRIPTS/analyze_changes.sh`)
7. Confirmer branche de base (ou `AskUserQuestion`)
8. Générer description PR intelligente
9. Push et créer PR (`$SCRIPTS_DIR/create_pr.sh`)
10. **Copier labels depuis issue liée** (`$SCRIPTS_DIR/copy_issue_labels.sh`)
11. **Appliquer labels CD** (`$SCRIPTS_DIR/apply_cd_labels.sh`)
12. Assigner milestone (`$CORE_SCRIPTS/assign_milestone.py`)
13. Assigner projet GitHub (`$CORE_SCRIPTS/assign_project.py`)
14. Code review automatique (si plugin review installé)
15. Nettoyage branche locale (`$CORE_SCRIPTS/cleanup_branch.sh`)

## Labels CD (Continuous Delivery)

**Ordre de détection du type de version :**
1. `BREAKING CHANGE` ou `!:` dans commits -> `version:major`
2. Labels de l'issue liée :
   - Patterns minor : `enhancement`, `feature`, `feat`, `nouvelle`, `new`
   - Patterns patch : `bug`, `fix`, `bugfix`, `correction`, `patch`
3. Nom de branche : `feat/*`, `feature/*` -> minor / `fix/*`, `hotfix/*` -> patch
4. Premier commit : `feat:` -> minor / `fix:` -> patch
5. Si indéterminé -> `AskUserQuestion`

**Feature flag :**
- Détecté si fichiers `.twig` modifiés contiennent `Feature:Flag` ou `Feature/Flag`
- Applique le label `Feature flag`

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
| `--no-interaction` | Mode automatique : passer confirmations, utiliser defaults |
| `--delete` | Supprimer branche LOCALE uniquement après création PR |
| `--no-review` | Désactiver code review automatique |

## Règles critiques

**INTERDICTION ABSOLUE** :
- Ne JAMAIS exécuter `git push origin --delete <branche>` ou `git push -d origin <branche>`
- Ne JAMAIS supprimer la branche remote (fermerait automatiquement la PR)
- Le flag `--delete` ne concerne QUE la branche locale

## Error Handling

- Template absent -> ARRÊT
- QA échouée -> ARRÊT
- Version non déterminée -> `AskUserQuestion` (non bloquant)
- Milestone/projet non trouvé -> WARNING (non bloquant)
