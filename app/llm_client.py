"""
LangChainLLMClient
------------------
This class wraps a LangChain LLM object, providing a unified async interface.
"""

from dataclasses import dataclass

@dataclass
class LLMResult:
    answer: str

class LangChainLLMClient:
    """
    Generic LLM client built on top of a LangChain LLM instance.
    """

    def __init__(self, llm):
        # The llm object must implement .invoke()
        self.llm = llm

    async def ask(self, prompt: str, context: str = None) -> LLMResult:
        """
        Calls the LLM via LangChain and returns an LLMResult.
        """
        # Many LangChain LLMs are sync, so we use to_thread for async compatibility
        from asyncio import to_thread
        # Prepare input for LLMChain; real chains expect a dict, often with key 'question' or 'input'
        def call_llm():
            input_data = {"question": prompt}
            if context:
                input_data["context"] = context
            # The LLM returns a dict with at least a 'text' field (standard in LangChain)
            result = self.llm.invoke(input_data)
            return result.get("text", "")

        answer = await to_thread(call_llm)
        return LLMResult(answer=answer)
