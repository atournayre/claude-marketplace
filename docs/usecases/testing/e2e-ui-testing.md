---
title: Test UI E2E avec scénario
description: Tests end-to-end avec Chrome automation, GIF recording et debug mode
category: testing
plugins:
  - name: chrome-ui-test
    skills: [/chrome-ui-test:ui-test]
complexity: 2
duration: 10
keywords: [e2e, ui, chrome, automation, testing, gif]
related:
  - /usecases/testing/responsive-testing
  - /usecases/development/full-feature-workflow
---

# Test UI E2E avec scénario <Badge type="info" text="★★ Intermédiaire" /> <Badge type="tip" text="~10 min" />

## Contexte

Tester manuellement les parcours utilisateurs dans une application web est chronophage et source d'oublis. Les tests E2E automatisés permettent de valider les scénarios critiques rapidement.

## Objectif

Automatiser les tests UI end-to-end avec :

- ✅ Chrome automation (navigation, clicks, forms)
- ✅ Enregistrement GIF du scénario
- ✅ Assertions visuelles et fonctionnelles
- ✅ Debug mode avec screenshots
- ✅ Rapport détaillé des résultats

## Prérequis

**Plugins :**
- [chrome-ui-test](/plugins/chrome-ui-test) - Chrome automation

**Outils :**
- Google Chrome installé
- Extension Claude in Chrome installée
- Application web accessible (local ou remote)

**Configuration :**
Aucune configuration particulière nécessaire.

## Workflow Étape par Étape

### Phase 1 : Définir le scénario de test

**Commande :**
```bash
/chrome-ui-test:ui-test
```

Claude te demande de décrire le scénario à tester.

**Exemple de scénario :**
```
Tester le parcours d'achat :
1. Ouvrir https://example.com/shop
2. Rechercher "laptop"
3. Cliquer sur le premier produit
4. Ajouter au panier
5. Aller au panier
6. Vérifier que le produit est présent
7. Valider que le total est correct
```

### Phase 2 : Exécution automatique

**Que se passe-t-il ?**

1. **Création tab Chrome** - Nouveau tab dans le groupe MCP
2. **Navigation** - Ouvre l'URL de départ
3. **GIF recording start** - Commence l'enregistrement
4. **Actions automatiques** - Exécute chaque étape du scénario
5. **Screenshots** - Capture d'écran à chaque étape clé
6. **Assertions** - Vérifie les conditions attendues
7. **GIF recording stop** - Arrête l'enregistrement
8. **Export GIF** - Télécharge le GIF de la session

**Output attendu :**
```
🔍 Test UI E2E - Parcours d'achat

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Étape 1/7 : Ouvrir page shop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Navigation vers https://example.com/shop
✅ Page chargée (2.3s)
📸 Screenshot : step-1-shop-page.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Étape 2/7 : Rechercher "laptop"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Champ de recherche trouvé (ref_3)
✅ Texte saisi : "laptop"
✅ Formulaire soumis
✅ Résultats affichés : 12 produits
📸 Screenshot : step-2-search-results.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Étape 3/7 : Cliquer premier produit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Premier produit trouvé : "Dell XPS 13"
✅ Click effectué
✅ Page produit chargée
📸 Screenshot : step-3-product-page.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Étape 4/7 : Ajouter au panier
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Bouton "Add to cart" trouvé
✅ Click effectué
✅ Notification affichée : "Product added"
📸 Screenshot : step-4-cart-notification.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Étape 5/7 : Aller au panier
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Icône panier cliquée
✅ Page panier chargée
📸 Screenshot : step-5-cart-page.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Étape 6/7 : Vérifier produit dans panier
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Produit trouvé : "Dell XPS 13"
✅ Quantité : 1
✅ Prix : 999.00€
📸 Screenshot : step-6-cart-item.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Étape 7/7 : Vérifier total
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Total trouvé : 999.00€
✅ Assertion OK : total = prix produit
📸 Screenshot : step-7-cart-total.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RÉSULTAT TEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Statut : ✅ PASSED
Durée : 12.8s
Étapes : 7/7 réussies
Screenshots : 7
GIF : test-parcours-achat-2026-02-01.gif

Fichiers générés :
- test-parcours-achat-2026-02-01.gif (2.3 MB)
- step-1-shop-page.png
- step-2-search-results.png
- step-3-product-page.png
- step-4-cart-notification.png
- step-5-cart-page.png
- step-6-cart-item.png
- step-7-cart-total.png
- test-report-2026-02-01.html
```

