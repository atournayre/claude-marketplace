# Exemples Complets de Tests UI

## 0. Mode Aide - Comprendre ce qui sera fait

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com --mobile --visual --scenario="Test du formulaire contact" --help
```

**Résultat Affiché :**
```
📋 RÉSUMÉ DU TEST UI

🎯 URL cible : https://example.com

📐 Configuration viewport :
→ Test mobile uniquement (375x667)

🎬 Actions prévues :
1. Créer un nouvel onglet Chrome dédié
2. Redimensionner la fenêtre en mode mobile (375x667)
3. Naviguer vers https://example.com
4. Exécuter le scénario : Test du formulaire contact
5. Capturer des screenshots à chaque étape
6. Générer rapport détaillé

⚙️ Options actives :
- --mobile : Test sur viewport mobile (375x667)
- --visual : Captures d'écran activées à chaque étape
- --scenario : Exécution d'un scénario personnalisé
- --help : Mode aide (ce résumé)

📊 Résultats attendus :
- Rapport Markdown : /tmp/claude-*/scratchpad/ui-test-report-[timestamp].md
- Screenshots : /tmp/claude-*/scratchpad/step-*.png

⏱️ Durée estimée : 1-2 minutes

Voulez-vous lancer ce test ? (oui/non)
```

**Utilité :**
- Comprendre exactement ce qui va se passer
- Vérifier les options avant de lancer
- Annuler si ce n'est pas ce que tu veux

---

## 1. Test de Login E2E avec Validation

**Commande :**
```bash
/chrome-ui-test:ui-test https://demo.example.com/login \
  --scenario="Test du flow de login complet :
    1. Vérifier que la page de login s'affiche
    2. Remplir le champ email avec demo@example.com
    3. Remplir le champ password avec Demo123!
    4. Cliquer sur le bouton Se connecter
    5. Attendre la redirection
    6. Vérifier que l'URL devient /dashboard
    7. Vérifier que le nom de l'utilisateur s'affiche
    8. Vérifier qu'aucune erreur console n'apparaît" \
  --visual \
  --debug \
  --gif
```

**Résultat Attendu :**
- ✅ Page login charge correctement
- ✅ Formulaire rempli avec succès
- ✅ Redirection vers /dashboard
- ✅ Nom utilisateur visible
- ✅ Aucune erreur console
- ✅ API /auth/login retourne 200
- 📸 5-6 screenshots du parcours
- 🎬 GIF du login complet

**Rapport Généré :**
```
✅ Tests réussis : 8
❌ Tests échoués : 0
⚠️  Avertissements : 0

Fichiers :
- ui-test-recording-*.gif
- step-01-login-page.png
- step-02-form-filled.png
- step-03-loading.png
- step-04-dashboard.png
```

---

## 2. Test Responsive de Homepage

**Commande :**
```bash
/chrome-ui-test:ui-test https://www.example.com \
  --responsive \
  --visual \
  --scenario="Vérifier l'affichage responsive :
    1. Sur mobile : vérifier que le menu hamburger est visible
    2. Sur mobile : ouvrir le menu et vérifier les liens
    3. Sur tablette : vérifier que les colonnes sont empilées
    4. Sur desktop : vérifier que le layout à 3 colonnes fonctionne
    5. Pour chaque taille : vérifier qu'il n'y a pas de scroll horizontal"
```

**Résultat Attendu :**
- 📱 Mobile (375x667) : menu hamburger ✅
- 📱 Tablette (768x1024) : colonnes empilées ✅
- 💻 Desktop (1920x1080) : layout 3 colonnes ✅
- ✅ Pas de scroll horizontal sur aucune taille
- 📸 9 screenshots (3 par viewport)

**Rapport Généré :**
```
### Responsive
- Mobile (375x667) : ✅
  - Menu hamburger visible
  - Navigation fonctionnelle
  - Pas d'overflow
- Tablette (768x1024) : ✅
  - Colonnes empilées correctement
  - Images redimensionnées
- Desktop (1920x1080) : ✅
  - Layout 3 colonnes
  - Tous éléments visibles

