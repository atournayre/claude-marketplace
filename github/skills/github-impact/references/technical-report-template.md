# Template Rapport d'Impact Technique

```markdown
## 🔧 Rapport d'Impact Technique

### Métriques
- Fichiers: [N]
- Ajouts: +[N]
- Suppressions: -[N]
- Commits: [N]

### Analyse par Type

| Type      | Fichiers | Ajouts | Suppressions | Impact Métier | Impact Technique |
|-----------|----------|--------|--------------|---------------|------------------|
| PHP       | [N]      | +[N]   | -[N]         | Backend       | [Score]          |
| JS/TS     | [N]      | +[N]   | -[N]         | Interface     | [Score]          |
| Templates | [N]      | +[N]   | -[N]         | Interface/UX  | Moyen            |
| CSS/SCSS  | [N]      | +[N]   | -[N]         | Apparence     | Faible           |
| Config    | [N]      | +[N]   | -[N]         | Infra         | Critique         |
| Assets    | [N]      | +[N]   | -[N]         | Visuel        | Faible           |

### Changements Architecturaux

#### Classes/Modules Modifiés
- `[Class]`: [Description]

#### Dépendances
##### Ajoutées
- [Package]: [Version] - [Raison]

##### Modifiées
- [Package]: [Old] → [New]

##### Supprimées
- [Package]: [Raison]

### Analyse Sécurité
- **Vulnérabilités corrigées**: [Liste]
- **Nouveaux vecteurs**: [Analyse]
- **Validations ajoutées**: [Liste]

### Couverture Tests
- Tests ajoutés: [N]
- Tests modifiés: [N]
- Couverture estimée: [%]%
- Fichiers non testés: [Liste]

### Points d'Attention

1. **Performance**:
   - [Impact requêtes DB]
   - [Impact mémoire]
   - [Impact temps réponse]

2. **Compatibilité**:
   - [Breaking changes APIs]
   - [Changements schéma DB]
   - [Modifications config]

3. **Dette Technique**:
   - [Dette ajoutée]
   - [Dette remboursée]
   - [Refactoring nécessaire]

### Checklist Revue
- [ ] Tous fichiers ont tests
- [ ] Standards de code respectés
- [ ] Documentation à jour
- [ ] Migrations DB réversibles
- [ ] Variables env documentées
- [ ] Logs appropriés
- [ ] Gestion erreur complète
```

## Scripts d'analyse

### Analyse dépendances PHP
```bash
FILES=$(gh pr diff $PR_NUMBER --name-only)
echo "$FILES" | grep "\.php$" | while read file; do
    grep "use.*;" "$file" 2>/dev/null || true
done
```

### Analyse dépendances JS/TS
```bash
echo "$FILES" | grep -E "\.(js|ts|jsx|tsx)$" | while read file; do
    grep -E "import|require" "$file" 2>/dev/null || true
done
```

### Détection templates
```bash
TEMPLATE_FILES=$(echo "$FILES" | grep -E "\.(twig|blade\.php|vue|svelte)$")
```

### Détection fichiers config
```bash
CONFIG_FILES=$(echo "$FILES" | grep -E "\.(json|yaml|yml|env|ini|conf|xml|toml)$")
```
