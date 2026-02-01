---
name: ui-test
description: >
  Teste automatiquement une interface utilisateur dans Chrome : navigation, clics,
  validation visuelle, tests fonctionnels, responsive, comportement et debug.
  Génère un rapport détaillé avec screenshots et optionnellement un GIF du parcours.
allowed-tools: [
  mcp__claude-in-chrome__tabs_context_mcp,
  mcp__claude-in-chrome__tabs_create_mcp,
  mcp__claude-in-chrome__navigate,
  mcp__claude-in-chrome__read_page,
  mcp__claude-in-chrome__find,
  mcp__claude-in-chrome__computer,
  mcp__claude-in-chrome__form_input,
  mcp__claude-in-chrome__javascript_tool,
  mcp__claude-in-chrome__read_console_messages,
  mcp__claude-in-chrome__read_network_requests,
  mcp__claude-in-chrome__resize_window,
  mcp__claude-in-chrome__gif_creator,
  mcp__claude-in-chrome__update_plan,
  Write,
  Read,
  Bash
]
model: sonnet
---

# Chrome UI Test Skill

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape de manière proactive.**

## Usage

```
/chrome-ui-test:ui-test <URL> [options]
```

**Arguments :**
- `<URL>` : URL de la page à tester (obligatoire)

**Options :**
- `--scenario="description"` : Scénario de test à exécuter (ex: "login avec email/password")
- `--responsive` : Tester sur 3 tailles d'écran (mobile 375x667 + tablette 768x1024 + desktop 1920x1080)
- `--mobile` : Tester uniquement sur mobile (375x667)
- `--tablet` : Tester uniquement sur tablette (768x1024)
- `--desktop` : Tester uniquement sur desktop (1920x1080)
- `--visual` : Capturer des screenshots pour validation visuelle
- `--debug` : Activer le mode debug (console logs, network requests)
- `--gif` : Enregistrer un GIF du parcours utilisateur
- `--viewport=WIDTHxHEIGHT` : Taille de fenêtre custom (ex: 1366x768)
- `--help` : Afficher un résumé des actions qui seront effectuées (avec les options actives) et demander confirmation

**Exemples :**
```bash
# Test simple de navigation
/chrome-ui-test:ui-test https://example.com

# Test d'un scénario de login avec GIF
/chrome-ui-test:ui-test https://app.example.com/login --scenario="login avec credentials valides" --gif

# Test responsive (3 tailles : mobile + tablette + desktop)
/chrome-ui-test:ui-test https://example.com --responsive --visual

# Test mobile uniquement
/chrome-ui-test:ui-test https://m.example.com --mobile --visual

# Test desktop uniquement
/chrome-ui-test:ui-test https://example.com --desktop

# Debug d'une page avec erreurs
/chrome-ui-test:ui-test https://example.com/broken-page --debug

# Voir ce qui sera fait avant de lancer
/chrome-ui-test:ui-test https://example.com --mobile --visual --help
```

## Workflow

### Phase -1 : Mode Aide (si --help)

**IMPORTANT : Cette phase s'exécute UNIQUEMENT si l'option --help est présente.**

1. **Analyser l'URL et les options**
   - URL cible : afficher l'URL qui sera testée
   - Options actives : lister toutes les options détectées

2. **Générer le résumé des actions**
   ```
   📋 RÉSUMÉ DU TEST UI

   🎯 URL cible : [URL]

   📐 Configuration viewport :
   [Si --responsive] → Tests sur 3 viewports (mobile 375x667, tablette 768x1024, desktop 1920x1080)
   [Si --mobile] → Test mobile uniquement (375x667)
   [Si --tablet] → Test tablette uniquement (768x1024)
   [Si --desktop] → Test desktop uniquement (1920x1080)
   [Si --viewport=WxH] → Viewport custom WxH
   [Sinon] → Viewport par défaut (1920x1080)

   🎬 Actions prévues :
   1. Créer un nouvel onglet Chrome dédié
   2. [Si viewport spécifique] Redimensionner la fenêtre
   3. [Si --gif] Démarrer l'enregistrement GIF
   4. Naviguer vers l'URL
   5. [Si --scenario] Exécuter le scénario : [description du scénario]
   6. [Sinon] Explorer la page (tests basiques)
   7. [Si --visual] Capturer des screenshots à chaque étape
   8. [Si --debug] Analyser console logs et network requests
   9. [Si --responsive] Répéter tests sur chaque viewport
   10. [Si --gif] Arrêter enregistrement et exporter le GIF
   11. Générer rapport détaillé

   ⚙️ Options actives :
   [Liste toutes les options avec leur signification]

   📊 Résultats attendus :
   - Rapport Markdown : /tmp/claude-*/scratchpad/ui-test-report-[timestamp].md
   [Si --visual] - Screenshots : /tmp/claude-*/scratchpad/step-*.png
   [Si --gif] - GIF animé : téléchargé dans Downloads/ui-test-recording-*.gif
   [Si --responsive] - [X] screenshots (X par viewport)

   ⏱️ Durée estimée : [estimer selon options : 30s simple, 1-2min avec scénario, 2-3min responsive, etc.]
   ```

