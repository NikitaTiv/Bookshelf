from flask_wtf import FlaskForm
from wtforms import SelectMultipleField


class BookForm(FlaskForm):
    """Форма для выбора книг."""

    books = SelectMultipleField('books', choices=[])
