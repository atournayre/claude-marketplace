---
title: Index des Skills
---

# Index des Skills

78 skills disponibles dans le marketplace.

**Note** : Les skills sont invoquées via slash commands (ex: `/git:commit`, `/dev:feature`).

| Skill | Plugin | Description |
|-------|--------|-------------|
| `/apex` | [mlvn](/plugins/mlvn) | Systematic implementation using APEX methodology (Analyze-Plan-Execute-eXamine) with parallel agents, self-validation, and optional adversarial review. Use when implementing features, fixing bugs, or making code changes that benefit from structured workflow. |
| `/apex` | [mlvn](/plugins/mlvn) | Systematic implementation using APEX methodology (Analyze-Plan-Execute-Validate) with parallel agents and self-validation. Use when implementing features, fixing bugs, or making code changes that benefit from structured workflow. |
| `/claude-memory` | [claude](/plugins/claude) | Create and optimize CLAUDE.md memory files or .claude/rules/ modular rules for Claude Code projects. Comprehensive guidance on file hierarchy, content structure, path-scoped rules, best practices, and anti-patterns. Use when working with CLAUDE.md files, .claude/rules directories, setting up new projects, or improving Claude Code's context awareness. |
| `/claude:alias:add` | [claude](/plugins/claude) | Crée un alias de commande qui délègue à une autre slash command |
| `/claude:challenge` | [claude](/plugins/claude) | Évalue ma dernière réponse, donne une note sur 10 et propose des améliorations |
| `/claude:doc:load` | [claude](/plugins/claude) | Charge la documentation Claude Code depuis docs.claude.com dans des fichiers markdown locaux |
| `/claude:doc:question` | [claude](/plugins/claude) | Interroger la documentation Claude Code locale pour répondre à une question |
| `/commit` | [mlvn](/plugins/mlvn) | Quick commit and push with minimal, clean messages |
| `/create-pr` | [mlvn](/plugins/mlvn) | Create and push PR with auto-generated title and description |
| `/dev:auto:check-prerequisites` | [dev](/plugins/dev) | Vérifier tous les prérequis - Mode AUTO (Phase -1) |
| `/dev:auto:clarify` | [dev](/plugins/dev) | Lever ambiguités avec heuristiques automatiques (Phase 3) |
| `/dev:auto:code` | [dev](/plugins/dev) | Implémenter selon le plan - Mode AUTO (Phase 6) |
| `/dev:auto:design` | [dev](/plugins/dev) | Choisir architecture automatiquement (Phase 4) |
| `/dev:auto:discover` | [dev](/plugins/dev) | Comprendre le besoin avant développement - Mode AUTO (Phase 0) |
| `/dev:auto:explore` | [dev](/plugins/dev) | Explorer le codebase automatiquement - Mode AUTO (Phase 2) |
| `/dev:auto:feature` | [dev](/plugins/dev) | Workflow complet de développement automatisé (mode non-interactif) |
| `/dev:auto:fetch-issue` | [dev](/plugins/dev) | Récupérer le contenu d'une issue GitHub - Mode AUTO (Phase 0) |
| `/dev:auto:plan` | [dev](/plugins/dev) | Générer plan d'implémentation automatiquement - Mode AUTO (Phase 5) |
| `/dev:auto:review` | [dev](/plugins/dev) | Review avec auto-fix automatique - Mode AUTO (Phase 7) |
| `/dev:clarify` | [dev](/plugins/dev) | Poser questions pour lever ambiguités (Phase 2) |
| `/dev:code` | [dev](/plugins/dev) | Implémenter selon le plan (Phase 5) |
| `/dev:debug` | [dev](/plugins/dev) | Analyser et résoudre une erreur (message simple ou stack trace) |
| `/dev:design` | [dev](/plugins/dev) | Designer 2-3 approches architecturales (Phase 3) |
| `/dev:discover` | [dev](/plugins/dev) | Comprendre le besoin avant développement (Phase 0) |
| `/dev:explore` | [dev](/plugins/dev) | Explorer le codebase avec agents parallèles (Phase 1) |
| `/dev:feature` | [dev](/plugins/dev) | Workflow complet de développement de feature |
| `/dev:log` | [dev](/plugins/dev) | Ajoute des fonctionnalités de log au fichier en cours |
| `/dev:plan` | [dev](/plugins/dev) | Générer plan d'implémentation dans docs/specs/ (Phase 4) |
| `/dev:review` | [dev](/plugins/dev) | Review qualité complète - PHPStan + Elegant Objects + code review (Phase 6) |
| `/dev:status` | [dev](/plugins/dev) | Affiche le workflow et l'étape courante |
| `/dev:summary` | [dev](/plugins/dev) | Résumé de ce qui a été construit (Phase 7) |
| `/dev:worktree` | [dev](/plugins/dev) | Gestion des git worktrees pour développement parallèle |
| `/doc-loader` | [doc](/plugins/doc) | > |
| `/doc:adr` | [doc](/plugins/doc) | Génère un Architecture Decision Record (ADR) formaté et structuré |
| `/doc:rtfm` | [doc](/plugins/doc) | Lit la documentation technique - RTFM (Read The Fucking Manual) |
| `/doc:update` | [doc](/plugins/doc) | Crées la documentation pour la fonctionnalité en cours. Mets à jour le readme global du projet si nécessaire. Lie les documents entre eux pour ne pas avoir de documentation orpheline. La documentation est générée dans les répertoire de documentation du projet. |
| `/elegant-objects` | [qa](/plugins/qa) | > |
| `/fix-errors` | [mlvn](/plugins/mlvn) | Fix all ESLint and TypeScript errors with parallel processing using snipper agents |
| `/fix-grammar` | [utils](/plugins/utils) | Fix grammar and spelling errors in one or multiple files while preserving formatting |
| `/fix-pr-comments` | [git](/plugins/git) | Fetch PR review comments and implement all requested changes |
| `/framework:make:all` | [framework](/plugins/framework) | Génère tous les fichiers pour une entité complète (orchestrateur) |
| `/framework:make:collection` | [framework](/plugins/framework) | Génère classe Collection typée avec traits Atournayre |
| `/framework:make:contracts` | [framework](/plugins/framework) | Génère les interfaces de contrats pour une architecture Elegant Objects |
| `/framework:make:entity` | [framework](/plugins/framework) | Génère une entité Doctrine avec repository selon principes Elegant Objects |
| `/framework:make:factory` | [framework](/plugins/framework) | Génère Factory Foundry pour tests |
| `/framework:make:invalide` | [framework](/plugins/framework) | Génère classe Invalide (exceptions métier) |
| `/framework:make:out` | [framework](/plugins/framework) | Génère classe Out (DTO immuable pour output) |
| `/framework:make:story` | [framework](/plugins/framework) | Génère Story Foundry pour fixtures de tests |
| `/framework:make:urls` | [framework](/plugins/framework) | Génère classe Urls + Message CQRS + Handler |
| `/gemini:analyze` | [gemini](/plugins/gemini) | Analyse une codebase ou documentation avec Gemini (1M tokens) |
| `/gemini:search` | [gemini](/plugins/gemini) | Recherche temps réel via Google Search intégré à Gemini |
| `/gemini:think` | [gemini](/plugins/gemini) | Délègue un problème complexe à Gemini Deep Think |
| `/gen-release-notes` | [git](/plugins/git) | > |
| `/git-cd-pr` | [git](/plugins/git) | > |
| `/git-pr` | [git](/plugins/git) | > |
| `/git-pr-core` | [git](/plugins/git) | > |
| `/git:branch` | [git](/plugins/git) | Création de branche Git avec workflow structuré |
| `/git:commit` | [git](/plugins/git) | Créer des commits bien formatés avec format conventional et emoji |
| `/git:conflit` | [git](/plugins/git) | Analyse les conflits git et propose à l'utilisateur une résolution pas à pas avec validation de chaque étape. |
| `/git:release-report` | [git](/plugins/git) | Génère un rapport HTML d'analyse d'impact entre deux branches |
| `/github-impact` | [github](/plugins/github) | > |
| `/github:fix` | [github](/plugins/github) | Corriger une issue GitHub avec workflow simplifié et efficace |
| `/marketing:linkedin` | [marketing](/plugins/marketing) | Génère un post LinkedIn attractif basé sur les dernières modifications du marketplace |
| `/merge` | [mlvn](/plugins/mlvn) | Intelligently merge branches with context-aware conflict resolution |
| `/oneshot` | [dev](/plugins/dev) | Ultra-fast feature implementation using Explore → Code → Test workflow. Use when implementing focused features, single tasks, or when speed over completeness is priority. |
| `/phpstan-resolver` | [qa](/plugins/qa) | > |
| `/prompt-creator` | [mlvn](/plugins/mlvn) | Expert prompt engineering for creating effective prompts for Claude, GPT, and other LLMs. Use when writing system prompts, user prompts, few-shot examples, or optimizing existing prompts for better performance. |
| `/prompt:start` | [prompt](/plugins/prompt) | Démarre un développement avec un starter léger puis active le mode plan |
| `/prompt:transform` | [prompt](/plugins/prompt) | Transforme un prompt en prompt exécutable compatible avec le Task Management System (TaskCreate/TaskUpdate/TaskList) |
| `/prompt:validate` | [prompt](/plugins/prompt) | Vérifie la checklist avant exécution et liste les oublis |
| `/setup-ralph` | [dev](/plugins/dev) | Setup the Ralph autonomous AI coding loop - ships features while you sleep |
| `/skill-creator` | [claude](/plugins/claude) | This skill should be used when the user asks to "create a skill", "build a skill", "write a skill", "improve skill structure", "understand skill creation", or mentions SKILL.md files, skill development, progressive disclosure, XML structure, or bundled resources (scripts, references, assets). Comprehensive guide for creating effective Claude Code skills. |
| `/skill-workflow-creator` | [claude](/plugins/claude) | Expert guidance for creating, building, and using Claude Code subagents and the Task tool. Use when working with subagents, setting up agent configurations, understanding how agents work, or using the Task tool to launch specialized agents. |
| `/symfony-framework` | [symfony](/plugins/symfony) | Comprehensive Symfony 6.4 development skill for web applications, APIs, and microservices. |
| `/symfony:doc:load` | [symfony](/plugins/symfony) | Charge la documentation Symfony depuis son site web dans des fichiers markdown locaux |
| `/symfony:doc:question` | [symfony](/plugins/symfony) | Interroger la documentation Symfony locale pour répondre à une question |
| `/symfony:make` | [symfony](/plugins/symfony) | Cherche si il existe un maker Symfony pour faire la tache demandée et l'utilise si il existe. Si aucun maker n'existe alors utilise la slash command "/prepare |
| `/ui-test` | [chrome-ui-test](/plugins/chrome-ui-test) | > |
