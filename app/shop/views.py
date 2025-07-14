from flask import render_template, Blueprint
from app.shop.models import Product

blueprint = Blueprint('shop', __name__, url_prefix='/shop', template_folder='templates/shop')




@blueprint.route("/")
def shop():
    page_title = 'Магазин'
    products_list = Product.query.order_by(Product.id).all()
    return render_template('shop/shop.html',
                           page_title=page_title, products=products_list, contetn="Товары")



# @blueprint.route('/<product_id>')
# def product():
#     products_list = Product.query.order_by(Product.id).all
#     title = f"Страница продукта {products_list['id']}"
#     content = 'Страничка продукта'
#     return render_template('shop/product.html',
#                            page_title=title, content=content)
