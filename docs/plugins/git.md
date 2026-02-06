---
title: "git"
description: "Workflow Git complet  - branches, commits, conflits, PR avec automation QA"
version: "1.12.0"
---

# git <Badge type="info" text="v1.12.0" />


Workflow Git complet : branches, commits, conflits, PR.

## Installation

```bash
/plugin install git@atournayre
```

## Skills Disponibles

Le plugin git fournit 9 skills (format natif Claude Code) :

## Task Management System

**Nouveauté v1.9.1** : Les skills de workflow PR intègrent le task management system pour un suivi détaillé.

### Skills avec task management

| Skill | Nombre de tâches | Type de workflow |
|-------|------------------|------------------|
| `git-pr` | 13 tâches | Workflow création PR standard |
| `git-cd-pr` | 15 tâches | Workflow CD avec labels version |
| `git:gen-release-notes` | 5 tâches | Génération notes de release |

### Fonctionnalités

- **Progression visible** : Suivi étape par étape de la création de PR
- **Statuts clairs** : pending → in_progress → completed
- **Workflow complet** : De la QA à la création de PR en passant par le code review
- **Tâches conditionnelles** : Review automatique seulement si plugin installé

---

### `/git:branch`

Création de branche Git avec workflow structuré.

**Arguments :**
```bash
/git:branch <source-branch> [issue-number-or-text]
```

**Exemples :**
```bash
# Depuis main avec numéro d'issue
/git:branch main 123

# Depuis main avec description
/git:branch main "add user authentication"

# Depuis develop
/git:branch develop 456
```

**Workflow :**
- Vérifie branche source existe
- Crée branche avec nom normalisé
- Format : `feature/123-short-description` ou `feature/add-user-authentication`
- Checkout automatique
- Push upstream si configuré

---

### `/git:commit` ⭐ v1.12.0 - REFONTE

Créer des commits bien formatés avec format conventional et emoji, avec **Task Management System intégré**.

**Arguments :**
```bash
/git:commit [--verify] [--no-push]
```

**Nouveautés v1.12.0 :**
- ✅ **Task Management System** : Chaque étape trackée via TaskCreate/TaskUpdate
- ✅ **5 tâches** : Vérification → Analyse → Stratégie → Création → Push
- ✅ **Détection automatique** de division des commits (feat + docs, fix + refactor, etc.)
- ✅ **20+ emojis spécialisés** : Table complète avec contextes (breaking, security, hotfix, etc.)
- ✅ **Mode HEREDOC obligatoire** : Format sécurisé pour messages commits
- ✅ **Directives de division** : Quand créer plusieurs commits

**Format Conventional Commits :**
```
<emoji> <type>(<scope>): <description impérative courte>

[body optionnel - explique le "pourquoi"]

[footer optionnel - références issues]
```

**Types disponibles (10) :**
- `feat` ✨ - Nouvelle fonctionnalité
- `fix` 🐛 - Correction de bug
- `docs` 📝 - Documentation
- `refactor` ♻️ - Refactorisation
- `test` ✅ - Tests
- `chore` 🔧 - Maintenance
- `perf` ⚡ - Performance
- `style` 💄 - Formatage
- `ci` 🚀 - CI/CD
- `revert` ⏪ - Annulation

**Emojis spécialisés (10+) :**
- `💥` Breaking change
- `🔒️` Sécurité
- `🚑️` Hotfix critique
- `✏️` Faute de frappe
- `🚧` WIP
- `🚨` Lint warnings
- Et bien d'autres...

**Exemples :**
```bash
# Commit simple (Task Management automatique)
/git:commit

# Avec vérification QA avant commit
/git:commit --verify

# Sans push automatique
/git:commit --no-push

# Combinaison
/git:commit --verify --no-push
```

