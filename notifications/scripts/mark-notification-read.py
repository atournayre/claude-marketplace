#!/usr/bin/env python3
"""
Mark notification(s) as read in queue.jsonl.
Usage:
    mark-notification-read.py <notification_id>
    mark-notification-read.py --all
"""

import sys
import os
import json
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


def mark_as_read(notification_id: str = None, mark_all: bool = False) -> int:
    """Mark notification(s) as read. Returns count of notifications marked."""
    queue_file = get_queue_file()
    notifications = read_notifications(queue_file)

    count = 0
    for notification in notifications:
        if mark_all:
            if notification.get('status') == 'unread':
                notification['status'] = 'read'
                count += 1
        elif notification.get('id') == notification_id:
            if notification.get('status') == 'unread':
                notification['status'] = 'read'
                count += 1
            break

    if count > 0:
        write_notifications(queue_file, notifications)

    return count


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: mark-notification-read.py <notification_id>")
        print("       mark-notification-read.py --all")
        sys.exit(1)

    if sys.argv[1] == '--all':
        count = mark_as_read(mark_all=True)
        print(f"✅ Marked {count} notification(s) as read")
    else:
        notification_id = sys.argv[1]
        count = mark_as_read(notification_id=notification_id)
        if count > 0:
            print(f"✅ Notification {notification_id} marked as read")
        else:
            print(f"❌ Notification {notification_id} not found or already read")


if __name__ == '__main__':
    main()
