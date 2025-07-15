from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired


class CartForm(FlaskForm):

    submit_increase = SubmitField("+", render_kw={"class": "btn btn-primary btn-sm"})

    submit_decrease = SubmitField("-", render_kw= {"class": "btn btn-primary btn-sm"})


