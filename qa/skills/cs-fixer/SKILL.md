---
name: cs-fixer
description: >
  Analyse et corrige automatiquement le style de code PHP avec PHP-CS-Fixer.
  Détecte les violations de style, applique les corrections automatiques,
  et génère un rapport détaillé des modifications effectuées.
allowed-tools: [Bash, Read, Grep, Glob, TodoWrite]
model: sonnet
---

# PHP-CS-Fixer Skill

## Variables

```bash
CS_FIXER_BIN="./vendor/bin/php-cs-fixer"
CS_FIXER_CONFIG=".php-cs-fixer.dist.php"  # ou .php-cs-fixer.php
TARGET="$ARGUMENTS"  # Fichier/dossier spécifique ou vide pour tout le projet
```

## Workflow

### Étape 0: Timing

```bash
START_TIME=$(date +%s)
date
```

### Étape 1: Vérification Environnement

```bash
# Vérifier PHP-CS-Fixer installé
if [ ! -f "$CS_FIXER_BIN" ]; then
    # Essayer chemin global
    if command -v php-cs-fixer &> /dev/null; then
        CS_FIXER_BIN="php-cs-fixer"
    else
        echo "❌ PHP-CS-Fixer non trouvé"
        echo "   Installation: composer require --dev friendsofphp/php-cs-fixer"
        exit 1
    fi
fi

# Vérifier config PHP-CS-Fixer
if [ ! -f "$CS_FIXER_CONFIG" ] && [ ! -f ".php-cs-fixer.php" ]; then
    echo "⚠️ Configuration PHP-CS-Fixer non trouvée"
    echo "   Utilisation des règles par défaut (@Symfony)"
    CS_FIXER_CONFIG=""
else
    # Utiliser .php-cs-fixer.php si .php-cs-fixer.dist.php absent
    if [ ! -f "$CS_FIXER_CONFIG" ]; then
        CS_FIXER_CONFIG=".php-cs-fixer.php"
    fi
    echo "✅ Configuration: $CS_FIXER_CONFIG"
fi

echo "✅ Environnement PHP-CS-Fixer valide"
```

### Étape 2: TodoWrite Initialisation

```yaml
todos:
  - content: "Vérifier environnement PHP-CS-Fixer"
    status: "completed"
    activeForm: "Vérification de l'environnement"
  - content: "Analyser violations de style (dry-run)"
    status: "pending"
    activeForm: "Analyse des violations de style"
  - content: "Appliquer corrections automatiques"
    status: "pending"
    activeForm: "Application des corrections"
  - content: "Générer rapport des modifications"
    status: "pending"
    activeForm: "Génération du rapport"
```

### Étape 3: Analyse Dry-Run

Marquer todo #2 `in_progress`.

```bash
echo "🔍 Analyse des violations de style..."

# Déterminer la cible
if [ -n "$TARGET" ]; then
    TARGET_PATH="$TARGET"
    echo "   Cible: $TARGET_PATH"
else
    TARGET_PATH="src"
    echo "   Cible: $TARGET_PATH (par défaut)"
fi

# Exécuter en mode dry-run pour voir les violations
if [ -n "$CS_FIXER_CONFIG" ]; then
    $CS_FIXER_BIN fix "$TARGET_PATH" --config="$CS_FIXER_CONFIG" --dry-run --diff --format=json > /tmp/cs-fixer-dry-run.json 2>&1
else
    $CS_FIXER_BIN fix "$TARGET_PATH" --rules=@Symfony --dry-run --diff --format=json > /tmp/cs-fixer-dry-run.json 2>&1
fi

# Parser résultat
TOTAL_FILES=$(jq '.files | length' /tmp/cs-fixer-dry-run.json 2>/dev/null || echo "0")

if [ "$TOTAL_FILES" -eq 0 ]; then
    echo "✅ Aucune violation de style détectée"
    exit 0
fi

echo "📊 Fichiers avec violations: $TOTAL_FILES"

# Lister fichiers affectés
echo ""
echo "📁 Fichiers à corriger:"
jq -r '.files[].name' /tmp/cs-fixer-dry-run.json 2>/dev/null | while read file; do
    echo "  - $file"
done
```

Marquer todo #2 `completed`.

### Étape 4: Demande de Confirmation

```bash
echo ""
echo "❓ Voulez-vous appliquer les corrections automatiquement?"
echo "   (Les fichiers seront modifiés)"
echo ""
echo "   Répondez 'oui' pour continuer ou 'non' pour annuler"
```

**Note:** L'assistant doit demander confirmation à l'utilisateur avant de continuer.
Si l'utilisateur refuse, afficher le rapport dry-run et terminer.

### Étape 5: Application des Corrections

Marquer todo #3 `in_progress`.

```bash
echo "🔧 Application des corrections..."

# Exécuter PHP-CS-Fixer en mode correction
if [ -n "$CS_FIXER_CONFIG" ]; then
    $CS_FIXER_BIN fix "$TARGET_PATH" --config="$CS_FIXER_CONFIG" --diff --format=json > /tmp/cs-fixer-fix.json 2>&1
else
    $CS_FIXER_BIN fix "$TARGET_PATH" --rules=@Symfony --diff --format=json > /tmp/cs-fixer-fix.json 2>&1
fi

# Compter fichiers corrigés
FIXED_FILES=$(jq '.files | length' /tmp/cs-fixer-fix.json 2>/dev/null || echo "0")

echo "✅ $FIXED_FILES fichier(s) corrigé(s)"
```

