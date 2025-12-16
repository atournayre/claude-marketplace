# Modèles Gemini - Référence

> Source : https://ai.google.dev/gemini-api/docs/models
> Dernière mise à jour : 2025-12-16

## Modèles recommandés

| Usage | Model ID | Notes |
|-------|----------|-------|
| Raisonnement complexe | `gemini-3-pro-preview` | Gemini 3, preview |
| Contexte ultra-long | `gemini-2.5-pro` | Stable, 1M tokens |
| Recherche rapide | `gemini-2.5-flash` | Stable, rapide |
| Ultra-léger | `gemini-2.5-flash-lite` | Stable, économique |

## Liste complète

### Gemini 3

| Model ID | Description |
|----------|-------------|
| `gemini-3-pro-preview` | Raisonnement avancé, multimodal |
| `gemini-3-pro-image-preview` | Génération/édition d'images |

### Gemini 2.5 Flash

| Model ID | Description |
|----------|-------------|
| `gemini-2.5-flash` | **Stable** - Usage général, rapide |
| `gemini-2.5-flash-lite` | **Stable** - Ultra-léger, économique |
| `gemini-2.5-flash-image` | Génération d'images |
| `gemini-2.5-flash-native-audio-preview-12-2025` | Audio natif |
| `gemini-2.5-flash-preview-tts` | Text-to-speech |

### Gemini 2.5 Pro

| Model ID | Description |
|----------|-------------|
| `gemini-2.5-pro` | **Stable** - Contexte long (1M tokens) |
| `gemini-2.5-pro-preview-tts` | Text-to-speech |

### Gemini 2.0 (Legacy)

| Model ID | Description |
|----------|-------------|
| `gemini-2.0-flash` | Usage général |
| `gemini-2.0-flash-001` | Version spécifique |
| `gemini-2.0-flash-lite` | Léger |
| `gemini-2.0-flash-lite-001` | Version spécifique |

## Utilisation dans ce plugin

| Agent | Modèle Gemini | Raison |
|-------|---------------|--------|
| `gemini-analyzer` | `gemini-3-pro-preview` | Raisonnement + contexte long |
| `gemini-thinker` | `gemini-3-pro-preview` | Deep Think, réflexion avancée |
| `gemini-researcher` | `gemini-2.5-flash` | Rapidité pour recherche web |

## Notes

- Les modèles **stable** sont recommandés pour la production
- Les modèles **preview** peuvent changer sans préavis
- Gemini 3 Pro n'a pas encore de version stable (preview uniquement)
