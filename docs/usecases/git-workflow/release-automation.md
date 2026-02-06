---
title: Automatiser les release notes
description: Génération automatique de notes de release HTML orientées utilisateurs finaux
category: git-workflow
plugins:
  - name: git
    skills: [/git:gen-release-notes, /git:release-report]
  - name: doc
    skills: []
complexity: 2
duration: 5
keywords: [release, notes, changelog, git, automation]
related:
  - /usecases/git-workflow/create-pr-with-qa
  - /usecases/development/full-feature-workflow
---

# Automatiser les release notes <Badge type="info" text="★★ Intermédiaire" /> <Badge type="tip" text="~5 min" />

## Contexte

Écrire des release notes manuellement après chaque déploiement est fastidieux. Parser les commits, identifier les features, bugfixes et breaking changes, puis formatter le tout en HTML/Markdown prend du temps.

## Objectif

Générer automatiquement des release notes professionnelles avec :

- ✅ Parsing automatique des commits (Conventional Commits)
- ✅ Regroupement par type (features, fixes, breaking changes)
- ✅ Format HTML orienté utilisateurs finaux
- ✅ Changelog technique pour développeurs
- ✅ Rapport d'impact pour stakeholders

## Prérequis

**Plugins :**
- [git](/plugins/git) - Release automation
- [doc](/plugins/doc) - Documentation

**Outils :**
- Git configuré
- Commits au format Conventional Commits
- Tags Git pour versions

**Configuration :**

Commits doivent suivre le format :
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types :**
- `feat`: nouvelle feature
- `fix`: bugfix
- `docs`: documentation
- `style`: formatage
- `refactor`: refactoring
- `perf`: performance
- `test`: tests
- `chore`: maintenance

## Workflow Étape par Étape

### Phase 1 : Générer release notes

**Commande :**
```bash
/git:gen-release-notes v1.2.0..v1.3.0
```

Génère les notes de release entre deux tags.

**Que se passe-t-il ?**

1. **Parse commits** - Récupère tous les commits entre les tags
2. **Analyse** - Extrait type, scope, description
3. **Regroupe** - Classe par catégorie
4. **Génère HTML** - Format orienté utilisateurs
5. **Génère Markdown** - Format pour GitHub/GitLab

**Output attendu :**
```
🚀 Génération Release Notes v1.3.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyse des commits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commits analysés : 42
Features : 8
Fixes : 12
Breaking changes : 2
Documentation : 5
Autres : 15

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Features (8)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Add user authentication with JWT
- Add product search with filters
- Add email notifications for orders
- Add dashboard analytics
- Add export to CSV feature
- Add dark mode toggle
- Add multi-language support (EN, FR)
- Add payment integration (Stripe)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐛 Bug Fixes (12)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Fix null pointer in OrderService
- Fix memory leak in cart component
- Fix CORS errors on API calls
- Fix responsive layout on mobile
- Fix pagination not working
- Fix email template rendering
- Fix timezone issues in dashboard
- Fix duplicate entries in search results
- Fix slow query performance
- Fix file upload validation
- Fix session timeout not working
- Fix broken links in footer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Breaking Changes (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- API: Change /api/users endpoint to /api/v2/users
  Migration: Update all API calls to use /api/v2/*

- Database: Remove deprecated 'status' column from orders table
  Migration: Run `php bin/console doctrine:migrations:migrate`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Documentation (5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Add API documentation with OpenAPI
- Update installation guide
- Add troubleshooting section
- Document authentication flow
- Add contributing guidelines

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files changed : 156
Insertions : +3,421
Deletions : -1,234
Contributors : 7

Top contributors :
1. John Doe (24 commits)
2. Jane Smith (12 commits)
3. Bob Johnson (6 commits)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fichiers générés
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ RELEASE_NOTES_v1.3.0.html (format utilisateurs)
✅ CHANGELOG_v1.3.0.md (format GitHub)
✅ RELEASE_REPORT_v1.3.0.html (rapport technique)
```

### Phase 2 : Format HTML orienté utilisateurs

**Fichier généré : `RELEASE_NOTES_v1.3.0.html`**