**Workflow (5 étapes) :**
1. **Vérifier les changements** - git status, staging automatique si nécessaire
2. **Analyser le diff** - Détection des types de changements
3. **Déterminer la stratégie** - Décision : 1 ou plusieurs commits
4. **Créer le(s) commit(s)** - Messages formatés avec HEREDOC
5. **Push vers remote** - Automatique (sauf `--no-push`)

**Task Management (nouveau v1.12.0) :**
- ✅ Progression visible via 5 tâches
- ✅ Validation avant chaque étape
- ✅ Checklist complète de validation finale
- ✅ Impossibilité de skip une étape

---

### `/fix-pr-comments` ⭐ NOUVEAU

Récupère et implémente systématiquement TOUS les commentaires de review PR.

**Usage :**
```bash
# Auto-détecte la PR de la branche courante
/fix-pr-comments

# PR spécifique
/fix-pr-comments 123
```

**Workflow automatisé :**
1. **Fetch comments** : Récupère via `gh pr review list` + `gh api`
   - Review comments (CHANGES_REQUESTED)
   - Inline code comments
2. **Analyze & plan** : Extrait file:line, groupe par fichier
3. **Implement fixes** : Batch avec MultiEdit pour efficacité
4. **Commit & push** : `fix: address PR review comments`

**Features :**
- ✅ Batched MultiEdit pour same-file modifications (efficacité)
- ✅ ALWAYS Read files BEFORE editing (sécurité)
- ✅ Checklist avec progression visible
- ✅ STAY IN SCOPE : never fix unrelated issues
- ✅ Auto-commit + auto-push

**Exemple output :**
```
✅ Fetched 5 review comments
📋 Plan:
  - src/User.php (3 comments)
  - tests/UserTest.php (2 comments)

🔧 Implementing fixes...
  ✅ src/User.php: Addressed 3 comments
  ✅ tests/UserTest.php: Addressed 2 comments

✅ Committed and pushed: fix: address PR review comments
```

---

### `/git:conflit`

Analyse les conflits git et propose une résolution pas à pas avec validation de chaque étape.

**Arguments :**
```bash
/git:conflit <branche-destination>
```

**Exemples :**
```bash
/git:conflit main
/git:conflit develop
```

**Workflow :**
- Détecte conflits entre branche courante et destination
- Liste fichiers en conflit
- Analyse chaque conflit
- Propose résolution pour chaque fichier
- Validation étape par étape
- Test après résolution
- Commit de merge

**Rapport :**
```
🔀 Analyse des conflits

Fichiers en conflit : 3
- src/User.php (5 conflits)
- src/Auth.php (2 conflits)
- config/services.yaml (1 conflit)

Résolution proposée :
[détail par fichier]

Validation : [étape par étape]
```

---

### `/git:release-report`

Génère un rapport HTML d'analyse d'impact entre deux branches.

**Arguments :**
```bash
/git:release-report <branche-source> <branche-cible> [nom-release]
```

> **Note :** Si les arguments obligatoires ne sont pas fournis, la commande les demandera interactivement.

**Exemples :**
```bash
# Rapport release vs main
/git:release-report release/v27.0.0 main

# Avec nom custom
/git:release-report release/v27.0.0 develop v27.0.0

# Feature vs main
/git:release-report feature/new-module main "Module XYZ"

# Sans arguments (mode interactif)
/git:release-report
```

**Contenu du rapport :**
- Statistiques globales (fichiers, lignes, commits)
- Répartition par type de fichier (PHP, Twig, JS, etc.)
- Fonctionnalités principales extraites depuis commits
- Impact métier par domaine fonctionnel
- Qualité et maintenabilité
- KPI visuels orientés Product Owner

**Sortie :**
```
REPORT_PATH/impact_<nom-release>.html
```

**Format :**
- HTML auto-suffisant avec CSS inline
- Design moderne (gradient violet)
- KPI avec couleurs par impact
- Charts et progress bars
- Responsive et imprimable

---

### `/git:pr`

Crée une Pull Request optimisée avec workflow structuré.

