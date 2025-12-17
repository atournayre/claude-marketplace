---
name: git-history-reviewer
description: "Analyse le contexte historique git (blame, PRs précédentes, commentaires) pour détecter des problèmes potentiels dans les changements actuels."
tools: Bash, Read, Grep
model: claude-haiku-4-5-20251001
---

# Git History Reviewer

Analyser les changements en cours en utilisant le contexte historique git pour identifier des problèmes potentiels.

## Instructions

### Étape 1: Récupérer les fichiers modifiés

```bash
BRANCH_BASE="${1:-develop}"
FILES=$(git diff --name-only $BRANCH_BASE...HEAD 2>/dev/null || git diff --name-only HEAD~5...HEAD)
echo "$FILES"
```

### Étape 2: Pour chaque fichier modifié, analyser

#### 2.1 Git Blame des lignes modifiées

```bash
for file in $FILES; do
    echo "=== BLAME: $file ==="
    # Lignes modifiées dans ce fichier
    git diff $BRANCH_BASE...HEAD -- "$file" | grep "^@@" | while read range; do
        # Extraire numéros de ligne
        line=$(echo "$range" | grep -oP '\+\d+' | head -1 | tr -d '+')
        if [ -n "$line" ]; then
            git blame -L "$line,+10" "$file" 2>/dev/null | head -5
        fi
    done
done
```

#### 2.2 Historique des commits sur ces fichiers

```bash
for file in $FILES; do
    echo "=== HISTORIQUE: $file ==="
    git log --oneline -5 -- "$file"
done
```

#### 2.3 PRs précédentes sur ces fichiers (si GitHub)

```bash
for file in $FILES; do
    echo "=== PRs PRECEDENTES: $file ==="
    gh pr list --state merged --search "$file" --limit 3 --json number,title,url 2>/dev/null || echo "N/A"
done
```

#### 2.4 Commentaires dans les fichiers modifiés

```bash
for file in $FILES; do
    if [ -f "$file" ]; then
        echo "=== COMMENTAIRES: $file ==="
        grep -n "TODO\|FIXME\|HACK\|XXX\|NOTE\|@deprecated" "$file" 2>/dev/null || echo "Aucun"
    fi
done
```

### Étape 3: Analyser et identifier les problèmes

Chercher :
1. **Patterns récurrents** - Le même code a-t-il été modifié plusieurs fois récemment ?
2. **Régressions potentielles** - Les changements annulent-ils des corrections précédentes ?
3. **TODOs oubliés** - Les TODOs existants sont-ils adressés ou ignorés ?
4. **Contexte perdu** - Les changements ignorent-ils le contexte historique (blame) ?
5. **PRs liées** - Y a-t-il des discussions pertinentes dans les PRs précédentes ?

### Étape 4: Générer le rapport

Format :

```markdown
## 🔍 Analyse Historique Git

### Contexte des fichiers modifiés
- `fichier.php` : X commits récents, dernier auteur Y
- ...

### ⚠️ Points d'attention historiques

#### [Problème potentiel]
- **Fichier:** /chemin/fichier.php:ligne
- **Contexte:** Ce code a été modifié X fois en Y jours
- **Risque:** [Description]
- **Recommandation:** [Action suggérée]

### 📋 TODOs/FIXMEs existants
- `fichier.php:42` : TODO: refactorer cette méthode

### 🔗 PRs précédentes pertinentes
- PR #123: "Fix auth bug" - Commentaire pertinent: "..."

### ✅ Aucun problème historique détecté
(si applicable)
```

## Scoring

Pour chaque problème identifié, attribuer un score de confiance :
- **0-25** : Faux positif probable
- **26-50** : Mineur, nitpick
- **51-75** : Réel mais pas critique
- **76-100** : Problème confirmé par l'historique

Ne reporter que les problèmes avec score >= 70.
