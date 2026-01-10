---
description: Implémenter selon le plan (Phase 5)
argument-hint: [path-to-plan]
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: |
            # Hook 3: Vérifier qu'on a un plan à suivre
            if [ -f ".claude/data/.dev-workflow-state.json" ]; then
              PLAN_PATH=$(jq -r '.planPath // empty' .claude/data/.dev-workflow-state.json 2>/dev/null || echo "")
              if [ -z "$PLAN_PATH" ] || [ ! -f "$PLAN_PATH" ]; then
                echo "❌ ERREUR : Aucun plan trouvé"
                echo "Lance d'abord : /dev:plan"
                exit 1
              fi
            fi
          once: true
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: |
            # Hook 1: PHPStan après chaque Edit (fichiers PHP uniquement)
            # Extraction du chemin de fichier depuis les arguments de l'outil
            FILE=$(echo "$CLAUDE_TOOL_ARGS" | grep -oP '(?<=file_path: ).*?(?=,|$)' || echo "")

            if [ -n "$FILE" ] && [[ "$FILE" == *.php ]]; then
              echo "🔍 Vérification PHPStan de $FILE..."

              # Détection méthode PHPStan disponible
              if [ -f "Makefile" ] && grep -q "^phpstan:" Makefile; then
                make phpstan FILES="$FILE" 2>/dev/null || vendor/bin/phpstan analyse "$FILE" --level=9 --no-progress 2>/dev/null || echo "⚠️  PHPStan non disponible"
              elif [ -f "vendor/bin/phpstan" ]; then
                vendor/bin/phpstan analyse "$FILE" --level=9 --no-progress || {
                  echo "⚠️  Erreurs PHPStan détectées dans $FILE"
                  echo "Corrige-les avant de continuer"
                }
              fi
            fi
          once: false
    - matcher: "Write"
      hooks:
        - type: command
          command: |
            # Hook 2: Auto-format après Write (fichiers PHP uniquement)
            FILE=$(echo "$CLAUDE_TOOL_ARGS" | grep -oP '(?<=file_path: ).*?(?=,|$)' || echo "")

            if [ -n "$FILE" ] && [[ "$FILE" == *.php ]] && [ -f "$FILE" ]; then
              echo "🎨 Auto-formatage PSR-12 de $FILE..."

              if [ -f "vendor/bin/php-cs-fixer" ]; then
                vendor/bin/php-cs-fixer fix "$FILE" --rules=@PSR12 --quiet 2>/dev/null && echo "✅ Formaté : $FILE" || echo "⚠️  Formatage ignoré"
              elif [ -f "Makefile" ] && grep -q "^fix:" Makefile; then
                make fix FILES="$FILE" 2>/dev/null || echo "⚠️  Formatage ignoré"
              fi
            fi
          once: false
---

# Objectif

Phase 5 du workflow de développement : implémenter la feature selon le plan généré.

# Variables

PATH_TO_PLAN: $ARGUMENTS

# Instructions

## 1. Vérifier le contexte

- Si `PATH_TO_PLAN` non fourni, chercher dans `.claude/data/.dev-workflow-state.json` le `planPath`
- Si toujours pas de plan, demander à l'utilisateur :
  ```
  ⚠️ Aucun plan trouvé.

  Usage : /dev:code docs/specs/feature-xxx.md

  Ou lance le workflow complet : /dev:feature <description>
  ```

## 2. Demander approbation

⚠️ **CRITIQUE : Ne PAS commencer l'implémentation sans approbation explicite.**

```
📋 Plan à implémenter : {PATH_TO_PLAN}

Résumé des étapes :
1. {étape 1}
2. {étape 2}
...

Prêt à implémenter ?
```

Attendre confirmation avant de continuer.

## 3. Lire le plan

- Lire le fichier plan complet
- Extraire les étapes d'implémentation
- Identifier les fichiers à créer/modifier

## 4. Implémenter étape par étape

Pour chaque étape du plan :

1. **Créer une todo** pour l'étape
2. **Lire les fichiers** concernés (si modification)
3. **Implémenter** le code
4. **Respecter** :
   - Les conventions du projet (CLAUDE.md)
   - Les patterns identifiés dans l'exploration
   - Les décisions prises en phase 2
5. **Marquer la todo** comme complétée

## 5. Créer les tests

- Créer les tests unitaires spécifiés dans le plan
- Suivre l'approche TDD si possible
- S'assurer que les tests passent

## 6. Vérifications qualité

Lancer les vérifications :

```bash
make phpstan    # PHPStan niveau 9
make fix        # Formatage PSR-12
```

⚠️ **Corriger TOUTES les erreurs PHPStan avant de continuer.**

## 7. Mettre à jour le workflow state

```json
{
  "currentPhase": 5,
  "phases": {
    "5": {
      "status": "completed",
      "completedAt": "{timestamp}",
      "filesCreated": ["{liste}"],
      "filesModified": ["{liste}"],
      "testsCreated": ["{liste}"]
    }
  }
}
```

## 8. Rapport

```
✅ Implémentation terminée

**Fichiers créés :**
- `{fichier}` : {description}

**Fichiers modifiés :**
- `{fichier}` : {description}

**Tests créés :**
- `{fichier}` : {description}

**Vérifications :**
- PHPStan : ✅ 0 erreurs
- PSR-12 : ✅ Formaté

Prochaine étape : /dev:review pour la review qualité
```

# Règles

- **Approbation obligatoire** avant de commencer
- **PHPStan = 0 erreurs** (bloquant CI)
- Respecter le **plan** (pas d'improvisation)
- **Tests** pour chaque composant
- **Conventions françaises** pour les variables et documentation
