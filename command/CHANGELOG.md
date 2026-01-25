# Changelog - Plugin Command

Toutes les modifications notables de ce plugin seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-26

### Added
- 🎉 Création initiale du plugin `command`
- 📦 Import de 63 commandes depuis 11 plugins :
  - claude : 5 commandes
  - dev : 23 commandes
  - git : 8 commandes
  - github : 2 commandes
  - qa : 2 commandes
  - doc : 4 commandes
  - symfony : 4 commandes
  - framework : 9 commandes
  - gemini : 3 commandes
  - marketing : 1 commande
  - prompt : 7 commandes
- 📝 Documentation complète (README.md)
- ⚙️ Configuration plugin.json
- 🔧 Structure centralisée pour workaround issue #15178

### Context
Ce plugin est un **workaround temporaire** pour [Claude Code issue #15178](https://github.com/anthropics/claude-code/issues/15178).

L'issue empêche les skills d'être directement utilisables comme slash commands. Ce plugin centralise donc toutes les commandes qui appellent les skills de leurs plugins d'origine.

### Migration
- ✅ Toutes les commandes conservent leurs fonctionnalités
- ✅ Tous les appels de skills sont préservés
- ✅ Metadata (description, allowed-tools, argument-hint) migrées
- ✅ Compatibilité complète avec les plugins existants

### Notes
Une fois l'issue #15178 résolue, ce plugin pourra être supprimé et les commandes restaurées dans leurs plugins d'origine.
