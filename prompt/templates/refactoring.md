# Refactoring : {TARGET_FILE}

**Projet** : {PROJECT_NAME}
**Type d'optimisation** : {OPTIMIZATION_TYPE}
**Date** : {DATE}
**Auteur** : {AUTHOR}

## Objectif

Refactorer et optimiser `{TARGET_FILE}` avec le pattern {OPTIMIZATION_TYPE}.

### Problème Actuel

**Métriques** :
- Complexité cyclomatique : {CURRENT_COMPLEXITY}
- Objectif d'amélioration : {IMPROVEMENT_TARGET}%
- [Autres métriques : performance, maintenabilité, etc.]

**Symptômes** :
- [Lister les problèmes observés]
- [Code dupliqué, performance, complexité]

## Architecture

### Pattern {OPTIMIZATION_TYPE}

#### Avant Refactoring

```
[Structure actuelle du code]
```

#### Après Refactoring

```
[Nouvelle structure proposée]
```

### Composants

**Si Decorator** :
```
DecoratedService/
├── ServiceInterface.php
├── ConcreteService.php (service original)
└── Decorator/
    └── {OPTIMIZATION_TYPE}Decorator.php
```

**Si Cache** :
```
Service/
├── {SERVICE_NAME}Interface.php
├── {SERVICE_NAME}.php
└── Cached{SERVICE_NAME}.php (decorator cache)
```

## Plan d'Implémentation

### Phase 1 : Préparation

#### 1.1 Analyse de la Complexité Actuelle

```bash
# Mesurer complexité cyclomatique
vendor/bin/phpstan analyse {TARGET_FILE} --level=9

# Profiler si optimisation performance
# [Command de profiling]
```

#### 1.2 Créer Tests de Non-Régression

**Fichier** : `tests/[Path]/{TARGET_FILE}Test.php`

- Créer tests couvrant le comportement actuel
- Coverage minimum 80%
- Tests de performance (benchmarks)

### Phase 2 : Refactoring

#### 2.1 Extraire Interface (si nécessaire)

**Fichier** : `src/[Path]/{SERVICE_NAME}Interface.php`

```php
namespace {NAMESPACE}\[Path];

interface {SERVICE_NAME}Interface
{
    // Méthodes publiques du service
}
```

#### 2.2 Implémenter le Pattern

**Si Decorator** :

**Fichier** : `src/[Path]/Decorator/{OPTIMIZATION_TYPE}Decorator.php`

```php
namespace {NAMESPACE}\[Path]\Decorator;

final readonly class {OPTIMIZATION_TYPE}Decorator implements {SERVICE_NAME}Interface
{
    public function __construct(
        private {SERVICE_NAME}Interface $decorated,
    ) {
    }

    // Implémenter méthodes avec décoration
}
```

**Si Refactoring Simple** :
- Extraire méthodes complexes
- Réduire niveaux d'indentation
- Appliquer SRP (Single Responsibility Principle)

#### 2.3 Mettre à Jour Configuration

**Fichier** : `config/services.yaml`

```yaml
services:
    # Service décoré
    {NAMESPACE}\[Path]\{OPTIMIZATION_TYPE}Decorator:
        decorates: {NAMESPACE}\[Path]\{SERVICE_NAME}Interface
        arguments:
            $decorated: '@.inner'
```

### Phase 3 : Validation

#### 3.1 Tests Unitaires

- Vérifier tous les tests passent
- Comparer benchmarks avant/après
- Valider amélioration performance

#### 3.2 Benchmarks Comparatifs

```bash
# Benchmark avant
[Command de benchmark sur version actuelle]

# Benchmark après
[Command de benchmark sur version refactorée]
```

**Métriques attendues** :
- Complexité cyclomatique : {CURRENT_COMPLEXITY} → {IMPROVEMENT_TARGET}
- Performance : [Gain attendu]
- Maintenabilité : [Amélioration]

### Phase 4 : Déploiement Progressif

#### 4.1 Feature Flag (si applicable)

```php
if ($featureFlag->isEnabled('use_optimized_{SERVICE_NAME}')) {
    // Nouvelle implémentation
} else {
    // Ancienne implémentation (fallback)
}
```

#### 4.2 Monitoring

- Logger métriques clés
- Alertes si dégradation
- Rollback automatique si nécessaire

## Vérification

### Tests Automatisés

```bash
# PHPStan niveau 9
make phpstan

# Tests unitaires
make test

# Benchmarks
[Command benchmark]
```

### Checklist Qualité

- [ ] Complexité réduite de {CURRENT_COMPLEXITY} à {IMPROVEMENT_TARGET}
- [ ] Tous les tests passent
- [ ] Benchmarks montrent amélioration
- [ ] PHPStan niveau 9 : 0 erreur
- [ ] Code coverage ≥ 80%
- [ ] Pattern {OPTIMIZATION_TYPE} correctement appliqué
- [ ] Interface créée si service décoré
- [ ] Configuration services.yaml mise à jour
- [ ] Documentation mise à jour

## Points d'Attention

### Standards Qualité

- **Backward Compatibility** : Ne pas casser l'API existante
- **Tests** : Coverage avant/après identique ou meilleur
- **Performance** : Mesurer, ne pas supposer
- **Elegant Objects** : Classes final readonly, pas de setters

### Risques Identifiés

| Risque | Mitigation |
|--------|-----------|
| Régression fonctionnelle | Tests de non-régression avant refactoring |
| Dégradation performance | Benchmarks avant/après obligatoires |
| Complexité accrue | Mesurer complexité cyclomatique |
| Breaking changes | Versionner API, feature flags |

### Patterns à Éviter

- ❌ Refactoring sans tests
- ❌ Optimisation prématurée sans mesures
- ❌ Décorateurs imbriqués à l'infini
- ❌ Extraction excessive (over-engineering)

### Patterns Recommandés

- ✅ TDD : Tests avant refactoring
- ✅ Decorator pour ajout de comportement
- ✅ Strategy pour algorithmes interchangeables
- ✅ Feature flags pour déploiement progressif
- ✅ Benchmarks pour validation performance

## Métriques de Succès

### Avant Refactoring

- Complexité cyclomatique : {CURRENT_COMPLEXITY}
- Performance : [Baseline]
- Maintenabilité : [Score actuel]
- Coverage : [%]

### Après Refactoring (Objectifs)

- Complexité cyclomatique : {IMPROVEMENT_TARGET}
- Performance : [Amélioration de X%]
- Maintenabilité : [Score cible]
- Coverage : ≥ 80%

### Validation

```bash
# Comparer métriques
vendor/bin/phpmetrics --report-html=build/metrics src/

# Comparer avant/après
diff build/metrics-before/ build/metrics-after/
```

## Fichiers Créés

- `src/[Path]/{SERVICE_NAME}Interface.php` (si nécessaire)
- `src/[Path]/Decorator/{OPTIMIZATION_TYPE}Decorator.php` (si decorator)
- `tests/[Path]/{TARGET_FILE}Test.php` (si manquant)

## Fichiers Modifiés

- `{TARGET_FILE}` (refactoré)
- `config/services.yaml` (si decorator)
- Documentation technique
