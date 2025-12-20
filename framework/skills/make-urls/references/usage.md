# Usage de la classe Urls générée

## Implémentation dans l'entité

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

## Architecture CQRS

### Message (Query)

```php
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
```

### Handler

```php
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

## Notes

- Pattern CQRS : séparation query (Message) / handler
- UrlGeneratorInterface injecté pour génération d'URLs
- Repository utilisé pour récupérer l'entité par ID
- Classe Urls peut être enrichie avec méthodes spécifiques au besoin
- Respecte le principe d'immutabilité (readonly)
