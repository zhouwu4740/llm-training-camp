from typing import Optional
from schema import Book, Page, TableContent, TextContent
from parser import BaseParser
import pdfplumber

from translate import PageOutOfRangeException
from utils import logger


def parse_page(pdf_page) -> Page:
    """ 解析 PDF 页面"""
    raw_text = pdf_page.extract_text(layout=True)
    tables = pdf_page.extract_tables()

    logger.debug(raw_text)
    # 从 raw_text中去除 table 内容
    for table in pdf_page.find_tables():
        # 获取 table 的坐标
        bbox = table.bbox
        # 从页面裁剪出 table，并获取 table 文本
        table_text = pdf_page.crop(bbox).extract_text(layout=True)
        # 去除 raw_text中的 table 文本内容
        for row_text in table_text.splitlines():
            raw_text = raw_text.replace(row_text, '', 1)

    page = Page()
    if raw_text:
        # Remove empty lines and leading/trailing whitespaces
        raw_text_lines = raw_text.splitlines()
        cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
        cleaned_raw_text = "\n".join(cleaned_raw_text_lines)
        text_content = TextContent(cleaned_raw_text)
        page.add_content(text_content)

    if tables:
        table = TableContent(tables)
        page.add_content(table)

    return page


class PdfParser(BaseParser):
    def parse(self, file_path: str, pages: Optional[int] = None) -> Book:
        book = Book(file_path)

        with pdfplumber.open(file_path) as pdf:
            if pages is not None and len(pdf.pages) < pages:
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                # 解析页面
                page = parse_page(pdf_page)
                book.add_page(page)

        return book