**Arguments :**
```bash
/git:pr [branch-base] [milestone] [project] [--cd | --no-cd] [--no-interaction] [--delete] [--no-review]
```

**Features :**
- Détection automatique mode Standard vs CD
- QA complète avant création (PHPStan, tests, linting)
- Vérification branche à jour avec origin
- Templates PR adaptés

---

### `/git:gen-release-notes`

**🔹 Skill disponible : `gen-release-notes`**

Génère des notes de release HTML orientées **utilisateurs finaux** (sans jargon technique).

**Arguments :**
```bash
/git:gen-release-notes <branche-source> <branche-cible> [nom-release]
```

> **Note :** Si les arguments obligatoires ne sont pas fournis, la commande les demandera interactivement.

**Exemples :**
```bash
# Notes de release
/git:gen-release-notes release/v27.0.0 main

# Avec nom personnalisé
/git:gen-release-notes release/v27.0.0 develop "Version 27"
```

**Différence avec `/git:release-report` :**

| Aspect | release-report | gen-release-notes |
|--------|----------------|---------------|
| Public cible | Équipe technique / PO | Utilisateurs finaux |
| Langage | Technique (KPI, stats) | Simple, accessible |
| Contenu | Fichiers, lignes, % | Nouveautés, corrections |
| Focus | Impact code | Bénéfice utilisateur |

**Catégories :**
- **Nouveautés** - Nouvelles fonctionnalités
- **Améliorations** - Optimisations UX/performance
- **Corrections** - Bugs résolus
- **Sécurité** - Si applicable

**Sortie :**
```
REPORT_PATH/release_notes_<nom-release>.html
```

**Format :**
- HTML responsive (mobile-friendly)
- Design moderne et accessible
- Peut être envoyé par email
- Aucune info technique sensible

---

### `/git:pr`

Crée une Pull Request optimisée avec workflow structuré.

**Arguments :**
```bash
/git:pr [branch-base] [milestone] [project] [--delete] [--no-review] [--no-interaction]
```

**Exemples :**
```bash
# PR simple
/git:pr

# PR vers branche spécifique
/git:pr develop

# PR avec milestone
/git:pr main "v1.2.0"

# PR sans demander review
/git:pr --no-review

# PR avec suppression branche après merge
/git:pr --delete

# PR automatisée (depuis config .env.claude)
/git:pr --no-interaction
```

**Configuration Automation (`.env.claude`) :**

Pour automatiser la création de PR sans interaction :

```bash
# .env.claude
MAIN_BRANCH=main
REPO=atournayre/claude-marketplace
PROJECT=
```

**Comportement avec `--no-interaction` :**
- Charge automatiquement `MAIN_BRANCH`, `REPO`, `PROJECT` depuis `.env.claude`
- Utilise les arguments fournis en ligne de commande (priorité haute)
- Ignore les demandes interactives (confirmations, choix)
- Essentiiel pour workflows entièrement automatisés (ex: `/dev:auto:feature`)

**Prérequis :**
- Branche avec commits
- Repository GitHub configuré
- `gh` CLI installé

**Workflow :**
- Analyse tous les commits de la branche
- Génère titre PR depuis commits
- Crée description structurée :
  - Summary (bullet points)
  - Test plan (checklist)
  - Footer Claude Code
- Push branche si nécessaire
- Crée PR via `gh`
- Retourne URL de la PR

**Template PR :**
```markdown
## Summary
- Changement 1
- Changement 2

## Test plan
- [ ] Tests unitaires passent
- [ ] Tests d'intégration OK
- [ ] Testé manuellement

🤖 Generated with Claude Code
```

## Scripts Utilitaires

### `skills/git-pr-core/scripts/smart_qa.sh`

Script de validation QA avant création de Pull Request. Détection automatique des outils disponibles.

