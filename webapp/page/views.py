from flask import Blueprint, current_app,  render_template, flash, request, redirect, url_for
from flask_login import current_user
import os
from werkzeug.utils import secure_filename

from webapp.page.utils import allowed_file

blueprint = Blueprint('page', __name__)

@blueprint.route('/')
def main_page():
    return render_template('page/main_page.html')

@blueprint.route('/my_bookshelf')
def bookshelf():
    title = 'Моя полка'
    return render_template('page/my_shelf.html', page_title=title)

@blueprint.route('/work_book', methods=['POST'])
def work_book():
    if "upload" in request.form:
        file = request.files['file']
        name = request.form['name']
        description = request.form['description']
        if not allowed_file(file.filename):
            flash('У файла некорректное расширение')
            return redirect(url_for('page.bookshelf'))
        if file:
            flash('Файл загружен.')
            filename = secure_filename(file.filename)
            os.makedirs(f'upload/{current_user.username}', exist_ok=True)
            file.save(os.path.join('upload', current_user.username, filename))
            return redirect(url_for('page.bookshelf'))