Marquer todo #3 `completed`.

### Étape 6: Génération du Rapport

Marquer todo #4 `in_progress`.

```bash
echo ""
echo "📊 Rapport des corrections:"
echo ""

# Détailler les modifications par fichier
jq -r '.files[] | "📝 \(.name)\n   Règles appliquées: \(.appliedFixers | join(", "))"' /tmp/cs-fixer-fix.json 2>/dev/null

# Statistiques des règles
echo ""
echo "📈 Règles les plus appliquées:"
jq -r '[.files[].appliedFixers[]] | group_by(.) | map({rule: .[0], count: length}) | sort_by(-.count) | .[:10][] | "  - \(.rule): \(.count) fois"' /tmp/cs-fixer-fix.json 2>/dev/null
```

Marquer todo #4 `completed`.

### Étape 7: Rapport Final

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
echo "   Fichiers analysés: $(find "$TARGET_PATH" -name '*.php' 2>/dev/null | wc -l)"
echo "   Fichiers corrigés: $FIXED_FILES"
echo "   Durée: $DURATION_STR"
echo ""

if [ "$FIXED_FILES" -gt 0 ]; then
    echo "💡 Conseil: Vérifiez les modifications avec 'git diff'"
    echo "   Puis committez avec: /git:commit \"style: apply PHP-CS-Fixer corrections\""
fi
```

```yaml
task: "Correction de style PHP avec PHP-CS-Fixer"
status: "terminé"
details:
  files_analyzed: "[Nombre de fichiers PHP]"
  files_fixed: $FIXED_FILES
  execution_time: "$DURATION_STR"
  config: "$CS_FIXER_CONFIG"
rules_applied:
  - [Liste des règles appliquées]
files_modified:
  - [Liste des fichiers modifiés]
next_steps:
  - "Vérifier les modifications avec git diff"
  - "Exécuter les tests pour valider"
  - "Committer les corrections de style"
```

## Règles PHP-CS-Fixer Courantes

### Règles @Symfony (par défaut)
- `array_syntax` - Syntaxe array courte `[]`
- `blank_line_after_namespace` - Ligne vide après namespace
- `blank_line_after_opening_tag` - Ligne vide après `<?php`
- `braces` - Position des accolades
- `class_definition` - Espacement définition classe
- `concat_space` - Espaces autour de concaténation
- `declare_strict_types` - Ajout déclaration strict_types
- `function_declaration` - Espacement déclaration fonction
- `indentation_type` - Type d'indentation (spaces)
- `line_ending` - Fin de ligne Unix
- `lowercase_keywords` - Mots-clés en minuscules
- `method_argument_space` - Espacement arguments
- `no_closing_tag` - Pas de `?>` final
- `no_empty_statement` - Pas de statements vides
- `no_extra_blank_lines` - Pas de lignes vides superflues
- `no_trailing_whitespace` - Pas d'espaces en fin de ligne
- `no_unused_imports` - Pas d'imports non utilisés
- `ordered_imports` - Imports triés
- `phpdoc_align` - Alignement PHPDoc
- `phpdoc_order` - Ordre des annotations PHPDoc
- `phpdoc_scalar` - Types scalaires PHPDoc
- `phpdoc_separation` - Séparation PHPDoc
- `phpdoc_trim` - Trim PHPDoc
- `single_blank_line_at_eof` - Ligne vide en fin de fichier
- `single_class_element_per_statement` - Un élément par statement
- `single_import_per_statement` - Un import par statement
- `single_line_after_imports` - Ligne après imports
- `single_quote` - Guillemets simples
- `trailing_comma_in_multiline` - Virgule finale multiline
- `trim_array_spaces` - Trim espaces array
- `visibility_required` - Visibilité requise
- `whitespace_after_comma_in_array` - Espace après virgule array

## Configuration Recommandée

Exemple `.php-cs-fixer.dist.php`:

```php
<?php

$finder = (new PhpCsFixer\Finder())
    ->in(__DIR__)
    ->exclude('var')
    ->exclude('vendor')
    ->exclude('node_modules')
;

return (new PhpCsFixer\Config())
    ->setRules([
        '@Symfony' => true,
        '@Symfony:risky' => true,
        'array_syntax' => ['syntax' => 'short'],
        'declare_strict_types' => true,
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'no_unused_imports' => true,
        'trailing_comma_in_multiline' => true,
        'phpdoc_order' => true,
        'strict_param' => true,
        'strict_comparison' => true,
    ])
    ->setFinder($finder)
    ->setRiskyAllowed(true)
;
```

## Error Handling

- PHP-CS-Fixer non trouvé → ARRÊT avec instructions d'installation
- Config absente → Utilise règles @Symfony par défaut
- Erreur d'analyse → Affiche erreur et continue autres fichiers
- Permissions → Vérifie droits d'écriture avant correction

## Notes

- Demande confirmation avant modification des fichiers
- Support des règles @Symfony, @PSR12, @PhpCsFixer
- Compatible avec configurations personnalisées
- Génère rapport détaillé des règles appliquées
- Marquer CHAQUE todo completed immédiatement après succès
