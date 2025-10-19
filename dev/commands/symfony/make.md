---
allowed-tools: Bash,Read,SlashCommand
argument-hint: <tâche>
description: Cherche si il existe un maker Symfony pour faire la tache demandée et l'utilise si il existe. Si aucun maker n'existe alors utilise la slash command "/prepare"
model: claude-sonnet-4-5-20250929
---

# Symfony Maker - Générateur Intelligent

Recherche et utilise automatiquement les makers Symfony disponibles pour la tâche demandée. Si aucun maker approprié n'existe, génère un plan d'implémentation via `/prepare`.

## Purpose
Automatiser la création de code Symfony en utilisant les makers officiels lorsque disponibles, avec fallback vers la planification manuelle.

## Variables
- TASK: Description de la tâche à réaliser (ex: "créer un controller", "ajouter une entité")
- MAKER_COMMAND: Commande maker Symfony identifiée (ex: make:controller, make:entity)
- MAKER_ARGS: Arguments à passer au maker

## Instructions
Vous êtes un assistant Symfony expert qui :
- Identifie le maker Symfony approprié pour chaque tâche
- Vérifie la disponibilité du maker dans le projet
- Exécute le maker avec les bons arguments
- Génère un plan alternatif si aucun maker n'existe
- Valide la création et suggère les étapes suivantes

## Relevant Files
- `bin/console` - Console Symfony
- `config/packages/maker.yaml` - Configuration Maker Bundle
- `composer.json` - Dépendances incluant symfony/maker-bundle

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
- Enregistrer le timestamp pour calcul ultérieur

### Étape 1: Analyse de la tâche
- Parser la description de la tâche fournie
- Identifier les mots-clés Symfony (controller, entity, form, command, etc.)
- Déterminer le maker Symfony potentiel

### Étape 2: Vérification de l'environnement
- Vérifier la présence de `bin/console`
- Lister les makers disponibles : `bin/console list make`
- Confirmer que symfony/maker-bundle est installé

### Étape 3: Décision et exécution
**Si un maker existe :**
- Construire la commande maker avec arguments appropriés
- Demander confirmation à l'utilisateur si des paramètres sont requis
- Exécuter le maker via Bash
- Valider la création des fichiers

**Si aucun maker n'existe :**
- Informer l'utilisateur qu'aucun maker n'est disponible
- Utiliser SlashCommand pour exécuter `/prepare [TASK]`
- Transmettre la description complète de la tâche

### Étape 4: Rapport final
- Résumer les fichiers créés ou le plan généré
- Suggérer les prochaines étapes (tests, configuration, etc.)
- Afficher le timing de fin et la durée

## Expertise

### Mapping Tâche → Maker
- **Controller/Contrôleur** → `make:controller`
- **Entity/Entité** → `make:entity`
- **Form/Formulaire** → `make:form`
- **Command/Commande** → `make:command`
- **Voter** → `make:voter`
- **Event Subscriber** → `make:subscriber`
- **Service/Repository** → `make:service` ou `make:repository`
- **Test/Tests** → `make:test` ou `make:functional-test`
- **Fixture** → `make:fixtures`
- **CRUD** → `make:crud`
- **Authentication** → `make:auth`
- **Registration** → `make:registration-form`
- **Reset Password** → `make:reset-password`
- **Migration** → `make:migration`

### Makers courants
```bash
# Vérifier tous les makers disponibles
bin/console list make

# Makers les plus utilisés
make:controller      # Créer un controller
make:entity          # Créer/modifier une entité
make:form            # Créer un FormType
make:crud            # Générer CRUD complet
make:command         # Créer une commande console
make:subscriber      # Créer un event subscriber
make:voter           # Créer un voter de sécurité
make:test            # Créer un test unitaire
make:migration       # Générer migration DB
make:fixtures        # Créer des fixtures
```

## Examples

### Exemple 1: Créer un controller
```bash
# Input
/symfony:make "créer un controller pour gérer les utilisateurs"

# Sortie attendue
🕐 Démarrage: 2025-10-15 23:55:00 CEST

Analyse: création d'un controller
Maker identifié: make:controller

Exécution:
$ bin/console make:controller UserController

✅ Controller créé: src/Controller/UserController.php

Prochaines étapes:
- Ajouter les routes dans les annotations
- Créer les templates Twig associés
- Écrire les tests fonctionnels

---
✅ Terminé : 2025-10-15 23:55:12 CEST
⏱️ Durée : 12s
```

### Exemple 2: Créer une entité
```bash
# Input
/symfony:make "ajouter une entité Product avec nom et prix"

# Sortie attendue
🕐 Démarrage: 2025-10-15 23:56:00 CEST

Analyse: création d'une entité
Maker identifié: make:entity

Exécution:
$ bin/console make:entity Product

[Interactive] Ajout des champs:
- name (string, 255)
- price (decimal, 10,2)

✅ Entité créée: src/Entity/Product.php
✅ Repository créé: src/Repository/ProductRepository.php

Prochaines étapes:
- Générer la migration: bin/console make:migration
- Exécuter la migration: bin/console doctrine:migrations:migrate
- Créer les fixtures de test

---
✅ Terminé : 2025-10-15 23:56:45 CEST
⏱️ Durée : 45s
```

### Exemple 3: Tâche sans maker (fallback)
```bash
# Input
/symfony:make "implémenter un système de cache Redis personnalisé"

# Sortie attendue
🕐 Démarrage: 2025-10-15 23:57:00 CEST

Analyse: système de cache Redis personnalisé
Aucun maker Symfony disponible pour cette tâche

Génération du plan d'implémentation...
[Exécution de /prepare "implémenter un système de cache Redis personnalisé"]

---
✅ Terminé : 2025-10-15 23:57:30 CEST
⏱️ Durée : 30s
```

## Report

### Format du rapport
```markdown
🕐 Démarrage: [timestamp]

## Analyse de la tâche
- Tâche demandée: [TASK]
- Maker identifié: [MAKER_COMMAND ou "Aucun"]

## Exécution
[Commandes exécutées ou plan généré]

## Fichiers créés
- [Liste des fichiers]

## Prochaines étapes
- [Suggestions]

---
✅ Terminé : [timestamp]
⏱️ Durée : [durée]
```

## Best Practices
- Toujours vérifier la disponibilité du maker avant exécution
- Fournir le contexte complet au `/prepare` en cas de fallback
- Suggérer les commandes de migration si entité créée
- Proposer la création de tests associés
- Documenter les fichiers générés
- Afficher le timing au début et à la fin
