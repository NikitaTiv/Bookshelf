from typing import Type

from webapp.user.models import Book, User
from webapp.db import db


def save_user_book_to_db(book: Type) -> None:
    new_book = Book(
        user=book.user, name=book.name, author=book.author,
        description=book.description, filename=book.filename,
    )
    db.session.add(new_book)
    db.session.commit()


def delete_user_book_from_db(book: Type) -> None:
    deleted_book = Book.query.filter(
        Book.user==book.user, Book.name==book.name, Book.author==book.author,
    ).first()
    db.session.delete(deleted_book)
    db.session.commit()


def find_book_in_db(username: str, bookname: str, author: str) -> Book:
    book = Book.query.filter(
        Book.user==username, Book.name==bookname, Book.author==author,
    ).first()
    return book


def create_user(user: Type) -> None:
    new_user = User(
        username=user.username, email=user.email, role='user', is_active=True,
    )
    new_user.set_password(user.password)
    db.session.add(new_user)
    db.session.commit()


def checking_book_availability(book: Type) -> bool:
    """Проверяет наличие книги в базе данных."""
    book = Book.query.filter(
        Book.user==book.user, Book.name==book.name, Book.author==book.author,
    ).first()
    if book:
        return True
    return False


def checking_user_availability(user: Type) -> bool:
    """Проверяет наличие пользователя в базе данных."""
    user = User.query.filter(
        User.username==user.username, User.email==user.email,
    ).first()
    if user:
        return True
    return False


def delete_all_records_from(model: Type) -> None:
    db.session.query(model).delete()
    db.session.commit()
