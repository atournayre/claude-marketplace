# Patterns de détection Elegant Objects

## Patterns Regex pour analyse

### Classes non-final
```php
/^class\s+\w+/  # sans 'final' avant
```

### Getters
```php
/public\s+function\s+get[A-Z]\w*\s*\(/
```

### Setters
```php
/public\s+function\s+set[A-Z]\w*\s*\(/
```

### Méthodes statiques
```php
/public\s+static\s+function/
```

### Noms en -er (anti-pattern)
```php
/class\s+\w+(er|or|Manager|Handler|Helper|Builder|Factory|Provider|Controller|Processor)\b/
```

### Retour null
```php
/return\s+null\s*;/
```

### Lignes vides dans méthodes
```php
/\{\s*\n\s*\n/  # ouverture suivie de ligne vide
```

### Commentaires dans corps
```php
/^\s+\/\//  # à l'intérieur des méthodes
```

## Règles de conception des classes

1. **Classes final** - Toutes les classes doivent être `final` (sauf abstraites)
2. **Attributs max 4** - Chaque classe encapsule 1 à 4 attributs maximum
3. **Pas de getters** - Éviter les méthodes `getX()` (modèle anémique)
4. **Pas de setters** - Éviter les méthodes `setX()` (mutabilité)
5. **Pas de méthodes statiques** - Strictement interdites dans les classes
6. **Pas de classes utilitaires** - Classes avec uniquement des méthodes statiques interdites
7. **Noms sans -er** - Noms de classes ne finissant pas par -er (Manager, Handler, Helper...)
8. **Constructeur unique** - Un seul constructeur principal par classe
9. **Constructeurs simples** - Ne contiennent que des affectations

## Règles de méthodes

1. **Pas de retour null** - Les méthodes ne doivent jamais retourner `null`
2. **Pas d'argument null** - `null` ne doit pas être passé en argument
3. **Corps sans lignes vides** - Les corps de méthodes sans lignes vides
4. **Corps sans commentaires** - Les corps de méthodes sans commentaires inline
5. **Noms verbes simples** - Noms de méthodes sont des verbes simples (pas composés)
6. **CQRS** - Séparation commandes (void) et queries (retour valeur)

## Règles de style

1. **Messages sans point final** - Messages d'erreur/log sans point final
2. **Messages une phrase** - Messages d'erreur/log en une seule phrase
3. **Fail fast** - Exceptions lancées au plus tôt

## Règles de tests

1. **Une assertion par test** - Chaque test ne contient qu'une assertion
2. **Assertion dernière** - L'assertion est la dernière instruction
3. **Pas de setUp/tearDown** - Ne pas utiliser ces méthodes
4. **Noms français** - Noms de tests en français décrivant le comportement
5. **Messages négatifs** - Assertions avec messages d'échec négatifs
6. **Pas de constantes partagées** - Pas de littéraux statiques partagés

## Format du rapport

```
## Score de conformité Elegant Objects

Score global: X/100

## Violations critiques (bloquantes)

### [Règle violée]
- **Fichier:** /chemin/fichier.php:ligne
- **Problème:** Description précise
- **Suggestion:** Code corrigé ou approche

## Violations majeures (à corriger)

[Même format]

## Recommandations (améliorations)

[Même format]

## Statistiques

- Fichiers analysés: X
- Classes analysées: Y
- Méthodes analysées: Z
- Tests analysés: W
- Total violations: N

## Prochaines étapes

Liste priorisée des corrections à effectuer
```

## Calcul du score

- Violation critique: -10 points
- Violation majeure: -5 points
- Recommandation: -2 points
- Score de base: 100

## Notes

- Ignorer fichiers vendor/, var/, cache/
- Contexte framework Symfony considéré (Controllers tolérés)
- Prioriser violations par criticité
- Proposer code corrigé quand possible
