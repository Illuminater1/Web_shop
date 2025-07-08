from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/user')


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField("Пароль", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary w-100 py-2"})
    remember_me = BooleanField("Запомнить меня", default=True,
                               render_kw={"class": "form-check-input"})


class RegistrationForm(FlaskForm):
    username = StringField('Введите имя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Введите Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Введите пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary w-100"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста введите другое имя')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот логин уже используется, введите другой')
