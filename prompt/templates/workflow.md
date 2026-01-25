# Workflow : {WORKFLOW_NAME}

**Projet** : {PROJECT_NAME}
**Workflow** : {WORKFLOW_NAME}
**Date** : {DATE}
**Auteur** : {AUTHOR}

## Objectif

Créer un workflow GitHub Actions pour {WORKFLOW_NAME}.

### Besoin

[Décrire le besoin d'automation en 2-3 phrases]

### Déclencheurs

- [ ] Push sur branches (main, develop, feature/*)
- [ ] Pull Request
- [ ] Schedule (cron)
- [ ] Workflow dispatch (manuel)
- [ ] Release published

## Architecture

### Jobs

```
workflow {WORKFLOW_NAME}:
├── job: setup
├── job: quality (phpstan, cs-fixer)
├── job: tests (phpunit)
└── job: deploy (si applicable)
```

### Matrice de Tests (si applicable)

- PHP 8.2, 8.3
- Symfony 6.4, 7.0
- MySQL 8.0, PostgreSQL 15

## Plan d'Implémentation

### Phase 1 : Workflow de Base

#### 1.1 Créer Workflow File

**Fichier** : `.github/workflows/{WORKFLOW_NAME}.yml`

```yaml
name: {WORKFLOW_NAME}

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          extensions: mbstring, xml, ctype, iconv, intl, pdo_mysql
          coverage: xdebug

      - name: Cache Composer
        uses: actions/cache@v3
        with:
          path: vendor
          key: composer-${{ hashFiles('composer.lock') }}

      - name: Install dependencies
        run: composer install --no-interaction --prefer-dist

  quality:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'

      - name: Restore Composer cache
        uses: actions/cache@v3
        with:
          path: vendor
          key: composer-${{ hashFiles('composer.lock') }}

      - name: PHPStan
        run: vendor/bin/phpstan analyse --level=9

      - name: PHP CS Fixer
        run: vendor/bin/php-cs-fixer fix --dry-run --diff

  tests:
    needs: quality
    runs-on: ubuntu-latest
    strategy:
      matrix:
        php: ['8.2', '8.3']
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          coverage: xdebug

      - name: Restore Composer cache
        uses: actions/cache@v3
        with:
          path: vendor
          key: composer-${{ matrix.php }}-${{ hashFiles('composer.lock') }}

      - name: Install dependencies
        run: composer install --no-interaction

      - name: Run tests
        run: vendor/bin/phpunit --coverage-clover coverage.xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

### Phase 2 : Secrets et Variables

#### 2.1 Configurer Secrets GitHub

Dans GitHub → Settings → Secrets and variables → Actions :

```
CODECOV_TOKEN=xxx
DEPLOY_SSH_KEY=xxx (si déploiement)
```

#### 2.2 Variables d'Environnement

```yaml
env:
  APP_ENV: test
  DATABASE_URL: mysql://root:root@127.0.0.1:3306/test_db
```

### Phase 3 : Job de Déploiement (si applicable)

#### 3.1 Déploiement Automatique

```yaml
  deploy:
    needs: tests
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        env:
          SSH_PRIVATE_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
        run: |
          # Script de déploiement
          ssh user@server 'cd /path/to/app && git pull && composer install --no-dev'
```

### Phase 4 : Notifications

#### 4.1 Notifications Slack (optionnel)

```yaml
  notify:
    needs: [tests, deploy]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Vérification

### Tests Locaux

```bash
# Simuler l'environnement CI localement
act -j quality
act -j tests
```

### Checklist Qualité

- [ ] Workflow déclenché sur push/PR
- [ ] Cache Composer configuré
- [ ] PHPStan niveau 9 passe
- [ ] Tests unitaires passent
- [ ] Coverage uploadé sur Codecov
- [ ] Matrice de tests (PHP 8.2, 8.3)
- [ ] Secrets configurés dans GitHub
- [ ] Déploiement uniquement sur main
- [ ] Notifications configurées (si nécessaire)

### Tests Manuels

1. Créer une PR de test
2. Vérifier que le workflow se déclenche
3. Vérifier tous les jobs passent
4. Merger et vérifier déploiement (si applicable)

## Points d'Attention

### Performance

- **Cache** : Toujours cacher vendor, node_modules
- **Parallélisation** : Jobs indépendants en parallèle
- **Matrice** : Ne pas tester trop de combinaisons (coût)

### Sécurité

- **Secrets** : JAMAIS dans le code, toujours via GitHub Secrets
- **Pull Requests** : Ne pas déployer depuis fork (risque d'exposition secrets)
- **Permissions** : Minimal nécessaire (GITHUB_TOKEN)

### Risques Identifiés

| Risque | Mitigation |
|--------|-----------|
| Workflow trop long | Cache, parallélisation |
| Secrets exposés | Pull request secrets protection |
| Déploiement raté | Rollback automatique + notifications |
| Tests flaky | Retry automatique (max 3) |

### Best Practices

- ✅ Fail fast : PHPStan avant tests
- ✅ Cache dependencies
- ✅ Matrice pour compatibilité multi-versions
- ✅ Déploiement uniquement si tests passent
- ✅ Notifications en cas d'échec

## Fichiers Créés

- `.github/workflows/{WORKFLOW_NAME}.yml`

## Fichiers Modifiés

- Aucun (sauf si scripts de déploiement)

## Monitoring

### GitHub Actions Dashboard

- Temps d'exécution par job
- Taux de succès/échec
- Cache hit rate

### Alertes

- Slack si workflow échoue sur main
- Email si déploiement échoue
