from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from app.user.forms import LoginForm
from app.user.models import User, Order
from app.product.models import  Product
from app.shop.models import db, Category, OrderedProduct
from app.config import SECRET_KEY
from app.user.views import blueprint as user_blueprint
from app.shop.views import blueprint as shop_blueprint
from app.admin.views import blueprint as admin_blueprint
from app.main.views import blueprint as main_blueprint
from app.product.views import blueprint as product_blueprint



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = "Пожалуйста авторизуйтесь"
    app.register_blueprint(user_blueprint)
    app.register_blueprint(shop_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(product_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.errorhandler(404)
    def page_error(error):
        return render_template('page_error.html')

    return app
