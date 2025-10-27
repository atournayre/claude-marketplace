# Doctrine Advanced Patterns & Optimization

## Query Optimization Techniques

### 1. Eager Loading (Avoiding N+1 Problem)

```php
// Bad: N+1 queries
$products = $repository->findAll();
foreach ($products as $product) {
    echo $product->getCategory()->getName(); // Extra query for each product
}

// Good: Eager loading with JOIN
$products = $repository->createQueryBuilder('p')
    ->leftJoin('p.category', 'c')
    ->addSelect('c')
    ->leftJoin('p.tags', 't')
    ->addSelect('t')
    ->getQuery()
    ->getResult();
```

### 2. Partial Objects

```php
// Load only specific fields
$query = $em->createQuery('
    SELECT partial p.{id, name, price}
    FROM App\Entity\Product p
    WHERE p.active = true
');
$products = $query->getResult();
```

### 3. Query Result Cache

```php
$query = $em->createQuery('SELECT p FROM App\Entity\Product p')
    ->useQueryCache(true)
    ->useResultCache(true, 3600, 'products_list')
    ->setResultCacheDriver($cache);
```

## Advanced Mapping

### Inheritance Mapping

#### Single Table Inheritance
```php
#[ORM\Entity]
#[ORM\InheritanceType("SINGLE_TABLE")]
#[ORM\DiscriminatorColumn(name: "type", type: "string")]
#[ORM\DiscriminatorMap(["person" => Person::class, "employee" => Employee::class])]
class Person
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    protected ?int $id = null;
    
    #[ORM\Column]
    protected ?string $name = null;
}

#[ORM\Entity]
class Employee extends Person
{
    #[ORM\Column]
    private ?string $department = null;
}
```

#### Class Table Inheritance
```php
#[ORM\Entity]
#[ORM\InheritanceType("JOINED")]
#[ORM\DiscriminatorColumn(name: "discr", type: "string")]
#[ORM\DiscriminatorMap(["person" => Person::class, "employee" => Employee::class])]
class Person
{
    // Base class fields
}
```

### Embeddables

```php
#[ORM\Embeddable]
class Address
{
    #[ORM\Column]
    private ?string $street = null;
    
    #[ORM\Column]
    private ?string $city = null;
    
    #[ORM\Column]
    private ?string $zipCode = null;
}

#[ORM\Entity]
class User
{
    #[ORM\Embedded(class: Address::class)]
    private ?Address $address = null;
}
```

## Repository Patterns

### Specification Pattern

```php
interface Specification
{
    public function modify(QueryBuilder $qb, string $alias): void;
}

class ActiveProductSpecification implements Specification
{
    public function modify(QueryBuilder $qb, string $alias): void
    {
        $qb->andWhere("$alias.active = :active")
           ->setParameter('active', true);
    }
}

class PriceRangeSpecification implements Specification
{
    public function __construct(
        private float $min,
        private float $max
    ) {}
    
    public function modify(QueryBuilder $qb, string $alias): void
    {
        $qb->andWhere("$alias.price BETWEEN :min AND :max")
           ->setParameter('min', $this->min)
           ->setParameter('max', $this->max);
    }
}

// Repository implementation
class ProductRepository extends ServiceEntityRepository
{
    public function findBySpecifications(array $specifications): array
    {
        $qb = $this->createQueryBuilder('p');
        
        foreach ($specifications as $specification) {
            $specification->modify($qb, 'p');
        }
        
        return $qb->getQuery()->getResult();
    }
}

// Usage
$products = $repository->findBySpecifications([
    new ActiveProductSpecification(),
    new PriceRangeSpecification(10.00, 100.00)
]);
```

### Custom Hydration

```php
class SimpleArrayHydrator extends AbstractHydrator
{
    protected function hydrateAllData()
    {
        $result = [];
        foreach ($this->_stmt->fetchAll(PDO::FETCH_ASSOC) as $row) {
            $result[] = $row;
        }
        return $result;
    }
}

// Register hydrator
$em->getConfiguration()->addCustomHydrationMode(
    'SimpleArrayHydrator',
    SimpleArrayHydrator::class
);

// Use custom hydrator
$query = $em->createQuery('SELECT p.name, p.price FROM App\Entity\Product p');
$results = $query->getResult('SimpleArrayHydrator');
```

