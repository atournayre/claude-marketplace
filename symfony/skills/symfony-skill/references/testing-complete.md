# Symfony Testing Complete Guide

## Test Environment Setup

### Configuration

```yaml
# config/packages/test/framework.yaml
framework:
    test: true
    session:
        storage_factory_id: session.storage.factory.mock_file

# config/packages/test/doctrine.yaml
doctrine:
    dbal:
        url: '%env(resolve:DATABASE_URL_TEST)%'
```

### Test Database Setup

```bash
# Create test database
php bin/console doctrine:database:create --env=test

# Run migrations
php bin/console doctrine:migrations:migrate --env=test --no-interaction

# Load fixtures
php bin/console doctrine:fixtures:load --env=test --no-interaction
```

## Unit Testing

### Testing Services

```php
namespace App\Tests\Service;

use App\Service\PriceCalculator;
use PHPUnit\Framework\TestCase;

class PriceCalculatorTest extends TestCase
{
    private PriceCalculator $calculator;
    
    protected function setUp(): void
    {
        $this->calculator = new PriceCalculator();
    }
    
    public function testCalculatePrice(): void
    {
        $result = $this->calculator->calculate(100, 0.2, 10);
        
        $this->assertEquals(110, $result);
    }
    
    /**
     * @dataProvider priceProvider
     */
    public function testCalculatePriceWithDataProvider(
        float $basePrice,
        float $tax,
        float $discount,
        float $expected
    ): void {
        $result = $this->calculator->calculate($basePrice, $tax, $discount);
        
        $this->assertEquals($expected, $result);
    }
    
    public function priceProvider(): array
    {
        return [
            'with tax and discount' => [100, 0.2, 10, 110],
            'no tax' => [100, 0, 10, 90],
            'no discount' => [100, 0.2, 0, 120],
            'zero price' => [0, 0.2, 10, 0],
        ];
    }
    
    public function testCalculatePriceThrowsExceptionForNegativePrice(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Price cannot be negative');
        
        $this->calculator->calculate(-10, 0.2, 0);
    }
}
```

### Testing Entities

```php
namespace App\Tests\Entity;

use App\Entity\Product;
use App\Entity\Category;
use PHPUnit\Framework\TestCase;

class ProductTest extends TestCase
{
    public function testGettersAndSetters(): void
    {
        $product = new Product();
        
        $product->setName('Test Product');
        $this->assertEquals('Test Product', $product->getName());
        
        $product->setPrice(99.99);
        $this->assertEquals(99.99, $product->getPrice());
        
        $category = new Category();
        $category->setName('Electronics');
        
        $product->setCategory($category);
        $this->assertSame($category, $product->getCategory());
    }
    
    public function testProductValidation(): void
    {
        $product = new Product();
        
        // Test required fields
        $this->assertNull($product->getName());
        
        // Test default values
        $this->assertTrue($product->isActive());
        $this->assertEquals(0, $product->getStock());
    }
    
    public function testProductSlugGeneration(): void
    {
        $product = new Product();
        $product->setName('Test Product Name');
        
        $this->assertEquals('test-product-name', $product->getSlug());
    }
}
```

## Functional Testing

### Testing Controllers

