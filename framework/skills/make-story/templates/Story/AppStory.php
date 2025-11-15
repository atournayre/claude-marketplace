<?php

namespace App\Story;

use App\Contracts\Story\StoryInterface;
use Zenstruck\Foundry\Attribute\AsFixture;
use Zenstruck\Foundry\Story;

#[AsFixture(name: 'main')]
final class AppStory extends Story implements StoryInterface
{
    public function build(): void
    {
        UtilisateurStory::load();
    }
}
