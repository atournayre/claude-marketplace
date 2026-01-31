# Changelog - Atournayre Claude Plugin Marketplace

Toutes les modifications notables du marketplace seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [Unreleased]

## [2026.01.31] - 2026-01-31

### Plugins Added
- **utils v1.0.0** - Nouveau plugin skills/agents utilitaires génériques
  - Skill `/fix-grammar` : correction grammaire/orthographe (single/multi mode, auto-detect langue)
  - Agent `action` : validation conditionnelle avant exécution
  - Agent `explore-codebase` : exploration avec imports chains
  - Migration depuis mlvn plugin (AIBlueprint v1.0.0)
  - Dépôt : [utils/CHANGELOG.md](utils/CHANGELOG.md)

### Plugins Updated
- **mlvn v1.1.0** - Nettoyage après migration vers écosystème
  - Suppression éléments migrés (security validator, skill-creator, memory, subagent, ralph, fix-grammar, agents, etc.)
  - Conservé : skills Git, meta-prompt-creator, workflow-apex, utils-fix-errors, agents explore-docs/websearch
  - Documentation mise à jour pour refléter la structure réduite
  - Dépôt : [mlvn/CHANGELOG.md](mlvn/CHANGELOG.md)

- **dev v2.5.0** - Nouveaux skills oneshot, ralph + examine step
  - Nouveau skill `/oneshot` : implémentation ultra-rapide (speed > completeness)
  - Nouveau skill `/ralph` (setup-ralph) : autonomous coding loop (PRD → stories → loop)
  - Examine step ajouté dans `/dev:review` : adversarial review (challenge decisions, edge cases)
  - TaskManagement : 5 tâches dans review (examine bloquée par consolidation)
  - Migration depuis mlvn plugin (AIBlueprint v1.0.0)
  - Dépôt : [dev/CHANGELOG.md](dev/CHANGELOG.md)

- **git v1.11.0** - Nouveau skill fix-pr-comments + clarification auto-push
  - Nouveau skill `/fix-pr-comments` : implémente systématiquement TOUS les commentaires de review PR
  - Batched MultiEdit pour efficacité (same-file modifications)
  - Auto-commit + auto-push avec checklist progression
  - Clarification documentation `/git:commit` : auto-push déjà activé par défaut (flag `--no-push` pour désactiver)
  - Migration depuis mlvn plugin (AIBlueprint v1.0.0)
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)

- **claude v1.3.0** - Intégration skills mlvn (skill-creator, memory, make-subagent)
  - Nouveau skill `/skill-creator` : créateur complet avec progressive disclosure, bundled resources, scripts TypeScript
  - Nouveau skill `/memory` : gestion CLAUDE.md 4-level hierarchy (global, workspace, package, directory)
  - Nouveau skill `/make-subagent` : créateur subagents YAML avec orchestration patterns
  - Suppression `/claude:make:command` (remplacé par skill-creator, supérieur 100%)
  - Migration depuis mlvn plugin (AIBlueprint v1.0.0)
  - Dépôt : [claude/CHANGELOG.md](claude/CHANGELOG.md)

- **customize v1.1.0** - Intégration Bash Security Validator (100+ patterns, 82+ tests)
  - Validateur de sécurité pour commandes Bash via hook PreToolUse
  - Architecture hybride Python (hooks) + TypeScript/Bun (validators)
  - Détection patterns malveillants : fork bombs, backdoors, exfiltration données
  - Protection chemins système : /etc, /usr, /bin, /sys, /proc, /dev, /root
  - Logs sécurité avec traçabilité complète
  - Dépôt : [customize/CHANGELOG.md](customize/CHANGELOG.md)

### Plugins Added
- **mlvn v1.0.0** - Intégration AIBlueprint by Melvynx
  - 4 agents spécialisés (action, explore-codebase, explore-docs, websearch)
  - 4 skills Git (commit, create-pr, fix-pr-comments, merge)
  - 4 skills Meta (claude-memory, prompt-creator, skill-creator, subagent-creator)
  - 3 skills Workflow (ralph-loop, apex, apex-free)
  - 3 skills Utilities (fix-errors, fix-grammar, oneshot)
  - Hook de sécurité PreToolUse pour validation de commandes Bash
  - Scripts utilitaires (command-validator, statusline)
  - Documentation complète en français
  - Dépôt : [mlvn/CHANGELOG.md](mlvn/CHANGELOG.md)

## [2026.01.28] - 2026-01-28

