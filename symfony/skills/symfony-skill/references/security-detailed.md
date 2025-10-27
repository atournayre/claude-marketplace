# Symfony Security Advanced Configuration

## Authentication Systems

### JWT Authentication

```php
// Install required packages
// composer require lexik/jwt-authentication-bundle

// config/packages/lexik_jwt_authentication.yaml
lexik_jwt_authentication:
    secret_key: '%env(resolve:JWT_SECRET_KEY)%'
    public_key: '%env(resolve:JWT_PUBLIC_KEY)%'
    pass_phrase: '%env(JWT_PASSPHRASE)%'
    token_ttl: 3600
    
// config/packages/security.yaml
security:
    firewalls:
        login:
            pattern: ^/api/login
            stateless: true
            json_login:
                check_path: /api/login_check
                success_handler: lexik_jwt_authentication.handler.authentication_success
                failure_handler: lexik_jwt_authentication.handler.authentication_failure
        
        api:
            pattern: ^/api
            stateless: true
            jwt: ~
```

### OAuth2 Implementation

```php
// Using KnpU OAuth2 Client Bundle
// composer require knpuniversity/oauth2-client-bundle

// config/packages/knpu_oauth2_client.yaml
knpu_oauth2_client:
    clients:
        google:
            type: google
            client_id: '%env(GOOGLE_CLIENT_ID)%'
            client_secret: '%env(GOOGLE_CLIENT_SECRET)%'
            redirect_route: connect_google_check
            redirect_params: {}

// Controller for OAuth
#[Route('/connect/google', name: 'connect_google')]
public function connectGoogle(ClientRegistry $clientRegistry): Response
{
    return $clientRegistry
        ->getClient('google')
        ->redirect(['email', 'profile']);
}

#[Route('/connect/google/check', name: 'connect_google_check')]
public function connectGoogleCheck(Request $request, ClientRegistry $clientRegistry): Response
{
    $client = $clientRegistry->getClient('google');
    $user = $client->fetchUser();
    
    // Handle user creation/authentication
    // ...
}
```

### Two-Factor Authentication

```php
// composer require scheb/2fa-bundle scheb/2fa-totp

// Entity with 2FA
#[ORM\Entity]
class User implements UserInterface, TwoFactorInterface
{
    #[ORM\Column(nullable: true)]
    private ?string $totpSecret = null;
    
    public function isTotpAuthenticationEnabled(): bool
    {
        return $this->totpSecret !== null;
    }
    
    public function getTotpAuthenticationUsername(): string
    {
        return $this->email;
    }
    
    public function getTotpAuthenticationConfiguration(): ?TotpConfigurationInterface
    {
        return new TotpConfiguration($this->totpSecret, TotpConfiguration::ALGORITHM_SHA1, 30, 6);
    }
}

// config/packages/security.yaml
security:
    firewalls:
        main:
            two_factor:
                auth_form_path: 2fa_login
                check_path: 2fa_login_check
```

## Custom Authenticators

### API Key Authenticator

```php
namespace App\Security;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Exception\AuthenticationException;
use Symfony\Component\Security\Http\Authenticator\AbstractAuthenticator;
use Symfony\Component\Security\Http\Authenticator\Passport\Badge\UserBadge;
use Symfony\Component\Security\Http\Authenticator\Passport\Passport;
use Symfony\Component\Security\Http\Authenticator\Passport\SelfValidatingPassport;

class ApiKeyAuthenticator extends AbstractAuthenticator
{
    public function __construct(
        private UserRepository $userRepository
    ) {}
    
    public function supports(Request $request): ?bool
    {
        return $request->headers->has('X-API-KEY');
    }
    
    public function authenticate(Request $request): Passport
    {
        $apiKey = $request->headers->get('X-API-KEY');
        
        if (null === $apiKey) {
            throw new CustomUserMessageAuthenticationException('No API key provided');
        }
        
        return new SelfValidatingPassport(
            new UserBadge($apiKey, function($apiKey) {
                $user = $this->userRepository->findOneBy(['apiKey' => $apiKey]);
                
                if (!$user) {
                    throw new CustomUserMessageAuthenticationException('Invalid API Key');
                }
                
                return $user;
            })
        );
    }
    
    public function onAuthenticationSuccess(Request $request, TokenInterface $token, string $firewallName): ?Response
    {
        return null;
    }
    
    public function onAuthenticationFailure(Request $request, AuthenticationException $exception): ?Response
    {
        return new JsonResponse([
            'message' => strtr($exception->getMessageKey(), $exception->getMessageData())
        ], Response::HTTP_UNAUTHORIZED);
    }
}
```

