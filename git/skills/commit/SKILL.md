---
name: git:commit
description: Créer des commits bien formatés avec format conventional et emoji
model: claude-haiku-4-5-20251001
allowed-tools: [Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git push:*)]
argument-hint: [message] [--verify] [--no-push]
version: 1.0.0
license: MIT
hooks:
  PreToolUse:
    - matcher: "Bash(git commit:*)"
      hooks:
        - type: command
          command: |
            # Hook 1: Vérifier si --verify est passé en argument
            if echo "$ARGUMENTS" | grep -q -- "--verify"; then
              echo "🔍 Exécution de make qa..."
              make qa || {
                echo "❌ QA échouée. Voulez-vous continuer quand même ?"
                exit 1
              }
            fi
          once: false
    - matcher: "Bash(git status:*)"
      hooks:
        - type: command
          command: |
            # Hook 2: Vérifier qu'il y a des changements à committer
            if git diff --cached --quiet && git diff --quiet; then
              echo "❌ Aucun changement détecté (stagé ou non stagé)"
              exit 1
            fi
          once: true
  PostToolUse:
    - matcher: "Bash(git commit:*)"
      hooks:
        - type: command
          command: |
            # Hook 3: Push automatique avec tracking intelligent
            BRANCH=$(git branch --show-current)
            echo "✅ Commit créé : $(git log -1 --oneline)"

            # Vérifier si --no-push est passé
            if echo "$ARGUMENTS" | grep -q -- "--no-push"; then
              echo "📝 Commit local uniquement (--no-push)"
              exit 0
            fi

            # Vérifier si la branche a un tracking remote
            if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
              echo "🚀 Premier commit sur $BRANCH - configuration du tracking..."
              git push -u origin "$BRANCH"
              echo "✅ Branche pushée et tracking configuré"
            else
              echo "🚀 Push vers origin/$BRANCH..."
              git push
              echo "✅ Commit pushé"
            fi
          once: false
---

# Workflow Git Commit

Tu dois créer un commit bien formaté avec les arguments : $ARGUMENTS

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**

1. **Vérifications pre-commit (optionnel)**
   - Si l'utilisateur a passé `--verify`, exécute `make qa` d'abord
   - Si ça échoue, demande confirmation avant de continuer

2. **Vérifier les fichiers stagés**
   - Exécute `git status` pour voir ce qui est stagé
   - Exécute `git diff --cached` pour voir les changements stagés

3. **Stager automatiquement si nécessaire**
   - Si 0 fichiers stagés : exécute `git add .` pour tout ajouter
   - Puis re-vérifie avec `git status`

4. **Analyser les changements**
   - Exécute `git diff --cached` pour voir TOUS les changements
   - Analyse le diff pour détecter si plusieurs préoccupations distinctes sont mélangées

5. **Diviser si nécessaire**
   - Si plusieurs types de changements détectés (feat + docs + fix...), propose de diviser
   - Utilise `git add -p` ou `git reset` pour séparer les commits
   - Crée plusieurs commits atomiques successifs

6. **Créer le(s) commit(s)**
   - Analyse les changements pour déterminer le type (feat, fix, docs, etc.)
   - Choisis l'emoji approprié selon la table de référence ci-dessous
   - Construis un message format : `<emoji> <type>(<scope>): <description>`
   - **IMPORTANT : Utilise TOUJOURS un HEREDOC pour le message :**
   ```bash
   git commit -m "$(cat <<'EOF'
   <emoji> <type>: <description courte>

   <détails optionnels>
   EOF
   )"
   ```

7. **Push automatique**
   - Si l'utilisateur n'a PAS passé `--no-push`, exécute `git push`
   - Sinon, informe que le commit est local uniquement

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

- --verify: Exécuter les vérifications pre-commit (qa) avant de commiter
- --no-push: Ne pas pousser automatiquement le(s) commit(s) vers le remote après création

## Notes Importantes

- Par défaut, les vérifications pre-commit (qa) ne s'exécutent PAS pour permettre un workflow rapide
- Si vous utilisez --verify et que les vérifications échouent, il vous sera demandé si vous voulez procéder au commit quand même ou corriger les problèmes d'abord
- Si des fichiers spécifiques sont déjà stagés, la commande ne commitera que ces fichiers
- Si aucun fichier n'est stagé, elle stagera automatiquement tous les fichiers modifiés et nouveaux
- Le message de commit sera construit basé sur les changements détectés
- Avant de commiter, la commande révisera le diff pour identifier si plusieurs commits seraient plus appropriés
- Si elle suggère plusieurs commits, elle vous aidera à stager et commiter les changements séparément
- Révise toujours le diff du commit pour s'assurer que le message correspond aux changements
- Par défaut, le(s) commit(s) seront automatiquement poussés vers le remote après création
- Avec --no-push, le commit ne sera pas poussé et restera local
- Les options peuvent être combinées : /git:commit --verify --no-push
