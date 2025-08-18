from civis_backend_policy_analyser.core.model import get_rag_chain


class DocumentSummarizer:
    def __init__(self, retriever, llm_model):
        self.rag_chain = get_rag_chain(retriever=retriever, llm_model=llm_model)

    def summarize(self, prompt):
        return self.rag_chain.run(prompt)

    def assess(self, prompts, expected_format_instructions=""):
        queries = [{"query": expected_format_instructions.strip() + "\n" + item["query"]} for item in prompts]
        return self.rag_chain.batch(queries)
        