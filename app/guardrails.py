"""
guardrails.py
-------------
Handles content moderation. If no custom client is provided,
it uses OpenAI’s Moderation API by default.
"""

import os
import httpx
from dataclasses import dataclass
from dotenv import load_dotenv

# Ensure .env is loaded (so that OPENAI_API_KEY is in os.environ)
load_dotenv()


@dataclass
class ModerationResult:
    """
    Simple data structure to hold moderation outcome:
    - is_safe: True if content is allowed; False otherwise.
    - reason: Optional string explaining why it was blocked.
    """
    is_safe: bool
    reason: str = ""


class OpenAIModerationClient:
    """
    Real OpenAI moderation client. Uses the OpenAI Moderation API
    to check for disallowed content.
    """
    def __init__(self, api_key: str | None = None):
        # If no api_key is explicitly passed, read from environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    async def moderate(self, text: str) -> ModerationResult:
        """
        Calls OpenAI’s /v1/moderations endpoint.
        Returns a ModerationResult, indicating whether the text is allowed.
        """
        if not self.api_key:
            # If no API key is found, treat everything as “safe”
            return ModerationResult(is_safe=True, reason="No API key; skipped moderation")

        url = "https://api.openai.com/v1/moderations"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"input": text}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=10)
            if response.status_code != 200:
                # If moderation service fails, default to “safe”
                return ModerationResult(is_safe=True, reason="Moderation API error")

            result = response.json()
            flagged = result["results"][0]["flagged"]
            if flagged:
                # Collect any flagged categories (e.g. “hate” or “violence”)
                categories = result["results"][0]["categories"]
                reason_list = [cat for cat, was_flagged in categories.items() if was_flagged]
                reason = ", ".join(reason_list) if reason_list else "flagged"
                return ModerationResult(is_safe=False, reason=reason)

            return ModerationResult(is_safe=True, reason="")


class Guardrails:
    """
    Main moderation wrapper. If no client is provided, it creates
    an OpenAIModerationClient internally.
    """
    def __init__(self, client: OpenAIModerationClient | None = None):
        # If no custom client is passed, use the OpenAI‐based moderation client
        self.client = client or OpenAIModerationClient()

    async def moderate(self, text: str) -> ModerationResult:
        """
        Delegate moderation to the underlying client.
        """
        return await self.client.moderate(text)
