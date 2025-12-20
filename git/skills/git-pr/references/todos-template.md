# Template TodoWrite pour git-pr

## Todos initiaux

```yaml
todos:
  - content: "Vérifier template PR"
    status: "pending"
    activeForm: "Vérification du template PR"
  - content: "Lancer QA intelligente"
    status: "pending"
    activeForm: "Lancement de la QA intelligente"
  - content: "Analyser changements git"
    status: "pending"
    activeForm: "Analyse des changements git"
  - content: "Confirmer branche de base"
    status: "pending"
    activeForm: "Confirmation de la branche de base"
  - content: "Générer description PR intelligente"
    status: "pending"
    activeForm: "Génération de la description PR intelligente"
  - content: "Push et création PR"
    status: "pending"
    activeForm: "Push et création de la PR"
  - content: "Assigner milestone"
    status: "pending"
    activeForm: "Assignation du milestone"
  - content: "Assigner projet GitHub"
    status: "pending"
    activeForm: "Assignation du projet GitHub"
  - content: "Code review automatique"
    status: "pending"
    activeForm: "Code review automatique"
  - content: "Nettoyage branche locale"
    status: "pending"
    activeForm: "Nettoyage de la branche locale"
```

## Génération description PR intelligente

### Informations à récupérer

```bash
BRANCH_NAME=$(git branch --show-current)
echo "=== COMMITS ==="
git log $BRANCH_BASE..$BRANCH_NAME --oneline
echo ""
echo "=== DIFF STAT ==="
git diff $BRANCH_BASE..$BRANCH_NAME --stat
echo ""
echo "=== FICHIERS MODIFIÉS ==="
git diff $BRANCH_BASE..$BRANCH_NAME --name-only
```

### Remplissage du template PR

1. Lire le template PR avec Read tool : `$PR_TEMPLATE_PATH`
2. Analyser les commits et le diff
3. Remplir intelligemment chaque section :
   - **Bug fix** : supprimer si pas de fix, sinon lier l'issue
   - **Description** : résumer les changements basé sur les commits
   - **Type de changement** : cocher (✔️) les types appropriés
   - **Tests** : indiquer si tests ajoutés/modifiés
   - **Checklist** : cocher ce qui s'applique
   - **Actions** : cocher ce qui est nécessaire

### Sauvegarde

```bash
cat > /tmp/pr_body_generated.md << 'EOF'
[CONTENU GÉNÉRÉ]
EOF
```
