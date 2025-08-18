from langchain_openai import AzureChatOpenAI

from civis_backend_policy_analyser.core.llm.base_llm import BaseLLMModel
from civis_backend_policy_analyser.utils.constants import (
    AZURE_DEEPSEEK_API_KEY,
    AZURE_DEEPSEEK_ENDPOINT,
    AZURE_DEEPSEEK_MODEL,
    AZURE_OPENAI_API_VERSION,
)


class AzureLLMModel(BaseLLMModel):
    def get_llm(self):
        return AzureChatOpenAI(
            azure_endpoint=AZURE_DEEPSEEK_ENDPOINT,
            api_key=AZURE_DEEPSEEK_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            deployment_name=AZURE_DEEPSEEK_MODEL
        )
