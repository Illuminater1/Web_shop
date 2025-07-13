from flask import Blueprint, render_template

blueprint = Blueprint("product", __name__, url_prefix='/product')


@blueprint.route('/<product_id>')
def product():
    title = f"Страница продукта {product_list['id']}"
    content = 'Страничка продукта'
    return render_template('product/card.html',
                           page_title=title, content=content)