## Database Migrations

### Complex Migrations

```php
use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

final class Version20240101120000 extends AbstractMigration
{
    public function up(Schema $schema): void
    {
        // DDL changes
        $this->addSql('ALTER TABLE product ADD discount_price DECIMAL(10, 2) DEFAULT NULL');
        
        // Data migration
        $this->addSql('UPDATE product SET discount_price = price * 0.9 WHERE on_sale = true');
    }
    
    public function postUp(Schema $schema): void
    {
        // Complex data migrations after schema change
        $connection = $this->connection;
        $products = $connection->fetchAllAssociative('SELECT id, price FROM product');
        
        foreach ($products as $product) {
            // Complex calculation
            $newPrice = $this->calculateNewPrice($product['price']);
            $connection->update('product', 
                ['calculated_price' => $newPrice],
                ['id' => $product['id']]
            );
        }
    }
    
    public function down(Schema $schema): void
    {
        $this->addSql('ALTER TABLE product DROP discount_price');
    }
    
    private function calculateNewPrice(float $price): float
    {
        // Complex business logic
        return $price * 1.1;
    }
}
```

## Event Listeners & Lifecycle Callbacks

### Entity Listeners

```php
#[ORM\Entity]
#[ORM\EntityListeners([ProductListener::class])]
class Product
{
    // Entity code
}

class ProductListener
{
    #[ORM\PrePersist]
    public function prePersist(Product $product, LifecycleEventArgs $args): void
    {
        $product->setCreatedAt(new \DateTimeImmutable());
    }
    
    #[ORM\PreUpdate]
    public function preUpdate(Product $product, PreUpdateEventArgs $args): void
    {
        if ($args->hasChangedField('price')) {
            $oldPrice = $args->getOldValue('price');
            $newPrice = $args->getNewValue('price');
            
            // Log price change
            $this->logger->info('Price changed', [
                'product' => $product->getId(),
                'old' => $oldPrice,
                'new' => $newPrice
            ]);
        }
    }
}
```

### Doctrine Event Subscriber

```php
use Doctrine\Common\EventSubscriber;
use Doctrine\ORM\Events;
use Doctrine\Persistence\Event\LifecycleEventArgs;

class TimestampableSubscriber implements EventSubscriber
{
    public function getSubscribedEvents(): array
    {
        return [
            Events::prePersist,
            Events::preUpdate,
        ];
    }
    
    public function prePersist(LifecycleEventArgs $args): void
    {
        $entity = $args->getObject();
        
        if ($entity instanceof TimestampableInterface) {
            $entity->setCreatedAt(new \DateTimeImmutable());
            $entity->setUpdatedAt(new \DateTimeImmutable());
        }
    }
    
    public function preUpdate(LifecycleEventArgs $args): void
    {
        $entity = $args->getObject();
        
        if ($entity instanceof TimestampableInterface) {
            $entity->setUpdatedAt(new \DateTimeImmutable());
        }
    }
}
```

## Advanced Queries

### Native SQL Queries

```php
$rsm = new ResultSetMappingBuilder($em);
$rsm->addRootEntityFromClassMetadata(Product::class, 'p');

$sql = "
    SELECT p.*
    FROM product p
    WHERE MATCH(p.name, p.description) AGAINST(:search IN BOOLEAN MODE)
    ORDER BY MATCH(p.name, p.description) AGAINST(:search) DESC
";

$query = $em->createNativeQuery($sql, $rsm);
$query->setParameter('search', $searchTerm);
$results = $query->getResult();
```

### DQL Custom Functions

