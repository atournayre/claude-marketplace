# Plugin Command - Workaround Issue #15178

## 📋 Description

Plugin centralisé qui contient toutes les slash commands des autres plugins du marketplace. Ce plugin est un **workaround** pour [Claude Code issue #15178](https://github.com/anthropics/claude-code/issues/15178).

## ⚠️ Contexte

L'issue #15178 de Claude Code empêche les skills d'être directement utilisables comme slash commands. En attendant que cette limitation soit résolue, ce plugin centralise toutes les commandes et les fait pointer vers les skills correspondants dans leurs plugins d'origine.

## 🏗️ Architecture

```
command/
├── .claude-plugin/
│   └── plugin.json          # Métadonnées du plugin
├── commands/                 # Toutes les commandes centralisées
│   ├── claude/              # Commandes du plugin claude
│   ├── dev/                 # Commandes du plugin dev
│   ├── git/                 # Commandes du plugin git
│   ├── github/              # Commandes du plugin github
│   ├── qa/                  # Commandes du plugin qa
│   ├── doc/                 # Commandes du plugin doc
│   ├── symfony/             # Commandes du plugin symfony
│   ├── framework/           # Commandes du plugin framework
│   ├── gemini/              # Commandes du plugin gemini
│   ├── marketing/           # Commandes du plugin marketing
│   └── prompt/              # Commandes du plugin prompt
└── README.md                # Ce fichier
```

## 📝 Fonctionnement

Chaque commande dans ce plugin :

1. Est définie dans `commands/[plugin]/[command].md`
2. Contient un frontmatter YAML avec metadata (description, allowed-tools, argument-hint)
3. Appelle le Skill tool pour invoquer le skill du plugin d'origine
4. Contient une note explicite sur le workaround

### Exemple de commande

```markdown
---
description: Description de la commande
argument-hint: "[args optionnels]"
allowed-tools:
  - Read
  - Write
---
# plugin:command-name

Description détaillée

---

**IMPORTANT**: Use the Skill tool to invoke the skill `plugin:command-name` with arguments: $ARGUMENTS.

Execute the skill immediately. Do not explain or describe what you will do - just invoke the skill using the Skill tool.

---

**Note**: This slash command was auto-generated to workaround Claude Code bug #15178.
Once fixed, this workaround can be removed.
```

## 🔄 Plugins sources

Les skills restent dans leurs plugins d'origine :

- **claude** : Plugin de base pour Claude Code
- **dev** : Workflow de développement de features
- **git** : Workflow Git complet
- **github** : Gestion GitHub
- **qa** : Quality assurance
- **doc** : Documentation
- **symfony** : Plugin Symfony
- **framework** : Plugin atournayre/framework
- **gemini** : Délégation Gemini CLI
- **marketing** : Génération de contenu marketing
- **prompt** : Générateur de prompts structurés

## ⏭️ Après résolution de l'issue

Une fois que l'issue #15178 sera résolue :

1. Ce plugin pourra être supprimé
2. Les commandes pourront être restaurées dans leurs plugins d'origine
3. Les skills pourront être utilisés directement comme slash commands

## 📚 Ressources

- [Claude Code issue #15178](https://github.com/anthropics/claude-code/issues/15178)
- [Documentation Claude Code](https://code.claude.com/docs)
- [Marketplace atournayre](https://github.com/atournayre/claude-marketplace)

## 📄 Licence

MIT - Voir le fichier LICENSE du repository principal
