from flask import Blueprint, render_template

blueprint = Blueprint("product", __name__, url_prefix='/product')


@blueprint.route('/')
def product():
    title = "Страница продукта"
    content = 'Страничка продукта'
    return render_template('product/card.html',
                           page_title=title, content=content)

