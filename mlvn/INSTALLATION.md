# Installation du Plugin MLVN

## ✅ Dépendances installées

### 1. Bun Runtime v1.3.8
- **Installé dans** : `~/.bun/bin/bun`
- **Ajouté au PATH** : `~/.bashrc`
- **Vérification** : `~/.bun/bin/bun --version`

### 2. Dépendances NPM (8 packages)
```
typescript@5.9.3
@biomejs/biome@2.3.11
@types/bun@1.3.5
@ai-sdk/anthropic@3.0.6
ai@6.0.11
picocolors@1.1.1
table@6.9.0
zod@4.3.5
```

### 3. Tests validés
- ✅ 86/86 tests passent
- ✅ Command-validator fonctionnel
- ✅ Sécurité Bash validée

## 🎯 Activation du Plugin

### Étape 1 : Recharger le shell
```bash
source ~/.bashrc
# Vérifier que bun est disponible
bun --version
```

### Étape 2 : Tester le plugin
```bash
# Tester la validation de sécurité (commande sûre)
echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' | \
  bun mlvn/scripts/command-validator/src/cli.ts

# Tester avec une commande dangereuse (doit bloquer)
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | \
  bun mlvn/scripts/command-validator/src/cli.ts
```

### Étape 3 : Activer le hook PreToolUse (optionnel mais recommandé)

Le hook PreToolUse valide automatiquement toutes les commandes Bash avant exécution.

**Option A : Configuration globale** (`~/.claude/settings.json`)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bun ${CLAUDE_PLUGIN_ROOT}/mlvn/scripts/command-validator/src/cli.ts"
          }
        ]
      }
    ]
  }
}
```

**Option B : Configuration projet** (`.claude/settings.json`)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bun mlvn/scripts/command-validator/src/cli.ts"
          }
        ]
      }
    ]
  }
}
```

### Étape 4 : Installer le plugin dans Claude Code
```bash
# Si pas déjà fait
/plugin install mlvn@atournayre
```

## 🚀 Utilisation des Skills

### Skills Git
```bash
/commit                   # Commit rapide + auto-push
/create-pull-request      # Créer une PR
/fix-pr-comments          # Résoudre commentaires PR
/git-merge                # Merge avec gestion conflits
```

### Skills Meta
```bash
/claude-memory           # Gestion CLAUDE.md
/prompt-creator          # Créer des prompts
/skill-creator           # Générateur de skills
/subagent-creator        # Générateur de subagents
```

### Skills Workflow
```bash
/setup-ralph -i          # Setup Ralph Loop interactif
/apex                    # Workflow apex (premium)
/apex-free               # Workflow apex (free)
```

### Skills Utils
```bash
/fix-errors              # Corriger erreurs ESLint/TypeScript
/fix-grammar             # Correction grammaticale
/oneshot                 # Actions rapides
```

## 🧪 Tests et Développement

### Exécuter les tests
```bash
cd mlvn/scripts
bun test
```

### Lint et format
```bash
cd mlvn/scripts
bun run lint             # Lint avec Biome
bun run format           # Format avec Biome
```

### Tester la statusline (nécessite configuration)
```bash
bun mlvn/scripts/statusline/src/index.ts
```

## 🛡️ Sécurité

Le hook PreToolUse bloque automatiquement :
- ❌ Commandes destructives (`rm -rf /`, `dd`, `mkfs`)
- ❌ Escalade de privilèges (`sudo`, `chmod 777`, `passwd`)
- ❌ Attaques réseau (`nc`, `nmap`, `telnet`)
- ❌ Patterns malicieux (fork bombs, backdoors)
- ❌ Accès fichiers sensibles (`/etc/passwd`, `/etc/shadow`)

Logs de sécurité : `mlvn/scripts/command-validator/data/security.log`

## 📚 Documentation

- [README.md](README.md) - Documentation complète du plugin
- [DEPENDENCY_ANALYSIS.md](DEPENDENCY_ANALYSIS.md) - Analyse détaillée des dépendances
- [CHANGELOG.md](CHANGELOG.md) - Historique des versions

## 🔧 Dépannage

### Bun non trouvé après installation
```bash
# Recharger le shell
source ~/.bashrc

# Ou utiliser le chemin complet
~/.bun/bin/bun --version
```

### Tests échouent
```bash
# Réinstaller les dépendances
cd mlvn/scripts
rm -rf node_modules
bun install
bun test
```

### Hook ne fonctionne pas
1. Vérifier que le chemin dans settings.json est correct
2. Tester le script manuellement (voir Étape 2)
3. Vérifier les logs : `~/.claude/logs/`

## 📞 Support

- [Projet original AIBlueprint](https://github.com/melvynx/aiblueprint)
- [Marketplace atournayre](https://github.com/atournayre/claude-plugin-marketplace)
- Issues : Ouvrir une issue sur GitHub

---

**Installation terminée !** 🎉

Toutes les dépendances sont installées et le plugin est prêt à l'emploi.
