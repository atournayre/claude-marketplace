# Claude Plugin Marketplace

> ⚠️ **DISCLAIMER:** Ce plugin est en cours de développement actif. Utilise-le avec précaution et n'hésite pas à remonter tout bug ou comportement inattendu via les issues GitHub.

Marketplace de plugins pour Claude Code, offrant un ensemble d'outils pour améliorer ton workflow de développement.

## 📦 Plugins disponibles

### 🤖 Claude
Plugin de base pour Claude Code avec commandes essentielles.

**Commandes:**
- `/claude:challenge` - Évaluation et amélioration de tes réponses
- `/claude:make:command` - Générateur de slash commands
- `/claude:doc:load` - Chargement de la documentation Claude Code
- `/claude:doc:question` - Questions sur la documentation Claude Code
- `/claude:alias:add` - Créer des alias de commandes

### 🎨 Customize
Personnalise ton expérience Claude avec hooks, output styles et status lines.

**Fonctionnalités:**
- Hooks personnalisés (notification, pre/post tool use, session management)
- Output styles variés (YAML, Markdown, HTML, bullet points, etc.)
- Status lines customisables (5 variantes)

### ⚙️ Dev
Toolkit général de développement.

**Commandes:**
- `/dev:code` - Coder depuis un plan
- `/dev:docker` - Actions via Docker
- `/dev:prepare` - Génération plan d'implémentation
- `/dev:question` - Questions structure projet
- `/dev:context:load` - Charger preset de contexte
- `/dev:debug:error` - Analyser et résoudre erreurs

### 🔧 Git
Workflow Git complet.

**Commandes:**
- `/git:branch` - Création branches structurées
- `/git:commit` - Commits conventional avec emoji
- `/git:conflit` - Résolution conflits guidée
- `/git:pr` - Création Pull Request optimisée

### 🐙 GitHub
Gestion GitHub et analyse.

**Commandes:**
- `/github:fix` - Corriger une issue GitHub
- `/github:impact` - Analyse impact modifications PR

### 📋 QA
Quality assurance et tests.

**Commandes:**
- `/qa:phpstan` - Résolution erreurs PHPStan

### 📚 Doc
Gestion documentation.

**Commandes:**
- `/doc:adr` - Génération Architecture Decision Record
- `/doc:framework-load` - Charger doc framework
- `/doc:framework-question` - Interroger doc framework
- `/doc:rtfm` - Lire documentation technique
- `/doc:update` - Créer/mettre à jour documentation

### 🎯 Symfony
Plugin spécialisé pour le framework Symfony.

**Commandes:**
- `/symfony:make` - Utilisation des makers Symfony
- `/symfony:doc:load` - Chargement de la documentation Symfony
- `/symfony:doc:question` - Questions sur la documentation Symfony

### 📊 Output Styles
Styles de sortie personnalisés pour formater les réponses.

**Styles disponibles:**
- `/output-styles:style-ultra-concise` - Mode ultra-concis
- `/output-styles:style-yaml-structured` - Format YAML structuré
- `/output-styles:style-markdown-focused` - Markdown enrichi
- `/output-styles:style-genui` - UI générative avec HTML
- `/output-styles:style-html-structured` - HTML sémantique
- `/output-styles:style-table-based` - Tableaux markdown
- `/output-styles:style-bullet-points` - Listes à puces hiérarchiques

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

# Plugin Dev (toolkit développement)
/plugin install dev@atournayre

# Plugin Git (workflow Git)
/plugin install git@atournayre

# Plugin GitHub (gestion GitHub)
/plugin install github@atournayre

# Plugin QA (quality assurance)
/plugin install qa@atournayre

# Plugin Doc (documentation)
/plugin install doc@atournayre

# Plugin Symfony (commandes Symfony)
/plugin install symfony@atournayre

# Plugin Output Styles (styles de sortie)
/plugin install output-styles@atournayre
```

### Vérifier l'installation

Vérifie que les plugins sont bien installés :

```bash
/help
```

Tu devrais voir les nouvelles commandes disponibles avec leurs préfixes (`/claude:`, `/dev:`, `/git:`, `/github:`, `/qa:`, `/doc:`, `/symfony:`, `/output-styles:`).

### Configuration équipe (optionnel)

Pour partager la configuration avec ton équipe, ajoute dans `.claude/settings.json` de ton projet :

```json
{
  "plugins": {
    "marketplaces": ["atournayre/claude-marketplace"],
    "installed": [
      "claude@atournayre",
      "customize@atournayre",
      "dev@atournayre",
      "git@atournayre",
      "github@atournayre",
      "qa@atournayre",
      "doc@atournayre",
      "symfony@atournayre",
      "output-styles@atournayre"
    ]
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
├── dev/                      # Plugin de développement
│   ├── .claude-plugin/
│   ├── commands/
│   └── agents/
├── git/                      # Plugin Git
│   ├── .claude-plugin/
│   └── commands/
├── github/                   # Plugin GitHub
│   ├── .claude-plugin/
│   └── commands/
├── qa/                       # Plugin QA
│   ├── .claude-plugin/
│   └── commands/
├── doc/                      # Plugin Documentation
│   ├── .claude-plugin/
│   └── commands/
├── symfony/                  # Plugin Symfony
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/
└── output-styles/            # Plugin styles de sortie
    ├── .claude-plugin/
    ├── commands/
    └── hooks/
```

## 🔧 Configuration

Chaque plugin contient:
- `.claude-plugin/plugin.json` - Métadonnées du plugin
- `commands/` - Slash commands disponibles
- `skills/` - Compétences spécialisées (dev, symfony)
- `hooks/` - Scripts de hooks (customize, output-styles)

## 📖 Utilisation

Une fois installé, tu peux utiliser les commandes avec le préfixe du plugin:

```bash
# Exemples
/claude:challenge
/git:commit
/github:fix 123
/qa:phpstan
/doc:adr "Choix architecture API"
/symfony:make entity
/output-styles:style-yaml-structured
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
