import pytest
from app.vector_index import DocumentIndexer

class FakeLlamaIndex:
    def __init__(self, search_result):
        self._search_result = search_result

    def search(self, query):
        return self._search_result

@pytest.mark.asyncio
async def test_document_indexer_retrieves_context():
    """DocumentIndexer should return relevant context as string."""
    fake_index = FakeLlamaIndex(search_result="context from docs")
    indexer = DocumentIndexer(index=fake_index)
    result = await indexer.retrieve("What is Python?")
    assert isinstance(result, str)
    assert result == "context from docs"

