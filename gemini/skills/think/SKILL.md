---
name: gemini:think
description: Délègue un problème complexe à Gemini Deep Think
argument-hint: <problem-description>
version: 1.0.0
license: MIT
---

Soumet un problème complexe à Gemini pour une réflexion approfondie avec exploration multi-hypothèses.

## Arguments

- `<problem-description>` : Description du problème à résoudre

## Exemples

```
/gemini:think "Comment implémenter un système de saga pour transactions distribuées avec Symfony Messenger?"
/gemini:think "Quel algorithme de cache optimal pour 80% lectures, 20% écritures, données de 1KB à 10MB?"
/gemini:think "Architecture pour un système de notifications temps réel scalable à 1M users?"
```

## Cas d'usage idéaux

- Problèmes mathématiques/algorithmiques
- Décisions architecturales avec trade-offs
- Optimisation de systèmes complexes
- Raisonnement sur systèmes distribués

## Exécution

Tu dois utiliser l'agent `gemini-thinker` avec le problème fourni.

L'agent va :
1. Structurer le problème pour Gemini
2. Appeler Gemini 2.5 Pro en mode réflexion step-by-step
3. Retourner l'analyse complète avec recommandations

Après la réponse Gemini, synthétise les points clés et adapte la solution au contexte du projet si pertinent.
