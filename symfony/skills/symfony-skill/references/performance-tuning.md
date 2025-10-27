# Symfony Performance Optimization Guide

## Profiling & Monitoring

### Symfony Profiler Configuration

```yaml
# config/packages/dev/web_profiler.yaml
web_profiler:
    toolbar: true
    intercept_redirects: false

framework:
    profiler:
        only_exceptions: false
        collect: true
        only_master_requests: true
```

### Blackfire Integration

```php
// Install Blackfire
// composer require blackfire/php-sdk

use Blackfire\Client;

class PerformanceService
{
    private Client $blackfire;
    
    public function profileOperation(string $name, callable $operation)
    {
        $config = new \Blackfire\Profile\Configuration();
        $config->setTitle($name);
        $config->setSamples(10);
        
        $probe = $this->blackfire->createProbe($config);
        
        $result = $operation();
        
        $profile = $this->blackfire->endProbe($probe);
        
        return $result;
    }
}
```

## Database Optimization

### Query Optimization

```php
namespace App\Repository;

use Doctrine\ORM\QueryBuilder;
use Doctrine\ORM\Query;

class ProductRepository extends ServiceEntityRepository
{
    /**
     * Optimized query with proper indexing and eager loading
     */
    public function findActiveProductsOptimized(): array
    {
        return $this->createQueryBuilder('p', 'p.id') // Index by ID
            ->select('p', 'c', 'i', 't') // Select all at once
            ->leftJoin('p.category', 'c')
            ->leftJoin('p.images', 'i')
            ->leftJoin('p.tags', 't')
            ->where('p.active = :active')
            ->andWhere('p.stock > :stock')
            ->setParameter('active', true)
            ->setParameter('stock', 0)
            ->orderBy('p.createdAt', 'DESC')
            ->setMaxResults(100) // Limit results
            ->getQuery()
            ->setHint(Query::HINT_FORCE_PARTIAL_LOAD, true) // Force partial loading
            ->useQueryCache(true) // Use query cache
            ->useResultCache(true, 3600) // Cache for 1 hour
            ->getResult();
    }
    
    /**
     * Use raw SQL for complex queries
     */
    public function findProductsWithComplexCalculation(): array
    {
        $sql = "
            SELECT 
                p.id,
                p.name,
                p.price,
                COUNT(DISTINCT o.id) as order_count,
                SUM(oi.quantity) as total_sold,
                AVG(r.rating) as avg_rating
            FROM product p
            LEFT JOIN order_item oi ON oi.product_id = p.id
            LEFT JOIN `order` o ON o.id = oi.order_id
            LEFT JOIN review r ON r.product_id = p.id
            WHERE p.active = 1
            GROUP BY p.id
            HAVING order_count > 10
            ORDER BY total_sold DESC
            LIMIT 50
        ";
        
        $stmt = $this->getEntityManager()->getConnection()->prepare($sql);
        return $stmt->executeQuery()->fetchAllAssociative();
    }
    
    /**
     * Batch processing for large datasets
     */
    public function processLargeDataset(\Closure $processor): void
    {
        $batchSize = 100;
        $offset = 0;
        
        while (true) {
            $products = $this->createQueryBuilder('p')
                ->setFirstResult($offset)
                ->setMaxResults($batchSize)
                ->getQuery()
                ->getResult();
            
            if (empty($products)) {
                break;
            }
            
            foreach ($products as $product) {
                $processor($product);
            }
            
            $this->getEntityManager()->flush();
            $this->getEntityManager()->clear(); // Clear to free memory
            
            $offset += $batchSize;
        }
    }
}
```

### Database Indexes

```php
namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
#[ORM\Table(name: 'product')]
#[ORM\Index(name: 'idx_active_stock', columns: ['active', 'stock'])]
#[ORM\Index(name: 'idx_category_active', columns: ['category_id', 'active'])]
#[ORM\Index(name: 'idx_created_at', columns: ['created_at'])]
#[ORM\UniqueConstraint(name: 'uniq_sku', columns: ['sku'])]
class Product
{
    #[ORM\Column(length: 100)]
    #[ORM\Index] // Single column index
    private ?string $sku = null;
    
    // Other properties...
}
```

### Connection Pooling

