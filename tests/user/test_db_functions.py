import pytest

from webapp.user.db_fuctions import (save_user_book_to_db, delete_user_book_from_db,
                                     checking_book_availability, find_book_in_db, create_user,
                                     checking_user_availability, delete_all_records_from)
from webapp.user.models import User, Book


def test__delete_user_book__success_case(app, user, book, clear_tables):
    create_user(user)
    save_user_book_to_db(book)

    delete_user_book_from_db(book)
    result = checking_book_availability(book)

    assert not result


def test__save_user_book_to_db_success_case(app, user, book, clear_tables):
    create_user(user)
    save_user_book_to_db(book)

    result = checking_book_availability(book)
    
    assert result


def test__find_book_in_db__success_case(app, user, book, clear_tables):
    create_user(user)
    save_user_book_to_db(book)

    book = find_book_in_db(book.user, book.name, book.author)

    assert book.name == 'test_name'


def test__create_user__success_case(app, user, clear_tables):
    create_user(user)

    result = checking_user_availability(user)

    assert result


def test__checking_book_availability__success_case(app, book, user, clear_tables):
    create_user(user)
    save_user_book_to_db(book)

    result = checking_book_availability(book)

    assert result


def test__checking_user_availability__success_case(app, user, clear_tables):
    create_user(user)

    result = checking_user_availability(user)

    assert result


def test_delete_all_records_from__success_case(app, user, book):
    create_user(user)
    save_user_book_to_db(book)

    delete_all_records_from(Book)
    delete_all_records_from(User)

    assert not checking_book_availability(book)
    assert not checking_user_availability(user)
