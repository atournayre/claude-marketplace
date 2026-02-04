# Checklist Sécurité

## Injection
- [ ] Pas d'injection SQL (requêtes préparées, ORM)
- [ ] Pas d'injection de commandes (escapeshellarg)
- [ ] Pas de XSS (échappement output)
- [ ] Pas d'injection LDAP/XML/XPath

## Authentification
- [ ] Mots de passe hashés (bcrypt/argon2)
- [ ] Tokens avec expiration
- [ ] Protection brute force (rate limiting, captcha)
- [ ] Sessions sécurisées (httpOnly, secure, sameSite)

## Autorisation
- [ ] Vérification des permissions à chaque requête
- [ ] Pas d'IDOR (accès objets par ID non autorisé)
- [ ] Principe du moindre privilège

## Données sensibles
- [ ] Pas de secrets en dur dans le code
- [ ] Pas de logs de données personnelles
- [ ] Chiffrement des données sensibles au repos
- [ ] HTTPS pour données en transit

## Fichiers
- [ ] Upload : validation type MIME + extension
- [ ] Upload : limite de taille
- [ ] Pas d'exécution de fichiers uploadés
- [ ] Pas de path traversal (../)

## Headers
- [ ] Content-Security-Policy
- [ ] X-Frame-Options
- [ ] X-Content-Type-Options
- [ ] Strict-Transport-Security

## Dépendances
- [ ] Pas de vulnérabilités connues (composer audit)
- [ ] Versions à jour des packages critiques

## OWASP Top 10
Vérifier : A01-Broken Access Control, A02-Crypto Failures, A03-Injection, A07-Auth Failures
