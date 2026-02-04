---
title: "claude"
description: "Plugin de base pour Claude Code avec commandes essentielles pour l'amélioration et la documentation"
version: "1.3.1"
---

# claude <Badge type="info" text="v1.3.1" />


Plugin de base pour Claude Code avec commandes essentielles pour l'amélioration et la documentation.

## Installation

```bash
/plugin install claude@atournayre
```

## Skills Disponibles

Le plugin claude fournit 7 skills (format natif Claude Code) :

### `/claude:challenge`

Évalue ta dernière réponse, donne une note sur 10 et propose des améliorations.

**Critères d'évaluation :**
- Pertinence
- Clarté
- Complétude
- Précision
- Format et style

**Usage :**
```bash
/claude:challenge
```

**Exemple de rapport :**
```
📊 Évaluation de ma dernière réponse

Note globale : 7/10

Points forts :
- Réponse directe et concise
- Format en listes à puces

Axes d'amélioration :
- Ajouter des exemples de code
- Préciser les limitations
```

---

### `/skill-creator` ⭐ NOUVEAU

Créateur de skills Claude Code complet avec progressive disclosure, bundled resources et scripts d'automatisation.

**Supérieur à make-command :**
- ✅ 6 fichiers références (progressive disclosure, workflows, examples, patterns, XML guide, output patterns)
- ✅ 3 scripts TypeScript (init-skill.ts, package-skill.ts, validate.ts)
- ✅ Bundled resources (scripts/, references/, assets/)
- ✅ Progressive disclosure pattern (docs chargées à la demande)
- ✅ Basé sur doc officielle https://code.claude.com/docs/llms.txt

**Usage :**
```bash
# Créer un nouveau skill
/skill-creator

# Comprendre la structure d'un skill
/skill-creator "explain skill anatomy"

# Améliorer un skill existant
/skill-creator "improve my-skill progressive disclosure"
```

**Génère automatiquement :**
- SKILL.md avec frontmatter YAML complet
- Structure références/ pour progressive disclosure
- Scripts d'automatisation si nécessaires
- Documentation complète avec exemples

---

### `/memory`

Gestion intelligente de CLAUDE.md avec 4-level hierarchy et path-scoped memory.

**Hiérarchie 4 niveaux :**
1. **Global** : `~/.claude/CLAUDE.md` (tous les projets)
2. **Workspace** : `.claude/CLAUDE.md` (projet courant)
3. **Package** : `package/.claude/CLAUDE.md` (package spécifique)
4. **Directory** : `.claude/CLAUDE.md` dans sous-dossiers (contexte local)

**Usage :**
```bash
# Créer/mettre à jour memory
/memory "remember: use PSR-12 for PHP formatting"

# Memory scopée au package
/memory "for package auth: use JWT tokens" --scope=package

# Memory directory-specific
/memory "for this component: always validate input" --scope=directory
```

**Features :**
- Path-scoped memory (workspace, package, directory)
- Fusion automatique des niveaux (global → workspace → package → directory)
- Patterns de projet (monorepo, microservices, etc.)
- Techniques de prompting intégrées

---

### `/make-subagent`

Créateur de subagents Claude Code avec configuration YAML, tool restrictions et orchestration patterns.

**Usage :**
```bash
# Créer un subagent
/make-subagent "security-reviewer" "Review code for security issues"

# Subagent avec tools restreints
/make-subagent "file-explorer" "Explore codebase" --tools=Read,Glob,Grep

# Subagent avec contexte spécifique
/make-subagent "test-runner" "Run and analyze tests" --context=testing
```

**Génère automatiquement :**
- Fichier YAML de configuration (.claude/agents/)
- Tool restrictions appropriées
- Context management patterns
- Error handling et recovery
- Orchestration patterns (pipeline, parallel, conditional)

**Features :**
- 7 fichiers références (orchestration, debugging, error handling, etc.)
- Patterns d'orchestration (sequential, parallel, conditional, retry)
- Gestion du contexte et de l'état
- Evaluation et testing des agents

---

### `/claude:doc:load`

Charge la documentation Claude Code depuis docs.claude.com dans des fichiers markdown locaux.

**Usage :**
```bash
/claude:doc:load
```

**Fonctionnalités :**
- Télécharge la documentation officielle
- Stocke localement dans `docs/claude/`
- Cache de 24h pour éviter les rechargements inutiles
- Support des agents pour utiliser la doc comme contexte

**Rapport :**
```yaml
task: "Chargement de la documentation Claude Code"
status: "terminé"
details:
  total_urls: 15
  processed: 12
  skipped: 3
  created: 12
```

---

### `/claude:doc:question`

Interroge la documentation Claude Code locale pour répondre à une question.

**Arguments :**
```bash
/claude:doc:question <question>
```

**Prérequis :**
- Documentation chargée via `/claude:doc:load`

**Exemples :**
```bash
/claude:doc:question "Comment créer une slash command ?"
/claude:doc:question "Comment utiliser les hooks ?"
/claude:doc:question "Comment créer un agent personnalisé ?"
```

**Réponse structurée :**
- Concept principal
- Exemples de code
- Références aux fichiers sources
- Liens vers sections connexes

---

### `/claude:alias:add`

Crée un alias de commande qui délègue à une autre slash command.

**Arguments :**
```bash
/claude:alias:add <alias> <commande>
```

**Exemples :**
```bash
# Alias pour git:status
/claude:alias:add status /git:status

# Alias pour doc:update
/claude:alias:add doc /doc:update
```

**Génère :**
- Skill dans `skills/alias-add/`
- Délégation automatique via Skill
- Mise à jour du README

## Licence

MIT
