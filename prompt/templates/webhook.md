# Webhook : {SERVICE_NAME} - {EVENT_TYPE}

**Projet** : {PROJECT_NAME}
**Service** : {SERVICE_NAME}
**Type d'événement** : {EVENT_TYPE}
**Date** : {DATE}
**Auteur** : {AUTHOR}

## Objectif

Intégrer un webhook pour recevoir les événements `{EVENT_TYPE}` depuis {SERVICE_NAME}.

### Format Webhook Attendu

```json
{
  "event": "{EVENT_TYPE}",
  "timestamp": "2024-01-01T12:00:00Z",
  "signature": "sha256=...",
  "data": {
    // Payload spécifique
  }
}
```

### Scope

**Inclus** :
- Endpoint de réception webhook (POST)
- Validation signature HMAC
- Command CQRS pour traitement asynchrone
- Handler avec logique métier
- Rate limiting
- Logging et monitoring

**Exclus** :
- Configuration côté {SERVICE_NAME} (manuel)
- Webhook sortants (ce prompt concerne la réception)

## Architecture

### Composants

```
Infrastructure/
├── Webhook/
│   ├── Controller/
│   │   └── {SERVICE_NAME}WebhookController.php
│   ├── Validator/
│   │   └── {SERVICE_NAME}SignatureValidator.php
│   └── DTO/
│       └── {SERVICE_NAME}WebhookPayload.php
Application/
├── Message/
│   └── Command/
│       └── Process{SERVICE_NAME}{EVENT_TYPE}Command.php
└── Handler/
    └── Command/
        └── Process{SERVICE_NAME}{EVENT_TYPE}Handler.php
```

### Flux de Traitement

```
1. {SERVICE_NAME} → POST /webhook/{SERVICE_NAME}
2. Controller → Valider signature HMAC
3. Controller → Créer Command depuis payload
4. Messenger → Dispatcher Command (async)
5. Handler → Traiter événement (logique métier)
6. Handler → Logger résultat
```

## Plan d'Implémentation

### Phase 1 : Configuration

#### 1.1 Variables d'Environnement

**Fichier** : `.env`

```env
# Webhook {SERVICE_NAME}
{WEBHOOK_URL_VAR}=secret_key_here
```

**Fichier** : `config/packages/webhook.yaml`

```yaml
parameters:
    webhook.{SERVICE_NAME}.secret: '%env({WEBHOOK_URL_VAR})%'
```

#### 1.2 Route

**Fichier** : `config/routes/webhook.yaml`

```yaml
webhook_{SERVICE_NAME}:
    path: /webhook/{SERVICE_NAME}
    controller: {NAMESPACE}\Infrastructure\Webhook\Controller\{SERVICE_NAME}WebhookController
    methods: [POST]
```

### Phase 2 : Réception Webhook

#### 2.1 Créer DTO Payload

**Fichier** : `src/Infrastructure/Webhook/DTO/{SERVICE_NAME}WebhookPayload.php`

```php
namespace {NAMESPACE}\Infrastructure\Webhook\DTO;

final readonly class {SERVICE_NAME}WebhookPayload
{
    private function __construct(
        public string $event,
        public \DateTimeImmutable $timestamp,
        public array $data,
    ) {
    }

    public static function fromRequest(string $json): self
    {
        $decoded = json_decode($json, true, 512, JSON_THROW_ON_ERROR);

        return new self(
            event: $decoded['event'],
            timestamp: new \DateTimeImmutable($decoded['timestamp']),
            data: $decoded['data'],
        );
    }
}
```

#### 2.2 Créer Validateur Signature

**Fichier** : `src/Infrastructure/Webhook/Validator/{SERVICE_NAME}SignatureValidator.php`

```php
namespace {NAMESPACE}\Infrastructure\Webhook\Validator;

final readonly class {SERVICE_NAME}SignatureValidator
{
    public function __construct(
        private string $secret,
    ) {
    }

    public function validate(string $payload, string $signature): bool
    {
        $expectedSignature = 'sha256=' . hash_hmac('sha256', $payload, $this->secret);

        return hash_equals($expectedSignature, $signature);
    }
}
```

#### 2.3 Créer Controller

**Fichier** : `src/Infrastructure/Webhook/Controller/{SERVICE_NAME}WebhookController.php`

