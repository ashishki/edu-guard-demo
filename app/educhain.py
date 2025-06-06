"""
EduChain — main orchestrator class.
Combines guardrails, document retrieval, and LLM answer into a single pipeline.
"""

from dataclasses import dataclass

@dataclass
class EduChainResult:
    context: str
    answer: str

class EduChain:
    def __init__(self, guardrails, indexer, llm_client):
        self.guardrails = guardrails
        self.indexer = indexer
        self.llm_client = llm_client

    async def process(self, prompt: str) -> EduChainResult:
        """
        1. Moderates the prompt.
        2. If allowed, retrieves context.
        3. Passes prompt + context to LLM.
        4. Returns EduChainResult (context + answer).
        """
        moderation = await self.guardrails.moderate(prompt)
        if not moderation.is_safe:
            raise ValueError(f"Blocked by guardrails: {moderation.reason}")
        context = await self.indexer.retrieve(prompt)
        llm_result = await self.llm_client.ask(prompt, context=context)
        return EduChainResult(context=context, answer=llm_result.answer)
