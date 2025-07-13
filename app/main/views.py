from flask import render_template, Blueprint

blueprint = Blueprint('main', __name__)


@blueprint.route("/", methods=['POST', 'GET'])
def index():
    page_title = 'Главная страница'
    content = 'Главная страница'
    return render_template('main/index.html',
                           page_title=page_title, content=content)


@blueprint.route("/about")
def about():
    page_title = 'О нас'
    content = 'Страница о нас'
    return render_template('main/about.html',
                           page_title=page_title, content=content)


@blueprint.route("/contacts")
def contacts():
    page_title = 'Контакты'
    content = 'Страница с контактами'
    return render_template('main/contacts.html',
                           page_title=page_title, content=content)


@blueprint.route("/questions")
def questions():
    page_title = 'Вопросы'
    content = 'Страница с вопросами'
    return render_template('main/questions.html',
                           page_title=page_title, content=content)
