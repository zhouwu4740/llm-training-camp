from .content import BaseContent


class Page:
    def __init__(self):
        self.contents = []

    def add_content(self, content: BaseContent):
        self.contents.append(content)
