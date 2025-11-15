<?php

declare(strict_types=1);

namespace App\Entity;

use App\Contracts\HasUrlsInterface;
use App\Contracts\InvalideInterface;
use App\Contracts\OutInterface;
use App\Invalide\UtilisateurInvalide;
use App\MessageHandler\UtilisateurUrlsMessage;
use App\Out\UtilisateurOut;
use App\Repository\UtilisateurRepository;
use App\Urls\UtilisateurUrls;
use Atournayre\Common\Persistance\DatabaseTrait;
use Atournayre\Contracts\DependencyInjection\DependencyInjectionAwareInterface;
use Atournayre\Contracts\Log\LoggableInterface;
use Atournayre\Contracts\Null\NullableInterface;
use Atournayre\Contracts\Persistance\DatabaseEntityInterface;
use Atournayre\Null\NullTrait;
use Atournayre\Traits\DependencyInjectionTrait;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Uid\Uuid;

#[ORM\Entity(repositoryClass: UtilisateurRepository::class)]
final class Utilisateur implements LoggableInterface, DatabaseEntityInterface, NullableInterface, DependencyInjectionAwareInterface, OutInterface, HasUrlsInterface, InvalideInterface
{
    use DatabaseTrait;
    use DependencyInjectionTrait;
    use NullTrait;

    private function __construct(
        #[ORM\Id]
        #[ORM\Column(type: 'uuid')]
        private Uuid $id,
    ) {
    }

    public static function create(
        Uuid $id,
    ): self {
        return new self(
            id: $id,
        );
    }

    public function id(): Uuid
    {
        return $this->id;
    }

    /**
     * @return array<string, mixed>
     */
    public function toLog(): array
    {
        return [
            'id' => $this->id,
        ];
    }

    public function invalide(): UtilisateurInvalide
    {
        return UtilisateurInvalide::new(
            utilisateur: $this,
        );
    }

    public function out(): UtilisateurOut
    {
        return UtilisateurOut::new(
            utilisateur: $this,
        );
    }

    public function urls(): UtilisateurUrls
    {
        /** @var UtilisateurUrls $urls */
        $urls = UtilisateurUrlsMessage::new(
            id: $this->id->toRfc4122(),
        )->query($this->dependencyInjection()->queryBus());

        return $urls;
    }
}