```php
use Doctrine\ORM\Query\AST\Functions\FunctionNode;

class MatchAgainst extends FunctionNode
{
    protected $columns = [];
    protected $needle;
    protected $mode;
    
    public function parse(\Doctrine\ORM\Query\Parser $parser): void
    {
        $parser->match(Lexer::T_IDENTIFIER);
        $parser->match(Lexer::T_OPEN_PARENTHESIS);
        
        $this->columns[] = $parser->StateFieldPathExpression();
        
        while ($parser->getLexer()->isNextToken(Lexer::T_COMMA)) {
            $parser->match(Lexer::T_COMMA);
            $this->columns[] = $parser->StateFieldPathExpression();
        }
        
        $parser->match(Lexer::T_COMMA);
        $this->needle = $parser->StringPrimary();
        
        $parser->match(Lexer::T_CLOSE_PARENTHESIS);
    }
    
    public function getSql(\Doctrine\ORM\Query\SqlWalker $sqlWalker): string
    {
        $columns = [];
        foreach ($this->columns as $column) {
            $columns[] = $column->dispatch($sqlWalker);
        }
        
        return sprintf(
            'MATCH(%s) AGAINST(%s IN BOOLEAN MODE)',
            implode(', ', $columns),
            $this->needle->dispatch($sqlWalker)
        );
    }
}

// Register function
$config->addCustomStringFunction('MATCH', MatchAgainst::class);
```

## Batch Processing

```php
class BatchProcessor
{
    private const BATCH_SIZE = 100;
    
    public function processBatch(EntityManagerInterface $em): void
    {
        $offset = 0;
        
        while (true) {
            $products = $em->getRepository(Product::class)
                ->createQueryBuilder('p')
                ->setFirstResult($offset)
                ->setMaxResults(self::BATCH_SIZE)
                ->getQuery()
                ->getResult();
            
            if (empty($products)) {
                break;
            }
            
            foreach ($products as $product) {
                // Process product
                $this->processProduct($product);
            }
            
            $em->flush();
            $em->clear(); // Detach entities to free memory
            
            $offset += self::BATCH_SIZE;
        }
    }
    
    public function iterableProcess(EntityManagerInterface $em): void
    {
        $query = $em->getRepository(Product::class)
            ->createQueryBuilder('p')
            ->getQuery();
        
        foreach ($query->toIterable() as $product) {
            $this->processProduct($product);
            
            if (($i++ % self::BATCH_SIZE) === 0) {
                $em->flush();
                $em->clear();
            }
        }
        
        $em->flush();
        $em->clear();
    }
}
```

## Database Connection Management

### Multiple Entity Managers

```yaml
# config/packages/doctrine.yaml
doctrine:
    dbal:
        default_connection: default
        connections:
            default:
                url: '%env(resolve:DATABASE_URL)%'
            analytics:
                url: '%env(resolve:ANALYTICS_DATABASE_URL)%'
    
    orm:
        default_entity_manager: default
        entity_managers:
            default:
                connection: default
                mappings:
                    App:
                        is_bundle: false
                        dir: '%kernel.project_dir%/src/Entity'
                        prefix: 'App\Entity'
            analytics:
                connection: analytics
                mappings:
                    Analytics:
                        is_bundle: false
                        dir: '%kernel.project_dir%/src/Entity/Analytics'
                        prefix: 'App\Entity\Analytics'
```

### Read/Write Splitting

```yaml
doctrine:
    dbal:
        connections:
            default:
                url: '%env(resolve:DATABASE_URL)%'
                replicas:
                    replica1:
                        url: '%env(resolve:DATABASE_REPLICA1_URL)%'
                    replica2:
                        url: '%env(resolve:DATABASE_REPLICA2_URL)%'
```

## Performance Best Practices

1. **Use indexes properly**: Add indexes on frequently queried columns
2. **Avoid SELECT ***: Only select needed columns
3. **Use pagination**: Don't load all records at once
4. **Cache metadata**: Cache entity metadata in production
5. **Use read-only entities**: Mark entities as read-only when possible
6. **Lazy loading vs Eager loading**: Choose based on use case
7. **Use DTO for read operations**: Avoid hydrating full entities
8. **Monitor slow queries**: Use Doctrine profiler in development
9. **Use transactions wisely**: Group related operations
10. **Clear entity manager**: Clear EM in batch operations