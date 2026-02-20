---
name: implementer:oneshot
description: Implémentation ultra-rapide d'une feature ciblée — Explore, Code, Test
argument-hint: <feature-description>
model: sonnet
allowed-tools: [Task, Read, Write, Edit, Grep, Glob, Bash]
version: 1.0.0
license: MIT
---

# OneShot — Implémentation rapide

Implémenter `$ARGUMENTS` à vitesse maximale. Ship fast, iterate later.

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow en 3 phases :**

### Phase 1 : EXPLORE (minimal)

Rassembler le contexte minimum viable :
- Utiliser `Glob` pour trouver 2-3 fichiers clés par pattern
- Utiliser `Grep` pour chercher des patterns spécifiques
- `WebSearch` uniquement si connaissance d'une API externe requise
- Pas de tour d'exploration — trouver des exemples et avancer

### Phase 2 : CODE (phase principale)

Exécuter les changements immédiatement :
- Suivre exactement les patterns existants du codebase
- Nommage clair plutôt que commentaires
- Rester STRICTEMENT dans le scope — ne modifier que ce qui est nécessaire
- Pas de commentaires sauf si vraiment complexe
- Pas de refactoring au-delà des exigences
- Lancer les formateurs si disponibles (`make fix`)

### Phase 3 : TEST (validation)

Vérifier la qualité :
- Lancer : `make phpstan` (ou équivalent)
- Si échec : corriger uniquement ce qui est cassé, relancer
- Pas de suite de tests complète sauf si explicitement demandé

## Sortie

```
## Terminé

**Tâche :** {ce qui a été implémenté}
**Fichiers modifiés :** {liste}
**Validation :** PHPStan OK
```

## Contraintes

- UNE seule tâche — pas d'améliorations tangentielles
- Pas de fichiers de documentation sauf si demandé
- Pas de refactoring hors du scope immédiat
- Pas d'ajouts "tant qu'on y est"
- Si bloqué plus de 2 tentatives : signaler le blocage et s'arrêter
- Ne JAMAIS créer de commits Git
