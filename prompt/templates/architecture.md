# Architecture : {COMPONENT_NAME}

**Projet** : {PROJECT_NAME}
**Composant** : {COMPONENT_NAME}
**Date** : {DATE}
**Auteur** : {AUTHOR}

## Objectif

Mettre en place une architecture pour {COMPONENT_NAME}.

### Besoin

[Décrire le besoin architectural en 2-3 phrases]

### Scope

**Inclus** :
- [Composants à créer]
- [Infrastructure nécessaire]

**Exclus** :
- [Ce qui n'est pas dans le scope]

## Architecture

### Pattern Principal

[Decorator / Cache / Strategy / Factory / etc.]

### Diagramme

```
[Diagramme ASCII de l'architecture]
```

### Composants

```
Infrastructure/
├── {COMPONENT_NAME}/
│   ├── Interface/
│   ├── Implementation/
│   └── Decorator/ (si applicable)
```

## Plan d'Implémentation

### Phase 1 : Interface et Contrat

#### 1.1 Définir Interface

**Fichier** : `src/Infrastructure/{COMPONENT_NAME}/{COMPONENT_NAME}Interface.php`

```php
namespace {NAMESPACE}\Infrastructure\{COMPONENT_NAME};

interface {COMPONENT_NAME}Interface
{
    // Méthodes du contrat
}
```

### Phase 2 : Implémentation Concrète

#### 2.1 Implémentation de Base

**Fichier** : `src/Infrastructure/{COMPONENT_NAME}/{COMPONENT_NAME}.php`

```php
namespace {NAMESPACE}\Infrastructure\{COMPONENT_NAME};

final readonly class {COMPONENT_NAME} implements {COMPONENT_NAME}Interface
{
    // Implémentation
}
```

### Phase 3 : Décorateurs (si applicable)

#### 3.1 Cache Decorator

**Fichier** : `src/Infrastructure/{COMPONENT_NAME}/Decorator/Cached{COMPONENT_NAME}.php`

```php
namespace {NAMESPACE}\Infrastructure\{COMPONENT_NAME}\Decorator;

use Symfony\Contracts\Cache\CacheInterface;

final readonly class Cached{COMPONENT_NAME} implements {COMPONENT_NAME}Interface
{
    public function __construct(
        private {COMPONENT_NAME}Interface $decorated,
        private CacheInterface $cache,
    ) {
    }

    // Méthodes avec cache
}
```

### Phase 4 : Configuration

#### 4.1 Services

**Fichier** : `config/services.yaml`

```yaml
services:
    {NAMESPACE}\Infrastructure\{COMPONENT_NAME}\{COMPONENT_NAME}Interface:
        alias: {NAMESPACE}\Infrastructure\{COMPONENT_NAME}\{COMPONENT_NAME}

    # Si decorator
    {NAMESPACE}\Infrastructure\{COMPONENT_NAME}\Decorator\Cached{COMPONENT_NAME}:
        decorates: {NAMESPACE}\Infrastructure\{COMPONENT_NAME}\{COMPONENT_NAME}Interface
        arguments:
            $decorated: '@.inner'
            $cache: '@cache.app'
```

### Phase 5 : Tests

#### 5.1 Tests Unitaires

**Fichier** : `tests/Infrastructure/{COMPONENT_NAME}/{COMPONENT_NAME}Test.php`

#### 5.2 Tests Décorateur

**Fichier** : `tests/Infrastructure/{COMPONENT_NAME}/Decorator/Cached{COMPONENT_NAME}Test.php`

## Vérification

### Tests Automatisés

```bash
make phpstan
make test
```

### Checklist Qualité

- [ ] Interface définie clairement
- [ ] Implémentation concrete en final readonly
- [ ] Décorateur implémente même interface
- [ ] Configuration services.yaml correcte
- [ ] Tests unitaires ≥ 80% coverage
- [ ] PHPStan niveau 9 : 0 erreur
- [ ] Documentation inline (docblocks)

## Points d'Attention

### Standards Qualité

- **Decorator Pattern** : Respecter l'interface, déléguer au decorated
- **Cache** : TTL approprié, invalidation sur mutation
- **Immutabilité** : final readonly pour tous les services

### Risques Identifiés

| Risque | Mitigation |
|--------|-----------|
| Cache stale | TTL court + invalidation explicite |
| Décorateurs imbriqués | Limiter à 2-3 niveaux max |
| Interface trop large | Appliquer ISP (Interface Segregation) |

## Fichiers Créés

- `src/Infrastructure/{COMPONENT_NAME}/{COMPONENT_NAME}Interface.php`
- `src/Infrastructure/{COMPONENT_NAME}/{COMPONENT_NAME}.php`
- `src/Infrastructure/{COMPONENT_NAME}/Decorator/Cached{COMPONENT_NAME}.php` (si applicable)
- `tests/Infrastructure/{COMPONENT_NAME}/{COMPONENT_NAME}Test.php`

## Fichiers Modifiés

- `config/services.yaml`
