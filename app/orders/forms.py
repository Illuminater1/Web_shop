import re

from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, IntegerField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length


class OrderForm(FlaskForm):

    first_name = StringField("Имя*:",
                             validators=[DataRequired(message="Введите имя")],
                             render_kw={"class": "form-control"})

    last_name = StringField("Фамилия*:",
                            validators=[DataRequired(message="Введите фамилию")],
                            render_kw={"class": "form-control"})

    phone_number = StringField("Номер телефона*:",
                            validators=[DataRequired()],
                            render_kw={"class": "form-control", "placeholder": "+7XXXXXXXXXX"})

    delivery_method = RadioField("Способ доставки:",
                                 render_kw={"class": "form-check-input"},
                                 choices=[('delivery', 'Нужна доставка'),
                                          ('pickup', 'Самовывоз')],
                                 default='delivery')

    address = TextAreaField("Адрес доставки:",
                            render_kw={"class": "form-control",
                                        "placeholder": "Введите адрес для доставки"}, )

    pay_method = RadioField("Способ оплаты:",
                            render_kw={"class": "form-check-input"},
                            choices=[('card', 'Картой онлайн'),
                                     ('cash', 'Оплата при получении')],
                            default='card')

    create_order = SubmitField("Оформить заказ",
                               render_kw={"class": "btn btn-primary"})


    def validate_phone_number(self, field):
        data = field.data

        pattern = re.compile(r'^(?:\+7|8)\d{10}$')
        if not re.match(pattern, data):
            raise ValidationError("Неверный формат номера")

    def validate_first_name(self, field):
        data = field.data.strip()
        if not data.isalpha():
            raise ValidationError("Недопустимые символы, имя должно содержать только буквы")


    def validate_last_name(self, field):
        data = field.data.strip()
        if not data.isalpha():
            raise ValidationError("Недопустимые символы, фамилия должна содержать только буквы")

    def __init__(self, default_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if default_name:
            self.name.data = default_name