```php
namespace {NAMESPACE}\Infrastructure\Webhook\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Messenger\MessageBusInterface;
use Psr\Log\LoggerInterface;

final readonly class {SERVICE_NAME}WebhookController
{
    public function __construct(
        private {SERVICE_NAME}SignatureValidator $signatureValidator,
        private MessageBusInterface $messageBus,
        private LoggerInterface $logger,
    ) {
    }

    public function __invoke(Request $request): Response
    {
        $payload = $request->getContent();
        $signature = $request->headers->get('X-{SERVICE_NAME}-Signature');

        if (null === $signature) {
            return new Response('Missing signature', Response::HTTP_BAD_REQUEST);
        }

        if (!$this->signatureValidator->validate($payload, $signature)) {
            $this->logger->warning('Invalid webhook signature from {SERVICE_NAME}');
            return new Response('Invalid signature', Response::HTTP_UNAUTHORIZED);
        }

        try {
            $webhookPayload = {SERVICE_NAME}WebhookPayload::fromRequest($payload);

            if ('{EVENT_TYPE}' !== $webhookPayload->event) {
                return new Response('Event ignored', Response::HTTP_OK);
            }

            $command = Process{SERVICE_NAME}{EVENT_TYPE}Command::fromPayload($webhookPayload);
            $this->messageBus->dispatch($command);

            $this->logger->info('Webhook {EVENT_TYPE} from {SERVICE_NAME} dispatched');

            return new Response('OK', Response::HTTP_OK);
        } catch (\Throwable $e) {
            $this->logger->error('Webhook processing error', ['exception' => $e]);
            return new Response('Internal error', Response::HTTP_INTERNAL_SERVER_ERROR);
        }
    }
}
```

### Phase 3 : Traitement Asynchrone (CQRS)

#### 3.1 Créer Command

**Fichier** : `src/Application/Message/Command/Process{SERVICE_NAME}{EVENT_TYPE}Command.php`

```php
namespace {NAMESPACE}\Application\Message\Command;

final readonly class Process{SERVICE_NAME}{EVENT_TYPE}Command
{
    private function __construct(
        public array $data,
        public \DateTimeImmutable $occurredAt,
    ) {
    }

    public static function fromPayload({SERVICE_NAME}WebhookPayload $payload): self
    {
        return new self(
            data: $payload->data,
            occurredAt: $payload->timestamp,
        );
    }
}
```

#### 3.2 Créer Handler

**Fichier** : `src/Application/Handler/Command/Process{SERVICE_NAME}{EVENT_TYPE}Handler.php`

```php
namespace {NAMESPACE}\Application\Handler\Command;

use Symfony\Component\Messenger\Attribute\AsMessageHandler;
use Psr\Log\LoggerInterface;

#[AsMessageHandler]
final readonly class Process{SERVICE_NAME}{EVENT_TYPE}Handler
{
    public function __construct(
        private LoggerInterface $logger,
        // Injecter repositories, services nécessaires
    ) {
    }

    public function __invoke(Process{SERVICE_NAME}{EVENT_TYPE}Command $command): void
    {
        $this->logger->info('Processing {EVENT_TYPE} from {SERVICE_NAME}', [
            'data' => $command->data,
            'occurred_at' => $command->occurredAt->format('c'),
        ]);

        // Logique métier ici
        // Exemple : créer entité, mettre à jour statut, envoyer notification, etc.

        $this->logger->info('{EVENT_TYPE} processed successfully');
    }
}
```

### Phase 4 : Sécurité et Rate Limiting

#### 4.1 Rate Limiter

**Fichier** : `config/packages/rate_limiter.yaml`

```yaml
framework:
    rate_limiter:
        webhook_{SERVICE_NAME}:
            policy: 'sliding_window'
            limit: 100
            interval: '1 minute'
```

#### 4.2 Appliquer Rate Limiter

Ajouter dans le Controller :

```php
use Symfony\Component\RateLimiter\RateLimiterFactory;

public function __construct(
    // ...
    private RateLimiterFactory $webhook{SERVICE_NAME}Limiter,
) {
}

public function __invoke(Request $request): Response
{
    $limiter = $this->webhook{SERVICE_NAME}Limiter->create($request->getClientIp());

    if (!$limiter->consume(1)->isAccepted()) {
        return new Response('Too many requests', Response::HTTP_TOO_MANY_REQUESTS);
    }

    // ... reste du code
}
```

