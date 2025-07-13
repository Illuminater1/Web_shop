from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user
from app.user.forms import LoginForm, RegistrationForm
from app.user.models import User, db
from sqlalchemy.exc import SQLAlchemyError

blueprint = Blueprint('user', __name__,
                      url_prefix='/user',
                      template_folder='templates/user')


@blueprint.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('Вы уже авторизованы')
        return redirect(url_for('main.index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)

            db.session.add(new_user)

            db.session.commit()
            flash("Вы успешно зарегистрировались")
            return redirect(url_for("user.login"))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Произошла ошибка при записи в базу данных")
            return redirect(url_for('user.register'))

    return render_template('user/register.html',
                           page_title='Регистрация', form=form)


@blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()

    return render_template('user/login.html',
                           page_title="Авторизация", form=form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы успешно вошли на сайт")
            return redirect(url_for("main.index"))

    flash("Неправильный логин или пароль")
    return redirect(url_for("user.login"))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли')
    return redirect(url_for('main.index'))

