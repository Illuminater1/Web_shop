from flask_login import current_user, login_required
from flask import Blueprint, flash, redirect, url_for, render_template, request

from app.shop.models import Product, OrderedProduct
from app.db import db
from app.carts.models import Cart

blueprint = Blueprint('cart', __name__, url_prefix='/cart',
                      template_folder='templates/cart')


@blueprint.route("/", methods=['GET'])
def cart():
    if current_user.is_anonymous:
        flash("Пожалуйста авторизуйтесь")
        return redirect(url_for('user.login'))
    user_cart = Cart.query.filter_by(user_id=current_user.id).all()

    total = 0
    for item in user_cart:
        total += item.product.price * item.quantity

    return render_template('carts/cart.html', page_title="Корзина", total=total)


def get_user_cart(user_id):
    pass


@blueprint.route("/add/<int:product_id>", methods=['GET','POST'])
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    quantity = request.form.get('quantity', 1)

    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash(f"Товар {product.name} добавлен в корзину")
    return redirect(request.referrer or url_for('shop.shop', product_id=product_id))

@blueprint.route("/update", methods=['POST'])
def update_cart():
    pass


@blueprint.route("/remove", methods=['POST'])
def remove_from_cart():
    pass
