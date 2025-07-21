from flask import Blueprint, render_template, url_for, redirect
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


from app.user.models import User
from app.orders.models import Order, OrderedProduct
from app.shop.models import Product, Category
from app.db import db
from flask_login import current_user

# blueprint = Blueprint('admin', __name__, url_prefix='/admin')


class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.login'))

admin = Admin(name='АДМИНКА',
              template_mode='bootstrap4',
              index_view=AdminView(url='/admin', endpoint='admin'))


class UsersForAdmin(ModelView):
    column_list = ['username',
                   'email',
                   'role']

    form_columns = ['username',
                    'email',
                    'role']

class OrdersForAdmin(ModelView):
    column_list = ['delivery_method',
                   'status',
                   'payment',
                   'user_id']

    form_columns = ['delivery_method',
                    'status',
                    'payment',
                    'user_id']


class OrdersForAdmin(ModelView):
    column_list = ['delivery_method',
                   'status',
                   'payment',
                   'user_id',
                   'created_time',]

    form_columns = ['delivery_method',
                    'status',
                    'payment',
                    'user_id']


def init_admin(app):
    admin.add_view(UsersForAdmin(User, db.session, name='Пользователи', endpoint='admin_users'))
    admin.add_view(OrdersForAdmin(Order, db.session, name='Заказы', endpoint='admin_orders'))
    admin.add_view(ModelView(Category, db.session, name='Категории'))
    admin.add_view(ModelView(Product, db.session, name='Товары'))
    admin.add_view(ModelView(OrderedProduct, db.session, name='Заказанные товары'))

    admin.init_app(app)