```html
<!DOCTYPE html>
<html>
<head>
  <title>Release Notes v1.3.0</title>
  <style>
    body { font-family: -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; }
    h1 { color: #2c3e50; }
    h2 { color: #3498db; margin-top: 40px; }
    .feature { background: #e8f5e9; padding: 10px; margin: 10px 0; border-radius: 5px; }
    .fix { background: #fff3e0; padding: 10px; margin: 10px 0; border-radius: 5px; }
    .breaking { background: #ffebee; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #f44336; }
    .tag { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin-left: 10px; }
    .tag-new { background: #4caf50; color: white; }
    .tag-improved { background: #2196f3; color: white; }
    .tag-fixed { background: #ff9800; color: white; }
  </style>
</head>
<body>
  <h1>🚀 What's New in v1.3.0</h1>
  <p><em>Released on February 1, 2026</em></p>

  <h2>✨ New Features</h2>

  <div class="feature">
    <strong>User Authentication</strong> <span class="tag tag-new">NEW</span>
    <p>You can now create an account and login securely with JWT authentication. Your session stays active for 7 days.</p>
  </div>

  <div class="feature">
    <strong>Advanced Product Search</strong> <span class="tag tag-new">NEW</span>
    <p>Find products faster with our new search filters: price range, category, brand, and availability.</p>
  </div>

  <div class="feature">
    <strong>Email Notifications</strong> <span class="tag tag-new">NEW</span>
    <p>Receive email updates when your order status changes. Stay informed at every step!</p>
  </div>

  <div class="feature">
    <strong>Dashboard Analytics</strong> <span class="tag tag-new">NEW</span>
    <p>View your order history, spending trends, and favorite products in the new analytics dashboard.</p>
  </div>

  <div class="feature">
    <strong>Dark Mode</strong> <span class="tag tag-new">NEW</span>
    <p>Toggle between light and dark themes for a comfortable viewing experience.</p>
  </div>

  <h2>🐛 Bug Fixes</h2>

  <div class="fix">
    <strong>Responsive Layout</strong> <span class="tag tag-fixed">FIXED</span>
    <p>Mobile layout now displays correctly on all screen sizes.</p>
  </div>

  <div class="fix">
    <strong>Search Performance</strong> <span class="tag tag-fixed">FIXED</span>
    <p>Search results now load 3x faster thanks to database optimizations.</p>
  </div>

  <div class="fix">
    <strong>Cart Issues</strong> <span class="tag tag-fixed">FIXED</span>
    <p>Fixed memory leak that caused cart to freeze on large orders.</p>
  </div>

  <h2>⚠️ Important Changes</h2>

  <div class="breaking">
    <strong>API Version Update</strong>
    <p>The API has been upgraded to v2. If you're using our API, please update your endpoints from <code>/api/users</code> to <code>/api/v2/users</code>.</p>
    <p><a href="/docs/migration-guide">View migration guide →</a></p>
  </div>

  <h2>🙏 Thank You</h2>
  <p>This release was made possible by 7 contributors who submitted 42 commits. Thank you for making our product better!</p>

  <hr>
  <p><small>For technical details, see the <a href="CHANGELOG_v1.3.0.md">full changelog</a>.</small></p>
</body>
</html>
```

### Phase 3 : Rapport d'impact

**Commande :**
```bash
/git:release-report v1.2.0 v1.3.0
```

Génère un rapport d'impact métier ET technique.

**Rapport généré :**
```
📊 Release Impact Report v1.2.0 → v1.3.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Business Impact
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User Experience :
✅ 8 new features improving UX
✅ 12 bug fixes enhancing stability
⚠️  2 breaking changes requiring user action

Expected Outcomes :
📈 +15% conversion (search filters)
📈 +20% retention (email notifications)
📈 +10% engagement (dashboard analytics)
📊 -30% support tickets (bug fixes)

User Communication Required :
⚠️  Email users about API changes
⚠️  Update help documentation
⚠️  Publish migration guide

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Technical Impact
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Code Changes :
- Files modified : 156
- Lines added : +3,421
- Lines removed : -1,234
- Net change : +2,187

Affected Components :
- Authentication : 24 files
- Search : 18 files
- Email : 12 files
- Dashboard : 22 files
- API : 34 files

Database Changes :
⚠️  Migration required (remove orders.status column)
⚠️  Index added on products.name (performance)

Dependencies :
✅ Updated 5 packages
⚠️  New dependency: lexik/jwt-authentication-bundle

Performance :
📈 +200% search speed (optimized queries)
📉 -15% page load time (lazy loading)
📉 -30% memory usage (fixed leaks)

Security :
✅ JWT authentication added
✅ CSRF protection enabled
✅ SQL injection vulnerabilities fixed

Testing :
✅ 42 new tests added
✅ Coverage: 78% → 85% (+7%)
✅ All tests passing

Deployment Checklist :
- [ ] Run database migrations
- [ ] Update environment variables (JWT_SECRET)
- [ ] Clear cache
- [ ] Restart workers
- [ ] Test in staging
- [ ] Monitor errors after deploy
```

## Exemple Complet

### Scénario : Release v2.0.0 (breaking changes)

**Contexte :** Mise à jour majeure avec API v2, nouveau design, optimisations.

**Commande :**
```bash
/git:gen-release-notes v1.9.0..v2.0.0
```

**Release notes générées :**