### Plugins Updated
- **prompt v1.3.0** - Nouvelle skill de transformation de prompts en prompts exécutables
  - Nouvelle skill `prompt:transform` pour transformer un prompt quelconque en prompt exécutable
  - Compatible avec le Task Management System (TaskCreate/TaskUpdate/TaskList)
  - Support de fichiers et texte en entrée
  - Génération de fichiers dans `.claude/prompts/` du projet utilisateur
  - Bump MINOR : nouvelle fonctionnalité (skill)
  - Dépôt : [prompt/CHANGELOG.md](prompt/CHANGELOG.md)

## [2026.01.26.1] - 2026-01-26

### Plugins Updated
- **notifications v1.0.2** - Correction structure manifest plugin.json
  - Conformité avec validation Claude Code
  - `author` : string → objet
  - `repository` : objet → string
  - Suppression clés invalides (`hooks`, `scripts`, `requirements`, `features`)
  - Dépôt : [notifications/CHANGELOG.md](notifications/CHANGELOG.md)

## [2026.01.26] - 2026-01-26

### Plugins Added
- **command v1.0.0** - Plugin centralisé de commandes
  - Workaround temporaire pour Claude Code issue #15178
  - 63 commandes centralisées depuis 11 plugins
  - Permet d'utiliser les skills via des slash commands
  - Dépôt : [command/CHANGELOG.md](command/CHANGELOG.md)

### Plugins Updated
- **claude v1.2.1** - Migration commandes vers plugin centralisé
  - Suppression de 5 commandes legacy
  - Dépôt : [claude/CHANGELOG.md](claude/CHANGELOG.md)
- **dev v2.4.1** - Migration commandes vers plugin centralisé
  - Suppression de 23 commandes legacy
  - Dépôt : [dev/CHANGELOG.md](dev/CHANGELOG.md)
- **doc v1.6.1** - Migration commandes vers plugin centralisé
  - Suppression de 4 commandes legacy
  - Dépôt : [doc/CHANGELOG.md](doc/CHANGELOG.md)
- **framework v1.1.1** - Migration commandes vers plugin centralisé
  - Suppression de 9 commandes legacy
  - Dépôt : [framework/CHANGELOG.md](framework/CHANGELOG.md)
- **gemini v1.4.1** - Migration commandes vers plugin centralisé
  - Suppression de 3 commandes legacy
  - Dépôt : [gemini/CHANGELOG.md](gemini/CHANGELOG.md)
- **git v1.10.2** - Migration commandes vers plugin centralisé
  - Suppression de 8 commandes legacy
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)
- **github v1.3.1** - Migration commandes vers plugin centralisé
  - Suppression de 2 commandes legacy
  - Dépôt : [github/CHANGELOG.md](github/CHANGELOG.md)
- **marketing v1.2.1** - Migration commandes vers plugin centralisé
  - Suppression de 1 commande legacy
  - Dépôt : [marketing/CHANGELOG.md](marketing/CHANGELOG.md)
- **prompt v1.1.1** - Migration commandes vers plugin centralisé
  - Suppression de 7 commandes legacy
  - Dépôt : [prompt/CHANGELOG.md](prompt/CHANGELOG.md)
- **qa v1.3.1** - Migration commandes vers plugin centralisé
  - Suppression de 2 commandes legacy
  - Dépôt : [qa/CHANGELOG.md](qa/CHANGELOG.md)
- **symfony v1.3.1** - Migration commandes vers plugin centralisé
  - Suppression de 4 commandes legacy
  - Dépôt : [symfony/CHANGELOG.md](symfony/CHANGELOG.md)

## [2026.01.25-3] - 2026-01-25

### Plugins Updated
- **git v1.10.1** - Mise à jour légacy command reference
  - Commande `/git:commit` : référence mise à jour vers skill

### Plugins Added
- **notifications v1.0.0** - Système de notifications avancé
  - Queue persistante `queue.jsonl` pour historique complet
  - Auto-détection multi-projet (4 niveaux de fallback)
  - Dispatchers configurables : `notify-send`, `phpstorm` (futur), `custom`
  - Gestion statuts `unread`/`read` avec marquage manuel
  - Scripts CLI : `dispatch-notifications.py`, `view-notifications.sh`, `mark-notification-read.py`
  - Hook `notification.py` + API `write_notification.py`
  - Support priorités (`low`, `normal`, `high`, `critical`) et types
  - Backend `FileQueueBackend` avec utils complets
  - Documentation complète + guide migration
  - Dépôt : [notifications/CHANGELOG.md](notifications/CHANGELOG.md)

### Plugins Removed
- **output-styles v1.0.0** - Supprimé (migration vers mécanisme natif `~/.claude/output-styles/`)

