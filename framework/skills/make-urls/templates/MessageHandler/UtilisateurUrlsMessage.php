<?php

declare(strict_types=1);

namespace App\MessageHandler;

use Atournayre\Common\AbstractQueryEvent;
use Atournayre\Contracts\CommandBus\QueryInterface;

final class UtilisateurUrlsMessage extends AbstractQueryEvent implements QueryInterface
{
    private function __construct(
        public string $id,
    ) {
    }

    public static function new(
        string $id,
    ): self {
        return new self(
            id: $id,
        );
    }

    public function id(): string
    {
        return $this->id;
    }
}
