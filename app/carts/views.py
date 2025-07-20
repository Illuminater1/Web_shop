from flask_login import current_user, login_required
from flask import Blueprint, flash, redirect, url_for, render_template, request

from app.db import db
from app.carts.models import Cart
from app.carts.forms import CartForm

blueprint = Blueprint('cart', __name__, url_prefix='/cart',
                      template_folder='templates/cart')


@blueprint.route("/", methods=['GET', 'POST'])
def cart():
    if current_user.is_anonymous:
        flash("Пожалуйста авторизуйтесь")
        return redirect(url_for('user.login'))
    user_cart = Cart.query.filter_by(user_id=current_user.id).all()

    form = CartForm()
    amount = 0
    total = 0
    for item in user_cart:
        total += int(item.quantity)
        amount += item.product.price * item.quantity

    return render_template('carts/cart.html', cart_items=user_cart,
                           amount=amount, form=form, total=total)


def get_cart_item(product_id):
    try:
        cart_item = Cart.query.filter_by(user_id=current_user.id,
                                     product_id=product_id).first()
        return cart_item
    except:
        return flash('Товар не найден')




@blueprint.route("/add/<int:product_id>", methods=['POST'])
@login_required
def add_to_cart(product_id):
    cart_item = get_cart_item(product_id)

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id,
                         product_id=product_id,
                         quantity=1)
        db.session.add(cart_item)
        db.session.commit()
        flash(f"Товар {cart_item.product.name} добавлен в корзину")
        return redirect(request.referrer or url_for('shop.shop', product_id=product_id))

    db.session.commit()
    flash(f"Количество {cart_item.product.name} увеличено")
    return redirect(request.referrer or url_for('shop.shop', product_id=product_id))



@blueprint.route("/remove/<int:product_id>", methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart_item = get_cart_item(product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        flash (f"Количество {cart_item.product.name} уменьшено")
    else:
        product_name = cart_item.product.name
        db.session.delete(cart_item)
        flash (f"Товар {product_name} удалён из корзины")

    db.session.commit()
    return redirect(request.referrer or url_for('shop.shop'))




@blueprint.route("/delete/<int:product_id>", methods=['POST'])
@login_required
def delete_product(product_id):
    cart_item = get_cart_item(product_id)

    if cart_item:
        product_name = cart_item.product.name
        db.session.delete(cart_item)
        db.session.commit()
        flash(f"Товар {product_name} удалён из корзины")

    else:
        flash("Такого товара нет в вашей корзине")
    return redirect(request.referrer or url_for('shop.shop'))


