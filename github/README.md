# Plugin GitHub

Gestion GitHub : issues, PR, analyse d'impact.

## Installation

```bash
/plugin install github@atournayre
```

## Prérequis

- `gh` CLI installé et configuré
- Repository GitHub
- Token d'accès GitHub configuré

## Commandes

### `/github:fix`

Corriger une issue GitHub avec workflow simplifié et efficace.

**Arguments :**
```bash
/github:fix [issue-number]
```

**Exemples :**
```bash
# Fix issue #123
/github:fix 123

# Fix sans numéro (demande interactivement)
/github:fix
```

**Workflow :**
1. Récupère détails de l'issue via `gh`
2. Analyse description et labels
3. Crée branche `fix/123-issue-title`
4. Guide implémentation du fix
5. Crée tests reproductibles
6. Commit avec référence issue
7. Optionnel : crée PR automatiquement

**Format commit :**
```
🐛 fix: resolve issue description

Fixes #123

- Detail 1
- Detail 2

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### `/github:impact`

Analyse le détail des modifications git et fournit 2 rapports d'impact (métier + technique).

**Arguments :**
```bash
/github:impact <pr-number>
```

**Exemple :**
```bash
/github:impact 456
```

**Workflow :**
1. Récupère diff de la PR via `gh pr diff`
2. Analyse tous les changements
3. Catégorise par type :
   - Features
   - Fixes
   - Refactoring
   - Breaking changes
4. Génère 2 rapports :
   - **Rapport Métier** : impact fonctionnel
   - **Rapport Technique** : impact code/architecture
5. Ajoute rapports à la description de la PR

**Rapport Métier :**
```markdown
## 📊 Impact Métier

### Nouvelles Fonctionnalités
- Authentification utilisateur
- Export PDF des rapports

### Améliorations
- Performance de recherche (+40%)
- UX du formulaire de contact

### Corrections
- Bug validation email
- Erreur affichage mobile

### ⚠️ Breaking Changes
- API endpoint `/users` renommé en `/accounts`
```

**Rapport Technique :**
```markdown
## 🔧 Impact Technique

### Architecture
- Ajout service AuthenticationService
- Refactoring UserRepository
- Migration database (add user_roles table)

### Dépendances
- symfony/security ^6.4
- doctrine/orm ^2.16

### Tests
- 15 tests unitaires ajoutés
- 5 tests d'intégration modifiés
- Couverture : 78% → 82%

### Performance
- Optimisation requêtes SQL (N+1 eliminated)
- Cache Redis pour sessions

### ⚠️ Migrations Requises
- `php bin/console doctrine:migrations:migrate`
- Clear cache production
```

**Post-rapport :**
- Rapports ajoutés automatiquement à la description PR
- Facilite code review
- Documente les changements

## Workflow Complet

### Fix Issue Standard

```bash
# 1. Corriger issue
/github:fix 123

# 2. Implémenter fix guidé

# 3. Analyser impact de la PR créée
/github:impact <pr-number>

# 4. Review avec rapports d'impact
```

### Analyse PR Existante

```bash
# Analyser impact PR existante
/github:impact 456

# Rapports ajoutés à la description
# Review facilitée
```

## Configuration

`.claude/plugins.settings.json` :
```json
{
  "atournayre-claude-plugin-marketplace": {
    "github": {
      "auto_assign": true,
      "default_labels": [],
      "pr": {
        "add_impact_report": true
      }
    }
  }
}
```

### Options

- `auto_assign` (bool) : Auto-assign issues (défaut: `true`)
- `default_labels` (array) : Labels par défaut (défaut: `[]`)
- `pr.add_impact_report` (bool) : Ajouter rapport d'impact auto (défaut: `true`)

### Utilisation avec Config

```bash
# Avec auto_assign: true configuré
/github:fix 123                    # Auto-assigné

# Avec pr.add_impact_report: true configuré
/github:impact 456                 # Rapport ajouté auto à la PR
```

## Cas d'Usage

**Fix rapide :**
- Issue simple
- `/github:fix 123`
- Commit + PR automatique

**Fix complexe :**
- Issue avec multiples fichiers
- `/github:fix 456`
- Guidance étape par étape
- Tests reproductibles
- `/github:impact <pr>` pour documenter

**Code Review :**
- PR à reviewer
- `/github:impact 789`
- Rapports métier + technique
- Décision éclairée

## Licence

MIT
