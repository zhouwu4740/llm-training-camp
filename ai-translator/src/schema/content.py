from abc import ABC, abstractmethod
from typing import List, Any

import pandas as pd


# class ContentType(Enum):
#     """
#     An enum class that represents the type of content in a page.
#     """
#     TEXT = auto()
#     TABLE = auto()
#     IMAGE = auto()


class BaseContent(ABC):
    """
    A class that represents a content in a page.
    """

    def __init__(self, original, translation=None, status=False):
        if not type(original) in self.content_types():
            raise ValueError(
                f'Invalid translation data type. Expected {self.content_types()}, but got {type(original)}')

        self.original = original
        self.translation = translation
        self.status = status

    @abstractmethod
    def set_translation(self, translation, status):
        """
        Args:
            translation: the result of translation
            status: translate status
        """

    @abstractmethod
    def content_types(self) -> List[Any]:
        """
        The data types accepted by the Content Type
        """


class TextContent(BaseContent):

    def set_translation(self, translation, status):
        self.translation = translation
        self.status = status

    @classmethod
    def content_types(cls):
        return [str]


class TableContent(BaseContent):
    def __init__(self, data):
        df = pd.DataFrame(data)
        super().__init__(df)

    def set_translation(self, translation, status):
        pass

    @classmethod
    def content_types(cls) -> List[Any]:
        return [pd.DataFrame]


