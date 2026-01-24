---
name: git-pr
description: >
  Crée une Pull Request GitHub standard avec workflow complet :
  QA, commits, assignation milestone/projet, code review automatique.
allowed-tools: [Bash, Read, Write, TaskCreate, TaskUpdate, TaskList, AskUserQuestion]
model: claude-sonnet-4-5-20250929
---

# Git PR Skill (Standard)

## Usage
```
/git:pr [branche-base] [milestone] [projet] [--no-interaction] [--delete] [--no-review]
```

## Configuration

```bash
CORE_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/git-pr-core/scripts"
PR_TEMPLATE_PATH=".github/PULL_REQUEST_TEMPLATE/default.md"
ENV_FILE_PATH=".env.claude"
```

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

### Initialisation

**Créer les tâches du workflow avec TaskCreate :**

```
TaskCreate #1: Charger config .env.claude
TaskCreate #2: Confirmation initiale (si --no-interaction absent)
TaskCreate #3: Vérifier scopes GitHub
TaskCreate #4: Vérifier template PR
TaskCreate #5: Lancer QA intelligente
TaskCreate #6: Analyser changements git
TaskCreate #7: Confirmer branche de base
TaskCreate #8: Générer description PR
TaskCreate #9: Push et créer PR
TaskCreate #10: Assigner milestone
TaskCreate #11: Assigner projet GitHub
TaskCreate #12: Code review automatique (si plugin installé)
TaskCreate #13: Nettoyage branche locale
```

**Important :**
- Utiliser `activeForm` (ex: "Chargeant config", "Vérifiant scopes GitHub")
- Ne créer la tâche #12 que si plugin review installé ET `--no-review` absent
- Chaque tâche doit être marquée `in_progress` puis `completed`

**Pattern d'exécution pour chaque étape :**
1. `TaskUpdate` → tâche en `in_progress`
2. Exécuter l'étape
3. `TaskUpdate` → tâche en `completed`

### Étapes

1. **Charger configuration depuis `.env.claude`** :
   - Vérifier si le fichier `.env.claude` existe à la racine du projet
   - Si oui, parser les variables (format `KEY=VALUE`) :
     - `MAIN_BRANCH` : branche de base par défaut
     - `PROJECT` : projet GitHub par défaut
   - Pour chaque paramètre manquant dans les arguments :
     - Utiliser la variable d'env correspondante si elle existe
   - Ignorer `.env.claude` si absent (comportement standard)

2. **Confirmation initiale** :
   - Si flag `--no-interaction` présent :
     - Passer toutes les confirmations
     - Utiliser les valeurs pré-remplies (arguments + `.env.claude`) sans validation
     - Continuer directement à l'étape 3
   - Sinon :
     - Confirmer à l'utilisateur que la skill `git:pr` est lancée
     - Résumer tous les paramètres reçus :
       - Branche de base (si fournie)
       - Milestone (si fourni)
       - Projet (si fourni)
       - Flags : `--delete`, `--no-review` (si présents)
     - Demander confirmation explicite avant de continuer

3. Vérifier scopes GitHub (`$CORE_SCRIPTS/check_scopes.sh`)
4. Vérifier template PR (`$CORE_SCRIPTS/verify_pr_template.sh`)
5. Lancer QA intelligente (`$CORE_SCRIPTS/smart_qa.sh`)
6. Analyser changements git (`$CORE_SCRIPTS/analyze_changes.sh`)
7. Confirmer branche de base (ou `AskUserQuestion`)
8. Générer description PR intelligente
9. Push et créer PR avec titre Conventional Commits (`$CORE_SCRIPTS/create_pr.sh`)
10. Assigner milestone (`$CORE_SCRIPTS/assign_milestone.py` - voir [git-pr-core/SKILL.md](../git-pr-core/SKILL.md) pour usage)
11. Assigner projet GitHub (`$CORE_SCRIPTS/assign_project.py` - voir [git-pr-core/SKILL.md](../git-pr-core/SKILL.md) pour usage)
12. Code review automatique (si plugin review installé)
13. Nettoyage branche locale (`$CORE_SCRIPTS/cleanup_branch.sh` - branche remote préservée)

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
| `--delete` | Supprimer branche LOCALE uniquement après création PR (JAMAIS la branche remote) |
| `--no-review` | Désactiver code review automatique |

## References

- [Template review](../git-pr-core/references/review-template.md) - Format commentaire et agents
- [Todos template](../git-pr-core/references/todos-template.md) - TodoWrite et génération description

## Task Management

**Progression du workflow :**
- 13 tâches créées à l'initialisation (ou 12 si `--no-review` ou pas de plugin review)
- Chaque étape suit le pattern : `in_progress` → exécution → `completed`
- Utiliser `TaskList` pour voir la progression globale
- Les tâches permettent à l'utilisateur de suivre l'avancement de la création de PR

## Règles critiques

⚠️ **INTERDICTION ABSOLUE** :
- Ne JAMAIS exécuter `git push origin --delete <branche>` ou `git push -d origin <branche>`
- Ne JAMAIS supprimer la branche remote (fermerait automatiquement la PR)
- Le flag `--delete` ne concerne QUE la branche locale

## Error Handling

- Template absent → ARRÊT
- QA échouée → ARRÊT
- Milestone/projet non trouvé → WARNING (non bloquant)
