<?php

declare(strict_types=1);

namespace App\Collection;

use App\Entity\Utilisateur;
use Atournayre\Contracts\Collection\AsListInterface;
use Atournayre\Contracts\Collection\AtLeastOneElementInterface;
use Atournayre\Contracts\Collection\CountByInterface;
use Atournayre\Contracts\Collection\CountInterface;
use Atournayre\Contracts\Collection\HasNoElementInterface;
use Atournayre\Contracts\Collection\HasOneElementInterface;
use Atournayre\Contracts\Collection\HasSeveralElementsInterface;
use Atournayre\Contracts\Collection\HasXElementsInterface;
use Atournayre\Contracts\Collection\ToArrayInterface;
use Atournayre\Contracts\Log\LoggableInterface;
use Atournayre\Primitives\Collection as PrimitiveCollection;
use Atournayre\Primitives\Traits\Collection;

final class UtilisateurCollection implements AsListInterface, ToArrayInterface, CountInterface, CountByInterface, AtLeastOneElementInterface, HasSeveralElementsInterface, HasNoElementInterface, HasOneElementInterface, HasXElementsInterface, LoggableInterface
{
    use Collection;
    use Collection\ToArray;
    use Collection\Countable;

    public static function asList(array $collection): self
    {
        return new self(PrimitiveCollection::of($collection));
    }

    /**
     * @return array<string, mixed>
     */
    public function toLog(): array
    {
        return [
            'count' => $this->count()->value(),
            'items' => $this->collection->map(fn (Utilisateur $item) => $item->toLog()),
        ];
    }

    // UNIQUEMENT les méthodes EXPLICITEMENT demandées par l'utilisateur
    // PAS d'anticipation de besoins futurs
    // PAS de méthodes génériques (add, remove, filter, map, etc.)
}
