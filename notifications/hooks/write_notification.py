#!/usr/bin/env python3
"""
Write notification to queue.jsonl.
Simple writer without backend complexity.
"""

import os
import sys
import json
import uuid
from pathlib import Path
from datetime import datetime


def get_queue_file() -> str:
    """
    Get notification queue file path with project auto-detection.

    Priority:
    1. CLAUDE_FILE_QUEUE_FILE env var (if set and not empty)
    2. CLAUDE_PROJECT_PATH env var (from hooks)
    3. Nearest .claude directory (search upward)
    4. Fallback to ~/.claude/notifications/queue.jsonl
    """
    # 1. Check if explicitly configured
    queue_file = os.getenv('CLAUDE_FILE_QUEUE_FILE')
    if queue_file:
        return os.path.expanduser(queue_file)

    # 2. Check if CLAUDE_PROJECT_PATH env var is set (from hooks)
    project_path = os.getenv('CLAUDE_PROJECT_PATH')
    if project_path and os.path.exists(project_path):
        # If project_path already ends with .claude, use it directly
        if project_path.endswith('.claude'):
            claude_dir = project_path
        else:
            claude_dir = os.path.join(project_path, '.claude')

        if os.path.isdir(claude_dir):
            return os.path.join(claude_dir, 'notifications', 'queue.jsonl')

    # 3. Find nearest .claude directory from current working directory
    cwd = os.getcwd()

    # If we're already inside a .claude directory, use it
    if '.claude' in cwd.split(os.sep):
        parts = cwd.split(os.sep)
        try:
            claude_index = parts.index('.claude')
            claude_dir = os.sep.join(parts[:claude_index + 1])
            return os.path.join(claude_dir, 'notifications', 'queue.jsonl')
        except ValueError:
            pass

    # Otherwise, search upwards
    current_dir = cwd
    while current_dir != '/':
        claude_dir = os.path.join(current_dir, '.claude')
        if os.path.isdir(claude_dir):
            return os.path.join(claude_dir, 'notifications', 'queue.jsonl')
        current_dir = os.path.dirname(current_dir)

    # 4. Fallback to global ~/.claude/notifications/queue.jsonl
    return os.path.expanduser('~/.claude/notifications/queue.jsonl')


def write_notification(
    message: str,
    type: str = 'info',
    emoji: str = '📋',
    priority: str = 'normal',
    title: str = None,
    session_title: str = None,
    project_name: str = None,
    metadata: dict = None
) -> bool:
    """Write notification to queue file."""
    try:
        queue_file = get_queue_file()
        os.makedirs(os.path.dirname(queue_file), exist_ok=True)

        # Create notification entry
        notification = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'status': 'unread',
            'title': title or f"{emoji} {type}",
            'message': message,
            'type': type,
            'emoji': emoji,
            'priority': priority,
            'session_title': session_title or '',
            'project_name': project_name or '',
            'metadata': metadata or {}
        }

        # Append to queue
        with open(queue_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(notification, ensure_ascii=False) + '\n')

        return True

    except (OSError, IOError, json.JSONDecodeError):
        return False


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: write_notification.py <message> [type] [emoji] [priority]")
        sys.exit(1)

    message = sys.argv[1]
    type = sys.argv[2] if len(sys.argv) > 2 else 'info'
    emoji = sys.argv[3] if len(sys.argv) > 3 else '📋'
    priority = sys.argv[4] if len(sys.argv) > 4 else 'normal'

    success = write_notification(message, type, emoji, priority)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
