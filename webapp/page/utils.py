from flask import current_app

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']