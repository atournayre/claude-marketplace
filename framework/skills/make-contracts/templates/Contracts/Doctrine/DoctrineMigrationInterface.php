<?php

declare(strict_types=1);

namespace App\Contracts\Doctrine;

use Doctrine\DBAL\Schema\Schema;

interface DoctrineMigrationInterface
{
    public function up(Schema $schema): void;

    public function down(Schema $schema): void;

    public function description(): string;

    public function isTransactional(): bool;
}
