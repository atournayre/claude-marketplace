---
title: Index des Agents
---

# Index des Agents

19 agents disponibles dans le marketplace.

**Note** : Les agents sont des sous-agents spécialisés qui peuvent être invoqués via le Task tool.

| Agent | Plugin | Description | Outils |
|-------|--------|-------------|--------|
| `action` | [utils](/plugins/utils) | Conditional action executor - performs actions only when specific conditions are met | N/A |
| `api-platform-docs-scraper` | [dev](/plugins/dev) | À utiliser de manière proactive pour extraire et sauvegarder spécifiquement la documentation API Platform dans docs/api-platform/. Spécialisé pour créer des fichiers individuels par URL sans écrasement. | WebFetch, Read, Write, MultiEdit, Grep, Glob |
| `atournayre-framework-docs-scraper` | [dev](/plugins/dev) | A utiliser de manière proactive pour extraire et sauvegarder la documentation d'atournayre-framework depuis readthedocs.io | WebFetch, Write, Read, Glob |
| `claude-docs-scraper` | [dev](/plugins/dev) | À utiliser de manière proactive pour extraire et sauvegarder spécifiquement la documentation Claude Code dans docs/claude/. Spécialisé pour créer des fichiers individuels par URL sans écrasement. | WebFetch, Read, Write, MultiEdit, Grep, Glob |
| `code-reviewer` | [review](/plugins/review) | Review de code complète pour conformité CLAUDE.md, détection de bugs, et qualité. À utiliser de manière proactive après l'écriture de code ou avant de créer une PR. Scoring 0-100 avec seuil 80. | Read, Grep, Glob, Bash |
| `elegant-objects-reviewer` | [dev](/plugins/dev) | Spécialiste pour examiner le code PHP et vérifier la conformité aux principes Elegant Objects. À utiliser de manière proactive après l'écriture de code pour garantir le respect des patterns de conception de Yegor Bugayenko. | Read, Grep, Glob, Bash |
| `explore-codebase` | [utils](/plugins/utils) | Use this agent whenever you need to explore the codebase to realize a feature. | N/A |
| `explore-docs` | [mlvn](/plugins/mlvn) | Use this agent to research library documentation and gather implementation context using Context7 MCP | N/A |
| `gemini-analyzer` | [gemini](/plugins/gemini) | Délègue l'analyse de contextes ultra-longs (codebases, docs) à Gemini 3 Pro (1M tokens). À utiliser quand le contexte dépasse les capacités de Claude ou pour analyser une codebase entière. | Bash, Read, Glob, Grep |
| `gemini-researcher` | [gemini](/plugins/gemini) | Recherche infos fraîches via Google Search intégré à Gemini. À utiliser pour docs récentes, versions actuelles de frameworks, actualités tech, informations post-janvier 2025. | Bash |
| `gemini-thinker` | [gemini](/plugins/gemini) | Délègue les problèmes complexes (math, logique, architecture) à Gemini 3 Deep Think. À utiliser pour réflexion approfondie nécessitant exploration multi-hypothèses. | Bash |
| `git-history-reviewer` | [review](/plugins/review) | Analyse le contexte historique git (blame, PRs précédentes, commentaires) pour détecter des problèmes potentiels dans les changements actuels. | Bash, Read, Grep |
| `meilisearch-docs-scraper` | [dev](/plugins/dev) | À utiliser de manière proactive pour extraire et sauvegarder spécifiquement la documentation Meilisearch dans docs/meilisearch/. Spécialisé pour créer des fichiers individuels par URL sans écrasement. | WebFetch, Read, Write, MultiEdit, Grep, Glob |
| `meta-agent` | [dev](/plugins/dev) | Génère un nouveau fichier de configuration d'agent Claude Code complet à partir de la description d'un utilisateur. Utilisez-le pour créer de nouveaux agents. À utiliser de manière proactive lorsque l'utilisateur demande de créer un nouveau sous-agent. | Write, WebFetch, mcp__firecrawl-mcp__firecrawl_scrape, mcp__firecrawl-mcp__firecrawl_search, MultiEdit |
| `phpstan-error-resolver` | [dev](/plugins/dev) | À utiliser de manière proactive pour analyser et corriger systématiquement les erreurs PHPStan niveau 9 dans les projets PHP/Symfony. Spécialiste pour résoudre les problèmes de types stricts, annotations generics, array shapes et collections Doctrine. | Read, Edit, Grep, Glob, Bash |
| `silent-failure-hunter` | [review](/plugins/review) | Détecte les erreurs silencieuses, catch vides, et gestion d'erreurs inadéquate dans le code PHP. À utiliser de manière proactive après l'écriture de code impliquant des try-catch, fallbacks, ou gestion d'erreurs. | Read, Grep, Glob, Bash |
| `symfony-docs-scraper` | [dev](/plugins/dev) | À utiliser de manière proactive pour extraire et sauvegarder spécifiquement la documentation Symfony dans docs/symfony/. Spécialisé pour créer des fichiers individuels par URL sans écrasement. | WebFetch, Read, Write, MultiEdit, Grep, Glob |
| `test-analyzer` | [review](/plugins/review) | Analyse la couverture et qualité des tests PHPUnit dans une PR. À utiliser de manière proactive avant de créer une PR pour identifier les tests manquants critiques. | Read, Grep, Glob, Bash |
| `websearch` | [mlvn](/plugins/mlvn) | Use this agent when you need to make a quick web search. | WebSearch, WebFetch |
