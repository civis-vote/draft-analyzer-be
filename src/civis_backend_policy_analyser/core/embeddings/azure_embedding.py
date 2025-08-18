from langchain_openai import AzureOpenAIEmbeddings

from civis_backend_policy_analyser.core.embeddings.base_embedding import (
    BaseEmbeddingModel,
)
from civis_backend_policy_analyser.utils.constants import (
    AZURE_DEEPSEEK_API_KEY,
    AZURE_DEEPSEEK_DEPLOYMENT_NAME,
    AZURE_DEEPSEEK_ENDPOINT,
)


class AzureEmbeddingModel(BaseEmbeddingModel):
    def get_embedding_model(self):
        return AzureOpenAIEmbeddings(
            model=AZURE_DEEPSEEK_DEPLOYMENT_NAME,
            api_key=AZURE_DEEPSEEK_API_KEY,
            azure_endpoint=AZURE_DEEPSEEK_ENDPOINT,
            azure_deployment=AZURE_DEEPSEEK_DEPLOYMENT_NAME,
        )
