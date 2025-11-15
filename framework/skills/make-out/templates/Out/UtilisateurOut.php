<?php

declare(strict_types=1);

namespace App\Out;

use App\Entity\Utilisateur;

final readonly class UtilisateurOut
{
    private function __construct(
        private Utilisateur $utilisateur,
    ) {
    }

    public static function new(
        Utilisateur $utilisateur,
    ): self {
        return new self(
            utilisateur: $utilisateur,
        );
    }
}
