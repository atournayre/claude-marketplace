---
name: cs-fixer
description: >
  Analyse et corrige automatiquement le style de code PHP en utilisant les scripts
  du projet (Makefile ou composer.json). Détecte automatiquement les commandes
  CS-Fixer définies et les utilise pour respecter les conventions du projet.
allowed-tools: [Bash, Read, Grep, Glob, TodoWrite]
model: sonnet
---

# PHP-CS-Fixer Skill

## Principe

Ce skill respecte les conventions du projet en détectant et utilisant les commandes
existantes pour PHP-CS-Fixer. Il cherche d'abord dans le Makefile, puis dans
composer.json. Il ne force jamais de règles arbitraires.

## Variables

```bash
TARGET="$ARGUMENTS"  # Fichier/dossier spécifique ou vide pour tout le projet
TOOL_TYPE=""         # "make" ou "composer"
DRY_RUN_CMD=""       # Commande de vérification
FIX_CMD=""           # Commande de correction
```

## Workflow

### Étape 0: Timing

```bash
START_TIME=$(date +%s)
date
```

### Étape 1: Détection des Commandes du Projet

```bash
echo "🔍 Détection des commandes CS-Fixer du projet..."
echo ""

MAKEFILE_FOUND=false
COMPOSER_FOUND=false

# Vérifier présence Makefile
if [ -f "Makefile" ] || [ -f "makefile" ]; then
    MAKEFILE_FOUND=true
    echo "📄 Makefile détecté"
fi

# Vérifier présence composer.json
if [ -f "composer.json" ]; then
    COMPOSER_FOUND=true
    echo "📄 composer.json détecté"
fi

if [ "$MAKEFILE_FOUND" = false ] && [ "$COMPOSER_FOUND" = false ]; then
    echo "❌ Aucun Makefile ni composer.json trouvé"
    exit 1
fi
```

### Étape 2: Recherche dans le Makefile (prioritaire)

Si un Makefile existe, chercher les targets liées au code style.

**Patterns de targets make courants:**

Vérification (dry-run):
- `cs`, `cs-check`, `check-cs`, `lint`, `style`, `phpcs`, `code-style`
- `cs.check`, `lint.php`, `style.check`

Correction:
- `cs-fix`, `fix-cs`, `cs.fix`, `fix`, `style-fix`, `phpcbf`

```bash
if [ "$MAKEFILE_FOUND" = true ]; then
    echo ""
    echo "🔎 Recherche des targets make CS-Fixer..."

    # Extraire les targets du Makefile
    MAKE_TARGETS=$(grep -E '^[a-zA-Z_-]+[a-zA-Z0-9_.-]*:' Makefile 2>/dev/null | sed 's/:.*//' | sort -u)

    echo ""
    echo "📋 Targets make disponibles:"
    echo "$MAKE_TARGETS" | while read target; do
        echo "  - $target"
    done

    # Chercher targets CS-Fixer par nom
    CS_MAKE_TARGETS=$(echo "$MAKE_TARGETS" | grep -iE '^(cs|lint|style|phpcs|phpcbf|fix|code-style)' || true)

    # Ou chercher targets contenant php-cs-fixer dans leur commande
    if [ -z "$CS_MAKE_TARGETS" ]; then
        CS_MAKE_TARGETS=$(grep -B1 'php-cs-fixer\|phpcs\|phpcbf' Makefile 2>/dev/null | grep -E '^[a-zA-Z_-]+:' | sed 's/:.*//' || true)
    fi

    if [ -n "$CS_MAKE_TARGETS" ]; then
        TOOL_TYPE="make"
        echo ""
        echo "✅ Targets CS-Fixer détectées:"
        echo "$CS_MAKE_TARGETS" | while read target; do
            echo "  - make $target"
        done

        # Sélectionner dry-run target
        for t in "cs" "cs-check" "check-cs" "lint" "style" "phpcs" "code-style" "cs.check"; do
            if echo "$CS_MAKE_TARGETS" | grep -qx "$t"; then
                DRY_RUN_CMD="make $t"
                break
            fi
        done

        # Sélectionner fix target
        for t in "cs-fix" "fix-cs" "cs.fix" "fix" "style-fix" "phpcbf" "code-style-fix"; do
            if echo "$CS_MAKE_TARGETS" | grep -qx "$t"; then
                FIX_CMD="make $t"
                break
            fi
        done
    fi
fi
```

