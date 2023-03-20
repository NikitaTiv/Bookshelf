from flask_wtf import FlaskForm
from wtforms import SelectMultipleField


class BookForm(FlaskForm):
    books = SelectMultipleField('books', choices=[])
