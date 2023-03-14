from flask import Blueprint, current_app, flash, send_file, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename

from webapp.dataclasses import UserBook
from webapp.page.forms import BookForm
from webapp.user.db_fuctions import save_user_book, delete_user_book
from webapp.user.models import Book
from webapp.utils.handler_strings import split_row_book_delete
from webapp.utils.handler_files import allowed_file

blueprint = Blueprint('page', __name__)


@blueprint.route('/')
def main_page():
    return render_template('page/main_page.html')


@blueprint.route('/my_bookshelf')
@login_required
def bookshelf():
    form = BookForm()
    form.books.choices = [
        f'{book.name} / {book.author}' for book in Book.query.filter(Book.user==current_user.username)
    ]
    return render_template('page/my_shelf.html', form=form)


@blueprint.route('/upload_book', methods=['POST'])
@login_required
def upload_book():
    file = request.files['file']
    name = request.form['name']
    author = request.form['author']
    description = request.form['description']
    if not description:
        description = None
    if not allowed_file(file.filename):
        flash('У файла некорректное расширение')
        return redirect(url_for('page.bookshelf'))
    if file and name and author:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username)
        os.makedirs(filepath, exist_ok=True)
        file.save(os.path.join(filepath, filename))
        save_user_book(current_user.username, name, author, description, filename)
        flash('Файл загружен.')
        return redirect(url_for('page.bookshelf'))
    else:
        flash('Заполните все поля.')
        return redirect(url_for('page.bookshelf'))


@blueprint.route('/delete_book', methods=['POST'])
@login_required
def delete_book():
    form = BookForm()
    book_name, author = split_row_book_delete(form.books.data[0])
    delete_user_book(book_name, author)
    return redirect(url_for('page.bookshelf'))


@blueprint.route('/download-my-book', methods=['POST'])
@login_required
def download_book():
    form = BookForm()
    book_name, author = split_row_book_delete(form.books.data[0])
    book = Book.query.filter(
        Book.user==current_user.username, Book.name==book_name, Book.author==author,
    ).first()
    filepath = os.path.join(
        current_app.config[current_app.config['UPLOAD_FOLDER']], current_user.username, book.filename,
    )
    return send_file(filepath, as_attachment=True, download_name=f'{book_name}.txt')


@blueprint.route('/global-search')
@login_required
def global_search():
    books = Book.query.filter(Book.description is not None).all()
    form = BookForm()
    list_books = []
    for book in books:
        list_books.append(UserBook(book.name, book.author, book.description))
    if not list_books:
        return render_template(
            'page/search_book.html', book_active=None, form=form,
        )
    return render_template(
        'page/search_book.html', book_active=list_books[0], list_books=list_books[1:], form=form,
    )


@blueprint.route('/search-book', methods=['POST'])
@login_required
def process_search():
    books = Book.query.filter(Book.description is not None).all()
    form = BookForm()
    list_books = []
    for book in books:
        list_books.append(UserBook(book.name, book.author, book.description))
    name_book = request.form['book']
    form.books.choices = [book.name for book in Book.query.filter(Book.name==name_book).all()]
    if not list_books:
        return render_template(
            'page/search_book.html', book_active=None, form=form,
        )
    return render_template(
        'page/search_book.html', book_active=list_books[0], list_books=list_books[1:], form=form,
    )


@blueprint.route('/download-global-book', methods=['POST'])
@login_required
def download_global_book():
    form = BookForm()
    book_name = form.books.data[0]
    book = Book.query.filter(Book.name==book_name).first()
    filepath = os.path.join(current_app.config[current_app.config['UPLOAD_FOLDER']], book.user, book.filename)
    return send_file(filepath, as_attachment=True, download_name=f'{book_name}.txt')
