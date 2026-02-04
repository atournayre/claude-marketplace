# Checklist PHP

## Code Quality
- [ ] PHPStan niveau 9 : 0 erreur
- [ ] PSR-12 respecté (formatage)
- [ ] Pas de code mort / commenté

## Elegant Objects
- [ ] Classes `final readonly` (sauf héritage nécessaire)
- [ ] Constructeur privé + factory statique `::create()` ou `::from*()`
- [ ] Pas de setters (immutabilité)
- [ ] Pas de getters triviaux (exposer comportement, pas données)
- [ ] Max 4 propriétés par classe
- [ ] Pas de `null` en retour (Option/Result pattern)

## Typage
- [ ] Types stricts sur toutes les méthodes
- [ ] Return types explicites
- [ ] Pas de `mixed` sauf cas justifié
- [ ] Collections typées (pas de `array`)

## Tests
- [ ] Tests unitaires présents
- [ ] Pattern AAA (Arrange-Act-Assert)
- [ ] Factories Foundry utilisées
- [ ] Cas nominaux + edge cases couverts

## Conventions
- [ ] Nommage : PascalCase classes, camelCase méthodes
- [ ] Conditions Yoda : `null === $value`
- [ ] Early return (fail fast)
- [ ] Messages d'erreur avec contexte

## Commandes de vérification
```bash
./vendor/bin/phpstan analyse
./vendor/bin/php-cs-fixer fix --dry-run
./vendor/bin/phpunit
```
