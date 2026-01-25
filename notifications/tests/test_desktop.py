#!/usr/bin/env python3
"""
Unit tests for desktop notification module.
Run with: python3 -m unittest test_desktop.py
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import subprocess
import json
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'hooks'))

# Import modules to test
from utils.notification.desktop import DesktopNotification
from utils.notification.icons import get_emoji_for_notification_type, get_icon_path
from utils.notification.formatters import get_session_title, format_completion_message


class TestDesktopNotification(unittest.TestCase):
    """Tests for DesktopNotification class"""

    @patch('utils.notification.desktop.subprocess.run')
    def test_is_available_when_notify_send_exists(self, mock_run):
        """Test that notification is enabled when notify-send is available"""
        mock_run.return_value = MagicMock(returncode=0)

        notif = DesktopNotification(enabled=True)

        self.assertTrue(notif.enabled)
        mock_run.assert_called_once()

    @patch('utils.notification.desktop.subprocess.run')
    def test_is_available_when_notify_send_missing(self, mock_run):
        """Test that notification is disabled when notify-send is not available"""
        mock_run.side_effect = FileNotFoundError()

        notif = DesktopNotification(enabled=True)

        self.assertFalse(notif.enabled)

    @patch('utils.notification.desktop.subprocess.run')
    def test_send_when_disabled(self, mock_run):
        """Test that send returns False when notifications are disabled"""
        notif = DesktopNotification(enabled=False)

        result = notif.send("Title", "Message")

        self.assertFalse(result)
        mock_run.assert_not_called()

    @patch('utils.notification.desktop.subprocess.run')
    def test_send_with_all_parameters(self, mock_run):
        """Test send constructs correct notify-send command"""
        # Mock both which and notify-send calls
        mock_run.side_effect = [
            MagicMock(returncode=0),  # which notify-send
            MagicMock(returncode=0)   # notify-send command
        ]

        notif = DesktopNotification(enabled=True)
        result = notif.send(
            title="Test Title",
            message="Test Message",
            urgency="critical",
            icon="dialog-error",
            timeout=3000
        )

        self.assertTrue(result)
        # Check that notify-send was called (second call)
        self.assertEqual(mock_run.call_count, 2)


class TestIcons(unittest.TestCase):
    """Tests for icon functions"""

    def test_get_icon_path_success(self):
        """Test getting icon for success status"""
        icon = get_icon_path('success')
        self.assertEqual(icon, 'dialog-information')

    def test_get_icon_path_error(self):
        """Test getting icon for error status"""
        icon = get_icon_path('error')
        self.assertEqual(icon, 'dialog-error')

    def test_get_icon_path_unknown(self):
        """Test getting icon for unknown status returns default"""
        icon = get_icon_path('unknown')
        self.assertEqual(icon, 'dialog-information')

    def test_get_emoji_permission_prompt(self):
        """Test emoji for permission_prompt notification"""
        emoji = get_emoji_for_notification_type('permission_prompt')
        self.assertEqual(emoji, '🔐')

    def test_get_emoji_idle_prompt(self):
        """Test emoji for idle_prompt notification"""
        emoji = get_emoji_for_notification_type('idle_prompt')
        self.assertEqual(emoji, '⏰')

    def test_get_emoji_auth_success(self):
        """Test emoji for auth_success notification"""
        emoji = get_emoji_for_notification_type('auth_success')
        self.assertEqual(emoji, '✅')

    def test_get_emoji_elicitation_dialog(self):
        """Test emoji for elicitation_dialog notification"""
        emoji = get_emoji_for_notification_type('elicitation_dialog')
        self.assertEqual(emoji, '❓')

    def test_get_emoji_unknown(self):
        """Test emoji for unknown notification type returns default"""
        emoji = get_emoji_for_notification_type('unknown')
        self.assertEqual(emoji, 'ℹ️')


class TestFormatters(unittest.TestCase):
    """Tests for formatter functions"""

    @patch('utils.notification.formatters.Path')
    def test_get_session_title_when_file_not_exists(self, mock_path):
        """Test get_session_title returns None when sessions-index.json doesn't exist"""
        mock_path.home.return_value = Path('/home/user')
        mock_sessions_index = MagicMock()
        mock_sessions_index.exists.return_value = False
        mock_path.home.return_value.__truediv__.return_value = mock_sessions_index

        title = get_session_title('abc123', '/home/user/project')

        self.assertIsNone(title)

    @patch('builtins.open', new_callable=mock_open, read_data='{"entries": [{"sessionId": "abc123", "summary": "Test Session"}]}')
    @patch('utils.notification.formatters.Path')
    def test_get_session_title_when_session_found(self, mock_path, mock_file):
        """Test get_session_title returns title when session is found"""
        mock_path.home.return_value = Path('/home/user')
        mock_sessions_index = MagicMock()
        mock_sessions_index.exists.return_value = True
        mock_path.home.return_value.__truediv__.return_value = mock_sessions_index

        title = get_session_title('abc123', '/home/user/project')

        self.assertEqual(title, 'Test Session')

    def test_format_completion_message_without_session_title(self):
        """Test format_completion_message returns generic title when no session title"""
        title, body = format_completion_message('abc12345', 42.5, '')

        self.assertEqual(title, '✅ Claude Code - Tâche terminée')
        self.assertIn('abc12345', body)
        self.assertIn('42.5s', body)

    @patch('utils.notification.formatters.get_session_title')
    def test_format_completion_message_with_session_title(self, mock_get_title):
        """Test format_completion_message uses session title when available"""
        mock_get_title.return_value = 'My Custom Task'

        title, body = format_completion_message('abc123', 30.0, '/home/user/project')

        self.assertEqual(title, '✅ My Custom Task')
        self.assertEqual(body, 'Durée: 30.0s')


if __name__ == '__main__':
    unittest.main()
