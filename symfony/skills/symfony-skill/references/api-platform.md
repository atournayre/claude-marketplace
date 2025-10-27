# API Platform & RESTful API Development

## Installation & Configuration

### Installing API Platform

```bash
composer require api

# Or manually
composer require symfony/serializer-pack
composer require symfony/validator
composer require symfony/property-access
composer require symfony/property-info
composer require doctrine/annotations
composer require api-platform/core
```

### Basic Configuration

```yaml
# config/packages/api_platform.yaml
api_platform:
    title: 'My API'
    version: '1.0.0'
    description: 'API documentation'
    
    # Swagger/OpenAPI configuration
    swagger:
        versions: [3]
        api_keys:
            apiKey:
                name: Authorization
                type: header
    
    # Collection configuration
    collection:
        pagination:
            enabled: true
            items_per_page: 30
            maximum_items_per_page: 100
            client_items_per_page: true
            client_enabled: true
    
    # Format configuration
    formats:
        jsonld: ['application/ld+json']
        json: ['application/json']
        xml: ['application/xml', 'text/xml']
        csv: ['text/csv']
```

## Creating API Resources

### Basic Resource

```php
namespace App\Entity;

use ApiPlatform\Metadata\ApiResource;
use ApiPlatform\Metadata\Get;
use ApiPlatform\Metadata\GetCollection;
use ApiPlatform\Metadata\Post;
use ApiPlatform\Metadata\Put;
use ApiPlatform\Metadata\Patch;
use ApiPlatform\Metadata\Delete;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Serializer\Annotation\Groups;
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Entity]
#[ApiResource(
    description: 'Product resource',
    operations: [
        new GetCollection(
            uriTemplate: '/products',
            normalizationContext: ['groups' => ['product:list']]
        ),
        new Get(
            uriTemplate: '/products/{id}',
            normalizationContext: ['groups' => ['product:read']]
        ),
        new Post(
            uriTemplate: '/products',
            denormalizationContext: ['groups' => ['product:write']],
            security: "is_granted('ROLE_ADMIN')"
        ),
        new Put(
            uriTemplate: '/products/{id}',
            denormalizationContext: ['groups' => ['product:write']],
            security: "is_granted('ROLE_ADMIN') or object.owner == user"
        ),
        new Patch(
            uriTemplate: '/products/{id}',
            denormalizationContext: ['groups' => ['product:write']],
            security: "is_granted('ROLE_ADMIN') or object.owner == user"
        ),
        new Delete(
            uriTemplate: '/products/{id}',
            security: "is_granted('ROLE_ADMIN')"
        )
    ],
    order: ['createdAt' => 'DESC'],
    paginationEnabled: true,
    paginationItemsPerPage: 20
)]
class Product
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    #[Groups(['product:read', 'product:list'])]
    private ?int $id = null;
    
    #[ORM\Column(length: 255)]
    #[Groups(['product:read', 'product:list', 'product:write'])]
    #[Assert\NotBlank]
    #[Assert\Length(min: 3, max: 255)]
    private ?string $name = null;
    
    #[ORM\Column(type: 'text')]
    #[Groups(['product:read', 'product:write'])]
    private ?string $description = null;
    
    #[ORM\Column(type: 'decimal', precision: 10, scale: 2)]
    #[Groups(['product:read', 'product:list', 'product:write'])]
    #[Assert\NotNull]
    #[Assert\Positive]
    private ?string $price = null;
    
    #[ORM\Column]
    #[Groups(['product:read'])]
    private ?\DateTimeImmutable $createdAt = null;
    
    #[ORM\ManyToOne(targetEntity: User::class)]
    #[Groups(['product:read'])]
    public ?User $owner = null;
}
```

### Custom Operations

```php
namespace App\Controller;

use App\Entity\Product;
use App\Service\ProductService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpKernel\Attribute\AsController;

#[AsController]
class ProductPublishController extends AbstractController
{
    public function __construct(
        private ProductService $productService
    ) {}
    
    public function __invoke(Product $data): Product
    {
        $this->productService->publish($data);
        
        return $data;
    }
}

// In Product entity
#[ApiResource(
    operations: [
        // ... other operations
        new Post(
            uriTemplate: '/products/{id}/publish',
            controller: ProductPublishController::class,
            openapiContext: [
                'summary' => 'Publish a product',
                'description' => 'Changes the product status to published',
                'responses' => [
                    '200' => [
                        'description' => 'Product published',
                    ],
                ],
            ],
            read: false,
            name: 'product_publish'
        )
    ]
)]
```

