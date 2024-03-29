from flask import Blueprint, current_app, flash, send_file, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename

from webapp.page.forms import BookForm
from webapp.user.db_fuctions import (save_user_book_to_db, delete_user_book_from_db,
                                     find_book_in_db)
from webapp.user.models import Book
from webapp.utils.handler_strings import split_row_book_delete
from webapp.utils.handler_files import checks_available_format, delete_bookfile

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
    if not checks_available_format(file.filename):
        flash('У файла некорректное расширение')
        return redirect(url_for('page.bookshelf'))
    if file and name and author:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.username)
        os.makedirs(filepath, exist_ok=True)
        file.save(os.path.join(filepath, filename))
        book = Book(
            user=current_user.username, name=name, author=author, filename=filename, description=description,
        )
        save_user_book_to_db(book)
        flash('Файл загружен.')
        return redirect(url_for('page.bookshelf'))
    else:
        flash('Заполните все поля.')
        return redirect(url_for('page.bookshelf'))


@blueprint.route('/delete_book', methods=['POST'])
@login_required
def delete_book():
    form = BookForm()
    if form.books.data:
        book_name, author = split_row_book_delete(form.books.data[0])
    else:
        flash('У вас нет загруженных книг')
        return redirect(url_for('page.bookshelf'))
    book = find_book_in_db(current_user.username, book_name, author)
    delete_user_book_from_db(book)
    delete_bookfile(book)
    return redirect(url_for('page.bookshelf'))


@blueprint.route('/download-my-book', methods=['POST'])
@login_required
def download_book():
    form = BookForm()
    if form.books.data:
        book_name, author = split_row_book_delete(form.books.data[0])
    else:
        flash('У вас нет загруженных книг')
        return redirect(url_for('page.bookshelf'))
    book = Book.query.filter(
        Book.user==current_user.username, Book.name==book_name, Book.author==author,
    ).first()
    filepath = os.path.join(
        current_app.config['UPLOAD_FOLDER'], current_user.username, book.filename,
    )
    return send_file(filepath, as_attachment=True, download_name=f'{book_name}.txt')


@blueprint.route('/global-search')
@login_required
def global_search():
    form = BookForm()
    books = Book.query.filter(Book.description is not None).all()
    list_books = [Book(name=book.name, author=book.author, description=book.description) for book in books]
    if not list_books:
        return render_template(
            'page/search_book.html', book_active=None, form=form,
        )
    return render_template(
        'page/search_book.html', book_active=list_books[0], list_books=list_books[1:], form=form,
    )


@blueprint.route('/search-book', methods=['POST'])
@login_required
def process_search():  # Тут подтягиваются сначала книги для карусели, а затем книги для поля MultiSelect
    form = BookForm()
    books = Book.query.filter(Book.description is not None).all()
    list_books = [Book(name=book.name, author=book.author, description=book.description) for book in books]
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
    if form.books.data:
        book_name = form.books.data[0]
    else:
        flash('Книга не найдена.')
        return redirect(url_for('page.global_search'))
    book = Book.query.filter(Book.name==book_name).first()
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], book.user, book.filename)
    return send_file(filepath, as_attachment=True, download_name=f'{book_name}.txt')
