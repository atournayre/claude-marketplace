---
name: release-notes
description: >
  Génère des notes de release HTML orientées utilisateurs finaux.
  Transforme les commits techniques en descriptions accessibles sans jargon.
allowed-tools: [Bash, Read, Write, Grep, Glob, AskUserQuestion]
model: sonnet
---

# Release Notes Skill

Génère un document HTML orienté utilisateurs finaux, sans jargon technique.

## Variables

```bash
REPORT_PATH=".claude/reports"
TARGET="$ARGUMENTS"  # Format: "branche-source branche-cible [nom-release]"
```

## Workflow

### Étape 0: Extraction et validation des arguments

```bash
# Parser les arguments
BRANCH_SOURCE=$(echo "$TARGET" | awk '{print $1}')
BRANCH_TARGET=$(echo "$TARGET" | awk '{print $2}')
RELEASE_NAME=$(echo "$TARGET" | awk '{print $3}')
```

**AVANT TOUTE EXÉCUTION**, vérifier que les arguments obligatoires sont fournis :

1. Si `$BRANCH_SOURCE` est manquant ou vide :
   - Lister les branches disponibles : `git branch -r --list 'origin/release/*' --list 'origin/feature/*' | head -10`
   - Utiliser `AskUserQuestion` pour demander la branche source
   - Question : "Quelle est la branche source à analyser ?"
   - Proposer les branches récentes de type `release/*` ou `feature/*`

2. Si `$BRANCH_TARGET` est manquant ou vide :
   - Utiliser `AskUserQuestion` pour demander la branche cible
   - Question : "Quelle est la branche de référence ?"
   - Options suggérées : `main`, `develop`, `master`

**Ne pas continuer** tant que les deux arguments obligatoires ne sont pas fournis.

Si `$RELEASE_NAME` n'est pas fourni, utiliser le nom de `$BRANCH_SOURCE` en retirant le préfixe "release/" ou "feature/".

### Étape 1: Validation des branches

```bash
# Vérifier que les branches existent
git rev-parse --verify $BRANCH_SOURCE
git rev-parse --verify $BRANCH_TARGET

# Vérifier qu'il y a des différences
DIFF_COUNT=$(git rev-list --count $BRANCH_TARGET..$BRANCH_SOURCE)
if [ $DIFF_COUNT -eq 0 ]; then
    echo "Aucune différence entre les branches"
    exit 0
fi

echo "Commits à analyser: $DIFF_COUNT"
```

### Étape 2: Collecte des commits

```bash
# Récupérer tous les commits avec leur message complet
git log $BRANCH_TARGET..$BRANCH_SOURCE --oneline --no-merges

# Pour plus de contexte si nécessaire
git log $BRANCH_TARGET..$BRANCH_SOURCE --pretty=format:"%h|%s|%b" --no-merges
```

### Étape 3: Analyse et catégorisation

Analyser chaque commit et le catégoriser selon son **impact utilisateur** :

#### Catégories

1. **Nouveautés** (icône étoile)
   - Nouvelles fonctionnalités visibles par l'utilisateur
   - Nouveaux écrans, boutons, options
   - Mots-clés : feat, feature, ✨, 🚀, nouveau, ajout

2. **Améliorations** (icône flèche vers le haut)
   - Améliorations de fonctionnalités existantes
   - Meilleure ergonomie, rapidité
   - Mots-clés : improve, enhance, ♻️, ⚡, amélioration, optimisation, perf

3. **Corrections** (icône coche)
   - Bugs corrigés impactant l'utilisateur
   - Problèmes résolus
   - Mots-clés : fix, 🐛, correction, résolution, bug

4. **Sécurité** (icône bouclier) - si applicable
   - Améliorations de sécurité
   - Mots-clés : security, 🔒, sécurité

#### Commits à IGNORER (ne pas inclure dans les notes)

- `refactor:` - Refactorisation interne
- `test:` / `✅` - Tests
- `chore:` / `🔧` - Maintenance technique
- `ci:` / `👷` - CI/CD
- `docs:` / `📝` - Documentation technique (sauf si user-facing)
- `style:` / `💄` - Formatage code
- Commits de merge
- Mises à jour de dépendances

### Étape 4: Rédaction des notes

Pour chaque commit retenu, rédiger une description **orientée utilisateur** :

**Règles de rédaction STRICTES :**

1. **ZÉRO jargon technique**
   - ❌ "Refactoring du composant UserController"
   - ✅ "Amélioration de la gestion de votre compte"
   - ❌ "Ajout d'un endpoint API REST"
   - ✅ "Nouvelle fonctionnalité disponible"

2. **Bénéfice utilisateur en premier**
   - ❌ "Ajout d'un cache sur les requêtes API"
   - ✅ "L'application est maintenant plus rapide"
   - ❌ "Optimisation des requêtes SQL"
   - ✅ "Les pages se chargent plus rapidement"

