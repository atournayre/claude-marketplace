---
name: github-impact
description: >
  Génère automatiquement deux rapports d'impact (métier et technique) pour une PR GitHub
  et les intègre dans la description. Analyse les modifications, dépendances, tests,
  sécurité et performance.
allowed-tools: [Bash, Read, Write, TodoWrite, Grep, Glob]
model: claude-opus-4-1-20250805
---

# GitHub PR Impact Analysis Skill

## Variables

```bash
ARGUMENTS="$ARGUMENTS"  # Numéro de PR passé en argument
PR_NUMBER=""
CURRENT_BRANCH=""
BASE_BRANCH=""
MODIFIED_FILES=""
COMMIT_COUNT=""
```

## Workflow

### Étape 0: Timing
```bash
START_TIME=$(date +%s)
date
```

### Étape 1: Parsing Arguments

```bash
PR_NUMBER="$ARGUMENTS"

# Validation
if [ -z "$PR_NUMBER" ]; then
    echo "❌ ERREUR: Numéro de PR requis"
    echo "Usage: /github:impact <pr-number>"
    exit 1
fi
```

### Étape 2: TodoWrite Initialisation

```yaml
todos:
  - content: "Récupérer informations PR"
    status: "pending"
    activeForm: "Récupération des informations PR"
  - content: "Identifier fichiers modifiés"
    status: "pending"
    activeForm: "Identification des fichiers modifiés"
  - content: "Analyser dépendances et templates"
    status: "pending"
    activeForm: "Analyse des dépendances et templates"
  - content: "Analyser tests"
    status: "pending"
    activeForm: "Analyse des tests"
  - content: "Générer rapport métier"
    status: "pending"
    activeForm: "Génération du rapport métier"
  - content: "Générer rapport technique"
    status: "pending"
    activeForm: "Génération du rapport technique"
  - content: "Ajouter rapports à la PR"
    status: "pending"
    activeForm: "Ajout des rapports à la PR"
  - content: "Sauvegarder localement"
    status: "pending"
    activeForm: "Sauvegarde locale"
```

### Étape 3: Récupération Informations PR

Marquer todo #1 `in_progress`.

```bash
# Récupérer infos PR
gh pr view $PR_NUMBER --json number,headRefName,baseRefName,state,title

# Extraire branches
CURRENT_BRANCH=$(gh pr view $PR_NUMBER --json headRefName -q .headRefName)
BASE_BRANCH=$(gh pr view $PR_NUMBER --json baseRefName -q .baseRefName)

# Vérifier existence
if [ -z "$CURRENT_BRANCH" ]; then
    echo "❌ ERREUR: PR #$PR_NUMBER introuvable"
    exit 1
fi

echo "✅ Analyse de la PR #$PR_NUMBER"
echo "   Branche: $CURRENT_BRANCH → $BASE_BRANCH"
```

Marquer todo #1 `completed`.

### Étape 4: Identification Modifications

Marquer todo #2 `in_progress`.

```bash
# Récupérer diff PR
gh pr diff $PR_NUMBER --name-status
gh pr diff $PR_NUMBER --stat

# Liste fichiers modifiés
MODIFIED_FILES=$(gh pr diff $PR_NUMBER --name-only)

# Compter commits
COMMIT_COUNT=$(gh pr view $PR_NUMBER --json commits -q '.commits | length')

echo "📊 Statistiques PR #$PR_NUMBER:"
echo "   - Fichiers modifiés: $(echo "$MODIFIED_FILES" | wc -l)"
echo "   - Commits: $COMMIT_COUNT"
```

Marquer todo #2 `completed`.

### Étape 5: Analyse Dépendances et Templates

Marquer todo #3 `in_progress`.

