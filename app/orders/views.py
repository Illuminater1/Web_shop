from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError


from app.db import db
from app.carts.models import Cart
from app.orders.models import Order, OrderedProduct
from app.carts.forms import CartForm
from app.orders.forms import OrderForm

blueprint = Blueprint('order', __name__, url_prefix='/order')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def preview_orders():
    user = current_user.id
    cart_form = CartForm()
    order_form = OrderForm()

    user_carts = get_user_carts(user)
    amount = user_carts['amount']
    total_product = user_carts['total_product']
    cart_items = user_carts['cart_items']

    return render_template('orders/order.html',
                           content='Заказ',
                           cart_items=cart_items,
                           form=cart_form,
                           order_form=order_form,
                           total=total_product,
                           amount=amount)


def get_user_carts(user):
    user_carts = Cart.query.filter_by(user_id=user).all()

    amount = 0
    total_product = 0
    for item in user_carts:
        total_product += int(item.quantity)
        amount += item.product.price * item.quantity

    return {"amount": amount, "total_product": total_product, "cart_items": user_carts}


@blueprint.route('/process-order', methods=['GET', 'POST'])
@login_required
def create_order():
    order_form = OrderForm()
    cart_form = CartForm()
    user = current_user.id
    cart_items = get_user_carts(user)["cart_items"]

    if not cart_items:
        flash("Ваша корзина пуста")
        return redirect(url_for('cart.cart'))

    if order_form.validate_on_submit():

        for cart_item in cart_items:
            if cart_item.product.stocks < cart_item.quantity:
                flash(
                    f"Недостаточное количество товара {cart_item.product.name} на складе, в наличии {cart_item.product.quantity}")
                return redirect(url_for('cart.cart'))

        try:
            order = Order(
                user_id=user,
                first_name=order_form.first_name.data,
                last_name=order_form.last_name.data,
                phone_number=order_form.phone_number.data,
                delivery_method=order_form.delivery_method.data,
                address=order_form.address.data,
                payment=order_form.pay_method.data,
            )
            db.session.add(order)


            for cart_item in cart_items:
                product = cart_item.product
                ordered_product = OrderedProduct(
                    name=product.name,
                    product_id=cart_item.product.id,
                    quantity=cart_item.quantity,
                    price=product.price,
                    order=order
                )
                db.session.add(ordered_product)
                product.stocks -= cart_item.quantity

                db.session.delete(cart_item)

            db.session.commit()
            flash("Заказ успешно оформлен!")
            return redirect(url_for("main.index"))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Произошла ошибка при оформлении заказа: {str(e)}")
            return redirect(url_for('cart.cart'))

    else:
        return render_template("orders/order.html",
                               order_form=order_form,
                               cart_items=cart_items,
                               form=cart_form)

