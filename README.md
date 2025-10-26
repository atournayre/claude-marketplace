# Claude Plugin Marketplace

> ⚠️ **DISCLAIMER:** Ce plugin est en cours de développement actif. Utilise-le avec précaution et n'hésite pas à remonter tout bug ou comportement inattendu via les issues GitHub.

Marketplace de plugins pour Claude Code, offrant un ensemble d'outils pour améliorer ton workflow de développement.

## 📦 Plugins disponibles

### 🤖 Claude
Plugin de base pour Claude Code avec commandes essentielles.

**Commandes:**
- `/claude:challenge` - Évaluation et amélioration de tes réponses
- `/claude:doc:load` - Chargement de la documentation Claude Code
- `/claude:doc:question` - Questions sur la documentation Claude Code
- `/claude:make:command` - Générateur de slash commands

### 🎨 Customize
Personnalise ton expérience Claude avec hooks, output styles et status lines.

**Fonctionnalités:**
- Hooks personnalisés (notification, pre/post tool use, session management)
- Output styles variés (YAML, Markdown, HTML, bullet points, etc.)
- Status lines customisables (5 variantes)

### ⚙️ Dev
Toolkit complet de développement pour Symfony/PHP.

**Domaines couverts:**
- **Git:** Gestion branches, commits, PRs, conflits, status
- **Documentation:** ADR, RTFM, mises à jour automatiques
- **Debugging:** Stack traces, error-fix
- **QA:** PHPStan level 9
- **Framework:** Symfony, API Platform, Meilisearch
- **Sessions:** Gestion de sessions de développement
- **Workflow:** Docker, analytics, context management

## 🚀 Installation

### Ajouter le marketplace

Depuis Claude Code, ajoute le marketplace à ta configuration :

```bash
/plugin marketplace add atournayre/claude-marketplace
```

### Installer tous les plugins

Pour installer tous les plugins du marketplace en une fois :

```bash
/plugin
```

Puis sélectionne "Browse Plugins" et installe les plugins souhaités.

### Installer un plugin spécifique

Pour installer un plugin individuellement :

```bash
# Plugin Claude (commandes essentielles)
/plugin install claude@atournayre

# Plugin Customize (hooks, output styles, status lines)
/plugin install customize@atournayre

# Plugin Dev (toolkit Symfony/PHP complet)
/plugin install dev@atournayre
```

### Vérifier l'installation

Vérifie que les plugins sont bien installés :

```bash
/help
```

Tu devrais voir les nouvelles commandes disponibles avec leurs préfixes (`/claude:`, `/customize:`, `/dev:`).

### Configuration équipe (optionnel)

Pour partager la configuration avec ton équipe, ajoute dans `.claude/settings.json` de ton projet :

```json
{
  "plugins": {
    "marketplaces": ["atournayre/claude-marketplace"],
    "installed": ["claude@atournayre", "customize@atournayre", "dev@atournayre"]
  }
}
```

Les plugins s'installeront automatiquement quand les membres de l'équipe trustent le dossier.

## 📝 Structure du projet

```
.
├── .claude-plugin/
│   └── marketplace.json       # Configuration du marketplace
├── claude/                    # Plugin Claude de base
│   ├── .claude-plugin/
│   └── commands/
├── customize/                 # Plugin de customisation
│   ├── hooks/
│   ├── output-styles/
│   └── status_lines/
└── dev/                      # Plugin de développement
    ├── commands/
    └── skills/
```

## 🔧 Configuration

Chaque plugin contient:
- `.claude-plugin/plugin.json` - Métadonnées du plugin
- `commands/` - Slash commands disponibles
- `skills/` - Compétences spécialisées (dev uniquement)
- `hooks/` - Scripts de hooks (customize uniquement)

## 📖 Utilisation

Une fois installé, tu peux utiliser les commandes avec le préfixe du plugin:

```bash
# Exemples
/claude:challenge
/dev:git:commit
/dev:symfony:make entity
/customize # Active les hooks et styles
```

### Gestion des plugins

**Activer/Désactiver un plugin** sans le désinstaller :

```bash
# Désactiver temporairement
/plugin disable dev@atournayre

# Réactiver
/plugin enable dev@atournayre
```

**Désinstaller un plugin** complètement :

```bash
/plugin uninstall dev@atournayre
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésite pas à ouvrir une issue ou une PR.

## 📄 License

MIT - voir [LICENSE](LICENSE)

## 👤 Auteur

**Aurélien Tournayre**
- Email: aurelien.tournayre@gmail.com
- GitHub: [@atournayre](https://github.com/atournayre)
