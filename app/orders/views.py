from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user

from app.shop.models import Product, Category
from app.carts.models import Cart
from app.carts.forms import CartForm



blueprint = Blueprint('order', __name__, url_prefix='/order')


@blueprint.route('/create-order', methods=['GET','POST'])
def create_order():
    user = current_user.id
    form = CartForm()
    cart_items = Cart.query.filter_by(user_id=user).all()

    amount = 0
    total_product = 0
    for item in cart_items:
        total_product += int(item.quantity)
        amount += item.product.price * item.quantity

    return render_template('orders/create_order.html', content='Заказ', cart_items=cart_items,
                           form=form, total=total_product, amount=amount)