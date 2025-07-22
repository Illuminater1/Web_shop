from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField


class UsersView(ModelView):
    AVAILABLE_ROLES = [('admin', 'Администратор'),
                       ('user', 'Пользователь'),
                       ('manager', 'Менеджер'),]

    form_overrides = {'role': SelectField, }

    column_list = ['role', 'id', 'username', 'email']

    column_labels = {'id': 'ID',
                     'username': 'Имя',
                     'email': 'Email',
                     'role': 'Роль', }

    form_columns = ['role', 'username', 'email']

    form_args = {'role': {'choices': AVAILABLE_ROLES}, 'coerce': str}

    column_filters = ['role', 'email', 'username']

    edit_modal = True


class ProductView(ModelView):
    column_labels = {'name': 'Название',
                     'slug': 'Ссылка',
                     'description': 'Описание',
                     'image': 'Изображение',
                     'stocks': 'Остаток',
                     'price': 'Цена',
                     }


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
