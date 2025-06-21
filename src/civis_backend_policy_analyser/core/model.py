from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from civis_backend_policy_analyser.utils.constants import (
    AZURE_DEEPSEEK_API_KEY,
    AZURE_DEEPSEEK_ENDPOINT,
    AZURE_DEEPSEEK_MODEL,
)


def get_rag_chain(retriever=None):
    """
    Constructs a retrieval-augmented generation chain using Azure-hosted DeepSeek R1.
    """
    llm = ChatOpenAI(
        openai_api_base=AZURE_DEEPSEEK_ENDPOINT,
        openai_api_key=AZURE_DEEPSEEK_API_KEY,
        model_name=AZURE_DEEPSEEK_MODEL,
        openai_api_type="azure"
    )
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
