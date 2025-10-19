---
model: claude-opus-4-1-20250805
allowed-tools: Bash(git diff:*), Bash(git log:*), Bash(git status:*), Bash(git show:*), Bash(gh pr view:*), Bash(gh pr diff:*), Read, Write, Grep, Glob, TodoWrite
argument-hint: <pr-number>
description: Analyses le détail des modifications git. Fournis 2 rapports d'impact - un rapport métier et un rapport technique. Ajoutes ce rapport à la description de la PR.
---

# Analyse d'Impact des Modifications Git

## Purpose
Analyser en profondeur les modifications d'une Pull Request spécifique pour générer deux rapports d'impact complémentaires (métier et technique) et les intégrer automatiquement à sa description.

## Timing

### Début d'Exécution
**OBLIGATOIRE - PREMIÈRE ACTION** :
1. Exécuter `date` pour obtenir l'heure réelle
2. Afficher immédiatement : 🕐 **Démarrage** : [Résultat de la commande date]
3. Stocker le timestamp pour le calcul de durée

### Fin d'Exécution
**OBLIGATOIRE - DERNIÈRE ACTION** :
1. Exécuter `date` à nouveau pour obtenir l'heure de fin
2. Calculer la durée réelle entre début et fin
3. Afficher :
   - ✅ **Terminé** : [Résultat de la commande date]
   - ⏱️ **Durée** : [Durée calculée au format lisible]

### Formats
- Date : résultat brut de la commande `date` (incluant CEST/CET automatiquement)
- Durée :
  - Moins d'1 minute : `XXs` (ex: 45s)
  - Moins d'1 heure : `XXm XXs` (ex: 2m 30s)
  - Plus d'1 heure : `XXh XXm XXs` (ex: 1h 15m 30s)

### Instructions CRITIQUES
- TOUJOURS exécuter `date` via Bash - JAMAIS inventer/halluciner l'heure
- Le timestamp de début DOIT être obtenu en exécutant `date` immédiatement
- Le timestamp de fin DOIT être obtenu en exécutant `date` à la fin
- Calculer la durée en soustrayant les timestamps unix (utiliser `date +%s`)
- NE JAMAIS supposer ou deviner l'heure

## Variables
- `PR_NUMBER`: Numéro de la PR à analyser (passé en paramètre)
- `CURRENT_BRANCH`: Branche de la PR
- `BASE_BRANCH`: Branche de base de la PR
- `MODIFIED_FILES`: Liste des fichiers modifiés dans la PR
- `COMMIT_COUNT`: Nombre de commits dans la PR

## Instructions
Tu dois analyser les modifications d'une Pull Request spécifique (dont le numéro est passé en paramètre) pour comprendre l'impact complet des changements. Génère deux rapports distincts : un pour les parties prenantes métier (clair, sans jargon) et un pour l'équipe technique (détaillé, avec métriques). Ajoute automatiquement ces rapports à la description de la PR.

### Points d'Attention
- ✅ Analyse complète de tous les fichiers modifiés
- ✅ Identification des dépendances impactées
- ✅ Évaluation des risques potentiels
- ✅ Détection des breaking changes
- ✅ Vérification de la couverture de tests

## Relevant Files
- `.git/`: Historique et état du repository
- `composer.json`: Dépendances PHP (si applicable)
- `package.json`: Dépendances JavaScript (si applicable)
- `tests/`: Tests associés aux modifications
- `config/`: Fichiers de configuration potentiellement impactés

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

### Étape 1: Initialisation TodoWrite
```
Créer une todo list avec toutes les étapes:
1. Récupérer les informations de la PR spécifiée
2. Analyser l'état de la PR (branches, statut)
3. Identifier tous les fichiers modifiés dans la PR
4. Examiner le détail des modifications
5. Analyser les dépendances et impacts
6. Générer le rapport métier
7. Générer le rapport technique
8. Ajouter les rapports à la description de la PR
9. Sauvegarder les rapports localement
```

