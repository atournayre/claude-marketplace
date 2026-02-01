# Guide de Contribution

Merci de ton intérêt pour contribuer au Claude Plugin Marketplace ! 🎉

## 📖 Documentation complète

Consulte le **[Guide de contribution complet](https://atournayre.github.io/claude-marketplace/guide/contributing)** pour tous les détails sur :

- ➕ Comment ajouter un nouveau plugin
- ✏️ Comment modifier un plugin existant
- 🔄 Comment fonctionne la génération automatique de la documentation
- 🐛 Dépannage des problèmes courants
- 📝 Checklist avant de pusher

## 🚀 Quick Start

### Ajouter un plugin

1. **Créer la structure** :
   ```bash
   mkdir mon-plugin
   cd mon-plugin
   mkdir -p .claude-plugin skills
   ```

2. **Créer `plugin.json`** :
   ```json
   {
     "name": "Mon Plugin",
     "version": "1.0.0",
     "description": "Description courte",
     "author": {
       "name": "Ton Nom",
       "email": "ton@email.com"
     },
     "keywords": ["tag1", "tag2"]
   }
   ```

3. **Créer `README.md`** avec la documentation du plugin

4. **Générer la doc** :
   ```bash
   cd docs
   npm install
   npm run generate
   npm run dev  # Vérifier localement
   ```

5. **Commit et push** :
   ```bash
   git add mon-plugin/ docs/
   git commit -m "feat: add mon-plugin"
   git push origin main
   ```

GitHub Actions déploiera automatiquement la doc mise à jour ! ✨

## 📋 Règles importantes

### ✅ À faire
- Modifier les sources (`*/README.md`, `*/plugin.json`, `*/skills/*/SKILL.md`)
- Lancer `npm run generate` après chaque modification
- Vérifier avec `npm run dev` avant de pusher
- Utiliser des liens relatifs vers d'autres plugins

### ❌ À éviter
- Modifier directement `docs/plugins/*.md` (sauf `index.md` et `by-category.md`)
- Modifier directement `docs/commands/index.md`
- Pusher sans avoir régénéré la doc
- Utiliser des liens vers `MODELS.md`, `CHANGELOG.md` (ils seront supprimés)

## 🔗 Liens utiles

- **Documentation du marketplace** : https://atournayre.github.io/claude-marketplace/
- **Guide de contribution détaillé** : https://atournayre.github.io/claude-marketplace/guide/contributing
- **Issues** : https://github.com/atournayre/claude-marketplace/issues
- **VitePress Docs** : https://vitepress.dev/

## 💬 Questions ?

Si tu as des questions ou rencontres des problèmes :
1. Consulte le [guide de contribution](https://atournayre.github.io/claude-marketplace/guide/contributing)
2. Cherche dans les [issues existantes](https://github.com/atournayre/claude-marketplace/issues)
3. Ouvre une nouvelle issue si nécessaire

Merci pour ta contribution ! 🙏
