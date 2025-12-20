---
description: Analyses le détail des modifications git. Fournis 2 rapports d'impact - un rapport métier et un rapport technique. Ajoutes ce rapport à la description de la PR.
argument-hint: <pr-number>
output-style: bullet-points
---

# Configuration de sortie

**IMPORTANT** : Cette commande génère une analyse d'impact structurée et nécessite un format de sortie spécifique.

Lis le frontmatter de cette commande. Si un champ `output-style` est présent, exécute immédiatement :
```
/output-style <valeur-du-champ>
```

*Note : Une fois que le champ `output-style` sera supporté nativement par Claude Code, cette instruction pourra être supprimée.*

# Analyse d'impact GitHub

You must use the Skill tool to invoke the "github-impact" skill with the following arguments.