```yaml
# config/packages/doctrine.yaml
doctrine:
    dbal:
        connections:
            default:
                url: '%env(resolve:DATABASE_URL)%'
                # Connection pooling
                options:
                    persistent: true
                    # Maximum lifetime of a connection
                    connect_timeout: 10
                    # Server settings
                    1002: 'SET sql_mode = TRADITIONAL'
                pool:
                    min_connections: 2
                    max_connections: 10
                    max_idle_time: 600
                    
            read_replica:
                url: '%env(resolve:DATABASE_REPLICA_URL)%'
                options:
                    persistent: true
```

## Caching Strategies

### Multi-level Caching

```php
namespace App\Service;

use Psr\Cache\CacheItemPoolInterface;
use Symfony\Contracts\Cache\ItemInterface;
use Symfony\Contracts\Cache\TagAwareCacheInterface;

class CacheService
{
    public function __construct(
        private TagAwareCacheInterface $cache,
        private CacheItemPoolInterface $redisCache,
        private CacheItemPoolInterface $apcu
    ) {}
    
    /**
     * Multi-level cache with fallback
     */
    public function getWithFallback(string $key, callable $callback, int $ttl = 3600): mixed
    {
        // Level 1: APCu (fastest, local)
        $apcuItem = $this->apcu->getItem($key);
        if ($apcuItem->isHit()) {
            return $apcuItem->get();
        }
        
        // Level 2: Redis (fast, shared)
        $redisItem = $this->redisCache->getItem($key);
        if ($redisItem->isHit()) {
            $value = $redisItem->get();
            
            // Store in APCu for next time
            $apcuItem->set($value);
            $apcuItem->expiresAfter(300); // 5 minutes in APCu
            $this->apcu->save($apcuItem);
            
            return $value;
        }
        
        // Level 3: Generate and store in both caches
        $value = $callback();
        
        // Store in Redis
        $redisItem->set($value);
        $redisItem->expiresAfter($ttl);
        $this->redisCache->save($redisItem);
        
        // Store in APCu
        $apcuItem->set($value);
        $apcuItem->expiresAfter(300);
        $this->apcu->save($apcuItem);
        
        return $value;
    }
    
    /**
     * Cache with tags for invalidation
     */
    public function getWithTags(string $key, array $tags, callable $callback, int $ttl = 3600): mixed
    {
        return $this->cache->get($key, function (ItemInterface $item) use ($callback, $tags, $ttl) {
            $item->expiresAfter($ttl);
            $item->tag($tags);
            
            return $callback();
        });
    }
    
    /**
     * Invalidate by tags
     */
    public function invalidateTags(array $tags): void
    {
        $this->cache->invalidateTags($tags);
    }
    
    /**
     * Warm cache
     */
    public function warmCache(array $keys, callable $generator): void
    {
        foreach ($keys as $key => $params) {
            $this->cache->get($key, function () use ($generator, $params) {
                return $generator($params);
            });
        }
    }
}
```

### HTTP Caching

```php
namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\Cache;

class ProductController extends AbstractController
{
    #[Route('/products', name: 'product_list')]
    #[Cache(maxage: 3600, public: true, mustRevalidate: true)]
    public function index(): Response
    {
        $response = $this->render('product/index.html.twig');
        
        // Set cache headers
        $response->setPublic();
        $response->setMaxAge(3600);
        $response->setSharedMaxAge(3600);
        $response->headers->addCacheControlDirective('must-revalidate', true);
        
        // ETag for validation
        $response->setEtag(md5($response->getContent()));
        
        return $response;
    }
    
    #[Route('/products/{id}', name: 'product_show')]
    public function show(Product $product, Request $request): Response
    {
        $response = new Response();
        
        // Set ETag
        $etag = md5($product->getUpdatedAt()->format('c'));
        $response->setEtag($etag);
        
        // Set Last-Modified
        $response->setLastModified($product->getUpdatedAt());
        
        // Check if not modified
        $response->setNotModified();
        if ($response->isNotModified($request)) {
            return $response;
        }
        
        // Generate content
        return $this->render('product/show.html.twig', [
            'product' => $product
        ], $response);
    }
}
```

### ESI (Edge Side Includes)

