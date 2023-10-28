from typing import Literal

from utils import logger
from prompt import prompt
from pydantic.v1 import BaseModel
from langchain.chains import RetrievalQA
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema.embeddings import Embeddings
from langchain.schema.runnable import Runnable, RunnablePassthrough
from langchain.output_parsers.openai_functions import PydanticAttrOutputFunctionsParser
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.schema.runnable import RunnableBranch, RunnableLambda, RunnablePassthrough
from operator import itemgetter


class BookConsultant:
    """Book Consultant
        1. Reply customer's any question about the book
        2. Help customer to shopping.eg, add book to shopping cart,
            delete book from shopping cart, view inventory, checkout
    """
    llm: BaseLanguageModel

    def __init__(self, llm: BaseLanguageModel = None, embedding: Embeddings = None) -> None:
        qa = self._qa_chain(llm, embedding=embedding)
        # self.shoppingcart_chain = self._shoppingcart_chain()
        self.full_chain = self.build_fullchain(qa)

    def build_fullchain(self, qa: Runnable):
        classifier_function = convert_pydantic_to_openai_function(TopicClassifier)
        llm = ChatOpenAI(temperature=0).bind(functions=[classifier_function], function_call={"name": "TopicClassifier"})
        parser = PydanticAttrOutputFunctionsParser(pydantic_schema=TopicClassifier, attr_name="topic")
        classifier_chain = llm | parser

        chain_branch = RunnableBranch(
            (lambda p: p['topic'] == "qa", qa),
            (lambda p: p['topic'] == "shopping",
             RunnablePassthrough.assign(result=lambda x: '购物车功能还在抓紧开发中，敬请期待！')),
            lambda x: x
        )

        full_chain = (
                RunnablePassthrough.assign(topic=itemgetter('query') | classifier_chain)
                | chain_branch
        )
        return full_chain

    def _qa_chain(self, llm: BaseLanguageModel = None, embedding: Embeddings = None) -> Runnable:
        _embedding = embedding if embedding is not None else OpenAIEmbeddings()

        db = FAISS.load_local('../jupyter/books', _embedding)
        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.7, "k": 3})
        llm = llm if llm is not None else ChatOpenAI(temperature=0)
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, verbose=True)
        qa.combine_documents_chain.verbose = True
        qa.return_source_documents = True
        # TODO 根据配置选择是否需要修改 prompt 模板
        qa.combine_documents_chain.llm_chain.prompt = prompt

        return qa

    def _shoppingcart_chain(self) -> Runnable:
        # return RunnablePassthrough.assign(result=lambda x: '购物车功能还在抓紧开发中，敬请期待！')
        # TODO 购物车功能还在抓紧开发中，敬请期待！
        pass

    def ask(self, question: str):
        logger.info(f"question: {question}")

        reply = self.full_chain.invoke({"query": question})
        logger.info(f"reply: {reply}")
        return reply["result"]


class TopicClassifier(BaseModel):
    """Classify the topic of the user question
    qa: Reply to user inquiries for books and provide some purchasing suggestions
    shopping: Assist customers in managing their shopping cart, including services such as adding products, deleting products, viewing inventory, and settling accounts
    """

    topic: Literal["qa", "shopping"]
    """The topic of the user question. One of 'qa' or 'shopping'."""


CONSULTANT = BookConsultant()

if __name__ == '__main__':
    consultant = BookConsultant()
    reply_result = consultant.ask("你这里有 Python 的书吗？")
    logger.info(f"reply result: {reply_result}")
