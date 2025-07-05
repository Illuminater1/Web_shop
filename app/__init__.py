from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from app.forms import LoginForm
from app.models import db, Category, Product, User, Order, Product_image
from app.config import SECRTET_KEY


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.config['SECRET_KEY'] = SECRTET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/", methods=['POST', 'GET'])
    def index():
        page_title = 'Главная страница'
        content = 'Главная страница'
        return render_template('index.html',
                               page_title=page_title, content=content)

    @app.route("/login")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        page_title = "Авторизация"

        return render_template('login.html',
                               page_title=page_title, form=form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username==form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Вы вошли на сайт")
                return redirect(url_for("index"))
        flash("Неправильный логин или пароль")
        return redirect(url_for("login"))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ!'

    @app.route("/shop")
    def shop():
        page_title = 'Магазин'
        content = 'Страница магазина'
        return render_template('shop.html',
                               page_title=page_title, content=content)

    @app.route("/about")
    def about():
        page_title = 'О нас'
        content = 'Страница о нас'
        return render_template('about.html',
                               page_title=page_title, content=content)

    @app.route("/contacts")
    def contacts():
        page_title = 'Контакты'
        content = 'Страница с контактами'
        return render_template('contacts.html',
                               page_title=page_title, content=content)

    @app.route("/questions")
    def questions():
        page_title = 'Вопросы'
        content = 'Страница с вопросами'
        return render_template('questions.html',
                               page_title=page_title, content=content)

    @app.errorhandler(404)
    def page_error(error):
        return render_template('page_error.html')

    return app

