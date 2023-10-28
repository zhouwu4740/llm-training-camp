from typing import List

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    price: float


class ShoppingCart(BaseModel):
    books: List[Book] = []

    def add_book(self, name: str, price: float):
        self.books.append(Book(title=name, price=price))

    def remove_book(self, name: str):
        for book in self.books:
            if book.title == name:
                self.books.remove(book)

    def view_inventory(self):
        return self.books

    def checkout(self):
        total = 0
        for book in self.books:
            total += book.price
        return total
