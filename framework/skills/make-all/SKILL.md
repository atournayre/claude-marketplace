---
name: framework:make:all
description: Génère tous les fichiers pour une entité complète (orchestrateur)
license: MIT
version: 1.0.0
---

# Framework Make All Skill

## Description
Orchestrateur qui génère tous les fichiers nécessaires pour une entité complète en appelant séquentiellement toutes les skills du framework.

Cette skill crée une stack complète respectant les principes Elegant Objects et DDD pour une entité donnée.

## Usage
```
Use skill framework:make:all

Vous serez invité à fournir :
- Le nom de l'entité (ex: Product, User, Order)
- Les propriétés avec leurs types (optionnel)
```

## Dépendances
Cette skill orchestre l'appel de toutes les autres skills :
1. `framework:make:contracts` (si pas déjà présents)
2. `framework:make:entity`
3. `framework:make:out`
4. `framework:make:invalide`
5. `framework:make:urls`
6. `framework:make:collection`
7. `framework:make:factory`
8. `framework:make:story`

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Utilisateur, Product)
- **{properties}** - Liste des propriétés avec types (optionnel, array)

## Outputs
Tous les fichiers générés par les 8 skills :

**Contracts** (si non existants)
- `src/Contracts/OutInterface.php`
- `src/Contracts/InvalideInterface.php`
- `src/Contracts/HasUrlsInterface.php`
- `src/Contracts/OutDataInterface.php`
- `src/Contracts/InvalideDataInterface.php`
- `src/Contracts/UrlsDataInterface.php`
- `src/Contracts/Story/StoryInterface.php`
- `src/Contracts/Doctrine/DoctrineMigrationInterface.php`

**Core**
- `src/Entity/{EntityName}.php`
- `src/Repository/{EntityName}Repository.php`
- `src/Repository/{EntityName}RepositoryInterface.php`

**Patterns**
- `src/Out/{EntityName}Out.php`
- `src/Invalide/{EntityName}Invalide.php`

**Avancé**
- `src/Urls/{EntityName}Urls.php`
- `src/MessageHandler/{EntityName}UrlsMessage.php`
- `src/MessageHandler/{EntityName}UrlsMessageHandler.php`
- `src/Collection/{EntityName}Collection.php`

**Tests**
- `src/Factory/{EntityName}Factory.php`
- `src/Story/{EntityName}Story.php`
- `src/Story/AppStory.php` (updated)

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Demander les propriétés (optionnel)
3. Vérifier si `src/Contracts/` existe
   - Si non : exécuter `framework:make:contracts`
4. Exécuter séquentiellement :
   1. `framework:make:entity` (avec EntityName et properties)
   2. `framework:make:out` (avec EntityName)
   3. `framework:make:invalide` (avec EntityName)
   4. `framework:make:urls` (avec EntityName)
   5. `framework:make:collection` (avec EntityName)
   6. `framework:make:factory` (avec EntityName et properties)
   7. `framework:make:story` (avec EntityName)
5. Afficher le résumé de tous les fichiers créés
6. Afficher les prochaines étapes recommandées

## Ordre d'exécution (critique)

L'ordre d'appel des skills est important car il respecte les dépendances :

```
Phase 1 - Fondation
└── make:contracts (si besoin)

Phase 2 - Core
└── make:entity (dépend de: contracts)

Phase 3 - Patterns (parallélisables mais dépendent de entity)
├── make:out (dépend de: entity)
└── make:invalide (dépend de: entity)

Phase 4 - Avancé (dépendent de entity + repository)
├── make:urls (dépend de: entity, repository)
└── make:collection (dépend de: entity)

Phase 5 - Tests (dépendent de entity)
├── make:factory (dépend de: entity)
└── make:story (dépend de: entity, factory)
```

## Exemple

```bash
Use skill framework:make:all

# Saisies utilisateur :
EntityName: Product
Properties:
  - name: string
  - description: string
  - price: float
  - stock: int
  - isActive: bool

# Résultat :
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

📝 Prochaines étapes recommandées:
1. Créer la migration Doctrine: php bin/console make:migration
2. Exécuter la migration: php bin/console doctrine:migrations:migrate
3. Enrichir ProductInvalide avec exceptions métier
4. Enrichir ProductUrls avec méthodes d'URLs
5. Enrichir ProductOut avec propriétés exposées
6. Enrichir ProductCollection avec méthodes métier (si besoin)
7. Enrichir ProductFactory avec méthodes custom (si besoin)
8. Enrichir ProductStory avec scénarios de test
9. Lancer les tests: php bin/phpunit
```

## Validation après génération

La skill doit vérifier que tous les fichiers ont été créés correctement :

1. Vérifier existence de tous les fichiers
2. Vérifier que les imports sont corrects
3. Vérifier que les namespaces sont cohérents
4. Vérifier que AppStory a été mis à jour

## Gestion des erreurs

Si une skill échoue :
1. Afficher l'erreur clairement
2. Indiquer quelle skill a échoué
3. Proposer de corriger manuellement
4. Ne pas continuer avec les skills suivantes si une skill critique échoue

## Options avancées (futur)

Potentiellement ajouter des flags :
- `--skip-tests` : ne pas générer Factory et Story
- `--skip-urls` : ne pas générer Urls + handlers
- `--minimal` : générer uniquement Entity + Repository + Out
- `--api-only` : générer pour API (Entity + Repository + Out + Collection)

## Notes
- Cette skill est un orchestrateur, elle ne contient pas de templates
- Elle appelle séquentiellement toutes les autres skills
- L'ordre d'exécution est critique et respecte les dépendances
- Idéale pour démarrer rapidement avec une nouvelle entité
- Génère une stack complète Elegant Objects + DDD
