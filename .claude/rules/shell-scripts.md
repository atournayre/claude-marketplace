---
path: "**/scripts/**/*.sh"
---

# Conventions des scripts shell

Tout script shell dans `scripts/` DOIT respecter ces regles :

1. **`set -euo pipefail`** en premiere ligne apres le shebang
2. **Pas d'`eval`** — utiliser des tableaux bash et expansion directe
3. **Pas de `2>/dev/null` sans gestion d'erreur** — toujours verifier le resultat ou utiliser `|| echo ""` avec un guard clause
4. **Fichiers temporaires** : `mktemp` + `trap 'rm -f "$TMPFILE"' EXIT`
5. **Verifier les outils requis** au debut :
   ```bash
   command -v jq >/dev/null 2>&1 || { echo "jq requis" >&2; exit 1; }
   ```
6. **Guard clauses pour inputs vides** — ne jamais produire de sortie trompeuse sur input vide/invalide
7. **Pas de fichiers temporaires a chemin previsible** — toujours `mktemp` avec pattern `XXXXXX`
