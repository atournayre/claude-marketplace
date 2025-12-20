# Template Code Review Automatique

## Format du commentaire PR

```markdown
## 🔍 Code Review Automatique

### ✅ Points positifs
- [ce qui est bien fait - agrégé des agents]

### 🚨 Issues critiques (score >= 90)
- [issues de code-reviewer]
- [issues de silent-failure-hunter]

### ⚠️ Points d'attention (score 80-89)
- [issues des agents avec score 80-89]

### 🧪 Couverture tests
- [résumé de test-analyzer]
- [tests manquants critiques]

### 📜 Contexte historique
- [insights de git-history-reviewer]
- [TODOs/FIXMEs existants]
- [PRs précédentes pertinentes]

### 💡 Suggestions
- [améliorations proposées par les agents]

### 📋 Checklist conformité
- [ ] CLAUDE.md respecté
- [ ] Pas d'erreurs silencieuses
- [ ] Tests suffisants
- [ ] TODOs adressés

---
*Review générée par 4 agents spécialisés via git-pr skill*
```

## Agents de review

### 1. code-reviewer
- **Focus**: Conformité CLAUDE.md, bugs, qualité code
- **Prompt**: "Review les changements de la PR #$PR_NUMBER. Fichiers : $(git diff --name-only $BRANCH_BASE...$BRANCH_NAME)"

### 2. silent-failure-hunter
- **Focus**: Catch vides, erreurs silencieuses, fallbacks dangereux
- **Prompt**: "Analyse la gestion d'erreurs dans les fichiers modifiés de la branche actuelle"

### 3. test-analyzer
- **Focus**: Tests manquants, qualité des tests, edge cases
- **Prompt**: "Analyse la couverture de tests pour les changements de la branche actuelle vs $BRANCH_BASE"

### 4. git-history-reviewer
- **Focus**: Blame, PRs précédentes, TODOs existants
- **Prompt**: "Analyse le contexte historique des fichiers modifiés dans la branche actuelle"

## Filtrage des résultats

Seules les issues avec **score >= 80** sont incluses dans le rapport.

| Score | Niveau | Action |
|-------|--------|--------|
| >= 90 | Critique | Bloquant, à corriger avant merge |
| 80-89 | Attention | À considérer, non bloquant |
| < 80 | Info | Ignoré dans le rapport |