## Advanced Voters

### Hierarchical Voters

```php
namespace App\Security\Voter;

use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;
use Symfony\Component\Security\Core\Authorization\Voter\Voter;

class DocumentVoter extends Voter
{
    public const VIEW = 'DOCUMENT_VIEW';
    public const EDIT = 'DOCUMENT_EDIT';
    public const DELETE = 'DOCUMENT_DELETE';
    public const SHARE = 'DOCUMENT_SHARE';
    
    protected function supports(string $attribute, mixed $subject): bool
    {
        return in_array($attribute, [self::VIEW, self::EDIT, self::DELETE, self::SHARE])
            && $subject instanceof Document;
    }
    
    protected function voteOnAttribute(string $attribute, mixed $subject, TokenInterface $token): bool
    {
        $user = $token->getUser();
        
        if (!$user instanceof User) {
            return false;
        }
        
        /** @var Document $document */
        $document = $subject;
        
        // Check hierarchical permissions
        if ($this->hasHierarchicalAccess($user, $document, $attribute)) {
            return true;
        }
        
        return match($attribute) {
            self::VIEW => $this->canView($document, $user),
            self::EDIT => $this->canEdit($document, $user),
            self::DELETE => $this->canDelete($document, $user),
            self::SHARE => $this->canShare($document, $user),
            default => false,
        };
    }
    
    private function hasHierarchicalAccess(User $user, Document $document, string $attribute): bool
    {
        // Check department hierarchy
        if ($user->isDepartmentHead() && $document->getDepartment() === $user->getDepartment()) {
            return true;
        }
        
        // Check organization hierarchy
        if ($user->isOrganizationAdmin()) {
            return true;
        }
        
        return false;
    }
    
    private function canView(Document $document, User $user): bool
    {
        // Public documents
        if ($document->isPublic()) {
            return true;
        }
        
        // Owner can view
        if ($document->getOwner() === $user) {
            return true;
        }
        
        // Shared with user
        if ($document->getSharedUsers()->contains($user)) {
            return true;
        }
        
        // Team member can view team documents
        if ($document->getTeam() && $document->getTeam()->hasMember($user)) {
            return true;
        }
        
        return false;
    }
    
    private function canEdit(Document $document, User $user): bool
    {
        // Owner can edit
        if ($document->getOwner() === $user) {
            return true;
        }
        
        // Check edit permissions
        return $document->hasEditPermission($user);
    }
    
    private function canDelete(Document $document, User $user): bool
    {
        // Only owner and admins can delete
        return $document->getOwner() === $user || $user->hasRole('ROLE_ADMIN');
    }
    
    private function canShare(Document $document, User $user): bool
    {
        // Owner and users with share permission
        return $document->getOwner() === $user || $document->hasSharePermission($user);
    }
}
```

## Role Hierarchy & Dynamic Roles

### Dynamic Role Provider

```php
namespace App\Security;

use Symfony\Component\Security\Core\Role\RoleHierarchyInterface;

class DynamicRoleHierarchy implements RoleHierarchyInterface
{
    public function __construct(
        private RoleRepository $roleRepository
    ) {}
    
    public function getReachableRoleNames(array $roles): array
    {
        $reachableRoles = $roles;
        
        foreach ($roles as $role) {
            $roleEntity = $this->roleRepository->findOneBy(['name' => $role]);
            
            if ($roleEntity) {
                // Add inherited roles
                foreach ($roleEntity->getInheritedRoles() as $inheritedRole) {
                    $reachableRoles[] = $inheritedRole->getName();
                }
                
                // Add permission-based roles
                foreach ($roleEntity->getPermissions() as $permission) {
                    $reachableRoles[] = 'ROLE_' . strtoupper($permission->getName());
                }
            }
        }
        
        return array_unique($reachableRoles);
    }
}
```

