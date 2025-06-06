"""
LangChainLLMClient
------------------
Wraps a LangChain LLM object, providing a unified async interface.
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
        # The llm object must implement .invoke(input_str: str)
        # and return some kind of response that has either:
        #  - a .content attribute, OR
        #  - a .generations list (where each generation has .text or .content), OR
        #  - a dict containing "content" or "text" keys.
        self.llm = llm

    async def ask(self, prompt: str, context: str = None) -> LLMResult:
        """
        Calls the LLM via LangChain and returns an LLMResult.
        We concatenate "context" + "user prompt" into a single string,
        because ChatOpenAI.invoke() expects a str (or list of BaseMessage).
        """
        from asyncio import to_thread

        def call_llm():
            # Build a single textual prompt by appending context, if any.
            if context:
                full_prompt = f"Context:\n{context.strip()}\n\nQuestion:\n{prompt.strip()}"
            else:
                full_prompt = prompt.strip()

            # Call the underlying LangChain LLM’s .invoke() with a plain string.
            response = self.llm.invoke(full_prompt)

            # 1) If the response is a dict, check for "content" or "text":
            if isinstance(response, dict):
                if "content" in response:
                    return response["content"]
                if "text" in response:
                    return response["text"]
                # Fallback to the full dict as string
                return str(response)

            # 2) If the response has a .content attribute (e.g., ChatGeneration):
            if hasattr(response, "content"):
                try:
                    return response.content
                except Exception:
                    # In rare cases, content might be a method or other; cast to str
                    return str(response.content)

            # 3) If the response has a .generations attribute (list of GenerationResult):
            #    We pick the first generation’s text/content.
            if hasattr(response, "generations"):
                gens = response.generations
                if isinstance(gens, list) and len(gens) > 0:
                    first = gens[0]
                    # A generation may have .text or .content
                    if hasattr(first, "text"):
                        return first.text
                    if hasattr(first, "content"):
                        return first.content
                    # Fallback:
                    return str(first)

            # 4) As a last resort, convert entire response to string:
            return str(response)

        # Run the (synchronous) call_llm in a background thread:
        answer_text = await to_thread(call_llm)
        return LLMResult(answer=answer_text)
