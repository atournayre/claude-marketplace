# Catalogue des Templates

## Starters

Templates légers (10-15 lignes) pour démarrer un développement avec le mode plan.

### feature.md
- **Usage** : Nouvelle fonctionnalité métier
- **Variables** : `{ENTITY_NAME}`, `{BOUNDED_CONTEXT}`, `{TASK_DESCRIPTION}`
- **Checklist associée** : php.md

### refactor.md
- **Usage** : Refactoring de code existant
- **Variables** : `{TARGET_FILES}`, `{REFACTOR_TYPE}`, `{TASK_DESCRIPTION}`
- **Checklist associée** : php.md

### api.md
- **Usage** : API ou intégration externe
- **Variables** : `{SERVICE_NAME}`, `{INTEGRATION_TYPE}`, `{TASK_DESCRIPTION}`
- **Checklist associée** : api.md

### fix.md
- **Usage** : Correction de bug
- **Variables** : `{BUG_SYMPTOM}`, `{SUSPECT_FILES}`
- **Checklist associée** : php.md

## Checklists

Listes de vérification pour validation avant exécution.

### php.md
Points vérifiés :
- PHPStan niveau 9
- PSR-12
- Elegant Objects (final readonly, factory statique, immutabilité)
- Tests unitaires

### api.md
Points vérifiés :
- Validation des entrées
- Authentification/Sécurité
- Robustesse (timeout, retry, circuit breaker)
- Logging & Monitoring

### security.md
Points vérifiés :
- Injections (SQL, XSS, commandes)
- Authentification/Autorisation
- Données sensibles
- Headers de sécurité

## Variables automatiques

Détectées depuis le projet :
- `{PROJECT_NAME}` - depuis composer.json
- `{NAMESPACE}` - depuis composer.json
- `{AUTHOR}` - depuis git config
- `{DATE}` - date actuelle

## Usage

```bash
# Démarrer avec un starter
/prompt:start feature "Ma feature" --entity=MonEntite

# Valider avant exécution
/prompt:validate --checklist=php
```