### Étape 2: Récupération des Informations de la PR
```bash
# Récupérer le numéro de PR depuis les arguments
PR_NUMBER="$ARGUMENTS"

# Vérifier que le numéro de PR est fourni
if [ -z "$PR_NUMBER" ]; then
    echo "❌ ERREUR: Numéro de PR requis"
    echo "Usage: /impact <pr-number>"
    exit 1
fi

# Récupérer les informations de la PR
gh pr view $PR_NUMBER --json number,headRefName,baseRefName,state,title

# Extraire les branches
CURRENT_BRANCH=$(gh pr view $PR_NUMBER --json headRefName -q .headRefName)
BASE_BRANCH=$(gh pr view $PR_NUMBER --json baseRefName -q .baseRefName)

# Vérifier que la PR existe
if [ -z "$CURRENT_BRANCH" ]; then
    echo "❌ ERREUR: PR #$PR_NUMBER introuvable"
    exit 1
fi

echo "✅ Analyse de la PR #$PR_NUMBER"
echo "   Branche: $CURRENT_BRANCH → $BASE_BRANCH"
```

### Étape 3: Identification des Modifications dans la PR
```bash
# Récupérer le diff de la PR via gh
gh pr diff $PR_NUMBER --name-status

# Statistiques globales de la PR
gh pr diff $PR_NUMBER --stat

# Liste des fichiers modifiés
MODIFIED_FILES=$(gh pr diff $PR_NUMBER --name-only)

# Compter les commits dans la PR
COMMIT_COUNT=$(gh pr view $PR_NUMBER --json commits -q '.commits | length')

echo "📊 Statistiques de la PR #$PR_NUMBER:"
echo "   - Fichiers modifiés: $(echo "$MODIFIED_FILES" | wc -l)"
echo "   - Commits: $COMMIT_COUNT"
```

### Étape 4: Analyse des Dépendances et Templates
```bash
# Récupérer les fichiers modifiés de la PR
FILES=$(gh pr diff $PR_NUMBER --name-only)

# Pour PHP
echo "$FILES" | grep "\.php$" | while read file; do
    grep "use.*;" "$file" 2>/dev/null || true
done

# Pour JavaScript/TypeScript
echo "$FILES" | grep -E "\.(js|ts|jsx|tsx)$" | while read file; do
    grep -E "import|require" "$file" 2>/dev/null || true
done

# Pour les templates (Twig, Blade, Vue, etc.)
TEMPLATE_FILES=$(echo "$FILES" | grep -E "\.(twig|blade\.php|vue|svelte|hbs|handlebars|mustache|ejs|pug|jade)$")
if [ -n "$TEMPLATE_FILES" ]; then
    echo "📄 Templates modifiés:"
    echo "$TEMPLATE_FILES" | while read file; do
        echo "  - $file"
        # Analyser les variables et fonctions utilisées dans les templates
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

# Fichiers de styles (CSS, SCSS, SASS, etc.)
STYLE_FILES=$(echo "$FILES" | grep -E "\.(css|scss|sass|less|styl)$")
if [ -n "$STYLE_FILES" ]; then
    echo "🎨 Fichiers de styles modifiés:"
    echo "$STYLE_FILES"
fi

# Fichiers de configuration modifiés dans la PR
CONFIG_FILES=$(echo "$FILES" | grep -E "\.(json|yaml|yml|env|ini|conf|xml|toml)$")
if [ -n "$CONFIG_FILES" ]; then
    echo "⚙️ Fichiers de configuration modifiés:"
    echo "$CONFIG_FILES"
fi

# Assets et medias
ASSET_FILES=$(echo "$FILES" | grep -E "\.(png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$")
if [ -n "$ASSET_FILES" ]; then
    echo "🖼️ Assets modifiés:"
    echo "$ASSET_FILES"
fi
```

### Étape 5: Analyse des Tests
```bash
# Vérifier si des tests ont été ajoutés/modifiés dans la PR
gh pr diff $PR_NUMBER --name-only | grep -E "(test|spec)\.(php|js|ts)$"

# Vérifier la couverture des nouveaux fichiers de la PR
for file in $(gh pr diff $PR_NUMBER --name-only | grep -E "\.(php|js|ts)$"); do
    # Chercher les tests correspondants
    basename=$(basename "$file" | sed 's/\.[^.]*$//')
    find tests/ -name "*${basename}*Test*" 2>/dev/null || echo "⚠️ Pas de test trouvé pour $file"
done
```

