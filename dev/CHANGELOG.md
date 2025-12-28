# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [2.1.2] - 2025-12-28

### Changed
- Ajout du timing complet du workflow `/dev:feature` :
  - Enregistrement des timestamps `startedAt` et `completedAt` pour chaque phase
  - Calcul automatique de la durée en millisecondes par phase
  - Affichage des durées formattées (s, m, h) dans le statut du workflow
  - Récapitulatif final avec temps total de développement
  - Affichage des durées dans la commande `/dev:status`
  - Tableau des temps dans le résumé final `/dev:summary`

## [2.1.1] - 2025-12-20

### Changed
- Ajout du champ `output-style` dans le frontmatter des commandes pour formatage automatique
  - `dev:status` → `ultra-concise`
  - `dev:summary` → `ultra-concise`
  - `dev:explore` → `bullet-points`
  - `dev:discover` → `bullet-points`
  - `dev:design` → `table-based`
  - `dev:clarify` → `table-based`

## [2.1.0] - 2025-12-20

### Added
- Support complet des **git worktrees** pour le développement parallèle de features
- Commande `/dev:worktree` pour gérer les worktrees :
  - `create <name> [base]` : Créer un worktree pour une feature
  - `list` : Lister tous les worktrees actifs
  - `status [name]` : Afficher le statut d'un worktree
  - `remove <name>` : Supprimer un worktree
  - `switch <name>` : Basculer vers un worktree
- Fichier `.claude/data/.dev-worktrees.json` pour tracker les métadonnées des worktrees
- Proposition automatique de création de worktree dans `/dev:feature` (Phase init)
- Phase 8 (Cleanup) dans `/dev:feature` pour nettoyer les worktrees après merge

### Changed
- Workflow `/dev:feature` étendu à 9 phases (ajout de la Phase 8 : Cleanup)
- Fichier `.dev-workflow-state.json` : ajout du champ `worktree` pour tracker le worktree associé

### Benefits
- **Développement parallèle** : Travailler sur plusieurs features simultanément
- **Pas de stash** : Fini les `git stash` qui s'accumulent
- **Contexte préservé** : IDE, serveur de dev et tests restent dans leur état
- **Branche main propre** : Isolation complète de chaque feature

## [2.0.1] - 2025-12-19

### Changed
- Déplacement du fichier `.dev-workflow-state.json` vers `.claude/data/.dev-workflow-state.json` (non versionné)
- Mise à jour de toutes les instructions pour utiliser le nouveau chemin

## [2.0.0] - 2025-12-17

### Added
- Workflow structuré en 8 phases pour le développement de features
- Commande `/dev:feature <desc>` : orchestrateur principal du workflow
- Commande `/dev:status` : affiche l'état du workflow et les commandes disponibles
- Commande `/dev:discover <desc>` : Phase 0 - comprendre le besoin
- Commande `/dev:explore` : Phase 1 - explorer le codebase avec agents parallèles
- Commande `/dev:clarify` : Phase 2 - questions de clarification
- Commande `/dev:design` : Phase 3 - proposer 2-3 architectures
- Commande `/dev:plan` : Phase 4 - générer plan dans `docs/specs/`
- Commande `/dev:review` : Phase 6 - QA complète (PHPStan + Elegant Objects + review)
- Commande `/dev:summary` : Phase 7 - résumé final
- Fichier `.claude/data/.dev-workflow-state.json` pour tracker l'état du workflow (non versionné)
- Checkpoints utilisateur aux phases critiques (0, 2, 3, 5, 6)

### Changed
- Commande `/dev:code` : Phase 5 - adaptée pour le nouveau workflow avec approbation explicite
- Commande `/dev:debug:error` → `/dev:debug` : simplification du nom

### Removed
- Commande `/dev:prepare` : remplacée par `/dev:plan`
- Commande `/dev:question` : peu utilisée
- Commande `/dev:docker` : peu utilisée
- Commande `/dev:context:load` : peu utilisée

### Dependencies
- Plugin `feature-dev@claude-code-plugins` recommandé pour les agents:
  - `code-explorer` (exploration codebase)
  - `code-architect` (design architecture)
  - `code-reviewer` (review qualité)

---

## [1.3.0] - 2025-12-17

### Added
- Commande `/dev:log [FICHIER]` : ajoute des fonctionnalités de logging avec `LoggableInterface`
  - Analyse les classes et propriétés du fichier PHP
  - Ajoute l'interface `LoggableInterface` d'Atournayre
  - Génère la méthode `toLog()` avec annotations PHPDoc pour PHPStan
  - Détecte les objets implémentant déjà `LoggableInterface` pour appeler `->toLog()`

## [1.2.0] - 2025-12-16

### Changed
- Commande `/dev:prepare` : utilise désormais le **Plan Mode natif** de Claude Code
  - Workflow interactif avec approbation utilisateur
  - Exploration du codebase avant planification
  - Option de lancer un swarm pour implémenter
  - Sauvegarde du plan dans `docs/specs/`
- Commande `/dev:code` : modèle sonnet → haiku (exécution mécanique de plans détaillés)

### Removed
- Skill `prepare` (remplacé par Plan Mode natif)

## [1.1.1] - 2025-12-14

### Changed
- Commande `/dev:question` : modèle sonnet → haiku (recherche simple, plus rapide/économique)

## [1.1.0] - 2025-11-15

### Added
- Agent `dev:meta-agent` - Génère configuration agents Claude Code
- Agent `dev:phpstan-error-resolver` - Résout erreurs PHPStan niveau 9
- Agent `dev:elegant-objects-reviewer` - Vérifie conformité principes Elegant Objects
- Commandes de chargement documentation (API Platform, Symfony, Meilisearch, Claude Code)

## [1.0.0] - Version initiale

### Added
- Commande `/dev:code` - Code codebase selon plan
- Commande `/dev:prepare` - Crée plan d'implémentation engineering
- Commande `/dev:question` - Répond questions sans coder
- Commande `/dev:docker` - Utilise Docker pour actions
- Commande `/dev:context:load` - Charge preset contexte session
- Commande `/dev:debug:error` - Analyse et résout erreurs
- Agents scrapers documentation divers frameworks