### Phase 5 : Tests

#### 5.1 Tests Unitaires Validator

**Fichier** : `tests/Infrastructure/Webhook/Validator/{SERVICE_NAME}SignatureValidatorTest.php`

#### 5.2 Tests Fonctionnels Controller

**Fichier** : `tests/Infrastructure/Webhook/Controller/{SERVICE_NAME}WebhookControllerTest.php`

- Tester signature valide
- Tester signature invalide
- Tester payload malformé
- Tester rate limiting

## Vérification

### Tests Manuels

#### 1. Générer Signature HMAC

```bash
echo -n '{"event":"{EVENT_TYPE}","timestamp":"2024-01-01T12:00:00Z","data":{}}' \
  | openssl dgst -sha256 -hmac "secret_key_here" \
  | awk '{print "sha256="$2}'
```

#### 2. Envoyer Webhook de Test

```bash
curl -X POST http://localhost/webhook/{SERVICE_NAME} \
  -H "Content-Type: application/json" \
  -H "X-{SERVICE_NAME}-Signature: sha256=..." \
  -d '{"event":"{EVENT_TYPE}","timestamp":"2024-01-01T12:00:00Z","data":{}}'
```

#### 3. Vérifier Logs

```bash
tail -f var/log/dev.log | grep "{SERVICE_NAME}"
```

#### 4. Vérifier Message Async

```bash
# Consommer messages
bin/console messenger:consume async -vv
```

### Checklist Qualité

- [ ] Route `/webhook/{SERVICE_NAME}` configurée
- [ ] Variable env {WEBHOOK_URL_VAR} définie
- [ ] Validation signature HMAC implémentée
- [ ] Rate limiting configuré (100/min)
- [ ] Command CQRS créé
- [ ] Handler async (#[AsMessageHandler])
- [ ] Logging activé (info + warning + error)
- [ ] Tests signature valide/invalide
- [ ] Tests rate limiting
- [ ] PHPStan niveau 9 : 0 erreur

## Points d'Attention

### Sécurité

- **Signature HMAC** : TOUJOURS valider avant traitement
- **HTTPS** : Obligatoire en production (Let's Encrypt)
- **IP Whitelisting** : Optionnel mais recommandé si {SERVICE_NAME} publie ses IPs
- **Secrets** : Ne JAMAIS commit {WEBHOOK_URL_VAR} en clair

### Rate Limiting

- **Limite par IP** : 100 requêtes/minute (ajustable)
- **Limite globale** : Optionnel selon volumétrie
- **Burst** : Sliding window permet pics courts

### Monitoring

- **Logs structurés** : JSON pour parsing facile
- **Alertes** : Si taux d'erreur > 5% ou latence > 1s
- **Métriques** : Compter webhooks reçus, traités, échoués

### Risques Identifiés

| Risque | Mitigation |
|--------|-----------|
| Replay attacks | Vérifier timestamp, rejeter si > 5min |
| DDoS | Rate limiting + IP whitelisting |
| Handler synchrone bloque webhook | Handler ASYNC obligatoire |
| Secret exposé | Variables env + vault en prod |

## Fichiers Créés

- `src/Infrastructure/Webhook/Controller/{SERVICE_NAME}WebhookController.php`
- `src/Infrastructure/Webhook/Validator/{SERVICE_NAME}SignatureValidator.php`
- `src/Infrastructure/Webhook/DTO/{SERVICE_NAME}WebhookPayload.php`
- `src/Application/Message/Command/Process{SERVICE_NAME}{EVENT_TYPE}Command.php`
- `src/Application/Handler/Command/Process{SERVICE_NAME}{EVENT_TYPE}Handler.php`
- `tests/Infrastructure/Webhook/Validator/{SERVICE_NAME}SignatureValidatorTest.php`
- `tests/Infrastructure/Webhook/Controller/{SERVICE_NAME}WebhookControllerTest.php`

## Fichiers Modifiés

- `.env` (ajouter {WEBHOOK_URL_VAR})
- `config/packages/webhook.yaml`
- `config/routes/webhook.yaml`
- `config/packages/rate_limiter.yaml`
- `config/packages/messenger.yaml` (routing async)