## [2026.01.25-2] - 2026-01-25

### Plugins Updated
- **notifications v1.0.1** - Amélioration notifications desktop
  - Nouvelle fonction `play_beep()` pour audio feedback PulseAudio/terminal
  - Support `get_friendly_title()` pour titres plus lisibles
  - Cleanups whitespace et suppression imports inutilisés
  - Dépôt : [notifications/CHANGELOG.md](notifications/CHANGELOG.md)

## [2026.01.25] - 2026-01-25

### Plugins Updated
- **claude v1.2.0** - Migration commands → skills complète
  - 5 nouveaux skills : `alias:add`, `challenge`, `doc:load`, `doc:question`, `make:command`
  - Dépôt : [claude/CHANGELOG.md](claude/CHANGELOG.md)
- **dev v2.4.0** - Migration commands → skills complète
  - 23 nouveaux skills (incluant 10 auto:*)
  - Dépôt : [dev/CHANGELOG.md](dev/CHANGELOG.md)
- **doc v1.6.0** - Migration commands → skills complète
  - 4 nouveaux skills : `adr`, `doc-loader`, `rtfm`, `update`
  - Dépôt : [doc/CHANGELOG.md](doc/CHANGELOG.md)
- **framework v1.1.0** - Migration commands → skills complète
  - 9 nouveaux skills : `make:all`, `make:collection`, `make:contracts`, `make:entity`, `make:factory`, `make:invalide`, `make:out`, `make:story`, `make:urls`
  - Dépôt : [framework/CHANGELOG.md](framework/CHANGELOG.md)
- **gemini v1.4.0** - Migration commands → skills complète
  - 3 nouveaux skills : `analyze`, `search`, `think`
  - Dépôt : [gemini/CHANGELOG.md](gemini/CHANGELOG.md)
- **git v1.10.0** - Migration commands → skills complète
  - 8 nouveaux skills : `branch`, `commit`, `conflit`, `git-cd-pr`, `git-pr-core`, `git-pr`, `release-notes`, `release-report`
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)
- **github v1.3.0** - Migration commands → skills complète
  - 2 nouveaux skills : `fix`, `github-impact`
  - Dépôt : [github/CHANGELOG.md](github/CHANGELOG.md)
- **marketing v1.2.0** - Migration commands → skills complète
  - 1 nouveau skill : `linkedin`
  - Dépôt : [marketing/CHANGELOG.md](marketing/CHANGELOG.md)
- **prompt v1.1.0** - Nouveau plugin générateur de prompts
  - 7 nouveaux skills : `architecture`, `configuration`, `feature`, `generic`, `refactoring`, `webhook`, `workflow`
  - Dépôt : [prompt/CHANGELOG.md](prompt/CHANGELOG.md)
- **qa v1.3.0** - Migration commands → skills complète
  - 2 nouveaux skills : `elegant-objects`, `phpstan-resolver`
  - Dépôt : [qa/CHANGELOG.md](qa/CHANGELOG.md)
- **symfony v1.3.0** - Migration commands → skills complète
  - 4 nouveaux skills : `doc:load`, `doc:question`, `make`, `symfony-framework`
  - Dépôt : [symfony/CHANGELOG.md](symfony/CHANGELOG.md)

## [2026.01.24.2] - 2026-01-24

### Plugins Updated
- **claude v1.1.1** - Stabilisation suite à migration commands → skills
- **dev v2.3.3** - Stabilisation suite à migration commands → skills
- **doc v1.5.1** - Stabilisation suite à migration commands → skills
- **framework v1.0.3** - Stabilisation suite à migration commands → skills
- **git v1.9.2** - Stabilisation suite à migration commands → skills
- **github v1.2.2** - Stabilisation suite à migration commands → skills
- **marketing v1.1.1** - Stabilisation suite à migration commands → skills
- **qa v1.2.5** - Stabilisation suite à migration commands → skills
- **symfony v1.2.1** - Stabilisation suite à migration commands → skills

## [2026.01.24] - 2026-01-24

### Plugins Updated
- **dev v2.3.2** - Intégration task management system
  - 5 skills modifiés : `dev:feature` (9 tâches), `dev:auto:feature` (11 tâches), `dev:review` (4 tâches), `dev:explore` (4 tâches), `dev:plan` (5 tâches)
  - TaskCreate/TaskUpdate pour suivi progression workflows en temps réel
  - Support des dépendances entre tâches (addBlockedBy)
  - Documentation patterns task management et agents parallèles
  - Dépôt : [dev/CHANGELOG.md](dev/CHANGELOG.md)
