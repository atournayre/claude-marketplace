---
title: "claude"
description: "Plugin de base pour Claude Code avec commandes essentielles pour l'amélioration et la documentation"
version: "1.2.1"
---

# claude <Badge type="info" text="v1.2.1" />


Plugin de base pour Claude Code avec commandes essentielles pour l'amélioration et la documentation.

## Installation

```bash
/plugin install claude@atournayre
```

## Skills Disponibles

Le plugin claude fournit 5 skills (format natif Claude Code) :

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

### `/claude:make:command`

Générateur de slash commands pour Claude Code avec workflow structuré et bonnes pratiques.

**Arguments :**
```bash
/claude:make:command [nom-commande] [description] [--tools=outil1,outil2] [--category=categorie]
```

**Options :**
- `nom-commande` : Format kebab-case
- `description` : Description courte
- `--tools` : Outils autorisés (défaut: Bash,Read,Write,Edit)
- `--category` : Catégorie (git, doc, build, etc.)

**Exemples :**
```bash
# Commande Git
/claude:make:command git-hotfix "Création de hotfix avec workflow Git" --tools=Bash,Edit --category=git

# Commande Build
/claude:make:command deploy-staging "Déploiement en staging" --tools=Bash,Read --category=build
```

**Génère automatiquement :**
- Frontmatter YAML avec métadonnées
- Structure de workflow
- Section timing
- Documentation

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
