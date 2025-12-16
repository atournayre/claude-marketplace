---
description: Analyse une codebase ou documentation avec Gemini (1M tokens)
argument-hint: <path> <question>
---

Délègue l'analyse de contextes ultra-longs à Gemini 2.5 Pro.

## Arguments

- `<path>` : Chemin du répertoire ou fichier à analyser
- `<question>` : Question ou instruction pour l'analyse

## Exemples

```
/gemini:analyze src/ "Identifie tous les problèmes de sécurité potentiels"
/gemini:analyze docs/ "Résume l'architecture du projet"
/gemini:analyze tests/ "Quels cas de test manquent?"
```

## Exécution

Tu dois utiliser l'agent `gemini-analyzer` avec les arguments fournis.

L'agent va :
1. Valider le chemin et la question
2. Préparer le contexte (concaténation fichiers, exclusion sensibles)
3. Vérifier la taille (< 4MB)
4. Appeler Gemini 2.5 Pro
5. Retourner la réponse

Après l'analyse Gemini, synthétise la réponse pour l'utilisateur et propose des actions concrètes si pertinent.