- **git v1.9.1** - Intégration task management system
  - 3 skills modifiés : `git-pr` (13 tâches), `git-cd-pr` (15 tâches), `git:release-notes` (5 tâches)
  - Suivi détaillé workflows création PR (QA → création → review)
  - Tâches conditionnelles (review automatique si plugin installé)
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)
- **framework v1.0.2** - Intégration task management system
  - 1 skill modifié : `framework:make:all` (10 tâches)
  - Orchestration séquentielle de 8 skills avec dépendances
  - Suivi progression génération complète (contracts → tests)
  - Dépôt : [framework/CHANGELOG.md](framework/CHANGELOG.md)
- **qa v1.2.4** - Intégration task management system
  - 1 skill modifié : `qa:phpstan` (5 tâches avec boucle itérative)
  - Suivi boucle auto-fix PHPStan (max 10 itérations)
  - Tâche longue durée restant `in_progress` pendant la boucle
  - Dépôt : [qa/CHANGELOG.md](qa/CHANGELOG.md)
- **github v1.2.1** - Intégration task management system
  - 1 skill modifié : `github:fix` (6 tâches)
  - Workflow structuré résolution issue (analyse → implémentation → tests)
  - Validation qualité intégrée au workflow
  - Dépôt : [github/CHANGELOG.md](github/CHANGELOG.md)

## [2026.01.22] - 2026-01-22

### Plugins Updated
- **claude v1.1.0** - Migration commands → skills
  - 5 skills créés (alias-add, challenge, doc-load, doc-question, make-command)
  - Format natif Claude Code avec support complet frontmatter YAML
  - Remplacement "SlashCommand" → "Skill" dans toute la documentation
  - Suppression complète du répertoire /commands/
  - Dépôt : [claude/CHANGELOG.md](claude/CHANGELOG.md)
- **dev v1.9.0** - Migration 23 commands dev → skills (incluant 10 auto)
  - Préservation des 3 hooks complexes (PreToolUse/PostToolUse)
  - Support complet workaround output-style via instructions explicites
  - Dépôt : [dev/CHANGELOG.md](dev/CHANGELOG.md)
- **git v1.9.0** - Migration 4 commands git → skills
  - Préservation des hooks avancés (validation, push automatique, feedback)
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)
- **doc v1.5.0** - Migration 3 commands doc → skills
  - Dépôt : [doc/CHANGELOG.md](doc/CHANGELOG.md)
- **symfony v1.2.0** - Migration 3 commands symfony → skills
  - Dépôt : [symfony/CHANGELOG.md](symfony/CHANGELOG.md)
- **gemini v1.3.0** - Migration 3 commands gemini → skills
  - Dépôt : [gemini/CHANGELOG.md](gemini/CHANGELOG.md)
- **github v1.2.0** - Migration github:fix vers skill
  - Dépôt : [github/CHANGELOG.md](github/CHANGELOG.md)
- **marketing v1.1.0** - Migration linkedin vers skill
  - Dépôt : [marketing/CHANGELOG.md](marketing/CHANGELOG.md)
- **qa v1.1.0** - Skills elegant-objects et phpstan-resolver maintenues
  - Dépôt : [qa/CHANGELOG.md](qa/CHANGELOG.md)

## [2026.01.18] - 2026-01-18

### Plugins Updated
- **git v1.8.2** - Documentation des scripts assign_milestone et assign_project
  - Clarification de la syntaxe requise : `--milestone` et `--project` comme flags
  - Ajout d'exemples corrects/incorrects pour éviter les erreurs d'appel
  - Références croisées dans les skills `git-pr` et `git-cd-pr`
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)

## [2026.01.15] - 2026-01-15

### Plugins Updated
- **git v1.8.1** - Script de détection CD amélioré
  - Flag `--limit 1000` ajouté pour lister tous les labels (évite limite 30 par défaut)
  - Améliore fiabilité détection mode CD sur repos avec 30+ labels
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)

## [2026.01.10] - 2026-01-10

### Plugins Updated
- **marketing v1.0.2** - Correction format argument-hint
  - Conformité avec documentation officielle Claude Code
  - Dépôt : [marketing/CHANGELOG.md](marketing/CHANGELOG.md)

- **github v1.1.3** - Correction format argument-hint
  - Conformité avec documentation officielle Claude Code
  - Dépôt : [github/CHANGELOG.md](github/CHANGELOG.md)

