#!/usr/bin/env python3
"""
Desktop notification module for Claude Code hooks.
Sends notifications using notify-send (Linux).
"""

import subprocess
import os
from typing import Optional


class DesktopNotification:
    """Send desktop notifications using notify-send (Linux)."""

    def __init__(self, enabled: bool = True):
        """
        Initialize desktop notification handler.

        Args:
            enabled: Whether notifications are enabled
        """
        self.enabled = enabled and self._is_available()

    def _is_available(self) -> bool:
        """
        Check if notify-send is available on the system.

        Returns:
            True if notify-send is available, False otherwise
        """
        try:
            subprocess.run(
                ['which', 'notify-send'],
                capture_output=True,
                check=True,
                timeout=5
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def send(
        self,
        title: str,
        message: str,
        urgency: str = 'normal',
        icon: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Send a desktop notification.

        Args:
            title: Notification title
            message: Notification body/message
            urgency: Urgency level ('low', 'normal', 'critical')
            icon: Icon name or path (e.g., 'dialog-information', 'dialog-error')
            timeout: Timeout in milliseconds (0 = default, -1 = never expire)
                     If None, reads from CLAUDE_DESKTOP_NOTIFY_TIMEOUT env var (default: -1)

        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not self.enabled:
            return False

        try:
            # Read urgency from env if not overridden
            if urgency == 'normal':
                urgency = os.getenv('CLAUDE_DESKTOP_NOTIFY_URGENCY', 'normal')

            # Read timeout from env if not provided (default: -1 = permanent)
            if timeout is None:
                timeout = int(os.getenv('CLAUDE_DESKTOP_NOTIFY_TIMEOUT', '-1'))

            # Build notify-send command
            cmd = ['notify-send']

            # Add urgency
            if urgency in ('low', 'normal', 'critical'):
                cmd.extend(['--urgency', urgency])

            # Add icon
            if icon:
                cmd.extend(['--icon', icon])

            # Add timeout (-1 = permanent, 0 = default, >0 = milliseconds)
            cmd.extend(['--expire-time', str(timeout)])

            # Add title and message
            cmd.append(title)
            cmd.append(message)

            # Execute notification
            subprocess.run(
                cmd,
                capture_output=True,
                timeout=10
            )
            return True

        except (subprocess.SubprocessError, subprocess.TimeoutExpired, FileNotFoundError):
            # Fail silently
            return False
