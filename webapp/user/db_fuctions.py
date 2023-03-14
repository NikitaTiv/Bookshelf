from flask_login import current_user
import os

from webapp.user.models import Book
from webapp.db import db


def save_user_book(user: str, name: str, author: str, description: str, filename: str) -> None:
    new_book = Book(
        user=user, name=name, author=author, description=description, filename=filename,
    )
    db.session.add(new_book)
    db.session.commit()


def delete_user_book(book_name: str, author: str) -> None:
    book = Book.query.filter(
        Book.user==current_user.username, Book.name==book_name, Book.author==author,
    ).first()
    os.remove(f'upload/{current_user.username}/{book.filename}')
    db.session.delete(book)
    db.session.commit()
