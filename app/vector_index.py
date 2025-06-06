"""
DocumentIndexer
---------------
Builds and manages a semantic vector index with Chroma and LlamaIndex 0.12.x.
Updated for new import structure and API changes.
"""
import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore


class DocumentIndexer:
    def __init__(self, data_dir=None, persist_dir=None):
        # Directory containing .txt files to index
        self.data_dir = data_dir or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data")
        )
        # Directory where Chroma and LlamaIndex will store files
        self.persist_dir = persist_dir or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "chroma_db")
        )
        # Build or load the index upon initialization
        self.index = self._build_or_load_index()

    def _build_or_load_index(self):
        # Create the persistence directory if it doesn't exist
        if not os.path.exists(self.persist_dir):
            os.makedirs(self.persist_dir, exist_ok=True)

        # Initialize a persistent Chroma client
        chroma_client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Try to get existing collection or create new one
        try:
            chroma_collection = chroma_client.get_collection(name="edu_docs")
        except Exception:
            chroma_collection = chroma_client.create_collection(name="edu_docs")

        # Wrap that Chroma collection for LlamaIndex
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Try to load an existing index
        try:
            # Check if we have documents in the collection
            if chroma_collection.count() > 0:
                # Load from existing vector store
                index = VectorStoreIndex.from_vector_store(
                    vector_store=vector_store,
                    storage_context=storage_context
                )
            else:
                raise Exception("No documents in collection")
        except Exception:
            # If no index exists yet, build a new one from the .txt files
            docs = SimpleDirectoryReader(self.data_dir).load_data()
            index = VectorStoreIndex.from_documents(
                docs,
                storage_context=storage_context
            )

        return index

    async def retrieve(self, question: str) -> str:
        """
        Asynchronously query the index to retrieve the most relevant context.
        Since `index.as_query_engine().query(...)` is synchronous, we wrap it in to_thread.
        """
        from asyncio import to_thread

        def search():
            engine = self.index.as_query_engine()
            response = engine.query(question)
            return str(response)

        return await to_thread(search)

    def get_retriever(self):
        """
        Return a retriever object from LlamaIndex.
        This is useful if you want to plug it into other pipelines.
        """
        return self.index.as_retriever()