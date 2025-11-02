---
model: claude-sonnet-4-5-20250929
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git push:*)
argument-hint: [message] | --no-verify | --push
description: Créer des commits bien formatés avec format conventional et emoji
---

# Commit Git Intelligent

Créer un commit bien formaté : $ARGUMENTS

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

## Ce Que Fait Cette Commande

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```

1. Sauf si spécifié avec --no-verify, exécute automatiquement les vérifications pre-commit :
    - make qa pour assurer la qualité du code
2. Vérifie quels fichiers sont stagés avec git status
3. Si 0 fichiers sont stagés, ajoute automatiquement tous les fichiers modifiés et nouveaux avec git add
4. Effectue un git diff pour comprendre les changements à commiter
5. Analyse le diff pour déterminer si plusieurs changements logiques distincts sont présents
6. Si plusieurs changements distincts sont détectés, suggère de diviser le commit en plusieurs commits plus petits
7. Pour chaque commit (ou le commit unique si pas de division), crée un message de commit utilisant le format conventional avec emoji
8. Si l'option --push est spécifiée, pousse automatiquement le(s) commit(s) vers le remote avec git push

## Bonnes Pratiques pour les Commits

- **Vérifier avant de commiter** : S'assurer que le code est linté, se build correctement, et que la documentation est à jour
- **Commits atomiques** : Chaque commit doit contenir des changements liés qui servent un seul objectif
- **Diviser les gros changements** : Si les changements touchent plusieurs préoccupations, les diviser en commits séparés
- **Format conventional commit** : Utiliser le format <type>: <description> où type est un de :
    - feat: Une nouvelle fonctionnalité
    - fix: Une correction de bug
    - docs: Changements de documentation
    - style: Changements de style de code (formatage, etc)
    - refactor: Changements de code qui ne corrigent pas de bugs ni n'ajoutent de fonctionnalités
    - perf: Améliorations de performance
    - test: Ajout ou correction de tests
    - chore: Changements du processus de build, outils, etc.
- **Présent, mode impératif** : Écrire les messages de commit comme des commandes (ex. "ajouter fonctionnalité" pas "ajouté fonctionnalité")
- **Première ligne concise** : Garder la première ligne sous 72 caractères
- **Emoji** : Chaque type de commit est associé à un emoji approprié :
    - ✨ feat: Nouvelle fonctionnalité
    - 🐛 fix: Correction de bug
    - 📝 docs: Documentation
    - 💄 style: Formatage/style
    - ♻️ refactor: Refactorisation de code
    - ⚡️ perf: Améliorations de performance
    - ✅ test: Tests
    - 🔧 chore: Outils, configuration
    - 🚀 ci: Améliorations CI/CD
    - 🗑️ revert: Annulation de changements
    - 🧪 test: Ajouter un test qui échoue
    - 🚨 fix: Corriger les warnings compilateur/linter
    - 🔒️ fix: Corriger les problèmes de sécurité
    - 👥 chore: Ajouter ou mettre à jour les contributeurs
    - 🚚 refactor: Déplacer ou renommer des ressources
    - 🏗️ refactor: Faire des changements architecturaux
    - 🔀 chore: Fusionner des branches
    - 📦️ chore: Ajouter ou mettre à jour les fichiers compilés ou packages
    - ➕ chore: Ajouter une dépendance
    - ➖ chore: Supprimer une dépendance
    - 🌱 chore: Ajouter ou mettre à jour les fichiers de seed
    - 🧑‍💻 chore: Améliorer l'expérience développeur
    - 🧵 feat: Ajouter ou mettre à jour le code lié au multithreading ou à la concurrence
    - 🔍️ feat: Améliorer le SEO
    - 🏷️ feat: Ajouter ou mettre à jour les types
    - 💬 feat: Ajouter ou mettre à jour le texte et les littéraux
    - 🌐 feat: Internationalisation et localisation
    - 👔 feat: Ajouter ou mettre à jour la logique métier
    - 📱 feat: Travailler sur le design responsive
    - 🚸 feat: Améliorer l'expérience utilisateur / utilisabilité
    - 🩹 fix: Correction simple pour un problème non-critique
    - 🥅 fix: Intercepter les erreurs
    - 👽️ fix: Mettre à jour le code suite aux changements d'API externe
    - 🔥 fix: Supprimer du code ou des fichiers
    - 🎨 style: Améliorer la structure/format du code
    - 🚑️ fix: Hotfix critique
    - 🎉 chore: Commencer un projet
    - 🔖 chore: Tags de release/version
    - 🚧 wip: Travail en cours
    - 💚 fix: Corriger le build CI
    - 📌 chore: Épingler les dépendances à des versions spécifiques
    - 👷 ci: Ajouter ou mettre à jour le système de build CI
    - 📈 feat: Ajouter ou mettre à jour le code d'analytics ou de tracking
    - ✏️ fix: Corriger les fautes de frappe
    - ⏪️ revert: Annuler les changements
    - 📄 chore: Ajouter ou mettre à jour la licence
    - 💥 feat: Introduire des changements cassants
    - 🍱 assets: Ajouter ou mettre à jour les assets
    - ♿️ feat: Améliorer l'accessibilité
    - 💡 docs: Ajouter ou mettre à jour les commentaires dans le code source
    - 🗃️ db: Effectuer des changements liés à la base de données
    - 🔊 feat: Ajouter ou mettre à jour les logs
    - 🔇 fix: Supprimer les logs
    - 🤡 test: Mocker des choses
    - 🥚 feat: Ajouter ou mettre à jour un easter egg
    - 🙈 chore: Ajouter ou mettre à jour le fichier .gitignore
    - 📸 test: Ajouter ou mettre à jour les snapshots
    - ⚗️ experiment: Effectuer des expériences
    - 🚩 feat: Ajouter, mettre à jour, ou supprimer les feature flags
    - 💫 ui: Ajouter ou mettre à jour les animations et transitions
    - ⚰️ refactor: Supprimer le code mort
    - 🦺 feat: Ajouter ou mettre à jour le code lié à la validation
    - ✈️ feat: Améliorer le support hors ligne

## Directives pour Diviser les Commits

Lors de l'analyse du diff, considérer diviser les commits selon ces critères :

1. **Préoccupations différentes** : Changements dans des parties non-liées du codebase
2. **Types de changements différents** : Mélange de fonctionnalités, corrections, refactorisation, etc.
3. **Patterns de fichiers** : Changements dans différents types de fichiers (ex. code source vs documentation)
4. **Groupement logique** : Changements qui seraient plus faciles à comprendre ou réviser séparément
5. **Taille** : Changements très larges qui seraient plus clairs s'ils étaient décomposés

## Exemples

Bons messages de commit :
- ✨ feat: ajouter système d'authentification utilisateur
- 🐛 fix: résoudre fuite mémoire dans le processus de rendu
- 📝 docs: mettre à jour documentation API avec nouveaux endpoints
- ♻️ refactor: simplifier la logique de gestion d'erreurs dans le parser
- 🚨 fix: résoudre warnings linter dans les fichiers de composants
- 🧑‍💻 chore: améliorer processus de setup des outils développeur
- 👔 feat: implémenter logique métier pour validation de transaction
- 🩹 fix: corriger incohérence de style mineure dans le header
- 🚑️ fix: patcher vulnérabilité de sécurité critique dans le flux d'auth
- 🎨 style: réorganiser structure des composants pour meilleure lisibilité
- 🔥 fix: supprimer code legacy déprécié
- 🦺 feat: ajouter validation d'entrée pour formulaire d'inscription utilisateur
- 💚 fix: résoudre tests CI pipeline qui échouent
- 📈 feat: implémenter tracking analytics pour engagement utilisateur
- 🔒️ fix: renforcer exigences de mot de passe d'authentification
- ♿️ feat: améliorer accessibilité des formulaires pour lecteurs d'écran

Exemple de division de commits :
- Premier commit : ✨ feat: ajouter définitions de types pour nouvelle version solc
- Deuxième commit : 📝 docs: mettre à jour documentation pour nouvelles versions solc
- Troisième commit : 🔧 chore: mettre à jour dépendances package.json
- Quatrième commit : 🏷️ feat: ajouter définitions de types pour nouveaux endpoints API
- Cinquième commit : 🧵 feat: améliorer gestion de concurrence dans worker threads
- Sixième commit : 🚨 fix: résoudre problèmes de linting dans nouveau code
- Septième commit : ✅ test: ajouter tests unitaires pour fonctionnalités nouvelle version solc
- Huitième commit : 🔒️ fix: mettre à jour dépendances avec vulnérabilités de sécurité

## Options de Commande

- --no-verify: Ignorer l'exécution des vérifications pre-commit (qa)
- --push: Pousser automatiquement le(s) commit(s) vers le remote après création

## Notes Importantes

- Par défaut, les vérifications pre-commit (qa) s'exécuteront pour assurer la qualité du code
- Si ces vérifications échouent, il vous sera demandé si vous voulez procéder au commit quand même ou corriger les problèmes d'abord
- Si des fichiers spécifiques sont déjà stagés, la commande ne commitera que ces fichiers
- Si aucun fichier n'est stagé, elle stagera automatiquement tous les fichiers modifiés et nouveaux
- Le message de commit sera construit basé sur les changements détectés
- Avant de commiter, la commande révisera le diff pour identifier si plusieurs commits seraient plus appropriés
- Si elle suggère plusieurs commits, elle vous aidera à stager et commiter les changements séparément
- Révise toujours le diff du commit pour s'assurer que le message correspond aux changements
- Avec --push, le commit sera automatiquement poussé vers le remote après création
- Les options peuvent être combinées : /git:commit --no-verify --push
