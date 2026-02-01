---
title: Test responsive multi-device
description: Tester l'affichage sur 3 viewports (mobile, tablet, desktop) avec screenshots comparatifs
category: testing
plugins:
  - name: chrome-ui-test
    skills: [/chrome-ui-test:ui-test]
complexity: 2
duration: 8
keywords: [responsive, viewport, mobile, tablet, desktop, screenshots]
related:
  - /usecases/testing/e2e-ui-testing
---

# Test responsive multi-device <Badge type="info" text="★★ Intermédiaire" /> <Badge type="tip" text="~8 min" />

## Contexte

Vérifier que votre application s'affiche correctement sur mobile, tablette et desktop manuellement est fastidieux. Automatiser ces tests visuels permet de détecter rapidement les problèmes de responsive.

## Objectif

Tester l'affichage responsive avec :

- ✅ 3 viewports (mobile 375px, tablet 768px, desktop 1920px)
- ✅ Screenshots de chaque page critique
- ✅ Comparaison visuelle
- ✅ Détection d'overflow/scroll horizontal
- ✅ Rapport HTML avec grille d'images

## Prérequis

**Plugins :**
- [chrome-ui-test](/plugins/chrome-ui-test) - Chrome automation

**Outils :**
- Google Chrome
- Extension Claude in Chrome
- Application web responsive

**Configuration :**
Aucune configuration particulière nécessaire.

## Workflow Étape par Étape

### Phase 1 : Définir les pages à tester

**Commande :**
```bash
/chrome-ui-test:ui-test --responsive
```

**Pages à tester (exemple) :**
```
1. Homepage : /
2. Product list : /products
3. Product detail : /products/1
4. Cart : /cart
5. Contact : /contact
```

### Phase 2 : Test automatique multi-viewport

**Que se passe-t-il ?**

Pour chaque page, Claude :

1. **Mobile (375x667) :**
   - Resize window à 375x667px
   - Navigate vers la page
   - Wait for load
   - Screenshot complet (avec scroll)
   - Check horizontal overflow
   - Check éléments tronqués

2. **Tablet (768x1024) :**
   - Resize window à 768x1024px
   - Navigate vers la page
   - Screenshot complet
   - Vérifier layout tablet

3. **Desktop (1920x1080) :**
   - Resize window à 1920x1080px
   - Navigate vers la page
   - Screenshot complet
   - Vérifier layout desktop

**Output attendu :**
```
📱 Test Responsive Multi-Device

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Page 1/5 : Homepage (/)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Mobile (375x667)
  ✅ Resize window
  ✅ Navigate to /
  ✅ Screenshot : homepage-mobile.png
  ✅ No horizontal overflow
  ✅ Menu burger visible
  ✅ Content readable

📱 Tablet (768x1024)
  ✅ Resize window
  ✅ Navigate to /
  ✅ Screenshot : homepage-tablet.png
  ✅ Layout adapté
  ✅ Images responsive

🖥️  Desktop (1920x1080)
  ✅ Resize window
  ✅ Navigate to /
  ✅ Screenshot : homepage-desktop.png
  ✅ Full navigation visible
  ✅ Content centered

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Page 2/5 : Product list (/products)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Mobile (375x667)
  ✅ Screenshot : products-mobile.png
  ✅ Grid : 1 column
  ✅ Cards stacked

📱 Tablet (768x1024)
  ✅ Screenshot : products-tablet.png
  ✅ Grid : 2 columns
  ⚠️  Warning: Small images

🖥️  Desktop (1920x1080)
  ✅ Screenshot : products-desktop.png
  ✅ Grid : 4 columns
  ✅ Layout optimal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Page 3/5 : Product detail (/products/1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Mobile (375x667)
  ✅ Screenshot : product-detail-mobile.png
  ❌ Error: Horizontal scroll detected (420px width)
  ❌ Image overflow container

📱 Tablet (768x1024)
  ✅ Screenshot : product-detail-tablet.png
  ✅ Layout OK

🖥️  Desktop (1920x1080)
  ✅ Screenshot : product-detail-desktop.png
  ✅ Layout OK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RÉSULTAT TEST RESPONSIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pages testées : 5
Viewports : 3 (mobile, tablet, desktop)
Screenshots : 15

Statut : ⚠️  ISSUES FOUND

Problèmes détectés :
❌ Product detail - Mobile : Horizontal overflow (420px)
⚠️  Products list - Tablet : Images too small

Fichiers générés :
- responsive-report-2026-02-01.html (grille comparative)
- screenshots/ (15 images)

Ouvrir rapport : file:///path/to/responsive-report-2026-02-01.html
```

