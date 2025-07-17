from flask import render_template, Blueprint

from app.shop.models import Product

blueprint = Blueprint('shop', __name__, url_prefix='/shop', template_folder='templates/shop')




@blueprint.route("/")
def shop():
    page_title = 'Магазин'
    products_list = Product.query.order_by(Product.id).all()
    return render_template('shop/shop.html',
                           page_title=page_title, products=products_list, content="Товары")



@blueprint.route('/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    title = f"Страница продукта {product.slug}"
    content = 'Страничка продукта'
    return render_template('shop/product.html',
                           page_title=title, content=content, product=product)



@blueprint.route('/cat/<int:category_id>')
def select_category(category_id):
    if category_id == 0:
        products_list = Product.query.order_by(Product.id).all()
        return render_template('shop/shop.html',
                               products=products_list, content="Товары")

    else:
        products_list = Product.query.filter_by(category_id=category_id).order_by(Product.id).all()

    return render_template('shop/shop.html',
                           page_title=f'Товары категории да', products=products_list)

