from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel

from app.db import db
from app.shop.models import Category, Product
from app.carts.models import Cart
from app.orders.models import Order, OrderedProduct
from app.user.models import User
from app.admin.views import init_admin

from app.user.forms import LoginForm
from app.config import SECRET_KEY

from app.user.views import blueprint as user_blueprint
from app.shop.views import blueprint as shop_blueprint
from app.main.views import blueprint as main_blueprint
from app.carts.views import blueprint as cart_blueprint
from app.orders.views import blueprint as orders_blueprint


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate = Migrate(app, db)
    babel = Babel(app)


    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = "Пожалуйста авторизуйтесь"



    app.register_blueprint(shop_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(orders_blueprint)
    app.register_blueprint(user_blueprint)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def page_error(error):
        return render_template('page_error.html'), 404

    init_admin(app)

    return app
