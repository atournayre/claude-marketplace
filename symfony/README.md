# Plugin Symfony

Plugin Symfony avec commandes make, documentation et intégrations framework.

## Installation

```bash
/plugin install symfony@atournayre
```

## Prérequis

- Projet Symfony 6.4+
- `symfony` CLI (optionnel mais recommandé)
- Maker Bundle installé

## Commandes

### `/symfony:make`

Utilise les makers Symfony pour générer du code.

**Arguments :**
```bash
/symfony:make <tâche>
```

**Makers supportés :**
- `entity` - Entité Doctrine
- `controller` - Controller
- `form` - Form Type
- `command` - Console Command
- `test` - Test unitaire/fonctionnel
- `voter` - Security Voter
- `subscriber` - Event Subscriber
- `validator` - Custom Validator
- `repository` - Repository
- `service` - Service
- Et tous les autres makers Symfony

**Exemples :**
```bash
# Créer entité
/symfony:make entity

# Créer controller
/symfony:make controller UserController

# Créer form
/symfony:make form UserType

# Créer test
/symfony:make test UserControllerTest
```

**Workflow :**
1. Vérifie si maker existe pour la tâche
2. Si existe : exécute `bin/console make:xxx`
3. Si n'existe pas : délègue à `/dev:prepare`
4. Guide interactivement si nécessaire
5. Génère code conforme PSR-12
6. Crée tests associés

**Makers personnalisés :**
Si aucun maker n'existe pour ta tâche, la commande bascule automatiquement sur `/dev:prepare` pour créer un plan d'implémentation.

---

### `/symfony:doc:load`

Charge la documentation Symfony depuis symfony.com dans des fichiers markdown locaux.

**Usage :**
```bash
/symfony:doc:load
```

**Fonctionnalités :**
- Download depuis symfony.com/doc/current
- Cache 24h
- Stockage `docs/symfony/`
- Support multi-versions
- Disponible offline

**Sauvegarde :**
```
docs/symfony/
├── README.md
├── setup/
├── components/
├── best_practices/
├── security/
├── doctrine/
├── forms/
├── routing/
└── ...
```

---

### `/symfony:doc:question`

Interroge la documentation Symfony locale pour répondre à une question.

**Arguments :**
```bash
/symfony:doc:question <question>
```

**Exemples :**
```bash
/symfony:doc:question "Comment créer un controller ?"
/symfony:doc:question "Configurer la sécurité avec JWT ?"
/symfony:doc:question "Utiliser les events Doctrine ?"
```

**Workflow :**
1. Cherche dans `docs/symfony/`
2. Grep mots-clés pertinents
3. Parse sections documentation
4. Présente réponse structurée :
   - Explication
   - Code examples
   - Configuration
   - Best practices
   - Références fichiers sources

**Prérequis :**
- Documentation chargée via `/symfony:doc:load`

## Skill Symfony

### `symfony:symfony-skill`

Skill complet pour développement Symfony 6.4.

**Capacités :**
- Controllers et routing
- Doctrine ORM/migrations
- Forms et validation
- Security et authentication
- Services et DI
- Tests (unit, functional, integration)
- API REST
- Events et subscribers
- Commands console
- Deployment

**Utilisation automatique :**
Le skill est chargé automatiquement dans les contextes Symfony.

## Workflow Recommandé

### Créer Feature Complète

```bash
# 1. Générer entité
/symfony:make entity User

# 2. Générer migration
bin/console make:migration

# 3. Générer controller
/symfony:make controller UserController

# 4. Générer form
/symfony:make form UserType

# 5. Générer tests
/symfony:make test UserControllerTest

# 6. Documentation
/doc:update
```

### Apprendre Symfony

```bash
# 1. Charger docs
/symfony:doc:load

# 2. Poser questions
/symfony:doc:question "Comment créer un service ?"

# 3. Implémenter avec guidance
/symfony:make service EmailService
```

### Debug Symfony

```bash
# Erreur Symfony
/dev:debug:error var/log/dev.log

# Questions structure
/dev:question "Comment fonctionne le routing ?"
```

## Configuration

`.claude/plugins.settings.json` :
```json
{
  "atournayre-claude-plugin-marketplace": {
    "symfony": {
      "default_version": "6.4",
      "maker": {
        "auto_install": false
      }
    }
  }
}
```

### Options

- `default_version` (string) : Version Symfony par défaut (défaut: `"6.4"`)
- `maker.auto_install` (bool) : Installer Maker Bundle auto (défaut: `false`)

### Utilisation avec Config

```bash
# Avec default_version: "7.0" configuré
/symfony:doc:load                  # Charge docs Symfony 7.0

# Avec maker.auto_install: true configuré
/symfony:make entity               # Installe Maker si absent
```

## Intégrations

**Doctrine :**
- Entités avec annotations
- Repositories custom
- Migrations automatiques
- Relations (OneToMany, ManyToOne, etc.)

**Security :**
- Voters
- Authenticators
- Password hashers
- Access control

**Forms :**
- Form Types
- Data Transformers
- Validators custom
- Themes

**API Platform :**
- Resources API
- Serialization groups
- Filters
- Custom operations

## Best Practices

**Makers :**
- Toujours via `/symfony:make`
- Génération interactive
- Tests automatiques

**Documentation :**
- Charger docs en local
- Questions offline
- Mise à jour régulière

**Structure :**
- PSR-12
- Symfony conventions
- Doctrine best practices
- Security hardening

## Extensions

Compatible avec :
- API Platform plugin
- Doctrine plugin
- PHPUnit plugin
- Maker Bundle

## Licence

MIT
