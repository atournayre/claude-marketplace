#!/usr/bin/env python3

import json
import os
import stat
import sys
from pathlib import Path

def fix_permissions(path: Path):
    """
    Ajuste les permissions des fichiers et dossiers créés.
    - Dossiers: 755 (rwxr-xr-x) - lecture/exécution pour tous
    - Fichiers: 644 (rw-r--r--) - lecture pour tous, écriture propriétaire
    """
    try:
        if path.is_dir():
            # Permissions dossiers: 755 (0o755)
            os.chmod(path, 0o755)
        elif path.is_file():
            # Permissions fichiers: 644 (0o644)
            os.chmod(path, 0o644)
    except (OSError, PermissionError):
        # Ignore silencieusement les erreurs de permissions
        pass

def process_write_tool(tool_input: dict):
    """Traite les outils Write pour ajuster les permissions."""
    file_path = tool_input.get('file_path')
    if file_path:
        path = Path(file_path)
        if path.exists():
            fix_permissions(path)
            # Corriger aussi le dossier parent si nécessaire
            parent = path.parent
            if parent.exists():
                fix_permissions(parent)

def process_bash_tool(tool_input: dict):
    """Traite les commandes Bash pour détecter mkdir et ajuster permissions."""
    command = tool_input.get('command', '')

    # Détecter mkdir avec extraction du chemin
    if 'mkdir' in command:
        # Extraction basique du chemin après mkdir
        parts = command.split()
        for i, part in enumerate(parts):
            if part == 'mkdir' and i + 1 < len(parts):
                # Ignorer les flags (-p, etc.)
                next_part = parts[i + 1]
                if not next_part.startswith('-'):
                    path = Path(next_part)
                    if path.exists():
                        fix_permissions(path)

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Traiter selon le type de tool
        tool_name = input_data.get('tool_name')
        tool_input = input_data.get('tool_input', {})

        # Debug log
        debug_path = Path.cwd() / '.claude' / 'logs' / 'permissions_debug.log'
        with open(debug_path, 'a') as f:
            f.write(f"Tool: {tool_name}, Input: {tool_input}\n")

        if tool_name == 'Write':
            process_write_tool(tool_input)
        elif tool_name == 'Bash':
            process_bash_tool(tool_input)

        # Ensure log directory exists
        log_dir = Path.cwd() / '.claude' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'post_tool_use.json'

        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)

if __name__ == '__main__':
    main()