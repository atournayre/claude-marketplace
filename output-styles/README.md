# Plugin Output Styles

Styles de sortie personnalisés pour formater les réponses de Claude.

## Installation

```bash
/plugin install output-styles@atournayre
```

## Styles Disponibles

### `/output-styles:style-ultra-concise`

Mode ultra-concis : minimum de mots, actions directes uniquement.

**Caractéristiques :**
- Pas de salutations ni formules de politesse
- Code/commandes en premier
- Skip étapes évidentes
- Fragments plutôt que phrases complètes
- Résumés en une ligne
- Expertise technique assumée
- Pas d'explications sauf si critique
- Focus : BUILD et SHIP

**Utilisation :**
```bash
/output-styles:style-ultra-concise
```

**Exemple de sortie :**
```
git status
3 files modified

Edit User.php:42
- Add getName() method
- Return string

Tests pass
✓
```

---

### `/output-styles:style-bullet-points`

Listes à puces hiérarchiques pour scan rapide.

**Caractéristiques :**
- Structure hiérarchique claire
- Points principaux en niveau 1
- Détails en sous-niveaux
- Facile à scanner
- Organisation logique

**Exemple de sortie :**
```
Action effectuée :
- Modification de User.php
  - Ajout méthode getName()
  - Return type : string
  - Tests unitaires créés
- Mise à jour documentation
  - README.md
  - docs/api/user.md
```

---

### `/output-styles:style-markdown-focused`

Markdown enrichi pour maximum de lisibilité.

**Caractéristiques :**
- Headers clairs (##, ###)
- Blocs de code avec syntax highlight
- Sections info/warning
- Listes numérotées/à puces
- Liens et références
- Tableaux si pertinent

**Exemple de sortie :**
```markdown
## Modification : User.php

### Changements Apportés

Ajout de la méthode `getName()` :

```php
public function getName(): string
{
    return $this->name;
}
```

### Tests

✅ 3 tests unitaires passent
- UserTest::testGetName()
- UserTest::testGetNameNotEmpty()
- UserTest::testGetNameReturnsString()

> ℹ️ Documentation mise à jour dans docs/api/user.md
```

---

### `/output-styles:style-table-based`

Tableaux markdown pour meilleure organisation.

**Caractéristiques :**
- Données tabulaires
- Comparaisons
- Listes d'items avec propriétés
- Facile à scanner

**Exemple de sortie :**
```markdown
| Fichier | Changement | Status |
|---------|-----------|--------|
| User.php | + getName() | ✅ |
| UserTest.php | + 3 tests | ✅ |
| README.md | Updated | ✅ |

| Test | Résultat | Durée |
|------|----------|-------|
| UserTest::testGetName | ✅ Pass | 0.02s |
| UserTest::testGetNameNotEmpty | ✅ Pass | 0.01s |
```

---

### `/output-styles:style-yaml-structured`

YAML structuré avec paires clé-valeur hiérarchiques.

**Caractéristiques :**
- Structure claire
- Facile à parser
- Hiérarchie visible
- Format machine-readable

**Exemple de sortie :**
```yaml
action: "Modification User.php"
changes:
  - file: "src/Entity/User.php"
    type: "method_added"
    details:
      name: "getName"
      return_type: "string"
      visibility: "public"
tests:
  total: 3
  passed: 3
  failed: 0
  files:
    - "tests/Entity/UserTest.php"
documentation:
  updated:
    - "README.md"
    - "docs/api/user.md"
```

---

### `/output-styles:style-html-structured`

HTML sémantique avec structure propre.

**Caractéristiques :**
- Tags sémantiques (<article>, <section>)
- Classes CSS
- Accessible
- Bien formé

**Exemple de sortie :**
```html
<article class="code-change">
  <header>
    <h2>Modification : User.php</h2>
  </header>

  <section class="changes">
    <h3>Changements</h3>
    <ul>
      <li>Ajout méthode <code>getName()</code></li>
      <li>Return type : <code>string</code></li>
    </ul>
  </section>

  <section class="tests">
    <h3>Tests</h3>
    <p class="status success">✅ 3 tests passent</p>
  </section>
</article>
```

---

### `/output-styles:style-genui`

UI générative avec HTML et styling moderne.

**Caractéristiques :**
- Composants UI riches
- Styling CSS inline
- Interactif visuellement
- Modern design
- Cards, badges, buttons

**Exemple de sortie :**
```html
<div style="font-family: system-ui; padding: 20px;">
  <div style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
    <h2 style="margin: 0 0 12px 0; color: #212529;">✅ Modification Complétée</h2>

    <div style="background: white; border-left: 4px solid #28a745; padding: 12px; margin: 8px 0;">
      <strong>User.php</strong>
      <p style="margin: 4px 0 0 0;">Méthode getName() ajoutée</p>
    </div>

    <div style="display: flex; gap: 8px; margin-top: 12px;">
      <span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
        3 tests ✓
      </span>
      <span style="background: #17a2b8; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
        Docs updated
      </span>
    </div>
  </div>
</div>
```

## Utilisation

### Activer un Style

Chaque style s'active via sa commande :

```bash
/output-styles:style-ultra-concise
/output-styles:style-bullet-points
/output-styles:style-markdown-focused
/output-styles:style-table-based
/output-styles:style-yaml-structured
/output-styles:style-html-structured
/output-styles:style-genui
```

### Persister le Style

Le style activé reste actif pour toute la session.

Pour changer de style :
```bash
# Passer en mode ultra-concise
/output-styles:style-ultra-concise

# Revenir au markdown enrichi
/output-styles:style-markdown-focused
```

### Configuration Projet

`.claude/settings.json` :
```json
{
  "output_style": "ultra-concise"
}
```

## Cas d'Usage

**Ultra Concise :**
- Développement rapide
- Expertise technique élevée
- Pas de temps à perdre

**Bullet Points :**
- Rapports
- Résumés
- Listes de tâches

**Markdown Focused :**
- Documentation
- Tutoriels
- Explications détaillées

**Table Based :**
- Comparaisons
- Résultats de tests
- Listes de fichiers

**YAML Structured :**
- Configurations
- Rapports machine-readable
- CI/CD outputs

**HTML Structured :**
- Documentation web
- Rapports formatés
- Export HTML

**GenUI :**
- Dashboards
- Rapports visuels
- Présentations

## Hooks

Le plugin utilise des hooks pour appliquer automatiquement le style :
- `user_prompt_submit.py` - Applique le style avant traitement
- Persiste dans la session

## Best Practices

- Ultra-concise pour workflow rapide
- Markdown pour documentation
- YAML pour CI/CD
- GenUI pour rapports visuels
- Changer selon contexte

## Licence

MIT