## Exemple Complet

### Scénario : Tester formulaire de contact

**Description :**
```
Tester le formulaire de contact :
1. Ouvrir https://example.com/contact
2. Remplir champ "Name" avec "John Doe"
3. Remplir champ "Email" avec "john@example.com"
4. Remplir champ "Message" avec "Test message"
5. Cliquer sur "Send"
6. Vérifier message de succès
```

**Commande :**
```bash
/chrome-ui-test:ui-test
```

**Workflow complet :**

**Étape 1 - Navigation :**
```javascript
// Claude exécute automatiquement
navigate('https://example.com/contact')
wait(2000) // Attend chargement
screenshot('step-1-contact-form.png')
```

**Étape 2 - Remplir champ Name :**
```javascript
find('Name input field')
// → ref_1 trouvé
form_input(ref: 'ref_1', value: 'John Doe')
screenshot('step-2-name-filled.png')
```

**Étape 3 - Remplir champ Email :**
```javascript
find('Email input field')
// → ref_2 trouvé
form_input(ref: 'ref_2', value: 'john@example.com')
screenshot('step-3-email-filled.png')
```

**Étape 4 - Remplir champ Message :**
```javascript
find('Message textarea')
// → ref_3 trouvé
form_input(ref: 'ref_3', value: 'Test message')
screenshot('step-4-message-filled.png')
```

**Étape 5 - Submit :**
```javascript
find('Send button')
// → ref_4 trouvé
left_click(ref: 'ref_4')
wait(1000) // Attend soumission
screenshot('step-5-form-submitted.png')
```

**Étape 6 - Vérifier succès :**
```javascript
find('success message')
// → ref_5 trouvé : "Message sent successfully!"
assert(ref_5.text.includes('successfully'))
screenshot('step-6-success-message.png')
```

**Résultat :**
```
✅ TEST PASSED

Durée : 8.2s
Étapes : 6/6
GIF : test-formulaire-contact.gif
```

## Variantes

### Test avec données multiples

Tester le formulaire avec plusieurs jeux de données :

```bash
/chrome-ui-test:ui-test --data-driven
```

```javascript
const testData = [
  { name: 'John Doe', email: 'john@example.com', message: 'Test 1' },
  { name: 'Jane Smith', email: 'jane@example.com', message: 'Test 2' },
  { name: 'Bob Johnson', email: 'bob@example.com', message: 'Test 3' }
]

testData.forEach((data, index) => {
  // Exécute le scénario avec chaque jeu de données
  // Génère un GIF par test
})
```

### Test avec assertions avancées

```bash
/chrome-ui-test:ui-test --advanced-assertions
```

Assertions disponibles :
- Texte contient
- Élément visible/caché
- Attribut a valeur
- Style CSS
- Nombre d'éléments
- URL contient
- Cookies/LocalStorage

### Mode debug

```bash
/chrome-ui-test:ui-test --debug
```

En mode debug :
- Pause à chaque étape
- Console logs affichés
- Screenshots automatiques
- Possibilité d'inspecter DOM

## Troubleshooting

### Élément non trouvé

**Symptôme :** `Element not found: "Add to cart button"`

**Solution :**
1. Prendre un screenshot : `/chrome-ui-test:screenshot`
2. Vérifier que l'élément existe
3. Ajuster la description de recherche
4. Augmenter le wait time si chargement lent

**Debugging :**
```javascript
// Au lieu de
find('Add to cart button')

// Essayer
find('button with text cart')
// ou
find('button with class add-to-cart')
```

### Timeout sur action

**Symptôme :** `Timeout after 30s waiting for element`

**Solution :**
1. Vérifier que la page charge correctement
2. Augmenter timeout global
3. Ajouter wait explicite avant l'action

```javascript
wait(5000) // Attendre 5s
find('slow loading element')
```

### GIF trop gros

**Symptôme :** `GIF size: 15 MB - too large`

