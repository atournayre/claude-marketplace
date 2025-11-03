---
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
description: Indique d'utiliser docker pour faire la ou les actions définies dans le prompt
model: claude-sonnet-4-5-20250929
---

# Contexte Docker

Active le mode Docker pour exécuter toutes les actions dans des conteneurs Docker plutôt que directement sur l'hôte.

## Purpose

Cette commande active un contexte spécial où Claude utilisera systématiquement Docker pour :
- Exécuter des commandes système
- Builder des projets
- Lancer des tests
- Gérer les dépendances
- Toute autre opération technique

## Variables

- DOCKER_COMPOSE_FILE: Fichier docker-compose à utiliser (défaut: docker-compose.yml)
- DOCKER_SERVICE: Service Docker à cibler pour les commandes (optionnel)
- DOCKER_ENV: Environnement Docker (dev/staging/prod, défaut: dev)

## Relevant Files

- `docker-compose.yml` - Configuration Docker Compose
- `Dockerfile` - Définition des images
- `.dockerignore` - Fichiers exclus du build
- `docker/` - Configurations Docker additionnelles

## Workflow

### Étape 1: Analyse de l'environnement Docker
- Détecter le fichier docker-compose.yml ou Dockerfile
- Identifier les services Docker disponibles
- Vérifier l'état des conteneurs (docker ps)
- Lister les services configurés

### Étape 2: Validation de Docker
- Vérifier que Docker est installé et accessible
- Confirmer que les conteneurs nécessaires sont démarrés ou peuvent l'être
- Identifier le service principal si plusieurs services existent

### Étape 3: Configuration du contexte
- Enregistrer le mode Docker comme actif pour la session
- Déterminer le préfixe de commande à utiliser :
  - `docker exec [container]` pour conteneurs running
  - `docker-compose exec [service]` pour docker-compose
  - `docker run` pour images standalone
- Mémoriser les paramètres pour les prochaines commandes

### Étape 4: Rapport de configuration
- Afficher la configuration Docker détectée
- Confirmer le mode actif
- Indiquer comment les prochaines commandes seront exécutées

## Instructions pour Claude

**MODE DOCKER ACTIF**

À partir de maintenant et jusqu'à nouvel ordre :

1. **Toutes les commandes système** doivent être exécutées via Docker
2. **Format des commandes** :
   - Avec Docker Compose : `docker compose exec [service] [commande]`
   - Sans Docker Compose : `docker exec [container] [commande]`
   - Pour les builds : `docker compose build` ou `docker build`

3. **Exemples de transformation** :
   ```bash
   # Au lieu de : composer install
   # Utiliser : docker compose exec php composer install

   # Au lieu de : npm run build
   # Utiliser : docker compose exec node npm run build

   # Au lieu de : php bin/console cache:clear
   # Utiliser : docker compose exec php php bin/console cache:clear
   ```

4. **Services communs à identifier** :
   - `php` / `app` - Application PHP
   - `node` / `frontend` - Build frontend
   - `web` / `nginx` - Serveur web
   - `db` / `database` - Base de données

5. **Gestion des erreurs** :
   - Si un conteneur n'est pas démarré → suggérer `docker compose up -d`
   - Si un service n'existe pas → lister les services disponibles
   - Si Docker n'est pas accessible → indiquer clairement l'erreur

6. **Persistance du contexte** :
   - Ce mode reste actif pour toute la session
   - Peut être désactivé avec une commande explicite de l'utilisateur
   - S'applique à toutes les opérations : build, test, deploy, etc.

## Report

```
🐳 Mode Docker Activé

Configuration détectée :
- Fichier : [docker-compose.yml / Dockerfile]
- Services disponibles :
  • [service1] - [description]
  • [service2] - [description]
  • [service3] - [description]

État des conteneurs :
- [X] [service1] - Running
- [ ] [service2] - Stopped
- [X] [service3] - Running

Format des commandes :
docker compose exec [service] [commande]

Exemples :
• composer install → docker compose exec php composer install
• npm run build → docker compose exec node npm run build
• php bin/console → docker compose exec php php bin/console

ℹ️ Toutes les prochaines commandes système seront exécutées via Docker.
```

## Examples

### Activation basique
```bash
/docker
```

### Avec projet Symfony + Docker Compose
```
🐳 Mode Docker Activé

Services disponibles : php, nginx, database, redis

Commandes transformées :
• composer install → docker compose exec php composer install
• symfony console cache:clear → docker compose exec php php bin/console cache:clear
```

### Avec projet Node.js
```
🐳 Mode Docker Activé

Service : node

Commandes transformées :
• npm install → docker compose exec node npm install
• npm run dev → docker compose exec node npm run dev
```

## Best Practices

- Toujours vérifier que Docker est accessible avant d'activer le mode
- Identifier le service principal pour les commandes fréquentes
- Proposer `docker compose up -d` si les conteneurs ne sont pas démarrés
- Conserver le contexte Docker pour toute la session une fois activé
- Adapter les commandes de manière transparente pour l'utilisateur
- En cas d'échec Docker, expliquer clairement la raison et la solution
