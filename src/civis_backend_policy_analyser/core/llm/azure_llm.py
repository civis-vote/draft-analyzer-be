from langchain_openai import ChatOpenAI
from civis_backend_policy_analyser.core.llm.base_llm import BaseLLMModel
from civis_backend_policy_analyser.utils.constants import AZURE_DEEPSEEK_MODEL, AZURE_DEEPSEEK_API_KEY, AZURE_DEEPSEEK_ENDPOINT

class AzureLLMModel(BaseLLMModel):
    def get_llm(self):
        return ChatOpenAI(
            openai_api_base=AZURE_DEEPSEEK_ENDPOINT,
            openai_api_key=AZURE_DEEPSEEK_API_KEY,
            model_name=AZURE_DEEPSEEK_MODEL,
            model_kwargs=dict(openai_api_type="azure"),
        )
