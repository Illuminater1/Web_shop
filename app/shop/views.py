from flask import render_template, Blueprint

blueprint = Blueprint('shop', __name__, url_prefix='/shop', template_folder='templates/shop')




@blueprint.route("/")
def shop():
    page_title = 'Магазин'
    content = 'Страница магазина'
    products = product_list
    return render_template('shop/shop.html',
                           page_title=page_title, content=content, products=products)
