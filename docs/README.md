# Claude Plugin Marketplace - Documentation

Site de documentation VitePress pour les plugins Claude Code.

## 🚀 Développement Local

```bash
# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev
# Ouvre http://localhost:5173
```

## 📦 Build Production

```bash
# Générer les docs depuis les plugins + build VitePress
npm run build

# Preview du build
npm run preview
```

## 🔄 Génération Automatique des Docs

**IMPORTANT** : Les fichiers de documentation sont **générés automatiquement** depuis les plugins sources. Ne modifie jamais directement les fichiers dans `docs/plugins/` (sauf `index.md` et `by-category.md`) !

### Sources → Destination

| Source | Destination | Description |
|--------|-------------|-------------|
| `*/README.md` | `docs/plugins/*.md` | Page complète du plugin |
| `*/.claude-plugin/plugin.json` | Frontmatter YAML | Métadonnées (titre, version) |
| `*/skills/*/SKILL.md` | `docs/commands/index.md` | Index des 70 commandes |

### Workflow de modification

1. **Modifier le source** (ex: `git/README.md`)
2. **Régénérer** : `npm run generate`
3. **Vérifier** : `npm run dev`
4. **Commiter** les sources ET les fichiers générés

```bash
# Exemple complet
cd docs
npm run generate  # Régénère tous les fichiers
npm run dev       # Vérifie en local
```

### Guide complet

Consulte [docs/guide/contributing.md](guide/contributing.md) pour :
- Ajouter un nouveau plugin
- Modifier un plugin existant
- Comprendre les transformations automatiques
- Dépanner les problèmes courants

## 📁 Structure

```
docs/
├── .vitepress/
│   ├── config.ts              # Config VitePress
│   ├── theme/                 # Custom theme (dark mode)
│   └── data/
│       └── plugins.data.ts    # Data loader pour métadonnées
├── public/                    # Assets statiques
├── index.md                   # Homepage
├── guide/                     # Guides d'installation
├── plugins/                   # Pages générées par plugin
└── commands/                  # Index des commandes
```

## 🔧 Scripts

- `npm run dev` - Serveur de développement
- `npm run build` - Build production (génère docs + VitePress)
- `npm run preview` - Preview du build
- `npm run generate` - Génère docs depuis plugins

## 🌐 Déploiement

Le site est déployé automatiquement sur GitHub Pages via GitHub Actions lors d'un push sur `main`.

URL : `https://atournayre.github.io/claude-marketplace`

## 📝 Maintenance

### Ajouter un nouveau plugin

1. Créer le plugin dans la racine du repo
2. Lancer `npm run generate`
3. Vérifier `docs/plugins/<plugin-name>.md`

### Mettre à jour un README

1. Modifier le README dans le plugin
2. Lancer `npm run generate`
3. Vérifier le build : `npm run build`

## ⚠️ Notes Importantes

- Les liens internes vers `MODELS.md`, `CHANGELOG.md` sont automatiquement supprimés
- Les badges GitHub Actions sont retirés lors de la génération
- Les liens relatifs entre plugins sont transformés en liens absolus VitePress
- Le frontmatter YAML est généré automatiquement depuis `plugin.json`

## 📚 Documentation VitePress

- [VitePress Docs](https://vitepress.dev/)
- [Config Reference](https://vitepress.dev/reference/site-config)
- [Theme Config](https://vitepress.dev/reference/default-theme-config)
