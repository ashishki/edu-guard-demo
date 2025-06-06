"""
DocumentIndexer
---------------
This class builds and manages a document index for retrieval.
"""

class DocumentIndexer:
    """
    Handles document indexing and retrieval.
    """

    def __init__(self, index=None):
        # If no index is passed, should build one (in real code).
        self.index = index

    async def retrieve(self, question: str) -> str:
        """
        Retrieves context for a question from the index.
        """
        # For now, just call .search() of the index (synchronously, for test)
        return self.index.search(question)
