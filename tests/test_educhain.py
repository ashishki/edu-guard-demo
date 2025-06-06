"""
Unit test for EduChain — pipeline class combining guardrails, retrieval, and LLM.
"""

import pytest
from app.educhain import EduChain, EduChainResult

class FakeGuardrails:
    def __init__(self, is_safe=True, reason=""):
        self._is_safe = is_safe
        self._reason = reason
    async def moderate(self, prompt):
        return type('ModerationResult', (), {
            "is_safe": self._is_safe,
            "reason": self._reason
        })()

class FakeIndexer:
    def __init__(self, context):
        self._context = context
    async def retrieve(self, question):
        return self._context

class FakeLLMClient:
    def __init__(self, answer):
        self._answer = answer
    async def ask(self, prompt, context=None):
        return type('LLMResult', (), {"answer": self._answer})()

@pytest.mark.asyncio
async def test_educhain_allows_and_responds():
    """
    EduChain should allow safe prompts, retrieve context, and get LLM answer.
    """
    guardrails = FakeGuardrails(is_safe=True)
    indexer = FakeIndexer(context="relevant context")
    llm = FakeLLMClient(answer="42 is the answer")
    chain = EduChain(guardrails, indexer, llm)
    result = await chain.process("What is the answer?")
    assert isinstance(result, EduChainResult)
    assert result.context == "relevant context"
    assert result.answer == "42 is the answer"

@pytest.mark.asyncio
async def test_educhain_blocks_unsafe_prompt():
    """
    EduChain should block unsafe prompts and raise ValueError.
    """
    guardrails = FakeGuardrails(is_safe=False, reason="hate")
    indexer = FakeIndexer(context="irrelevant")
    llm = FakeLLMClient(answer="should not be called")
    chain = EduChain(guardrails, indexer, llm)
    with pytest.raises(ValueError) as excinfo:
        await chain.process("some unsafe prompt")
    assert "Blocked by guardrails: hate" in str(excinfo.value)