### Étape 3: Recherche dans composer.json (fallback)

Si pas de targets make trouvées, chercher dans composer.json.

```bash
if [ -z "$TOOL_TYPE" ] && [ "$COMPOSER_FOUND" = true ]; then
    echo ""
    echo "🔎 Recherche des scripts composer CS-Fixer..."

    # Lister tous les scripts disponibles
    COMPOSER_SCRIPTS=$(jq -r '.scripts | keys[]' composer.json 2>/dev/null)

    echo ""
    echo "📋 Scripts composer disponibles:"
    echo "$COMPOSER_SCRIPTS" | while read script; do
        echo "  - $script"
    done

    # Chercher scripts contenant php-cs-fixer ou phpcs
    CS_COMPOSER_SCRIPTS=$(jq -r '.scripts | to_entries[] | select(.value | type == "string" and (contains("php-cs-fixer") or contains("phpcs"))) | .key' composer.json 2>/dev/null)

    if [ -z "$CS_COMPOSER_SCRIPTS" ]; then
        # Chercher par nom de script courant
        CS_COMPOSER_SCRIPTS=$(echo "$COMPOSER_SCRIPTS" | grep -iE '^(cs|lint|style|phpcs|phpcbf|fix|code-style)' || true)
    fi

    if [ -n "$CS_COMPOSER_SCRIPTS" ]; then
        TOOL_TYPE="composer"
        echo ""
        echo "✅ Scripts CS-Fixer détectés:"
        echo "$CS_COMPOSER_SCRIPTS" | while read script; do
            CMD=$(jq -r ".scripts[\"$script\"]" composer.json 2>/dev/null)
            echo "  - composer $script: $CMD"
        done

        # Sélectionner dry-run script
        for s in "cs" "cs:check" "cs-check" "lint" "style" "phpcs" "code-style"; do
            if echo "$CS_COMPOSER_SCRIPTS" | grep -qx "$s"; then
                DRY_RUN_CMD="composer $s"
                break
            fi
        done

        # Sélectionner fix script
        for s in "cs:fix" "cs-fix" "fix:cs" "fix" "style:fix" "phpcbf" "code-style:fix"; do
            if echo "$CS_COMPOSER_SCRIPTS" | grep -qx "$s"; then
                FIX_CMD="composer $s"
                break
            fi
        done
    fi
fi
```

### Étape 4: Aucune Commande Trouvée

```bash
if [ -z "$TOOL_TYPE" ]; then
    echo ""
    echo "⚠️ Aucune commande CS-Fixer détectée"
    echo ""
    echo "💡 Pour ajouter PHP-CS-Fixer au projet:"
    echo ""
    echo "   Option 1 - Makefile:"
    echo "   ─────────────────────"
    echo "   cs:                                        ## Check code style"
    echo "   	php-cs-fixer fix --dry-run --diff"
    echo ""
    echo "   cs-fix:                                    ## Fix code style"
    echo "   	php-cs-fixer fix"
    echo ""
    echo "   Option 2 - composer.json:"
    echo "   ──────────────────────────"
    echo '   "scripts": {'
    echo '       "cs": "php-cs-fixer fix --dry-run --diff",'
    echo '       "cs:fix": "php-cs-fixer fix"'
    echo '   }'
    exit 1
fi
```

### Étape 5: TodoWrite Initialisation

```yaml
todos:
  - content: "Détecter commandes CS-Fixer du projet"
    status: "completed"
    activeForm: "Détection des commandes CS-Fixer"
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

### Étape 6: Affichage des Commandes Sélectionnées

```bash
echo ""
echo "📌 Commandes sélectionnées ($TOOL_TYPE):"
[ -n "$DRY_RUN_CMD" ] && echo "   Vérification: $DRY_RUN_CMD"
[ -n "$FIX_CMD" ] && echo "   Correction: $FIX_CMD"

# Si pas de dry-run mais fix disponible, utiliser fix avec --dry-run
if [ -z "$DRY_RUN_CMD" ] && [ -n "$FIX_CMD" ]; then
    echo "ℹ️ Utilisation de '$FIX_CMD -- --dry-run' pour vérification"
    DRY_RUN_CMD="$FIX_CMD -- --dry-run --diff"
