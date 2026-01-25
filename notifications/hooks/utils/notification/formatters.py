#!/usr/bin/env python3
"""
Formatters for notification messages with session title support.
"""

import json
import os
from pathlib import Path
from typing import Optional, Tuple


def get_project_name(project_path: str) -> str:
    """
    Extract project name from project path.

    Args:
        project_path: Full path to project directory

    Returns:
        Project name (last directory in path) or 'Claude' as fallback
    """
    if not project_path:
        return 'Claude'

    try:
        # Get last directory name from path
        project_name = os.path.basename(os.path.normpath(project_path))
        # Remove leading dots if present (.claude → claude)
        project_name = project_name.lstrip('.')
        return project_name if project_name else 'Claude'
    except (OSError, AttributeError):
        return 'Claude'


def get_session_title(session_id: str, project_path: str) -> Optional[str]:
    """
    Get session title from sessions-index.json if it exists.

    Args:
        session_id: Session ID
        project_path: Path to project directory

    Returns:
        Session title (summary) or None if not found
    """
    try:
        # Construct path to sessions-index.json
        # Example: /home/user/.claude/projects/-home-user--claude/sessions-index.json
        # Claude Code replaces / with - and . with - in project paths
        # So /home/user/.claude becomes -home-user--claude (note the double --)
        project_dir_name = project_path.replace('/', '-').replace('.', '-')
        sessions_index = Path.home() / '.claude' / 'projects' / project_dir_name / 'sessions-index.json'

        if not sessions_index.exists():
            return None

        with open(sessions_index, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Search for session in entries
        for entry in data.get('entries', []):
            if entry.get('sessionId') == session_id:
                return entry.get('summary')

        return None

    except (FileNotFoundError, json.JSONDecodeError, KeyError, OSError):
        return None


def format_completion_message(
    session_id: str,
    duration: float,
    project_path: str = ''
) -> Tuple[str, str]:
    """
    Format completion notification (title, body).

    Args:
        session_id: Session ID
        duration: Duration in seconds
        project_path: Project path (for session title lookup)

    Returns:
        Tuple of (title, body)
    """
    # Get session title if available
    session_title = get_session_title(session_id, project_path) if project_path else None

    if session_title:
        title = f"✅ {session_title}"
        body = f"Durée: {duration:.1f}s"
    else:
        title = "✅ Claude Code - Tâche terminée"
        body = f"Session: {session_id[:8]}\nDurée: {duration:.1f}s"

    return title, body


def get_short_message(message: str, max_length: int = 25) -> str:
    """
    Shorten message for grouped notification display.

    Args:
        message: Original message
        max_length: Maximum length

    Returns:
        Shortened message
    """
    if len(message) <= max_length:
        return message
    return message[:max_length - 3] + '...'


def get_notification_replace_id(project_path: str) -> int:
    """
    Get a consistent replace ID for a project's grouped notification.

    Args:
        project_path: Project path

    Returns:
        Integer ID for notification replacement (hash of project name)
    """
    project_name = get_project_name(project_path)
    # Use a simple hash to get a consistent ID between 1000 and 9999
    return 1000 + (hash(project_name) % 9000)