## Security Event Listeners

### Login Success Handler

```php
namespace App\Security;

use Symfony\Component\Security\Http\Authentication\AuthenticationSuccessHandlerInterface;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Security\Core\Authentication\Token\TokenInterface;

class LoginSuccessHandler implements AuthenticationSuccessHandlerInterface
{
    public function __construct(
        private EntityManagerInterface $em,
        private LoggerInterface $logger,
        private IpGeolocationService $geolocation
    ) {}
    
    public function onAuthenticationSuccess(Request $request, TokenInterface $token): Response
    {
        $user = $token->getUser();
        
        // Log successful login
        $loginLog = new LoginLog();
        $loginLog->setUser($user);
        $loginLog->setIpAddress($request->getClientIp());
        $loginLog->setUserAgent($request->headers->get('User-Agent'));
        $loginLog->setTimestamp(new \DateTimeImmutable());
        
        // Get geolocation
        $location = $this->geolocation->locate($request->getClientIp());
        $loginLog->setLocation($location);
        
        // Check for suspicious activity
        if ($this->isSuspiciousLogin($user, $location)) {
            $this->notifyUserOfSuspiciousActivity($user, $loginLog);
        }
        
        // Update last login
        $user->setLastLoginAt(new \DateTimeImmutable());
        $user->setLastLoginIp($request->getClientIp());
        
        $this->em->persist($loginLog);
        $this->em->flush();
        
        // Log event
        $this->logger->info('User logged in', [
            'user' => $user->getUserIdentifier(),
            'ip' => $request->getClientIp()
        ]);
        
        return new RedirectResponse('/dashboard');
    }
    
    private function isSuspiciousLogin(User $user, ?Location $location): bool
    {
        // Check if login from new country
        $lastLogins = $this->em->getRepository(LoginLog::class)
            ->findLastLogins($user, 10);
        
        foreach ($lastLogins as $login) {
            if ($login->getLocation() && $login->getLocation()->getCountry() === $location->getCountry()) {
                return false;
            }
        }
        
        return true;
    }
}
```

## Access Control Lists (ACL)

### Custom ACL Implementation

```php
namespace App\Security\Acl;

class AclManager
{
    public function __construct(
        private EntityManagerInterface $em
    ) {}
    
    public function grantAccess(
        object $domainObject,
        UserInterface $user,
        array $permissions
    ): void {
        $acl = new Acl();
        $acl->setObjectClass(get_class($domainObject));
        $acl->setObjectId($domainObject->getId());
        $acl->setUser($user);
        $acl->setPermissions($permissions);
        
        $this->em->persist($acl);
        $this->em->flush();
    }
    
    public function revokeAccess(
        object $domainObject,
        UserInterface $user
    ): void {
        $acl = $this->em->getRepository(Acl::class)->findOneBy([
            'objectClass' => get_class($domainObject),
            'objectId' => $domainObject->getId(),
            'user' => $user
        ]);
        
        if ($acl) {
            $this->em->remove($acl);
            $this->em->flush();
        }
    }
    
    public function isGranted(
        string $permission,
        object $domainObject,
        UserInterface $user
    ): bool {
        $acl = $this->em->getRepository(Acl::class)->findOneBy([
            'objectClass' => get_class($domainObject),
            'objectId' => $domainObject->getId(),
            'user' => $user
        ]);
        
        return $acl && in_array($permission, $acl->getPermissions());
    }
}
```

## Security Headers & CORS

### Security Headers Subscriber

