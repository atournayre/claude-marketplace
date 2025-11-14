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

**Exemples :**
```bash
# Rapport release vs main
/git:release-report release/v27.0.0 main

# Avec nom custom
/git:release-report release/v27.0.0 develop v27.0.0

# Feature vs main
/git:release-report feature/new-module main "Module XYZ"
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
