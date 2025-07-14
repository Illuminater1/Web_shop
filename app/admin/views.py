from flask import Blueprint, render_template

from app.user.decorators import admin_required
from flask_login import current_user, login_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = 'Админ'
    content = "Страница для админа"
    return render_template("admin/index.html", page_title=title, content=content)
