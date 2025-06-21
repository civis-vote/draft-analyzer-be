import os

from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings

from civis_backend_policy_analyser.utils.constants import (
    DB_BASE_URL, VECTOR_DRIVER, AZURE_DEEPSEEK_MODEL
)


class VectorDB:
    """
    VectorDB handles async vector storage and deletion using PGVector.

    Methods:
        store(doc_id, texts): Embeds and stores text chunks
        delete(doc_id): Removes stored entries for a given document ID
    """

    def __init__(self, document_id):
        """
        As master data is store in Postgres. Using a PostgreSQL extension here as pgvector.
        This enables storing and querying vectors.

        Args:
            document_id (str): Unique identifier for the document
        """
        connection_string = DB_BASE_URL.format(driver_name=VECTOR_DRIVER)
        embeddings = OpenAIEmbeddings(model=AZURE_DEEPSEEK_MODEL)

        self._store = PGVector(
            embedding_function=embeddings,
            collection_name=f"CIVIS_DRAFT_ANALYSER_{document_id}",
            connection_string=connection_string,
            async_mode=True,
            use_jsonb=True,
        )
        self.retriever = self.__get_retriever(document_id)
        self.document_id = document_id

    def __get_retriever(self, document_id):
        return self._store.as_retriever(
            search_kwargs={"k": 5, "filter": {"document_id": document_id}}
        )

    def store_embedding(self, chunks):
        """
        Stores text embeddings in the vector database under a document namespace.

        TODO: Need to integrate Task Queues like, Celery, Redis or Dramatiq in the backend.

        Args:
            
            chunks (list): Multiple sub sets of document data, to embed in vector store.
        """
        ids = [f"{self.document_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"document_id": self.document_id} for _ in chunks]
        self._store.add_texts(chunks, metadatas=metadatas, ids=ids)

    def delete_all_vectors(self):
        """
        Deletes all vectors corresponding to a document ID prefix.
        """
        all_ids = [id for id in self._store.get_ids() if id.startswith(self.document_id)]
        self.store.delete(ids=all_ids)
