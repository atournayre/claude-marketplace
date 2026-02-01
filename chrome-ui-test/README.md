# Plugin Chrome UI Test

Plugin de tests automatisés d'interface utilisateur dans Chrome pour Claude Code.

## Description

Ce plugin permet à Claude de tester automatiquement des interfaces web dans Chrome avec :

- 🔍 **Navigation et exploration** : parcourir des pages, cliquer sur liens et boutons
- 📸 **Validation visuelle** : capturer des screenshots à chaque étape
- ✅ **Tests fonctionnels** : exécuter des scénarios complets (login, formulaires, workflows)
- 📱 **Tests responsive** : vérifier l'affichage sur mobile, tablette, desktop
- 🐛 **Debug** : analyser console logs, requêtes réseau, erreurs JavaScript
- 🎬 **Enregistrement GIF** : générer un GIF animé du parcours utilisateur

## Installation

```bash
claude plugins install ./chrome-ui-test
```

## Skills Disponibles

### `/chrome-ui-test:ui-test` - Test UI Complet

Teste une interface utilisateur avec génération de rapport détaillé.

**Syntaxe :**
```bash
/chrome-ui-test:ui-test <URL> [options]
```

**Options :**
- `--scenario="description"` : Scénario de test à exécuter
- `--responsive` : Tester sur 3 tailles (mobile + tablette + desktop)
- `--mobile` : Tester uniquement sur mobile (375x667)
- `--tablet` : Tester uniquement sur tablette (768x1024)
- `--desktop` : Tester uniquement sur desktop (1920x1080)
- `--visual` : Capturer des screenshots
- `--debug` : Activer logs console et network
- `--gif` : Enregistrer un GIF du parcours
- `--viewport=WIDTHxHEIGHT` : Taille de fenêtre custom
- `--help` : Afficher le résumé des actions et demander confirmation

## Exemples d'Utilisation

### Test Simple de Navigation

```bash
/chrome-ui-test:ui-test https://example.com
```

**Résultat :**
- Navigation vers la page
- Vérification du chargement
- Exploration des éléments principaux
- Rapport avec erreurs détectées

### Voir ce qui sera fait (Mode Aide)

```bash
/chrome-ui-test:ui-test https://example.com --mobile --visual --help
```

**Résultat :**
- Affiche un résumé détaillé des actions prévues
- Liste toutes les options actives et leur signification
- Indique les fichiers qui seront générés
- Donne une estimation de durée
- Demande confirmation avant d'exécuter
- **Utile pour comprendre ce qui va se passer avant de lancer un test**

### Test de Scénario de Login avec GIF

```bash
/chrome-ui-test:ui-test https://app.example.com/login \
  --scenario="Je veux tester le login :
    1. Remplir email avec test@example.com
    2. Remplir password avec password123
    3. Cliquer sur bouton Se connecter
    4. Vérifier redirection vers /dashboard" \
  --gif
```

**Résultat :**
- Exécution du scénario étape par étape
- Screenshots à chaque étape
- GIF animé du parcours
- Validation des redirections et messages
- Rapport détaillé

### Test Responsive avec Screenshots

```bash
/chrome-ui-test:ui-test https://example.com \
  --responsive \
  --visual
```

**Résultat :**
- Test sur 3 viewports (mobile 375x667, tablette 768x1024, desktop 1920x1080)
- Screenshot pour chaque taille d'écran
- Validation de l'affichage responsive
- Rapport avec recommandations

### Test Mobile Uniquement

```bash
/chrome-ui-test:ui-test https://m.example.com \
  --mobile \
  --visual
```

**Résultat :**
- Test uniquement sur mobile (375x667)
- Plus rapide que --responsive
- Idéal pour sites mobile-first

### Debug d'une Page avec Erreurs

```bash
/chrome-ui-test:ui-test https://example.com/broken-page \
  --debug
```

**Résultat :**
- Capture des erreurs JavaScript console
- Liste des requêtes réseau échouées (4xx, 5xx)
- Analyse des stack traces
- Recommandations de fix

### Test de Formulaire Contact

```bash
/chrome-ui-test:ui-test https://example.com/contact \
  --scenario="Tester le formulaire :
    1. Remplir nom avec John Doe
    2. Remplir email avec john@example.com
    3. Remplir message avec Test message
    4. Cliquer sur Envoyer
    5. Vérifier message de confirmation" \
  --visual \
  --debug
```

**Résultat :**
- Remplissage automatique du formulaire
- Screenshots avant/après soumission
- Vérification de l'appel API
- Validation du message de succès
- Détection d'erreurs éventuelles

### Test E-commerce avec Viewport Custom

```bash
/chrome-ui-test:ui-test https://shop.example.com \
  --scenario="Parcours d'achat :
    1. Chercher 'laptop' dans la recherche
    2. Cliquer sur premier résultat
    3. Cliquer sur Ajouter au panier
    4. Aller au panier
    5. Vérifier que l'article est bien présent" \
  --viewport=1366x768 \
  --gif
```

## Structure du Rapport Généré

