#!/usr/bin/env python3
"""
Base notification backend interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class NotificationBackend(ABC):
    """
    Abstract base class for notification backends.

    All notification backends must implement this interface.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize backend with configuration.

        Args:
            config: Backend-specific configuration
        """
        self.config = config or {}

    @abstractmethod
    def send(self, data: 'NotificationData') -> bool:
        """
        Send a notification.

        Args:
            data: NotificationData instance

        Returns:
            True if sent successfully, False otherwise
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this backend is available on the system.

        Returns:
            True if available, False otherwise
        """
        pass

    def get_name(self) -> str:
        """
        Get backend name.

        Returns:
            Backend name (e.g., 'zenity', 'notify-send')
        """
        return self.__class__.__name__.replace('Backend', '').lower()