## Filters & Search

### Built-in Filters

```php
use ApiPlatform\Doctrine\Orm\Filter\SearchFilter;
use ApiPlatform\Doctrine\Orm\Filter\RangeFilter;
use ApiPlatform\Doctrine\Orm\Filter\DateFilter;
use ApiPlatform\Doctrine\Orm\Filter\BooleanFilter;
use ApiPlatform\Doctrine\Orm\Filter\OrderFilter;

#[ApiResource]
#[ApiFilter(SearchFilter::class, properties: [
    'name' => 'partial',
    'description' => 'partial',
    'category.name' => 'exact',
    'sku' => 'exact'
])]
#[ApiFilter(RangeFilter::class, properties: ['price', 'stock'])]
#[ApiFilter(DateFilter::class, properties: ['createdAt'])]
#[ApiFilter(BooleanFilter::class, properties: ['active', 'featured'])]
#[ApiFilter(OrderFilter::class, properties: [
    'name' => 'ASC',
    'price' => 'DESC',
    'createdAt' => 'DESC'
])]
class Product
{
    // Entity properties
}
```

### Custom Filters

```php
namespace App\Filter;

use ApiPlatform\Doctrine\Orm\Filter\AbstractFilter;
use ApiPlatform\Doctrine\Orm\Util\QueryNameGeneratorInterface;
use ApiPlatform\Metadata\Operation;
use Doctrine\ORM\QueryBuilder;

class CustomSearchFilter extends AbstractFilter
{
    protected function filterProperty(
        string $property,
        $value,
        QueryBuilder $queryBuilder,
        QueryNameGeneratorInterface $queryNameGenerator,
        string $resourceClass,
        Operation $operation = null,
        array $context = []
    ): void {
        if ($property !== 'search') {
            return;
        }
        
        $alias = $queryBuilder->getRootAliases()[0];
        $queryBuilder
            ->andWhere(sprintf('%s.name LIKE :search OR %s.description LIKE :search', $alias, $alias))
            ->setParameter('search', '%' . $value . '%');
    }
    
    public function getDescription(string $resourceClass): array
    {
        return [
            'search' => [
                'property' => null,
                'type' => 'string',
                'required' => false,
                'description' => 'Search in name and description',
            ],
        ];
    }
}
```

## Serialization & Validation

### Serialization Groups

```php
#[ApiResource(
    normalizationContext: ['groups' => ['read']],
    denormalizationContext: ['groups' => ['write']],
    operations: [
        new GetCollection(
            normalizationContext: ['groups' => ['collection']]
        ),
        new Get(
            normalizationContext: ['groups' => ['item', 'read']]
        )
    ]
)]
class Order
{
    #[Groups(['read', 'collection', 'item'])]
    private ?int $id = null;
    
    #[Groups(['read', 'collection', 'write'])]
    private ?string $reference = null;
    
    #[Groups(['item', 'write'])]
    private ?string $customerEmail = null;
    
    #[Groups(['item'])]
    private ?array $items = [];
    
    #[Groups(['read'])]
    #[SerializedName('total_amount')]
    private ?float $totalAmount = null;
}
```

### Custom Normalizer

```php
namespace App\Serializer;

use App\Entity\Product;
use Symfony\Component\Serializer\Normalizer\ContextAwareNormalizerInterface;
use Symfony\Component\Serializer\Normalizer\ObjectNormalizer;

class ProductNormalizer implements ContextAwareNormalizerInterface
{
    public function __construct(
        private ObjectNormalizer $normalizer
    ) {}
    
    public function normalize($object, string $format = null, array $context = []): array
    {
        $data = $this->normalizer->normalize($object, $format, $context);
        
        // Add computed fields
        $data['formatted_price'] = number_format($object->getPrice(), 2, '.', ',') . ' €';
        $data['availability'] = $object->getStock() > 0 ? 'in_stock' : 'out_of_stock';
        
        // Add related data conditionally
        if (in_array('product:detailed', $context['groups'] ?? [])) {
            $data['reviews_count'] = count($object->getReviews());
            $data['average_rating'] = $this->calculateAverageRating($object);
        }
        
        return $data;
    }
    
    public function supportsNormalization($data, string $format = null, array $context = []): bool
    {
        return $data instanceof Product;
    }
    
    private function calculateAverageRating(Product $product): ?float
    {
        $reviews = $product->getReviews();
        
        if (count($reviews) === 0) {
            return null;
        }
        
        $total = array_reduce($reviews->toArray(), function ($sum, $review) {
            return $sum + $review->getRating();
        }, 0);
        
        return round($total / count($reviews), 1);
    }
}
```

