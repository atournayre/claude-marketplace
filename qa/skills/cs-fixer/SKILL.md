---
name: cs-fixer
description: >
  Analyse et corrige automatiquement le style de code PHP en utilisant les scripts
  composer du projet. Détecte automatiquement les scripts CS-Fixer définis dans
  composer.json et les utilise pour respecter les conventions du projet.
allowed-tools: [Bash, Read, Grep, Glob, TodoWrite]
model: sonnet
---

# PHP-CS-Fixer Skill

## Principe

Ce skill respecte les conventions du projet en détectant et utilisant les scripts
composer existants pour PHP-CS-Fixer. Il ne force jamais de règles arbitraires.

## Variables

```bash
TARGET="$ARGUMENTS"  # Fichier/dossier spécifique ou vide pour tout le projet
```

## Workflow

### Étape 0: Timing

```bash
START_TIME=$(date +%s)
date
```

### Étape 1: Détection des Scripts Composer

```bash
echo "🔍 Détection des scripts PHP-CS-Fixer du projet..."

# Vérifier présence composer.json
if [ ! -f "composer.json" ]; then
    echo "❌ Aucun composer.json trouvé"
    exit 1
fi

# Lister tous les scripts disponibles
echo ""
echo "📋 Scripts composer disponibles:"
jq -r '.scripts | keys[]' composer.json 2>/dev/null | while read script; do
    echo "  - $script"
done
```

### Étape 2: Identification des Scripts CS-Fixer

Analyser le composer.json pour identifier les scripts liés au code style.

**Patterns de scripts courants à détecter:**

Scripts dry-run (vérification):
- `cs`, `cs:check`, `cs-check`, `check:cs`
- `lint`, `lint:php`, `php:lint`
- `style`, `style:check`
- `phpcs`, `code-style`
- `fix:dry`, `cs:dry`

Scripts fix (correction):
- `cs:fix`, `cs-fix`, `fix:cs`, `fix`
- `style:fix`, `lint:fix`
- `phpcbf`, `code-style:fix`

```bash
# Extraire les scripts et leur commande
echo ""
echo "🔎 Recherche des scripts CS-Fixer..."

# Chercher scripts contenant php-cs-fixer ou phpcs
CS_SCRIPTS=$(jq -r '.scripts | to_entries[] | select(.value | type == "string" and (contains("php-cs-fixer") or contains("phpcs"))) | .key' composer.json 2>/dev/null)

if [ -z "$CS_SCRIPTS" ]; then
    # Chercher par nom de script courant
    CS_SCRIPTS=$(jq -r '.scripts | keys[] | select(test("^(cs|lint|style|phpcs|fix|code-style)"; "i"))' composer.json 2>/dev/null)
fi

if [ -z "$CS_SCRIPTS" ]; then
    echo "⚠️ Aucun script CS-Fixer détecté dans composer.json"
    echo ""
    echo "💡 Pour ajouter PHP-CS-Fixer au projet:"
    echo "   1. composer require --dev friendsofphp/php-cs-fixer"
    echo "   2. Créer .php-cs-fixer.dist.php avec vos règles"
    echo "   3. Ajouter dans composer.json:"
    echo '      "scripts": {'
    echo '          "cs": "php-cs-fixer fix --dry-run --diff",'
    echo '          "cs:fix": "php-cs-fixer fix"'
    echo '      }'
    exit 1
fi

echo "✅ Scripts CS-Fixer détectés:"
echo "$CS_SCRIPTS" | while read script; do
    CMD=$(jq -r ".scripts[\"$script\"]" composer.json 2>/dev/null)
    echo "  - $script: $CMD"
done
```

### Étape 3: TodoWrite Initialisation

```yaml
todos:
  - content: "Détecter scripts CS-Fixer du projet"
    status: "completed"
    activeForm: "Détection des scripts CS-Fixer"
  - content: "Exécuter vérification (dry-run)"
    status: "pending"
    activeForm: "Exécution de la vérification"
  - content: "Appliquer corrections si demandé"
    status: "pending"
    activeForm: "Application des corrections"
  - content: "Afficher rapport"
    status: "pending"
    activeForm: "Affichage du rapport"
```

### Étape 4: Sélection du Script

Identifier le script de vérification (dry-run) et le script de correction.

```bash
# Priorité pour dry-run: cs, cs:check, lint, style, phpcs
DRY_RUN_SCRIPT=""
for s in "cs" "cs:check" "cs-check" "lint" "style" "phpcs" "code-style"; do
    if echo "$CS_SCRIPTS" | grep -qx "$s"; then
        DRY_RUN_SCRIPT="$s"
        break
    fi
done

# Priorité pour fix: cs:fix, fix, cs-fix, style:fix, phpcbf
FIX_SCRIPT=""
for s in "cs:fix" "fix" "cs-fix" "fix:cs" "style:fix" "phpcbf" "code-style:fix"; do
    if echo "$CS_SCRIPTS" | grep -qx "$s"; then
        FIX_SCRIPT="$s"
        break
    fi
done

# Si pas de dry-run trouvé, utiliser le premier script avec --dry-run si possible
if [ -z "$DRY_RUN_SCRIPT" ] && [ -n "$FIX_SCRIPT" ]; then
    echo "ℹ️ Utilisation de 'composer $FIX_SCRIPT -- --dry-run' pour vérification"
    DRY_RUN_CMD="composer $FIX_SCRIPT -- --dry-run --diff"
else
    DRY_RUN_CMD="composer $DRY_RUN_SCRIPT"
fi

if [ -n "$FIX_SCRIPT" ]; then
    FIX_CMD="composer $FIX_SCRIPT"
else
    echo "⚠️ Aucun script de correction trouvé"
    echo "   La commande affichera uniquement les violations"
fi

echo ""
echo "📌 Scripts sélectionnés:"
echo "   Vérification: $DRY_RUN_CMD"
[ -n "$FIX_SCRIPT" ] && echo "   Correction: $FIX_CMD"
```

