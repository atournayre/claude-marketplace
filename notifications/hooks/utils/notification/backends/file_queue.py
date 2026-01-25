#!/usr/bin/env python3
"""
File Queue notification backend.
Generic JSONL queue file for any integration (not PhpStorm-specific).
"""

import subprocess
import os
import json
import uuid
from pathlib import Path
from typing import Optional
from .base import NotificationBackend


class FileQueueBackend(NotificationBackend):
    """File Queue notification backend - generic JSONL queue."""

    def is_available(self) -> bool:
        """Check if notification queue file can be created."""
        queue_file = self._get_queue_file()
        try:
            os.makedirs(os.path.dirname(queue_file), exist_ok=True)
            return True
        except (OSError, IOError):
            return False

    def _get_queue_file(self) -> str:
        """Get notification queue file path."""
        # 1. Check if explicitly configured
        if 'queue_file' in self.config and self.config['queue_file']:
            return os.path.expanduser(self.config['queue_file'])

        # 2. Check if CLAUDE_PROJECT_PATH env var is set (from hooks)
        project_path = os.getenv('CLAUDE_PROJECT_PATH')
        if project_path and os.path.exists(project_path):
            # If project_path already ends with .claude, use it directly
            if project_path.endswith('.claude'):
                claude_dir = project_path
            else:
                claude_dir = os.path.join(project_path, '.claude')

            if os.path.isdir(claude_dir):
                queue_file = os.path.join(claude_dir, 'notifications', 'queue.jsonl')
                return queue_file

        # 3. Find nearest .claude directory from current working directory
        cwd = os.getcwd()

        # If we're already inside a .claude directory, use it
        if '.claude' in cwd.split(os.sep):
            # Find the .claude part in the path
            parts = cwd.split(os.sep)
            try:
                claude_index = parts.index('.claude')
                claude_dir = os.sep.join(parts[:claude_index + 1])
                queue_file = os.path.join(claude_dir, 'notifications', 'queue.jsonl')
                return queue_file
            except ValueError:
                pass

        # Otherwise, search upwards
        current_dir = cwd
        while current_dir != '/':
            claude_dir = os.path.join(current_dir, '.claude')
            if os.path.isdir(claude_dir):
                queue_file = os.path.join(claude_dir, 'notifications', 'queue.jsonl')
                return queue_file
            current_dir = os.path.dirname(current_dir)

        # 4. Fallback to global ~/.claude/notifications/queue.jsonl
        return os.path.expanduser('~/.claude/notifications/queue.jsonl')

    def _get_notification_script(self) -> Optional[str]:
        """Get path to notification script if configured."""
        script = self.config.get('script')
        if script:
            return os.path.expanduser(script)
        return None

    def send(self, data: 'NotificationData') -> bool:
        """Send notification via file queue."""
        try:
            # Write to JSONL queue file
            queue_file = self._get_queue_file()
            os.makedirs(os.path.dirname(queue_file), exist_ok=True)

            # Create notification entry with unique ID and status
            notification_entry = {
                'id': str(uuid.uuid4()),
                'timestamp': data.timestamp or data.get_timestamp(),
                'status': 'unread',
                'title': data.get_title(),
                'message': data.message,
                'type': data.type,
                'emoji': data.emoji,
                'priority': data.priority,
                'session_title': data.session_title,
                'project_name': data.project_name,
                'metadata': data.metadata
            }

            # Append to queue file (JSONL format)
            with open(queue_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(notification_entry, ensure_ascii=False) + '\n')

            return True

        except (OSError, IOError, json.JSONDecodeError):
            return False

    def _execute_notification_script(self, script: str, notification_entry: dict):
        """Execute custom notification script."""
        try:
            # Pass notification data as JSON to script
            subprocess.Popen(
                [script, json.dumps(notification_entry)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except (subprocess.SubprocessError, OSError):
            pass

    def get_name(self) -> str:
        """Get backend name."""
        return 'file-queue'
