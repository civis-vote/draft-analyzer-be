from langchain.chains import RetrievalQA
from civis_backend_policy_analyser.core.llm.base_llm import BaseLLMModel


def get_rag_chain(retriever, llm_model: BaseLLMModel):
    llm = llm_model.get_llm()
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)