```php
namespace App\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;
use App\Repository\UserRepository;

class ProductControllerTest extends WebTestCase
{
    public function testIndexPageIsSuccessful(): void
    {
        $client = static::createClient();
        $client->request('GET', '/products');
        
        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Products');
    }
    
    public function testShowProduct(): void
    {
        $client = static::createClient();
        $client->request('GET', '/products/1');
        
        $this->assertResponseIsSuccessful();
        $this->assertSelectorExists('.product-details');
    }
    
    public function testCreateProductRequiresAuthentication(): void
    {
        $client = static::createClient();
        $client->request('GET', '/products/new');
        
        $this->assertResponseRedirects('/login');
    }
    
    public function testCreateProductAsAuthenticatedUser(): void
    {
        $client = static::createClient();
        
        // Authenticate user
        $userRepository = static::getContainer()->get(UserRepository::class);
        $testUser = $userRepository->findOneByEmail('admin@example.com');
        $client->loginUser($testUser);
        
        // Access protected page
        $crawler = $client->request('GET', '/products/new');
        
        $this->assertResponseIsSuccessful();
        
        // Fill and submit form
        $form = $crawler->selectButton('Save')->form([
            'product[name]' => 'Test Product',
            'product[price]' => '99.99',
            'product[description]' => 'Test description',
        ]);
        
        $client->submit($form);
        
        $this->assertResponseRedirects('/products');
        
        // Follow redirect
        $client->followRedirect();
        
        $this->assertSelectorTextContains('.alert-success', 'Product created successfully');
    }
}
```

### Testing Forms

```php
namespace App\Tests\Form;

use App\Form\ProductType;
use App\Entity\Product;
use Symfony\Component\Form\Test\TypeTestCase;

class ProductTypeTest extends TypeTestCase
{
    public function testSubmitValidData(): void
    {
        $formData = [
            'name' => 'Test Product',
            'price' => 99.99,
            'description' => 'Test description',
            'stock' => 10,
        ];
        
        $model = new Product();
        $form = $this->factory->create(ProductType::class, $model);
        
        $expected = new Product();
        $expected->setName('Test Product');
        $expected->setPrice(99.99);
        $expected->setDescription('Test description');
        $expected->setStock(10);
        
        $form->submit($formData);
        
        $this->assertTrue($form->isSynchronized());
        $this->assertEquals($expected->getName(), $model->getName());
        $this->assertEquals($expected->getPrice(), $model->getPrice());
        
        $view = $form->createView();
        $children = $view->children;
        
        foreach (array_keys($formData) as $key) {
            $this->assertArrayHasKey($key, $children);
        }
    }
}
```

## Integration Testing

### Testing API Endpoints

```php
namespace App\Tests\Api;

use ApiPlatform\Symfony\Bundle\Test\ApiTestCase;
use App\Entity\Product;

class ProductApiTest extends ApiTestCase
{
    public function testGetCollection(): void
    {
        $response = static::createClient()->request('GET', '/api/products');
        
        $this->assertResponseIsSuccessful();
        $this->assertResponseHeaderSame('content-type', 'application/ld+json; charset=utf-8');
        
        $this->assertJsonContains([
            '@context' => '/api/contexts/Product',
            '@id' => '/api/products',
            '@type' => 'hydra:Collection',
        ]);
        
        $this->assertCount(30, $response->toArray()['hydra:member']);
    }
    
    public function testCreateProduct(): void
    {
        $client = static::createClient();
        
        // Authenticate
        $token = $this->getToken($client);
        
        $response = $client->request('POST', '/api/products', [
            'headers' => [
                'Authorization' => 'Bearer ' . $token,
                'Content-Type' => 'application/json',
            ],
            'json' => [
                'name' => 'New Product',
                'price' => 149.99,
                'description' => 'A new product',
            ],
        ]);
        
        $this->assertResponseStatusCodeSame(201);
        $this->assertResponseHeaderSame('content-type', 'application/ld+json; charset=utf-8');
        $this->assertJsonContains([
            '@type' => 'Product',
            'name' => 'New Product',
            'price' => 149.99,
        ]);
    }
    
    public function testUpdateProduct(): void
    {
        $client = static::createClient();
        $iri = $this->findIriBy(Product::class, ['id' => 1]);
        
        $client->request('PUT', $iri, [
            'json' => [
                'price' => 199.99,
            ],
        ]);
        
        $this->assertResponseIsSuccessful();
        $this->assertJsonContains([
            '@id' => $iri,
            'price' => 199.99,
        ]);
    }
    
    public function testDeleteProduct(): void
    {
        $client = static::createClient();
        $iri = $this->findIriBy(Product::class, ['id' => 1]);
        
        $client->request('DELETE', $iri);
        
        $this->assertResponseStatusCodeSame(204);
        
        // Verify deletion
        $this->assertNull(
            static::getContainer()->get('doctrine')->getRepository(Product::class)->find(1)
        );
    }
    
    private function getToken($client): string
    {
        $response = $client->request('POST', '/api/login', [
            'json' => [
                'email' => 'admin@example.com',
                'password' => 'password123',
            ],
        ]);
        
        return $response->toArray()['token'];
    }
}
```

