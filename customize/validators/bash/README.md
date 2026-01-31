# Bash Command Validator

Validateur de sécurité pour les commandes bash dans Claude Code. Intégré via le hook PreToolUse pour bloquer les opérations dangereuses avant exécution.

## Fonctionnalités

- **100+ règles de sécurité** : Bloque commandes dangereuses (rm -rf /, dd, mkfs, etc.)
- **Détection de patterns malveillants** : Fork bombs, backdoors, exfiltration de données
- **Protection des chemins système** : Empêche écritures dans /etc, /usr, /bin, etc.
- **Validation des chaînes de commandes** : Analyse &&, ||, ;
- **82+ tests** : Suite de tests complète avec Vitest

## Installation

```bash
cd customize/validators/bash
bun install
```

## Utilisation

### En tant que hook Claude Code

Configuration dans `.claude-plugin/hooks.json` :

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bun ${CLAUDE_PLUGIN_ROOT}/validators/bash/src/cli.ts"
          }
        ]
      }
    ]
  }
}
```

### Utilisation programmatique

```typescript
import { CommandValidator } from "./src/lib/validator";

const validator = new CommandValidator();
const result = validator.validate("rm -rf /");

if (!result.isValid) {
  console.log(`Bloqué: ${result.violations.join(", ")}`);
  console.log(`Sévérité: ${result.severity}`);
}
```

## Tests

```bash
# Lancer tous les tests (82+)
bun test

# Tests avec interface UI
bun test:ui

# Linting
bun run lint

# Vérification types
bun run typecheck
```

## Couverture des Tests

### Commandes Sûres (Autorisées)
- Utilitaires standard : ls, git, npm, pnpm, node, python
- Opérations fichiers : cat, cp, mv, mkdir, touch
- Chaînes de commandes safe avec &&

### Commandes Dangereuses (Bloquées)
- Destruction système : rm -rf /, dd, mkfs, fdisk
- Escalade privilèges : sudo, chmod, chown, passwd
- Attaques réseau : nc, nmap, telnet
- Patterns malveillants : fork bombs, backdoors, manipulation logs
- Accès fichiers sensibles : /etc/passwd, /etc/shadow, /etc/sudoers

### Cas Spéciaux
- rm -rf sécurisé : Autorise suppressions dans chemins safe (~/Developer/, /tmp/)
- Chemins protégés : Bloque opérations dangereuses sur /etc, /usr, /bin, etc.
- Détection contenu binaire
- Limites longueur commandes

## Architecture

```
src/
├── cli.ts                 # Point d'entrée CLI (utilisé par hook Claude Code)
├── lib/
│   ├── types.ts           # Interfaces TypeScript
│   ├── security-rules.ts  # Base de données règles sécurité (100+ patterns)
│   └── validator.ts       # Logique validation principale
__tests__/
    └── validator.test.ts  # Suite tests complète (82+ tests)
```

## Règles de Sécurité

### Commandes Critiques
`del`, `format`, `mkfs`, `shred`, `dd`, `fdisk`, `parted`

### Escalade de Privilèges
`sudo`, `su`, `passwd`, `chpasswd`, `usermod`, `chmod`, `chown`

### Commandes Réseau
`nc`, `netcat`, `nmap`, `telnet`, `ssh-keygen`, `iptables`

### Manipulation Système
`systemctl`, `service`, `kill`, `killall`, `mount`, `umount`

### Chemins Protégés
`/etc/`, `/usr/`, `/sbin/`, `/boot/`, `/sys/`, `/proc/`, `/dev/`, `/root/`

## Logs de Sécurité

Événements sécurité loggés dans `data/security.log` :
- Timestamp
- Session ID
- Nom outil
- Commande (tronquée à 500 chars)
- Statut bloqué/autorisé
- Niveau sévérité
- Violations détectées

Le dossier `data/` est gitignored pour éviter commit données sensibles.

## Développement

```bash
# Linter
bun run lint

# Formater code
bun run format

# Type check
bun run typecheck
```

## Licence

MIT
