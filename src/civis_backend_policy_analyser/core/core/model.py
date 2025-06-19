from langchain_deepseek import ChatDeepSeek
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate



llm = ChatDeepSeek(model="deepseek-reasoner")


def get_rag_chain(retriever):
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


def ask_deepseek(prompt, content):
    template = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ])
    return llm.invoke(template.format_messages(input=content))