### Testing Services with Database

```php
namespace App\Tests\Service;

use App\Service\OrderService;
use App\Entity\Order;
use App\Entity\Product;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

class OrderServiceTest extends KernelTestCase
{
    private ?OrderService $orderService;
    private ?\Doctrine\ORM\EntityManager $entityManager;
    
    protected function setUp(): void
    {
        $kernel = self::bootKernel();
        
        $this->entityManager = $kernel->getContainer()
            ->get('doctrine')
            ->getManager();
        
        $this->orderService = $kernel->getContainer()
            ->get(OrderService::class);
    }
    
    public function testCreateOrder(): void
    {
        // Create test product
        $product = new Product();
        $product->setName('Test Product');
        $product->setPrice(99.99);
        $product->setStock(10);
        
        $this->entityManager->persist($product);
        $this->entityManager->flush();
        
        // Create order
        $order = $this->orderService->createOrder([
            'product_id' => $product->getId(),
            'quantity' => 2,
        ]);
        
        $this->assertInstanceOf(Order::class, $order);
        $this->assertEquals(199.98, $order->getTotal());
        $this->assertEquals(8, $product->getStock());
    }
    
    protected function tearDown(): void
    {
        parent::tearDown();
        
        $this->entityManager->close();
        $this->entityManager = null;
    }
}
```

## Test Doubles & Mocking

### Using Prophecy

```php
namespace App\Tests\Service;

use App\Service\EmailService;
use App\Service\NotificationService;
use PHPUnit\Framework\TestCase;
use Prophecy\PhpUnit\ProphecyTrait;

class NotificationServiceTest extends TestCase
{
    use ProphecyTrait;
    
    public function testSendNotification(): void
    {
        $emailService = $this->prophesize(EmailService::class);
        
        $emailService->send(
            'user@example.com',
            'Notification',
            'You have a new notification'
        )->shouldBeCalledOnce();
        
        $notificationService = new NotificationService($emailService->reveal());
        $notificationService->notify('user@example.com', 'You have a new notification');
    }
}
```

### Using PHPUnit Mock

```php
namespace App\Tests\Repository;

use App\Repository\ProductRepository;
use Doctrine\ORM\EntityManager;
use Doctrine\ORM\Query;
use PHPUnit\Framework\TestCase;

class ProductRepositoryTest extends TestCase
{
    public function testFindActiveProducts(): void
    {
        $query = $this->createMock(Query::class);
        $query->expects($this->once())
            ->method('getResult')
            ->willReturn(['product1', 'product2']);
        
        $qb = $this->getMockBuilder(\Doctrine\ORM\QueryBuilder::class)
            ->disableOriginalConstructor()
            ->getMock();
        
        $qb->expects($this->once())
            ->method('andWhere')
            ->with('p.active = :active')
            ->willReturnSelf();
        
        $qb->expects($this->once())
            ->method('setParameter')
            ->with('active', true)
            ->willReturnSelf();
        
        $qb->expects($this->once())
            ->method('getQuery')
            ->willReturn($query);
        
        $em = $this->createMock(EntityManager::class);
        $em->expects($this->once())
            ->method('createQueryBuilder')
            ->willReturn($qb);
        
        $repository = new ProductRepository($em);
        $result = $repository->findActiveProducts();
        
        $this->assertCount(2, $result);
    }
}
```