### Étape 6: Génération du Rapport Métier
```markdown
## 📊 Rapport d'Impact Métier

### Vue d'Ensemble
- **Portée des modifications** : [Nombre] fichiers modifiés sur [Nombre] commits
- **Domaines fonctionnels impactés** : [Liste des modules/fonctionnalités]
- **Niveau de risque estimé** : 🟢 Faible / 🟡 Modéré / 🔴 Élevé

### Changements Fonctionnels
#### Nouvelles Fonctionnalités
- [Description claire sans jargon technique]

#### Améliorations Interface Utilisateur
- **Templates modifiés** : [Pages/composants impactés]
- **Styles mis à jour** : [Changements visuels attendus]
- **Assets ajoutés/modifiés** : [Nouvelles images, icônes, fonts]

#### Améliorations Fonctionnelles
- [Liste des améliorations de fonctionnalités]

#### Corrections
- **Bugs d'interface** : [Corrections visuelles/UX]
- **Bugs fonctionnels** : [Corrections de logique métier]

### Impact Utilisateur
- **Expérience utilisateur** : [Changements visibles]
- **Performance** : [Améliorations/dégradations attendues]
- **Compatibilité** : [Breaking changes éventuels]

### Risques Identifiés
1. [Risque métier 1 et mitigation]
2. [Risque métier 2 et mitigation]

### Recommandations
- **Tests recommandés** : [Scénarios de test métier]
- **Communication** : [Points à communiquer aux utilisateurs]
- **Déploiement** : [Stratégie suggérée]
```

### Étape 7: Génération du Rapport Technique
```markdown
## 🔧 Rapport d'Impact Technique

### Métriques de Changement
- Fichiers modifiés : [Nombre]
- Lignes ajoutées   : +[Nombre]
- Lignes supprimées : -[Nombre]
- Commits           : [Nombre]

### Analyse par Type de Fichier
| Type      | Fichiers | Ajouts | Suppressions | Impact Métier   | Impact Technique |
|-----------|----------|--------|--------------|-----------------|------------------|
| PHP       | [N]      | +[N]   | -[N]         | Backend         | [Score]          |
| JS/TS     | [N]      | +[N]   | -[N]         | Interface       | [Score]          |
| Templates | [N]      | +[N]   | -[N]         | Interface/UX    | Moyen            |
| CSS/SCSS  | [N]      | +[N]   | -[N]         | Apparence       | Faible           |
| Config    | [N]      | +[N]   | -[N]         | Infrastructure  | Critique         |
| Assets    | [N]      | +[N]   | -[N]         | Visuel          | Faible           |

### Changements Architecturaux
#### Classes/Modules Modifiés
- `[Namespace\Class]`: [Description technique du changement]

#### Dépendances
##### Ajoutées
- [Package]: [Version] - [Raison]

##### Modifiées
- [Package]: [Ancienne version] → [Nouvelle version]

##### Supprimées
- [Package]: [Raison de la suppression]

### Analyse de Sécurité
- **Vulnérabilités corrigées** : [Liste]
- **Nouveaux vecteurs d'attaque** : [Analyse]
- **Validations ajoutées** : [Liste]

### Couverture de Tests
- Tests ajoutés     : [Nombre]
- Tests modifiés    : [Nombre]
- Couverture estimée: [Pourcentage]%
- Fichiers non testés: [Liste]

### Points d'Attention Technique
1. **Performance** :
   - [Impact sur les requêtes DB]
   - [Impact sur la mémoire]
   - [Impact sur le temps de réponse]

2. **Compatibilité** :
   - [Breaking changes dans les APIs]
   - [Changements de schéma DB]
   - [Modifications de configuration]

3. **Dette Technique** :
   - [Dette ajoutée]
   - [Dette remboursée]
   - [Refactoring nécessaire]

### Checklist de Revue
- [ ] Tous les nouveaux fichiers ont des tests
- [ ] Les modifications suivent les standards de code
- [ ] La documentation est à jour
- [ ] Les migrations DB sont réversibles
- [ ] Les variables d'environnement sont documentées
- [ ] Les logs sont appropriés
- [ ] La gestion d'erreur est complète
```

