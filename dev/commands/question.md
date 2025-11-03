---
model: claude-sonnet-4-5-20250929
allowed-tools: Bash(git ls-files:*), Read
description: Répondre aux questions sur la structure du projet et la documentation sans coder
---

# Question

Répondre à la question de l'utilisateur en analysant la structure du projet et la documentation. Cette invite est conçue pour fournir des informations et répondre aux questions sans apporter de modifications au code.

## Variables

$ARGUMENTS

## Instructions

- **IMPORTANT : Il s'agit uniquement d'une tâche de réponse à des questions - NE PAS écrire, éditer ou créer de fichiers**
- **IMPORTANT : Se concentrer sur la compréhension et l'explication du code existant et de la structure du projet**
- **IMPORTANT : Fournir des réponses claires et informatives basées sur l'analyse du projet**
- **IMPORTANT : Si la question nécessite des modifications de code, expliquer ce qui devrait être fait conceptuellement sans implémenter**

## Workflow

- Examiner la structure du projet depuis !`git ls-files`
- Comprendre l'objectif du projet depuis le @docs/README.md
- Connecter la question aux parties pertinentes du projet
- Fournir des réponses complètes basées sur l'analyse

## Format de réponse

- Réponse directe à la question
- Preuves à l'appui de la structure du projet
- Références à la documentation pertinente
- Explications conceptuelles le cas échéant
