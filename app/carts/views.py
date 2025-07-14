from app.shop.models import Product, OrderedProduct
from app.user.models import User

from flask import Blueprint, flash, redirect, url_for, render_template

blueprint = Blueprint('cart', __name__, url_prefix='/cart',
                      template_folder='templates/cart')


@blueprint.route("/", methods=['GET'])
def cart():
    title = 'Корзина'
    content = 'Корзина'

    return render_template('carts/cart.html', page_title=title, content=content)


def get_user_cart(user_id):
    pass


@blueprint.route("/add", methods=['GET', 'POST'])
def add_to_cart():
    product =Product.query.get(product_id)


@blueprint.route("/update", methods=['GET', 'POST'])
def update_cart():
    pass


@blueprint.route("/remove", methods=['GET', 'POST'])
def remove_from_cart():
    pass
