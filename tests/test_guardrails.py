"""
This module tests the Guardrails moderation class.
We start by using a fake moderation backend (no real API calls).
"""

import pytest
from app.guardrails import Guardrails, ModerationResult

class FakeModerationClient:
    """A simple fake moderation backend for unit tests."""
    def __init__(self, flagged=False, reason=""):
        self.flagged = flagged
        self.reason = reason

    async def moderate(self, text):
        # Always returns a ModerationResult with preset values
        return ModerationResult(is_safe=not self.flagged, reason=self.reason)

@pytest.mark.asyncio
async def test_moderate_safe_text():
    """
    If the moderation backend returns flagged=False,
    Guardrails should allow the text (is_safe == True).
    """
    guardrails = Guardrails(client=FakeModerationClient(flagged=False))
    result = await guardrails.moderate("Hello, world!")
    assert result.is_safe
    assert result.reason == ""

@pytest.mark.asyncio
async def test_moderate_blocked_text():
    """
    If the moderation backend returns flagged=True,
    Guardrails should block the text (is_safe == False).
    """
    guardrails = Guardrails(client=FakeModerationClient(flagged=True, reason="hate"))
    result = await guardrails.moderate("Some very bad text")
    assert not result.is_safe
    assert result.reason == "hate"