Le rapport est sauvegardé dans `/tmp/claude-*/scratchpad/ui-test-report-[timestamp].md`

```markdown
# Rapport de Test UI - https://example.com

**Date :** 2026-02-01 13:30:45
**Scénario :** Test de login
**Viewport(s) :** 1920x1080

## Résumé
- ✅ Tests réussis : 5
- ❌ Tests échoués : 0
- ⚠️  Avertissements : 1

## Actions Effectuées
1. Navigation vers https://example.com/login
2. Remplissage champ email
3. Remplissage champ password
4. Clic sur bouton "Se connecter"
5. Redirection vers /dashboard

## Résultats par Catégorie

### Navigation et Chargement
- Page charge en 1.2s ✅
- Redirection /login → /dashboard ✅

### Fonctionnalités
- Formulaire login fonctionne ✅
- Validation côté client active ✅

### Console et Erreurs
- Aucune erreur JavaScript ✅
- 1 warning : "Deprecated API usage" ⚠️

### Network
- POST /api/auth/login : 200 OK (350ms) ✅
- GET /api/user/profile : 200 OK (120ms) ✅

### Visuel
- Screenshots : 5 fichiers
  - step-01-login-page.png
  - step-02-form-filled.png
  - step-03-dashboard.png
  - ...

## Recommandations
1. Corriger le warning "Deprecated API usage" dans auth.js:42
2. Ajouter loading state pendant l'appel API login
3. Optimiser temps de chargement initial (1.2s → 0.8s)

## Fichiers Générés
- GIF : ui-test-recording-20260201-133045.gif
- Screenshots : 5 fichiers dans scratchpad/
```

## Cas d'Usage Avancés

### Test avec Upload de Fichier

```bash
/chrome-ui-test:ui-test https://example.com/upload \
  --scenario="Upload d'image :
    1. Prendre un screenshot de la page
    2. Utiliser upload_image pour uploader le screenshot
    3. Vérifier l'aperçu de l'image
    4. Soumettre le formulaire"
```

### Test d'Autocomplete

```bash
/chrome-ui-test:ui-test https://example.com/search \
  --scenario="Test autocomplete :
    1. Taper 'java' dans la recherche
    2. Attendre les suggestions (1s)
    3. Vérifier que suggestions contiennent 'JavaScript'
    4. Cliquer sur première suggestion"
```

### Test de Infinite Scroll

```bash
/chrome-ui-test:ui-test https://example.com/feed \
  --scenario="Test infinite scroll :
    1. Compter items initiaux
    2. Scroller vers le bas
    3. Attendre chargement (2s)
    4. Vérifier que nouveaux items apparaissent
    5. Répéter 3 fois"
```

## Bonnes Pratiques

### ✅ À Faire

- Toujours spécifier un scénario clair avec étapes numérotées
- Utiliser `--gif` pour documenter les parcours complexes
- Utiliser `--debug` dès qu'une page ne se comporte pas comme attendu
- Utiliser `--responsive` pour tout site public/e-commerce
- Nommer les actions de manière descriptive dans le scénario

### ❌ À Éviter

- Ne pas tester des pages nécessitant une authentification complexe (2FA, CAPTCHA)
- Ne pas hardcoder des coordonnées dans le scénario
- Ne pas oublier les temps d'attente entre actions
- Ne pas ignorer les erreurs console "non critiques"

## Limitations

- **CAPTCHA et 2FA** : non automatisables, nécessitent intervention manuelle
- **Contenu dynamique** : peut nécessiter des `wait` plus longs
- **Single Page Apps** : peuvent nécessiter des stratégies d'attente spécifiques
- **Vidéos et animations** : GIF peut être volumineux

## Dépannage

### "Tab invalide" ou "Tab not found"

La skill crée automatiquement un nouvel onglet. Si erreur persiste :
- Vérifier que Chrome est ouvert
- Vérifier que l'extension Claude in Chrome est active

### Screenshots vides ou noirs

- Ajouter `wait 2s` après navigation avant screenshot
- Vérifier que la page charge complètement

### GIF non généré

- Vérifier que `start_recording` a été appelé avant les actions
- Vérifier que `stop_recording` puis `export` ont été appelés
- Le GIF est téléchargé dans Downloads, pas dans scratchpad

### Éléments introuvables avec `find`

- Utiliser `read_page` pour voir les éléments disponibles
- Être plus spécifique dans la description ("email input" au lieu de "input")
- Utiliser `computer click` avec coordonnées en dernier recours

## Contribuer

Pour ajouter des patterns de test courants, modifier :
`skills/ui-test/references/common-patterns.md`

## Changelog

### v1.0.0 (2026-02-01)
- ✨ Création du plugin
- ✨ Skill `ui-test` avec tous types de tests
- 📚 Patterns courants et exemples
- 🎬 Support GIF recording
- 📱 Tests responsive
- 🐛 Mode debug avec console et network

## Auteur

**Aurélien Tournayre**
- GitHub: [@atournayre](https://github.com/atournayre)
- Email: aurelien.tournayre@gmail.com

## Licence

MIT