**Features :**
- Détection auto des outils QA (PHPStan, PHPUnit, PHP-CS-Fixer)
- Fallbacks multiples : make → vendor/bin → composer
- Pas d'échec si outil manque (feedback clair sur exécution)
- Réutilisable par n'importe quelle skill

**Usage :**
```bash
bash git/skills/git-pr-core/scripts/smart_qa.sh
```

**Exemple de sortie :**
```
🔍 Exécution QA complète avant création PR...
▶️  PHPStan (via vendor/bin)...
✅ PHPStan OK
▶️  Tests (via PHPUnit)...
✅ Tests OK
⚠️  Lint non détecté, ignoré
✅ QA passée avec succès
```

---

### `scripts/commit-emoji.sh`

Script centralisé pour le mapping type → emoji. Source de vérité unique utilisée par les autres scripts.

**Usage :**
```bash
# Sourcer pour utiliser la fonction
source scripts/commit-emoji.sh
emoji=$(get_commit_emoji "feat")  # ✨

# Ou appel direct
./scripts/commit-emoji.sh feat  # ✨
```

**Types supportés :**
| Type | Emoji | Description |
|------|-------|-------------|
| `feat` | ✨ | Nouvelle fonctionnalité |
| `fix` | 🐛 | Correction de bug |
| `docs` | 📝 | Documentation |
| `style` | 💄 | Formatage/style |
| `refactor` | ♻️ | Refactorisation |
| `perf` | ⚡️ | Performance |
| `test` | ✅ | Tests |
| `build` | 📦️ | Build |
| `ci` | 🚀 | CI/CD |
| `chore` | 🔧 | Maintenance |
| `revert` | ⏪️ | Annulation |
| `wip` | 🚧 | Travail en cours |
| `hotfix` | 🚑️ | Hotfix critique |
| `security` | 🔒️ | Sécurité |
| `deps` | ➕ | Dépendances |
| `breaking` | 💥 | Breaking change |

---

## Skills Disponibles

### `gen-release-notes`

**Localisation :** `skills/gen-release-notes/`

Skill spécialisé pour générer des notes de release orientées utilisateurs finaux.

**Fonctionnalités :**
- Transformation commits techniques → descriptions accessibles
- Catégorisation automatique (Nouveautés, Améliorations, Corrections, Sécurité)
- Filtrage des commits internes (tests, CI, refactoring)
- Génération HTML responsive avec CSS inline
- Demande interactive des arguments manquants

**Règles de rédaction :**
- Zéro jargon technique
- Bénéfice utilisateur en premier
- Ton positif et professionnel
- Phrases courtes (1-2 max)

**Modèle :** sonnet

**Outils :** Bash, Read, Write, Grep, Glob, AskUserQuestion

---

## Intégration Plugin Review

Le skill `/git:pr` utilise les agents du plugin `review` pour la code review automatique.

**Si le plugin review est installé**, 4 agents sont invoqués en parallèle :
- `code-reviewer` - Conformité CLAUDE.md, bugs, qualité
- `silent-failure-hunter` - Erreurs silencieuses, catch vides
- `test-analyzer` - Couverture PHPUnit, tests manquants
- `git-history-reviewer` - Contexte historique git

**Installation :**
```bash
/plugin install review@atournayre
```

---

## Workflow Complet

### Feature Standard

```bash
# 1. Créer branche
/git:branch main 123

# 2. Coder...

# 3. Commit
/git:commit "feat: implement feature"

# 4. Pull Request
/git:pr
```

### Hotfix avec Conflit

```bash
# 1. Créer branche hotfix
/git:branch main "fix critical bug"

# 2. Fix et commit
/git:commit "fix: resolve critical issue"

# 3. Si conflit lors du merge
/git:conflit main

# 4. PR
/git:pr
```

## Configuration Recommandée

`.claude/settings.json` :
```json
{
  "git": {
    "conventional_commits": true,
    "emoji": true,
    "auto_push": false,
    "default_branch": "main"
  }
}
```

## Licence

MIT