## Test Data Fixtures

### Creating Fixtures

```php
namespace App\DataFixtures;

use App\Entity\User;
use App\Entity\Product;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

class AppFixtures extends Fixture
{
    public const ADMIN_USER_REFERENCE = 'admin-user';
    
    public function __construct(
        private UserPasswordHasherInterface $passwordHasher
    ) {}
    
    public function load(ObjectManager $manager): void
    {
        // Create admin user
        $admin = new User();
        $admin->setEmail('admin@example.com');
        $admin->setRoles(['ROLE_ADMIN']);
        $admin->setPassword(
            $this->passwordHasher->hashPassword($admin, 'password123')
        );
        
        $manager->persist($admin);
        $this->addReference(self::ADMIN_USER_REFERENCE, $admin);
        
        // Create products
        for ($i = 1; $i <= 20; $i++) {
            $product = new Product();
            $product->setName('Product ' . $i);
            $product->setPrice(mt_rand(10, 200));
            $product->setDescription('Description for product ' . $i);
            $product->setStock(mt_rand(0, 100));
            
            $manager->persist($product);
        }
        
        $manager->flush();
    }
}
```

### Fixture Dependencies

```php
namespace App\DataFixtures;

use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Common\DataFixtures\DependentFixtureInterface;

class OrderFixtures extends Fixture implements DependentFixtureInterface
{
    public function load(ObjectManager $manager): void
    {
        $user = $this->getReference(AppFixtures::ADMIN_USER_REFERENCE);
        
        $order = new Order();
        $order->setUser($user);
        // ...
        
        $manager->persist($order);
        $manager->flush();
    }
    
    public function getDependencies(): array
    {
        return [
            AppFixtures::class,
        ];
    }
}
```

## Browser Testing with Panther

```php
namespace App\Tests\E2E;

use Symfony\Component\Panther\PantherTestCase;

class E2ETest extends PantherTestCase
{
    public function testHomePage(): void
    {
        $client = static::createPantherClient();
        $crawler = $client->request('GET', '/');
        
        $this->assertSelectorTextContains('h1', 'Welcome');
        
        // Take screenshot
        $client->takeScreenshot('tests/screenshots/homepage.png');
    }
    
    public function testJavaScriptInteraction(): void
    {
        $client = static::createPantherClient();
        $crawler = $client->request('GET', '/interactive');
        
        // Click button that triggers JavaScript
        $client->clickLink('Load More');
        
        // Wait for AJAX content
        $client->waitFor('.loaded-content');
        
        $this->assertSelectorExists('.loaded-content');
        $this->assertSelectorTextContains('.loaded-content', 'Dynamic content');
    }
    
    public function testFormSubmission(): void
    {
        $client = static::createPantherClient();
        $crawler = $client->request('GET', '/contact');
        
        // Fill form
        $crawler->filter('#contact_name')->sendKeys('John Doe');
        $crawler->filter('#contact_email')->sendKeys('john@example.com');
        $crawler->filter('#contact_message')->sendKeys('Test message');
        
        // Submit
        $crawler->filter('#contact_submit')->click();
        
        // Wait for response
        $client->waitFor('.alert-success');
        
        $this->assertSelectorTextContains('.alert-success', 'Message sent successfully');
    }
}
```

## Performance Testing

