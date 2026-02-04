---
name: symfony:doc:question
description: Interroger la documentation Symfony locale pour répondre à une question
allowed-tools: [Read, Grep, Glob, Bash]
argument-hint: <question>
model: sonnet
version: 1.0.0
license: MIT
---

# Interrogation de la Documentation Symfony

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Répondre à une question technique sur Symfony en utilisant la documentation locale présente dans `docs/symfony/`.

## Purpose
Fournir des réponses précises et contextualisées aux questions Symfony en s'appuyant sur la documentation officielle stockée localement, sans nécessiter d'accès web.

## Variables
- QUESTION: La question technique posée par l'utilisateur
- DOCS_PATH: `docs/symfony/` - Chemin vers la documentation locale
- SEARCH_KEYWORDS: Mots-clés extraits de la question pour la recherche

## Relevant Files
- `docs/symfony/` - Documentation Symfony locale
- `docs/symfony/README.md` - Index de la documentation chargée

## Workflow

### Étape 1: Vérification de la documentation locale
- Vérifier l'existence de `docs/symfony/`
- Si le répertoire n'existe pas ou est vide :
  - Informer l'utilisateur
  - Suggérer d'exécuter `/load:doc:symfony` pour charger la documentation
  - Arrêter l'exécution avec message explicite
- Si la documentation existe :
  - Lire `docs/symfony/README.md` pour connaître le contenu disponible
  - Continuer vers l'étape 2

### Étape 2: Analyse de la question
- Extraire les mots-clés principaux de QUESTION
- Identifier le contexte technique (composant, feature, concept)
- Exemples de mots-clés :
  - "routing" → chercher dans routing.md, controller.md
  - "doctrine" → chercher dans doctrine.md, database.md
  - "form" → chercher dans forms.md, validation.md
  - "security" → chercher dans security.md, authentication.md

### Étape 3: Recherche dans la documentation
- Utiliser Grep pour rechercher les mots-clés dans `docs/symfony/`
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
  - Blocs de code PHP/YAML/Twig selon contexte
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
- 📄 `docs/symfony/[fichier].md` - [Section]
- 📄 Autres fichiers pertinents

### Voir Aussi
- Concepts connexes
- Autres commandes utiles
```

## Error Handling
- **Documentation manquante** : Message clair + suggestion `/load:doc:symfony`
- **Aucun résultat trouvé** : Suggérer termes alternatifs ou reformulation
- **Question trop vague** : Demander précisions avec exemples
- **Fichiers corrompus** : Signaler et suggérer rechargement

## Examples

### Exemple 1 - Question simple
```bash
/symfony:doc:question "Comment créer une route ?"
```
**Résultat attendu** :
- Recherche dans routing.md, controller.md
- Exemples d'annotations/attributs PHP 8
- Exemples YAML
- Références aux fichiers sources

### Exemple 2 - Question sur composant
```bash
/symfony:doc:question "Comment utiliser les formulaires avec validation ?"
```
**Résultat attendu** :
- Recherche forms.md, validation.md
- Exemples de FormType
- Contraintes de validation
- Intégration Doctrine

### Exemple 3 - Question avancée
```bash
/symfony:doc:question "Quelle est la différence entre les voters et les guards ?"
```
**Résultat attendu** :
- Recherche security.md, voters.md, guard.md
- Comparaison conceptuelle
- Cas d'usage appropriés
- Exemples des deux approches

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
- La documentation doit être rafraîchie périodiquement avec `/load:doc:symfony`
- Supporte toutes les versions de Symfony présentes dans `docs/symfony/`
- Peut être étendue pour supporter d'autres frameworks avec le même pattern
