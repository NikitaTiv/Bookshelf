from flask import Blueprint, render_template

from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_page():
    title = 'Панель управления'
    return render_template('admin/admin.html', page_title=title)
