from langchain.prompts import PromptTemplate

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the 
answer, just say that using the general reply with "missing reply", don't try to make up an answer.All question reply 
in Chinese. If you have multiple books to recommend, you can use the multiple recommend list.

{context}

[multiple recommend]
1. book1
2. book2
3. book3

[missing reply]
We are missing this type of book, I will record it and inform the backend to replenish it. Can I 
notify you when the goods arrive?

Question: {question}
Helpful Answer:"""
prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
