<?php

declare(strict_types=1);

namespace App\MessageHandler;

use App\Repository\UtilisateurRepositoryInterface;
use App\Urls\UtilisateurUrls;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;

#[AsMessageHandler]
final readonly class UtilisateurUrlsMessageHandler
{
    public function __construct(
        private UtilisateurRepositoryInterface $utilisateurRepository,
        private UrlGeneratorInterface $urlGenerator,
    ) {
    }

    public function __invoke(UtilisateurUrlsMessage $message): UtilisateurUrls
    {
        $utilisateur = $this->utilisateurRepository->find($message->id());

        return UtilisateurUrls::new(
            urlGenerator: $this->urlGenerator,
            utilisateur: $utilisateur,
        );
    }
}
