from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField("Пароль", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary w-100 py-2"})
    remember_me = BooleanField("Запомнить меня", default=True,
                               render_kw={"class": "form-check-input"})