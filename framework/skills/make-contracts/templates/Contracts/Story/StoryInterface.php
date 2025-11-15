<?php

declare(strict_types=1);

namespace App\Contracts\Story;

interface StoryInterface
{
    public function build(): void;
}
