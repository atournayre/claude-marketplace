<?php

declare(strict_types=1);

namespace App\Invalide;

use App\Entity\Utilisateur;

final class UtilisateurInvalide
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
