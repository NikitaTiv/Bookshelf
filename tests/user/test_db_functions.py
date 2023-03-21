from webapp.user.db_fuctions import (save_user_book_to_db, delete_user_book_from_db,
                                     checking_book_availability, find_book_in_db, create_user,
                                     checking_user_availability, delete_all_records_from)
from webapp.user.models import User, Book


def test__delete_user_book__success_case(app, user, book, clear_tables):
    delete_user_book_from_db(book)

    result = checking_book_availability(book)

    assert not result


def test__save_user_book_to_db__success_case(app, user, clear_tables):
    book = Book(
        user='test_user', name='test_name', author='test_author',
        description='test_description', filename='test_filename',
    )

    save_user_book_to_db(book)

    assert checking_book_availability(book)


def test__find_book_in_db__success_case(app, user, book, clear_tables):
    assert find_book_in_db(book.user, book.name, book.author).name == 'test_name'


def test__create_user__success_case(app, clear_tables):
    user = User(
        username='test_user', email='test_email', password='test_password',
    )

    create_user(user)

    assert checking_user_availability(user)


def test__checking_book_availability__success_case(app, user, book, clear_tables):
    assert checking_book_availability(book)


def test__checking_user_availability__success_case(app, user, clear_tables):
    assert checking_user_availability(user)


def test_delete_all_records_from__success_case(app, user, book):
    delete_all_records_from(Book)
    delete_all_records_from(User)

    assert not checking_book_availability(book)
    assert not checking_user_availability(user)
