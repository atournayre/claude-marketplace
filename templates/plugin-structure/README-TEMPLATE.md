# Plugin [NOM]

[Description courte du plugin]

## Installation

```bash
/plugin install [nom]@atournayre
```

## Skills Disponibles

Le plugin [nom] fournit X skills :

### `/skill-name`

[Description du skill]

**Usage :**
```bash
/skill-name [arguments]
```

**Exemples :**
```bash
# Exemple 1
/skill-name arg1

# Exemple 2
/skill-name --option
```

---

## Agents Disponibles

Le plugin [nom] fournit X agents :

### `agent-name`

[Description de l'agent]

**Usage :**
```yaml
agents:
  - name: agent-name
    prompt: "Description de la tâche"
```

---

## Structure

```
[nom]/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── skill-name/
│       └── SKILL.md
├── agents/
│   └── agent-name.md
├── README.md
├── CHANGELOG.md
└── DEPENDENCIES.json
```

## Dépendances

Voir `DEPENDENCIES.json` pour la liste complète.

## Licence

MIT
