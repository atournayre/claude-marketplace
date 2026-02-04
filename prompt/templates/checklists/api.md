# Checklist API / Intégration

## Validation entrées
- [ ] Payload validé (types, formats, valeurs)
- [ ] Taille max des champs vérifiée
- [ ] Caractères spéciaux échappés/filtrés

## Authentification
- [ ] Mécanisme en place (API key, JWT, OAuth, HMAC)
- [ ] Secrets dans variables d'environnement
- [ ] Rotation des clés prévue

## Sécurité
- [ ] HTTPS obligatoire
- [ ] Rate limiting configuré
- [ ] Pas d'exposition de données sensibles dans logs
- [ ] Validation signature (webhook entrant)

## Robustesse
- [ ] Timeout configuré sur appels sortants
- [ ] Retry avec backoff exponentiel
- [ ] Circuit breaker si service critique
- [ ] Gestion des erreurs réseau

## Logging & Monitoring
- [ ] Logs des appels (request ID, durée, statut)
- [ ] Alertes sur erreurs 5xx
- [ ] Métriques de latence

## Tests
- [ ] Tests avec mocks des services externes
- [ ] Tests des cas d'erreur (timeout, 4xx, 5xx)
- [ ] Tests de validation payload

## Documentation
- [ ] Endpoint documenté (OpenAPI si applicable)
- [ ] Exemples de requêtes/réponses
- [ ] Codes d'erreur listés
