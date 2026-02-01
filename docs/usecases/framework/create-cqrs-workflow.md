---
title: Créer un workflow CQRS
description: Générer Message + Handler + Tests pour architecture CQRS
category: framework
plugins:
  - name: framework
    skills: [/framework:make-urls]
complexity: 3
duration: 8
keywords: [cqrs, message, handler, command, query]
related:
  - /usecases/framework/generate-entity-stack
  - /usecases/framework/setup-ddd-module
---

# Créer un workflow CQRS <Badge type="info" text="★★★ Avancé" /> <Badge type="tip" text="~8 min" />

## Contexte

Architecture CQRS (Command Query Responsibility Segregation) nécessite des Messages (Commands/Queries) et leurs Handlers. Créer tout ça manuellement est répétitif.

## Objectif

Générer automatiquement :

- ✅ Message (Command ou Query)
- ✅ Handler avec logique métier
- ✅ Tests unitaires
- ✅ Configuration Symfony Messenger

## Prérequis

**Plugins :**
- [framework](/plugins/framework) - Générateurs CQRS

**Outils :**
- Symfony Messenger configuré

## Workflow

**Commande :**
```bash
/framework:make-urls CreateOrder
```

**Fichiers générés :**
```
src/Message/CreateOrderMessage.php
src/MessageHandler/CreateOrderMessageHandler.php
tests/MessageHandler/CreateOrderMessageHandlerTest.php
```

## Exemple

```php
// Message
final readonly class CreateOrderMessage
{
    public function __construct(
        public int $userId,
        public array $items
    ) {
    }
}

// Handler
final class CreateOrderMessageHandler
{
    public function __invoke(CreateOrderMessage $message): Order
    {
        // Logique métier
    }
}
```

## Liens Connexes

**Use cases :**
- [Stack entité](/usecases/framework/generate-entity-stack)
- [Module DDD](/usecases/framework/setup-ddd-module)

**Plugins :**
- [Framework](/plugins/framework)
