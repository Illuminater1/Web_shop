from flask_admin.contrib.sqla import ModelView

from app.orders.forms import OrderForm
from wtforms import SelectField


class UsersView(ModelView):
    column_display_pk = True
    column_list = ['id',
                   'username',
                   'email',
                   'role']

    form_columns = ['username',
                    'email',
                    'role']

    column_labels = {'id': 'ID',
                     'username': 'Имя',
                     'email': 'Email',
                     'role': 'Роль', }


class ProductView(ModelView):
    column_labels = {'name': 'Название',
                     'slug': 'Ссылка',
                     'description': 'Описание',
                     'image': 'Изображение',
                     'stocks': 'Остаток',
                     'price': 'Цена',
                     }


class OrdersView(ModelView):
    form_overrides = {'status': SelectField,
        'delivery_method': SelectField,
        'payment': SelectField
    }



    column_list = ['first_name', 'last_name', 'phone_number', 'delivery_method',
                   'address','status', 'payment', 'user_id', 'created_time', 'user']

    column_labels = {'first_name': 'Имя',
                     'last_name': 'Фамилия',
                     'phone_number': 'Телефон',
                     'delivery_method': 'Доставка',
                     'address': 'Адрес',
                     'status': 'Статус заказа',
                     'payment': 'Оплата',
                     'user_id': 'user_ID',
                     'created_time': 'Время создания',
                     'user': 'Пользователь'
                     }

    form_columns = ['status', 'delivery_method', 'payment',
        'address', 'first_name', 'last_name', 'phone_number',]

    form_args = {
        'status': {
            'choices': OrderForm.AVAILABLE_STATUSES
        },
        'delivery_method': {
            'choices': [('delivery', 'Доставка'), ('pickup', 'Самовывоз')]
        },
        'payment': {
            'choices': [('card', 'Картой'), ('cash', 'Наличными')]
        }
    }


    can_export = True