```bash
FILES=$(gh pr diff $PR_NUMBER --name-only)

# PHP dependencies
echo "$FILES" | grep "\.php$" | while read file; do
    grep "use.*;" "$file" 2>/dev/null || true
done

# JS/TS dependencies
echo "$FILES" | grep -E "\.(js|ts|jsx|tsx)$" | while read file; do
    grep -E "import|require" "$file" 2>/dev/null || true
done

# Templates (Twig, Blade, Vue, etc.)
TEMPLATE_FILES=$(echo "$FILES" | grep -E "\.(twig|blade\.php|vue|svelte|hbs|handlebars|mustache|ejs|pug|jade)$")
if [ -n "$TEMPLATE_FILES" ]; then
    echo "📄 Templates modifiés:"
    echo "$TEMPLATE_FILES" | while read file; do
        echo "  - $file"
        case "$file" in
            *.twig)
                grep -E "\{\{|\{%" "$file" 2>/dev/null | head -10 || true
                ;;
            *.blade.php)
                grep -E "@[a-zA-Z]+|\{\{" "$file" 2>/dev/null | head -10 || true
                ;;
            *.vue)
                grep -E "v-|@|:\w+" "$file" 2>/dev/null | head -10 || true
                ;;
        esac
    done
fi

# Styles
STYLE_FILES=$(echo "$FILES" | grep -E "\.(css|scss|sass|less|styl)$")
if [ -n "$STYLE_FILES" ]; then
    echo "🎨 Fichiers styles modifiés:"
    echo "$STYLE_FILES"
fi

# Config
CONFIG_FILES=$(echo "$FILES" | grep -E "\.(json|yaml|yml|env|ini|conf|xml|toml)$")
if [ -n "$CONFIG_FILES" ]; then
    echo "⚙️ Fichiers config modifiés:"
    echo "$CONFIG_FILES"
fi

# Assets
ASSET_FILES=$(echo "$FILES" | grep -E "\.(png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$")
if [ -n "$ASSET_FILES" ]; then
    echo "🖼️ Assets modifiés:"
    echo "$ASSET_FILES"
fi
```

Marquer todo #3 `completed`.

### Étape 6: Analyse Tests

Marquer todo #4 `in_progress`.

```bash
# Vérifier tests ajoutés/modifiés
gh pr diff $PR_NUMBER --name-only | grep -E "(test|spec)\.(php|js|ts)$"

# Vérifier couverture
for file in $(gh pr diff $PR_NUMBER --name-only | grep -E "\.(php|js|ts)$"); do
    basename=$(basename "$file" | sed 's/\.[^.]*$//')
    find tests/ -name "*${basename}*Test*" 2>/dev/null || echo "⚠️ Pas de test pour $file"
done
```

Marquer todo #4 `completed`.

### Étape 7: Génération Rapport Métier

Marquer todo #5 `in_progress`.

Créer fichier `/tmp/impact_business_report.md` avec:

```markdown
## 📊 Rapport d'Impact Métier

### Vue d'Ensemble
- **Portée**: [N] fichiers sur [N] commits
- **Domaines impactés**: [Liste]
- **Risque estimé**: 🟢/🟡/🔴

### Changements Fonctionnels

#### Nouvelles Fonctionnalités
- [Liste]

#### Améliorations Interface Utilisateur
- **Templates**: [Pages/composants]
- **Styles**: [Changements visuels]
- **Assets**: [Nouvelles images/icônes]

#### Améliorations Fonctionnelles
- [Liste]

#### Corrections
- **Bugs interface**: [Liste]
- **Bugs fonctionnels**: [Liste]

### Impact Utilisateur
- **UX**: [Changements visibles]
- **Performance**: [Améliorations/dégradations]
- **Compatibilité**: [Breaking changes]

### Risques Identifiés
1. [Risque + mitigation]
2. [Risque + mitigation]

### Recommandations
- **Tests recommandés**: [Scénarios]
- **Communication**: [Points à communiquer]
- **Déploiement**: [Stratégie]
```

Marquer todo #5 `completed`.

### Étape 8: Génération Rapport Technique

Marquer todo #6 `in_progress`.

Créer fichier `/tmp/impact_technical_report.md` avec:

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

Marquer todo #6 `completed`.

### Étape 9: Ajout Rapports à PR

Marquer todo #7 `in_progress`.