- **git v1.8.0** - Script QA et hooks pour commandes : validation et automatisation
  - Nouveau script `qa-before-pr.sh` : détection auto outils QA (PHPStan, PHPUnit, php-cs-fixer)
  - `/git:commit` : Validation QA `--verify`, vérification workspace, push auto avec tracking intelligent
  - `/git:branch` : Blocage si modifs non commitées, validation branche source
  - `/git:pr` : Vérification branche à jour, QA avant création
  - Corrections `argument-hint` au format officiel
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)

- **dev v2.2.2** - Hooks pour commandes : validation et automatisation
  - `/dev:code` : PHPStan en temps réel après chaque Edit, auto-formatage PSR-12, validation plan existe
  - `/dev:review` : Tests automatiques avant review, suggestion commit après fixes
  - Dépôt : [dev/CHANGELOG.md](dev/CHANGELOG.md)

- **qa v1.2.2** - Correction format argument-hint
  - Conformité avec documentation officielle Claude Code
  - Dépôt : [qa/CHANGELOG.md](qa/CHANGELOG.md)

## [2026.01.08] - 2026-01-08

### Plugins Updated
- **git v1.7.7** - Documentation clarifiée pour flag `--delete`
  - Documentation explicite : `--delete` ne supprime que la branche LOCALE (jamais remote)
  - Règles critiques ajoutées dans skills `git:pr` et `git:cd-pr`
  - Commentaire renforcé dans `cleanup_branch.sh` expliquant pourquoi remote ne doit pas être supprimée
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)

## [2026.01.05] - 2026-01-05

### Plugins Updated
- **git v1.7.6** - Correction du chemin script de détection CD
  - Correction du chemin du script dans la commande `/git:pr` (chemin incorrect introduit en v1.7.5)
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)

## [2026.01.02] - 2026-01-02

### Plugins Updated
- **dev v2.2.1** - Refactorisation chemins git worktrees
  - Migration de chemins parallèles `../<repo>-<name>` vers structure standard `.worktrees/<name>`
  - Maintient tous les worktrees dans le repo (plus propre que polluer parent)
  - Découverte simplifiée (`.worktrees/` visible à la racine)
  - Suit les conventions habituelles des git worktrees
  - Dépôt : [dev/CHANGELOG.md](dev/CHANGELOG.md)

- **dev v2.2.0** - Mode automatisé complet `/dev:auto:feature`
  - 10 phases entièrement non-interactives : fetch issue → design → code → review → cleanup → PR
  - Récupération automatique spec GitHub issue
  - Détection multi-langage QA (PHP/JavaScript/Go) avec auto-fix loop (3x max)
  - Git worktree obligatoire avec cleanup automatique
  - Workflow state JSON complet avec timing détaillé
  - Rollback automatique en cas d'échec bloquant
  - Configuration `.env.claude` (MAIN_BRANCH, REPO, PROJECT)
  - Dépôt : [dev/CHANGELOG.md](dev/CHANGELOG.md)

- **git v1.7.5** - Support `.env.claude` et `--no-interaction` pour automation
  - Skills `git:pr` et `git:cd-pr` : chargement config depuis `.env.claude`
  - Support flag `--no-interaction` pour workflows automatisés
  - Lecture automatique MAIN_BRANCH, REPO, PROJECT si présents
  - Essentiel pour `/dev:auto:feature` phase création PR
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)

- **git v1.7.4** - Détection automatique du préfixe de branche
  - Commande `/git:branch` : détection intelligente du type de branche
  - Analyse prioritaire : labels GitHub → description → titre de l'issue
  - Préfixes supportés : `feature/`, `fix/`, `hotfix/`, `chore/`, `docs/`, `test/`
  - Détection automatique pour texte : analyse du préfixe explicite au début
  - Améliore la cohérence du nommage sans intervention manuelle
  - Dépôt : [git/CHANGELOG.md](git/CHANGELOG.md)

## [2025.12.31] - 2025-12-31

### Plugins Updated
- **git v1.7.3** - Détection fiable du mode CD
  - Nouveau script `detect_cd_mode.sh` : analyse TOUS les labels du repo sans troncature
  - Commande `/git:pr` utilise désormais le script dédié pour la détection du mode
  - Meilleure fiabilité avec repos ayant 20+ labels
  - Prévient les modifications ad-hoc de la commande de détection

- **git v1.7.2** - Confirmation initiale pour skills PR
  - Skills `git:pr` et `git:cd-pr` : ajout d'étape de confirmation avant exécution
  - Affichage du nom de la skill lancée avec résumé des paramètres (branche, milestone, projet, flags)
  - Demande de confirmation explicite pour valider le lancement du workflow

## [2025.12.30] - 2025-12-30

