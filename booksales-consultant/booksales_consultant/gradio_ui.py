import gradio as gr
from book_consultant import CONSULTANT
from utils import logger


def ask(question, history):
    reply = CONSULTANT.ask(question)
    logger.info(f"reply: {reply}")
    return reply


def launch():
    examples = [
        "有python方面的书吗",
        "你们有os方面的书吗",
        "我想学golang，有这方面的书吗",
        "我想成为编程高手，有这方面的书吗",
        "我想成为计算机专家，有这方面的书吗",
        "我想了解一些东方哲学，有什么书可以推荐吗",
        "我想了解一些西方哲学，有什么书可以推荐吗",
    ]
    demo = gr.ChatInterface(fn=ask,
                            textbox=gr.Textbox(placeholder="请输入任何关于书的问题"),
                            examples=examples,
                            title="Book Consultant",
                            retry_btn=None, clear_btn=None, undo_btn=None,
                            description="尊敬的客户，欢迎来到我们的书店！如果您有任何问题，欢迎随时向我们提问")
    logger.info("已启动 Book Consultant 服务")
    demo.launch(share=True, server_name="0.0.0.0")


if __name__ == "__main__":
    launch()
