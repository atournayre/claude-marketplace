---
description: Workflow complet de développement de feature
argument-hint: <description-feature>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Grep, Glob, Task, TodoWrite, AskUserQuestion, Bash
---

# Objectif

Orchestrateur du workflow de développement en 8 phases. Enchaîne automatiquement toutes les étapes avec des checkpoints utilisateur.

# Feature demandée

$ARGUMENTS

# Prérequis

⚠️ **Plugin feature-dev requis** pour les agents spécialisés.

Si non installé, afficher :
```
⚠️ Pour une expérience optimale, installe le plugin feature-dev :
/plugin install feature-dev@claude-code-plugins

Ce plugin fournit les agents :
- code-explorer (exploration codebase)
- code-architect (design architecture)
- code-reviewer (review qualité)

Continuer sans ces agents ? (Les phases 1, 3, 6 seront simplifiées)
```

# Workflow

## Initialisation

1. Créer le fichier `.dev-workflow-state.json` :
```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "startedAt": "{timestamp}",
  "currentPhase": 0,
  "phases": {}
}
```

2. Créer la todo list avec toutes les phases :
```
🔄 Workflow de développement : {feature}

⬜ 0. Discover   - Comprendre le besoin
⬜ 1. Explore    - Explorer codebase
⬜ 2. Clarify    - Questions clarification
⬜ 3. Design     - Proposer architectures
⬜ 4. Plan       - Générer specs
⬜ 5. Code       - Implémenter
⬜ 6. Review     - QA complète
⬜ 7. Summary    - Résumé final
```

## Phase 0 : Discover

Exécuter le contenu de `/dev:discover` :
- Clarifier la demande si ambiguë
- Identifier le problème résolu
- Résumer et confirmer compréhension

**Checkpoint :** Confirmer que la compréhension est correcte.

## Phase 1 : Explore

Exécuter le contenu de `/dev:explore` :
- Lancer agents `code-explorer` si disponibles
- Sinon, exploration manuelle avec Glob/Grep/Read
- Identifier les patterns et fichiers clés

## Phase 2 : Clarify

Exécuter le contenu de `/dev:clarify` :
- Poser les questions de clarification
- Documenter les décisions

**Checkpoint :** Attendre toutes les réponses.

## Phase 3 : Design

Exécuter le contenu de `/dev:design` :
- Lancer agents `code-architect` si disponibles
- Sinon, proposer 2-3 approches manuellement
- Présenter comparaison et recommandation

**Checkpoint :** Attendre le choix de l'architecture.

## Phase 4 : Plan

Exécuter le contenu de `/dev:plan` :
- Générer le plan dans `docs/specs/`
- Détailler les étapes d'implémentation

## Phase 5 : Code

Exécuter le contenu de `/dev:code` :
- Implémenter selon le plan
- Créer les tests
- Vérifier PHPStan

**Checkpoint :** Demander approbation avant de commencer.

## Phase 6 : Review

Exécuter le contenu de `/dev:review` :
- Lancer agent `code-reviewer` si disponible
- Lancer `phpstan-error-resolver`
- Lancer `elegant-objects-reviewer`
- Consolider les résultats

**Checkpoint :** Demander action (fix now / fix later / proceed).

## Phase 7 : Summary

Exécuter le contenu de `/dev:summary` :
- Résumer ce qui a été construit
- Documenter les décisions
- Suggérer prochaines étapes

# Affichage du statut

À chaque transition de phase, afficher :

```
🔄 Workflow de développement : {feature}

  ✅ 0. Discover   - Comprendre le besoin
  ✅ 1. Explore    - Explorer codebase
  🔵 2. Clarify    - Questions clarification  ← En cours
  ⬜ 3. Design     - Proposer architectures
  ⬜ 4. Plan       - Générer specs
  ⬜ 5. Code       - Implémenter
  ⬜ 6. Review     - QA complète
  ⬜ 7. Summary    - Résumé final
```

# Règles

- **Checkpoints obligatoires** aux phases 0, 2, 3, 5, 6
- **Ne jamais sauter de phase**
- **Mettre à jour** `.dev-workflow-state.json` après chaque phase
- **Afficher le statut** à chaque transition
- Si l'utilisateur interrompt, il peut reprendre avec `/dev:status` + la commande de la phase suivante

# Commande d'aide

Si l'utilisateur tape `/dev:feature` sans arguments :

```
📖 Workflow de développement de feature

Usage : /dev:feature <description>

Exemple :
  /dev:feature Ajouter authentification OAuth
  /dev:feature Refactorer le module de paiement

Ce workflow exécute 8 phases :
0. Discover → Comprendre le besoin
1. Explore  → Explorer le codebase
2. Clarify  → Questions de clarification
3. Design   → Proposer architectures
4. Plan     → Générer le plan
5. Code     → Implémenter
6. Review   → QA complète
7. Summary  → Résumé final

Pour voir le statut : /dev:status
```
