<?php

declare(strict_types=1);

namespace App\Factory;

use App\Entity\Utilisateur;
use Symfony\Component\Uid\Uuid;
use Zenstruck\Foundry\Persistence\PersistentObjectFactory;

/**
 * @extends PersistentObjectFactory<Utilisateur>
 */
final class UtilisateurFactory extends PersistentObjectFactory
{
    public static function class(): string
    {
        return Utilisateur::class;
    }

    protected function defaults(): array|callable
    {
        return [
            'id' => Uuid::v4(),
        ];
    }

    protected function initialize(): static
    {
        return $this
            ->instantiateWith(function (array $attributes) {
                return Utilisateur::create(
                    id: $attributes['id'],
                );
            })
        ;
    }

    public function withSpecificId(string $uuid): self
    {
        return $this->with([
            'id' => Uuid::fromString($uuid),
        ]);
    }
}
