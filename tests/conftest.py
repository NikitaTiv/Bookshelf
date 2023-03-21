import pytest

from webapp import create_app
from webapp.user.models import Book, User
from webapp.user.db_fuctions import (delete_all_records_from, save_user_book_to_db,
                                     create_user)


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture
def user():
    user = User(
        username='test_user', email='test_email', password='test_password',
    )
    create_user(user)
    yield user


@pytest.fixture
def book():
    book = Book(
        user='test_user', name='test_name', author='test_author',
        description='test_description', filename='test_filename',
    )
    save_user_book_to_db(book)
    yield book


@pytest.fixture
def clear_tables(app):
    yield
    delete_all_records_from(Book)
    delete_all_records_from(User)