### Plugins Updated
- **git v1.7.1** - Reformulation commande commit pour fiabilité
  - Commande `/git:commit` : instructions reformatées en format impératif
  - Utilisation HEREDOC pour éviter problèmes permissions bash
  - Clarification étapes workflow pour comportement stable jour après jour

## [2025.12.28] - 2025-12-28

### Plugins Updated
- **dev v2.1.2** - Timing complet du workflow de développement
  - Enregistrement automatique des timestamps `startedAt` et `completedAt` pour chaque phase (0-7)
  - Calcul des durées en millisecondes par phase
  - Affichage formé des durées (s, m, h) à côté du statut de chaque phase
  - Récapitulatif final avec temps total de développement dans `/dev:summary`
  - Intégration timing dans `/dev:status` et `/dev:feature`
  - Format du fichier d'état étendu : `timing.totalDurationMs`

## [2025.12.27] - 2025-12-27

### Plugins Updated
- **git v1.7.0** - Refactoring architecture core + CD variant
  - Nouveau skill `git-pr-core` : centralisation du workflow PR standard
    - Scripts core partagés : `safe_push_pr.sh`, `create_pr.sh`, `final_report.sh`, etc.
    - Support assignation milestone et projet GitHub
    - Code review automatique multi-agents
    - Templates références (review et todos)
  - Nouveau skill `git-cd-pr` : workflow PR optimisé pour Continuous Delivery
    - Héritage des fonctionnalités core
    - Copie automatique des labels d'issue
    - Détection intelligente du type de version CD
    - Labels version (major/minor/patch) et feature flags automatiques
  - Architecture modulaire : skills spécialisés héritent du core pour éviter duplication
  - Permissions exécution corrigées : scripts `.sh` et `.py` maintenant exécutables

## [2025.12.26] - 2025-12-26

### Plugins Updated
- **git v1.6.0** - Labels CD + copie labels issue
  - Nouveau script `copy_issue_labels.sh` : copie automatique labels issue → PR
  - Nouveau script `apply_cd_labels.sh` : labels CD (version:major/minor/patch, 🚩 Feature flag)
    - Détection CD via présence labels `version:*`
    - Détection intelligente du type de version : breaking change, labels issue, branche, commit, fallback utilisateur
    - Detection feature flag si composant `Feature:Flag` dans fichiers Twig modifiés
    - Création automatique des labels manquants
  - Skill `git-pr` : intégration nouvelle logique dans workflow création PR

## [2025.12.20] - 2025-12-20

### Plugins Updated
- **dev v2.1.1** - Support output-style dans frontmatter
  - Ajout champ `output-style` pour formatage automatique (6 commandes)
  - Styles : `ultra-concise`, `bullet-points`, `table-based`
- **doc v1.1.3** - Support output-style dans frontmatter
  - Ajout champ `output-style` : `markdown-focused` (2 commandes)
- **gemini v1.0.1** - Support output-style dans frontmatter
  - Ajout champ `output-style` : `bullet-points` (1 commande)
- **git v1.5.0** - Script centralisé emoji + PR titles Conventional Commits
  - Nouveau script `scripts/commit-emoji.sh` : source de vérité unique pour mapping type → emoji
  - Support 16 types (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert, wip, hotfix, security, deps, breaking)
  - Skill `git-pr` : utilisation script centralisé pour titres PR
  - Titres PR au format `emoji type(scope): description` conforme aux conventions
  - Détection automatique type et scope optionnel depuis nom de branche
- **git v1.4.18** - Support output-style dans frontmatter
  - Ajout champ `output-style` : `ultra-concise`, `html-structured` (2 commandes)
- **github v1.1.2** - Support output-style dans frontmatter
  - Ajout champ `output-style` : `bullet-points` (1 commande)
- **marketing v1.0.1** - Support output-style dans frontmatter
  - Ajout champ `output-style` : `markdown-focused` (1 commande)
- **doc v1.1.2** - Réduction tokens skills
  - Skill `doc-loader` : optimisation SKILL.md (85→53 lignes)
  - Externalisation workflow dans `references/workflow-scripts.md`
- **framework v1.0.1** - Réduction tokens skills
  - Skills `make-collection`, `make-entity`, `make-out`, `make-factory`, `make-story`, `make-urls`, `make-invalide`, `make-all` : optimisées
  - Externalisation templates et exemples vers `references/usage.md`
  - Économie tokens: ~16k (72% réduction)
- **git v1.4.18** - Réoptimisation commande git:commit
  - Commande `git:commit` : meilleure organisation des options
- **git v1.4.17** - Réduction tokens skills
  - Skills `git-pr`, `release-notes` : optimisées
  - Externalisation templates vers `references/`
