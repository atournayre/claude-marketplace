---
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Edit, Write, MultiEdit, Bash
argument-hint:
description: Charge les règles de conception Elegant Objects pour l'écriture de code orienté objet élégant
---

# Règles de Conception Elegant Objects

## Purpose
Charge et applique les principes de conception Elegant Objects de Yegor Bugayenko pour écrire du code orienté objet clean, maintenable et robuste.

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
- Respecte les règles Elegant Objects ci-dessous
- Écris des tests unitaires avant l'implémentation
- Vérifie que chaque classe encapsule 1 à 4 attributs maximum
- Assure-toi que toutes les classes sont déclarées `final`

## Expertise

### Principes architecturaux Elegant Objects

#### Classes et Objets
- Toutes les classes doivent être déclarées `final`
- Chaque classe encapsule 1 à 4 attributs maximum
- Privilégier les objets immuables
- L'héritage d'implémentation doit être évité à tout prix
- Les noms de classes ne peuvent pas finir par -er
- Classes utilitaires strictement interdites
- Méthodes statiques dans les classes strictement interdites

#### Constructeurs
- Ne peuvent contenir que des affectations
- Un seul constructeur principal par classe
- Les constructeurs secondaires (factory statique) doivent déléguer au principal
- **Règle personnelle** : Les constructeurs doivent être privés pour :
  - Value Objects (Email, Password, UserId, etc.)
  - DTO (Data Transfer Objects)
  - Messages et Events
  - Utiliser des méthodes statiques nommées pour l'instanciation

#### Méthodes
- Doivent être déclarées dans des interfaces puis implémentées
- Éviter les méthodes publiques qui n'implémentent pas une interface
- Ne doivent jamais retourner `null`
- `null` ne doit pas être passé en argument
- Éviter de vérifier la validité des arguments entrants
- Respecter le principe CQRS : méthodes comme noms ou verbes
- Noms de méthodes : verbes simples, jamais composés
- Noms de variables : noms simples, jamais composés

#### Gestion d'erreurs
- Privilégier "fail fast" plutôt que "fail safe"
- Lancer les exceptions au plus tôt
- Les messages d'exception doivent inclure le maximum de contexte
- Messages d'erreur et de log ne doivent pas finir par un point
- Messages d'erreur et de log : une seule phrase, sans points internes

#### Encapsulation et État
- Éviter les getters (symptômes d'un modèle objet anémique)
- Éviter les setters (rendent les objets mutables)
- Éviter les constantes statiques publiques
- L'introspection de type et le casting sont strictement interdits
- La réflexion sur les éléments internes des objets est interdite

### Style de Code

#### Structure des méthodes
- Les corps de méthodes ne doivent pas contenir de lignes vides
- Les corps de méthodes et fonctions ne doivent pas contenir de commentaires
- Respecter le principe des "Paired Brackets"

#### Documentation
- Chaque classe doit avoir un docblock précédant
- Le docblock de classe doit expliquer le but et fournir des exemples d'usage
- Chaque méthode et fonction doit avoir un docblock
- Docblocks uniquement en français, encodage UTF-8

### Principes de Tests

#### Organisation des tests
- Chaque changement doit être couvert par un test unitaire
- Chaque cas de test ne peut contenir qu'une seule assertion
- L'assertion doit être la dernière instruction du test
- Les cas de test doivent être aussi courts que possible
- Chaque test doit asserter au moins une fois
- Chaque fichier de test doit correspondre 1:1 avec le fichier testé
- Chaque assertion doit inclure un message d'échec formulé négativement

#### Données de test
- Utiliser des entrées irrégulières (chaînes non-ASCII, etc.)
- Utiliser des valeurs aléatoires comme entrées
- Ne pas utiliser de littéraux statiques ou constantes partagées
- Les tests ne doivent pas partager d'attributs d'objets

#### Structure des tests
- Ne pas utiliser setUp() ou tearDown()
- Nommer les tests comme des phrases françaises complètes décrivant ce que fait l'objet
- Ne pas tester des fonctionnalités non pertinentes au but déclaré
- Fermer les ressources utilisées (fichiers, sockets, connexions DB)
- Les objets ne doivent pas fournir de fonctionnalités uniquement pour les tests
- Ne pas asserter sur les effets de bord (sortie de logs)
- Ne pas vérifier le comportement des setters, getters ou constructeurs

#### Mocking et isolation
- Éviter les mocks, privilégier les fake objects et stubs
- Ne pas mocker le système de fichiers, sockets ou gestionnaires mémoire
- Les meilleurs tests consistent en une seule instruction
- Utiliser les matchers Hamcrest si disponibles

#### Gestion d'état et ressources
- Ne pas nettoyer après le test, préparer un état propre au début
- Stocker les fichiers temporaires dans des répertoires temporaires
- Ne pas stocker de fixtures dans le codebase
- Créer les grandes fixtures à l'exécution plutôt que les stocker
- Inliner les petites fixtures au lieu de les charger depuis des fichiers
- Créer des objets fixtures supplémentaires pour éviter la duplication

## Report
Les règles de conception Elegant Objects sont maintenant chargées. Applique ces principes à tout le code que tu écris ou modifies.

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
