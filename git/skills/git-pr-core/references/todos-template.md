# Template Task Management pour git-pr

## Tâches initiales (avec TaskCreate)

Les tâches doivent être créées à l'initialisation du workflow avec `TaskCreate` :

```
TaskCreate #1: Charger config .env.claude
TaskCreate #2: Confirmation initiale (si --no-interaction absent)
TaskCreate #3: Vérifier scopes GitHub
TaskCreate #4: Vérifier template PR
TaskCreate #5: Lancer QA intelligente
TaskCreate #6: Analyser changements git
TaskCreate #7: Confirmer branche de base
TaskCreate #8: Générer description PR
TaskCreate #9: Push et créer PR
TaskCreate #10: Assigner milestone
TaskCreate #11: Assigner projet GitHub
TaskCreate #12: Code review automatique (si plugin installé)
TaskCreate #13: Nettoyage branche locale
```

**Important :**
- Utiliser `activeForm` avec forme progressive (ex: "Chargeant config", "Vérifiant scopes GitHub")
- Pattern d'exécution : `TaskUpdate` → `in_progress` → exécution → `TaskUpdate` → `completed`

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
