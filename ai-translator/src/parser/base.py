from abc import abstractmethod
from typing import Optional

from schema import Book


class BaseParser:
    @abstractmethod
    def parse(self, file_path: str, pages: Optional[int] = None) -> Book:
        raise NotImplementedError('parse() method must be implemented')
