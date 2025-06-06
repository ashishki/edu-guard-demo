"""
Tests for LangChainLLMClient — LLM interface built on top of LangChain.
We'll use a fake (mocked) LangChain LLM for testing.
"""

import pytest
from app.llm_client import LangChainLLMClient, LLMResult

class FakeLangChainLLM:
    """A mock LLM for unit testing."""
    def __init__(self, answer):
        self._answer = answer

    def invoke(self, input, **kwargs):
        # Simulate LangChain's LLMChain.invoke({"question": ...})
        return {"text": self._answer}

@pytest.mark.asyncio
async def test_langchain_llmclient_returns_answer():
    """
    LangChainLLMClient should return a string answer from the underlying LLM.
    """
    fake_llm = FakeLangChainLLM(answer="This is a test answer.")
    client = LangChainLLMClient(llm=fake_llm)
    result = await client.ask("What is the meaning of life?", context="philosophy")
    assert isinstance(result, LLMResult)
    assert result.answer == "This is a test answer."
