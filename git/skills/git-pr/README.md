# Git PR Skill - Documentation

## Configuration Initiale

### Authentification GitHub

Ce skill nécessite une authentification GitHub avec des scopes spécifiques.

#### Scopes Requis

| Scope | Description | Usage |
|-------|-------------|-------|
| `repo` | Accès complet aux repos | Création PR, lecture commits, gestion branches |
| `read:org` | Lecture infos organisation | Récupération infos repository organisation |
| `read:project` | Lecture projets GitHub | Liste et lecture des projets |
| `project` | Écriture aux projets | Assignation PR aux projets |
| `gist` | Gestion gists | Partage extraits de code si nécessaire |

#### Configuration Automatique (Recommandé)

```bash
bash scripts/gh_auth_setup.sh
```

Ce script configure automatiquement TOUS les scopes requis.

#### Configuration Manuelle

```bash
gh auth refresh --hostname github.com \
  -s repo \
  -s read:org \
  -s read:project \
  -s project \
  -s gist
```

#### Vérification

```bash
gh auth status
```

Sortie attendue:
```
Token scopes: 'gist', 'project', 'read:org', 'repo'
```

⚠️ **Note**: `read:project` n'apparaît pas toujours explicitement mais est inclus avec `project`.

## Protection Contre les Oublis

Le skill vérifie automatiquement les scopes au démarrage (Étape 1.5).

Si un scope manque :
- ❌ Arrêt immédiat avec message d'erreur
- 📋 Liste des scopes manquants affichée
- 🔄 Commande de renouvellement suggérée

## Utilisation

### Via Slash Command

```bash
/git:pr <branche-base> [milestone] [projet] [--delete] [--no-review]
```

### Via Skill Direct

```bash
ARGUMENTS="develop 1.0.0 TMA --delete" skill dev:git-pr
```

## Dépannage

### Erreur: "Scopes manquants"

```bash
❌ Scopes GitHub manquants: read:project project
```

**Solution**: Relancer `gh_auth_setup.sh`

### Erreur: "Impossible de récupérer les projets"

Vérifier authentification:
```bash
gh auth status
```

Si scopes corrects mais erreur persiste:
```bash
# Forcer renouvellement
gh auth logout
bash scripts/gh_auth_setup.sh
```

### Erreur: "your authentication token is missing required scopes"

**Cause**: Token obsolète ou scopes révoqués

**Solution**:
```bash
bash scripts/gh_auth_setup.sh
```

## Cache Persistant

Le skill utilise un système de cache pour optimiser les performances.

### Cache Milestones

**Fichier**: `.claude/cache/git-milestones.json`

**Fonctionnalités**:
- Stockage des milestones GitHub
- Recherche par titre exact ou alias
- Normalisation semver automatique (`26` → `26.0.0`)
- Génération d'aliases depuis titres (`26.0.0 (Hotfix)` → alias `26.0.0`)

**Refresh**: Automatique si milestone introuvable

### Cache Projets

**Fichier**: `.claude/cache/git-projects.json`

**Fonctionnalités**:
- Stockage des projets GitHub
- Recherche case-insensitive par titre ou alias
- Génération d'aliases depuis mots-clés (`Bug Tracking` → `["bug", "tracking"]`)

**Refresh**: Automatique si projet introuvable

### Commandes Utiles

```bash
# Vider cache milestones
rm .claude/cache/git-milestones.json

# Vider cache projets
rm .claude/cache/git-projects.json

# Vider tout le cache
rm -rf .claude/cache/
```

## Architecture

```
git-pr/
├── SKILL.md              # Définition du skill et workflow
├── README.md             # Cette documentation
├── scripts/
│   ├── gh_auth_setup.sh          # Configuration automatique auth
│   ├── verify_pr_template.sh
│   ├── smart_qa.sh
│   ├── analyze_changes.sh
│   ├── confirm_base_branch.py
│   ├── safe_push_pr.sh
│   ├── assign_milestone.py       # Assignation milestone avec cache
│   ├── milestone_cache.py        # Module cache milestones
│   ├── assign_project.py         # Assignation projet avec cache
│   ├── project_cache.py          # Module cache projets
│   └── cleanup_branch.sh
└── tests/
    ├── run_tests.sh              # Lance tous les tests
    ├── test_milestone_cache.py   # Tests unitaires milestones
    └── test_project_cache.py     # Tests unitaires projets
```

## Maintenance

### Ajout d'un Nouveau Scope

1. Modifier `gh_auth_setup.sh`:
   ```bash
   REQUIRED_SCOPES=(
       # ... scopes existants
       "nouveau_scope"  # Description
   )
   ```

2. Modifier `SKILL.md` section "Scopes Requis"

3. Mettre à jour ce README

### Tests Unitaires

```bash
# Lancer tous les tests
bash tests/run_tests.sh

# Lancer un test spécifique
cd tests
python3 test_milestone_cache.py -v
python3 test_project_cache.py -v
```

### Test de Consistance

Après modification:
```bash
# Tester le script
bash scripts/gh_auth_setup.sh

# Vérifier
gh auth status

# Tester assignation projet
python3 scripts/assign_project.py <pr-number> --project <nom>
```
