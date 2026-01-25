#!/usr/bin/env python3
"""
Notification data structure.
"""

from datetime import datetime
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class NotificationData:
    """
    Structured notification data.

    This is the common format used across all notification backends.
    """

    # Core fields
    emoji: str
    type: str
    message: str
    project_name: str

    # Optional fields
    session_title: Optional[str] = None
    priority: str = 'normal'
    timestamp: Optional[str] = None

    # Metadata
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NotificationData':
        """Create from dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'NotificationData':
        """Create from JSON string."""
        import json
        return cls.from_dict(json.loads(json_str))

    def get_title(self) -> str:
        """Get notification title."""
        return f"{self.emoji} {self.project_name}"

    def get_body(self) -> str:
        """Get notification body."""
        if self.session_title:
            return f"{self.message}\n{self.session_title}"
        return self.message

    def get_short_title(self) -> str:
        """Get short title (for compact display)."""
        return f"{self.emoji} {self.type}"
