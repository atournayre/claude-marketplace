# Configuration : {CONFIG_NAME}

**Projet** : {PROJECT_NAME}
**Configuration** : {CONFIG_NAME}
**Date** : {DATE}
**Auteur** : {AUTHOR}

## Objectif

Mettre en place la configuration pour {CONFIG_NAME}.

### Besoin

[Décrire le besoin de configuration en 2-3 phrases]

### Type de Configuration

- [ ] Feature Flag (activation/désactivation fonctionnalité)
- [ ] Paramètre métier (seuils, limites, durées)
- [ ] Configuration technique (URLs, credentials, timeouts)
- [ ] A/B Testing

## Architecture

### Approche

**Feature Flags** :
```
Infrastructure/
└── FeatureFlag/
    ├── FeatureFlagInterface.php
    └── SymfonyFeatureFlag.php (utilise parameters)
```

**Configuration Dynamique** :
```
config/
└── packages/
    └── {CONFIG_NAME}.yaml
```

## Plan d'Implémentation

### Phase 1 : Définir Configuration

#### 1.1 Paramètres dans config

**Fichier** : `config/packages/{CONFIG_NAME}.yaml`

```yaml
parameters:
    {CONFIG_NAME}:
        feature_enabled: '%env(bool:FEATURE_{CONFIG_NAME}_ENABLED)%'
        threshold: 100
        timeout: 30
        api_url: '%env(API_{CONFIG_NAME}_URL)%'
```

#### 1.2 Variables d'Environnement

**Fichier** : `.env`

```env
# {CONFIG_NAME} Configuration
FEATURE_{CONFIG_NAME}_ENABLED=true
API_{CONFIG_NAME}_URL=https://api.example.com
```

### Phase 2 : Feature Flag (si applicable)

#### 2.1 Interface

**Fichier** : `src/Infrastructure/FeatureFlag/FeatureFlagInterface.php`

```php
namespace {NAMESPACE}\Infrastructure\FeatureFlag;

interface FeatureFlagInterface
{
    public function isEnabled(string $featureName): bool;
}
```

#### 2.2 Implémentation

**Fichier** : `src/Infrastructure/FeatureFlag/SymfonyFeatureFlag.php`

```php
namespace {NAMESPACE}\Infrastructure\FeatureFlag;

final readonly class SymfonyFeatureFlag implements FeatureFlagInterface
{
    public function __construct(
        private array $featureFlags,
    ) {
    }

    public function isEnabled(string $featureName): bool
    {
        return $this->featureFlags[$featureName] ?? false;
    }
}
```

#### 2.3 Configuration Service

**Fichier** : `config/services.yaml`

```yaml
services:
    {NAMESPACE}\Infrastructure\FeatureFlag\FeatureFlagInterface:
        class: {NAMESPACE}\Infrastructure\FeatureFlag\SymfonyFeatureFlag
        arguments:
            $featureFlags:
                '{CONFIG_NAME}': '%{CONFIG_NAME}.feature_enabled%'
```

### Phase 3 : Utilisation dans le Code

#### 3.1 Injection dans Service

```php
namespace {NAMESPACE}\Application\Service;

final readonly class MyService
{
    public function __construct(
        private FeatureFlagInterface $featureFlag,
    ) {
    }

    public function execute(): void
    {
        if ($this->featureFlag->isEnabled('{CONFIG_NAME}')) {
            // Nouvelle implémentation
        } else {
            // Ancienne implémentation (fallback)
        }
    }
}
```

#### 3.2 Dans Twig (si applicable)

**Fichier** : `src/Infrastructure/Twig/FeatureFlagExtension.php`

```php
namespace {NAMESPACE}\Infrastructure\Twig;

use Twig\Extension\AbstractExtension;
use Twig\TwigFunction;

final class FeatureFlagExtension extends AbstractExtension
{
    public function __construct(
        private FeatureFlagInterface $featureFlag,
    ) {
    }

    public function getFunctions(): array
    {
        return [
            new TwigFunction('feature_enabled', [$this->featureFlag, 'isEnabled']),
        ];
    }
}
```

**Usage dans template** :

```twig
{% if feature_enabled('{CONFIG_NAME}') %}
    {# Nouvelle UI #}
{% else %}
    {# Ancienne UI #}
{% endif %}
```

### Phase 4 : Tests

#### 4.1 Tests Feature Flag

**Fichier** : `tests/Infrastructure/FeatureFlag/SymfonyFeatureFlagTest.php`

