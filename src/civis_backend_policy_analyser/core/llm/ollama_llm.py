from langchain_community.chat_models import ChatOllama
from civis_backend_policy_analyser.core.llm.base_llm import BaseLLMModel

class OllamaLLMModel(BaseLLMModel):
    def get_llm(self):
        return ChatOllama(model="deepseek-r1:1.5b")
