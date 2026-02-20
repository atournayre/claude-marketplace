---
name: git:release-report
description: Génère un rapport HTML d'analyse d'impact entre deux branches
argument-hint: <branche-source> <branche-cible> [nom-release]
version: 1.0.0
license: MIT
arguments:
  - name: branche-source
    description: Branche source à analyser (ex release/v27.0.0)
    required: true
  - name: branche-cible
    description: Branche de référence (ex main ou develop)
    required: true
  - name: nom-release
    description: Nom de la release pour le fichier (optionnel)
    required: false
---

> ⚠️ **Déprécié** : Cette skill est remplacée par `devops:release-report`. Voir le plugin `devops`. Sera supprimée en v3.0.

# Configuration de sortie

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


**IMPORTANT** : Cette skill génère un rapport HTML et nécessite un format de sortie spécifique.

Lis le frontmatter de cette skill. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

# Générer rapport d'analyse de release

Génère un rapport HTML détaillé comparant deux branches pour analyser l'impact d'une release.

## Usage

```bash
/git:release-report <branche-source> <branche-cible> [nom-release]
```

**Exemples :**
- `/git:release-report release/v27.0.0 main`
- `/git:release-report release/v27.0.0 develop v27.0.0`
- `/git:release-report feature/new-module main "Module XYZ"`

## Description

Cette commande génère un rapport HTML orienté Product Owner qui analyse :

1. **Statistiques globales** : fichiers modifiés, lignes ajoutées/supprimées, commits
2. **Répartition par type de fichier** : PHP, Twig, JS, etc.
3. **Fonctionnalités principales** : extraction depuis les commits
4. **Impact métier** : par domaine fonctionnel
5. **Qualité & maintenabilité** : évolution du code

Le rapport est généré dans `REPORT_PATH/impact_<nom-release>.html`

## Variables

REPORT_PATH: `.claude/reports`

Variables à extraire des arguments :

- `$BRANCH_SOURCE` : Branche source à analyser (ex: release/v27.0.0)
- `$BRANCH_TARGET` : Branche de référence (ex: main ou develop)
- `$RELEASE_NAME` : Nom de la release pour le fichier (ex: v27.0.0)

Si `$RELEASE_NAME` n'est pas fourni, utiliser le nom de `$BRANCH_SOURCE` en retirant le préfixe "release/"

## Workflow

### 0. Vérification des arguments obligatoires

**AVANT TOUTE EXÉCUTION**, vérifier que les arguments obligatoires sont fournis :

1. Si `$BRANCH_SOURCE` est manquant :
   - Utiliser `AskUserQuestion` pour demander la branche source
   - Question : "Quelle est la branche source à analyser ?"
   - Proposer les branches récentes de type `release/*` ou `feature/*`

2. Si `$BRANCH_TARGET` est manquant :
   - Utiliser `AskUserQuestion` pour demander la branche cible
   - Question : "Quelle est la branche de référence ?"
   - Options suggérées : `main`, `develop`, `master`

**Ne pas continuer** tant que les deux arguments obligatoires ne sont pas fournis.

### 1. Validation des paramètres

```bash
# Vérifier que les branches existent
git rev-parse --verify $BRANCH_SOURCE
git rev-parse --verify $BRANCH_TARGET

# Vérifier qu'il y a des différences
DIFF_COUNT=$(git rev-list --count $BRANCH_TARGET..$BRANCH_SOURCE)
if [ $DIFF_COUNT -eq 0 ]; then
    echo "Aucune différence entre les branches"
    exit 1
fi
```

### 2. Collecte des statistiques git

Exécuter les commandes suivantes en parallèle :

