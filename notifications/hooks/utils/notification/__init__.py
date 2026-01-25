#!/usr/bin/env python3
"""
Notification module for Claude Code hooks.
"""

# Data structure
from .data import NotificationData

# Backends
from .backends import (
    NotificationBackend,
    FileQueueBackend
)

# Desktop notifications
from .desktop import DesktopNotification
from .icons import get_emoji_for_notification_type, get_icon_path
from .formatters import (
    format_completion_message,
    get_session_title,
    get_project_name
)

__all__ = [
    # Core
    'NotificationData',
    'NotificationBackend',
    'FileQueueBackend',

    # Desktop
    'DesktopNotification',
    'get_emoji_for_notification_type',
    'get_icon_path',
    'format_completion_message',
    'get_session_title',
    'get_project_name'
]
