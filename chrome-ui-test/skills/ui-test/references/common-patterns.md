# Patterns Courants de Tests UI

## Patterns de Navigation

### Attendre le chargement complet
```
1. navigate vers URL
2. wait 2-3 secondes
3. read_page pour confirmer contenu chargé
```

### Navigation multi-pages
```
Pour chaque page :
- screenshot initial
- read_page pour identifier liens
- click sur lien cible
- wait 2s
- screenshot après navigation
```

## Patterns de Formulaires

### Formulaire basique (form_input)
```
1. read_page pour identifier champs (ref_id)
2. Pour chaque champ :
   - form_input avec ref et value
   - wait 0.5s
3. find "submit button" ou équivalent
4. computer click sur bouton
5. wait 2s
6. Valider résultat
```

### Formulaire complexe (computer type)
```
1. find ou read_page pour coordonnées
2. computer click sur champ
3. computer type avec texte
4. Répéter pour chaque champ
5. computer click sur submit
6. Attendre et valider
```

## Patterns de Validation

### Validation visuelle
```
Avant action :
- screenshot "before-[action].png"

Après action :
- screenshot "after-[action].png"

Comparer :
- Changement visible attendu
- Pas d'éléments cassés
- Layout correct
```

### Validation fonctionnelle
```
1. Exécuter action
2. read_page pour vérifier changement DOM
3. read_console_messages pattern="success|error"
4. read_network_requests urlPattern="/api/"
5. Vérifier :
   - Message UI correct
   - Pas d'erreurs console
   - API response 200/201
```

### Validation responsive
```
Pour chaque breakpoint :
1. resize_window
2. wait 1s (reflow)
3. screenshot
4. read_page avec filter="interactive"
5. Vérifier :
   - Menu hamburger visible (mobile)
   - Colonnes empilées (< 768px)
   - Pas de scroll horizontal
   - Boutons accessibles
```

## Patterns de Debug

### Identifier erreurs JavaScript
```
1. navigate vers page
2. wait 2s
3. read_console_messages pattern="error|exception|failed"
4. Analyser stack traces
5. Identifier ligne/fichier problématique
```

### Identifier requêtes échouées
```
1. Effectuer action
2. read_network_requests
3. Filtrer status codes 4xx, 5xx
4. Analyser :
   - URL de la requête
   - Payload si POST
   - Response body
   - Timing (lenteur ?)
```

### Debug interactif
```
1. navigate vers page
2. javascript_tool pour inspecter état :
   - window.appState
   - localStorage
   - sessionStorage
   - Variables globales
3. Modifier état si besoin pour reproduire bug
4. Continuer test
```

## Patterns d'Enregistrement

### GIF complet d'un parcours
```
1. gif_creator start_recording
2. screenshot initial (première frame)
3. Exécuter scénario avec waits entre actions
4. screenshot final (dernière frame)
5. gif_creator stop_recording
6. gif_creator export download=true
```

### Optimisation du GIF
```
Options pour export :
{
  quality: 10,  // 1-30 (10 = bon compromis)
  showClickIndicators: true,
  showActionLabels: true,
  showProgressBar: true
}
```

## Patterns de Scénarios Complexes

### Login avec validation 2FA
```
1. Remplir email/password
2. Submit
3. wait 2s
4. read_page pour trouver champ code 2FA
5. Demander code à l'utilisateur (pas automatisable)
6. Remplir code
7. Submit
8. Valider redirection dashboard
```

### Recherche avec autocomplete
```
1. find "search input"
2. computer click sur input
3. computer type premiers caractères
4. wait 1s (laisser autocomplete charger)
5. read_page pour voir suggestions
6. computer click sur suggestion
7. Valider résultats
```

### Upload de fichier
```
1. Préparer image avec screenshot
2. find file input (peut être caché)
3. upload_image avec imageId et ref
4. wait 2s
5. Vérifier preview ou confirmation
```

### Infinite scroll
```
1. read_page initiale
2. computer scroll down
3. wait 2s (charger plus)
4. read_page pour nouveaux éléments
5. Comparer avec état précédent
6. Répéter N fois
```

## Anti-Patterns à Éviter

❌ **Clic sans wait**
```
computer click
read_page immédiatement  // ❌ Trop rapide
```

✅ **Clic avec wait**
```
computer click
wait 1-2s
read_page  // ✅ Laisse temps de réagir
```

❌ **Hardcoder les coordonnées**
```
computer click coordinate=[500, 300]  // ❌ Fragile
```

✅ **Utiliser find ou ref**
```
find "login button"
computer click ref=ref_42  // ✅ Robuste
```

❌ **Ignorer les erreurs console**
```
Faire actions sans vérifier console  // ❌ Rate bugs JS
```

✅ **Vérifier console après actions critiques**
```
Action
read_console_messages pattern="error"  // ✅ Détecte bugs
```

❌ **Screenshots génériques**
```
screenshot  → image.png
screenshot  → image.png (écrase)  // ❌ Perd historique
```

✅ **Screenshots nommés**
```
screenshot → step-01-login.png
screenshot → step-02-dashboard.png  // ✅ Traçable
```

## Exemples de Tests Complets

### Test E2E Login → Dashboard
```
1. gif_creator start_recording
2. screenshot "00-initial.png"
3. navigate https://app.example.com/login
4. wait 2s
5. screenshot "01-login-page.png"
6. find "email input" → ref_1
7. form_input ref_1 "test@example.com"
8. find "password input" → ref_2
9. form_input ref_2 "password123"
10. screenshot "02-form-filled.png"
11. find "login button" → ref_3
12. computer click ref_3
13. wait 3s
14. screenshot "03-dashboard.png"
15. read_console_messages pattern="error"
16. read_network_requests urlPattern="/api/auth"
17. Valider :
    - URL = /dashboard
    - Pas erreurs console
    - API auth returned 200
    - Nom utilisateur visible
18. screenshot "04-final.png"
19. gif_creator stop_recording
20. gif_creator export download=true
```

### Test Responsive Homepage
```
Viewports = [375x667, 768x1024, 1920x1080]

Pour chaque viewport :
  1. resize_window width height
  2. wait 1s
  3. navigate https://example.com
  4. wait 2s
  5. screenshot "homepage-{width}x{height}.png"
  6. read_page filter="interactive"
  7. Vérifier :
     - Menu hamburger si < 768
     - Tous boutons visibles
     - Images pas déformées
  8. find "menu button" si mobile
  9. computer click menu
  10. screenshot "menu-open-{width}x{height}.png"
```

### Debug Page avec Erreurs
```
1. navigate https://example.com/broken
2. wait 3s
3. read_console_messages (tous messages)
4. read_network_requests
5. screenshot "page-state.png"
6. javascript_tool "window.errors || []"
7. Analyser :
   - Erreurs JS : fichier, ligne, message
   - Requêtes 4xx/5xx : URL, payload, response
   - État application : variables globales
8. Créer rapport avec :
   - Stack traces console
   - Requêtes échouées
   - Screenshot de l'état
   - Recommandations de fix
```