3. **Demander confirmation**
   - Afficher : "Voulez-vous lancer ce test ? (oui/non)"
   - Attendre réponse utilisateur
   - Si "oui" ou "yes" ou "o" : continuer vers Phase 0
   - Si "non" ou "no" ou "n" : arrêter et afficher "Test annulé"
   - Toute autre réponse : redemander

### Phase 0 : Initialisation (OBLIGATOIRE)

1. **Récupérer le contexte Chrome**
   ```
   Utiliser mcp__claude-in-chrome__tabs_context_mcp avec createIfEmpty=true
   ```

2. **Créer un nouvel onglet dédié**
   ```
   Utiliser mcp__claude-in-chrome__tabs_create_mcp
   Stocker le tabId pour toutes les opérations suivantes
   ```

3. **Présenter le plan à l'utilisateur**
   ```
   Utiliser mcp__claude-in-chrome__update_plan avec :
   - domains: liste des domaines qui seront visités
   - approach: liste des actions qui seront effectuées
   ```

4. **Configurer la fenêtre**
   - Si `--viewport=WxH` : utiliser `resize_window` avec les dimensions custom
   - Si `--mobile` : utiliser `resize_window` avec 375x667
   - Si `--tablet` : utiliser `resize_window` avec 768x1024
   - Si `--desktop` : utiliser `resize_window` avec 1920x1080
   - Si `--responsive` : préparer liste des 3 viewports à tester (375x667, 768x1024, 1920x1080)
   - Sinon (aucune option) : viewport par défaut 1920x1080

5. **Démarrer l'enregistrement GIF (si --gif)**
   ```
   Utiliser gif_creator avec action="start_recording"
   ```

### Phase 1 : Navigation et Exploration

1. **Naviguer vers l'URL**
   ```
   Utiliser navigate avec l'URL fournie et le tabId
   Attendre le chargement complet (wait 2-3 secondes)
   ```

2. **Capturer screenshot initial (si --visual ou --gif)**
   ```
   Utiliser computer avec action="screenshot"
   Sauvegarder avec nom descriptif
   ```

3. **Lire la structure de la page**
   ```
   Utiliser read_page pour obtenir l'arbre d'accessibilité
   Identifier les éléments clés : formulaires, boutons, liens
   ```

4. **Mode debug (si --debug)**
   ```
   - Lire console_messages avec pattern pertinent
   - Lire network_requests pour voir les appels API
   - Identifier erreurs JavaScript ou requêtes échouées
   ```

### Phase 2 : Exécution du Scénario

**Si `--scenario` est fourni :**

1. **Analyser le scénario**
   - Décomposer en étapes atomiques
   - Identifier les éléments à manipuler
   - Définir les validations attendues

2. **Exécuter chaque étape**
   ```
   Pour chaque action :
   a. find ou read_page pour localiser l'élément
   b. computer (click/type) ou form_input pour interagir
   c. Attendre réaction (wait 1-2s)
   d. Vérifier résultat (read_page, console, network)
   e. Screenshot si --visual
   ```

