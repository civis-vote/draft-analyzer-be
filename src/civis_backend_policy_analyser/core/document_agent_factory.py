from enum import Enum

from civis_backend_policy_analyser.core.document_agent import DocumentAgent
from civis_backend_policy_analyser.core.embeddings.azure_embedding import (
    AzureEmbeddingModel,
)
from civis_backend_policy_analyser.core.embeddings.ollama_embedding import (
    OllamaEmbeddingModel,
)
from civis_backend_policy_analyser.core.llm.azure_llm import AzureLLMModel
from civis_backend_policy_analyser.core.llm.ollama_llm import OllamaLLMModel


class LLMClient(str, Enum):
    OLLAMA = "ollama"
    AZURE = "azure"


def create_document_agent(client: LLMClient, document_id=None) -> DocumentAgent:
    if client == LLMClient.AZURE:
        embedding_model = AzureEmbeddingModel()
        llm_model = AzureLLMModel()
    elif client == LLMClient.OLLAMA:
        embedding_model = OllamaEmbeddingModel()
        llm_model = OllamaLLMModel()
    else:
        raise ValueError(f"Unsupported LLM client: {client}")
    
    return DocumentAgent(embedding_model=embedding_model, llm_model=llm_model, document_id=document_id)
