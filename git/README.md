# Plugin Git

Workflow Git complet : branches, commits, conflits, PR.

## Installation

```bash
/plugin install git@atournayre
```

## Commandes

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

### `/git:commit`

Créer des commits bien formatés avec format conventional et emoji.

**Arguments :**
```bash
/git:commit [message]
/git:commit --no-verify
/git:commit --push
```

**Format Conventional Commits :**
```
<emoji> <type>: <description>

[body optionnel]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types disponibles :**
- `feat` ✨ - Nouvelle fonctionnalité
- `fix` 🐛 - Correction de bug
- `docs` 📝 - Documentation
- `refactor` ♻️ - Refactorisation
- `test` ✅ - Tests
- `chore` 🔧 - Maintenance
- `perf` ⚡ - Performance
- `style` 💄 - Formatage
- `ci` 👷 - CI/CD
- `build` 📦 - Build
- `revert` ⏪ - Revert

**Exemples :**
```bash
# Commit simple
/git:commit "feat: add user login"

# Sans hooks
/git:commit "fix: correct validation" --no-verify

# Commit et push
/git:commit "docs: update README" --push
```

**Workflow :**
- Analyse des changements staged/unstaged
- Génération message selon conventions
- Commit avec emoji approprié
- Gestion des pre-commit hooks
- Push optionnel

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

### `/git:release-notes`

**🔹 Skill disponible : `release-notes`**

Génère des notes de release HTML orientées **utilisateurs finaux** (sans jargon technique).

**Arguments :**
```bash
/git:release-notes <branche-source> <branche-cible> [nom-release]
```

> **Note :** Si les arguments obligatoires ne sont pas fournis, la commande les demandera interactivement.

**Exemples :**
```bash
# Notes de release
/git:release-notes release/v27.0.0 main

# Avec nom personnalisé
/git:release-notes release/v27.0.0 develop "Version 27"
```

**Différence avec `/git:release-report` :**

| Aspect | release-report | release-notes |
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
/git:pr [branch-base] [milestone] [project] [--delete] [--no-review]
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
```

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

## Skills Disponibles

### `release-notes`

**Localisation :** `skills/release-notes/`

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

## Agents Disponibles

### `git-history-reviewer`

**Localisation :** `agents/git-history-reviewer.md`

Agent spécialisé pour analyser le contexte historique git et détecter des problèmes potentiels dans les changements actuels.

**Analyse :**
- Git blame des lignes modifiées
- Historique des commits sur fichiers touchés
- PRs précédentes pertinentes (via GitHub)
- TODOs/FIXMEs existants dans les fichiers modifiés

**Détection :**
- Patterns récurrents (code modifié plusieurs fois)
- Régressions potentielles (corrections annulées)
- TODOs oubliés
- Contexte perdu (ignoré dans blame)

**Scoring :**
- 0-25 : Faux positif probable
- 26-50 : Mineur
- 51-75 : Réel mais pas critique
- 76-100 : Problème confirmé par l'historique

Ne reporte que les problèmes avec score >= 70.

**Modèle :** haiku

**Outils :** Bash, Read, Grep

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
