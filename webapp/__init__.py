from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from settings_box import config
from webapp.forms import LoginForm
from webapp.models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def main_page():
        greet = "Привет Buddy!"
        return render_template('main_page.html', greetings=greet)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('main_page'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username==form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт.')
                return redirect(url_for('main_page'))
        flash('Неправильное имя или пароль.')
        return redirect(url_for('login'))
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились.')
        return redirect(url_for('main_page'))
    
    @app.route('/admin')
    @login_required
    def admin_page():
        if current_user.is_admin:
            return 'Привет админ!'
        else:
            return 'Ты не админ!'
    
    return app