### Étape 5: Exécution Dry-Run

Marquer todo #2 `in_progress`.

```bash
echo ""
echo "🔍 Exécution de la vérification..."
echo ""

# Exécuter le script de vérification
$DRY_RUN_CMD 2>&1 | tee /tmp/cs-fixer-output.txt

# Vérifier le code de retour
EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Aucune violation de style détectée"
    echo "   Le code respecte les conventions du projet"
    exit 0
fi

echo ""
echo "📊 Des violations de style ont été détectées"
```

Marquer todo #2 `completed`.

### Étape 6: Demande de Confirmation

```bash
if [ -n "$FIX_SCRIPT" ]; then
    echo ""
    echo "❓ Voulez-vous appliquer les corrections automatiquement?"
    echo "   Commande: $FIX_CMD"
    echo ""
    echo "   Répondez 'oui' pour continuer ou 'non' pour annuler"
else
    echo ""
    echo "ℹ️ Aucun script de correction disponible"
    echo "   Corrigez manuellement ou ajoutez un script 'cs:fix' dans composer.json"
fi
```

**Note:** L'assistant doit demander confirmation à l'utilisateur avant de continuer.
Si l'utilisateur refuse ou si pas de script fix, afficher le rapport et terminer.

### Étape 7: Application des Corrections

Marquer todo #3 `in_progress`.

```bash
if [ -n "$FIX_SCRIPT" ]; then
    echo ""
    echo "🔧 Application des corrections..."
    echo "   Commande: $FIX_CMD"
    echo ""

    # Exécuter le script de correction
    $FIX_CMD 2>&1 | tee /tmp/cs-fixer-fix-output.txt

    EXIT_CODE=${PIPESTATUS[0]}

    if [ $EXIT_CODE -eq 0 ]; then
        echo ""
        echo "✅ Corrections appliquées avec succès"
    else
        echo ""
        echo "⚠️ Corrections appliquées (certaines erreurs peuvent persister)"
    fi
fi
```

Marquer todo #3 `completed`.

### Étape 8: Rapport Final

Marquer todo #4 `in_progress`.

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

echo ""
echo "═══════════════════════════════════════════════"
echo "📋 Résumé PHP-CS-Fixer"
echo "═══════════════════════════════════════════════"
echo ""
echo "   Script vérification: $DRY_RUN_CMD"
[ -n "$FIX_SCRIPT" ] && echo "   Script correction: $FIX_CMD"
echo "   Durée: $DURATION_STR"
echo ""

if [ -n "$FIX_SCRIPT" ]; then
    echo "💡 Conseil: Vérifiez les modifications avec 'git diff'"
    echo "   Puis committez avec: /git:commit \"style: apply PHP-CS-Fixer corrections\""
fi
```

Marquer todo #4 `completed`.

```yaml
task: "Correction de style PHP avec scripts composer"
status: "terminé"
details:
  dry_run_script: "$DRY_RUN_CMD"
  fix_script: "$FIX_CMD"
  execution_time: "$DURATION_STR"
next_steps:
  - "Vérifier les modifications avec git diff"
  - "Exécuter les tests pour valider"
  - "Committer les corrections de style"
```

## Scripts Composer Courants

### Patterns de nommage fréquents

**Vérification (dry-run):**
```json
{
    "scripts": {
        "cs": "php-cs-fixer fix --dry-run --diff",
        "cs:check": "php-cs-fixer fix --dry-run --diff",
        "lint": "php-cs-fixer fix --dry-run",
        "phpcs": "phpcs --standard=PSR12 src/",
        "style": "php-cs-fixer fix --dry-run --diff --verbose"
    }
}
```

**Correction:**
```json
{
    "scripts": {
        "cs:fix": "php-cs-fixer fix",
        "fix": "php-cs-fixer fix",
        "phpcbf": "phpcbf --standard=PSR12 src/",
        "style:fix": "php-cs-fixer fix --diff"
    }
}
```

### Configuration complète recommandée

```json
{
    "scripts": {
        "cs": "php-cs-fixer fix --dry-run --diff",
        "cs:fix": "php-cs-fixer fix --diff",
        "qa": [
            "@cs",
            "@phpstan"
        ]
    }
}
```

## Error Handling

- composer.json absent → ARRÊT avec message
- Aucun script CS-Fixer → ARRÊT avec instructions d'installation
- Script dry-run absent → Utilise script fix avec --dry-run
- Script fix absent → Affiche violations sans correction
- Erreur d'exécution → Affiche sortie complète

## Notes

- Respecte toujours les conventions du projet via composer.json
- Ne force jamais de règles arbitraires
- Détecte automatiquement les scripts existants
- Demande confirmation avant modification des fichiers
- Compatible avec php-cs-fixer et phpcs/phpcbf
- Marquer CHAQUE todo completed immédiatement après succès
