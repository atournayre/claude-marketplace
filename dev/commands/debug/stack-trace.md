---
model: claude-sonnet-4-5-20250929
allowed-tools: Read,Write,Grep
description: Prend en paramètre une trace d'erreur. Génère un fichier lisible avec la trace formatée. Fourni une première analyse de l'erreur. Propose 2 ou 3 solutions de résolution.
argument-hint: <stack-trace-text-or-file-path>
---

# Stack Trace Analyzer

## Purpose
Analyser une trace d'erreur (stack trace) pour :
- Formater la trace de manière lisible
- Identifier la cause racine de l'erreur
- Proposer des solutions de résolution concrètes

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

## Variables
- STACK_TRACE: Trace d'erreur fournie (texte brut ou chemin de fichier)
- ERROR_TYPE: Type d'erreur détecté (PHP, JavaScript, Python, etc.)
- ROOT_CAUSE: Cause racine identifiée
- TIMESTAMP: Horodatage pour le fichier de rapport

## Instructions
Tu es un expert en debugging et analyse de stack traces. Ton rôle :
- Accepter une trace d'erreur sous forme de texte ou fichier
- Parser et formater la trace pour la rendre lisible
- Identifier le point d'origine exact de l'erreur
- Analyser le contexte et les causes probables
- Proposer 2-3 solutions concrètes et priorisées

## Relevant Files
- Fichier source où l'erreur est survenue (identifié dans la trace)
- Fichiers de configuration pertinents
- Logs d'application associés

## Workflow

### Étape 0: Initialisation du Timing (OBLIGATOIRE - PREMIÈRE ACTION)
```
🕐 Démarrage: [timestamp Europe/Paris avec CEST/CET]
```
- Cette étape DOIT être la toute première action
- Enregistrer le timestamp pour calcul ultérieur

### 1. Lecture de la stack trace
- Si argument est un chemin de fichier : lire avec Read
- Si argument est du texte : traiter directement
- Détecter le type/langage de la trace (PHP, JS, Python, etc.)

### 2. Parsing et formatage
- Extraire les éléments clés :
  - Type d'exception/erreur
  - Message d'erreur principal
  - Fichier et ligne d'origine
  - Call stack complet
  - Variables/contexte si disponible
- Formater de manière hiérarchique et lisible

### 3. Analyse approfondie
- Identifier le point d'origine exact (fichier:ligne)
- Lire le code source à la ligne incriminée
- Analyser le contexte (méthodes appelantes, état)
- Rechercher des patterns d'erreur connus
- Vérifier les changements récents (git blame si pertinent)

### 4. Diagnostic
- Déterminer la cause racine (pas juste le symptôme)
- Identifier les facteurs contributifs
- Évaluer la criticité et l'impact

### 5. Génération du rapport
- Créer fichier dans `/tmp/stack-trace-analysis-[timestamp].md`
- Structure du rapport :
  - Résumé exécutif
  - Stack trace formatée
  - Analyse détaillée
  - 2-3 solutions priorisées
  - Prochaines étapes recommandées

### 6. Présentation des solutions
- Solution 1 (Quick Fix) : rapide, traite le symptôme
- Solution 2 (Recommended) : équilibrée, traite la cause
- Solution 3 (Long-term) : robuste, prévient les récurrences

## Examples

### Exemple 1 : Trace PHP
```bash
/stack-trace "Fatal error: Uncaught Error: Call to undefined method User::getName() in /app/src/Service.php:42"
```

### Exemple 2 : Fichier de log
```bash
/stack-trace /var/log/app-error.log
```

### Exemple 3 : Trace JavaScript
```bash
/stack-trace "TypeError: Cannot read property 'id' of undefined at Object.process (main.js:156:23)"
```

## Report Structure
```markdown
# Stack Trace Analysis - [TIMESTAMP]

## Résumé Exécutif
- Type d'erreur : [ERROR_TYPE]
- Localisation : [FILE:LINE]
- Cause racine : [ROOT_CAUSE]
- Sévérité : [CRITICAL/HIGH/MEDIUM/LOW]

## Stack Trace Formatée
[Trace complète avec highlighting et indentation]

## Analyse Détaillée
### Point d'origine
- Fichier : [FILE]
- Ligne : [LINE]
- Méthode/Fonction : [METHOD]
- Code :
  ```[lang]
  [code context]
  ```

### Contexte
- Call stack simplifié
- État probable au moment de l'erreur
- Dépendances impliquées

### Cause Racine
[Explication détaillée de ce qui a causé l'erreur]

## Solutions Proposées

### Solution 1 : Quick Fix ⚡
**Description :** [Solution rapide]
**Implémentation :**
- [Étape 1]
- [Étape 2]
**Avantages :** Rapide, minimal
**Inconvénients :** Traite le symptôme

### Solution 2 : Recommandée ✅
**Description :** [Solution équilibrée]
**Implémentation :**
- [Étape 1]
- [Étape 2]
- [Étape 3]
**Avantages :** Traite la cause, maintenable
**Inconvénients :** Effort modéré

### Solution 3 : Long-terme 🎯
**Description :** [Solution robuste]
**Implémentation :**
- [Étape 1]
- [Étape 2]
- [Étape 3]
**Avantages :** Prévient récurrences, robuste
**Inconvénients :** Plus d'effort initial

## Prochaines Étapes
1. [Action immédiate]
2. [Action de suivi]
3. [Action de prévention]

## Ressources
- Fichiers modifiés potentiels : [LIST]
- Documentation pertinente : [LINKS]
- Issues similaires : [REFERENCES]

---
✅ Terminé : [timestamp Europe/Paris avec CEST/CET]

⏱️ Durée : [durée formatée]
```

## Best Practices
- Parser intelligemment selon le langage/framework
- Privilégier la lecture du code source pour contexte
- Chercher les patterns d'erreur récurrents
- Proposer des solutions testables
- Inclure des exemples de code dans les solutions
- Garder le rapport concis mais complet
