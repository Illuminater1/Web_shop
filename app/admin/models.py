import os

from flask import url_for
from markupsafe import Markup

from app.db import db
from flask_admin import form
from slugify import slugify
from wtforms import SelectField
import secrets

from flask_admin.contrib.sqla import ModelView

from flask_admin.form.upload import ImageUploadField

file_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class UsersView(ModelView):
    AVAILABLE_ROLES = [('admin', 'Администратор'),
                       ('user', 'Пользователь'),
                       ('manager', 'Менеджер'), ]

    form_overrides = {'role': SelectField, }

    column_list = ['id', 'username', 'email', 'role']

    column_labels = {'id': 'ID',
                     'username': 'Имя',
                     'email': 'Email',
                     'role': 'Роль', }

    form_columns = ['username', 'email', 'role']

    form_args = {'role': {'choices': AVAILABLE_ROLES}}

    column_filters = ['role', 'email', 'username']

    edit_modal = True


def generate_name(file_data):
    random_hex = secrets.token_hex(8)
    name, ext = os.path.splitext(file_data.filename)
    img_name = f"{random_hex}{ext.lower()}"

    return img_name


class ProductView(ModelView):
    # Изменение названия колонок
    column_labels = {'name': 'Название',
                     'slug': 'Ссылка',
                     'description': 'Описание',
                     'image': 'Изображение',
                     'stocks': 'Остаток',
                     'price': 'Цена',
                     'category': 'Категория'}

    # исключенные колонки
    form_excluded_columns = ['carts', 'ordered_products']

    # фильтрация по категории и цене
    column_filters = ['category', 'price']

    # переопределение формы
    form_overrides = {'image': ImageUploadField}

    # Отображение картинки в админпанели
    def _list_thumbnail(self, context, model, name):
        if not model.image:
            return ''
        url = url_for('static', filename=os.path.join(f"media/products/{model.image}"))
        return Markup(f'<img src="{url}" width="100">')

    def _category_formatter(view, context, model, name):
        category = model.category
        return f"{category.name}(ID-{category.id})"

    column_formatters = {'image': _list_thumbnail,
                         'category': _category_formatter}

    # форма для сохранения картинки
    form_extra_fields = {
        'image': form.ImageUploadField(
            'Изображение товара',
            base_path=os.path.join(file_path, 'static', 'media', 'products', ),
            url_relative_path='static/media/products/',
            namegen=generate_name,
            allowed_extensions=['jpg', 'jpeg', 'png', 'svg'],
            max_size=(1200, 780, True),
            thumbgen=(100, 100, True)
        )}


    def on_model_change(self, form, model, is_created):

        db.session.add(model)
        db.session.flush()

        # Создание slug
        name = form.name.data
        if not form.slug.data and name:
            model.slug = f"{slugify(name)}-{str(model.id)}"

        # сохранение товара
        super().on_model_change(form, model, is_created)



class OrdersView(ModelView):
    AVAILABLE_STATUSES = [('new', 'Новый'),
                          ('processing', 'В обработке'),
                          ('shipped', 'Отправлен'),
                          ('delivered', 'Доставлен'),
                          ('canceled', 'Отменен'), ]

    form_overrides = {'status': SelectField,
                      'delivery_method': SelectField,
                      'payment': SelectField}

    column_list = ['status', 'first_name', 'last_name', 'phone_number', 'delivery_method',
                   'address', 'payment', 'created_time', 'user']

    column_labels = {'first_name': 'Имя',
                     'last_name': 'Фамилия',
                     'phone_number': 'Телефон',
                     'delivery_method': 'Доставка',
                     'address': 'Адрес',
                     'status': 'Статус заказа',
                     'payment': 'Оплата',
                     'created_time': 'Время создания',
                     'user': 'Покупатель'}

    form_columns = ['status', 'delivery_method', 'payment',
                    'address', 'first_name', 'last_name', 'phone_number', ]

    form_args = {
        'status': {'choices': AVAILABLE_STATUSES},

        'delivery_method': {'choices': [('delivery', 'Доставка'), ('pickup', 'Самовывоз')]},

        'payment': {'choices': [('card', 'Картой'), ('cash', 'Наличными')]}
    }

    def _user_formatter(view, context, model, name):
        user = model.user
        return f"Покупатель: {user.username} (email: {user.email})"

    def _delivery_formatter(view, context, model, name):
        delivery_translate = {'delivery': 'Доставка',
                              'pickup': 'Самовывоз'
                              }
        return delivery_translate[model.delivery_method]

    def _payment_formatter(view, context, model, name):
        payment_translate = {'card': 'Картой',
                             'cash': 'Наличными'
                             }
        return payment_translate[model.payment]

    column_formatters = {
        'user': _user_formatter,
        'delivery_method': _delivery_formatter,
        'payment': _payment_formatter

    }

    edit_modal = True

    can_export = True


class CategoryView(ModelView):
    column_labels = {'name': 'Название  категории'}

    form_excluded_columns = ['products']


class OrderedProductView(ModelView):
    column_labels = {'order': 'ID заказa',
                     'product': 'ID товарa',
                     'name': 'Название товара',
                     'quantity': 'Количество',
                     'price': 'цена',
                     'created timestamp': 'Дата заказа'

                     }
    column_filters = ['order.id', 'price', 'name', 'quantity', 'created_timestamp', 'product.id']

    def _time_formatter(view, context, model, name):
        return model.created_timestamp.strftime('%d.%m.%Y %H:%M:%S')

    def _product_formatter(view, context, model, name):
        product = model.product
        return f"Товар - {product.name} (id-{product.id})"

    def _order_formatter(view, context, model, name):
        order = model.order
        return f"Покупатель-{order.user.username} (ID заказa-{order.id})"

    column_formatters = {
        'created_timestamp': _time_formatter,
        'product': _product_formatter,
        'order': _order_formatter

    }

    can_create = False