Screenshots :
- homepage-375x667.png
- menu-open-375x667.png
- homepage-768x1024.png
- homepage-1920x1080.png
```

---

## 3. Test de Formulaire Contact avec Validation

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com/contact \
  --scenario="Tester le formulaire de contact :
    1. Vérifier que tous les champs sont présents (nom, email, message)
    2. Tester validation : soumettre formulaire vide
    3. Vérifier messages d'erreur de validation
    4. Remplir nom avec Jean Dupont
    5. Remplir email avec jean.dupont@example.com
    6. Remplir message avec Ceci est un message de test
    7. Soumettre le formulaire
    8. Vérifier le message de confirmation
    9. Vérifier que l'API POST /contact retourne 201
    10. Vérifier qu'un email de confirmation est mentionné" \
  --visual \
  --debug
```

**Résultat Attendu :**
- ✅ Formulaire avec 3 champs détecté
- ✅ Validation côté client fonctionne
- ✅ Messages d'erreur affichés correctement
- ✅ Soumission réussie avec données valides
- ✅ Message de confirmation visible
- ✅ API POST /contact : 201 Created
- 📸 Screenshots des états (vide, erreurs, rempli, succès)

---

## 4. Debug d'une Page avec Erreurs

**Commande :**
```bash
/chrome-ui-test:ui-test https://staging.example.com/broken-feature \
  --debug \
  --scenario="Analyser les erreurs de la page :
    1. Charger la page et attendre 3 secondes
    2. Identifier toutes les erreurs JavaScript console
    3. Identifier toutes les requêtes HTTP échouées
    4. Tenter de cliquer sur le bouton principal
    5. Observer les erreurs après le clic
    6. Inspecter l'état de l'application avec JavaScript"
```

**Résultat Attendu :**
- 🐛 Erreurs console identifiées avec stack traces
- 🐛 Requêtes 4xx/5xx listées
- 🐛 État de l'application inspecté
- 📊 Rapport détaillé avec recommandations de fix

**Rapport Généré :**
```
❌ Tests échoués : 3
⚠️  Avertissements : 2

### Erreurs Console
1. TypeError: Cannot read property 'data' of undefined
   - Fichier: app.js:156
   - Stack: [trace complet]

2. ReferenceError: jQuery is not defined
   - Fichier: main.js:42

### Requêtes Échouées
1. GET /api/user/profile : 401 Unauthorized
   - Temps: 250ms
   - Response: {"error": "Token expired"}

2. GET /static/image.png : 404 Not Found

### Recommandations
1. Corriger app.js:156 - vérifier que response.data existe
2. Charger jQuery avant main.js
3. Régénérer token d'auth pour /api/user/profile
4. Vérifier chemin de l'image manquante
```

---

## 5. Test E-commerce : Ajout au Panier

**Commande :**
```bash
/chrome-ui-test:ui-test https://shop.example.com \
  --scenario="Parcours d'achat complet :
    1. Sur la homepage, utiliser la recherche pour chercher laptop
    2. Attendre les résultats de recherche
    3. Vérifier qu'au moins 3 produits sont affichés
    4. Cliquer sur le premier produit
    5. Attendre le chargement de la fiche produit
    6. Vérifier que le prix est affiché
    7. Cliquer sur Ajouter au panier
    8. Vérifier le message de confirmation
    9. Cliquer sur l'icône panier
    10. Vérifier que le produit est bien dans le panier
    11. Vérifier que le total est correct" \
  --gif \
  --visual \
  --debug
```

**Résultat Attendu :**
- ✅ Recherche fonctionne
- ✅ Résultats affichés (>= 3 produits)
- ✅ Fiche produit charge
- ✅ Ajout au panier réussi
- ✅ Produit visible dans panier
- ✅ Total calculé correctement
- 🎬 GIF du parcours complet
- 📸 10+ screenshots

---

