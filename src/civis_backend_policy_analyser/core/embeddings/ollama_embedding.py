from langchain_community.embeddings import OllamaEmbeddings
from civis_backend_policy_analyser.core.embeddings.base_embedding import BaseEmbeddingModel

class OllamaEmbeddingModel(BaseEmbeddingModel):
    def get_embedding_model(self):
        return OllamaEmbeddings(model="nomic-embed-text")
