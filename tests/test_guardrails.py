"""
Guardrails class for moderation.
Provides both real and fake moderation for flexibility.
"""

from dataclasses import dataclass
import os
import httpx

@dataclass
class ModerationResult:
    is_safe: bool
    reason: str = ""

class OpenAIModerationClient:
    """
    Real moderation backend using OpenAI Moderation API.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    async def moderate(self, text):
        if not self.api_key:
            # Allow all if no API key (for dev)
            return ModerationResult(is_safe=True, reason="")
        url = "https://api.openai.com/v1/moderations"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"input": text}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data, timeout=10)
            if resp.status_code != 200:
                return ModerationResult(is_safe=True, reason="Moderation API error")
            result = resp.json()
            flagged = result["results"][0]["flagged"]
            if flagged:
                # Возьмём первую причину, если есть
                categories = result["results"][0]["categories"]
                reason = ", ".join([k for k, v in categories.items() if v]) or "flagged"
                return ModerationResult(is_safe=False, reason=reason)
            return ModerationResult(is_safe=True, reason="")

class Guardrails:
    """
    Main moderation entry point. By default uses OpenAI Moderation.
    """
    def __init__(self, client=None):
        self.client = client or OpenAIModerationClient()

    async def moderate(self, text: str) -> ModerationResult:
        return await self.client.moderate(text)
