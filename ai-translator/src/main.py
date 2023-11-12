import os
import sys

from langchain.chat_models import ChatOpenAI

from config import Config
from model import ModelProvider, get_model
from parser import PdfParser
from translate import Translator
from utils import ArgumentParser

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse()
    # 初始化配置单例
    config = Config()
    config.initialize(args)

    pdfparser = PdfParser()
    book = pdfparser.parse(file_path=config.input_file, pages=config.pages)
    # print(book.pages[0].contents[0].original)
    # print("----")
    # print(book.pages[0].contents[1].original)

    llm = get_model(config.model)
    translator = Translator(llm=llm)
    translator.translate(source_language="English", target_language="Chinese", book=book)
