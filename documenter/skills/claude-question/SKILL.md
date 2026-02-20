---
name: documenter:claude-question
description: Interroger la documentation Claude Code locale pour répondre à une question
allowed-tools: [Read, Grep, Glob, Bash]
argument-hint: <question>
model: sonnet
version: 1.0.0
license: MIT
---

# Interrogation de la Documentation Claude Code

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Répondre à une question technique sur Claude Code en utilisant la documentation locale présente dans `docs/claude/`.

## Purpose
Fournir des réponses précises et contextualisées aux questions Claude Code en s'appuyant sur la documentation officielle stockée localement, sans nécessiter d'accès web.

## Variables
- QUESTION: La question technique posée par l'utilisateur
- DOCS_PATH: `docs/claude/` - Chemin vers la documentation locale
- SEARCH_KEYWORDS: Mots-clés extraits de la question pour la recherche

## Relevant Files
- `docs/claude/` - Documentation Claude Code locale
- `docs/claude/README.md` - Index de la documentation chargée

## Workflow

### Étape 1: Vérification de la documentation locale
- Vérifier l'existence de `docs/claude/`
- Si le répertoire n'existe pas ou est vide :
  - Informer l'utilisateur
  - Suggérer d'exécuter `/documenter:claude-load` pour charger la documentation
  - Arrêter l'exécution avec message explicite
- Si la documentation existe :
  - Lire `docs/claude/README.md` pour connaître le contenu disponible
  - Continuer vers l'étape 2

### Étape 2: Analyse de la question
- Extraire les mots-clés principaux de QUESTION
- Identifier le contexte technique (composant, feature, concept)
- Exemples de mots-clés :
  - "slash command" → chercher dans commands.md, custom-commands.md
  - "agent" → chercher dans agents.md, subagents.md
  - "hook" → chercher dans hooks.md, lifecycle.md
  - "tool" → chercher dans tools.md, permissions.md

### Étape 3: Recherche dans la documentation
- Utiliser Grep pour rechercher les mots-clés dans `docs/claude/`
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
  - Blocs de code Markdown/Python/Shell selon contexte
  - Sections info/warning si pertinent
  - Liste hiérarchique pour les étapes

### Étape 6: Rapport final avec timing
- Présenter la réponse formatée
- Calculer et afficher la durée totale
- Afficher le timestamp de fin

## Report Format
```markdown
## Réponse : [Sujet principal]

### Concept
- Explication principale
- Points clés

### Exemple de Code
[Bloc de code si disponible]

### Documentation de Référence
- `docs/claude/[fichier].md` - [Section]
- Autres fichiers pertinents

### Voir Aussi
- Concepts connexes
- Autres commandes utiles
```

## Error Handling
- **Documentation manquante** : Message clair + suggestion `/documenter:claude-load`
- **Aucun résultat trouvé** : Suggérer termes alternatifs ou reformulation
- **Question trop vague** : Demander précisions avec exemples
- **Fichiers corrompus** : Signaler et suggérer rechargement

## Examples

### Exemple 1 - Question simple
```bash
/documenter:claude-question "Comment créer une slash command ?"
```
**Résultat attendu** :
- Recherche dans commands.md, custom-commands.md
- Format de fichier de commande
- Exemples de frontmatter YAML
- Références aux fichiers sources

### Exemple 2 - Question sur composant
```bash
/documenter:claude-question "Comment utiliser les hooks ?"
```
**Résultat attendu** :
- Recherche hooks.md, lifecycle.md
- Types de hooks disponibles
- Exemples Python
- Cas d'usage

## Best Practices
- Toujours vérifier la présence de la documentation avant recherche
- Privilégier la précision sur l'exhaustivité
- Citer les sources (fichiers markdown consultés)
- Fournir des exemples de code concrets
- Suggérer des commandes connexes si pertinent
- Garder les réponses concises mais complètes
- **Afficher le timing au début et à la fin**

## Notes
- Cette commande fonctionne 100% offline une fois la documentation chargée
- La documentation doit être rafraîchie périodiquement avec `/documenter:claude-load`
- Supporte toutes les versions de Claude Code présentes dans `docs/claude/`
