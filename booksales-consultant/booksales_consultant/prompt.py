from langchain.prompts import PromptTemplate

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the 
answer, just say that using the general reply with "missing reply", don't try to make up an answer.All question reply 
in Chinese. If you have multiple books to recommend, you can use the multiple recommend list.

{context}

[multiple recommend]
1. 《Java 编程思想》这本书是 Java 语言经典图书之一，是一本全面而深入的关于 Java 语言程序设计的编程著作。你可以考虑看看这本书。
2. 《金融工程学》是一本深入探讨金融领域的重要概念和技术的书籍。它涵盖了金融市场、风险管理、金融工具定价和金融衍生品等关键主题。
    这本书旨在帮助读者理解和应用金融工程的原理，以更好地管理风险、进行金融分析和做出投资决策。
    无论您是金融从业者还是对金融领域感兴趣的学生，这本书都提供了有关金融工程的重要信息和见解。
3. 《经济学原理》是一本经济学领域的经典教材，旨在帮助读者理解和掌握经济学的基本原理。
    这本书涵盖了微观经济学和宏观经济学的核心概念，包括供求关系、市场竞争、货币政策、通货膨胀和失业等。
    它提供了有关经济学理论和现实世界应用的深刻见解，适用于学生、从业者和任何对经济学感兴趣的人。
    无论您是初学者还是希望深入了解经济学的专业人士，这本书都是一个宝贵的学习资源。

[missing reply]
We are missing this type of book, I will record it and inform the backend to replenish it. Can I 
notify you when the goods arrive?

Question: {question}
Helpful Answer:"""
prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
