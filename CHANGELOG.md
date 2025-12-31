# Changelog - Atournayre Claude Plugin Marketplace

Toutes les modifications notables du marketplace seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [Unreleased]

### Plugins Removed
- **output-styles v1.0.0** - Supprimé (migration vers mécanisme natif `~/.claude/output-styles/`)

## [2025.12.31] - 2025-12-31

### Plugins Updated
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
- TodoWrite systématique dans skills pour suivi progression

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
- [framework/CHANGELOG.md](framework/CHANGELOG.md)
- [gemini/CHANGELOG.md](gemini/CHANGELOG.md)
- [git/CHANGELOG.md](git/CHANGELOG.md)
- [review/CHANGELOG.md](review/CHANGELOG.md)
- [symfony/CHANGELOG.md](symfony/CHANGELOG.md)
- [dev/CHANGELOG.md](dev/CHANGELOG.md)
- [qa/CHANGELOG.md](qa/CHANGELOG.md)
- [doc/CHANGELOG.md](doc/CHANGELOG.md)
- [github/CHANGELOG.md](github/CHANGELOG.md)
- [claude/CHANGELOG.md](claude/CHANGELOG.md)
- [customize/CHANGELOG.md](customize/CHANGELOG.md)
