#!/usr/bin/env python3
"""
Icon and emoji mappings for notifications.
"""


def get_icon_path(status: str) -> str:
    """
    Get system icon path for notification status.

    Args:
        status: Status type ('success', 'error', 'warning', 'info')

    Returns:
        Icon name compatible with notify-send
    """
    icons = {
        'success': 'dialog-information',
        'error': 'dialog-error',
        'warning': 'dialog-warning',
        'info': 'dialog-information'
    }
    return icons.get(status, 'dialog-information')


def get_emoji_for_notification_type(notification_type: str) -> str:
    """
    Get emoji for Claude Code notification type.

    Args:
        notification_type: Type of notification from Claude Code

    Returns:
        Emoji character for the notification type
    """
    emojis = {
        'permission_prompt': '🔐',
        'idle_prompt': '⏰',
        'auth_success': '✅',
        'elicitation_dialog': '❓',
    }
    return emojis.get(notification_type, 'ℹ️')


def get_friendly_title(notification_type: str) -> str:
    """
    Get user-friendly title for Claude Code notification type.

    Args:
        notification_type: Type of notification from Claude Code

    Returns:
        User-friendly title in French
    """
    titles = {
        'permission_prompt': 'Autorisation requise',
        'idle_prompt': 'Claude attend',
        'auth_success': 'Authentification réussie',
        'elicitation_dialog': 'Question',
        'error': 'Erreur',
        'warning': 'Attention',
        'info': 'Information',
        'success': 'Succès',
        'test': 'Test',
    }
    return titles.get(notification_type, notification_type.replace('_', ' ').title())
