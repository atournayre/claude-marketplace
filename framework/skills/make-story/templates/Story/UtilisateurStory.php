<?php

declare(strict_types=1);

namespace App\Story;

use App\Contracts\Story\StoryInterface;
use App\Factory\UtilisateurFactory;
use Zenstruck\Foundry\Story;

final class UtilisateurStory extends Story implements StoryInterface
{
    public function build(): void
    {
        // Utilisateur par défaut
        UtilisateurFactory::createOne();

        // Utilisateurs avec IDs spécifiques pour les tests
        UtilisateurFactory::new()
            ->withSpecificId('01234567-89ab-cdef-0123-456789abcdef')
            ->create();

        // Créer plusieurs utilisateurs
        UtilisateurFactory::createMany(10);
    }
}