```markdown
# Release v2.0.0 - Major Update

## 🎉 Highlights

This is our biggest release ever! We've completely redesigned the user interface, rebuilt the API from scratch, and added powerful new features.

## ✨ What's New

### Complete UI Redesign
- Modern, clean interface
- Improved navigation
- Faster page loads
- Mobile-first approach

### API v2
- RESTful architecture
- Better performance
- Comprehensive documentation
- Backward compatibility layer

### New Features
- Real-time notifications
- Advanced analytics
- Team collaboration
- Role-based permissions
- Activity logs
- Webhooks

## 🐛 Bug Fixes (32)

We've fixed 32 bugs reported by our users. Thank you for your feedback!

## ⚠️ Breaking Changes

### API v1 Deprecated
The old API (v1) is now deprecated and will be removed in v3.0.0 (6 months).

**Migration Guide:**
- Update base URL: `api.example.com/v1` → `api.example.com/v2`
- Update authentication: Bearer tokens now required
- Update response format: wrapped in `{ data: ... }` object

See full [migration guide](MIGRATION_v2.md).

### Database Schema Changes
Run migrations before deploying:
```bash
php bin/console doctrine:migrations:migrate
```

## 📊 Statistics

- 6 months of development
- 248 commits
- 15 contributors
- 1,247 files changed
- +42,156 lines added
- -18,923 lines removed

## 🙏 Contributors

Thank you to all 15 contributors who made this release possible!

## 🚀 Upgrade Instructions

1. Backup your database
2. Run `git pull origin main`
3. Run `composer install`
4. Run `php bin/console doctrine:migrations:migrate`
5. Clear cache: `php bin/console cache:clear`
6. Test thoroughly in staging

For help, contact support@example.com
```

## Variantes

### Release notes pour GitHub

```bash
/git:gen-release-notes v1.2.0..v1.3.0 --format=github
```

Génère format optimisé pour GitHub Releases.

### Changelog pour CHANGELOG.md

```bash
/git:gen-release-notes --append-changelog
```

Ajoute automatiquement à `CHANGELOG.md` au format Keep a Changelog.

### Release notes automatiques sur PR merge

Configurer GitHub Action :

```yaml
# .github/workflows/gen-release-notes.yml
name: Auto Release Notes
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Generate release notes
        run: /git:gen-release-notes ${{ github.ref_name }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          body_path: RELEASE_NOTES.md
          files: |
            RELEASE_NOTES.html
            CHANGELOG.md
```

## Troubleshooting

### Commits non parsés

**Symptôme :** Commits ignorés dans release notes

**Solution :**

Commits doivent suivre Conventional Commits :
```bash
# ❌ Mauvais
git commit -m "fixed bug"

# ✅ Bon
git commit -m "fix(auth): resolve login timeout issue"
```

### Breaking changes non détectés

**Symptôme :** Breaking change pas dans section "Breaking Changes"

**Solution :**

Utiliser footer BREAKING CHANGE :
```bash
git commit -m "feat(api): upgrade to v2

BREAKING CHANGE: API v1 endpoints removed"
```

## Liens Connexes

**Use cases :**
- [Créer PR avec QA](/usecases/git-workflow/create-pr-with-qa)
- [Workflow feature complet](/usecases/development/full-feature-workflow)

**Plugins :**
- [Git](/plugins/git)
- [Doc](/plugins/doc)

**Documentation externe :**
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## Tips & Best Practices

### ✅ Bonnes pratiques

**Conventional Commits :**
```bash
feat: nouvelle feature (MINOR bump)
fix: bugfix (PATCH bump)
feat!: breaking change (MAJOR bump)

# Avec scope
feat(auth): add JWT authentication
fix(cart): resolve memory leak
docs(api): update OpenAPI spec
```

**Versioning sémantique :**
- MAJOR (v1.0.0 → v2.0.0) : breaking changes
- MINOR (v1.0.0 → v1.1.0) : nouvelles features
- PATCH (v1.0.0 → v1.0.1) : bugfixes

**Release notes orientées utilisateurs :**
- Langage simple, pas de jargon technique
- Focus sur bénéfices utilisateurs
- Screenshots/GIFs pour nouvelles features
- Migration guide pour breaking changes

## Checklist Validation

Avant la release :

- [ ] Tous les commits au format Conventional Commits
- [ ] Tag Git créé (`git tag v1.3.0`)
- [ ] Tests passent
- [ ] Documentation à jour

Génération :

- [ ] Release notes générées
- [ ] Changelog mis à jour
- [ ] Rapport d'impact créé
- [ ] Migration guide écrit (si breaking changes)

Publication :

- [ ] Release notes publiées sur GitHub
- [ ] Email envoyé aux utilisateurs
- [ ] Blog post publié
- [ ] Documentation déployée
- [ ] Social media updates