```twig
{# templates/base.html.twig #}
<!DOCTYPE html>
<html>
<body>
    <header>
        {{ render_esi(controller('App\\Controller\\HeaderController::index')) }}
    </header>
    
    <main>
        {% block body %}{% endblock %}
    </main>
    
    <aside>
        {{ render_esi(controller('App\\Controller\\SidebarController::popularProducts', {
            'max': 5,
            '_cache': 3600
        })) }}
    </aside>
</body>
</html>
```

## Asset Optimization

### Webpack Encore Configuration

```javascript
// webpack.config.js
const Encore = require('@symfony/webpack-encore');

Encore
    .setOutputPath('public/build/')
    .setPublicPath('/build')
    
    // Enable production optimizations
    .enableSingleRuntimeChunk()
    .enableIntegrityHashes(Encore.isProduction())
    .enableBuildNotifications()
    
    // Split vendor code
    .splitEntryChunks()
    
    // Configure optimization
    .configureOptimizationSplitChunks((config) => {
        config.chunks = 'all';
        config.cacheGroups = {
            vendors: {
                test: /[\\/]node_modules[\\/]/,
                priority: 20,
                name: 'vendors',
                enforce: true
            },
            commons: {
                minChunks: 2,
                priority: 10,
                reuseExistingChunk: true
            }
        };
    })
    
    // Enable compression
    .configureCompressionPlugin((options) => {
        options.algorithm = 'gzip';
        options.test = /\.(js|css|html|svg)$/;
        options.threshold = 10240;
        options.minRatio = 0.8;
    })
    
    // Image optimization
    .configureImageRule({
        type: 'asset',
        maxSize: 4 * 1024 // 4 kb
    })
    
    // Enable versioning
    .enableVersioning(Encore.isProduction())
    
    // CDN support
    .setManifestKeyPrefix('build/')
    .configureCdn('https://cdn.example.com')
;

module.exports = Encore.getWebpackConfig();
```

### Lazy Loading Assets

```twig
{# Lazy load images #}
<img 
    src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3C/svg%3E"
    data-src="{{ asset('images/product.jpg') }}"
    loading="lazy"
    alt="Product"
    class="lazyload"
/>

{# Lazy load scripts #}
<script>
    // Dynamic import for code splitting
    document.getElementById('load-feature').addEventListener('click', async () => {
        const { FeatureModule } = await import('./features/heavy-feature.js');
        FeatureModule.init();
    });
</script>

{# Preload critical assets #}
<link rel="preload" href="{{ asset('build/app.css') }}" as="style">
<link rel="preload" href="{{ asset('build/app.js') }}" as="script">
<link rel="preload" href="{{ asset('fonts/main.woff2') }}" as="font" type="font/woff2" crossorigin>
```

## PHP Optimization

### OPcache Configuration

```ini
; php.ini or opcache.ini
opcache.enable=1
opcache.enable_cli=0
opcache.memory_consumption=256
opcache.interned_strings_buffer=16
opcache.max_accelerated_files=20000
opcache.max_wasted_percentage=10
opcache.validate_timestamps=0
opcache.revalidate_freq=0
opcache.fast_shutdown=1
opcache.enable_file_override=1
opcache.max_file_size=0
opcache.file_cache=/var/cache/opcache
opcache.file_cache_only=0
opcache.file_cache_consistency_checks=0

; Preload Symfony application
opcache.preload=/var/www/config/preload.php
opcache.preload_user=www-data
```

### Preloading Script

```php
// config/preload.php
if (file_exists(dirname(__DIR__).'/var/cache/prod/App_KernelProdContainer.preload.php')) {
    require dirname(__DIR__).'/var/cache/prod/App_KernelProdContainer.preload.php';
}

// Additional files to preload
$files = [
    __DIR__ . '/../src/Entity/',
    __DIR__ . '/../src/Repository/',
    __DIR__ . '/../src/Service/',
];

foreach ($files as $file) {
    if (is_dir($file)) {
        foreach (glob($file . '*.php') as $filename) {
            opcache_compile_file($filename);
        }
    } elseif (is_file($file)) {
        opcache_compile_file($file);
    }
}
```

## Async Processing

### Symfony Messenger Optimization

