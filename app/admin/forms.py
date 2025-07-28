from flask import current_app
from flask_admin.form import SecureForm
from app.shop.models import Category
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, IntegerField, TextAreaField, FloatField, FileField
from wtforms.validators import DataRequired
import secrets
from PIL import Image
import os


class CreateProduct(SecureForm):
    name = StringField('Название', validators=[DataRequired()])

    description = TextAreaField('Описание')

    stocks = IntegerField('В наличии', validators=[DataRequired()])

    price = FloatField('Цена')

    # category = SelectField('Категория', choices=[(str(c.id), c.name) for c in Category.query.all()])

    image = FileField('Загрузите файл', validators=[
                                                FileRequired(),
                                                FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Только изображения!')])


def save_file(form, file_field):

    random_hex = secrets.token_hex(8)
    name, ext = os.path.splitext(file_field.filename)
    img_name = f"{random_hex}{ext.lower()}"

    upload_dir  = os.path.join(current_app.root_path, 'static', 'products', form.name.data)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, img_name)

    file_field.data.save(file_path)

    try:
        img = Image.open(file_field.data)
        img.thumbnail((500, 500))
        img.save(file_path)

        return f"products/{img_name}"

    except:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise ValueError(f"Ошибка обработки изображения")
