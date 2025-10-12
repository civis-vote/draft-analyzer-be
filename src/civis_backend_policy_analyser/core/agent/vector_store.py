from civis_backend_policy_analyser.core.vector_db_store import VectorDB

class DocumentVectorStore:
    def __init__(self, document_id, embedding_model):
        self.vector_store = VectorDB(document_id, embedding_model)

    async def store_embedding(self, chunks):
        await self.vector_store.store_embedding(chunks)

    async def delete_all_vectors(self):
        await self.vector_store.delete_all_vectors()

    @property
    def retriever(self):
        return self.vector_store.retriever