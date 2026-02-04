## [2.5.1] - 2026-02-04

### Changed
- Migrer noms de modèles Claude vers format court (sonnet, haiku, opus)

# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [2.5.0] - 2026-01-31

### Added
- **Skill `/oneshot`** - Implémentation ultra-rapide (speed > completeness)
  - Workflow minimal : Explore (minimal) → Code (main) → Test (validate)
  - Philosophy : Ship fast, iterate later
  - Contraintes strictes : ONE task, NO refactoring, NO tangents
  - Validation simple : lint + typecheck uniquement
  - Idéal pour : petits fixes, single tasks, prototypes rapides
  - Migré depuis mlvn plugin (AIBlueprint v1.0.0)

- **Skill `/ralph`** (setup-ralph) - Setup Ralph autonomous coding loop
  - Alternative à `/dev:auto:feature` pour workflows autonomes
  - Workflow : PRD interactif → user stories → ralph.sh loop
  - Setup ONLY : ne lance jamais le loop automatiquement
  - Structure complète : scripts/setup.sh + steps/ (4 étapes)
  - Accumulation learnings entre iterations
  - Migré depuis mlvn plugin (AIBlueprint v1.0.0)

### Changed
- **Skill `/dev:review`** - Ajout Examine step (adversarial review) ⭐
  - Nouvelle tâche #5 : Examine (challenge decisions, edge cases)
  - Questions adversariales : edge cases, limites, sécurité, performance, concurrence
  - Focus : chercher ce qui **pourrait casser** en production
  - Identifier hypothèses non validées
  - Challenger décisions d'architecture
  - TaskManagement : 5 tâches au lieu de 4 (examine bloquée par consolidation)

## [2.4.1] - 2026-01-26

