from flask import current_app
import os
from typing import Type


def checks_available_format(filename: str) -> bool:
    """Функция проверки расширения файла."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config[
        'ALLOWED_EXTENSIONS'
    ]


def delete_bookfile(book: Type) -> None:
    os.remove(f'upload/{book.user}/{book.filename}')
