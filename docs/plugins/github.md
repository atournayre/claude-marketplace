---
title: "github"
description: "Gestion GitHub  - issues, PR, analyse d'impact avec skills spécialisés"
version: "1.3.1"
---

# github <Badge type="info" text="v1.3.1" />


Gestion GitHub : issues, PR, analyse d'impact.

## Installation

```bash
/plugin install github@atournayre
```

## Prérequis

- `gh` CLI installé et configuré
- Repository GitHub
- Token d'accès GitHub configuré

## Skills Disponibles

Le plugin github fournit 2 skills (format natif Claude Code) :

## Task Management System

**Nouveauté v1.2.1** : Le skill de résolution d'issue intègre le task management system.

### Skill avec task management

| Skill | Nombre de tâches | Type de workflow |
|-------|------------------|------------------|
| `github:fix` | 6 tâches | Workflow résolution d'issue GitHub |

### Fonctionnalités

- **Progression visible** : Suivi étape par étape (analyse → branche → investigation → implémentation → tests → finalisation)
- **Statuts clairs** : pending → in_progress → completed
- **Workflow structuré** : De l'analyse de l'issue à la solution testée
- **Validation qualité** : Tests et PHPStan intégrés au workflow

---

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

**🔹 Skill disponible : `github-impact`**

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
2. Analyse tous les changements :
   - Fichiers modifiés (PHP, JS/TS, templates, styles, config, assets)
   - Dépendances (composer, npm)
   - Tests associés
   - Couverture de tests
3. Catégorise par type :
   - Features
   - Fixes
   - Refactoring
   - Breaking changes
4. Génère 2 rapports :
   - **Rapport Métier** : impact fonctionnel, UX, risques identifiés
   - **Rapport Technique** : métriques, architecture, sécurité, performance
5. Ajoute rapports à la description de la PR avec marqueurs `<!-- IMPACT-REPORTS-START/END -->`
6. Sauvegarde locale dans `.analysis-reports/impact_pr_<number>.md`

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

`.claude/settings.json` :
```json
{
  "github": {
    "auto_create_pr": true,
    "auto_add_impact": true,
    "default_labels": ["bug", "automated-fix"]
  }
}
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

## Skills Disponibles

### `github-impact`

**Localisation :** `skills/github-impact/`

Skill spécialisé pour l'analyse d'impact des PR. Utilisé automatiquement par `/github:impact`.

**Fonctionnalités :**
- Analyse complète des modifications (fichiers, dépendances, tests)
- Détection automatique des templates (Twig, Blade, Vue, etc.)
- Analyse des styles (CSS, SCSS, SASS, LESS)
- Détection des assets (images, fonts)
- Analyse de sécurité
- Génération rapports métier + technique
- Intégration automatique dans description PR

**Modèle :** opus-4

**Outils :** Bash, Read, Write, Grep, Glob

## Licence

MIT
