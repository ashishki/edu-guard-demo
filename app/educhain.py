"""
EduChain (LangChain version)
----------------------------
Pipeline: Guardrails → Retriever → MultiLLM → Results
"""

from dataclasses import dataclass

@dataclass
class EduChainMultiResult:
    context: str
    answers: dict   # {"model_name": "answer"}

class EduChain:
    def __init__(self, guardrails, indexer, llm_clients: dict):
        self.guardrails = guardrails
        self.indexer = indexer
        self.llm_clients = llm_clients  # {"openai": llm, "together": llm, ...}

    async def process(self, prompt: str) -> EduChainMultiResult:
        """
        1. Moderates prompt.
        2. Retrieves context.
        3. Asks all LLMs in parallel.
        """
        moderation = await self.guardrails.moderate(prompt)
        if not moderation.is_safe:
            raise ValueError(f"Blocked by guardrails: {moderation.reason}")

        context = await self.indexer.retrieve(prompt)
        
        # Query all LLMs in parallel, passing context
        import asyncio
        async def ask_llm(name, client):
            result = await client.ask(prompt, context=context)
            return (name, result.answer)
        answers = dict(await asyncio.gather(
            *(ask_llm(name, client) for name, client in self.llm_clients.items())
        ))
        return EduChainMultiResult(context=context, answers=answers)