```yaml
# config/packages/messenger.yaml
framework:
    messenger:
        transports:
            async_priority_high:
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                options:
                    queue_name: high_priority
                    exchange:
                        name: high_priority
                        type: direct
                retry_strategy:
                    max_retries: 3
                    delay: 1000
                    
            async_priority_normal:
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                options:
                    queue_name: normal_priority
                    
            async_priority_low:
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                options:
                    queue_name: low_priority
                    
        routing:
            'App\Message\EmailMessage': async_priority_high
            'App\Message\ProcessImage': async_priority_normal
            'App\Message\GenerateReport': async_priority_low
            
        buses:
            messenger.bus.default:
                middleware:
                    - doctrine_ping_connection
                    - doctrine_clear_entity_manager
```

### Batch Message Processing

```php
namespace App\MessageHandler;

use App\Message\ProcessOrder;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
class ProcessOrderHandler
{
    private array $batch = [];
    private const BATCH_SIZE = 100;
    
    public function __invoke(ProcessOrder $message): void
    {
        $this->batch[] = $message;
        
        if (count($this->batch) >= self::BATCH_SIZE) {
            $this->processBatch();
        }
    }
    
    private function processBatch(): void
    {
        // Process entire batch at once
        $orderIds = array_map(fn($msg) => $msg->getOrderId(), $this->batch);
        
        $orders = $this->orderRepository->findByIds($orderIds);
        
        foreach ($orders as $order) {
            $this->processOrder($order);
        }
        
        $this->entityManager->flush();
        $this->batch = [];
    }
    
    public function __destruct()
    {
        if (!empty($this->batch)) {
            $this->processBatch();
        }
    }
}
```

## Server Optimization

### PHP-FPM Configuration

```ini
; /etc/php/8.1/fpm/pool.d/www.conf
[www]
pm = dynamic
pm.max_children = 50
pm.start_servers = 10
pm.min_spare_servers = 5
pm.max_spare_servers = 20
pm.max_requests = 500
pm.process_idle_timeout = 10s

; Performance tuning
request_terminate_timeout = 30
request_slowlog_timeout = 10s
slowlog = /var/log/php-fpm/slow.log

; Resource limits
rlimit_files = 65536
rlimit_core = unlimited
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/symfony
server {
    server_name example.com;
    root /var/www/symfony/public;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml application/atom+xml image/svg+xml text/javascript application/vnd.ms-fontobject application/x-font-ttf font/opentype;
    
    # Browser caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # PHP-FPM
    location ~ ^/index\.php(/|$) {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_split_path_info ^(.+\.php)(/.*)$;
        include fastcgi_params;
        
        # Performance
        fastcgi_buffer_size 128k;
        fastcgi_buffers 4 256k;
        fastcgi_busy_buffers_size 256k;
        fastcgi_temp_file_write_size 256k;
        
        # Cache
        fastcgi_cache_bypass $http_pragma $http_authorization;
        fastcgi_no_cache $http_pragma $http_authorization;
        
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        fastcgi_param DOCUMENT_ROOT $realpath_root;
        
        internal;
    }
    
    location / {
        try_files $uri /index.php$is_args$args;
    }
}
```

## Monitoring & Metrics

```php
namespace App\Service;

use Prometheus\CollectorRegistry;
use Prometheus\Storage\Redis;

class MetricsService
{
    private CollectorRegistry $registry;
    
    public function __construct()
    {
        Redis::setDefaultOptions([
            'host' => '127.0.0.1',
            'port' => 6379,
        ]);
        
        $this->registry = new CollectorRegistry(new Redis());
    }
    
    public function recordRequestDuration(string $route, float $duration): void
    {
        $histogram = $this->registry->getOrRegisterHistogram(
            'symfony',
            'request_duration_seconds',
            'Request duration in seconds',
            ['route']
        );
        
        $histogram->observe($duration, [$route]);
    }
    
    public function incrementCounter(string $name, array $labels = []): void
    {
        $counter = $this->registry->getOrRegisterCounter(
            'symfony',
            $name,
            'Counter for ' . $name,
            array_keys($labels)
        );
        
        $counter->inc(array_values($labels));
    }
}
```

## Performance Checklist

1. **Enable OPcache with preloading**
2. **Use HTTP caching headers**
3. **Implement database query caching**
4. **Optimize database indexes**
5. **Use CDN for static assets**
6. **Enable Gzip compression**
7. **Minimize and combine assets**
8. **Use async processing for heavy tasks**
9. **Implement lazy loading**
10. **Monitor and profile regularly**