**Solution :**
1. Réduire qualité : `--gif-quality=20` (défaut: 10)
2. Réduire frame rate : `--gif-fps=5` (défaut: 10)
3. Limiter durée du test

### Tests flaky (intermittents)

**Symptôme :** Test passe parfois, échoue parfois

**Solution :**

**Causes communes :**
- Timing issues (wait insuffisant)
- Animations CSS
- Requêtes API lentes
- Cache browser

**Fixes :**
```javascript
// Attendre que l'élément soit vraiment cliquable
wait_for_element_stable(ref: 'ref_1', timeout: 5000)

// Désactiver animations
javascript_tool(`
  document.querySelectorAll('*').forEach(el => {
    el.style.transition = 'none';
    el.style.animation = 'none';
  });
`)

// Attendre requêtes réseau
wait_for_network_idle(timeout: 3000)
```

### Page ne charge pas

**Symptôme :** `Page load timeout`

**Solution :**
1. Vérifier URL accessible
2. Vérifier connexion internet
3. Vérifier que le site n'est pas down
4. Essayer en mode headless: `--headless=false`

## Liens Connexes

**Use cases :**
- [Test responsive](/usecases/testing/responsive-testing)
- [Workflow feature complet](/usecases/development/full-feature-workflow)

**Plugins :**
- [Chrome UI Test](/plugins/chrome-ui-test)

**Documentation externe :**
- [Claude in Chrome Extension](https://chrome.google.com/webstore)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

## Tips & Best Practices

### ✅ Bonnes pratiques

- **Tests atomiques** : un scénario = un parcours métier complet
- **Idempotence** : tests doivent pouvoir se rejouer sans setup manuel
- **Wait smart** : utiliser `wait_for_element` plutôt que `wait(5000)`
- **Nommer clairement** : screenshots et GIFs avec noms descriptifs
- **Assertions explicites** : vérifier résultats attendus, pas juste "ça passe"

### 🔍 Optimisations

**Structure de test recommandée :**
```javascript
// Setup
navigate(url)
wait_for_page_load()

// Given (contexte)
login('user@example.com', 'password')

// When (action)
click_add_to_cart()

// Then (vérification)
assert_product_in_cart()
assert_cart_total_correct()

// Cleanup (optionnel)
logout()
```

**Réutiliser des helpers :**
```javascript
// Définir helpers réutilisables
function login(email, password) {
  find('email field')
  form_input(ref: 'ref_1', value: email)
  find('password field')
  form_input(ref: 'ref_2', value: password)
  find('login button')
  left_click(ref: 'ref_3')
  wait_for_element('dashboard')
}

// Utiliser dans tests
test('add product to cart', () => {
  login('user@example.com', 'password')
  // ... reste du test
})
```

**CI/CD Integration :**
```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Start app
        run: npm start &

      - name: Wait for app
        run: npx wait-on http://localhost:3000

      - name: Run E2E tests
        run: /chrome-ui-test:ui-test --headless

      - name: Upload GIFs
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: test-gifs
          path: '*.gif'
```

### 🎯 Métriques de qualité

Un bon test E2E c'est :
- ✅ Durée < 30s par scénario
- ✅ Pas de `wait(5000)` hardcodés
- ✅ Assertions explicites à chaque étape critique
- ✅ GIF généré pour documentation
- ✅ 0% flaky (toujours même résultat)

### 📊 Scénarios critiques à tester

**E-commerce :**
- Parcours d'achat complet
- Ajout/suppression panier
- Checkout et paiement
- Création compte

**SaaS :**
- Login/logout
- Onboarding
- Features principales
- Settings/profil

**Formulaires :**
- Validation champs
- Messages d'erreur
- Soumission réussie
- Upload fichiers

## Checklist Validation

Avant de lancer le test :

- [ ] URL accessible
- [ ] Chrome ouvert avec extension Claude
- [ ] Scénario défini clairement
- [ ] Assertions identifiées

Pendant le test :

- [ ] Chaque étape passe
- [ ] Screenshots capturés
- [ ] GIF enregistré
- [ ] Pas d'erreurs console critiques

Après le test :

- [ ] Résultat PASSED
- [ ] GIF généré et exploitable
- [ ] Screenshots utiles pour debug
- [ ] Rapport HTML généré
- [ ] Test reproductible (relance OK)
