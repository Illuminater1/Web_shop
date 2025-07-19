import re

from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, validators, TelField, TextAreaField, ValidationError


class OrderForm(FlaskForm):
    first_name = StringField("Имя*:", render_kw={"class": "form-control"})

    last_name = StringField("Фамилия*:", render_kw={"class": "form-control"})

    phone_number = TelField("Номер телефона*:", render_kw={"class": "form-control"})

    delivery_method = RadioField("Способ доставки: ", render_kw={"class": "form-check-input"},
                                 choices=[('delivery', 'Нужна доставка'), ('pickup', 'Самовывоз')], default='delivery')

    address = TextAreaField("Адрес доставки:  ", render_kw={"class": "form-control",
                                                            "placeholder": "Введите адрес для доставки"}, )

    pay_method = RadioField("Способ оплаты:  ", render_kw={"class": "form-check-input"},
                            choices=[('card', 'Картой онлайн'), ('cash', 'Оплата при получении')], default='card')

    create_order = SubmitField("Оформить заказ", render_kw={"class": "btn btn-primary"})


    def validate_phone_number(self):
        data = self.phone_number

        if not data.isdigit():
            raise ValidationError("Нормер телефона должен содержать только цифры")

        pattern = re.compile(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
        if not re.match(data, pattern):
            raise ValidationError("Неверный формат номера")
