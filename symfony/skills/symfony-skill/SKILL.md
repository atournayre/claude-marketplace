---
name: symfony-framework
description: Comprehensive Symfony 6.4 development skill for creating web applications, APIs, and microservices. Provides workflows, best practices, and tools for efficient Symfony development including controllers, routing, database operations with Doctrine, forms, security, testing, and deployment.
license: MIT
version: 1.0.0
---

# Symfony Framework Development Skill

This skill provides comprehensive guidance for developing applications with Symfony 6.4, the leading PHP framework for web applications and APIs.

## Quick Start Workflow

### 1. Project Initialization

For a new Symfony project:
```bash
# Full web application
symfony new project_name --version="6.4.*" --webapp

# API/Microservice
symfony new project_name --version="6.4.*"

# If Symfony CLI not available, use Composer
composer create-project symfony/skeleton:"6.4.*" project_name
```

### 2. Development Server
```bash
symfony server:start
# Access at http://localhost:8000
```

## Core Development Patterns

### Controller Creation

Always extend `AbstractController` and use attributes for routing:

```php
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

class ProductController extends AbstractController
{
    #[Route('/products', name: 'product_list')]
    public function list(): Response
    {
        return $this->render('product/list.html.twig', [
            'products' => $products,
        ]);
    }
    
    #[Route('/products/{id}', name: 'product_show')]
    public function show(Product $product): Response
    {
        // Automatic entity parameter conversion
        return $this->render('product/show.html.twig', [
            'product' => $product,
        ]);
    }
}
```

### Service Configuration

Use autowiring by default in `config/services.yaml`:

```yaml
services:
    _defaults:
        autowire: true
        autoconfigure: true
        public: false
    
    App\:
        resource: '../src/'
        exclude:
            - '../src/DependencyInjection/'
            - '../src/Entity/'
            - '../src/Kernel.php'
```

### Database Operations with Doctrine

#### Entity Creation
```bash
php bin/console make:entity Product
```

#### Migration Workflow
```bash
# Generate migration
php bin/console make:migration

# Execute migration
php bin/console doctrine:migrations:migrate
```

#### Repository Pattern
```php
// In controller
public function index(ProductRepository $repository): Response
{
    $products = $repository->findBy(['active' => true]);
    // Custom repository methods
    $featured = $repository->findFeaturedProducts();
}
```

### Form Handling

Build forms in dedicated classes:

```php
namespace App\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class ProductType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('name')
            ->add('price')
            ->add('description')
        ;
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => Product::class,
        ]);
    }
}
```

Controller handling:
```php
#[Route('/product/new', name: 'product_new')]
public function new(Request $request, EntityManagerInterface $em): Response
{
    $product = new Product();
    $form = $this->createForm(ProductType::class, $product);
    $form->handleRequest($request);

    if ($form->isSubmitted() && $form->isValid()) {
        $em->persist($product);
        $em->flush();
        
        return $this->redirectToRoute('product_show', ['id' => $product->getId()]);
    }

    return $this->render('product/new.html.twig', [
        'form' => $form,
    ]);
}
```

### Security Implementation

#### User Authentication
```yaml
# config/packages/security.yaml
security:
    password_hashers:
        App\Entity\User:
            algorithm: auto
    
    providers:
        app_user_provider:
            entity:
                class: App\Entity\User
                property: email
    
    firewalls:
        main:
            form_login:
                login_path: app_login
                check_path: app_login
            logout:
                path: app_logout
```

#### Authorization with Voters
```php
namespace App\Security\Voter;

use Symfony\Component\Security\Core\Authorization\Voter\Voter;

class ProductVoter extends Voter
{
    public const EDIT = 'PRODUCT_EDIT';
    public const VIEW = 'PRODUCT_VIEW';

    protected function supports(string $attribute, mixed $subject): bool
    {
        return in_array($attribute, [self::EDIT, self::VIEW])
            && $subject instanceof Product;
    }

    protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool
    {
        $user = $token->getUser();
        
        return match($attribute) {
            self::VIEW => true,
            self::EDIT => $user && $subject->getOwner() === $user,
            default => false,
        };
    }
}
```

### API Development

#### JSON Responses
```php
#[Route('/api/products', name: 'api_products')]
public function apiList(ProductRepository $repository): JsonResponse
{
    $products = $repository->findAll();
    
    return $this->json($products, 200, [], [
        'groups' => ['product:read']
    ]);
}
```

#### Request Validation
```php
#[Route('/api/product', methods: ['POST'])]
public function create(
    #[MapRequestPayload] ProductDto $dto,
    ValidatorInterface $validator
): JsonResponse {
    $errors = $validator->validate($dto);
    
    if (count($errors) > 0) {
        return $this->json($errors, 400);
    }
    
    // Process valid data
}
```

## Essential Commands

### Development
```bash
# Clear cache
php bin/console cache:clear

# Show routes
php bin/console debug:router

# Show services
php bin/console debug:container

# Show configuration
php bin/console debug:config framework

# Create controller
php bin/console make:controller

# Create CRUD
php bin/console make:crud Product
```