3. **Verbes d'action simples**
   - Vous pouvez maintenant...
   - Il est désormais possible de...
   - Nous avons corrigé...
   - Nous avons amélioré...

4. **Phrases courtes et claires**
   - Max 1-2 phrases par élément
   - Pas d'acronymes sans explication (pas de API, SQL, REST, etc.)

5. **Ton positif et professionnel**
   - Éviter les formulations négatives
   - Focus sur ce qui est possible/amélioré

### Étape 5: Génération du HTML

Utiliser le template suivant avec CSS inline :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notes de version - [RELEASE_NAME]</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background: #f8f9fa;
        }
        header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            color: white;
        }
        header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .version { font-size: 1.2rem; opacity: 0.9; }
        .date { font-size: 0.9rem; opacity: 0.7; }
        main { display: flex; flex-direction: column; gap: 2rem; }
        .category {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .category h2 {
            font-size: 1.3rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #eee;
        }
        .category.new h2 { border-color: #ffd700; }
        .category.improved h2 { border-color: #4caf50; }
        .category.fixed h2 { border-color: #2196f3; }
        .category.security h2 { border-color: #ff5722; }
        .category ul { list-style: none; }
        .category li {
            padding: 0.75rem 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .category li:last-child { border-bottom: none; }
        footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            color: #666;
            font-size: 0.9rem;
        }
        @media (max-width: 600px) {
            body { padding: 1rem; }
            header h1 { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <header>
        <h1>Quoi de neuf ?</h1>
        <p class="version">Version [RELEASE_NAME]</p>
        <p class="date">[DATE du jour]</p>
    </header>

    <main>
        <!-- Section Nouveautés (si non vide) -->
        <section class="category new">
            <h2>⭐ Nouveautés</h2>
            <ul>
                <li>Description orientée utilisateur...</li>
            </ul>
        </section>

        <!-- Section Améliorations (si non vide) -->
        <section class="category improved">
            <h2>📈 Améliorations</h2>
            <ul>
                <li>Description orientée utilisateur...</li>
            </ul>
        </section>

        <!-- Section Corrections (si non vide) -->
        <section class="category fixed">
            <h2>✅ Corrections</h2>
            <ul>
                <li>Description orientée utilisateur...</li>
            </ul>
        </section>

        <!-- Section Sécurité (si applicable et non vide) -->
        <section class="category security">
            <h2>🔒 Sécurité</h2>
            <ul>
                <li>Description orientée utilisateur...</li>
            </ul>
        </section>
    </main>

    <footer>
        <p>Merci d'utiliser notre application !</p>
    </footer>
</body>
</html>
```

**Notes :**
- Ne pas inclure les sections vides
- Remplacer [RELEASE_NAME] par le nom de la release
- Remplacer [DATE] par la date du jour au format "26 novembre 2025"

### Étape 6: Sauvegarde du fichier

```bash
OUTPUT_FILE="$REPORT_PATH/release_notes_${RELEASE_NAME}.html"
mkdir -p "$REPORT_PATH"
```

Utiliser le tool `Write` pour écrire le contenu HTML dans `$OUTPUT_FILE`.

Afficher le résumé :
```
Notes de release générées : $OUTPUT_FILE

Résumé :
- X nouveautés
- Y améliorations
- Z corrections
```

## Exemples de transformation

| Commit technique | Note utilisateur |
|------------------|------------------|
| `✨ feat: implémenter cache Redis sur endpoint /api/users` | L'affichage de la liste des utilisateurs est maintenant plus rapide |
| `🐛 fix: corriger validation email dans le formulaire d'inscription` | Nous avons corrigé un problème qui empêchait certaines adresses email d'être acceptées lors de l'inscription |
| `⚡ perf: optimiser requêtes N+1 sur la page dashboard` | Le tableau de bord se charge maintenant plus rapidement |
| `✨ feat: ajouter export CSV des factures` | Vous pouvez maintenant exporter vos factures au format Excel |
| `🐛 fix: résoudre crash sur iOS 16 lors de l'upload` | Nous avons corrigé un problème qui pouvait faire fermer l'application lors de l'envoi de fichiers |

## Règles importantes

1. **ZÉRO jargon technique** - L'utilisateur final ne doit pas voir de termes comme "API", "refactoring", "backend", "cache", "endpoint", "requête"
2. **Bénéfice utilisateur** - Chaque item doit répondre à "Qu'est-ce que ça change pour moi ?"
3. **Ignorer l'invisible** - Ne pas mentionner les changements internes (tests, CI, deps, refactoring)
4. **Ton positif** - Utiliser un ton accueillant et positif
5. **Accessibilité** - HTML sémantique, contrastes suffisants, responsive
6. **Concision** - Max 1-2 phrases par item, pas de détails superflus
