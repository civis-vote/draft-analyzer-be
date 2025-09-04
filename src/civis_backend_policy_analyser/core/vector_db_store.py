import os
import tracemalloc
from civis_backend_policy_analyser.config.logging_config import logger
from sqlalchemy.ext.asyncio import create_async_engine

from langchain_postgres.vectorstores import PGVector
from langchain_openai import AzureOpenAIEmbeddings

from civis_backend_policy_analyser.core.embeddings.base_embedding import BaseEmbeddingModel
from civis_backend_policy_analyser.utils.constants import (
    VECTOR_CONNECTION_STRING
)


tracemalloc.start()


class VectorDB:
    """
    VectorDB handles async vector storage and deletion using PGVector.

    Methods:
        store(doc_id, texts): Embeds and stores text chunks
        delete(doc_id): Removes stored entries for a given document ID
    """

    def __init__(self, document_id, embedding_model: BaseEmbeddingModel):
        embedding = embedding_model.get_embedding_model()
        self._store = PGVector(
            embeddings=embedding,
            collection_name=f"CIVIS_DRAFT_ANALYSER_{document_id}",
            connection=VECTOR_CONNECTION_STRING,
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
        logger.info(f"{self.document_id}: Storing total {len(chunks)} embeddings with metadata.")
        result = self._store.add_texts(texts=chunks, metadatas=metadatas, ids=ids)
        return result

    def delete_all_vectors(self):
        """
        Deletes all vectors corresponding to a document ID prefix.
        """
        all_ids = [id for id in self._store.get_ids() if id.startswith(self.document_id)]
        self.store.delete(ids=all_ids)