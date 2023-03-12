from flask import Blueprint, flash, send_file, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename

from webapp.page.forms import BookForm
from webapp.page.utils import (allowed_file, save_user_book,
                               delete_user_book, split_row_book_delete)
from webapp.user.models import Book

blueprint = Blueprint('page', __name__)


@blueprint.route('/')
def main_page():
    return render_template('page/main_page.html')


@blueprint.route('/my_bookshelf')
@login_required
def bookshelf():
    title = 'Моя полка'
    form = BookForm()
    form.books.choices = [
        f'{book.name} / {book.author}' for book in Book.query.filter(Book.user==current_user.username)
    ]
    return render_template('page/my_shelf.html', page_title=title, form=form)


@blueprint.route('/work_book', methods=['POST'])
@login_required
def work_book():
    form = BookForm()
    if 'upload' in request.form:
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
            filepath = os.path.join('upload', current_user.username, filename)
            os.makedirs(f'upload/{current_user.username}', exist_ok=True)
            file.save(filepath)
            save_user_book(current_user.username, name, author, description, filename)
            flash('Файл загружен.')
            return redirect(url_for('page.bookshelf'))
        else:
            flash('Заполните все поля.')
            return redirect(url_for('page.bookshelf'))
    if 'delete' in request.form:
        book_name, author = split_row_book_delete(form.books.data[0])
        delete_user_book(book_name, author)
        return redirect(url_for('page.bookshelf'))
    if 'download' in request.form:
        book_name, author = split_row_book_delete(form.books.data[0])
        book = Book.query.filter(
            Book.user==current_user.username, Book.name==book_name, Book.author==author,
        ).first()
        filepath = f'/home/nikita/Projects/Bookshelf/upload/{book.user}/{book.filename}'
        return send_file(filepath, as_attachment=True, download_name=f'{book_name}.txt')
    return redirect(url_for('page.bookshelf'))


@blueprint.route('/search-book')
@login_required
def search_book():
    title = 'Поиск книги'
    books = Book.query.filter(Book.description != None).all()
    form = BookForm()
    list_books = []
    for book in books:
        name = f'«{book.name}»'
        author = book.author
        description = book.description
        list_books.append({'name': name, 'author': author, 'description': description})
    return render_template(
        'page/search_book.html', page_title=title, book_active=list_books[0], list_books=list_books[1:], form=form,
    )


@blueprint.route('/process-search', methods=['POST'])
@login_required
def process_search():
    title = 'Поиск книги'
    books = Book.query.filter(Book.description).all()
    form = BookForm()
    list_books = []
    for book in books:
        name = f'«{book.name}»'
        author = book.author
        description = book.description
        list_books.append({'name': name, 'author': author, 'description': description})
    if 'search' in request.form:
        name_book = request.form['book']
        form.books.choices = [book.name for book in Book.query.filter(Book.name==name_book).all()]
    if 'download' in request.form:
        book_name = form.books.data[0]
        book = Book.query.filter(Book.name==book_name).first()
        filepath = f'/home/nikita/Projects/Bookshelf/upload/{book.user}/{book.filename}'
        return send_file(filepath, as_attachment=True, download_name=f'{book_name}.txt')
    return render_template(
        'page/search_book.html', page_title=title, book_active=list_books[0], list_books=list_books[1:], form=form,
    )