### Étape 8: Ajout des Rapports à la PR
```bash
# La PR existe forcément (vérifiée à l'étape 2)
echo "Mise à jour de la PR #$PR_NUMBER..."

# Récupérer la description actuelle
gh pr view $PR_NUMBER --json body -q .body > /tmp/pr_current_body.md

# Vérifier si les rapports d'impact existent déjà
if grep -q "📊 Rapport d'Impact Métier" /tmp/pr_current_body.md; then
    echo "⚠️ Les rapports d'impact existent déjà, mise à jour..."
    # Supprimer les anciens rapports (entre les marqueurs)
    sed -i '/<!-- IMPACT-REPORTS-START -->/,/<!-- IMPACT-REPORTS-END -->/d' /tmp/pr_current_body.md
fi

# Créer le nouveau contenu avec les rapports
cat /tmp/pr_current_body.md > /tmp/pr_new_body.md
echo "" >> /tmp/pr_new_body.md
echo "<!-- IMPACT-REPORTS-START -->" >> /tmp/pr_new_body.md
echo "---" >> /tmp/pr_new_body.md
echo "" >> /tmp/pr_new_body.md
cat /tmp/impact_report.md >> /tmp/pr_new_body.md
echo "" >> /tmp/pr_new_body.md
echo "<!-- IMPACT-REPORTS-END -->" >> /tmp/pr_new_body.md

# Mettre à jour la PR
gh pr edit $PR_NUMBER --body-file /tmp/pr_new_body.md

echo "✅ Rapports d'impact ajoutés à la PR #$PR_NUMBER"
```

### Étape 9: Sauvegarde Locale
```bash
# Créer un répertoire pour les rapports
mkdir -p .analysis-reports

# Sauvegarder avec le numéro de PR
cp /tmp/impact_report.md ".analysis-reports/impact_pr_${PR_NUMBER}.md"

# Ajouter un timestamp dans le fichier pour tracer la date d'analyse
echo "" >> ".analysis-reports/impact_pr_${PR_NUMBER}.md"
echo "---" >> ".analysis-reports/impact_pr_${PR_NUMBER}.md"
echo "*Analyse générée le $(date '+%Y-%m-%d à %H:%M:%S')*" >> ".analysis-reports/impact_pr_${PR_NUMBER}.md"

echo "📁 Rapport sauvegardé : .analysis-reports/impact_pr_${PR_NUMBER}.md"
```

## Report

### Format de Sortie
```yaml
analysis_completed: true
reports_generated:
  - type: "business"
    risk_level: "[low|medium|high]"
    functional_impacts: [count]
  - type: "technical"
    files_modified: [count]
    lines_changed: [total]
    test_coverage: "[percentage]%"

pr_update:
  status: "[success|not_found|error]"
  pr_number: [number]

local_save:
  path: ".analysis-reports/impact_pr_[pr_number].md"

recommendations:
  - category: "testing"
    priority: "[high|medium|low]"
    actions: [list]
  - category: "deployment"
    priority: "[high|medium|low]"
    strategy: "[description]"
```

### Exemple de Résumé Final
```
✅ ANALYSE D'IMPACT COMPLÈTE

📊 Résumé:
- Fichiers analysés: 24
- Risque métier: 🟡 Modéré
- Risque technique: 🟢 Faible
- Couverture de tests: 87%

📝 Rapports générés:
- Rapport métier: Focus sur l'impact utilisateur
- Rapport technique: Analyse détaillée du code

🔄 Intégration PR:
- PR #42 mise à jour avec les rapports
- URL: https://github.com/[repo]/pull/42

💾 Sauvegarde locale:
- .analysis-reports/impact_pr_42.md

⚠️ Actions recommandées:
1. Tests de régression sur le module authentification
2. Revue de sécurité pour les nouvelles validations
3. Communication aux utilisateurs sur les breaking changes

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
```

## Expertise

### Bonnes Pratiques d'Analyse
- **Exhaustivité** : Ne jamais ignorer de fichiers, même mineurs
- **Contextualisation** : Toujours relier les changements techniques aux impacts métier
- **Priorisation** : Mettre en avant les risques et breaking changes
- **Clarté** : Adapter le niveau de détail selon l'audience (métier vs technique)

### Métriques Clés
- **Complexité cyclomatique** : Identifier les fonctions devenues trop complexes
- **Couplage** : Détecter les dépendances nouvelles ou renforcées
- **Duplication** : Signaler le code dupliqué introduit
- **Coverage Delta** : Évolution de la couverture de tests

### Points de Vigilance
- Les modifications de configuration peuvent avoir des impacts majeurs
- Les changements dans les tests peuvent indiquer des modifications de comportement
- Les suppressions de code peuvent casser des dépendances non évidentes
- Les ajouts de dépendances augmentent la surface d'attaque