### Validation

```php
use Symfony\Component\Validator\Constraints as Assert;

#[ApiResource]
class Product
{
    #[Assert\NotBlank(groups: ['create'])]
    #[Assert\Length(
        min: 3,
        max: 255,
        groups: ['create', 'update']
    )]
    private ?string $name = null;
    
    #[Assert\Positive]
    #[Assert\LessThan(10000)]
    private ?float $price = null;
    
    #[Assert\Email]
    #[Assert\NotBlank(groups: ['create'])]
    private ?string $contactEmail = null;
    
    #[Assert\Valid]
    private ?Category $category = null;
    
    #[Assert\Callback]
    public function validate(ExecutionContextInterface $context): void
    {
        if ($this->startDate && $this->endDate && $this->startDate > $this->endDate) {
            $context->buildViolation('Start date must be before end date')
                ->atPath('startDate')
                ->addViolation();
        }
    }
}
```

## Authentication & Security

### JWT Authentication

```php
// config/packages/security.yaml
security:
    firewalls:
        api:
            pattern: ^/api
            stateless: true
            jwt: ~
            
    access_control:
        - { path: ^/api/login, roles: PUBLIC_ACCESS }
        - { path: ^/api, roles: IS_AUTHENTICATED_FULLY }

// Login endpoint
namespace App\Controller;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Http\Attribute\CurrentUser;

class SecurityController extends AbstractController
{
    #[Route('/api/login', name: 'api_login', methods: ['POST'])]
    public function login(#[CurrentUser] ?User $user): JsonResponse
    {
        if (null === $user) {
            return $this->json(['message' => 'Invalid credentials'], 401);
        }
        
        $token = $this->jwtManager->create($user);
        
        return $this->json([
            'user' => $user->getUserIdentifier(),
            'token' => $token,
        ]);
    }
}
```

### Resource Security

```php
#[ApiResource(
    security: "is_granted('ROLE_USER')",
    operations: [
        new Get(
            security: "is_granted('VIEW', object)"
        ),
        new Put(
            security: "is_granted('EDIT', object)",
            securityMessage: "Only the owner can edit this resource"
        ),
        new Delete(
            security: "is_granted('ROLE_ADMIN')",
            securityPostDenormalize: "is_granted('DELETE', object)"
        )
    ]
)]
class Document
{
    // Properties
}
```

## Pagination & Performance

### Custom Pagination

```php
namespace App\Pagination;

use ApiPlatform\State\Pagination\PaginatorInterface;

class CustomPaginator implements PaginatorInterface
{
    public function __construct(
        private iterable $items,
        private float $currentPage,
        private float $itemsPerPage,
        private float $totalItems
    ) {}
    
    public function count(): int
    {
        return $this->totalItems;
    }
    
    public function getLastPage(): float
    {
        return ceil($this->totalItems / $this->itemsPerPage);
    }
    
    public function getTotalItems(): float
    {
        return $this->totalItems;
    }
    
    public function getCurrentPage(): float
    {
        return $this->currentPage;
    }
    
    public function getItemsPerPage(): float
    {
        return $this->itemsPerPage;
    }
    
    public function getIterator(): \Traversable
    {
        return new \ArrayIterator($this->items);
    }
}
```

### Data Provider with Optimization

```php
namespace App\DataProvider;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProviderInterface;
use Doctrine\ORM\EntityManagerInterface;

class ProductCollectionDataProvider implements ProviderInterface
{
    public function __construct(
        private EntityManagerInterface $entityManager
    ) {}
    
    public function provide(Operation $operation, array $uriVariables = [], array $context = []): object|array|null
    {
        $queryBuilder = $this->entityManager
            ->getRepository(Product::class)
            ->createQueryBuilder('p')
            ->leftJoin('p.category', 'c')
            ->addSelect('c')
            ->leftJoin('p.images', 'i')
            ->addSelect('i');
        
        // Apply filters
        if (isset($context['filters']['category'])) {
            $queryBuilder
                ->andWhere('c.id = :category')
                ->setParameter('category', $context['filters']['category']);
        }
        
        // Apply pagination
        $page = $context['filters']['page'] ?? 1;
        $itemsPerPage = $context['filters']['itemsPerPage'] ?? 30;
        
        $queryBuilder
            ->setFirstResult(($page - 1) * $itemsPerPage)
            ->setMaxResults($itemsPerPage);
        
        return $queryBuilder->getQuery()->getResult();
    }
}
```

