from typing import Any

from langchain.chains import RetrievalQA
from langchain.vectorstores.faiss import FAISS
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from pydantic import BaseModel
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema.embeddings import Embeddings
from prompt import prompt
from logger import LOGGER as logger


class BookConsultant:
    """Book Consultant
        Reply customer's any question about the book
    """
    llm: BaseLanguageModel

    def __init__(self, llm: BaseLanguageModel = None, embedding: Embeddings = None) -> None:
        self.llm = llm if llm is not None else OpenAI(temperature=0)
        _embedding = embedding if embedding is not None else OpenAIEmbeddings()

        self.db = FAISS.load_local('../jupyter/books', _embedding)
        self.retriever = self.db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.7, "k": 3})
        self.consultant = RetrievalQA.from_chain_type(llm=self.llm, retriever=self.retriever, verbose=True)
        self.consultant.combine_documents_chain.verbose = True
        self.consultant.return_source_documents = True
        # TODO 根据配置选择是否需要修改 prompt 模板
        self.consultant.combine_documents_chain.llm_chain.prompt = prompt

    def ask(self, question):
        logger.info(f"question: {question}")
        reply = self.consultant(question)
        logger.info(f"reply: {reply}")
        return reply["result"]


CONSULTANT = BookConsultant()

if __name__ == '__main__':
    consultant = BookConsultant()
    reply_result = consultant.ask("你这里有 Python 的书吗？")
    logger.info(f"reply result: {reply_result}")