```php
namespace App\EventSubscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\ResponseEvent;
use Symfony\Component\HttpKernel\KernelEvents;

class SecurityHeadersSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            KernelEvents::RESPONSE => 'onKernelResponse',
        ];
    }
    
    public function onKernelResponse(ResponseEvent $event): void
    {
        $response = $event->getResponse();
        
        // Content Security Policy
        $response->headers->set(
            'Content-Security-Policy',
            "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        );
        
        // XSS Protection
        $response->headers->set('X-XSS-Protection', '1; mode=block');
        
        // Prevent MIME sniffing
        $response->headers->set('X-Content-Type-Options', 'nosniff');
        
        // Clickjacking protection
        $response->headers->set('X-Frame-Options', 'SAMEORIGIN');
        
        // HTTPS enforcement
        $response->headers->set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
        
        // Referrer Policy
        $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');
    }
}
```

### CORS Configuration

```yaml
# config/packages/nelmio_cors.yaml
nelmio_cors:
    defaults:
        origin_regex: true
        allow_origin: ['%env(CORS_ALLOW_ORIGIN)%']
        allow_methods: ['GET', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE']
        allow_headers: ['Content-Type', 'Authorization', 'X-API-KEY']
        expose_headers: ['Link', 'X-Total-Count']
        max_age: 3600
    paths:
        '^/api/':
            allow_origin: ['*']
            allow_headers: ['*']
            allow_methods: ['POST', 'PUT', 'GET', 'DELETE', 'OPTIONS']
            max_age: 3600
```

## Rate Limiting

```php
namespace App\Security;

use Symfony\Component\RateLimiter\RateLimiterFactory;
use Symfony\Component\HttpKernel\Exception\TooManyRequestsHttpException;

class RateLimitingService
{
    public function __construct(
        private RateLimiterFactory $apiLimiter,
        private RateLimiterFactory $loginLimiter
    ) {}
    
    public function checkApiLimit(string $apiKey): void
    {
        $limiter = $this->apiLimiter->create($apiKey);
        
        if (!$limiter->consume(1)->isAccepted()) {
            throw new TooManyRequestsHttpException(
                $limiter->getRetryAfter()->getTimestamp() - time(),
                'API rate limit exceeded'
            );
        }
    }
    
    public function checkLoginLimit(string $username, string $ip): void
    {
        $limiter = $this->loginLimiter->create($username . '_' . $ip);
        
        if (!$limiter->consume(1)->isAccepted()) {
            throw new TooManyRequestsHttpException(
                $limiter->getRetryAfter()->getTimestamp() - time(),
                'Too many login attempts'
            );
        }
    }
}

// config/packages/rate_limiter.yaml
framework:
    rate_limiter:
        api:
            policy: 'sliding_window'
            limit: 100
            interval: '60 minutes'
        login:
            policy: 'fixed_window'
            limit: 5
            interval: '15 minutes'
```

## Encryption & Hashing

### Field-level Encryption

```php
namespace App\Security;

use Symfony\Component\Security\Core\Encoder\EncoderFactoryInterface;

class EncryptionService
{
    private string $key;
    
    public function __construct(string $encryptionKey)
    {
        $this->key = $encryptionKey;
    }
    
    public function encrypt(string $data): string
    {
        $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length('aes-256-cbc'));
        $encrypted = openssl_encrypt($data, 'aes-256-cbc', $this->key, 0, $iv);
        
        return base64_encode($encrypted . '::' . $iv);
    }
    
    public function decrypt(string $data): string
    {
        list($encrypted_data, $iv) = explode('::', base64_decode($data), 2);
        
        return openssl_decrypt($encrypted_data, 'aes-256-cbc', $this->key, 0, $iv);
    }
}

// Doctrine Type for encrypted fields
class EncryptedStringType extends Type
{
    public function convertToDatabaseValue($value, AbstractPlatform $platform)
    {
        return $this->encryptionService->encrypt($value);
    }
    
    public function convertToPHPValue($value, AbstractPlatform $platform)
    {
        return $this->encryptionService->decrypt($value);
    }
}
```

## Security Best Practices

1. **Always use HTTPS in production**
2. **Implement CSRF protection for forms**
3. **Use parameterized queries to prevent SQL injection**
4. **Validate and sanitize all user input**
5. **Implement proper session management**
6. **Use strong password policies**
7. **Implement account lockout mechanisms**
8. **Log security events**
9. **Regular security audits**
10. **Keep dependencies updated**