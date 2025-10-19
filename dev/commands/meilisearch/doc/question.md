---
allowed-tools: [Read, Grep, Glob, Bash]
description: Interroger la documentation Meilisearch locale pour répondre à une question
argument-hint: <question>
model: claude-sonnet-4-5-20250929
---

# Interrogation de la Documentation Meilisearch

Répondre à une question technique sur Meilisearch en utilisant la documentation locale présente dans `docs/meilisearch/`.

## Purpose
Fournir des réponses précises et contextualisées aux questions Meilisearch en s'appuyant sur la documentation officielle stockée localement, sans nécessiter d'accès web.

## Variables
- QUESTION: La question technique posée par l'utilisateur
- DOCS_PATH: `docs/meilisearch/` - Chemin vers la documentation locale
- SEARCH_KEYWORDS: Mots-clés extraits de la question pour la recherche

## Relevant Files
- `docs/meilisearch/` - Documentation Meilisearch locale
- `docs/meilisearch/README.md` - Index de la documentation chargée

## Timing

### Début d'Exécution
**OBLIGATOIRE - PREMIÈRE ACTION** :
1. Exécuter `date` pour obtenir l'heure réelle
2. Afficher immédiatement : 🕐 **Démarrage** : [Résultat de la commande date]
3. Stocker le timestamp pour le calcul de durée

### Fin d'Exécution
**OBLIGATOIRE - DERNIÈRE ACTION** :
1. Exécuter `date` à nouveau pour obtenir l'heure de fin
2. Calculer la durée réelle entre début et fin
3. Afficher :
   - ✅ **Terminé** : [Résultat de la commande date]
   - ⏱️ **Durée** : [Durée calculée au format lisible]

### Formats
- Date : résultat brut de la commande `date` (incluant CEST/CET automatiquement)
- Durée :
  - Moins d'1 minute : `XXs` (ex: 45s)
  - Moins d'1 heure : `XXm XXs` (ex: 2m 30s)
  - Plus d'1 heure : `XXh XXm XXs` (ex: 1h 15m 30s)

### Instructions CRITIQUES
- TOUJOURS exécuter `date` via Bash - JAMAIS inventer/halluciner l'heure
- Le timestamp de début DOIT être obtenu en exécutant `date` immédiatement
- Le timestamp de fin DOIT être obtenu en exécutant `date` à la fin
- Calculer la durée en soustrayant les timestamps unix (utiliser `date +%s`)
- NE JAMAIS supposer ou deviner l'heure

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Enregistrer le timestamp de début pour calcul ultérieur

### Étape 1: Vérification de la documentation locale
- Vérifier l'existence de `docs/meilisearch/`
- Si le répertoire n'existe pas ou est vide :
  - Informer l'utilisateur
  - Suggérer d'exécuter `/meilisearch:doc:load` pour charger la documentation
  - Arrêter l'exécution avec message explicite
- Si la documentation existe :
  - Lire `docs/meilisearch/README.md` pour connaître le contenu disponible
  - Continuer vers l'étape 2

### Étape 2: Analyse de la question
- Extraire les mots-clés principaux de QUESTION
- Identifier le contexte technique (composant, feature, concept)
- Exemples de mots-clés :
  - "index" → chercher dans indexes.md, indexing.md
  - "search" → chercher dans search.md, query.md
  - "filter" → chercher dans filters.md, facets.md
  - "ranking" → chercher dans ranking.md, relevance.md

### Étape 3: Recherche dans la documentation
- Utiliser Grep pour rechercher les mots-clés dans `docs/meilisearch/`
- Paramètres de recherche :
  - Case insensitive (`-i`)
  - Afficher le contexte (3 lignes avant/après avec `-C 3`)
  - Limiter les résultats pertinents
- Lire les fichiers markdown pertinents identifiés
- Si aucun résultat :
  - Élargir la recherche avec des termes associés
  - Suggérer des termes de recherche alternatifs

### Étape 4: Analyse et synthèse
- Extraire les sections pertinentes de la documentation
- Organiser les informations par ordre de pertinence
- Identifier :
  - Concept principal
  - Exemples de code
  - Bonnes pratiques
  - Warnings et notes importantes
  - Liens vers documentation connexe

### Étape 5: Construction de la réponse
- Réponse structurée en format bullet points
- Inclure :
  - Explication concise du concept
  - Exemples de code si disponibles
  - Références aux fichiers de documentation sources
  - Liens internes vers sections connexes
- Format markdown enrichi avec :
  - Blocs de code JSON/cURL selon contexte
  - Sections info/warning si pertinent
  - Liste hiérarchique pour les étapes

### Étape 6: Rapport final avec timing
- Présenter la réponse formatée
- Calculer et afficher la durée totale
- Afficher le timestamp de fin

## Report Format
```markdown
## 📚 Réponse : [Sujet principal]

### Concept
- Explication principale
- Points clés

### Exemple de Code
[Bloc de code si disponible]

### Documentation de Référence
- 📄 `docs/meilisearch/[fichier].md` - [Section]
- 📄 Autres fichiers pertinents

### Voir Aussi
- Concepts connexes
- Autres commandes utiles

---
✅ **Terminé** : [timestamp Europe/Paris]

⏱️ **Durée** : [durée formatée]
```

## Error Handling
- **Documentation manquante** : Message clair + suggestion `/meilisearch:doc:load`
- **Aucun résultat trouvé** : Suggérer termes alternatifs ou reformulation
- **Question trop vague** : Demander précisions avec exemples
- **Fichiers corrompus** : Signaler et suggérer rechargement

## Examples

### Exemple 1 - Question simple
```bash
/meilisearch:doc:question "Comment créer un index ?"
```
**Résultat attendu** :
- Recherche dans indexes.md, indexing.md
- Exemples d'API REST
- Configuration d'index
- Références aux fichiers sources

### Exemple 2 - Question sur composant
```bash
/meilisearch:doc:question "Comment configurer les filtres ?"
```
**Résultat attendu** :
- Recherche filters.md, facets.md
- Attributs filtrables
- Exemples de requêtes filtrées
- Bonnes pratiques

### Exemple 3 - Question avancée
```bash
/meilisearch:doc:question "Comment optimiser le ranking ?"
```
**Résultat attendu** :
- Recherche ranking.md, relevance.md
- Règles de ranking
- Cas d'usage appropriés
- Exemples de configuration

## Best Practices
- Toujours vérifier la présence de la documentation avant recherche
- Privilégier la précision sur l'exhaustivité
- Citer les sources (fichiers markdown consultés)
- Fournir des exemples de code concrets
- Suggérer des commandes connexes si pertinent
- Garder les réponses concises mais complètes
- **Afficher le timing au début et à la fin**
- **Calculer précisément la durée d'exécution**

## Notes
- Cette commande fonctionne 100% offline une fois la documentation chargée
- La documentation doit être rafraîchie périodiquement avec `/meilisearch:doc:load`
- Supporte toutes les versions de Meilisearch présentes dans `docs/meilisearch/`
- Peut être étendue pour supporter d'autres frameworks avec le même pattern
