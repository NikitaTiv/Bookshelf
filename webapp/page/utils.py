from flask import current_app
from flask_login import current_user
import os

from webapp.user.models import Book
from webapp.db import db


def allowed_file(filename: str) -> bool:
    """Функция проверки расширения файла."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def split_row_book_delete(row: str) -> tuple[str]:
    """Функция, которая делит получаемую строку."""
    return row.split('/')[0].strip(), row.split('/')[1].strip()


def save_user_book(user: str, name: str, author: str, description: str, filename: str) -> None:
    """Сохраняет в БД закруженную книгу."""
    new_book = [
        {'user': user, 'name': name, 'author': author, 'description': description, 'filename': filename},
    ]
    db.session.bulk_insert_mappings(Book, new_book)
    db.session.commit()


def delete_user_book(book_name: str, author: str) -> None:
    """Удаляет книгу из БД."""
    book = Book.query.filter(
        Book.user==current_user.username, Book.name==book_name, Book.author==author,
    ).first()
    os.remove(f'upload/{current_user.username}/{book.filename}')
    db.session.delete(book)
    db.session.commit()
