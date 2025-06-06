from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from app.guardrails import Guardrails
from app.vector_index import DocumentIndexer
from app.llm_client import LangChainLLMClient
from langchain_openai import ChatOpenAI
from langchain_together import Together
from app.educhain import EduChain


app = FastAPI(title="Edu-Guard API")

class AskRequest(BaseModel):
    prompt: str

indexer = DocumentIndexer()
openai_llm = LangChainLLMClient(
    llm=ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4"
    )
)
# together_llm = LangChainLLMClient(
#     llm=Together(
#         together_api_key=os.getenv("TOGETHER_API_KEY"),
#         model="mistralai/Mixtral-8x7B-Instruct-v0.1"
#     )
# )
guardrails = Guardrails()
chain = EduChain(guardrails, indexer, {"openai": openai_llm})

@app.post("/ask")
async def ask_endpoint(request: AskRequest):
    try:
        result = await chain.process(request.prompt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(exc))
    return {
        "context": result.context,
        "answers": result.answers
    }
