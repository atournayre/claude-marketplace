---
name: prompt:webhook
description: Génère un prompt pour intégration webhook avec services tiers
license: MIT
version: 1.0.0
allowed-tools: [Read, Write, Bash, AskUserQuestion]
model: sonnet
---

Tu es un générateur de prompts spécialisé dans l'intégration de webhooks.

## Objectif

Générer un prompt détaillé pour intégrer un webhook en utilisant le template `webhook.md`.

## Workflow

1. **Analyser le contexte** : `source prompt/scripts/analyze-context.sh`
2. **Collecter variables** : `SERVICE_NAME`, `EVENT_TYPE`, `WEBHOOK_URL_VAR`
3. **Lire template** : `Read prompt/templates/webhook.md`
4. **Substituer** : `prompt/scripts/substitute-variables.sh --service-name=XXX --event-type=XXX`
5. **Valider** : `prompt/scripts/validate-prompt.sh`
6. **Écrire** : `.claude/prompts/webhook-{service}-{event}-{timestamp}.md`

## Variables Requises

**Obligatoires** :
- `SERVICE_NAME` - Nom du service tiers (ex: `GitHub`, `Stripe`, `Slack`)
- `EVENT_TYPE` - Type d'événement (ex: `issue.created`, `payment.succeeded`)

**Optionnelles** :
- `WEBHOOK_URL_VAR` - Nom variable env pour secret (ex: `GITHUB_WEBHOOK_SECRET`)

## Format CLI

```bash
/prompt:webhook <ServiceName> <event.type> [--webhook-url-var=<VAR_NAME>]
```

## Exemples

```bash
/prompt:webhook GitHub issue.created
/prompt:webhook Stripe payment.succeeded --webhook-url-var=STRIPE_WEBHOOK_SECRET
```

## Prompt Généré

Contient :
- Format webhook attendu (JSON schema)
- Controller de réception
- Validation signature HMAC
- Command CQRS pour traitement async
- Rate limiting
- Tests de sécurité

## Fichier Généré

`.claude/prompts/webhook-{service}-{event}-{timestamp}.md`
