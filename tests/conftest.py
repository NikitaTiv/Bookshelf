import pytest

from webapp import create_app
from webapp.user.models import Book, User
from webapp.user.db_fuctions import create_user, delete_all_records_from, save_user_book_to_db


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture
def user():
    user = User(
        username='test_user', email='test_email', password='test_password'
    )
    yield user


@pytest.fixture
def book():
    book = Book(
        user='test_user', name='test_name', author='test_author', description='test_description', filename='test_filename'
    )
    yield book


@pytest.fixture
def clear_tables(app):
    yield
    delete_all_records_from(Book)
    delete_all_records_from(User)


@pytest.fixture
def create_name_extension():
    def create_name_extension_function(elem1, elem2):
        file_path = f'text{elem1}{elem2}'
        return file_path
    return create_name_extension_function
