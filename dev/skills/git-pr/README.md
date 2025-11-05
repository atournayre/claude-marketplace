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

## Architecture

```
git-pr/
├── SKILL.md              # Définition du skill et workflow
├── README.md             # Cette documentation
└── scripts/
    ├── gh_auth_setup.sh  # Configuration automatique auth (⭐ NOUVEAU)
    ├── verify_pr_template.sh
    ├── smart_qa.sh
    ├── analyze_changes.sh
    ├── confirm_base_branch.py
    ├── safe_push_pr.sh
    ├── assign_milestone.py
    ├── assign_project.py  # Nécessite scopes project
    └── cleanup_branch.sh
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
