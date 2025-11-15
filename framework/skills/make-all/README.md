# Framework Make All

Orchestrateur générant une stack complète pour une entité.

## Vue d'ensemble
Cette skill orchestre l'appel de toutes les skills du framework pour générer une entité complète avec tous ses composants selon les principes Elegant Objects et DDD.

## Caractéristiques

### Stack complète générée
- **Contracts** - Interfaces de base (si absentes)
- **Entity** - Entité Doctrine + Repository
- **Out** - DTO immuable pour output
- **Invalide** - Exceptions métier
- **Urls** - Génération d'URLs + CQRS
- **Collection** - Collection typée
- **Factory** - Factory Foundry pour tests
- **Story** - Story Foundry pour fixtures

## Utilisation

```bash
Use skill framework:make:all
```

Vous serez invité à fournir :
1. Nom de l'entité
2. Propriétés avec types (optionnel)

## Exemple d'utilisation

```bash
EntityName: Product
Properties:
  - name: string
  - description: string
  - price: float
  - stock: int
  - isActive: bool
```

Génère 15+ fichiers en une seule commande.

## Ordre d'exécution

### Phase 1 - Fondation
```
framework:make:contracts (si besoin)
```

### Phase 2 - Core
```
framework:make:entity
```

### Phase 3 - Patterns
```
framework:make:out
framework:make:invalide
```

### Phase 4 - Avancé
```
framework:make:urls
framework:make:collection
```

### Phase 5 - Tests
```
framework:make:factory
framework:make:story
```

## Fichiers générés

### Contracts (si absents)
```
src/Contracts/
├── OutInterface.php
├── InvalideInterface.php
├── HasUrlsInterface.php
├── OutDataInterface.php
├── InvalideDataInterface.php
├── UrlsDataInterface.php
├── Story/
│   └── StoryInterface.php
└── Doctrine/
    └── DoctrineMigrationInterface.php
```

### Core
```
src/
├── Entity/
│   └── Product.php
└── Repository/
    ├── ProductRepository.php
    └── ProductRepositoryInterface.php
```

### Patterns
```
src/
├── Out/
│   └── ProductOut.php
└── Invalide/
    └── ProductInvalide.php
```

### Avancé
```
src/
├── Urls/
│   └── ProductUrls.php
├── MessageHandler/
│   ├── ProductUrlsMessage.php
│   └── ProductUrlsMessageHandler.php
└── Collection/
    └── ProductCollection.php
```

### Tests
```
src/
├── Factory/
│   └── ProductFactory.php
└── Story/
    ├── ProductStory.php
    └── AppStory.php (updated)
```

## Output exemple

```
✓ Phase 1 - Fondation
  ✓ Contracts déjà présents

✓ Phase 2 - Core
  ✓ src/Entity/Product.php
  ✓ src/Repository/ProductRepository.php
  ✓ src/Repository/ProductRepositoryInterface.php

✓ Phase 3 - Patterns
  ✓ src/Out/ProductOut.php
  ✓ src/Invalide/ProductInvalide.php

✓ Phase 4 - Avancé
  ✓ src/Urls/ProductUrls.php
  ✓ src/MessageHandler/ProductUrlsMessage.php
  ✓ src/MessageHandler/ProductUrlsMessageHandler.php
  ✓ src/Collection/ProductCollection.php

✓ Phase 5 - Tests
  ✓ src/Factory/ProductFactory.php
  ✓ src/Story/ProductStory.php
  ✓ src/Story/AppStory.php (updated)

📊 Total: 15 fichiers créés
```

## Prochaines étapes

Après génération, suivre ces étapes :

1. **Migration Doctrine**
```bash
php bin/console make:migration
php bin/console doctrine:migrations:migrate
```

2. **Enrichir les classes**
- ProductInvalide : ajouter exceptions métier
- ProductUrls : ajouter méthodes d'URLs
- ProductOut : ajouter propriétés exposées
- ProductCollection : ajouter méthodes métier (YAGNI)
- ProductFactory : ajouter méthodes custom (YAGNI)
- ProductStory : ajouter scénarios de test

3. **Tests**
```bash
php bin/phpunit
```

4. **Validation PHPStan**
```bash
vendor/bin/phpstan analyse
```

## Prérequis

- Framework `atournayre/framework` installé avec ses dépendances
- Projet Symfony avec Doctrine ORM configuré
- Zenstruck Foundry pour les tests (optionnel)

## Avantages

### Rapidité
- Une seule commande pour générer toute la stack
- Pas besoin d'appeler 8 skills manuellement
- Gain de temps considérable

### Cohérence
- Ordre d'exécution garanti
- Dépendances gérées automatiquement
- Pas de risque d'oublier un composant

### Best practices
- Principes Elegant Objects appliqués partout
- DDD respecté
- Architecture cohérente

## Cas d'usage

### Nouveau projet
```bash
# Créer première entité complète
Use skill framework:make:all
EntityName: User
```

### Ajout feature
```bash
# Ajouter nouvelle entité au projet existant
Use skill framework:make:all
EntityName: Order
```

### Prototypage rapide
```bash
# Générer rapidement plusieurs entités
Use skill framework:make:all (Product)
Use skill framework:make:all (Category)
Use skill framework:make:all (Review)
```

## Gestion d'erreurs

Si une skill échoue :
1. Affichage clair de l'erreur
2. Indication de la skill en erreur
3. Arrêt du processus
4. Fichiers déjà créés conservés

## Options futures

Possibles extensions :
- `--skip-tests` : sans Factory/Story
- `--skip-urls` : sans Urls/CQRS
- `--minimal` : Entity + Repository + Out uniquement
- `--api-only` : Stack pour API (Entity + Repository + Out + Collection)

## Principes Elegant Objects appliqués
- Toutes les classes finales
- Constructeurs privés
- Factory statiques
- Immutabilité encouragée
- Interfaces pour tous les contrats
- Tests first-class citizens
