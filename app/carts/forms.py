from flask_wtf import FlaskForm
from wtforms import SubmitField


class CartForm(FlaskForm):

    submit_increase = SubmitField("+", render_kw={"class": "btn btn-primary btn-sm"})

    submit_decrease = SubmitField("-", render_kw= {"class": "btn btn-primary btn-sm"})

    submit_order = SubmitField("Оформить заказ", render_kw={"class": "btn btn-primary"})