```bash
# Statistiques globales
git diff --stat $BRANCH_TARGET..$BRANCH_SOURCE | tail -1

# Nombre total de fichiers modifiés et détails lignes
git diff --numstat $BRANCH_TARGET..$BRANCH_SOURCE | \
  awk '{files++; added+=$1; deleted+=$2} END {print files, added, deleted}'

# Répartition par type de fichier
git diff --numstat $BRANCH_TARGET..$BRANCH_SOURCE | python3 -c "
import sys
from collections import defaultdict

stats = defaultdict(lambda: {'count': 0, 'added': 0, 'deleted': 0})

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) < 3:
        continue

    added = int(parts[0]) if parts[0] != '-' else 0
    deleted = int(parts[1]) if parts[1] != '-' else 0
    path = parts[2]

    ext = 'autre'
    if path.endswith('.php'):
        ext = 'php'
    elif path.endswith('.twig'):
        ext = 'twig'
    elif path.endswith(('.yml', '.yaml')):
        ext = 'yaml'
    elif path.endswith('.js'):
        ext = 'js'
    elif path.endswith('.scss'):
        ext = 'scss'
    elif path.endswith('.md'):
        ext = 'md'
    elif path.endswith('.json'):
        ext = 'json'
    elif path.endswith('.sh'):
        ext = 'sh'

    stats[ext]['count'] += 1
    stats[ext]['added'] += added
    stats[ext]['deleted'] += deleted
    stats[ext]['total'] = stats[ext]['added'] + stats[ext]['deleted']

for ext in sorted(stats.items(), key=lambda x: x[1]['total'], reverse=True):
    name = ext[0]
    data = ext[1]
    print(f'{name}|{data[\"count\"]}|{data[\"added\"]}|{data[\"deleted\"]}|{data[\"total\"]}')
"

# Types de modifications (A/M/D/R)
git diff --name-status $BRANCH_TARGET..$BRANCH_SOURCE | cut -f1 | sort | uniq -c

# Nombre de commits
git rev-list --count $BRANCH_TARGET..$BRANCH_SOURCE

# Total fichiers dans la branche cible
git ls-tree -r $BRANCH_TARGET --name-only | wc -l

# Top commits avec features/fixes
git log $BRANCH_TARGET..$BRANCH_SOURCE --oneline --no-merges | \
  grep -E "(feat|feature|✨|🚀|📝|🐛|fix|♻️|refactor)" | head -50
```

### 3. Analyse des domaines fonctionnels

Analyser les commits pour identifier les domaines principaux impactés :

- Grouper par préfixe de commit (AVENANT, DOSSIER, APF, etc.)
- Identifier les patterns récurrents
- Extraire les fonctionnalités majeures avec leur impact

### 4. Génération du rapport HTML

Utiliser le template suivant et remplir avec les données collectées :

**Structure du rapport :**

1. **Header** avec executive summary
   - Nom de la release
   - Résumé en 2-3 phrases
   - Chiffres clés (% code modifié, commits, variation nette)

2. **KPI Grid** (4 indicateurs visuels)
   - % du code modifié
   - Nombre de commits
   - Variation nette (simplification/ajout)
   - Domaine principal (ex: "70% focus AVENANTS")

3. **Fonctionnalités principales** (cards avec impact)
   - Impact Très élevé (rouge)
   - Impact Élevé (orange)
   - Impact Moyen (jaune)
   - Impact Faible (vert)

4. **Corrections majeures**
   - Liste des bugs corrigés

5. **Qualité & Maintenabilité**
   - Code simplifié
   - Documentation
   - Refactoring
   - Interface

6. **Vue d'ensemble technique**
   - Chart bars par type de fichier
   - Métrique périmètre impacté

7. **Impact business** (4 axes)
   - Gestion administrative
   - Communication
   - Performance
   - Sécurité

**Style CSS :**
- Gradient violet (#667eea → #764ba2)
- Cards avec border-left coloré selon impact
- Progress bars animées
- KPI boxes avec fond dégradé
- Design responsive

### 5. Sauvegarde du fichier

```bash
OUTPUT_FILE="REPORT_PATH/impact_${RELEASE_NAME}.html"
mkdir -p REPORT_PATH
# Écrire le contenu HTML généré
echo "Rapport généré : $OUTPUT_FILE"
```

## Format de sortie

Le rapport doit être :

- **Orienté Product Owner** : focus sur l'impact métier, pas les détails techniques
- **Visuel** : KPI, charts, couleurs par niveau d'impact
- **Actionnable** : lister les features, bugs corrigés, améliorations
- **Comparable** : même structure pour toutes les releases

## Règles importantes

1. **NE PAS** utiliser de termes techniques obscurs
2. **TOUJOURS** expliquer l'impact utilisateur
3. **GROUPER** les changements par domaine fonctionnel
4. **QUANTIFIER** l'impact (%, nombre, ratio)
5. **PRIORISER** par impact métier (Très élevé → Faible)

## Exemple d'exécution

```bash
$ /git:release-report release/v27.0.0 main

Analyse de release/v27.0.0 vs main...

✓ Collecte statistiques git
✓ Analyse types de fichiers
✓ Extraction fonctionnalités
✓ Génération rapport HTML

Rapport généré : REPORT_PATH/impact_v27.0.0.html

Résumé :
- 1 250 fichiers modifiés (17.5% du codebase)
- 45 320 lignes ajoutées, 38 100 lignes supprimées
- +7 220 lignes nettes (+10.2%)
- 780 commits
- Focus principal : NOTIFICATIONS (65%)
```

## Notes

- Le rapport est auto-suffisant (HTML avec CSS inline)
- Compatible tous navigateurs modernes
- Peut être imprimé ou converti en PDF
- Les couleurs suivent le design system du projet
