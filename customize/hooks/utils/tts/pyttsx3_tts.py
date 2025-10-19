#!/usr/bin/env python3

import sys
import random

def main():
    """
    pyttsx3 TTS Script
    
    Uses pyttsx3 for offline text-to-speech synthesis.
    Accepts optional text prompt as command-line argument.
    
    Usage:
    - ./pyttsx3_tts.py                    # Uses default text
    - ./pyttsx3_tts.py "Your custom text" # Uses provided text
    
    Features:
    - Offline TTS (no API key required)
    - Cross-platform compatibility
    - Configurable voice settings
    - Immediate audio playback
    """
    
    try:
        import pyttsx3
        
        # Initialize TTS engine
        engine = pyttsx3.init()
        
        # Configure French voice if available
        voices = engine.getProperty('voices')
        french_voice = None
        
        # Priority order for French voices
        french_voice_preferences = [
            'roa/fr',           # French (France) - preferred
            'roa/fr-be',        # French (Belgium)
            'roa/fr-ch',        # French (Switzerland)
        ]
        
        # Find the best French voice (exact match)
        for pref in french_voice_preferences:
            for voice in voices:
                if voice.id == pref:  # Exact match instead of substring
                    french_voice = voice
                    break
            if french_voice:
                break
        
        # Set French voice if found
        if french_voice:
            engine.setProperty('voice', french_voice.id)
            print(f"🎙️  Voix française sélectionnée: {french_voice.name}")
        else:
            print("⚠️  Aucune voix française trouvée, utilisation de la voix par défaut")
        
        # Configure engine settings  
        engine.setProperty('rate', 160)    # Slightly slower for better French pronunciation
        engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
        
        print("🎙️  pyttsx3 TTS")
        print("=" * 15)
        
        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # Join all arguments as text
        else:
            # Default completion messages in French
            completion_messages = [
                "Travail terminé !",
                "Tout est fini !",
                "Tâche accomplie !",
                "Mission accomplie !",
                "Prêt pour la prochaine tâche !",
                "C'est dans la boîte !",
                "Opération réussie !"
            ]
            text = random.choice(completion_messages)
        
        print(f"🎯 Text: {text}")
        print("🔊 Speaking...")
        
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        
        print("✅ Playback complete!")
        
    except ImportError:
        print("❌ Error: pyttsx3 package not installed")
        print("This script uses UV to auto-install dependencies.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()