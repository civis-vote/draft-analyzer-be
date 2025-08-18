from civis_backend_policy_analyser.core.vector_db_store import VectorDB


class DocumentVectorStore:
    def __init__(self, document_id, embedding_model):
        self.vector_store = VectorDB(document_id, embedding_model)

    def store_embedding(self, chunks):
        self.vector_store.store_embedding(chunks)

    def delete_all_vectors(self):
        self.vector_store.delete_all_vectors()

    @property
    def retriever(self):
        return self.vector_store.retriever