# Skill : prompt:webhook

Génère un prompt pour intégration webhook avec services tiers.

## Usage

```bash
/prompt:webhook <ServiceName> <event.type> [--webhook-url-var=<VAR>]
```

## Arguments

| Argument | Type | Requis | Description | Exemple |
|----------|------|--------|-------------|---------|
| `ServiceName` | string | Oui | Nom service tiers | `GitHub` |
| `event.type` | string | Oui | Type événement | `issue.created` |
| `--webhook-url-var` | flag | Non | Nom variable env secret | `--webhook-url-var=GITHUB_WEBHOOK_SECRET` |

## Exemples

```bash
# Webhook GitHub
/prompt:webhook GitHub issue.created

# Webhook Stripe
/prompt:webhook Stripe payment.succeeded --webhook-url-var=STRIPE_WEBHOOK_SECRET
```

## Variables Substituées

- `{SERVICE_NAME}` - Nom service
- `{EVENT_TYPE}` - Type événement
- `{WEBHOOK_URL_VAR}` - Variable env

## Prompt Généré

Inclut :
- Endpoint POST `/webhook/{service}`
- Validation HMAC signature
- DTO Payload
- Command + Handler async
- Rate limiting (100/min)
- Tests sécurité

## Fichier Généré

`.claude/prompts/webhook-{service}-{event}-{timestamp}.md`