## 6. Test d'Autocomplete de Recherche

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com \
  --scenario="Test autocomplete :
    1. Localiser le champ de recherche
    2. Cliquer dans le champ
    3. Taper les lettres p-y-t-h-o (une par une)
    4. Attendre 1 seconde après chaque lettre
    5. Vérifier que des suggestions apparaissent
    6. Vérifier que Python est dans les suggestions
    7. Cliquer sur la suggestion Python
    8. Vérifier que la recherche est lancée avec Python" \
  --visual
```

**Résultat Attendu :**
- ✅ Autocomplete s'active après 2-3 lettres
- ✅ Suggestions pertinentes affichées
- ✅ Clic sur suggestion fonctionne
- ✅ Recherche lancée avec le bon terme
- 📸 Screenshots de l'évolution de l'autocomplete

---

## 7. Test de Modal/Popup

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com \
  --scenario="Test ouverture et fermeture de modal :
    1. Cliquer sur le bouton Ouvrir modal
    2. Vérifier que la modal s'affiche
    3. Vérifier que le fond est assombri (overlay)
    4. Lire le contenu de la modal
    5. Cliquer sur le bouton Fermer (X)
    6. Vérifier que la modal se ferme
    7. Réouvrir la modal
    8. Cliquer en dehors de la modal (sur overlay)
    9. Vérifier que la modal se ferme aussi" \
  --visual
```

**Résultat Attendu :**
- ✅ Modal s'ouvre au clic
- ✅ Overlay visible
- ✅ Fermeture avec bouton X fonctionne
- ✅ Fermeture en cliquant overlay fonctionne
- 📸 Screenshots des états (fermée, ouverte)

---

## 8. Test de Tableau avec Tri

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com/users \
  --scenario="Test tri de tableau :
    1. Identifier le tableau d'utilisateurs
    2. Cliquer sur en-tête colonne Nom pour trier
    3. Vérifier que les noms sont triés alphabétiquement (A-Z)
    4. Cliquer à nouveau sur Nom
    5. Vérifier que le tri s'inverse (Z-A)
    6. Cliquer sur en-tête colonne Date
    7. Vérifier que les dates sont triées
    8. Vérifier qu'une seule colonne a l'indicateur de tri actif" \
  --visual \
  --debug
```

**Résultat Attendu :**
- ✅ Tri par nom fonctionne (A-Z puis Z-A)
- ✅ Tri par date fonctionne
- ✅ Indicateur visuel de tri correct
- ✅ Requête API de tri si applicable
- 📸 Screenshots des différents états de tri

---

## 9. Test de Pagination

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com/articles \
  --scenario="Test pagination :
    1. Vérifier que la page 1 est active
    2. Compter le nombre d'articles affichés
    3. Cliquer sur Page 2
    4. Vérifier que l'URL change (ou état change)
    5. Vérifier que de nouveaux articles s'affichent
    6. Cliquer sur Suivant
    7. Vérifier passage à la page 3
    8. Cliquer sur Précédent
    9. Vérifier retour à la page 2" \
  --debug
```

**Résultat Attendu :**
- ✅ Navigation entre pages fonctionne
- ✅ URL ou état mis à jour correctement
- ✅ Nouveaux contenus chargés
- ✅ Boutons Suivant/Précédent fonctionnent
- ✅ Requêtes API paginées détectées

---

## 10. Test d'Accessibilité Basique

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com \
  --scenario="Vérifications d'accessibilité :
    1. Vérifier que tous les boutons ont un label visible
    2. Vérifier que toutes les images ont un attribut alt
    3. Tester navigation au clavier : Tab entre éléments interactifs
    4. Vérifier que le focus est visible
    5. Vérifier le contraste des textes (console warnings)
    6. Vérifier structure des headings (h1, h2, h3...)" \
  --debug \
  --visual
