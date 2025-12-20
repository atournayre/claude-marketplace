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

1. **Proposition de worktree** (optionnel)

Demander à l'utilisateur s'il souhaite créer un worktree pour cette feature :

```
📂 Créer un worktree pour cette feature ?

Avantages des worktrees :
  • Garder votre branche main propre
  • Travailler sur plusieurs features en parallèle
  • Préserver le contexte de développement (IDE, serveur, tests)
  • Pas besoin de stash ou de switcher de branche

Le worktree sera créé dans : ../{repo-name}-{feature-slug}

Créer le worktree ? (o/n)
```

Si oui :
- Normaliser le nom de la feature en slug (kebab-case)
- Créer le worktree avec `/dev:worktree create {feature-slug}`
- Informer l'utilisateur du chemin et qu'il doit relancer Claude Code dans le worktree
- **ARRÊTER le workflow** avec un message :
  ```
  ✅ Worktree créé : ../{repo-name}-{feature-slug}

  Pour continuer le workflow :
    1. cd ../{repo-name}-{feature-slug}
    2. Relancer Claude Code
    3. /dev:feature {description}
  ```

Si non : Continuer le workflow normalement.

2. Créer le fichier `.claude/data/.dev-workflow-state.json` (créer le répertoire `.claude/data/` si nécessaire) :
```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "startedAt": "{timestamp}",
  "currentPhase": 0,
  "worktree": null,
  "phases": {}
}
```

Si un worktree a été créé, mettre à jour avec :
```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "startedAt": "{timestamp}",
  "currentPhase": 0,
  "worktree": {
    "name": "{feature-slug}",
    "path": "../{repo-name}-{feature-slug}",
    "branch": "feature/{feature-slug}"
  },
  "phases": {}
}
```

3. Créer la todo list avec toutes les phases :
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

## Phase 8 : Cleanup (optionnel)

Si un worktree a été créé (vérifier dans `.claude/data/.dev-workflow-state.json`), proposer de le nettoyer :

```
🧹 Nettoyage du worktree

La feature est terminée et prête à être mergée.
Souhaitez-vous nettoyer le worktree ?

Actions disponibles :
  1. Nettoyer maintenant (supprimer worktree + branche)
  2. Garder pour l'instant (vous pouvez le supprimer plus tard)
  3. Voir le statut du worktree

Votre choix ? (1/2/3)
```

**Option 1 : Nettoyer maintenant**
- Exécuter `/dev:worktree remove {feature-name}`
- Confirmer la suppression de la branche si elle a été mergée
- Mettre à jour `.claude/data/.dev-workflow-state.json` (status: "completed", worktree: null)

**Option 2 : Garder**
- Informer comment nettoyer plus tard :
  ```
  Pour nettoyer plus tard :
    /dev:worktree remove {feature-name}
  ```

**Option 3 : Voir le statut**
- Exécuter `/dev:worktree status {feature-name}`
- Puis reproposer les options 1 et 2

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
  ⬜ 8. Cleanup    - Nettoyer worktree (si créé)
```

# Règles

- **Proposition de worktree** à l'initialisation (optionnel)
- **Checkpoints obligatoires** aux phases 0, 2, 3, 5, 6
- **Ne jamais sauter de phase** (0-7)
- **Phase 8 (Cleanup)** uniquement si un worktree a été créé
- **Mettre à jour** `.claude/data/.dev-workflow-state.json` après chaque phase
- **Afficher le statut** à chaque transition
- Si l'utilisateur interrompt, il peut reprendre avec `/dev:status` + la commande de la phase suivante
- **Worktrees** : Toutes les métadonnées sont dans `.claude/data/.dev-worktrees.json`

# Commande d'aide

Si l'utilisateur tape `/dev:feature` sans arguments :

```
📖 Workflow de développement de feature

Usage : /dev:feature <description>

Exemple :
  /dev:feature Ajouter authentification OAuth
  /dev:feature Refactorer le module de paiement

Ce workflow exécute jusqu'à 9 phases :
0. Discover → Comprendre le besoin
1. Explore  → Explorer le codebase
2. Clarify  → Questions de clarification
3. Design   → Proposer architectures
4. Plan     → Générer le plan
5. Code     → Implémenter
6. Review   → QA complète
7. Summary  → Résumé final
8. Cleanup  → Nettoyer worktree (si créé)

💡 Worktrees (optionnel) :
Le workflow peut créer un git worktree pour isoler votre feature
et permettre le développement parallèle. Voir /dev:worktree --help

Pour voir le statut : /dev:status
Pour gérer les worktrees : /dev:worktree
```
