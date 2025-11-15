---
name: framework:make:urls
description: Génère classe Urls + Message CQRS + Handler
license: MIT
version: 1.0.0
---

# Framework Make Urls Skill

## Description
Génère une classe Urls pour la génération d'URLs d'une entité, avec le pattern CQRS (Message + MessageHandler).

La classe Urls encapsule la logique de génération d'URLs pour une entité, le Message représente la query CQRS, et le Handler orchestre la récupération de l'entité et la création des URLs.

## Usage
```
Use skill framework:make:urls

Vous serez invité à fournir :
- Le nom de l'entité (ex: Product, User, Order)
```

## Templates
- `Urls/UtilisateurUrls.php` - Template de classe Urls
- `MessageHandler/UtilisateurUrlsMessage.php` - Template de message CQRS
- `MessageHandler/UtilisateurUrlsMessageHandler.php` - Template de handler

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Utilisateur, Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: utilisateur, product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Requiert que l'entité existe dans `src/Entity/{EntityName}.php`
- Requiert que le repository existe dans `src/Repository/{EntityName}Repository.php`
- Requiert que l'interface repository existe dans `src/Repository/{EntityName}RepositoryInterface.php`

## Outputs
- `src/Urls/{EntityName}Urls.php`
- `src/MessageHandler/{EntityName}UrlsMessage.php`
- `src/MessageHandler/{EntityName}UrlsMessageHandler.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Vérifier que le repository existe
   - Si non : arrêter et demander de créer l'entité avec repository d'abord
4. Générer les 3 classes depuis les templates :
   - Remplacer `{EntityName}` par le nom fourni
   - Remplacer `{entityName}` par la version camelCase
5. Afficher les fichiers créés

## Patterns appliqués

### Classe Urls
- Classe `final readonly`
- Constructeur privé
- Factory statique `new()`
- Propriétés : UrlGeneratorInterface + entité
- Méthodes pour générer URLs spécifiques

### Message CQRS
- Extends AbstractQueryEvent
- Implements QueryInterface
- Classe `final`
- Constructeur privé avec factory `new()`
- Propriété publique `id`
- Méthode getter `id()`

### MessageHandler
- Classe `final readonly`
- Attribut #[AsMessageHandler]
- Constructeur avec repository + UrlGeneratorInterface
- Méthode `__invoke()` retournant Urls

## Exemple

```bash
Use skill framework:make:urls

# Saisies utilisateur :
EntityName: Product

# Résultat :
✓ src/Urls/ProductUrls.php
✓ src/MessageHandler/ProductUrlsMessage.php
✓ src/MessageHandler/ProductUrlsMessageHandler.php
```

Fichiers générés :

```php
// src/Urls/ProductUrls.php
final readonly class ProductUrls
{
    private function __construct(
        private UrlGeneratorInterface $urlGenerator,
        private Product $product,
    ) {}

    public static function new(
        UrlGeneratorInterface $urlGenerator,
        Product $product,
    ): self {
        return new self(
            urlGenerator: $urlGenerator,
            product: $product,
        );
    }
}

// src/MessageHandler/ProductUrlsMessage.php
final class ProductUrlsMessage extends AbstractQueryEvent implements QueryInterface
{
    private function __construct(
        public string $id,
    ) {}

    public static function new(string $id): self
    {
        return new self(id: $id);
    }

    public function id(): string
    {
        return $this->id;
    }
}

// src/MessageHandler/ProductUrlsMessageHandler.php
#[AsMessageHandler]
final readonly class ProductUrlsMessageHandler
{
    public function __construct(
        private ProductRepositoryInterface $productRepository,
        private UrlGeneratorInterface $urlGenerator,
    ) {}

    public function __invoke(ProductUrlsMessage $message): ProductUrls
    {
        $product = $this->productRepository->find($message->id());
        return ProductUrls::new(
            urlGenerator: $this->urlGenerator,
            product: $product,
        );
    }
}
```

## Usage dans l'entité

L'entité doit implémenter la méthode `urls()` :

```php
public function urls(): ProductUrls
{
    /** @var ProductUrls $urls */
    $urls = ProductUrlsMessage::new(
        id: $this->id->toRfc4122(),
    )->query($this->dependencyInjection()->queryBus());

    return $urls;
}
```

## Enrichissement avec URLs spécifiques

```php
final readonly class ProductUrls
{
    private function __construct(
        private UrlGeneratorInterface $urlGenerator,
        private Product $product,
    ) {}

    public static function new(
        UrlGeneratorInterface $urlGenerator,
        Product $product,
    ): self {
        return new self(
            urlGenerator: $urlGenerator,
            product: $product,
        );
    }

    public function show(): string
    {
        return $this->urlGenerator->generate(
            'product_show',
            ['id' => $this->product->id()->toRfc4122()],
            UrlGeneratorInterface::ABSOLUTE_URL
        );
    }

    public function edit(): string
    {
        return $this->urlGenerator->generate(
            'product_edit',
            ['id' => $this->product->id()->toRfc4122()],
            UrlGeneratorInterface::ABSOLUTE_URL
        );
    }

    public function delete(): string
    {
        return $this->urlGenerator->generate(
            'product_delete',
            ['id' => $this->product->id()->toRfc4122()],
            UrlGeneratorInterface::ABSOLUTE_URL
        );
    }
}
```

## Notes
- Pattern CQRS : séparation query (Message) / handler
- UrlGeneratorInterface injecté pour génération d'URLs
- Repository utilisé pour récupérer l'entité par ID
- Classe Urls peut être enrichie avec méthodes spécifiques au besoin
- Respecte le principe d'immutabilité (readonly)
