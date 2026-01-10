---
description: Crée une Pull Request optimisée avec workflow structuré
argument-hint: [branch-base] [milestone] [project] [--cd | --no-cd] [--no-interaction] [--delete] [--no-review]
hooks:
  PreToolUse:
    - matcher: "Bash(gh pr:*)"
      hooks:
        - type: command
          command: |
            # Hook 1: Vérification branche à jour avec origin
            BRANCH=$(git branch --show-current)
            echo "🔍 Vérification que $BRANCH est à jour avec origin..."

            git fetch origin "$BRANCH" 2>/dev/null || true

            LOCAL=$(git rev-parse "$BRANCH")
            REMOTE=$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "")

            if [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
              echo "⚠️  Attention : ta branche n'est pas à jour avec origin"
              echo "Lance : git pull origin $BRANCH"
              exit 1
            fi
          once: true
        - type: command
          command: "bash ${CLAUDE_PLUGIN_ROOT}/git/commands/scripts/qa-before-pr.sh"
          once: true
---

# Détection automatique du mode (Standard vs CD)

## Étape 1 : Vérifier les flags explicites

Analyser les arguments fournis :
- Si `--cd` présent → Utiliser skill `git-cd-pr`
- Si `--no-cd` présent → Utiliser skill `git-pr`
- Sinon → Passer à l'étape 2

## Étape 2 : Détection automatique

Exécuter le script de détection (NE PAS modifier ou tronquer la commande) :

```bash
bash "${CLAUDE_PLUGIN_ROOT}/commands/scripts/detect_cd_mode.sh"
```

Le script analyse TOUS les labels du repo (pas de troncature avec head/tail).

- Si output = `CD_DETECTED` → Utiliser skill `git-cd-pr`
- Si output = `STANDARD` → Utiliser skill `git-pr`

## Étape 3 : Invoquer le skill approprié

### Mode Standard (git-pr)
- Template PR : `.github/PULL_REQUEST_TEMPLATE/default.md`
- Pas de labels version automatiques

### Mode CD (git-cd-pr)
- Template PR : `.github/PULL_REQUEST_TEMPLATE/cd_pull_request_template.md`
- Labels version:major/minor/patch automatiques
- Copie des labels depuis l'issue liée
- Détection feature flags

## Arguments transmis au skill

Transmettre tous les arguments sauf `--cd` et `--no-cd` au skill sélectionné.
