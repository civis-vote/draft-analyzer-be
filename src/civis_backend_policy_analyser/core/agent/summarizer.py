from civis_backend_policy_analyser.core.model import get_rag_chain
from civis_backend_policy_analyser.decorator.log_execution_time import log_execution_time

class DocumentSummarizer:
    def __init__(self, retriever, llm_model):
        self.llm_model = llm_model
        self.retriever = retriever

    @log_execution_time
    async def summarize(self, prompt):
        rag_chain = get_rag_chain(retriever=self.retriever, llm_model=self.llm_model)
        result = await rag_chain.ainvoke(prompt)
        return result["result"]

    @log_execution_time
    async def assess(self, prompts, expected_format_instructions=""):
        rag_chain = get_rag_chain(retriever=self.retriever, llm_model=self.llm_model)
        queries = [{"query": expected_format_instructions.strip() + "\n" + item["query"]} for item in prompts]
        results = await rag_chain.abatch(queries)
        return [result["result"] for result in results]
