from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/user')


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()],
                           render_kw={"class": "form-control"})

    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})

    submit = SubmitField("Отправить",
                         render_kw={"class": "btn btn-primary w-100 py-2"})

    remember_me = BooleanField("Запомнить меня", default=True,
                               render_kw={"class": "form-check-input"})


class RegistrationForm(FlaskForm):
    username = StringField('Введите имя', validators=[DataRequired()],
                           render_kw={"class": "form-control"})

    email = StringField('Введите Email', validators=[DataRequired(), Email('Введен некоректный Email')],
                        render_kw={"class": "form-control"})

    password = PasswordField('Введите пароль', validators=[DataRequired(), Length(min=6)],
                             render_kw={"class": "form-control", "placeholder": "Не менее 6 символов"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(), EqualTo('password', 'Введенные пароли не совпадают')],
                              render_kw={"class": "form-control", "placeholder": "Повторите пароль"})

    submit = SubmitField('Зарегистрироваться',
                         render_kw={"class": "btn btn-primary w-100"})

    def validate_username(self, username):
        user_count = User.query.filter(User.username.ilike(username.data)).first()
        if user_count:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        user_count = User.query.filter(User.email.ilike(email.data)).first()
        if user_count:
            raise ValidationError('Пользователь с таким Email уже существует')
