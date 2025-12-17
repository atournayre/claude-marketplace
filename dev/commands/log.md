---
description: Ajoute des fonctionnalités de log au fichier en cours
argument-hint: [FICHIER]
allowed-tools: Read, Edit, Grep, Glob
---

# Ajout de logging avec LoggableInterface

Fichier cible : $ARGUMENTS

## Workflow

### 1. Lire et analyser le fichier
- Lire le contenu du fichier PHP
- Identifier la classe principale et ses propriétés
- Vérifier si `LoggableInterface` est déjà implémentée

### 2. Chercher les dépendances LoggableInterface
Pour chaque type-hint de propriété ou paramètre :
- Utiliser Grep pour chercher si la classe implémente `LoggableInterface`
- Noter les classes qui l'implémentent pour appeler `->toLog()` dessus

### 3. Ajouter LoggableInterface

Si la classe n'implémente pas encore `LoggableInterface` :

**Ajouter l'import :**
```php
use Atournayre\Contracts\Log\LoggableInterface;
```

**Ajouter l'interface à la déclaration de classe :**
```php
final class NomClasse implements LoggableInterface
```

**Ajouter la méthode toLog() :**
```php
/**
 * @return array<string, mixed>
 */
public function toLog(): array
{
    return [
        // Propriétés clés de l'objet
    ];
}
```

### 4. Règles pour le contenu de toLog()

**Propriétés à inclure :**
- `id` (si présent)
- Identifiants métier (email, code, référence...)
- États/statuts importants
- Dates clés (createdAt, updatedAt...)

**Propriétés à exclure :**
- Mots de passe, tokens, secrets
- Données personnelles sensibles
- Propriétés volumineuses (blobs, textes longs)

**Pour les objets imbriqués :**
- Si l'objet implémente `LoggableInterface` : `'relation' => $this->relation->toLog()`
- Sinon : `'relationId' => $this->relation->getId()` ou ignorer

**Pour les collections :**
```php
/**
 * @return array{count: int, items: array<int, array<string, mixed>>}
 */
public function toLog(): array
{
    return [
        'count' => $this->count(),
        'items' => array_map(fn ($item) => $item->toLog(), $this->items),
    ];
}
```

### 5. Vérification PHPStan
- Toujours ajouter `@return array<string, mixed>` sur la méthode
- Pour les collections : utiliser le type array shape approprié

## Exemple de résultat

```php
use Atournayre\Contracts\Log\LoggableInterface;

final class Commande implements LoggableInterface
{
    private Uuid $id;
    private string $reference;
    private Client $client;
    private \DateTimeImmutable $createdAt;
    private string $password; // Sensible, à exclure

    /**
     * @return array<string, mixed>
     */
    public function toLog(): array
    {
        return [
            'id' => $this->id->toRfc4122(),
            'reference' => $this->reference,
            'client' => $this->client->toLog(), // Si Client implémente LoggableInterface
            'createdAt' => $this->createdAt->format('c'),
            // password exclu intentionnellement
        ];
    }
}
```