### Database
```bash
# Create database
php bin/console doctrine:database:create

# Update schema (dev only)
php bin/console doctrine:schema:update --force

# Load fixtures
php bin/console doctrine:fixtures:load
```

### Testing
```bash
# Run all tests
php bin/phpunit

# Specific test file
php bin/phpunit tests/Controller/ProductControllerTest.php

# With coverage
php bin/phpunit --coverage-html coverage/
```

## Directory Structure

```
project/
├── assets/           # Frontend assets (JS, CSS)
├── bin/              # Executables (console, phpunit)
├── config/           # Configuration files
│   ├── packages/     # Package-specific config
│   ├── routes/       # Routing configuration
│   └── services.yaml # Service definitions
├── migrations/       # Database migrations
├── public/           # Web root
│   └── index.php     # Front controller
├── src/              # Application code
│   ├── Controller/   # Controllers
│   ├── Entity/       # Doctrine entities
│   ├── Form/         # Form types
│   ├── Repository/   # Doctrine repositories
│   └── Service/      # Business logic
├── templates/        # Twig templates
├── tests/            # Test suites
├── translations/     # Translation files
├── var/              # Generated files (cache, logs)
└── vendor/           # Dependencies
```

## Performance Optimization

### Caching Strategy
```yaml
# config/packages/cache.yaml
framework:
    cache:
        pools:
            cache.product:
                adapter: cache.adapter.redis
                default_lifetime: 3600
```

Usage:
```php
public function __construct(private CacheInterface $productCache) {}

public function getProduct(int $id): ?Product
{
    return $this->productCache->get(
        'product_' . $id,
        function (ItemInterface $item) use ($id) {
            $item->expiresAfter(3600);
            return $this->repository->find($id);
        }
    );
}
```

### Query Optimization
```php
// Eager loading with Doctrine
$products = $repository->createQueryBuilder('p')
    ->leftJoin('p.category', 'c')
    ->addSelect('c')
    ->leftJoin('p.tags', 't')
    ->addSelect('t')
    ->getQuery()
    ->getResult();
```

## Error Handling

```php
// In controller
if (!$product) {
    throw $this->createNotFoundException('Product not found');
}

// Custom exception
throw new BadRequestHttpException('Invalid product data');

// API error response
return $this->json([
    'error' => 'Invalid request',
    'details' => $errors
], Response::HTTP_BAD_REQUEST);
```

## Deployment Checklist

1. **Environment setup**
   ```bash
   APP_ENV=prod
   APP_DEBUG=0
   ```

2. **Optimize autoloader**
   ```bash
   composer install --no-dev --optimize-autoloader
   ```

3. **Clear and warm cache**
   ```bash
   php bin/console cache:clear --env=prod
   php bin/console cache:warmup --env=prod
   ```

4. **Compile assets**
   ```bash
   npm run build
   ```

5. **Run migrations**
   ```bash
   php bin/console doctrine:migrations:migrate --env=prod
   ```

## Testing Patterns

### Functional Tests
```php
use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class ProductControllerTest extends WebTestCase
{
    public function testListProducts(): void
    {
        $client = static::createClient();
        $client->request('GET', '/products');
        
        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Products');
    }
    
    public function testCreateProduct(): void
    {
        $client = static::createClient();
        $client->request('POST', '/api/products', [], [], [
            'CONTENT_TYPE' => 'application/json'
        ], json_encode(['name' => 'Test Product']));
        
        $this->assertResponseStatusCodeSame(201);
    }
}
```

## Common Patterns to Follow

1. **Always use dependency injection** - Never instantiate services manually
2. **Prefer composition over inheritance** - Use services and traits
3. **Keep controllers thin** - Move business logic to services
4. **Use DTOs for API input/output** - Decouple API from entities
5. **Implement repository pattern** - Keep database queries in repositories
6. **Use voters for authorization** - Centralize access control logic
7. **Cache expensive operations** - Use Symfony's cache component
8. **Write tests first** - TDD approach for critical features

## Troubleshooting Guide

### Common Issues

**Issue**: Services not autowiring
```bash
php bin/console debug:container ServiceName
# Check if service is properly registered
```

**Issue**: Route not found
```bash
php bin/console debug:router | grep pattern
# Verify route registration
```

**Issue**: Database connection errors
```bash
php bin/console doctrine:database:create
# Verify database credentials in .env
```

**Issue**: Template not found
- Check template path relative to `templates/`
- Verify file extension is `.html.twig`

## When to Use Scripts

Refer to bundled scripts in `scripts/` for:
- Complex entity generation
- Database migration helpers
- Deployment automation
- Performance profiling

## Additional Resources

For detailed documentation on specific topics, load the appropriate reference file from `references/`:
- `references/doctrine-advanced.md` - Complex ORM patterns
- `references/security-detailed.md` - Advanced security configurations
- `references/api-platform.md` - API Platform integration
- `references/testing-complete.md` - Comprehensive testing strategies
- `references/performance-tuning.md` - Performance optimization techniques