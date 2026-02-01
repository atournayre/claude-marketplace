# Template Plugin Structure

Ce template fournit la structure standard pour créer un nouveau plugin.

## Utilisation

1. Copier ce dossier : `cp -r templates/plugin-structure/ nouveau-plugin/`
2. Renommer `nouveau-plugin` selon le nom du plugin
3. Éditer `plugin.json` avec les informations du plugin
4. Remplir `README-TEMPLATE.md` et renommer en `README.md`
5. Remplir `CHANGELOG-TEMPLATE.md` et renommer en `CHANGELOG.md`
6. Adapter `DEPENDENCIES.json` selon les besoins
7. Si scripts TypeScript : `bun install` pour installer dépendances

## Fichiers fournis

- `.claude-plugin/plugin.json` : Métadonnées du plugin
- `README-TEMPLATE.md` : Template documentation
- `CHANGELOG-TEMPLATE.md` : Template changelog
- `DEPENDENCIES.json` : Template dépendances
- `biome.json` : Configuration linting (si TypeScript)
- `package.json` : Configuration npm/bun (si scripts)

## Standards qualité

Voir `docs/QUALITY_STANDARDS.md` pour les standards complets.

### Checklist nouveau plugin

- [ ] plugin.json rempli correctement
- [ ] README.md documenté (skills, agents, exemples)
- [ ] CHANGELOG.md avec version initiale
- [ ] DEPENDENCIES.json si dépendances externes
- [ ] Tests unitaires si scripts complexes
- [ ] Linting configuré (Biome) si TypeScript
- [ ] Ajouté dans `.claude-plugin/marketplace.json`
- [ ] Ajouté dans `README.md` global
- [ ] Ajouté dans `CHANGELOG.md` global
