#!/usr/bin/env python3
"""
Dispatch unread notifications from queue.jsonl.
Reads unread notifications and dispatches them to configured dispatcher(s).
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# Add plugin hooks directory to path using CLAUDE_PLUGIN_ROOT env var
plugin_root = os.getenv('CLAUDE_PLUGIN_ROOT', str(Path(__file__).parent.parent))
sys.path.insert(0, os.path.join(plugin_root, 'hooks'))
from utils.notification.backends.file_queue import FileQueueBackend


def get_queue_file() -> str:
    """Get queue file path using same logic as FileQueueBackend."""
    backend = FileQueueBackend({})
    return backend._get_queue_file()


def read_notifications(queue_file: str) -> List[Dict[str, Any]]:
    """Read all notifications from queue file."""
    if not os.path.exists(queue_file):
        return []

    notifications = []
    with open(queue_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                notifications.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    return notifications


def write_notifications(queue_file: str, notifications: List[Dict[str, Any]]):
    """Write all notifications back to queue file."""
    os.makedirs(os.path.dirname(queue_file), exist_ok=True)
    with open(queue_file, 'w', encoding='utf-8') as f:
        for notif in notifications:
            f.write(json.dumps(notif, ensure_ascii=False) + '\n')


def dispatch_notify_send(notification: Dict[str, Any]) -> bool:
    """Dispatch notification via notify-send (auto-read)."""
    try:
        # Map priority to urgency
        priority_map = {
            'critical': 'critical',
            'high': 'normal',
            'normal': 'normal',
            'low': 'low'
        }
        urgency = priority_map.get(notification.get('priority', 'normal'), 'normal')

        # Use timeout from environment variable (default: 0 = permanent)
        timeout = os.getenv('CLAUDE_DESKTOP_NOTIFY_TIMEOUT', '0')

        title = notification.get('title', 'Claude Code')
        message = notification.get('message', '')
        emoji = notification.get('emoji', '')

        # Combine emoji and message
        full_message = f"{emoji} {message}" if emoji else message

        subprocess.run([
            'notify-send',
            '--urgency', urgency,
            '--expire-time', timeout,
            title,
            full_message
        ], check=True)

        return True
    except subprocess.SubprocessError:
        return False


def main():
    """Main dispatcher function."""
    # Get dispatcher type from environment
    dispatcher_type = os.getenv('CLAUDE_NOTIFICATION_DISPATCHER', 'notify-send')

    # Get queue file
    queue_file = get_queue_file()

    # Read all notifications
    notifications = read_notifications(queue_file)

    if not notifications:
        return

    # Filter unread
    unread = [n for n in notifications if n.get('status') == 'unread']

    if not unread:
        return

    # Dispatch each unread notification
    for notification in unread:
        if dispatcher_type == 'notify-send':
            success = dispatch_notify_send(notification)
            if success:
                # Mark as read automatically for notify-send
                notification['status'] = 'read'

        elif dispatcher_type == 'phpstorm':
            # PhpStorm plugin will mark as read manually
            # Just log for now (plugin will be developed later)
            pass

        # Add more dispatchers here as needed

    # Write back updated notifications
    write_notifications(queue_file, notifications)


if __name__ == '__main__':
    main()