- **github v1.1.1** - Réduction tokens skills
  - Skill `github-impact` : optimisation SKILL.md
  - Externalisation report templates vers `references/`
- **qa v1.2.1** - Réduction tokens skills
  - Skills `elegant-objects`, `phpstan-resolver` : optimisées
  - Externalisation patterns et workflows vers `references/`
- **symfony v1.0.1** - Réduction tokens skills
  - Skill `symfony-skill` : optimisation SKILL.md (495→83 lignes)

## [2025.12.19] - 2025-12-19

### Plugins Updated
- **dev v2.0.1** - Déplacement du workflow state
  - Fichier `.dev-workflow-state.json` déplacé vers `.claude/data/.dev-workflow-state.json` (non versionné)
  - Mise à jour de toutes les instructions des phases

## [2025.12.17] - 2025-12-17

### Plugins Added
- **marketing v1.0.0** - Génération de contenu marketing
  - Commande `/linkedin` : posts LinkedIn optimisés
  - Support tone et length personnalisés

### Plugins Updated
- **dev v2.0.0** - Workflow structuré 8 phases
  - Orchestrateur `/dev:feature` avec 8 phases automatiques
  - Phases individuelles : discover, explore, clarify, design, plan, code, review, summary
  - Checkpoints utilisateur aux phases critiques
  - Fichier `.dev-workflow-state.json` pour tracking

### Plugins Added
- **review v1.0.0** - Plugin agents spécialisés code review
  - Agent `code-reviewer` : review complète (conformité CLAUDE.md, bugs, qualité code)
  - Agent `silent-failure-hunter` : détection catch vides, erreurs silencieuses
  - Agent `test-analyzer` : analyse couverture PHPUnit, tests manquants
  - Agent `git-history-reviewer` : contexte historique git (blame, PRs, TODOs)
  - Scoring 0-100 avec seuil >= 80
  - Intégration automatique avec skill `/git:pr`

- **gemini v1.0.0** - Plugin délégation Gemini CLI
  - Agent `gemini-analyzer` : analyse contextes ultra-longs (1M tokens)
  - Agent `gemini-thinker` : Deep Think pour problèmes complexes (math, logique, architecture)
  - Agent `gemini-researcher` : recherche temps réel via Google Search intégré
  - Commandes `/gemini:analyze`, `/gemini:think`, `/gemini:search`
  - Filtrage automatique fichiers sensibles, limite 4MB

### Plugins Updated
- **dev v1.3.0** - Nouvelle commande logging
  - Commande `/dev:log [FICHIER]` : ajoute `LoggableInterface` avec méthode `toLog()` aux classes PHP
  - Détection automatique objets imbriqués implémentant `LoggableInterface`
  - Annotations PHPDoc générées pour PHPStan

- **dev v1.2.0** - Migration Plan Mode natif
  - Commande `/dev:prepare` : utilise désormais Plan Mode natif Claude Code
  - Workflow interactif avec approbation utilisateur
  - Option swarm pour implémentation parallélisée
  - Suppression skill `prepare` (remplacé par Plan Mode)

- **git v1.4.16** - Intégration plugin review
  - Skill `git-pr` : délégation review au plugin `review` avec 4 agents parallèles
  - Vérification automatique présence plugin review avec message d'incitation
  - Agent `git-history-reviewer` déplacé vers plugin `review`

## [2025.11.16] - 2025-11-16

### Skills Added
- **github-impact** (`github` v1.1.0) - Skill spécialisé analyse d'impact PR
  - Analyse complète modifications (fichiers, dépendances, tests, sécurité)
  - Détection automatique templates (Twig, Blade, Vue, etc.)
  - Analyse styles (CSS, SCSS, SASS, LESS) et assets
  - Génération 2 rapports (métier + technique)
  - Intégration automatique description PR
  - Sauvegarde locale `.analysis-reports/`

- **phpstan-resolver** (`qa` v1.1.0) - Skill spécialisé résolution erreurs PHPStan
  - Boucle résolution itérative (max 10 itérations)
  - Batch processing (5 erreurs/fichier/itération)
  - Détection automatique stagnation
  - Support PHPStan format JSON
  - Rapport détaillé avec taux de succès
  - Délégation agent `@phpstan-error-resolver`

- **doc-loader** (`doc` v1.1.0) - Skill générique chargement documentation frameworks
  - Support multi-framework (Symfony, API Platform, Meilisearch, atournayre-framework, Claude Code)
  - Support multi-version (argument optionnel)
  - Cache intelligent 24h (ignore récents, supprime anciens)
  - Délégation agents scraper spécialisés
  - Anti-rate-limiting (délai 2s entre URLs)
  - Statistiques détaillées (couverture, taille, fichiers)

