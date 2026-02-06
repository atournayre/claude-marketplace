# Règles de rédaction des notes de release

## Principe fondamental

**ZÉRO jargon technique** - L'utilisateur final ne doit pas voir de termes comme "API", "refactoring", "backend", "cache", "endpoint", "requête".

## Règles de rédaction

### 1. ZÉRO jargon technique
- ❌ "Refactoring du composant UserController"
- ✅ "Amélioration de la gestion de votre compte"
- ❌ "Ajout d'un endpoint API REST"
- ✅ "Nouvelle fonctionnalité disponible"

### 2. Bénéfice utilisateur en premier
- ❌ "Ajout d'un cache sur les requêtes API"
- ✅ "L'application est maintenant plus rapide"
- ❌ "Optimisation des requêtes SQL"
- ✅ "Les pages se chargent plus rapidement"

### 3. Verbes d'action simples
- Vous pouvez maintenant...
- Il est désormais possible de...
- Nous avons corrigé...
- Nous avons amélioré...

### 4. Phrases courtes et claires
- Max 1-2 phrases par élément
- Pas d'acronymes sans explication (pas de API, SQL, REST, etc.)

### 5. Ton positif et professionnel
- Éviter les formulations négatives
- Focus sur ce qui est possible/amélioré

## Exemples de transformation

| Commit technique | Note utilisateur |
|------------------|------------------|
| `✨ feat: implémenter cache Redis sur endpoint /api/users` | L'affichage de la liste des utilisateurs est maintenant plus rapide |
| `🐛 fix: corriger validation email dans le formulaire d'inscription` | Nous avons corrigé un problème qui empêchait certaines adresses email d'être acceptées lors de l'inscription |
| `⚡ perf: optimiser requêtes N+1 sur la page dashboard` | Le tableau de bord se charge maintenant plus rapidement |
| `✨ feat: ajouter export CSV des factures` | Vous pouvez maintenant exporter vos factures au format Excel |
| `🐛 fix: résoudre crash sur iOS 16 lors de l'upload` | Nous avons corrigé un problème qui pouvait faire fermer l'application lors de l'envoi de fichiers |

## Catégorisation des commits

### Nouveautés (⭐)
- Mots-clés : feat, feature, ✨, 🚀, nouveau, ajout

### Améliorations (📈)
- Mots-clés : improve, enhance, ♻️, ⚡, amélioration, optimisation, perf

### Corrections (✅)
- Mots-clés : fix, 🐛, correction, résolution, bug

### Sécurité (🔒)
- Mots-clés : security, 🔒, sécurité

## Commits à IGNORER

- `refactor:` - Refactorisation interne
- `test:` / `✅` - Tests
- `chore:` / `🔧` - Maintenance technique
- `ci:` / `👷` - CI/CD
- `docs:` / `📝` - Documentation technique (sauf si user-facing)
- `style:` / `💄` - Formatage code
- Commits de merge
- Mises à jour de dépendances
