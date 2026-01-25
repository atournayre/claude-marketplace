#!/usr/bin/env python3

import argparse
import json
import os
import sys
import subprocess
import random
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Add plugin hooks directory to path using CLAUDE_PLUGIN_DIR env var
script_dir = os.getenv('CLAUDE_PLUGIN_DIR', str(Path(__file__).parent))
sys.path.insert(0, script_dir)

# Desktop notification support
try:
    from utils.notification import DesktopNotification
except ImportError:
    DesktopNotification = None


def get_tts_script_path():
    """
    Determine which TTS script to use - only pyttsx3 is available.
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Use pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)
    
    return None


def announce_notification():
    """Announce that the agent needs user input."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Get engineer name if available
        engineer_name = os.getenv('ENGINEER_NAME', '').strip()

        # Create notification message with 30% chance to include name
        if engineer_name and random.random() < 0.3:
            notification_message = f"{engineer_name}, your agent needs your input"
        else:
            notification_message = "Your agent needs your input"

        # Call the TTS script with the notification message
        subprocess.run([
            "python3", tts_script, notification_message
        ],
        capture_output=True,  # Suppress output
        timeout=10  # 10-second timeout
        )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def play_beep():
    """Play a simple beep sound for desktop notifications."""
    try:
        # Try paplay first (PulseAudio - most common)
        subprocess.run(
            ["paplay", "/usr/share/sounds/freedesktop/stereo/message.oga"],
            capture_output=True,
            timeout=2
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        try:
            # Fallback to terminal beep
            print('\a', end='', flush=True)
        except Exception:
            pass  # Fail silently


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--notify', action='store_true', help='Enable TTS notifications')
        parser.add_argument('--desktop', action='store_true', help='Enable desktop notifications')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Ensure log directory exists
        import os
        log_dir = os.path.join(os.getcwd(), '.claude', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'notification.json')
        
        # Read existing log data or initialize empty list
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Announce notification via TTS only if --notify flag is set
        # Skip TTS for the generic "Claude is waiting for your input" message
        if args.notify and input_data.get('message') != 'Claude is waiting for your input':
            announce_notification()

        # Desktop notification (if --desktop flag is set and module available)
        if args.desktop and DesktopNotification:
            try:
                # Check if desktop notifications are enabled
                if os.getenv('CLAUDE_DESKTOP_NOTIFY', 'true').lower() != 'true':
                    return

                # Play beep sound
                play_beep()

                notification_type = input_data.get('notification_type', 'unknown')
                message = input_data.get('message', 'Claude Code notification')
                session_id = input_data.get('session_id', '')
                project_path = input_data.get('cwd', os.getcwd())

                # Import notification utils
                from utils.notification import (
                    get_emoji_for_notification_type,
                    get_friendly_title,
                    get_project_name,
                    get_session_title
                )
                # Import write_notification from same directory
                import importlib.util
                write_notif_path = os.path.join(script_dir, 'write_notification.py')
                spec = importlib.util.spec_from_file_location("write_notification", write_notif_path)
                write_notif_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(write_notif_module)
                write_notification = write_notif_module.write_notification

                # Get notification components
                emoji = get_emoji_for_notification_type(notification_type)
                friendly_title = get_friendly_title(notification_type)
                project_name = get_project_name(project_path) if project_path else 'Claude'
                session_title = get_session_title(session_id, project_path) if session_id and project_path else None

                # Set CLAUDE_PROJECT_PATH for write_notification
                os.environ['CLAUDE_PROJECT_PATH'] = project_path

                # Write notification to queue
                write_notification(
                    message=message,
                    type=notification_type,
                    emoji=emoji,
                    priority='normal',
                    title=f"{emoji} {friendly_title}",
                    session_title=session_title,
                    project_name=project_name,
                    metadata={
                        'session_id': session_id,
                        'project_path': project_path
                    }
                )
            except Exception:
                # Fail silently if desktop notification fails
                pass

        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == '__main__':
    main()