```php
namespace {NAMESPACE}\Tests\Infrastructure\FeatureFlag;

use PHPUnit\Framework\TestCase;

final class SymfonyFeatureFlagTest extends TestCase
{
    public function testFeatureEnabled(): void
    {
        $featureFlag = new SymfonyFeatureFlag(['{CONFIG_NAME}' => true]);

        self::assertTrue($featureFlag->isEnabled('{CONFIG_NAME}'));
    }

    public function testFeatureDisabled(): void
    {
        $featureFlag = new SymfonyFeatureFlag(['{CONFIG_NAME}' => false]);

        self::assertFalse($featureFlag->isEnabled('{CONFIG_NAME}'));
    }

    public function testUnknownFeature(): void
    {
        $featureFlag = new SymfonyFeatureFlag([]);

        self::assertFalse($featureFlag->isEnabled('unknown'));
    }
}
```

#### 4.2 Tests avec Feature Flag

Dans les tests qui dépendent de la feature :

```php
public function testWithFeatureEnabled(): void
{
    $featureFlag = new SymfonyFeatureFlag(['{CONFIG_NAME}' => true]);
    $service = new MyService($featureFlag);

    // Test comportement avec feature activée
}

public function testWithFeatureDisabled(): void
{
    $featureFlag = new SymfonyFeatureFlag(['{CONFIG_NAME}' => false]);
    $service = new MyService($featureFlag);

    // Test comportement avec feature désactivée (fallback)
}
```

## Vérification

### Tests Manuels

#### 1. Tester Feature Activée

```bash
# Dans .env.local
FEATURE_{CONFIG_NAME}_ENABLED=true

# Vérifier comportement
bin/console app:test-command
```

#### 2. Tester Feature Désactivée

```bash
# Dans .env.local
FEATURE_{CONFIG_NAME}_ENABLED=false

# Vérifier fallback
bin/console app:test-command
```

### Checklist Qualité

- [ ] Configuration dans config/packages/{CONFIG_NAME}.yaml
- [ ] Variables env dans .env
- [ ] FeatureFlag interface implémentée (si applicable)
- [ ] Service configuré dans services.yaml
- [ ] Tests feature activée/désactivée
- [ ] Documentation mise à jour
- [ ] Fallback implémenté (comportement par défaut)
- [ ] Pas de breaking changes si feature désactivée

## Points d'Attention

### Déploiement Progressif

1. **Phase 1** : Déployer code avec feature DÉSACTIVÉE
2. **Phase 2** : Activer pour 10% utilisateurs (A/B testing)
3. **Phase 3** : Activer pour 50% si OK
4. **Phase 4** : Activer pour 100%
5. **Phase 5** : Retirer feature flag (cleanup)

### Cleanup

Une fois la feature stable (après 2-3 sprints) :
- Retirer le feature flag
- Supprimer le code de fallback
- Simplifier le code

### Monitoring

- Logger quand feature flag est utilisée
- Métriques : % d'utilisateurs avec feature activée
- A/B testing : comparer KPIs entre groupes

### Risques Identifiés

| Risque | Mitigation |
|--------|-----------|
| Feature flag oubliés | Revue trimestrielle, supprimer si > 6 mois |
| Trop de feature flags | Max 10 actifs simultanément |
| Complexité code (if/else partout) | Refactorer vers Strategy pattern |
| Inconsistance env dev/prod | Valider .env.dist synchronisé |

### Best Practices

- ✅ Feature flags temporaires (max 6 mois)
- ✅ Fallback toujours présent et testé
- ✅ Naming clair : `FEATURE_XXX_ENABLED`
- ✅ Documentation : pourquoi, quand retirer
- ✅ Monitoring : qui utilise quoi

## Fichiers Créés

- `config/packages/{CONFIG_NAME}.yaml`
- `src/Infrastructure/FeatureFlag/FeatureFlagInterface.php` (si applicable)
- `src/Infrastructure/FeatureFlag/SymfonyFeatureFlag.php` (si applicable)
- `tests/Infrastructure/FeatureFlag/SymfonyFeatureFlagTest.php` (si applicable)

## Fichiers Modifiés

- `.env` (ajouter variables)
- `config/services.yaml` (si feature flag)
- Services utilisant la configuration

## Documentation

### README Section

Ajouter section dans README.md :

```markdown
## Configuration {CONFIG_NAME}

### Variables d'Environnement

- `FEATURE_{CONFIG_NAME}_ENABLED` - Active/désactive la feature (default: false)
- `API_{CONFIG_NAME}_URL` - URL de l'API (required)

### Utilisation

[Exemples d'utilisation]
```