### Commands Updated
- **github** v1.1.0 - `/github:impact` convertie en délégation skill
- **qa** v1.1.0 - `/qa:phpstan` convertie en délégation skill
- **doc** v1.1.0 - `/doc:framework-load`, `/symfony:doc:load`, `/claude:doc:load` converties en délégation skill

### Architecture
- Pattern commande → skill pour tâches complexes orchestrées
- Réduction taille commandes (406 → 6 lignes pour github:impact)
- Meilleure séparation des responsabilités
- Task Management System (TaskCreate/TaskUpdate) pour suivi progression dans skills complexes

## [2025.11.15] - 2025-11-15

### Marketplace
- Ajout CHANGELOG.md pour tous les plugins
- Ajout CHANGELOG.md global marketplace

### Plugins Added
- **framework v1.0.0** - Plugin génération code PHP Elegant Objects
  - 9 skills pour génération automatisée (contracts, entity, out, invalide, urls, collection, factory, story, all)
  - Templates PHP pour chaque type de classe
  - Documentation complète SKILL.md + README.md

### Plugins Updated
- **git v1.4.1** - Corrections mineures
  - Stabilité commandes Git

- **git v1.4.0** - Nouvelle commande release-report
  - Commande `/git:release-report` - Génère rapports HTML d'analyse d'impact

## [2025.11.14] - Version antérieure

### Plugins Updated
- **git v1.3.0** - Documentation PR
  - Documentation arguments `/git:pr`

- **dev v1.1.0** - Nouveaux agents
  - Agent `dev:meta-agent` - Génération config agents
  - Agent `dev:phpstan-error-resolver` - Résolution erreurs PHPStan
  - Agent `dev:elegant-objects-reviewer` - Review conformité Elegant Objects

## [2025.11.01] - Version initiale

### Marketplace
- Structure initiale marketplace
- Configuration plugins système
- Documentation README globale

### Plugins Added
- **git v1.0.0** - Commandes Git workflow
  - `/git:branch`, `/git:commit`, `/git:conflit`, `/git:pr`
  - Skill `git:git-pr`

- **symfony v1.0.0** - Développement Symfony
  - Skill `symfony:symfony-skill`
  - Commandes `/symfony:make`, `/symfony:doc:load`, `/symfony:doc:question`

- **dev v1.0.0** - Développement général
  - Commandes `/dev:code`, `/dev:prepare`, `/dev:question`, `/dev:docker`
  - Agents scrapers documentation

- **qa v1.0.0** - Qualité code
  - Commande `/qa:phpstan`

- **doc v1.0.0** - Documentation
  - Commandes `/doc:adr`, `/doc:framework-load`, `/doc:rtfm`, `/doc:update`

- **github v1.0.0** - Intégration GitHub
  - Commandes `/github:fix`, `/github:impact`

- **claude v1.0.0** - Meta Claude Code
  - Commandes `/claude:alias:add`, `/claude:challenge`, `/claude:doc:load`, `/claude:make:command`

- **customize v1.0.0** - Personnalisation utilisateur
  - Plugin vide pour extensions custom

---

## Notes de version

Pour les détails complets de chaque plugin, voir les CHANGELOGs individuels:
- [claude/CHANGELOG.md](claude/CHANGELOG.md)
- [command/CHANGELOG.md](command/CHANGELOG.md)
- [customize/CHANGELOG.md](customize/CHANGELOG.md)
- [dev/CHANGELOG.md](dev/CHANGELOG.md)
- [doc/CHANGELOG.md](doc/CHANGELOG.md)
- [framework/CHANGELOG.md](framework/CHANGELOG.md)
- [gemini/CHANGELOG.md](gemini/CHANGELOG.md)
- [git/CHANGELOG.md](git/CHANGELOG.md)
- [github/CHANGELOG.md](github/CHANGELOG.md)
- [marketing/CHANGELOG.md](marketing/CHANGELOG.md)
- [mlvn/CHANGELOG.md](mlvn/CHANGELOG.md)
- [notifications/CHANGELOG.md](notifications/CHANGELOG.md)
- [prompt/CHANGELOG.md](prompt/CHANGELOG.md)
- [qa/CHANGELOG.md](qa/CHANGELOG.md)
- [review/CHANGELOG.md](review/CHANGELOG.md)
- [symfony/CHANGELOG.md](symfony/CHANGELOG.md)
