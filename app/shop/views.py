from flask import render_template, Blueprint
from app.shop.models import Product

blueprint = Blueprint('shop', __name__, url_prefix='/shop', template_folder='templates/shop')




@blueprint.route("/")
def shop():
    page_title = 'Магазин'
    products_list = Product.query.order_by(Product.id).all()
    return render_template('shop/shop.html',
                           page_title=page_title, products=products_list, contetn="Товары")



@blueprint.route('/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    title = f"Страница продукта {product.slug}"
    content = 'Страничка продукта'
    return render_template('shop/product.html',
                           page_title=title, content=content, product=product)
