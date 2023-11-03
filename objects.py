from dataclasses import dataclass

@dataclass
class Category:
    id: int = 0
    name: str = ""

@dataclass
class Author:
    id: int = 0
    name: str = ""

@dataclass
class Book:
    id: int = 0
    title: str = ""
    author_id: int = 0
    category_id: int = 0

@dataclass
class Review:
    id: int = 0
    book_id: int = 0
    user_id: int = 0
    rating: int = 0
    review_text: str = ""