3. **Validations**
   - Vérifier les changements de page (navigate, URL)
   - Vérifier les messages d'erreur ou de succès
   - Vérifier les appels API (network_requests)
   - Vérifier la console (pas d'erreurs JS)

**Sinon (exploration libre) :**

1. **Tests basiques**
   - Vérifier que la page charge sans erreur 404/500
   - Vérifier absence d'erreurs JavaScript console
   - Tester les liens principaux (clic sur 2-3 liens majeurs)
   - Vérifier formulaires (remplir et valider un formulaire si présent)

### Phase 3 : Tests Responsive (si --responsive)

**Viewports à tester :**
- Mobile : 375x667 (iPhone)
- Tablette : 768x1024 (iPad)
- Desktop : 1920x1080

**Pour chaque viewport :**
1. `resize_window` avec les dimensions
2. `wait` 1 seconde pour le reflow
3. `screenshot` avec nom incluant la taille
4. `read_page` pour vérifier éléments visibles
5. Valider :
   - Pas d'overflow horizontal
   - Éléments empilés correctement
   - Pas d'éléments coupés
   - Menu mobile fonctionnel (si < 768px)

### Phase 4 : Génération du Rapport

1. **Arrêter l'enregistrement GIF (si --gif)**
   ```
   - gif_creator avec action="stop_recording"
   - gif_creator avec action="export", download=true
   - Attendre téléchargement
   ```

2. **Compiler les résultats**
   - Résumé des actions effectuées
   - Screenshots capturés (liste avec descriptions)
   - Erreurs détectées (console, network, visuel)
   - Validations réussies/échouées
   - Recommandations d'amélioration

3. **Créer rapport Markdown**
   ```markdown
   # Rapport de Test UI - [URL]

   **Date :** [timestamp]
   **Scénario :** [description ou "exploration libre"]
   **Viewport(s) :** [liste]

   ## Résumé
   - ✅ Tests réussis : X
   - ❌ Tests échoués : Y
   - ⚠️  Avertissements : Z

   ## Actions Effectuées
   1. Navigation vers [URL]
   2. [liste des actions]

   ## Résultats par Catégorie

   ### Navigation et Chargement
   - Page charge en Xs
   - [détails]

   ### Fonctionnalités
   - [résultats des interactions]

   ### Console et Erreurs
   - [erreurs JS trouvées]

   ### Network
   - [appels API, erreurs HTTP]

   ### Visuel (si --visual)
   - Screenshots : [liste avec chemins]

   ### Responsive (si --responsive)
   - Mobile : [résultat]
   - Tablette : [résultat]
   - Desktop : [résultat]

   ## Recommandations
   1. [amélioration 1]
   2. [amélioration 2]

   ## Fichiers Générés
   - GIF : [chemin] (si --gif)
   - Screenshots : [liste]
   ```

4. **Sauvegarder le rapport**
   ```
   Utiliser Write pour créer :
   /tmp/claude-*/scratchpad/ui-test-report-[timestamp].md
   ```

## Gestion des Erreurs

### Erreurs de Navigation
- URL invalide → arrêter et signaler
- Page 404/500 → noter dans rapport et continuer
- Timeout → réessayer 1 fois, puis noter

### Erreurs d'Interaction
- Élément introuvable → noter et passer au suivant
- Clic échoué → réessayer avec coordonnées ajustées
- Formulaire non soumis → vérifier console/network

### Erreurs Chrome
- Tab invalide → recreate tab avec tabs_create_mcp
- Extension non responsive → attendre 5s max puis timeout

## Bonnes Pratiques

1. **Toujours attendre après interactions**
   - 1-2s après click/type
   - 2-3s après navigation
   - Éviter les race conditions

2. **Screenshots descriptifs**
   - Nommer : `step-01-homepage.png`
   - Capturer AVANT et APRÈS actions critiques

3. **GIF Recording**
   - Démarrer AVANT première action
   - Arrêter APRÈS dernière validation
   - Screenshot initial et final pour frames propres

4. **Console Logs**
   - Utiliser `pattern` pour filtrer (éviter spam)
   - Chercher `error|warn|failed` si debug
   - `clear=true` après lecture pour éviter doublons

5. **Network Requests**
   - Utiliser `urlPattern` si recherche spécifique
   - Vérifier status codes (4xx, 5xx)
   - Noter les API lentes (> 2s)

## Exemples de Scénarios

### Login Standard
```
--scenario="Je veux tester le login :
1. Remplir email avec test@example.com
2. Remplir password avec Test123!
3. Cliquer sur bouton Se connecter
4. Vérifier redirection vers dashboard"
```

### Formulaire Contact
```
--scenario="Tester formulaire contact :
1. Remplir nom, email, message
2. Soumettre
3. Vérifier message de confirmation
4. Vérifier appel API POST réussi"
```

### Navigation E-commerce
```
--scenario="Parcours d'achat :
1. Chercher 'laptop'
2. Cliquer sur premier résultat
3. Ajouter au panier
4. Aller au panier
5. Vérifier article présent"
```

## Notes Importantes

- **TOUJOURS** créer un nouvel onglet (tabs_create_mcp) au début
- **TOUJOURS** utiliser le même tabId pour toutes les opérations
- **JAMAIS** réutiliser un tabId d'une session précédente
- **TOUJOURS** présenter le plan (update_plan) avant d'agir
- Sauvegarder tous les fichiers dans le scratchpad
- Mode debug active automatiquement console + network
- GIF enregistre toutes les interactions automatiquement