```

**Résultat Attendu :**
- ✅ Tous boutons labellisés
- ✅ Toutes images ont alt
- ✅ Navigation clavier fonctionne
- ✅ Focus visible
- ⚠️  Warnings de contraste si problèmes
- ✅ Hiérarchie des headings correcte

---

## 11. Test de Formulaire Multi-étapes

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com/signup \
  --scenario="Inscription en 3 étapes :
    Étape 1 - Informations personnelles :
    1. Remplir prénom avec Alice
    2. Remplir nom avec Martin
    3. Remplir email avec alice.martin@example.com
    4. Cliquer sur Suivant

    Étape 2 - Informations de compte :
    5. Remplir nom d'utilisateur avec alicemartin
    6. Remplir mot de passe avec SecureP@ss123
    7. Confirmer mot de passe avec SecureP@ss123
    8. Cliquer sur Suivant

    Étape 3 - Préférences :
    9. Cocher newsletter
    10. Sélectionner langue Français
    11. Cliquer sur Terminer l'inscription

    Validation :
    12. Vérifier message de bienvenue
    13. Vérifier redirection vers /welcome
    14. Vérifier appel API POST /users" \
  --gif \
  --visual \
  --debug
```

**Résultat Attendu :**
- ✅ 3 étapes complétées
- ✅ Validation à chaque étape
- ✅ Inscription finalisée
- ✅ API POST /users : 201 Created
- 🎬 GIF du processus complet
- 📸 Screenshot de chaque étape

---

## 12. Test de Upload de Fichier

**Commande :**
```bash
/chrome-ui-test:ui-test https://example.com/upload \
  --scenario="Test upload d'image :
    1. Prendre un screenshot de la page actuelle
    2. Localiser le champ file input (peut être caché)
    3. Utiliser upload_image pour uploader le screenshot
    4. Vérifier qu'un aperçu de l'image apparaît
    5. Vérifier le nom du fichier affiché
    6. Cliquer sur Envoyer
    7. Vérifier message de succès
    8. Vérifier appel API POST /upload avec multipart/form-data" \
  --visual \
  --debug
```

**Résultat Attendu :**
- ✅ Screenshot capturé
- ✅ Upload réussi
- ✅ Aperçu affiché
- ✅ Nom de fichier correct
- ✅ Soumission réussie
- ✅ API POST /upload : 200 OK

---

## Templates de Scénarios Réutilisables

### Template Login
```
Test de login :
1. Remplir email avec {EMAIL}
2. Remplir password avec {PASSWORD}
3. Cliquer sur {LOGIN_BUTTON}
4. Vérifier redirection vers {SUCCESS_URL}
5. Vérifier élément {USER_INDICATOR} visible
```

### Template Recherche
```
Test de recherche :
1. Localiser champ de recherche
2. Taper {SEARCH_TERM}
3. Soumettre (Enter ou clic bouton)
4. Vérifier {MIN_RESULTS} résultats minimum
5. Vérifier premier résultat contient {EXPECTED_TEXT}
```

### Template Formulaire
```
Test formulaire :
1. Pour chaque champ : remplir avec {FIELD_DATA}
2. Vérifier validation côté client si champ invalide
3. Soumettre formulaire
4. Vérifier message {SUCCESS_MESSAGE}
5. Vérifier appel API {API_ENDPOINT} retourne {STATUS_CODE}
```

### Template CRUD
```
Test CRUD :
CREATE:
1. Cliquer Nouveau
2. Remplir formulaire avec {DATA}
3. Sauvegarder
4. Vérifier création réussie

READ:
5. Rechercher élément créé
6. Vérifier données affichées

UPDATE:
7. Cliquer Modifier
8. Changer {FIELD} en {NEW_VALUE}
9. Sauvegarder
10. Vérifier modification

DELETE:
11. Cliquer Supprimer
12. Confirmer
13. Vérifier disparition
```

---

## Commandes de Debug Rapide

### Vérifier si une page charge
```bash
/chrome-ui-test:ui-test https://example.com --debug
```

### Capturer l'état visuel actuel
```bash
/chrome-ui-test:ui-test https://example.com --visual --scenario="Prendre screenshot de la page"
```

### Identifier erreurs JS
```bash
/chrome-ui-test:ui-test https://example.com --debug --scenario="Lire toutes les erreurs console"
```

### Tester sur mobile rapidement
```bash
/chrome-ui-test:ui-test https://example.com --viewport=375x667 --visual
```

### Générer GIF de navigation
```bash
/chrome-ui-test:ui-test https://example.com --gif --scenario="Naviguer vers /about puis /contact"
```