### Removed
- Commandes legacy : 23 commandes migrées vers plugin centralisé `command`
  - Déplacement vers plugin `command` (workaround issue #15178)
  - Skills restent fonctionnels via le plugin `command`

## [2.4.0] - 2026-01-25

### Added
- Commande `/dev:auto:check-prerequisites` - Vérifier tous les prérequis - Mode AUTO (Phase -1)
- Commande `/dev:auto:clarify` - Lever ambiguités avec heuristiques automatiques (Phase 3)
- Commande `/dev:auto:code` - Implémenter selon le plan - Mode AUTO (Phase 6)
- Commande `/dev:auto:design` - Choisir architecture automatiquement (Phase 4)
- Commande `/dev:auto:discover` - Comprendre le besoin avant développement - Mode AUTO (Phase 0)
- Commande `/dev:auto:explore` - Explorer le codebase automatiquement - Mode AUTO (Phase 2)
- Commande `/dev:auto:feature` - Workflow complet de développement automatisé (mode non-interactif)
- Commande `/dev:auto:fetch-issue` - Récupérer le contenu d'une issue GitHub - Mode AUTO (Phase 0)
- Commande `/dev:auto:plan` - Générer plan d'implémentation automatiquement - Mode AUTO (Phase 5)
- Commande `/dev:auto:review` - Review avec auto-fix automatique - Mode AUTO (Phase 7)
- Commande `/dev:clarify` - Poser questions pour lever ambiguités (Phase 2)
- Commande `/dev:code` - Implémenter selon le plan (Phase 5)
- Commande `/dev:debug` - Analyser et résoudre une erreur (message simple ou stack trace)
- Commande `/dev:design` - Designer 2-3 approches architecturales (Phase 3)
- Commande `/dev:discover` - Comprendre le besoin avant développement (Phase 0)
- Commande `/dev:explore` - Explorer le codebase avec agents parallèles (Phase 1)
- Commande `/dev:feature` - Workflow complet de développement de feature
- Commande `/dev:log` - Ajoute des fonctionnalités de log au fichier en cours
- Commande `/dev:plan` - Générer plan d'implémentation dans docs/specs/ (Phase 4)
- Commande `/dev:review` - Review qualité complète - PHPStan + Elegant Objects + code review (Phase 6)
- Commande `/dev:status` - Affiche le workflow et l'étape courante
- Commande `/dev:summary` - Résumé de ce qui a été construit (Phase 7)
- Commande `/dev:worktree` - Gestion des git worktrees pour développement parallèle

## [2.3.3] - 2026-01-24

### Changed
- Stabilisation des skills du plugin dev suite à migration commands → skills

## [2.3.2] - 2026-01-24

### Changed
- Intégration du task management system dans 5 skills dev/ :
  - `dev:feature` - 9 tâches (phases 0-8)
  - `dev:auto:feature` - 11 tâches (phases 0-10 automatiques)
  - `dev:review` - 4 tâches (3 reviews parallèles + consolidation)
  - `dev:explore` - 4 tâches (3 agents parallèles + consolidation)
  - `dev:plan` - 5 tâches (étapes séquentielles)
- Ajout de TaskCreate/TaskUpdate pour suivi progression workflows
- Documentation patterns task management dans chaque skill
- Support des dépendances entre tâches (addBlockedBy)

## [2.3.1] - 2026-01-24

### Fixed
- Restauration du contenu complet des 10 skills auto-* (check-prerequisites, fetch-issue, discover, explore, clarify, design, plan, code, review, feature)
- Correction des 9 placeholders "DESCRIPTION" avec vraies descriptions
- Skills auto-* passés de stubs 23 lignes à implémentations complètes (60-300 lignes selon skill)

## [2.3.0] - 2026-01-22

### Changed
- Migration de tous les commands vers le format skills
- Conversion de 23 commands en 23 skills avec support natif Claude Code
  - 13 skills racine : status, feature, discover, explore, clarify, design, plan, code, review, summary, debug, log, worktree
  - 10 skills auto : check-prerequisites, fetch-issue, discover, explore, clarify, design, plan, code, review, feature

### Added
- Préservation complète des hooks complexes (PreToolUse/PostToolUse)
- Support output-style avec workaround pour skills concernées

### Removed
- Répertoire /commands/ - complètement migré en /skills/

## [2.2.2] - 2026-01-10

### Changed
- **Hooks pour commandes** : Ajout de hooks de validation et d'automatisation
  - `/dev:code` : PHPStan en temps réel après chaque Edit, auto-formatage PSR-12 après Write, validation plan existe
  - `/dev:review` : Tests automatiques avant review, suggestion de commit après fixes appliquées

## [2.2.1] - 2026-01-02

### Changed
- **Git worktree paths** : migré de chemins parallèles `../<repo>-<name>` vers structure standard `.worktrees/<name>`
  - Permet de garder tous les worktrees dans le repo au lieu de polluer le répertoire parent
  - Suit la convention habituelle des git worktrees
  - Chemins plus simples et découverte plus facile (`.worktrees/` visible à la racine)
  - Mise à jour dans `/dev:worktree`, `/dev:feature`, `/dev:auto:feature` et documentation

## [2.2.0] - 2026-01-02

### Added
- **Mode automatisé complet** : `/dev:auto:feature <issue-number>`
  - 10 phases non-interactives (0-9) : fetch → design → code → review → cleanup → PR
  - Récupération automatique des spécifications depuis GitHub issues
  - Détection multi-langage (PHP, JavaScript, Go) avec QA tools appropriés
  - Boucle auto-fix max 3 tentatives par langage (PHPStan L9 blocker)
  - Git worktree automatique (création, branchage, cleanup)
  - Workflow state JSON pour tracking complet (timing, décisions, erreurs)
  - Rollback automatique en cas d'échec
- Nouveaux skills du workflow auto:
  - `/dev:auto:check-prerequisites` (Phase 0) - Vérification prérequis
  - `/dev:auto:fetch-issue` (Phase 1) - Récupération issue GitHub
  - `/dev:auto:discover` (Phase 2) - Validation spec automatique
  - `/dev:auto:explore` (Phase 3) - Exploration codebase
  - `/dev:auto:clarify` (Phase 4) - Heuristiques automatiques
  - `/dev:auto:design` (Phase 5) - Sélection architecture (Pragmatic Balance)
  - `/dev:auto:plan` (Phase 6) - Génération plan
  - `/dev:auto:code` (Phase 7) - Implémentation directe
  - `/dev:auto:review` (Phase 8) - QA multi-langage + auto-fix
  - `/dev:auto:feature` (orchestrateur) - Coordination 10 phases
- Fichier `.env.claude` pour configuration defaults (MAIN_BRANCH, REPO, PROJECT)
- Support `--no-interaction` dans `/git:pr` et `/git:cd-pr` pour automation

### Changed
- `/dev:feature` reste inchangé (mode interactif)
- `/git:pr` et `/git:cd-pr` : chargement configuration depuis `.env.claude` + flag `--no-interaction`
- Description plugin : ajout de "automation" aux keywords

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