### Phase 3 : Rapport HTML visuel

Le rapport HTML généré contient une grille comparative :

```html
<!DOCTYPE html>
<html>
<head>
  <title>Responsive Test Report</title>
  <style>
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .card { border: 1px solid #ddd; padding: 10px; }
    .card img { width: 100%; }
    .error { border-color: red; }
    .warning { border-color: orange; }
    .success { border-color: green; }
  </style>
</head>
<body>
  <h1>Responsive Test Report</h1>

  <h2>Homepage (/)</h2>
  <div class="grid">
    <div class="card success">
      <h3>📱 Mobile (375x667)</h3>
      <img src="homepage-mobile.png" />
      <p>✅ All checks passed</p>
    </div>
    <div class="card success">
      <h3>📱 Tablet (768x1024)</h3>
      <img src="homepage-tablet.png" />
      <p>✅ All checks passed</p>
    </div>
    <div class="card success">
      <h3>🖥️ Desktop (1920x1080)</h3>
      <img src="homepage-desktop.png" />
      <p>✅ All checks passed</p>
    </div>
  </div>

  <h2>Product detail (/products/1)</h2>
  <div class="grid">
    <div class="card error">
      <h3>📱 Mobile (375x667)</h3>
      <img src="product-detail-mobile.png" />
      <p>❌ Horizontal overflow: 420px</p>
      <p>❌ Image overflow container</p>
    </div>
    <!-- ... -->
  </div>
</body>
</html>
```

## Exemple Complet

### Scénario : E-commerce responsive

**Pages critiques :**
1. Homepage
2. Category page
3. Product detail
4. Cart
5. Checkout

**Commande :**
```bash
/chrome-ui-test:ui-test --responsive --pages="/,/category/laptops,/product/123,/cart,/checkout"
```

**Problèmes détectés :**

**Mobile :**
- ❌ Product detail : image déborde (600px dans container 375px)
- ❌ Checkout : formulaire tronqué
- ⚠️  Cart : boutons trop petits (< 44px touch target)

**Tablet :**
- ⚠️  Homepage : hero image pixelisée
- ✅ Autres pages OK

**Desktop :**
- ✅ Toutes pages OK

**Corrections appliquées :**

**1. Image responsive (product detail) :**
```css
/* Avant */
.product-image {
  width: 600px;
}

/* Après */
.product-image {
  width: 100%;
  max-width: 600px;
  height: auto;
}
```

**2. Formulaire checkout (mobile) :**
```css
/* Avant */
.checkout-form {
  width: 500px;
}

/* Après */
.checkout-form {
  width: 100%;
  max-width: 500px;
  padding: 0 15px;
}

@media (max-width: 767px) {
  .checkout-form input {
    font-size: 16px; /* Évite zoom iOS */
  }
}
```

**3. Touch targets (cart) :**
```css
/* Avant */
.cart-button {
  padding: 5px 10px;
}

/* Après */
@media (max-width: 767px) {
  .cart-button {
    padding: 12px 20px; /* Min 44x44px */
    min-height: 44px;
  }
}
```

**Résultat après corrections :**
```
📱 Test Responsive - Après corrections

Pages testées : 5
Issues : 0 ❌ → ✅
Warnings : 2 ⚠️ → 0 ✅

✅ PASSED - Application fully responsive
```

## Variantes

### Viewports personnalisés

```bash
/chrome-ui-test:ui-test --viewports="320x568,375x667,414x896,768x1024,1366x768,1920x1080"
```

**Viewports courants :**
- iPhone SE : 320x568
- iPhone 12 : 390x844
- iPhone 12 Pro Max : 428x926
- iPad : 768x1024
- iPad Pro : 1024x1366
- Desktop HD : 1920x1080
- Desktop 4K : 3840x2160

### Test landscape/portrait

```bash
/chrome-ui-test:ui-test --orientations
```

Teste chaque viewport en portrait ET landscape.

### Comparaison visuelle

```bash
/chrome-ui-test:ui-test --visual-diff
```

Compare screenshots avec baseline et détecte différences visuelles.

## Troubleshooting

### Horizontal scroll détecté

**Symptôme :** `Horizontal overflow: 420px in 375px viewport`

**Debug :**
```javascript
// Trouver l'élément qui déborde
javascript_tool(`
  const elements = document.querySelectorAll('*');
  elements.forEach(el => {
    if (el.scrollWidth > window.innerWidth) {
      console.log('Overflow:', el, 'Width:', el.scrollWidth);
      el.style.outline = '2px solid red';
    }
  });
