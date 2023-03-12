from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import db


class User(db.Model, UserMixin):
    """Таблица 'Пользователь'."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String(10), index=True)
    is_active = db.Column(db.Boolean, index=True)
    email = db.Column(db.String, index=True, unique=True)

    def check_password(self, password):
        """Проверяет зашифрованный пароль."""
        return check_password_hash(self.password, password)

    def set_password(self, password):
        """Шифрует пароль."""
        self.password = generate_password_hash(password)

    @property
    def is_admin(self):
        """Проверяет является ли пользователь админом."""
        return self.role == 'admin'

    def __repr__(self):
        """Отображает корректно класс при печати."""
        return f'<User {self.username}: {self.role}>'


class Book(db.Model):
    """Таблица 'Книга'."""

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, index=True, nullable=False)
    name = db.Column(db.String, index=True, nullable=False)
    author = db.Column(db.String, index=True, nullable=False)
    filename = db.Column(db.String, index=True, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        """Отображает корректно класс при печати."""
        return f'Книга {self.name}, автор {self.author}'
