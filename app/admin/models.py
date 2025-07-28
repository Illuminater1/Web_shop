import os


from flask import url_for
from markupsafe import Markup

from flask_admin import form
from slugify import slugify
from wtforms import SelectField
import secrets

from flask_admin.contrib.sqla import ModelView

from flask_admin.form.upload import ImageUploadField

file_path = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.dirname(file_path)


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


def generate_name(model, file_data):
    random_hex = secrets.token_hex(8)
    name, ext = os.path.splitext(file_data.filename)
    img_name = f"{random_hex}{ext.lower()}"

    return img_name


class ProductView(ModelView):
    column_labels = {'name': 'Название',
                     'slug': 'Ссылка',
                     'description': 'Описание',
                     'image': 'Изображение',
                     'stocks': 'Остаток',
                     'price': 'Цена',
                     'category': 'Категория'}

    form_excluded_columns = ['carts', 'ordered_products', 's']

    column_filters = ['category', 'price']

    form_overrides = {'image': ImageUploadField}

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''
        url = url_for('static', filename=os.path.join('media', model.image))
        return Markup(f'<img src="{url}" width="100">')

    column_formatters = {'image': _list_thumbnail}

    form_extra_fields = {
        'image': form.ImageUploadField(
            'Изображение товара',
            base_path=os.path.join(file_path, 'static', 'media','products/'),
            url_relative_path='products/media/products/',
            namegen=generate_name,
            allowed_extensions=['jpg', 'jpeg', 'png', 'svg'],
            max_size=(1200, 780, True),
            thumbgen=(100, 100)
        )}

    def on_model_change(self, form, model, is_created):
        """Обрабатывает сохранение модели"""
        super().on_model_change(form, model, is_created)

        # Дополнительная обработка при создании
        if is_created:
            # Генерация slug на основе названия
            if not model.slug and model.name:
                model.slug = slugify(model.name)

    def create_form(self, obj=None):
        return super(ProductView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(ProductView, self).edit_form(obj)


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
                     'user': 'Пользователь'}

    form_columns = ['status', 'delivery_method', 'payment',
                    'address', 'first_name', 'last_name', 'phone_number', ]

    form_args = {
        'status': {'choices': AVAILABLE_STATUSES},

        'delivery_method': {'choices': [('delivery', 'Доставка'), ('pickup', 'Самовывоз')]},

        'payment': {'choices': [('card', 'Картой'), ('cash', 'Наличными')]}
    }

    edit_modal = True

    can_export = True
