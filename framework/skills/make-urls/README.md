# Framework Make Urls

Génère classe Urls + Message CQRS + Handler pour génération d'URLs.

## Vue d'ensemble
Cette skill crée un ensemble de classes respectant le pattern CQRS pour gérer la génération d'URLs d'une entité.

## Caractéristiques

### Classes générées
- **Urls** - Classe finale readonly encapsulant la génération d'URLs
- **UrlsMessage** - Query CQRS pour récupérer les URLs
- **UrlsMessageHandler** - Handler orchestrant récupération entité + génération URLs

## Utilisation

```bash
Use skill framework:make:urls
```

Vous serez invité à fournir le nom de l'entité.

## Exemple d'utilisation

```bash
EntityName: Product
```

Génère 3 fichiers :
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

## Structure créée

```
src/
├── Urls/
│   └── {EntityName}Urls.php
└── MessageHandler/
    ├── {EntityName}UrlsMessage.php
    └── {EntityName}UrlsMessageHandler.php
```

## Prérequis
- L'entité doit exister dans `src/Entity/{EntityName}.php`
- Le repository doit exister dans `src/Repository/{EntityName}Repository.php`
- L'interface repository doit exister
- Symfony Messenger configuré
- Atournayre packages installés (AbstractQueryEvent, QueryInterface)

## Usage recommandé

### Dans l'entité
```php
final class Product implements HasUrlsInterface
{
    public function urls(): ProductUrls
    {
        /** @var ProductUrls $urls */
        $urls = ProductUrlsMessage::new(
            id: $this->id->toRfc4122(),
        )->query($this->dependencyInjection()->queryBus());

        return $urls;
    }
}
```

### Ajout de méthodes d'URLs

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

    public function api(): string
    {
        return $this->urlGenerator->generate(
            'api_product_get',
            ['id' => $this->product->id()->toRfc4122()],
            UrlGeneratorInterface::ABSOLUTE_URL
        );
    }
}
```

### Utilisation dans templates Twig

```twig
{# product/show.html.twig #}
<a href="{{ product.urls.edit }}">Modifier</a>
<a href="{{ product.urls.delete }}">Supprimer</a>

{# API link #}
<code>{{ product.urls.api }}</code>
```

### Utilisation dans contrôleurs

```php
public function show(Product $product): Response
{
    return $this->render('product/show.html.twig', [
        'product' => $product,
        'editUrl' => $product->urls()->edit(),
    ]);
}
```

## Architecture CQRS

### Flow
1. Entité appelle `ProductUrlsMessage::new(id)`
2. Message envoyé au QueryBus
3. Handler intercepte le message
4. Handler récupère l'entité via repository
5. Handler crée et retourne ProductUrls
6. URLs disponibles dans l'entité

### Avantages
- Séparation des responsabilités
- Testabilité
- Injection de dépendances propre
- Pas de service locator dans l'entité

## Principes Elegant Objects appliqués
- Classes finales
- Constructeurs privés
- Factory statiques
- Immutabilité (readonly)
- Encapsulation de la logique d'URLs
- Pas de getters bruts