```php
namespace App\Tests\Performance;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class PerformanceTest extends WebTestCase
{
    public function testPageLoadTime(): void
    {
        $client = static::createClient();
        
        $startTime = microtime(true);
        $client->request('GET', '/products');
        $endTime = microtime(true);
        
        $loadTime = $endTime - $startTime;
        
        $this->assertLessThan(1, $loadTime, 'Page should load in less than 1 second');
    }
    
    public function testDatabaseQueryCount(): void
    {
        $client = static::createClient();
        $client->enableProfiler();
        
        $client->request('GET', '/products');
        
        if ($profile = $client->getProfile()) {
            $collector = $profile->getCollector('db');
            
            $this->assertLessThan(10, $collector->getQueryCount(), 
                'Page should execute less than 10 queries');
        }
    }
    
    public function testMemoryUsage(): void
    {
        $client = static::createClient();
        $client->enableProfiler();
        
        $client->request('GET', '/products');
        
        if ($profile = $client->getProfile()) {
            $collector = $profile->getCollector('memory');
            
            // Memory usage should be less than 50MB
            $this->assertLessThan(50 * 1024 * 1024, $collector->getMemory());
        }
    }
}
```

## Testing Commands

```php
namespace App\Tests\Command;

use Symfony\Bundle\FrameworkBundle\Console\Application;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;
use Symfony\Component\Console\Tester\CommandTester;

class ImportCommandTest extends KernelTestCase
{
    public function testExecute(): void
    {
        $kernel = static::createKernel();
        $application = new Application($kernel);
        
        $command = $application->find('app:import-products');
        $commandTester = new CommandTester($command);
        
        $commandTester->execute([
            'file' => 'tests/fixtures/products.csv',
            '--dry-run' => true,
        ]);
        
        $commandTester->assertCommandIsSuccessful();
        
        $output = $commandTester->getDisplay();
        $this->assertStringContainsString('Import completed', $output);
        $this->assertStringContainsString('10 products imported', $output);
    }
    
    public function testExecuteWithInvalidFile(): void
    {
        $kernel = static::createKernel();
        $application = new Application($kernel);
        
        $command = $application->find('app:import-products');
        $commandTester = new CommandTester($command);
        
        $commandTester->execute([
            'file' => 'nonexistent.csv',
        ]);
        
        $this->assertEquals(1, $commandTester->getStatusCode());
        $this->assertStringContainsString('File not found', $commandTester->getDisplay());
    }
}
```

## Code Coverage

### PHPUnit Configuration

```xml
<!-- phpunit.xml.dist -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         backupGlobals="false"
         colors="true"
         bootstrap="tests/bootstrap.php">
    
    <php>
        <ini name="display_errors" value="1" />
        <ini name="error_reporting" value="-1" />
        <env name="APP_ENV" value="test" force="true" />
        <env name="SHELL_VERBOSITY" value="-1" />
        <env name="SYMFONY_PHPUNIT_REMOVE" value="" />
        <env name="SYMFONY_PHPUNIT_VERSION" value="9.5" />
    </php>
    
    <testsuites>
        <testsuite name="Project Test Suite">
            <directory>tests</directory>
        </testsuite>
    </testsuites>
    
    <coverage processUncoveredFiles="true">
        <include>
            <directory suffix=".php">src</directory>
        </include>
        <exclude>
            <directory>src/Kernel.php</directory>
            <directory>src/DataFixtures</directory>
        </exclude>
    </coverage>
    
    <listeners>
        <listener class="Symfony\Bridge\PhpUnit\SymfonyTestsListener" />
    </listeners>
</phpunit>
```

### Running Tests with Coverage

```bash
# Generate HTML coverage report
php bin/phpunit --coverage-html coverage

# Generate text coverage in console
php bin/phpunit --coverage-text

# Generate Clover XML for CI
php bin/phpunit --coverage-clover coverage.xml
```

## Test Best Practices

1. **Follow AAA pattern**: Arrange, Act, Assert
2. **One assertion per test method** when possible
3. **Use descriptive test names** that explain what is being tested
4. **Test edge cases** and error conditions
5. **Mock external dependencies** in unit tests
6. **Use fixtures** for consistent test data
7. **Keep tests independent** - each test should be able to run alone
8. **Test public API only** - don't test private methods directly
9. **Use data providers** for testing multiple scenarios
10. **Write tests first** (TDD) for critical business logic