fi
```

### Étape 7: Exécution Dry-Run

Marquer todo #2 `in_progress`.

```bash
echo ""
echo "🔍 Exécution de la vérification..."
echo "   Commande: $DRY_RUN_CMD"
echo ""

# Exécuter la commande de vérification
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

### Étape 8: Demande de Confirmation

```bash
if [ -n "$FIX_CMD" ]; then
    echo ""
    echo "❓ Voulez-vous appliquer les corrections automatiquement?"
    echo "   Commande: $FIX_CMD"
    echo ""
    echo "   Répondez 'oui' pour continuer ou 'non' pour annuler"
else
    echo ""
    echo "ℹ️ Aucune commande de correction disponible"
    echo "   Ajoutez une target 'cs-fix' dans Makefile ou 'cs:fix' dans composer.json"
fi
```

**Note:** L'assistant doit demander confirmation à l'utilisateur avant de continuer.
Si l'utilisateur refuse ou si pas de commande fix, afficher le rapport et terminer.

### Étape 9: Application des Corrections

Marquer todo #3 `in_progress`.

```bash
if [ -n "$FIX_CMD" ]; then
    echo ""
    echo "🔧 Application des corrections..."
    echo "   Commande: $FIX_CMD"
    echo ""

    # Exécuter la commande de correction
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

### Étape 10: Rapport Final

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
echo "   Outil: $TOOL_TYPE"
echo "   Vérification: $DRY_RUN_CMD"
[ -n "$FIX_CMD" ] && echo "   Correction: $FIX_CMD"
echo "   Durée: $DURATION_STR"
echo ""

if [ -n "$FIX_CMD" ]; then
    echo "💡 Conseil: Vérifiez les modifications avec 'git diff'"
    echo "   Puis committez avec: /git:commit \"style: apply PHP-CS-Fixer corrections\""
fi
```

Marquer todo #4 `completed`.

```yaml
task: "Correction de style PHP"
status: "terminé"
details:
  tool_type: "$TOOL_TYPE"
  dry_run_cmd: "$DRY_RUN_CMD"
  fix_cmd: "$FIX_CMD"
  execution_time: "$DURATION_STR"
next_steps:
  - "Vérifier les modifications avec git diff"
  - "Exécuter les tests pour valider"
  - "Committer les corrections de style"
```

## Exemples de Configuration

### Makefile

```makefile
.PHONY: cs cs-fix

cs:                                         ## Check code style
	php-cs-fixer fix --dry-run --diff

cs-fix:                                     ## Fix code style
	php-cs-fixer fix

# Ou avec phpcs/phpcbf
lint:                                       ## Check code style (phpcs)
	phpcs --standard=PSR12 src/

fix:                                        ## Fix code style (phpcbf)
	phpcbf --standard=PSR12 src/
```

### composer.json

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

## Ordre de Priorité

1. **Makefile** (prioritaire) - Si un Makefile existe avec des targets CS-Fixer
2. **composer.json** (fallback) - Si pas de Makefile ou pas de targets trouvées

## Patterns Détectés

### Targets Make
- Vérification: `cs`, `cs-check`, `check-cs`, `lint`, `style`, `phpcs`, `code-style`
- Correction: `cs-fix`, `fix-cs`, `fix`, `style-fix`, `phpcbf`, `code-style-fix`

### Scripts Composer
- Vérification: `cs`, `cs:check`, `cs-check`, `lint`, `style`, `phpcs`, `code-style`
- Correction: `cs:fix`, `cs-fix`, `fix:cs`, `fix`, `style:fix`, `phpcbf`, `code-style:fix`

## Error Handling

- Ni Makefile ni composer.json → ARRÊT avec message
- Aucune commande CS-Fixer → ARRÊT avec instructions d'installation
- Commande dry-run absente → Utilise commande fix avec --dry-run
- Commande fix absente → Affiche violations sans correction
- Erreur d'exécution → Affiche sortie complète

## Notes

- Respecte toujours les conventions du projet
- Priorité au Makefile sur composer.json
- Ne force jamais de règles arbitraires
- Détecte automatiquement les commandes existantes
- Demande confirmation avant modification des fichiers
- Compatible avec php-cs-fixer et phpcs/phpcbf
- Marquer CHAQUE todo completed immédiatement après succès
