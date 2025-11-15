<?php

declare(strict_types=1);

namespace App\Urls;

use App\Entity\Utilisateur;
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;

final readonly class UtilisateurUrls
{
    private function __construct(
        private UrlGeneratorInterface $urlGenerator,
        private Utilisateur $utilisateur,
    ) {
    }

    public static function new(
        UrlGeneratorInterface $urlGenerator,
        Utilisateur $utilisateur,
    ): self {
        return new self(
            urlGenerator: $urlGenerator,
            utilisateur: $utilisateur,
        );
    }
}
