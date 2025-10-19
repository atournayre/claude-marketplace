# Claude Plugin Marketplace

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

```bash
# Clone le repo
git clone https://github.com/atournayre/claude-plugin.git

# Configure ton marketplace dans Claude Code settings
# Ajoute le chemin vers le fichier .claude-plugin/marketplace.json
```

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

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésite pas à ouvrir une issue ou une PR.

## 📄 License

MIT - voir [LICENSE](LICENSE)

## 👤 Auteur

**Aurélien Tournayre**
- Email: aurelien.tournayre@gmail.com
- GitHub: [@atournayre](https://github.com/atournayre)
