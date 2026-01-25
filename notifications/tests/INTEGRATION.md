# Tests d'intégration - Notifications Desktop Claude Code

## Prérequis

Vérifier que `notify-send` est installé :
```bash
which notify-send
# Si absent : sudo apt install libnotify-bin
```

## Test 1 : Notification de complétion

**Objectif** : Vérifier qu'une notification desktop s'affiche à la fin d'une tâche

**Étapes** :
1. Lancer Claude Code dans un projet
2. Exécuter une commande simple : `ls`
3. Attendre que Claude termine
4. Vérifier qu'une notification desktop apparaît avec :
   - Icône : ✅
   - Titre : "Claude Code - Tâche terminée" ou titre de session si défini
   - Corps : Session ID + durée

**Résultat attendu** : Notification visible avec emoji ✅

---

## Test 2 : Emojis par type de notification

### 2.1 Permission Prompt (🔐)

**Étapes** :
1. Configurer Claude Code pour demander permission sur certaines actions
2. Exécuter une action nécessitant permission
3. Vérifier notification avec 🔐

**Résultat attendu** : Notification "🔐 Claude Code" ou "🔐 [titre session]"

### 2.2 Idle Prompt (⏰)

**Étapes** :
1. Lancer Claude Code
2. Attendre 60+ secondes sans donner d'input
3. Vérifier notification idle_prompt

**Résultat attendu** : Notification "⏰ Claude Code" indiquant attente input

### 2.3 Auth Success (✅)

**Étapes** :
1. Se déconnecter de Claude Code
2. Se reconnecter
3. Vérifier notification auth_success

**Résultat attendu** : Notification "✅ Claude Code"

### 2.4 Elicitation Dialog (❓)

**Étapes** :
1. Utiliser un outil MCP nécessitant input utilisateur
2. Vérifier notification elicitation_dialog

**Résultat attendu** : Notification "❓ Claude Code"

---

## Test 3 : Titre de session (via /rename)

### 3.1 Sans titre de session

**Étapes** :
1. Lancer nouvelle session Claude Code (sans `/rename`)
2. Exécuter une tâche
3. Observer notification

**Résultat attendu** :
- Titre : "✅ Claude Code - Tâche terminée"
- Corps : "Session: abc123\nDurée: X.Xs"

### 3.2 Avec titre de session

**Étapes** :
1. Lancer nouvelle session
2. Exécuter `/rename "Amélioration notifications desktop"`
3. Exécuter une tâche
4. Observer notification

**Résultat attendu** :
- Titre : "✅ Amélioration notifications desktop"
- Corps : "Durée: X.Xs"

---

## Test 4 : Désactivation des notifications

**Étapes** :
1. Modifier `.claude/settings.json` :
   ```json
   {
     "env": {
       "CLAUDE_DESKTOP_NOTIFY": "false"
     }
   }
   ```
2. Redémarrer Claude Code
3. Exécuter une tâche

**Résultat attendu** : Aucune notification desktop (TTS peut toujours fonctionner)

---

## Test 5 : Fallback gracieux

**Étapes** :
1. Sauvegarder `notify-send` :
   ```bash
   sudo mv /usr/bin/notify-send /usr/bin/notify-send.bak
   ```
2. Lancer Claude Code
3. Exécuter une tâche
4. Vérifier que le hook ne crash pas
5. Restaurer `notify-send` :
   ```bash
   sudo mv /usr/bin/notify-send.bak /usr/bin/notify-send
   ```

**Résultat attendu** : Pas de crash, pas d'erreur visible, hook se termine proprement

---

## Test 6 : Notification subagent

**Étapes** :
1. Lancer une tâche nécessitant un sous-agent
2. Attendre fin du sous-agent
3. Observer notification

**Résultat attendu** :
- Titre : "🤖 [titre session]" ou "🤖 Sous-agent terminé"
- Urgency : low

---

## Checklist finale

- [ ] Test 1 : Notification complétion ✅
- [ ] Test 2.1 : Emoji permission_prompt 🔐
- [ ] Test 2.2 : Emoji idle_prompt ⏰
- [ ] Test 2.3 : Emoji auth_success ✅
- [ ] Test 2.4 : Emoji elicitation_dialog ❓
- [ ] Test 3.1 : Sans titre session (titre générique)
- [ ] Test 3.2 : Avec titre session (/rename)
- [ ] Test 4 : Désactivation CLAUDE_DESKTOP_NOTIFY=false
- [ ] Test 5 : Fallback sans notify-send
- [ ] Test 6 : Notification sous-agent 🤖
- [ ] Pas de régression TTS existant
- [ ] Logs JSON fonctionnent toujours

---

## Notes

- Les notifications desktop s'affichent en plus du TTS existant
- Les emojis doivent être visibles dans le titre de la notification
- Le titre de session doit être lu depuis `sessions-index.json`
- Tous les hooks doivent fail silently en cas d'erreur
