"""
Guardrails class for moderation.
This class wraps a moderation backend (for example, OpenAI Moderation API)
but can be used with any client implementing `moderate(text)`.
"""

from dataclasses import dataclass

@dataclass
class ModerationResult:
    is_safe: bool
    reason: str = ""

class Guardrails:
    """
    Main moderation entry point. Takes any moderation client (real or fake).
    """

    def __init__(self, client):
        # The moderation client must have an async moderate(text) method.
        self.client = client

    async def moderate(self, text: str) -> ModerationResult:
        """
        Returns ModerationResult with is_safe (bool) and reason (str).
        """
        return await self.client.moderate(text)
