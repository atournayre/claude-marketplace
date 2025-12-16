---
description: Recherche temps réel via Google Search intégré à Gemini
argument-hint: <query>
---

Recherche des informations fraîches et actuelles via l'intégration Google Search native de Gemini.

## Arguments

- `<query>` : Requête de recherche

## Exemples

```
/gemini:search "Symfony 7 latest version release date"
/gemini:search "PHP 8.4 new features 2025"
/gemini:search "Claude Code latest updates december 2025"
/gemini:search "Best PHP frameworks comparison 2025"
```

## Cas d'usage idéaux

- Versions actuelles de frameworks
- Documentation récente
- Actualités tech post-janvier 2025
- Comparatifs de technologies récents
- Release notes

## Exécution

Tu dois utiliser l'agent `gemini-researcher` avec la requête fournie.

L'agent va :
1. Structurer la requête pour Google Search
2. Appeler Gemini 2.5 Flash avec grounding web
3. Retourner les résultats avec sources

Après la réponse Gemini, vérifie la pertinence des infos et intègre-les dans le contexte de la conversation.