`)
```

**Solutions courantes :**
```css
/* Fix global */
* {
  box-sizing: border-box;
}

body {
  overflow-x: hidden; /* Dernier recours */
}

/* Fix images */
img {
  max-width: 100%;
  height: auto;
}

/* Fix containers */
.container {
  width: 100%;
  max-width: 1200px;
  padding: 0 15px;
}
```

### Screenshots incomplets

**Symptôme :** Screenshot ne capture que le viewport, pas la page complète

**Solution :**
```bash
/chrome-ui-test:ui-test --full-page-screenshots
```

### Éléments cachés en mobile

**Symptôme :** Navigation desktop visible en mobile

**Solution :**
```css
/* Desktop menu */
@media (min-width: 768px) {
  .mobile-menu { display: none; }
  .desktop-menu { display: block; }
}

/* Mobile menu */
@media (max-width: 767px) {
  .desktop-menu { display: none; }
  .mobile-menu { display: block; }
}
```

### Images pixelisées

**Symptôme :** Images floues sur tablet/desktop

**Solution :**
```html
<!-- Avant -->
<img src="image-small.jpg" />

<!-- Après : srcset responsive -->
<img
  src="image-medium.jpg"
  srcset="
    image-small.jpg 400w,
    image-medium.jpg 800w,
    image-large.jpg 1600w
  "
  sizes="
    (max-width: 767px) 100vw,
    (max-width: 1023px) 50vw,
    33vw
  "
  alt="Product"
/>
```

## Liens Connexes

**Use cases :**
- [Test UI E2E](/usecases/testing/e2e-ui-testing)

**Plugins :**
- [Chrome UI Test](/plugins/chrome-ui-test)

**Documentation externe :**
- [MDN - Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Google - Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)

## Tips & Best Practices

### ✅ Bonnes pratiques

**Mobile-first :**
```css
/* Base styles (mobile) */
.card {
  width: 100%;
  padding: 15px;
}

/* Tablet */
@media (min-width: 768px) {
  .card {
    width: 50%;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .card {
    width: 33.333%;
  }
}
```

**Touch targets :**
- Minimum 44x44px (iOS/Android guidelines)
- Espacement 8px entre éléments cliquables
- Éviter hover-only interactions

**Performance :**
```html
<!-- Lazy load images hors viewport -->
<img loading="lazy" src="image.jpg" />

<!-- Preload critical images -->
<link rel="preload" as="image" href="hero.jpg" />
```

### 🔍 Breakpoints recommandés

**Framework-agnostic :**
```css
/* Mobile small */
@media (min-width: 320px) { }

/* Mobile large */
@media (min-width: 375px) { }

/* Tablet portrait */
@media (min-width: 768px) { }

/* Tablet landscape / Desktop small */
@media (min-width: 1024px) { }

/* Desktop medium */
@media (min-width: 1280px) { }

/* Desktop large */
@media (min-width: 1920px) { }
```

**Tailwind CSS :**
- sm: 640px
- md: 768px
- lg: 1024px
- xl: 1280px
- 2xl: 1536px

**Bootstrap :**
- xs: < 576px
- sm: ≥ 576px
- md: ≥ 768px
- lg: ≥ 992px
- xl: ≥ 1200px
- xxl: ≥ 1400px

### 🎯 Checklist responsive

**Layout :**
- [ ] Pas de scroll horizontal
- [ ] Contenu lisible sans zoom
- [ ] Navigation accessible
- [ ] Formulaires utilisables

**Images :**
- [ ] Responsive (max-width: 100%)
- [ ] srcset pour HD displays
- [ ] Lazy loading
- [ ] Alt text présent

**Performance :**
- [ ] Fonts web optimisées
- [ ] CSS minifié
- [ ] Images compressées
- [ ] Critical CSS inline

**Accessibilité :**
- [ ] Touch targets ≥ 44px
- [ ] Contraste suffisant
- [ ] Texte redimensionnable
- [ ] Navigation clavier

## Checklist Validation

Avant le test :

- [ ] Pages critiques identifiées
- [ ] Viewports définis
- [ ] Application accessible

Pendant le test :

- [ ] Screenshots capturés pour chaque viewport
- [ ] Overflow détecté
- [ ] Layout vérifié
- [ ] Touch targets validés

Après le test :

- [ ] Rapport HTML généré
- [ ] Problèmes documentés
- [ ] Corrections appliquées
- [ ] Re-test après fixes
- [ ] 0 erreur responsive
