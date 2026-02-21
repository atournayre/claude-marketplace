---
title: Index des Skills
---

# Index des Skills

150 skills disponibles dans le marketplace.

**Note** : Les skills sont invoquées via slash commands (ex: `/git:commit`, `/dev:feature`). ⚠️ = plugin déprécié.

| Skill | Plugin | Description |
|-------|--------|-------------|
| `/analyst:clarify` | [analyst](/plugins/analyst) | Lever les ambiguïtés avant design - Phase 2 (mode interactif ou heuristiques automatiques) |
| `/analyst:discover` | [analyst](/plugins/analyst) | Comprendre le besoin avant développement - Phase 0 (supporte le mode automatique) |
| `/analyst:explore` | [analyst](/plugins/analyst) | Explorer le codebase avec agents parallèles - Phase 1 (supporte le mode automatique) |
| `/analyst:impact` | [analyst](/plugins/analyst) | Génère automatiquement deux rapports d'impact (métier et technique) pour une PR GitHub et les intègre dans la description |
| `/apex` | [mlvn](/plugins/mlvn) ⚠️ | Systematic implementation using APEX methodology (Analyze-Plan-Execute-eXamine) with parallel agents, self-validation, and optional adversarial review. Use when implementing features, fixing bugs, or making code changes that benefit from structured workflow. |
| `/apex` | [mlvn](/plugins/mlvn) ⚠️ | Systematic implementation using APEX methodology (Analyze-Plan-Execute-Validate) with parallel agents and self-validation. Use when implementing features, fixing bugs, or making code changes that benefit from structured workflow. |
| `/architect:adr` | [architect](/plugins/architect) | Génère un Architecture Decision Record (ADR) formaté et structuré |
| `/architect:design` | [architect](/plugins/architect) | Designer des approches architecturales et choisir la meilleure - Phase 3 (supporte le mode automatique) |
| `/architect:plan` | [architect](/plugins/architect) | Générer plan d'implémentation détaillé dans docs/specs/ - Phase 4 (supporte le mode automatique) |
| `/architect:start` | [architect](/plugins/architect) | Démarre un développement avec un starter léger puis active le mode plan |
| `/bump` | marketplace | Automatise les mises à jour de version des plugins avec détection automatique du type de version |
| `/claude-memory` | [claude](/plugins/claude) ⚠️ | Create and optimize CLAUDE.md memory files or .claude/rules/ modular rules for Claude Code projects. Comprehensive guidance on file hierarchy, content structure, path-scoped rules, best practices, and anti-patterns. Use when working with CLAUDE.md files, .claude/rules directories, setting up new projects, or improving Claude Code's context awareness. |
| `/claude:alias:add` | [claude](/plugins/claude) ⚠️ | Crée un alias de commande qui délègue à une autre slash command |
| `/claude:challenge` | [claude](/plugins/claude) ⚠️ | Évalue ma dernière réponse, donne une note sur 10 et propose des améliorations |
| `/claude:doc:load` | [claude](/plugins/claude) ⚠️ | Charge la documentation Claude Code depuis docs.claude.com dans des fichiers markdown locaux |
| `/claude:doc:question` | [claude](/plugins/claude) ⚠️ | Interroger la documentation Claude Code locale pour répondre à une question |
| `/commit` | [mlvn](/plugins/mlvn) ⚠️ | Quick commit and push with minimal, clean messages |
| `/create-pr` | [mlvn](/plugins/mlvn) ⚠️ | Create and push PR with auto-generated title and description |
| `/dev:auto:check-prerequisites` | [dev](/plugins/dev) ⚠️ | Vérifier tous les prérequis - Mode AUTO (Phase -1) |
| `/dev:auto:clarify` | [dev](/plugins/dev) ⚠️ | Lever ambiguités avec heuristiques automatiques (Phase 3) |
| `/dev:auto:code` | [dev](/plugins/dev) ⚠️ | Implémenter selon le plan - Mode AUTO (Phase 6) |
| `/dev:auto:design` | [dev](/plugins/dev) ⚠️ | Choisir architecture automatiquement (Phase 4) |
| `/dev:auto:discover` | [dev](/plugins/dev) ⚠️ | Comprendre le besoin avant développement - Mode AUTO (Phase 0) |
| `/dev:auto:explore` | [dev](/plugins/dev) ⚠️ | Explorer le codebase automatiquement - Mode AUTO (Phase 2) |
| `/dev:auto:feature` | [dev](/plugins/dev) ⚠️ | Workflow complet de développement automatisé (mode non-interactif) |
| `/dev:auto:fetch-issue` | [dev](/plugins/dev) ⚠️ | Récupérer le contenu d'une issue GitHub - Mode AUTO (Phase 0) |
| `/dev:auto:plan` | [dev](/plugins/dev) ⚠️ | Générer plan d'implémentation automatiquement - Mode AUTO (Phase 5) |
| `/dev:auto:review` | [dev](/plugins/dev) ⚠️ | Review avec auto-fix automatique - Mode AUTO (Phase 7) |
| `/dev:clarify` | [dev](/plugins/dev) ⚠️ | Poser questions pour lever ambiguités (Phase 2) |
| `/dev:code` | [dev](/plugins/dev) ⚠️ | Implémenter selon le plan (Phase 5) |
| `/dev:debug` | [dev](/plugins/dev) ⚠️ | Analyser et résoudre une erreur (message simple ou stack trace) |
| `/dev:design` | [dev](/plugins/dev) ⚠️ | Designer 2-3 approches architecturales (Phase 3) |
| `/dev:discover` | [dev](/plugins/dev) ⚠️ | Comprendre le besoin avant développement (Phase 0) |
| `/dev:explore` | [dev](/plugins/dev) ⚠️ | Explorer le codebase avec agents parallèles (Phase 1) |
| `/dev:feature` | [dev](/plugins/dev) ⚠️ | Workflow complet de développement de feature |
| `/dev:implement` | [dev](/plugins/dev) ⚠️ | Force l'implémentation complète d'une feature (pas juste planification) |
| `/dev:log` | [dev](/plugins/dev) ⚠️ | Ajoute des fonctionnalités de log au fichier en cours |
| `/dev:parallel-implement` | [dev](/plugins/dev) ⚠️ | Implémentation parallèle de N issues via worktrees isolés |
| `/dev:plan` | [dev](/plugins/dev) ⚠️ | Générer plan d'implémentation dans docs/specs/ (Phase 4) |
| `/dev:refactor-safe` | [dev](/plugins/dev) ⚠️ | Refactoring autonome piloté par tests — boucle refactor/test/ajust |
| `/dev:review` | [dev](/plugins/dev) ⚠️ | Review qualité complète - PHPStan + Elegant Objects + code review (Phase 6) |
| `/dev:status` | [dev](/plugins/dev) ⚠️ | Affiche le workflow et l'étape courante |
| `/dev:summary` | [dev](/plugins/dev) ⚠️ | Résumé de ce qui a été construit (Phase 7) |
| `/dev:worktree` | [dev](/plugins/dev) ⚠️ | Gestion des git worktrees pour développement parallèle |
| `/devops:branch` | [devops](/plugins/devops) | Création de branche Git avec workflow structuré |
| `/devops:cd-pr` | [devops](/plugins/devops) | > |
| `/devops:ci-autofix` | [devops](/plugins/devops) | Parse les logs CI et corrige automatiquement les erreurs |
| `/devops:commit` | [devops](/plugins/devops) | Créer des commits bien formatés avec format conventional et emoji |
| `/devops:conflict` | [devops](/plugins/devops) | Analyse les conflits git et propose à l'utilisateur une résolution pas à pas avec validation de chaque étape. |
| `/devops:pr` | [devops](/plugins/devops) | > |
| `/devops:release-notes` | [devops](/plugins/devops) | > |
| `/devops:release-report` | [devops](/plugins/devops) | Génère un rapport HTML d'analyse d'impact entre deux branches |
| `/devops:worktree` | [devops](/plugins/devops) | Gestion des git worktrees pour développement parallèle (création, liste, suppression, statut, switch) |
| `/doc-loader` | [doc](/plugins/doc) | > |
| `/doc:adr` | [doc](/plugins/doc) | Génère un Architecture Decision Record (ADR) formaté et structuré |
| `/doc:rtfm` | [doc](/plugins/doc) | Lit la documentation technique - RTFM (Read The Fucking Manual) |
| `/doc:update` | [doc](/plugins/doc) | Crées la documentation pour la fonctionnalité en cours. Mets à jour le readme global du projet si nécessaire. Lie les documents entre eux pour ne pas avoir de documentation orpheline. La documentation est générée dans les répertoire de documentation du projet. |
| `/documenter:claude-load` | [documenter](/plugins/documenter) | Charge la documentation Claude Code depuis docs.claude.com dans des fichiers markdown locaux |
| `/documenter:claude-question` | [documenter](/plugins/documenter) | Interroger la documentation Claude Code locale pour répondre à une question |
| `/documenter:load` | [documenter](/plugins/documenter) | > |
| `/documenter:rtfm` | [documenter](/plugins/documenter) | Lit la documentation technique - RTFM (Read The Fucking Manual) |
| `/documenter:summary` | [documenter](/plugins/documenter) | Résumé de ce qui a été construit (Phase 7 du workflow de développement) |
| `/documenter:update` | [documenter](/plugins/documenter) | Crées la documentation pour la fonctionnalité en cours. Mets à jour le readme global du projet si nécessaire. Lie les documents entre eux pour ne pas avoir de documentation orpheline. La documentation est générée dans les répertoire de documentation du projet. |
| `/elegant-objects` | [qa](/plugins/qa) ⚠️ | > |
| `/fix-errors` | [mlvn](/plugins/mlvn) ⚠️ | Fix all ESLint and TypeScript errors with parallel processing using snipper agents |
| `/fix-grammar` | [utils](/plugins/utils) ⚠️ | Fix grammar and spelling errors in one or multiple files while preserving formatting |
| `/fix-pr-comments` | [git](/plugins/git) ⚠️ | Fetch PR review comments and implement all requested changes |
| `/framework:make:all` | [framework](/plugins/framework) ⚠️ | Génère tous les fichiers pour une entité complète (orchestrateur) |
| `/framework:make:collection` | [framework](/plugins/framework) ⚠️ | Génère classe Collection typée avec traits Atournayre |
| `/framework:make:contracts` | [framework](/plugins/framework) ⚠️ | Génère les interfaces de contrats pour une architecture Elegant Objects |
| `/framework:make:entity` | [framework](/plugins/framework) ⚠️ | Génère une entité Doctrine avec repository selon principes Elegant Objects |
| `/framework:make:factory` | [framework](/plugins/framework) ⚠️ | Génère Factory Foundry pour tests |
| `/framework:make:invalide` | [framework](/plugins/framework) ⚠️ | Génère classe Invalide (exceptions métier) |
| `/framework:make:out` | [framework](/plugins/framework) ⚠️ | Génère classe Out (DTO immuable pour output) |
| `/framework:make:story` | [framework](/plugins/framework) ⚠️ | Génère Story Foundry pour fixtures de tests |
| `/framework:make:urls` | [framework](/plugins/framework) ⚠️ | Génère classe Urls + Message CQRS + Handler |
| `/gemini:analyze` | [gemini](/plugins/gemini) ⚠️ | Analyse une codebase ou documentation avec Gemini (1M tokens) |
| `/gemini:search` | [gemini](/plugins/gemini) ⚠️ | Recherche temps réel via Google Search intégré à Gemini |
| `/gemini:think` | [gemini](/plugins/gemini) ⚠️ | Délègue un problème complexe à Gemini Deep Think |
| `/gen-release-notes` | [git](/plugins/git) ⚠️ | > |
| `/git-branch-core` | [git](/plugins/git) ⚠️ | > |
| `/git-cd-pr` | [git](/plugins/git) ⚠️ | > |
| `/git-pr` | [git](/plugins/git) ⚠️ | > |
| `/git-pr-core` | [git](/plugins/git) ⚠️ | > |
| `/git:branch` | [git](/plugins/git) ⚠️ | Création de branche Git avec workflow structuré |
| `/git:ci-autofix` | [git](/plugins/git) ⚠️ | Parse les logs CI et corrige automatiquement les erreurs |
| `/git:commit` | [git](/plugins/git) ⚠️ | Créer des commits bien formatés avec format conventional et emoji |
| `/git:conflit` | [git](/plugins/git) ⚠️ | Analyse les conflits git et propose à l'utilisateur une résolution pas à pas avec validation de chaque étape. |
| `/git:release-report` | [git](/plugins/git) ⚠️ | Génère un rapport HTML d'analyse d'impact entre deux branches |
| `/git:worktree` | [git](/plugins/git) ⚠️ | Création de worktree Git avec workflow structuré |
| `/github-impact` | [github](/plugins/github) ⚠️ | > |
| `/github:fix` | [github](/plugins/github) ⚠️ | Corriger une issue GitHub avec workflow simplifié et efficace |
| `/implementer:code` | [implementer](/plugins/implementer) | Implémenter selon le plan — avec ou sans approbation préalable |
| `/implementer:debug` | [implementer](/plugins/implementer) | Analyser et résoudre une erreur (message simple ou stack trace) |
| `/implementer:fix-issue` | [implementer](/plugins/implementer) | Corriger une issue GitHub avec workflow structuré et efficace |
| `/implementer:fix-pr-comments` | [implementer](/plugins/implementer) | Récupérer les commentaires de review PR et implémenter tous les changements demandés |
| `/implementer:implement` | [implementer](/plugins/implementer) | Forcer l'implémentation complète d'une feature (pas juste planification) |
| `/implementer:log` | [implementer](/plugins/implementer) | Ajouter LoggableInterface à une classe PHP |
| `/implementer:oneshot` | [implementer](/plugins/implementer) | Implémentation ultra-rapide d'une feature ciblée — Explore, Code, Test |
| `/implementer:refactor` | [implementer](/plugins/implementer) | Refactoring autonome piloté par les tests — boucle refactor/test/ajust |
| `/infra:alias-add` | [infra](/plugins/infra) | Crée un alias de slash command qui délègue à une autre slash command existante. Valide les arguments, crée le fichier d'alias, et met à jour la documentation. |
| `/infra:bump` | [infra](/plugins/infra) | Automatise les mises à jour de version des plugins avec détection automatique du type (PATCH ou MINOR). Met à jour plugin.json, CHANGELOG, README du plugin, README global, CHANGELOG global, marketplace.json, template PR et documentation VitePress. |
| `/infra:fix-grammar` | [infra](/plugins/infra) | Corrige les fautes de grammaire et d'orthographe dans un ou plusieurs fichiers en préservant le formatage, la structure et les termes techniques. Traitement parallèle pour plusieurs fichiers. |
| `/infra:init` | [infra](/plugins/infra) | Initialise le marketplace et vérifie toutes les dépendances nécessaires aux plugins (git, gh, node, npm, bun). Génère un rapport avec les dépendances installées/manquantes et les commandes d'installation. |
| `/infra:make-subagent` | [infra](/plugins/infra) | Guide expert pour créer et configurer des sous-agents Claude Code spécialisés. Couvre la structure des fichiers agent, le frontmatter, les prompts système, les outils, les modes background et les patterns d'orchestration. Utiliser pour créer de nouveaux agents ou configurer des workflows multi-agents. |
| `/infra:memory` | [infra](/plugins/infra) | Crée et optimise les fichiers de mémoire Claude Code (CLAUDE.md ou .claude/rules/). Couvre la hiérarchie de fichiers, la structure du contenu, les règles path-scoped, les bonnes pratiques et les anti-patterns. Utiliser pour CLAUDE.md, .claude/rules/, nouveaux projets, ou améliorer la conscience contextuelle. |
| `/infra:skill-creator` | [infra](/plugins/infra) | Guide expert pour créer des skills Claude Code efficaces. Couvre la structure SKILL.md, le frontmatter, les ressources bundlées (scripts, references, assets), la progressive disclosure et les bonnes pratiques. Utiliser quand l'utilisateur demande de créer ou améliorer un skill. |
| `/init-marketplace` | marketplace | Initialise le marketplace et vérifie toutes les dépendances nécessaires aux plugins |
| `/marketing:linkedin` | [marketing](/plugins/marketing) | Génère un post LinkedIn attractif basé sur les dernières modifications du marketplace |
| `/merge` | [mlvn](/plugins/mlvn) ⚠️ | Intelligently merge branches with context-aware conflict resolution |
| `/oneshot` | [dev](/plugins/dev) ⚠️ | Ultra-fast feature implementation using Explore → Code → Test workflow. Use when implementing focused features, single tasks, or when speed over completeness is priority. |
| `/orchestrator:check-prerequisites` | [orchestrator](/plugins/orchestrator) | Vérifie tous les prérequis système avant de lancer un workflow automatique (gh CLI, jq, git). Exit code 1 si un prérequis manque. |
| `/orchestrator:feature` | [orchestrator](/plugins/orchestrator) | Workflow complet de développement de feature. Mode interactif (description texte) avec 8 phases et checkpoints utilisateur. Mode automatique (numéro issue GitHub) avec 10 phases sans interaction. Utilise worktrees, task management et agents spécialisés. |
| `/orchestrator:fetch-issue` | [orchestrator](/plugins/orchestrator) | Récupère et valide le contenu d'une issue GitHub pour le workflow automatique. Vérifie que l'issue est OPEN et a une description non vide. |
| `/orchestrator:parallel` | [orchestrator](/plugins/orchestrator) | Implémentation parallèle de N issues GitHub via worktrees isolés. Chaque issue est traitée par un agent indépendant. Max 3 agents simultanés. |
| `/orchestrator:ralph` | [orchestrator](/plugins/orchestrator) | Setup du loop autonome de développement Ralph. Crée la structure .claude/ralph/, génère le PRD interactivement ou pour une feature spécifique, et affiche la commande à exécuter. NE lance jamais ralph.sh automatiquement. |
| `/orchestrator:status` | [orchestrator](/plugins/orchestrator) | Affiche l'état actuel du workflow de développement (phases complétées, en cours, à faire) avec timings depuis le fichier d'état. |
| `/orchestrator:team` | [orchestrator](/plugins/orchestrator) | Orchestre une équipe d'agents spécialisés pour les tâches complexes. Auto-détecte le type (feature/refactor/api/fix), compose l'équipe, coordonne les phases analyse -> challenge -> implémentation -> QA. |
| `/orchestrator:transform` | [orchestrator](/plugins/orchestrator) | Transforme un prompt quelconque (texte libre ou fichier) en prompt exécutable structuré avec TaskCreate/TaskUpdate/TaskList. Génère un fichier .claude/prompts/executable-{name}-{timestamp}.md |
| `/orchestrator:validate` | [orchestrator](/plugins/orchestrator) | Vérifie la checklist (PHP, API ou sécurité) avant exécution. Effectue les vérifications automatiques (PHPStan, PSR-12, tests, Elegant Objects, sécurité) et liste les points à vérifier manuellement. |
| `/php:make-all` | [php](/plugins/php) | Génère tous les fichiers pour une entité complète (orchestrateur) |
| `/php:make-collection` | [php](/plugins/php) | Génère classe Collection typée avec traits Atournayre |
| `/php:make-contracts` | [php](/plugins/php) | Génère les interfaces de contrats pour une architecture Elegant Objects |
| `/php:make-entity` | [php](/plugins/php) | Génère une entité Doctrine avec repository selon principes Elegant Objects |
| `/php:make-factory` | [php](/plugins/php) | Génère Factory Foundry pour tests |
| `/php:make-invalide` | [php](/plugins/php) | Génère classe Invalide (exceptions métier) |
| `/php:make-out` | [php](/plugins/php) | Génère classe Out (DTO immuable pour output) |
| `/php:make-story` | [php](/plugins/php) | Génère Story Foundry pour fixtures de tests |
| `/php:make-urls` | [php](/plugins/php) | Génère classe Urls + Message CQRS + Handler |
| `/phpstan-resolver` | [qa](/plugins/qa) ⚠️ | > |
| `/prompt-creator` | [mlvn](/plugins/mlvn) ⚠️ | Expert prompt engineering for creating effective prompts for Claude, GPT, and other LLMs. Use when writing system prompts, user prompts, few-shot examples, or optimizing existing prompts for better performance. |
| `/prompt:start` | [prompt](/plugins/prompt) ⚠️ | Démarre un développement avec un starter léger puis active le mode plan |
| `/prompt:team` | [prompt](/plugins/prompt) ⚠️ | Orchestre une équipe d'agents spécialisés pour les tâches complexes. Auto-détecte le type, compose l'équipe, coordonne les phases analyse → challenge → implémentation → QA. |
| `/prompt:transform` | [prompt](/plugins/prompt) ⚠️ | Transforme un prompt en prompt exécutable compatible avec le Task Management System (TaskCreate/TaskUpdate/TaskList) |
| `/prompt:validate` | [prompt](/plugins/prompt) ⚠️ | Vérifie la checklist avant exécution et liste les oublis |
| `/researcher:analyze` | [researcher](/plugins/researcher) | Analyse une codebase ou documentation avec Gemini (1M tokens) |
| `/researcher:search` | [researcher](/plugins/researcher) | Recherche temps réel via Google Search intégré à Gemini |
| `/reviewer:challenge` | [reviewer](/plugins/reviewer) | Évaluer la dernière réponse Claude, donner une note sur 10 et proposer des améliorations |
| `/reviewer:elegant-objects` | [reviewer](/plugins/reviewer) | Vérifier la conformité du code PHP aux principes Elegant Objects de Yegor Bugayenko |
| `/reviewer:phpstan` | [reviewer](/plugins/reviewer) | Résoudre automatiquement les erreurs PHPStan niveau 9 — boucle jusqu'à zéro erreur |
| `/reviewer:review` | [reviewer](/plugins/reviewer) | Review qualité complète — PHPStan + Elegant Objects + code review + adversarial |
| `/setup-ralph` | [dev](/plugins/dev) ⚠️ | Setup the Ralph autonomous AI coding loop - ships features while you sleep |
| `/skill-creator` | [claude](/plugins/claude) ⚠️ | This skill should be used when the user asks to "create a skill", "build a skill", "write a skill", "improve skill structure", "understand skill creation", or mentions SKILL.md files, skill development, progressive disclosure, XML structure, or bundled resources (scripts, references, assets). Comprehensive guide for creating effective Claude Code skills. |
| `/skill-workflow-creator` | [claude](/plugins/claude) ⚠️ | Expert guidance for creating, building, and using Claude Code subagents and the Task tool. Use when working with subagents, setting up agent configurations, understanding how agents work, or using the Task tool to launch specialized agents. |
| `/symfony-framework` | [symfony](/plugins/symfony) | Comprehensive Symfony 6.4 development skill for web applications, APIs, and microservices. |
| `/symfony:doc:load` | [symfony](/plugins/symfony) | Charge la documentation Symfony depuis son site web dans des fichiers markdown locaux |
| `/symfony:doc:question` | [symfony](/plugins/symfony) | Interroger la documentation Symfony locale pour répondre à une question |
| `/symfony:make` | [symfony](/plugins/symfony) | Cherche si il existe un maker Symfony pour faire la tache demandée et l'utilise si il existe. Si aucun maker n'existe alors utilise la slash command "/prepare |
| `/tester:ui-test` | [tester](/plugins/tester) | > |
| `/ui-test` | [chrome-ui-test](/plugins/chrome-ui-test) ⚠️ | > |
