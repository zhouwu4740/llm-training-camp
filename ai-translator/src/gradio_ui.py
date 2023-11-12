import gradio as gr

from config import Config
from model import get_model
from parser import PdfParser
from translate import Translator
from utils import logger, ArgumentParser


def translation(input_file, provider, temperature, topn, max_tokens, source_language, target_language):
    logger.debug(
        f"[翻译任务]\n源文件: {input_file.name}\n模型供应商: {provider}\nTemperature: {temperature}\n"
        f"topN: {topn}\nmax tokens: {max_tokens}\n源语言: {source_language}\n目标语言: {target_language}")
    source_file = input_file.name
    pdfparser = PdfParser()
    book = pdfparser.parse(file_path=source_file)
    # 根据参数获取后端模型
    llm = get_model(Config().get_model_config(provider.lower()))
    translator = Translator(llm=llm)
    target_path = translator.translate(source_language=source_language,
                                       target_language=target_language,
                                       book=book)
    return target_path


def launch_gradio():
    with gr.Blocks() as app:
        with gr.Row():
            input_file = gr.File(label="上传PDF文件")
            output_file = gr.File(label="下载翻译文件")
        with gr.Row():
            with gr.Column():
                provider = gr.Radio(label="模型供应商", choices=["OpenAI", "ChatGLM"], value="OpenAI")
                source_language = gr.Dropdown(label="源语言", choices=["English", "Chinese"], value="English")
                target_language = gr.Dropdown(label="目标语言", choices=["English", "Chinese"], value="Chinese")
            with gr.Column():
                temperature = gr.Slider(label="Temperature", minimum=0.0, maximum=1.0, step=0.1, value=0.7)
                topn = gr.Slider(label="TopN", minimum=0, maximum=100, step=1, value=50)
                max_tokens = gr.Slider(label="Max Tokens", minimum=100, maximum=2000, step=1, value=1000)
        submit = gr.Button("提交")
        submit.click(fn=translation,
                     inputs=[input_file, provider, temperature, topn, max_tokens, source_language, target_language],
                     outputs=output_file)
        app.launch(share=True, server_name="0.0.0.0")


if __name__ == '__main__':
    argument_parser = ArgumentParser()
    args = argument_parser.parse()
    # 初始化配置单例
    config = Config()
    config.initialize(args)
    # 解析命令行
    launch_gradio()
