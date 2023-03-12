from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    """Форма для авторизации."""

    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={'class': 'form-check-input'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-secondary'})


class RegistrationForm(FlaskForm):
    """Форма для регистрации."""

    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password_2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={'class': 'form-control'},
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-secondary'})

    def validate_username(self, username):
        """Проверяет валидность поля username."""
        user_count = User.query.filter_by(username=username.data).count()
        if user_count:
            raise ValidationError('Пользователь с таким именем уже существует.')

    def validate_email(self, email):
        """Проверяет палидность поля email."""
        user_count = User.query.filter_by(email=email.data).count()
        if user_count:
            raise ValidationError('Пользователь с таким именем уже существует.')