## Subresources

```php
#[ApiResource]
class User
{
    #[ORM\OneToMany(targetEntity: Order::class, mappedBy: 'customer')]
    #[ApiSubresource]
    private Collection $orders;
}

// Access: GET /api/users/{id}/orders

// Custom subresource
#[ApiResource(
    uriTemplate: '/users/{id}/orders.{_format}',
    uriVariables: [
        'id' => new Link(fromClass: User::class, identifiers: ['id'])
    ],
    operations: [new GetCollection()]
)]
class Order
{
    // Properties
}
```

## GraphQL Support

```php
// Install GraphQL
// composer require webonyx/graphql-php

#[ApiResource(
    graphQlOperations: [
        new Query(),
        new QueryCollection(
            paginationType: 'page'
        ),
        new Mutation(
            name: 'create'
        ),
        new Mutation(
            name: 'update'
        ),
        new DeleteMutation(
            name: 'delete'
        )
    ]
)]
class Product
{
    // Properties
}

// Custom GraphQL resolver
#[ApiResource]
class Order
{
    #[GraphQL\Field]
    public function totalWithTax(): float
    {
        return $this->total * 1.2;
    }
    
    #[GraphQL\Query]
    public static function ordersByStatus(string $status): array
    {
        // Custom query logic
        return [];
    }
}
```

## Error Handling

### Custom Exception

```php
namespace App\Exception;

use ApiPlatform\Symfony\Validator\Exception\ValidationException;
use Symfony\Component\Validator\ConstraintViolationList;

class CustomApiException extends \Exception
{
    public function __construct(
        private string $detail,
        private int $statusCode = 400,
        private ?array $additionalData = null
    ) {
        parent::__construct($detail, $statusCode);
    }
    
    public function getStatusCode(): int
    {
        return $this->statusCode;
    }
    
    public function getDetail(): string
    {
        return $this->detail;
    }
    
    public function getAdditionalData(): ?array
    {
        return $this->additionalData;
    }
}

// Exception normalizer
class CustomExceptionNormalizer implements NormalizerInterface
{
    public function normalize($exception, string $format = null, array $context = []): array
    {
        $data = [
            'type' => 'https://tools.ietf.org/html/rfc7231#section-6.5.1',
            'title' => 'An error occurred',
            'detail' => $exception->getDetail(),
            'status' => $exception->getStatusCode(),
        ];
        
        if ($additionalData = $exception->getAdditionalData()) {
            $data['additionalData'] = $additionalData;
        }
        
        return $data;
    }
    
    public function supportsNormalization($data, string $format = null): bool
    {
        return $data instanceof CustomApiException;
    }
}
```

## Testing API

```php
namespace App\Tests\Api;

use ApiPlatform\Symfony\Bundle\Test\ApiTestCase;
use App\Entity\Product;
use Hautelook\AliceBundle\PhpUnit\RefreshDatabaseTrait;

class ProductApiTest extends ApiTestCase
{
    use RefreshDatabaseTrait;
    
    public function testGetCollection(): void
    {
        $response = static::createClient()->request('GET', '/api/products');
        
        $this->assertResponseIsSuccessful();
        $this->assertJsonContains([
            '@context' => '/api/contexts/Product',
            '@id' => '/api/products',
            '@type' => 'hydra:Collection',
        ]);
    }
    
    public function testCreateProduct(): void
    {
        $client = static::createClient();
        $client->request('POST', '/api/products', [
            'headers' => ['Content-Type' => 'application/ld+json'],
            'json' => [
                'name' => 'Test Product',
                'price' => 99.99,
                'description' => 'Test description',
            ],
        ]);
        
        $this->assertResponseStatusCodeSame(201);
        $this->assertJsonContains([
            '@type' => 'Product',
            'name' => 'Test Product',
        ]);
    }
}
```

## OpenAPI/Swagger Customization

```php
#[ApiResource(
    openapiContext: [
        'tags' => ['Products'],
        'summary' => 'Product management',
        'description' => 'Endpoints for managing products',
        'parameters' => [
            [
                'name' => 'X-API-VERSION',
                'in' => 'header',
                'required' => false,
                'schema' => [
                    'type' => 'string',
                    'default' => '1.0',
                ],
            ],
        ],
    ]
)]
class Product
{
    // Properties
}
```