```bash
echo "Mise à jour PR #$PR_NUMBER..."

# Récupérer description actuelle
gh pr view $PR_NUMBER --json body -q .body > /tmp/pr_current_body.md

# Vérifier si rapports existent déjà
if grep -q "📊 Rapport d'Impact Métier" /tmp/pr_current_body.md; then
    echo "⚠️ Rapports existent, mise à jour..."
    sed -i '/<!-- IMPACT-REPORTS-START -->/,/<!-- IMPACT-REPORTS-END -->/d' /tmp/pr_current_body.md
fi

# Créer nouveau contenu
cat /tmp/pr_current_body.md > /tmp/pr_new_body.md
echo "" >> /tmp/pr_new_body.md
echo "<!-- IMPACT-REPORTS-START -->" >> /tmp/pr_new_body.md
echo "---" >> /tmp/pr_new_body.md
echo "" >> /tmp/pr_new_body.md
cat /tmp/impact_business_report.md >> /tmp/pr_new_body.md
echo "" >> /tmp/pr_new_body.md
cat /tmp/impact_technical_report.md >> /tmp/pr_new_body.md
echo "" >> /tmp/pr_new_body.md
echo "<!-- IMPACT-REPORTS-END -->" >> /tmp/pr_new_body.md

# Mettre à jour PR
gh pr edit $PR_NUMBER --body-file /tmp/pr_new_body.md

echo "✅ Rapports ajoutés à PR #$PR_NUMBER"
```

Marquer todo #7 `completed`.

### Étape 10: Sauvegarde Locale

Marquer todo #8 `in_progress`.

```bash
mkdir -p .analysis-reports

# Combiner rapports
cat /tmp/impact_business_report.md > ".analysis-reports/impact_pr_${PR_NUMBER}.md"
echo "" >> ".analysis-reports/impact_pr_${PR_NUMBER}.md"
cat /tmp/impact_technical_report.md >> ".analysis-reports/impact_pr_${PR_NUMBER}.md"

# Timestamp
echo "" >> ".analysis-reports/impact_pr_${PR_NUMBER}.md"
echo "---" >> ".analysis-reports/impact_pr_${PR_NUMBER}.md"
echo "*Analyse générée le $(date '+%Y-%m-%d à %H:%M:%S')*" >> ".analysis-reports/impact_pr_${PR_NUMBER}.md"

echo "📁 Rapport sauvegardé: .analysis-reports/impact_pr_${PR_NUMBER}.md"
```

Marquer todo #8 `completed`.

### Étape 11: Rapport Final

```bash
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ $DURATION -lt 60 ]; then
    DURATION_STR="${DURATION}s"
elif [ $DURATION -lt 3600 ]; then
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    DURATION_STR="${MINUTES}m ${SECONDS}s"
else
    HOURS=$((DURATION / 3600))
    MINUTES=$(((DURATION % 3600) / 60))
    SECONDS=$((DURATION % 60))
    DURATION_STR="${HOURS}h ${MINUTES}m ${SECONDS}s"
fi

echo "⏱️ Durée: $DURATION_STR"
```

```yaml
analysis_completed: true
reports_generated:
  - type: "business"
    risk_level: "[low|medium|high]"
    functional_impacts: [count]
  - type: "technical"
    files_modified: [count]
    lines_changed: [total]
    test_coverage: "[%]%"

pr_update:
  status: "success"
  pr_number: $PR_NUMBER

local_save:
  path: ".analysis-reports/impact_pr_${PR_NUMBER}.md"

recommendations:
  - category: "testing"
    priority: "[high|medium|low]"
  - category: "deployment"
    strategy: "[description]"
```

## Error Handling

- Template PR absent → ARRÊT (exit 1)
- PR introuvable → ARRÊT (exit 1)
- Échec mise à jour PR → WARNING (non bloquant)

## Notes

- Utilise `gh` CLI pour GitHub
- Parser JSON via `jq` ou équivalent
- Marquer CHAQUE todo completed immédiatement après succès
