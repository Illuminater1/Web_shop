from flask import Blueprint, flash, redirect, url_for, render_template


blueprint = Blueprint('cart', __name__, url_prefix='/cart',
                      template_folder='templates/cart')


@blueprint.route("/", methods=['GET'])
def cart():
    title = 'Корзина'
    content = 'Корзина'

    return render_template('carts/cart.html', page_title=title, content=content)



@blueprint.route("/", methods=['GET', 'POST'])
def add_to_cart():
    pass
